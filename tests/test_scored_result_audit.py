"""Saved scoring stages are checked without molecular or native operations."""

import builtins
import json
from copy import deepcopy
from pathlib import Path

import pytest

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError

DATA = Path(__file__).resolve().parents[1] / 'devguide/validation/data/audit'


@pytest.fixture
def docking_record():
    return json.loads((DATA / 'minimal_vina_result.json').read_text())


@pytest.fixture
def scored_pose():
    return json.loads((DATA / 'minimal_scored_pose.json').read_text())


@pytest.fixture
def collection(scored_pose):
    return dmt.DockingResult(poses=[dmt.DockingPose.from_dict(scored_pose)]).to_dict()


def test_valid_scored_pose_collection_does_not_invent_docking_stage(collection):
    report = dmt.audit_result(collection)
    assert report['status'] == 'incomplete'  # Collection provenance is unavailable.
    assert not any(c['status'] == 'inconsistent' for c in report['checks'])
    checks = [c for c in report['checks'] if c['check'] == 'evaluation_value']
    assert len(checks) == 16 and all(c['status'] == 'consistent' for c in checks)
    assert all(
        c['path'].startswith('/poses/0/metadata/scoring_history/') for c in checks
    )


@pytest.mark.parametrize(
    'history', [None, {}, 'invalid', [None], [{'schema_version': '99'}]]
)
def test_known_malformed_history_is_not_ignored(docking_record, history):
    docking_record['poses'][0]['metadata']['scoring_history'] = history
    report = dmt.audit_result(docking_record)
    assert report['status'] == 'inconsistent'
    assert any(
        c['status'] == 'inconsistent'
        and '/poses/0/metadata/scoring_history' in c['path']
        for c in report['checks']
    )


def test_optional_empty_history_does_not_change_docking_only_report(docking_record):
    before = dmt.audit_result(docking_record)
    docking_record['poses'][0]['metadata']['scoring_history'] = []
    assert dmt.audit_result(docking_record) == before


@pytest.mark.parametrize(
    'change', ['value', 'descriptor', 'state', 'duplicate', 'capture']
)
def test_scoring_contradictions_are_checked_inside_collection(collection, change):
    pose = collection['poses'][0]
    if change == 'value':
        pose['scores']['vina'] += 1
    elif change == 'descriptor':
        pose['metadata']['score_definitions']['vina']['context']['weights'][0] += 1
    elif change == 'state':
        pose['partner_state_id'] = 'different-state'
    elif change == 'duplicate':
        pose['metadata']['scoring_history'].append(
            deepcopy(pose['metadata']['scoring_history'][0])
        )
    else:
        pose['metadata']['scoring_history'][0]['backend_artifacts']['partner'][
            'sha256'
        ] = '0' * 64
    assert dmt.audit_result(collection)['status'] == 'inconsistent'


@pytest.mark.parametrize('change', ['history', 'capture'])
def test_missing_scoring_evidence_stays_incomplete(collection, change):
    pose = collection['poses'][0]
    if change == 'history':
        del pose['metadata']['scoring_history']
    else:
        del pose['metadata']['scoring_history'][0]['backend_artifacts']['partner'][
            'content_base64'
        ]
    report = dmt.audit_result(collection)
    assert report['status'] == 'incomplete'
    assert not any(c['status'] == 'inconsistent' for c in report['checks'])


def test_original_docking_score_cannot_be_relabelled_as_scoring(docking_record):
    docking_record['poses'][0]['metadata']['score_definitions']['vina']['context'][
        'stage'
    ] = 'scoring'
    assert dmt.audit_result(docking_record)['status'] == 'inconsistent'


def test_overlapping_docking_and_scoring_producers_are_inconsistent(
    docking_record, scored_pose
):
    docking_record['poses'][0]['metadata']['scoring_history'] = [
        deepcopy(scored_pose['metadata']['scoring_history'][0])
    ]
    report = dmt.audit_result(docking_record)
    assert report['status'] == 'inconsistent'
    assert any(
        c['reason'] == 'docking_and_scoring_ownership_overlap' for c in report['checks']
    )


def test_appended_stage_routes_additions_without_weakening_original_docking(
    docking_record, scored_pose
):
    # Synthetic record-only control, not an evaluation of the saved docking pose.
    pose = docking_record['poses'][0]
    evaluation = deepcopy(scored_pose['metadata']['scoring_history'][0])
    evaluation['score_name'] = 'rescored'
    for key in ('scores', 'score_definitions'):
        evaluation[key] = {
            name.replace('vina', 'rescored', 1): value
            for name, value in evaluation[key].items()
        }
    for role in ('partner', 'receptor'):
        evaluation['preparation'][role]['state_id'] = pose[f'{role}_state_id']
    pose['scores'].update(evaluation['scores'])
    pose['metadata']['score_definitions'].update(evaluation['score_definitions'])
    pose['metadata']['scoring_history'] = [evaluation]
    assert dmt.audit_result(docking_record)['status'] == 'consistent'
    pose['scores']['vina'] += 1
    assert dmt.audit_result(docking_record)['status'] == 'inconsistent'


def test_audit_does_not_relax_score_comparison_context(scored_pose):
    first = dmt.DockingPose.from_dict(scored_pose)
    changed = deepcopy(scored_pose)
    changed['metadata']['score_definitions']['vina']['context']['partner_sha256'] = (
        '0' * 64
    )
    result = dmt.DockingResult(poses=[first, dmt.DockingPose.from_dict(changed)])
    dmt.audit_result(result.to_dict())
    with pytest.raises(ArgumentError):
        result.rank_by('vina')


def test_collection_audit_is_detached_and_does_no_external_work(
    collection, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Record audit attempted external work.')

    for name in ('get', 'select', 'extract', 'convert', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    original_import = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name.split('.')[0] in (
            'molsysmt',
            'vina',
            'molsysviewer',
            'rdkit',
            'openmm',
        ):
            forbidden()
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded)
    monkeypatch.setattr(builtins, 'open', forbidden)
    before = deepcopy(collection)
    report = dmt.audit_result(collection)
    assert report == dmt.audit_result(collection)
    assert collection == before
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert 'content_base64' not in json.dumps(report)
    report['checks'][0]['status'] = 'changed'
    assert dmt.audit_result(collection)['checks'][0]['status'] != 'changed'
