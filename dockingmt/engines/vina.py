from __future__ import annotations

import os
import tempfile
import time
from pathlib import Path
from typing import Any

import depdigest
import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError, LibraryNotFoundError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol, VinaProtocol
from dockingmt.core.results import DockingPose, DockingResult
from dockingmt.engines.base import DockingBackend


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

        import vina

        # Extract search box parameters in Angstroms
        if hasattr(problem.search_domain, 'to_backend_box'):
            box = problem.search_domain.to_backend_box(unit='angstrom')
        else:
            box_approx = problem.search_domain.as_box_approximation()
            box = box_approx.to_backend_box(unit='angstrom')
        center = [float(c) for c in box['center']]
        box_size = [float(s) for s in box['size']]

        # Prepare receptor and partner representations
        temp_files_to_remove: list[str] = []

        try:
            receptor_file = self._resolve_receptor_path(
                problem.receptor, temp_files_to_remove
            )
            partner_file, partner_string = self._resolve_partner(
                problem.partner, temp_files_to_remove
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

                partner_state_id = problem.metadata.get('partner_state_id')
                receptor_state_id = problem.metadata.get('receptor_state_id')

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
                    )
                    poses.append(pose)

            provenance: dict[str, Any] = {
                'backend': self.name,
                'backend_version': getattr(vina, '__version__', 'unknown'),
                'protocol': protocol.to_dict(),
                'search_domain': problem.search_domain.to_dict(),
                'seed': protocol.seed,
                'elapsed_seconds': elapsed_seconds,
            }

            return DockingResult(
                poses=poses,
                problem_info=problem.to_dict(),
                protocol_info=protocol.to_dict(),
                provenance=provenance,
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
                f'Receptor must be a valid PDBQT file path or PDBQT string, '
                f'got {type(receptor).__name__}.'
            ),
        )

    def _resolve_partner(
        self, partner: Any, temp_files: list[str]
    ) -> tuple[str | None, str | None]:
        """Resolve partner input to either a filepath or a PDBQT string."""
        if isinstance(partner, (str, Path)):
            path_str = str(partner)
            if os.path.isfile(path_str):
                return path_str, None
            if 'ROOT' in path_str or 'ATOM' in path_str:
                return None, path_str

        raise ArgumentError(
            arg_name='problem.partner',
            reason=(
                f'Partner must be a valid PDBQT file path or PDBQT string, '
                f'got {type(partner).__name__}.'
            ),
        )
