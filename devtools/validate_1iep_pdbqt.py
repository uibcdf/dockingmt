"""Audit the Vina adapter with the official externally prepared 1IEP PDBQT pair.

The input files are distributed by AutoDock Vina. See
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

INPUT_SHA256 = {
    'receptor': 'f13cf3b36f61d87c3b58983e0b8ecf1c3456a685eb86dfe9ccfb139c7bdc2586',
    'partner': '15fb35648d8c18c70317842f3a0631b73a19429c710a037ab07310084d579bb8',
}


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def run_case(
    receptor_path: Path,
    ligand_path: Path,
    manifest_path: Path,
    report_path: Path,
) -> dict[str, Any]:
    """Run one bounded adapter check with pinned external PDBQT inputs."""
    for role, path in (('receptor', receptor_path), ('partner', ligand_path)):
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != INPUT_SHA256[role]:
            raise ValueError(f'The {role} PDBQT does not match the pinned 1IEP input.')

    ligand_records = _pdbqt_atom_records(ligand_path.read_text())
    reference = np.asarray([xyz for _, xyz in ligand_records])
    heavy_indices = [
        index
        for index, (key, _) in enumerate(ligand_records)
        if key[2] not in ('H', 'HD')
    ]
    if len(ligand_records) != 40 or not heavy_indices:
        raise ValueError('The pinned 1IEP ligand atom records are incomplete.')

    box = dockingmt.BoxRegion(
        center=puw.quantity([15.190, 53.903, 16.917], 'angstrom'),
        size=puw.quantity([20.0, 20.0, 20.0], 'angstrom'),
    )
    problem = dockingmt.DockingProblem(
        receptor=receptor_path,
        partner=ligand_path,
        search_domain=box,
    )
    protocol = dockingmt.VinaProtocol(
        exhaustiveness=1,
        n_poses=5,
        seed=42,
        cpu=1,
        capture_backend_inputs=True,
    )
    result = dockingmt.dock(problem, protocol=protocol, backend='vina')
    artifacts = result.provenance['backend_artifacts']
    for role in ('receptor', 'partner'):
        if artifacts[role]['sha256'] != INPUT_SHA256[role]:
            raise ValueError(f'Vina did not receive the pinned {role} PDBQT.')
    _write_json(manifest_path, result.to_dict())

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
    report = {
        'schema_version': '1.0',
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
            'Identity-ordered heavy PDBQT atoms against the prepared bound ligand; '
            'no alignment or symmetry correction.'
        ),
        'n_partner_atoms': len(ligand_records),
        'n_heavy_partner_atoms': len(heavy_indices),
        'n_poses': len(poses),
        'poses': poses,
    }
    _write_json(report_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receptor', type=Path, required=True)
    parser.add_argument('--ligand', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    run_case(args.receptor, args.ligand, args.manifest, args.report)


if __name__ == '__main__':
    main()
