"""Replay the public 1IEP reference and displaced-box control from manifests.

The original receptor, ligand, and SDF paths are not needed. Both Vina PDBQT
inputs and the reference SDF are authenticated and recovered from the records.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import io
import json
import platform
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

import dockingmt
from devtools.redocking_181l import (
    RMSD_TOLERANCE_ANGSTROM,
    SCORE_TOLERANCE,
    _verify_captured_inputs,
)
from devtools.validate_1iep_pdbqt import (
    INPUT_SHA256,
    NEAR_NATIVE_CUTOFF_ANGSTROM,
    UPSTREAM_COMMIT,
    _displaced_control_box,
    _pose_metrics,
    _recorded_protocol,
    _reference_box,
    _source_atom_map,
    _source_revision,
    _write_json,
)
from dockingmt.engines.vina import _pdbqt_atom_records


def _decode_source(source: dict[str, Any]) -> bytes:
    """Validate the captured original SDF against its pinned public identity."""
    if (
        source.get('format') != 'sdf'
        or source.get('sha256') != INPUT_SHA256['source_ligand']
        or source.get('upstream_commit') != UPSTREAM_COMMIT
    ):
        raise ValueError('The recorded source ligand identity is invalid.')
    encoded = source.get('content_base64')
    if not isinstance(encoded, str):
        raise ValueError('The source ligand SDF bytes were not captured.')
    try:
        content = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError('The source ligand SDF bytes are invalid.') from exc
    if hashlib.sha256(content).hexdigest() != INPUT_SHA256['source_ligand']:
        raise ValueError('The source ligand SDF failed SHA-256 validation.')
    return content


def _load_record(path: Path) -> tuple[dict[str, Any], dockingmt.DockingResult, bytes]:
    content = path.read_bytes()
    manifest = json.loads(content)
    recorded = dockingmt.DockingResult.from_dict(manifest)
    if recorded.provenance.get('backend') != 'vina':
        raise ValueError('The recorded backend is not Vina.')
    if (
        recorded.protocol_info != _recorded_protocol().to_dict()
        or recorded.provenance.get('protocol') != recorded.protocol_info
    ):
        raise ValueError('The recorded Vina protocol differs from the pinned case.')
    artifacts = recorded.provenance.get('backend_artifacts')
    if not isinstance(artifacts, dict):
        raise ValueError('The recorded PDBQT artifacts are missing.')
    _verify_captured_inputs(artifacts)
    for role in ('receptor', 'partner'):
        if artifacts[role]['sha256'] != INPUT_SHA256[role]:
            raise ValueError(
                f'The captured {role} PDBQT differs from the pinned input.'
            )
        source_fingerprint = (
            recorded.problem_info.get('molecular_inputs', {})
            .get(role, {})
            .get('source_fingerprint')
        )
        if source_fingerprint != {'kind': 'file', 'sha256': INPUT_SHA256[role]}:
            raise ValueError(f'The recorded {role} source fingerprint is invalid.')
    source = manifest.get('benchmark_source')
    if not isinstance(source, dict):
        raise ValueError('The source ligand evidence is missing from the manifest.')
    _decode_source(source)
    return manifest, recorded, content


def _source_reference(
    source: dict[str, Any], partner_pdbqt: bytes
) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """Rebuild the known ligand and verify the recorded 1IEP atom map."""
    from rdkit import Chem

    content = _decode_source(source)
    molecules = list(Chem.ForwardSDMolSupplier(io.BytesIO(content), removeHs=False))
    if len(molecules) != 1 or molecules[0] is None:
        raise ValueError('The captured SDF must contain one valid ligand.')
    molsys = msm.convert(molecules[0], to_form='molsysmt.MolSys')
    n_atoms = int(msm.get(molsys, n_atoms=True))
    n_bonds = int(msm.get(molsys, n_bonds=True))
    if (
        n_atoms != source.get('n_atoms')
        or n_bonds != source.get('n_bonds')
        or n_atoms != 69
        or n_bonds != 73
    ):
        raise ValueError('The captured molecular graph differs from the pinned source.')
    coordinates = np.asarray(
        puw.get_value(
            msm.get(molsys, element='atom', coordinates=True), to_unit='angstrom'
        )[0]
    )
    elements = list(
        msm.get(
            molsys,
            element='atom',
            atom_type=True,
            chemical_state='structure',
            structure_indices=0,
        )
    )
    records = _pdbqt_atom_records(partner_pdbqt.decode('utf-8'))
    mapping = _source_atom_map(records, coordinates, elements)
    if mapping != source.get('pdbqt_to_source_atom_indices'):
        raise ValueError(
            'The recorded source-to-PDBQT atom map differs from the source.'
        )
    heavy_indices = [
        index
        for index, source_index in enumerate(mapping)
        if elements[source_index].upper() != 'H'
    ]
    if len(mapping) != 40 or len(heavy_indices) != 37:
        raise ValueError('The pinned source-to-PDBQT atom inventory has changed.')
    return coordinates, coordinates[mapping], heavy_indices


def _problem_semantics(problem_info: dict[str, Any]) -> dict[str, Any]:
    """Ignore only the temporary filenames used to restage identical PDBQT."""
    return {
        key: value
        for key, value in problem_info.items()
        if key not in ('receptor', 'partner')
    }


def _compare_run(
    recorded: dockingmt.DockingResult,
    replayed: dockingmt.DockingResult,
    reference: np.ndarray,
    heavy_indices: list[int],
) -> dict[str, Any]:
    """Compare one recorded/replayed Vina run with explicit tolerances."""
    if any(
        pose.n_atoms != len(reference) for pose in [*recorded.poses, *replayed.poses]
    ):
        raise ValueError('A recorded or replayed pose has the wrong atom count.')
    problem_match = _problem_semantics(recorded.problem_info) == _problem_semantics(
        replayed.problem_info
    )
    protocol_match = recorded.protocol_info == replayed.protocol_info
    backend_inputs_match = (
        recorded.provenance['backend_artifacts']
        == replayed.provenance['backend_artifacts']
    )
    backend_box_match = recorded.provenance.get(
        'backend_box'
    ) == replayed.provenance.get('backend_box')
    versions_match = all(
        recorded.provenance.get(field) == replayed.provenance.get(field)
        for field in ('backend_version', 'dockingmt_version', 'molsysmt_version')
    )
    pose_count_match = len(recorded) == len(replayed)
    has_poses = len(recorded) > 0
    identity_match = pose_count_match and all(
        first.rank == second.rank
        and first.pose_id == second.pose_id
        and first.partner_state_id == second.partner_state_id
        and first.receptor_state_id == second.receptor_state_id
        and first.metadata == second.metadata
        and first.metadata.get('pose_atom_order') == 'verified_pdbqt_order'
        and first.scores.keys() == second.scores.keys()
        and first.n_atoms == second.n_atoms == len(reference)
        for first, second in zip(recorded.poses, replayed.poses)
    )
    recorded_metrics = _pose_metrics(recorded, reference, heavy_indices)
    replayed_metrics = _pose_metrics(replayed, reference, heavy_indices)
    score_deltas = []
    pose_rmsds = []
    reference_rmsd_deltas = []
    if identity_match:
        for first, second, first_metric, second_metric in zip(
            recorded.poses, replayed.poses, recorded_metrics, replayed_metrics
        ):
            score_deltas.extend(
                abs(first.scores[name] - second.scores[name]) for name in first.scores
            )
            first_coords = np.asarray(
                puw.get_value(first.coordinates, to_unit='angstrom')
            )
            second_coords = np.asarray(
                puw.get_value(second.coordinates, to_unit='angstrom')
            )
            pose_rmsds.append(
                float(
                    np.sqrt(
                        np.mean(np.sum((first_coords - second_coords) ** 2, axis=1))
                    )
                )
            )
            reference_rmsd_deltas.append(
                abs(
                    first_metric['heavy_atom_positional_rmsd_angstrom']
                    - second_metric['heavy_atom_positional_rmsd_angstrom']
                )
            )
    max_score_delta = max(score_deltas, default=0.0)
    max_pose_rmsd = max(pose_rmsds, default=0.0)
    max_reference_rmsd_delta = max(reference_rmsd_deltas, default=0.0)
    within_tolerance = (
        problem_match
        and protocol_match
        and backend_inputs_match
        and backend_box_match
        and versions_match
        and pose_count_match
        and has_poses
        and identity_match
        and max_score_delta <= SCORE_TOLERANCE
        and max_pose_rmsd <= RMSD_TOLERANCE_ANGSTROM
        and max_reference_rmsd_delta <= RMSD_TOLERANCE_ANGSTROM
    )
    return {
        'within_tolerance': within_tolerance,
        'problem_match': problem_match,
        'protocol_match': protocol_match,
        'backend_inputs_match': backend_inputs_match,
        'backend_box_match': backend_box_match,
        'versions_match': versions_match,
        'pose_count_match': pose_count_match,
        'has_poses': has_poses,
        'identity_match': identity_match,
        'max_score_delta_kcal_per_mol': max_score_delta,
        'max_pose_coordinate_rmsd_angstrom': max_pose_rmsd,
        'max_reference_rmsd_delta_angstrom': max_reference_rmsd_delta,
        'score_tolerance_kcal_per_mol': SCORE_TOLERANCE,
        'rmsd_tolerance_angstrom': RMSD_TOLERANCE_ANGSTROM,
        'recorded_poses': recorded_metrics,
        'replayed_poses': replayed_metrics,
    }


def replay_pair(
    manifest_path: Path, control_manifest_path: Path, report_path: Path
) -> dict[str, Any]:
    """Verify and rerun both pinned cases without their original source paths."""
    if (
        len(
            {
                path.resolve()
                for path in (manifest_path, control_manifest_path, report_path)
            }
        )
        != 3
    ):
        raise ValueError('Manifest and report paths must be distinct.')
    reference_manifest, reference_result, reference_bytes = _load_record(manifest_path)
    control_manifest, control_result, control_bytes = _load_record(
        control_manifest_path
    )
    if reference_manifest['benchmark_source'] != control_manifest['benchmark_source']:
        raise ValueError(
            'The two manifests cite different source ligands or atom maps.'
        )
    recorded_revision = reference_manifest.get('benchmark_source_revision')
    replayed_revision = _source_revision()
    if (
        not isinstance(recorded_revision, dict)
        or recorded_revision != control_manifest.get('benchmark_source_revision')
        or recorded_revision != replayed_revision
    ):
        raise ValueError('The recorded and replayed source revisions differ.')
    reference_artifacts = reference_result.provenance['backend_artifacts']
    if reference_artifacts != control_result.provenance['backend_artifacts']:
        raise ValueError('The two runs used different PDBQT inputs.')
    if reference_result.protocol_info != control_result.protocol_info:
        raise ValueError('The two runs used different Vina protocols.')
    partner_pdbqt = base64.b64decode(
        reference_artifacts['partner']['content_base64'], validate=True
    )
    receptor_pdbqt = base64.b64decode(
        reference_artifacts['receptor']['content_base64'], validate=True
    )
    source_coordinates, reference, heavy_indices = _source_reference(
        reference_manifest['benchmark_source'], partner_pdbqt
    )
    expected_boxes = {
        'reference': _reference_box(),
        'displaced_box_control': _displaced_control_box(
            _reference_box(), source_coordinates
        ),
    }
    records = {'reference': reference_result, 'displaced_box_control': control_result}
    for name, recorded in records.items():
        if recorded.problem_info.get('search_domain') != expected_boxes[name].to_dict():
            raise ValueError(f'The {name} search domain differs from the pinned case.')
    if not all(
        expected_boxes['reference'].contains(puw.quantity(point, 'angstrom'))
        for point in source_coordinates
    ):
        raise ValueError(
            'The recorded reference box does not contain the source ligand.'
        )

    comparisons = {}
    with TemporaryDirectory() as directory:
        receptor_path = Path(directory) / 'receptor.pdbqt'
        partner_path = Path(directory) / 'partner.pdbqt'
        receptor_path.write_bytes(receptor_pdbqt)
        partner_path.write_bytes(partner_pdbqt)
        for name, recorded in records.items():
            problem = recorded.reconstruct_problem(
                receptor=receptor_path, partner=partner_path
            )
            protocol = dockingmt.VinaProtocol.from_dict(recorded.protocol_info)
            replayed = dockingmt.dock(problem, protocol=protocol, backend='vina')
            comparisons[name] = _compare_run(
                recorded, replayed, reference, heavy_indices
            )
    for name in records:
        comparison = comparisons[name]
        recorded_near_native = sum(
            pose['heavy_atom_positional_rmsd_angstrom'] <= NEAR_NATIVE_CUTOFF_ANGSTROM
            for pose in comparison['recorded_poses']
        )
        replayed_near_native = sum(
            pose['heavy_atom_positional_rmsd_angstrom'] <= NEAR_NATIVE_CUTOFF_ANGSTROM
            for pose in comparison['replayed_poses']
        )
        comparison['near_native_count_match'] = (
            recorded_near_native == replayed_near_native
        )
        comparison['recorded_near_native_count'] = recorded_near_native
        comparison['replayed_near_native_count'] = replayed_near_native
        comparison['within_tolerance'] &= comparison['near_native_count_match']
    if (
        comparisons['reference']['recorded_near_native_count'] == 0
        or comparisons['displaced_box_control']['recorded_near_native_count'] != 0
    ):
        raise ValueError('The recorded reference/control classification is invalid.')
    report = {
        'schema_version': '1.0',
        'case': 'Official AutoDock Vina 1IEP reference and displaced-box control',
        'assessment': 'external_preparation_unassessed',
        'manifest_sha256': {
            'reference': hashlib.sha256(reference_bytes).hexdigest(),
            'displaced_box_control': hashlib.sha256(control_bytes).hexdigest(),
        },
        'source_ligand_sha256': INPUT_SHA256['source_ligand'],
        'source_revision': recorded_revision,
        'python_version': platform.python_version(),
        'near_native_cutoff_angstrom': NEAR_NATIVE_CUTOFF_ANGSTROM,
        'runs': comparisons,
        'within_tolerance': all(
            comparison['within_tolerance'] for comparison in comparisons.values()
        ),
    }
    _write_json(report_path, report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--control-manifest', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    report = replay_pair(args.manifest, args.control_manifest, args.report)
    if not report['within_tolerance']:
        raise SystemExit('Replay differs from the recorded runs; inspect the report.')


if __name__ == '__main__':
    main()
