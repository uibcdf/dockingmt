"""Record and replay one exploratory 181L redocking regression case.

Usage:
    python devtools/redocking_181l.py record --manifest /tmp/181l-manifest.json
    python devtools/redocking_181l.py replay --manifest /tmp/181l-manifest.json --report /tmp/181l-report.json
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import platform
import subprocess
from pathlib import Path
from typing import Any

import molsysmt as msm
import pyunitwizard as puw

import dockingmt

NEAR_NATIVE_ANGSTROM = 2.5
SCORE_TOLERANCE = 0.05
RMSD_TOLERANCE_ANGSTROM = 0.25


def _source_revision() -> dict[str, Any]:
    """Identify the development checkout used by this bounded benchmark."""
    root = Path(__file__).resolve().parents[1]
    code_digest = hashlib.sha256()
    code_files = sorted([*root.joinpath('dockingmt').rglob('*.py'), Path(__file__)])
    for path in code_files:
        code_digest.update(path.relative_to(root).as_posix().encode())
        code_digest.update(path.read_bytes())
    head = subprocess.run(
        ['git', 'rev-parse', 'HEAD'],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    )
    return {
        'git_head': head,
        'worktree_dirty': dirty,
        'code_sha256': code_digest.hexdigest(),
    }


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def _verify_captured_inputs(artifacts: dict[str, Any]) -> dict[str, int]:
    """Reject a manifest whose retained PDBQT differs from its recorded digest."""
    sizes = {}
    for role in ('receptor', 'partner'):
        artifact = artifacts.get(role)
        if not isinstance(artifact, dict) or artifact.get('format') != 'pdbqt':
            raise ValueError(f'The {role} PDBQT artifact is missing or invalid.')
        encoded = artifact.get('content_base64')
        if not isinstance(encoded, str):
            raise ValueError(f'The {role} PDBQT input bytes were not captured.')
        try:
            content = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError(f'The {role} PDBQT input bytes are invalid.') from exc
        if hashlib.sha256(content).hexdigest() != artifact.get('sha256'):
            raise ValueError(f'The {role} PDBQT input bytes failed SHA-256 validation.')
        sizes[role] = len(content)
    return sizes


def record_manifest(path: Path) -> dict[str, Any]:
    """Run the provisional file-backed case and save its complete result."""
    source = Path(msm.systems['T4 lysozyme L99A']['181l.pdb']).resolve()
    problem = dockingmt.DockingProblem.for_redocking(
        complex_system=source,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
        padding=puw.quantity(8.0, 'angstrom'),
        metadata={'pdb_id': '181L', 'ligand_name': 'BNZ'},
    )
    protocol = dockingmt.VinaProtocol(
        exhaustiveness=1,
        n_poses=5,
        seed=42,
        cpu=1,
        allow_provisional_preparation=True,
        capture_backend_inputs=True,
    )
    result = dockingmt.dock(problem, protocol=protocol, backend='vina')
    manifest = result.to_dict()
    _verify_captured_inputs(manifest['provenance']['backend_artifacts'])
    manifest['benchmark_source_revision'] = _source_revision()
    _write_json(path, manifest)
    return manifest


def _summarize(result: dockingmt.DockingResult, reference: Any) -> dict[str, Any]:
    """Report every mapped pose without assigning scientific validity."""
    poses = []
    for pose in result.poses:
        rmsd = float(puw.get_value(pose.get_rmsd(reference), to_unit='angstrom'))
        poses.append(
            {
                'rank': pose.rank,
                'pose_id': pose.pose_id,
                'rmsd_angstrom': rmsd,
                'scores': dict(pose.scores),
                'partner_state_id': pose.partner_state_id,
                'receptor_state_id': pose.receptor_state_id,
            }
        )
    near_native = [
        pose['rank'] for pose in poses if pose['rmsd_angstrom'] <= NEAR_NATIVE_ANGSTROM
    ]
    vina_scores = [pose['scores']['vina'] for pose in poses]
    return {
        'n_poses': len(poses),
        'poses': poses,
        'near_native_rank': min(near_native) if near_native else None,
        'vina_score_range': [min(vina_scores), max(vina_scores)]
        if vina_scores
        else None,
        'failure_mode': 'no_poses'
        if not poses
        else 'no_near_native_pose'
        if not near_native
        else None,
    }


def _compare(
    recorded: dockingmt.DockingResult,
    replay: dockingmt.DockingResult,
    reference: Any,
) -> dict[str, Any]:
    """Compare two seeded runs with explicit numeric and identity tolerances."""
    problem_match = recorded.problem_info == replay.problem_info
    protocol_match = recorded.protocol_info == replay.protocol_info
    input_hashes_match = all(
        recorded.problem_info['molecular_inputs'][role]['source_fingerprint']
        == replay.problem_info['molecular_inputs'][role]['source_fingerprint']
        for role in ('receptor', 'partner')
    )
    pdbqt_hashes_match = (
        recorded.provenance['backend_artifacts']
        == replay.provenance['backend_artifacts']
    )
    software_versions_match = all(
        recorded.provenance.get(field) == replay.provenance.get(field)
        for field in ('backend_version', 'dockingmt_version', 'molsysmt_version')
    )
    pose_count_match = len(recorded) == len(replay)
    has_poses = len(recorded) > 0
    identity_match = pose_count_match and all(
        first.metadata.get('source_atom_keys')
        == second.metadata.get('source_atom_keys')
        and first.rank == second.rank
        and first.pose_id == second.pose_id
        and first.partner_state_id == second.partner_state_id
        and first.receptor_state_id == second.receptor_state_id
        for first, second in zip(recorded.poses, replay.poses)
    )
    score_deltas = []
    pose_rmsd_deltas = []
    reference_rmsd_deltas = []
    if identity_match:
        for first, second in zip(recorded.poses, replay.poses):
            if first.scores.keys() != second.scores.keys():
                identity_match = False
                break
            score_deltas.extend(
                abs(first.scores[name] - second.scores[name]) for name in first.scores
            )
            pose_rmsd_deltas.append(
                float(puw.get_value(first.get_rmsd(second), to_unit='angstrom'))
            )
            reference_rmsd_deltas.append(
                abs(
                    float(puw.get_value(first.get_rmsd(reference), to_unit='angstrom'))
                    - float(
                        puw.get_value(second.get_rmsd(reference), to_unit='angstrom')
                    )
                )
            )
    max_score_delta = max(score_deltas, default=0.0)
    max_pose_rmsd = max(pose_rmsd_deltas, default=0.0)
    max_reference_rmsd_delta = max(reference_rmsd_deltas, default=0.0)
    within_tolerance = (
        input_hashes_match
        and problem_match
        and protocol_match
        and pdbqt_hashes_match
        and software_versions_match
        and pose_count_match
        and has_poses
        and identity_match
        and max_score_delta <= SCORE_TOLERANCE
        and max_pose_rmsd <= RMSD_TOLERANCE_ANGSTROM
        and max_reference_rmsd_delta <= RMSD_TOLERANCE_ANGSTROM
    )
    return {
        'within_tolerance': within_tolerance,
        'input_hashes_match': input_hashes_match,
        'problem_match': problem_match,
        'protocol_match': protocol_match,
        'pdbqt_hashes_match': pdbqt_hashes_match,
        'software_versions_match': software_versions_match,
        'pose_count_match': pose_count_match,
        'has_poses': has_poses,
        'identity_match': identity_match,
        'max_score_delta': max_score_delta,
        'max_pose_coordinate_rmsd_angstrom': max_pose_rmsd,
        'max_reference_rmsd_delta_angstrom': max_reference_rmsd_delta,
        'score_tolerance': SCORE_TOLERANCE,
        'rmsd_tolerance_angstrom': RMSD_TOLERANCE_ANGSTROM,
    }


def replay_manifest(manifest_path: Path, report_path: Path) -> dict[str, Any]:
    """Load a saved result, rerun its recorded configuration, and write a report."""
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    recorded = dockingmt.DockingResult.from_dict(manifest)
    captured_sizes = _verify_captured_inputs(recorded.provenance['backend_artifacts'])
    problem = recorded.reconstruct_problem()
    protocol = dockingmt.VinaProtocol.from_dict(recorded.protocol_info)
    if recorded.provenance.get('backend') != 'vina':
        raise ValueError('The recorded backend is not Vina.')
    if not protocol.allow_provisional_preparation:
        raise ValueError('The 181L exploratory replay needs its recorded opt-in.')
    if not protocol.capture_backend_inputs:
        raise ValueError('The 181L replay needs its recorded PDBQT capture policy.')
    replay = dockingmt.dock(problem, protocol=protocol, backend='vina')
    reference = problem.partner_molsys
    comparison = _compare(recorded, replay, reference)
    recorded_revision = manifest.get('benchmark_source_revision')
    replayed_revision = _source_revision()
    comparison['source_revision_match'] = recorded_revision == replayed_revision
    comparison['within_tolerance'] &= comparison['source_revision_match']
    report = {
        'schema_version': '1.0',
        'case': 'T4 lysozyme L99A / benzene / PDB 181L',
        'assessment': 'exploratory_provisional_preparation',
        'metric_definition': {
            'rmsd': 'Mapped retained ligand atoms; no superposition',
            'near_native_cutoff_angstrom': NEAR_NATIVE_ANGSTROM,
            'score': 'Named Vina output in kcal/mol',
        },
        'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
        'source_revision': {
            'recorded': recorded_revision,
            'replayed': replayed_revision,
        },
        'versions': {
            'python': platform.python_version(),
            'dockingmt': dockingmt.__version__,
            'molsysmt': msm.__version__,
            'vina_recorded': recorded.provenance['backend_version'],
            'vina_replayed': replay.provenance['backend_version'],
        },
        'problem': recorded.problem_info,
        'protocol': recorded.protocol_info,
        'backend_artifacts': {
            role: {
                'format': artifact['format'],
                'sha256': artifact['sha256'],
                'captured_bytes': captured_sizes[role],
            }
            for role, artifact in recorded.provenance['backend_artifacts'].items()
        },
        'recorded': _summarize(recorded, reference),
        'replayed': _summarize(replay, reference),
        'comparison': comparison,
    }
    _write_json(report_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('record', 'replay'))
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.action == 'record':
        record_manifest(args.manifest)
        return
    if args.report is None:
        parser.error('--report is required for replay')
    report = replay_manifest(args.manifest, args.report)
    if not report['comparison']['within_tolerance']:
        raise SystemExit('Replay differs from the recorded run; inspect the report.')


if __name__ == '__main__':
    main()
