"""Audit the Vina adapter against the official 1IEP ligand molecular source.

The input files are distributed by AutoDock Vina. RDKit is needed to read the
source SDF before converting its molecular graph to MolSysMT. See
devguide/validation/1iep_external_pdbqt.md for pinned downloads and limits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

import dockingmt
from dockingmt.engines.vina import _pdbqt_atom_records
from dockingmt.preparation._molsys import autodock_element

INPUT_SHA256 = {
    'receptor': 'f13cf3b36f61d87c3b58983e0b8ecf1c3456a685eb86dfe9ccfb139c7bdc2586',
    'partner': '15fb35648d8c18c70317842f3a0631b73a19429c710a037ab07310084d579bb8',
    'source_ligand': '051b8742c32adc05c07fb486a4e7c9327f84e131cee33ac4e6a568d07553eb38',
}
NEAR_NATIVE_CUTOFF_ANGSTROM = 2.5


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def _source_atom_map(
    pdbqt_records: list[tuple[tuple[str, ...], np.ndarray]],
    source_coordinates: np.ndarray,
    source_elements: list[str],
) -> list[int]:
    """Verify the positional atom map for this pinned bound-ligand example.

    Coordinates are used only to identify the official, already aligned 1IEP
    source and prepared input. Other PDBQT inputs need an explicit source map.
    """
    if source_coordinates.shape != (len(source_elements), 3):
        raise ValueError('The source ligand coordinates and elements disagree.')
    if not np.isfinite(source_coordinates).all():
        raise ValueError('The source ligand has non-finite coordinates.')
    mapping: list[int] = []
    for key, coordinate in pdbqt_records:
        element = autodock_element(key[2])
        distances = np.linalg.norm(source_coordinates - coordinate, axis=1)
        matches = [
            index
            for index, distance in enumerate(distances)
            if source_elements[index].upper() == element.upper() and distance <= 0.02
        ]
        if len(matches) != 1 or matches[0] in mapping:
            raise ValueError('The PDBQT atom has no unique source ligand atom.')
        mapping.append(matches[0])
    return mapping


def _displaced_control_box(
    reference_box: dockingmt.BoxRegion, source_coordinates: np.ndarray
) -> dockingmt.BoxRegion:
    """Place a control box 30 Å away and prove it excludes the native ligand."""
    center = np.asarray(puw.get_value(reference_box.center, to_unit='angstrom'))
    control = dockingmt.BoxRegion(
        center=puw.quantity(center + np.array([30.0, 0.0, 0.0]), 'angstrom'),
        size=reference_box.size,
    )
    if any(
        control.contains(puw.quantity(coordinate, 'angstrom'))
        for coordinate in source_coordinates
    ):
        raise ValueError('The displaced control box overlaps the native ligand.')
    return control


def _pose_metrics(
    result: dockingmt.DockingResult,
    reference: np.ndarray,
    heavy_indices: list[int],
) -> list[dict[str, Any]]:
    poses = []
    for pose in result.poses:
        coordinates = np.asarray(puw.get_value(pose.coordinates, to_unit='angstrom'))
        differences = coordinates[heavy_indices] - reference[heavy_indices]
        positional_rmsd = float(np.sqrt(np.mean(np.sum(differences**2, axis=1))))
        poses.append(
            {
                'rank': pose.rank,
                'vina_score_kcal_per_mol': pose.scores['vina'],
                'heavy_atom_positional_rmsd_angstrom': positional_rmsd,
            }
        )
    return poses


def run_case(
    receptor_path: Path,
    ligand_path: Path,
    ligand_source_path: Path,
    manifest_path: Path,
    control_manifest_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    """Run the pinned 1IEP case and one displaced-search-domain control."""
    from rdkit import Chem

    paths = (
        receptor_path,
        ligand_path,
        ligand_source_path,
        manifest_path,
        control_manifest_path,
        report_path,
    )
    if len({path.resolve() for path in paths}) != len(paths):
        raise ValueError('Input, manifest, and report paths must be distinct.')

    for role, path in (
        ('receptor', receptor_path),
        ('partner', ligand_path),
        ('source_ligand', ligand_source_path),
    ):
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != INPUT_SHA256[role]:
            raise ValueError(f'The {role} file does not match the pinned 1IEP input.')

    ligand_records = _pdbqt_atom_records(ligand_path.read_text())
    source_molecules = list(Chem.SDMolSupplier(str(ligand_source_path), removeHs=False))
    if len(source_molecules) != 1 or source_molecules[0] is None:
        raise ValueError('The pinned source SDF must contain one valid ligand.')
    source = msm.convert(source_molecules[0], to_form='molsysmt.MolSys')
    source_bonds = int(msm.get(source, n_bonds=True))
    if source_bonds != source_molecules[0].GetNumBonds():
        raise ValueError(
            'The source ligand graph lost bonds during MolSysMT conversion.'
        )
    source_coordinates = np.asarray(
        puw.get_value(
            msm.get(source, element='atom', coordinates=True), to_unit='angstrom'
        )[0]
    )
    source_elements = list(
        msm.get(
            source,
            element='atom',
            atom_type=True,
            chemical_state='structure',
            structure_indices=0,
        )
    )
    source_indices = _source_atom_map(
        ligand_records, source_coordinates, source_elements
    )
    reference = source_coordinates[source_indices]
    heavy_indices = [
        index
        for index, source_index in enumerate(source_indices)
        if source_elements[source_index].upper() != 'H'
    ]
    if (
        len(source_elements) != 69
        or len(ligand_records) != 40
        or len(heavy_indices) != 37
    ):
        raise ValueError('The pinned 1IEP source-to-PDBQT atom inventory has changed.')

    box = dockingmt.BoxRegion(
        center=puw.quantity([15.190, 53.903, 16.917], 'angstrom'),
        size=puw.quantity([20.0, 20.0, 20.0], 'angstrom'),
    )
    if not all(
        box.contains(puw.quantity(coordinate, 'angstrom'))
        for coordinate in source_coordinates
    ):
        raise ValueError('The reference box does not contain the native ligand.')
    control_box = _displaced_control_box(box, source_coordinates)
    protocol = dockingmt.VinaProtocol(
        exhaustiveness=1,
        n_poses=5,
        seed=42,
        cpu=1,
        capture_backend_inputs=True,
    )
    runs = {}
    for name, search_box, output in (
        ('reference', box, manifest_path),
        ('displaced_box_control', control_box, control_manifest_path),
    ):
        problem = dockingmt.DockingProblem(
            receptor=receptor_path,
            partner=ligand_path,
            search_domain=search_box,
        )
        result = dockingmt.dock(problem, protocol=protocol, backend='vina')
        artifacts = result.provenance['backend_artifacts']
        for role in ('receptor', 'partner'):
            if artifacts[role]['sha256'] != INPUT_SHA256[role]:
                raise ValueError(f'Vina did not receive the pinned {role} PDBQT.')
        _write_json(output, result.to_dict())
        runs[name] = (result, _pose_metrics(result, reference, heavy_indices))

    result, poses = runs['reference']
    control_result, control_poses = runs['displaced_box_control']
    if any(
        pose['heavy_atom_positional_rmsd_angstrom'] <= NEAR_NATIVE_CUTOFF_ANGSTROM
        for pose in control_poses
    ):
        raise ValueError('The displaced-box control generated a near-native pose.')
    artifacts = result.provenance['backend_artifacts']
    report = {
        'schema_version': '1.1',
        'case': 'Official AutoDock Vina 1IEP prepared PDBQT pair',
        'assessment': 'external_preparation_unassessed',
        'source_commit': '3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645',
        'input_sha256': INPUT_SHA256,
        'submitted_sha256': {
            role: artifacts[role]['sha256'] for role in ('receptor', 'partner')
        },
        'protocol': protocol.to_dict(),
        'backend_box': result.provenance['backend_box'],
        'versions': {
            'dockingmt': dockingmt.__version__,
            'molsysmt': msm.__version__,
            'vina': result.provenance['backend_version'],
        },
        'source_revision': {
            'git_head': subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip(),
            'worktree_dirty': bool(
                subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=Path(__file__).resolve().parents[1],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip()
            ),
        },
        'metric_definition': (
            'Mapped heavy PDBQT atoms against the original SDF ligand converted '
            'to MolSysMT; no alignment or symmetry correction.'
        ),
        'source_ligand_form': 'rdkit.Chem.Mol -> molsysmt.MolSys',
        'n_source_atoms': len(source_elements),
        'n_source_bonds': source_bonds,
        'pdbqt_to_source_atom_indices': source_indices,
        'omitted_source_atom_indices': sorted(
            set(range(len(source_elements))) - set(source_indices)
        ),
        'n_partner_atoms': len(ligand_records),
        'n_heavy_partner_atoms': len(heavy_indices),
        'n_poses': len(poses),
        'poses': poses,
        'displaced_box_control': {
            'purpose': 'methodological negative control for search-domain placement',
            'offset_angstrom': [30.0, 0.0, 0.0],
            'reference_atom_overlap': False,
            'near_native_cutoff_angstrom': NEAR_NATIVE_CUTOFF_ANGSTROM,
            'near_native_pose_count': 0,
            'backend_box': control_result.provenance['backend_box'],
            'submitted_sha256': {
                role: control_result.provenance['backend_artifacts'][role]['sha256']
                for role in ('receptor', 'partner')
            },
            'manifest_sha256': hashlib.sha256(
                control_manifest_path.read_bytes()
            ).hexdigest(),
            'n_poses': len(control_poses),
            'poses': control_poses,
        },
    }
    _write_json(report_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receptor', type=Path, required=True)
    parser.add_argument('--ligand', type=Path, required=True)
    parser.add_argument('--ligand-source', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--control-manifest', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    run_case(
        args.receptor,
        args.ligand,
        args.ligand_source,
        args.manifest,
        args.control_manifest,
        args.report,
    )


if __name__ == '__main__':
    main()
