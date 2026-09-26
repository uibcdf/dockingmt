"""Protect 1IEP replay input authentication and measured comparisons."""

import base64

import numpy as np
import pytest
import pyunitwizard as puw

from devtools.replay_1iep_pdbqt import _compare_run, _decode_source
from devtools.validate_1iep_pdbqt import INPUT_SHA256, UPSTREAM_COMMIT
from dockingmt import DockingPose, DockingResult


def _result(*, score=-7.0, x=0.0, protocol=None, pose=True):
    poses = (
        [
            DockingPose(
                coordinates=puw.quantity([[x, 0.0, 0.0]], 'angstrom'),
                scores={'vina': score},
                rank=1,
                pose_id='pose-1',
                metadata={'pose_atom_order': 'verified_pdbqt_order'},
            )
        ]
        if pose
        else []
    )
    return DockingResult(
        poses=poses,
        problem_info={
            'receptor': '/original/receptor.pdbqt',
            'partner': '/original/ligand.pdbqt',
            'search_domain': {'box': [1, 2, 3]},
        },
        protocol_info=protocol or {'seed': 42},
        provenance={
            'backend_artifacts': {'receptor': 'same', 'partner': 'same'},
            'backend_box': {'center': [1, 2, 3]},
            'backend_version': '1.2.7',
            'dockingmt_version': 'test',
            'molsysmt_version': 'test',
        },
    )


def test_1iep_replay_accepts_relocated_identical_results():
    recorded = _result()
    replayed = _result()
    replayed.problem_info['receptor'] = '/temporary/receptor.pdbqt'
    replayed.problem_info['partner'] = '/temporary/ligand.pdbqt'

    comparison = _compare_run(recorded, replayed, np.zeros((1, 3)), [0])

    assert comparison['within_tolerance'] is True
    assert comparison['max_score_delta_kcal_per_mol'] == 0.0
    assert comparison['max_pose_coordinate_rmsd_angstrom'] == 0.0


@pytest.mark.parametrize(
    ('change', 'expected'),
    [
        ({'score': -6.9}, 'max_score_delta_kcal_per_mol'),
        ({'x': 0.3}, 'max_pose_coordinate_rmsd_angstrom'),
        ({'protocol': {'seed': 43}}, 'protocol_match'),
        ({'pose': False}, 'pose_count_match'),
    ],
)
def test_1iep_replay_detects_run_drift(change, expected):
    comparison = _compare_run(_result(), _result(**change), np.zeros((1, 3)), [0])

    assert comparison['within_tolerance'] is False
    if expected.endswith('_match'):
        assert comparison[expected] is False
    else:
        assert comparison[expected] > 0.05


def test_1iep_replay_requires_a_pose():
    comparison = _compare_run(
        _result(pose=False), _result(pose=False), np.zeros((1, 3)), [0]
    )

    assert comparison['pose_count_match'] is True
    assert comparison['has_poses'] is False
    assert comparison['within_tolerance'] is False


def test_1iep_replay_rejects_corrupt_source_bytes():
    source = {
        'format': 'sdf',
        'sha256': INPUT_SHA256['source_ligand'],
        'upstream_commit': UPSTREAM_COMMIT,
        'content_base64': base64.b64encode(b'changed SDF').decode('ascii'),
    }

    with pytest.raises(ValueError, match='failed SHA-256 validation'):
        _decode_source(source)
