"""Protect 1IEP replay input authentication and measured comparisons."""

import base64
from types import SimpleNamespace

import numpy as np
import pytest
import pyunitwizard as puw

from bindingmt import DockingPose, DockingResult
from bmt_test_support.replay_1iep_pdbqt import _compare_run, _decode_source
from bmt_test_support.validate_1iep_pdbqt import INPUT_SHA256, UPSTREAM_COMMIT


@pytest.mark.parametrize(
    'changed_helper', ['validate_1iep_pdbqt.py', 'replay_1iep_pdbqt.py']
)
def test_installed_1iep_attribution_tracks_actual_helpers_without_git(
    monkeypatch, tmp_path, changed_helper
):
    from bmt_test_support import redocking_181l, validate_1iep_pdbqt

    def forbidden(*args, **kwargs):
        raise AssertionError('Installed source attribution must not query Git.')

    monkeypatch.setattr(redocking_181l.subprocess, 'run', forbidden)
    identities = []
    for name in ('producer', 'receiver'):
        package = tmp_path / name / 'runtime' / 'bindingmt'
        helpers = tmp_path / name / 'support' / 'bmt_test_support'
        package.mkdir(parents=True)
        helpers.mkdir(parents=True)
        (package / '__init__.py').write_text('# imported runtime\n')
        for helper in (
            'redocking_181l.py',
            'validate_1iep_pdbqt.py',
            'replay_1iep_pdbqt.py',
        ):
            (helpers / helper).write_text('# retained ' + helper + '\n')
        monkeypatch.setattr(
            redocking_181l,
            'bindingmt',
            SimpleNamespace(__file__=str(package / '__init__.py')),
        )
        monkeypatch.setattr(
            redocking_181l, '__file__', str(helpers / 'redocking_181l.py')
        )
        monkeypatch.setattr(
            validate_1iep_pdbqt, '__file__', str(helpers / 'validate_1iep_pdbqt.py')
        )
        identities.append(validate_1iep_pdbqt._source_revision())
    first, second = identities
    assert first == second
    assert first['git_head'] is None and first['worktree_dirty'] is None
    assert first['shared_checkout'] is False
    assert first['code_scope'] == 'imported_bindingmt_core_redocking_and_1iep_helpers'

    (helpers / changed_helper).write_text('# changed receiving helper\n')
    changed = validate_1iep_pdbqt._source_revision()
    assert changed['code_sha256'] != first['code_sha256']


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
            'bindingmt_version': 'test',
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
