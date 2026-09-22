from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path
from typing import Any

import depdigest
import molsysmt as msm
import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError, LibraryNotFoundError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol, VinaProtocol
from dockingmt.core.results import DockingPose, DockingResult
from dockingmt.engines.base import DockingBackend
from dockingmt.preparation import (
    PreparedLigand,
    PreparedReceptor,
    prepare_ligand,
    prepare_receptor,
)


def _pdbqt_atom_records(
    text: str,
) -> list[tuple[tuple[str, str, str], tuple[float, float, float]]]:
    """Read stable atom labels and rounded coordinates from Vina PDBQT text."""
    records = []
    for line in text.splitlines():
        if not line.startswith(('ATOM', 'HETATM')):
            continue
        try:
            key = (line[6:11].strip(), line[12:16].strip(), line.split()[-1])
            xyz = tuple(float(line[start : start + 8]) for start in (30, 38, 46))
        except (ValueError, IndexError) as exc:
            raise ArgumentError(
                arg_name='problem.partner',
                reason='Cannot read atom identity from a PDBQT ligand record.',
            ) from exc
        records.append((key, xyz))
    return records


def _verify_pose_atom_order(
    ligand_pdbqt: str, poses_pdbqt: str, coordinates: np.ndarray
) -> None:
    """Verify that Vina's coordinate arrays follow the supplied PDBQT atom order."""
    source = _pdbqt_atom_records(ligand_pdbqt)
    output = _pdbqt_atom_records(poses_pdbqt)
    expected = [record[0] for record in source]
    if (
        not source
        or len(set(expected)) != len(expected)
        or coordinates.ndim != 3
        or coordinates.shape[1:] != (len(source), 3)
        or len(output) != len(source) * len(coordinates)
    ):
        raise ArgumentError(
            arg_name='problem.partner',
            reason='Cannot verify the PDBQT source-to-pose atom map.',
        )
    for pose_index, pose_coordinates in enumerate(coordinates):
        records = output[pose_index * len(source) : (pose_index + 1) * len(source)]
        if [record[0] for record in records] != expected or not np.allclose(
            np.asarray([record[1] for record in records]),
            pose_coordinates,
            atol=0.001,
            rtol=0.0,
        ):
            raise ArgumentError(
                arg_name='problem.partner',
                reason='Vina pose atom order or coordinates differ from the supplied ligand PDBQT.',
            )


def _provisional_preparation_reasons(prepared: Any) -> list[str]:
    """Identify temporary chemistry assigned by DockingMT's preparation helpers."""
    if not isinstance(prepared, (PreparedLigand, PreparedReceptor)):
        return []
    metadata = prepared.metadata
    reasons = []
    if metadata.get('charge_source') == 'zero_placeholder':
        reasons.append('zero-placeholder partial charges')
    if 'heuristic' in str(metadata.get('atom_type_source', '')):
        reasons.append('heuristic AutoDock atom types')
    return reasons


class VinaBackend(DockingBackend):
    """DockingBackend adapter for AutoDock Vina.

    Isolates Vina execution behind standard DockingMT contracts. Handles
    conversion of search domains, invocation of Vina's C++ computational core,
    extraction of poses and affinity scores, and normalization into DockingResult.
    """

    def __init__(self) -> None:
        self._name = 'vina'
        self._capabilities = {
            'rigid_receptor',
            'small_molecule',
            'box_search',
            'scoring_vina',
            'scoring_vinardo',
            'scoring_ad4',
        }

    @property
    def name(self) -> str:
        """Name of the backend."""
        return self._name

    @property
    def capabilities(self) -> set[str]:
        """Set of capabilities advertised by AutoDock Vina."""
        return set(self._capabilities)

    @property
    def is_available(self) -> bool:
        """Whether the 'vina' package is installed and importable."""
        return depdigest.is_installed('vina')

    def dock(
        self,
        problem: DockingProblem,
        protocol: DockingProtocol | None = None,
    ) -> DockingResult:
        """Execute AutoDock Vina docking calculation.

        Parameters
        ----------
        problem : DockingProblem
            Scientific docking problem specification.
        protocol : DockingProtocol | None, optional
            Docking protocol configuration. If None, default VinaProtocol() is used.

        Returns
        -------
        DockingResult
            Normalized docking result containing poses, plural scores, and provenance.
        """
        if not self.is_available:
            raise LibraryNotFoundError(
                library='vina',
                hint='conda install vina -c conda-forge',
            )

        if protocol is None:
            protocol = VinaProtocol()

        # Validate capabilities and problem compatibility
        self.validate_capabilities(protocol)
        protocol.validate_problem(problem)

        if not isinstance(protocol, VinaProtocol):
            raise ArgumentError(
                arg_name='protocol',
                reason=f'VinaBackend requires a VinaProtocol instance, got {type(protocol).__name__}.',
            )

        # Extract search box parameters in Angstroms
        if hasattr(problem.search_domain, 'to_backend_box'):
            box = problem.search_domain.to_backend_box(unit='angstrom')
        else:
            box_approx = problem.search_domain.as_box_approximation()
            box = box_approx.to_backend_box(unit='angstrom')
        center = [float(c) for c in box['center']]
        box_size = [float(s) for s in box['size']]

        # Prepare selected MolSys inputs only at the backend boundary.
        receptor = problem.receptor
        partner = problem.partner
        receptor_mode = 'provided'
        partner_mode = 'provided'
        partner_selected_indices: list[int] | None = None
        partner_source_indices: list[int] | None = None
        partner_source_n_atoms: int | None = None
        if (
            not isinstance(receptor, PreparedReceptor)
            and problem.receptor_molsys is not None
        ):
            receptor = prepare_receptor(
                problem.receptor_molsys,
                selection='all',
                state_id=problem.metadata.get('receptor_state_id'),
            )
            receptor_mode = 'automatic'
        if (
            not isinstance(partner, PreparedLigand)
            and problem.partner_molsys is not None
        ):
            partner = prepare_ligand(
                problem.partner_molsys,
                selection='all',
                state_id=problem.metadata.get('partner_state_id'),
            )
            source_n_atoms = msm.get(
                problem.partner_molsys, element='system', n_atoms=True
            )
            retained = partner.metadata.get('retained_atom_indices')
            if (
                not isinstance(retained, list)
                or len(retained) != partner.n_atoms
                or len(set(retained)) != len(retained)
                or any(
                    not isinstance(i, int) or i < 0 or i >= source_n_atoms
                    for i in retained
                )
                or partner.metadata.get('atom_map_status')
                not in ('identity', 'hydrogen_subset_mapped')
            ):
                raise ArgumentError(
                    arg_name='problem.partner',
                    reason=(
                        'Vina preparation has no valid source-to-PDBQT atom map. '
                        'A verified source-to-pose atom map is required (dockingmt#8).'
                    ),
                )
            partner_selected_indices = retained
            partner_source_n_atoms = source_n_atoms
            if problem.partner_atom_indices is not None:
                partner_source_indices = [
                    problem.partner_atom_indices[i] for i in retained
                ]
            partner_mode = 'automatic'

        receptor_reasons = _provisional_preparation_reasons(receptor)
        partner_reasons = _provisional_preparation_reasons(partner)
        if not protocol.allow_provisional_preparation:
            for role, reasons in (
                ('receptor', receptor_reasons),
                ('partner', partner_reasons),
            ):
                if reasons:
                    raise ArgumentError(
                        arg_name=f'problem.{role}',
                        reason=(
                            f'Vina preparation would use {", ".join(reasons)}. '
                            'Provide chemically parameterized PDBQT input, or set '
                            'VinaProtocol(allow_provisional_preparation=True) for '
                            'exploratory docking only. See dockingmt#5 and '
                            'molsysmt#221/#222.'
                        ),
                    )

        preparation = {
            'receptor': {
                'mode': receptor_mode,
                'state_id': getattr(receptor, 'state_id', None),
                'metadata': getattr(receptor, 'metadata', None),
                'assessment': 'provisional' if receptor_reasons else 'unassessed',
                'provisional_reasons': receptor_reasons,
            },
            'partner': {
                'mode': partner_mode,
                'state_id': getattr(partner, 'state_id', None),
                'metadata': getattr(partner, 'metadata', None),
                'assessment': 'provisional' if partner_reasons else 'unassessed',
                'provisional_reasons': partner_reasons,
            },
        }

        # Prepare receptor and partner representations
        temp_files_to_remove: list[str] = []

        import vina

        try:
            receptor_file = self._resolve_receptor_path(receptor, temp_files_to_remove)
            partner_file, partner_string = self._resolve_partner(
                partner, temp_files_to_remove
            )

            # Initialize Vina engine
            v = vina.Vina(
                sf_name=protocol.scoring,
                cpu=protocol.cpu,
                seed=protocol.seed if protocol.seed is not None else 0,
                verbosity=0,
            )

            v.set_receptor(rigid_pdbqt_filename=receptor_file)

            if partner_file is not None:
                v.set_ligand_from_file(partner_file)
            elif partner_string is not None:
                v.set_ligand_from_string(partner_string)
            else:
                raise ArgumentError(
                    arg_name='problem.partner',
                    reason='Could not resolve partner representation to a file or PDBQT string.',
                )

            # Compute affinity maps
            v.compute_vina_maps(center=center, box_size=box_size)

            # Run global docking optimization
            start_time = time.time()
            v.dock(
                exhaustiveness=protocol.exhaustiveness,
                n_poses=protocol.n_poses,
            )
            elapsed_seconds = time.time() - start_time

            # Retrieve poses and scores
            energy_range_val = float(
                puw.get_value(puw.convert(protocol.energy_range, to_unit='kcal/mol'))
            )
            coords_arr = v.poses(
                n_poses=protocol.n_poses,
                energy_range=energy_range_val,
                coordinates_only=True,
            )
            energies_arr = v.energies(
                n_poses=protocol.n_poses,
                energy_range=energy_range_val,
            )

            poses: list[DockingPose] = []
            if coords_arr is not None and len(coords_arr) > 0:
                coords_np = np.asarray(coords_arr)
                energies_np = np.asarray(energies_arr)
                ligand_pdbqt = (
                    partner_string
                    if partner_string is not None
                    else Path(partner_file).read_text()
                )
                _verify_pose_atom_order(
                    ligand_pdbqt,
                    v.poses(
                        n_poses=protocol.n_poses,
                        energy_range=energy_range_val,
                        coordinates_only=False,
                    ),
                    coords_np,
                )
                if isinstance(partner, PreparedLigand) and (
                    coords_np.ndim != 3 or coords_np.shape[1:] != (partner.n_atoms, 3)
                ):
                    raise ArgumentError(
                        arg_name='problem.partner',
                        reason='Vina pose coordinates do not match the prepared ligand atom count; a verified atom map is required.',
                    )

                partner_state_id = getattr(
                    partner,
                    'state_id',
                    problem.metadata.get('partner_state_id'),
                )
                receptor_state_id = getattr(
                    receptor,
                    'state_id',
                    problem.metadata.get('receptor_state_id'),
                )

                for idx in range(len(coords_np)):
                    pose_coords = puw.quantity(coords_np[idx], 'angstrom')
                    row_e = energies_np[idx]
                    scores: dict[str, float] = {
                        protocol.scoring: float(row_e[0]),
                        'inter': float(row_e[1]),
                        'intra': float(row_e[2]),
                        'torsion': float(row_e[3]),
                    }
                    pose = DockingPose(
                        coordinates=pose_coords,
                        scores=scores,
                        rank=idx + 1,
                        pose_id=f'pose_{idx + 1}',
                        partner_state_id=partner_state_id,
                        receptor_state_id=receptor_state_id,
                        metadata={
                            'pose_atom_order': 'verified_pdbqt_order',
                            'prepared_atom_indices': list(range(partner.n_atoms)),
                            'selected_atom_indices': partner_selected_indices,
                            'source_atom_indices': partner_source_indices,
                            'selected_partner_n_atoms': partner_source_n_atoms,
                        }
                        if isinstance(partner, PreparedLigand)
                        else {
                            'pose_atom_order': 'verified_pdbqt_order',
                        },
                    )
                    poses.append(pose)

            provenance: dict[str, Any] = {
                'backend': self.name,
                'backend_version': getattr(vina, '__version__', 'unknown'),
                'protocol': protocol.to_dict(),
                'search_domain': problem.search_domain.to_dict(),
                'seed': protocol.seed,
                'elapsed_seconds': elapsed_seconds,
                'preparation': preparation,
            }

            return DockingResult(
                poses=poses,
                problem_info=problem.to_dict(),
                protocol_info=protocol.to_dict(),
                provenance=provenance,
                problem=problem,
            )

        finally:
            for temp_path in temp_files_to_remove:
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass

    def _resolve_receptor_path(self, receptor: Any, temp_files: list[str]) -> str:
        """Resolve receptor input to a filesystem path acceptable by Vina."""
        if hasattr(receptor, 'to_pdbqt'):
            pdbqt_str = receptor.to_pdbqt()
            tmp = tempfile.NamedTemporaryFile(suffix='.pdbqt', mode='w', delete=False)
            tmp.write(pdbqt_str)
            tmp.flush()
            tmp.close()
            temp_files.append(tmp.name)
            return tmp.name

        if isinstance(receptor, (str, Path)):
            path_str = str(receptor)
            if os.path.isfile(path_str):
                return path_str
            # Might be a raw PDBQT string
            if 'ATOM' in path_str or 'HETATM' in path_str:
                tmp = tempfile.NamedTemporaryFile(
                    suffix='.pdbqt', mode='w', delete=False
                )
                tmp.write(path_str)
                tmp.flush()
                tmp.close()
                temp_files.append(tmp.name)
                return tmp.name

        raise ArgumentError(
            arg_name='problem.receptor',
            reason=(
                f'Receptor must be a valid PreparedReceptor, PDBQT file path, or PDBQT string, '
                f'got {type(receptor).__name__}.'
            ),
        )

    def _resolve_partner(
        self, partner: Any, temp_files: list[str]
    ) -> tuple[str | None, str | None]:
        """Resolve partner input to either a filepath or a PDBQT string."""
        if hasattr(partner, 'to_pdbqt'):
            return None, partner.to_pdbqt()

        if isinstance(partner, (str, Path)):
            path_str = str(partner)
            if os.path.isfile(path_str):
                return path_str, None
            if 'ROOT' in path_str or 'ATOM' in path_str:
                return None, path_str

        raise ArgumentError(
            arg_name='problem.partner',
            reason=(
                f'Partner must be a valid PreparedLigand, PDBQT file path, or PDBQT string, '
                f'got {type(partner).__name__}.'
            ),
        )
