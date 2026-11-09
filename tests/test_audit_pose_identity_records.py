"""Stored identity/rank declarations retain the public model's value contract."""

import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError

DATA = Path(__file__).resolve().parents[1] / 'devguide/validation/data/audit'
KINDS = ['standalone', 'docking', 'scored_collection']
IDS = ['pose_id', 'partner_state_id', 'receptor_state_id']


def _records(kind):
    filename = (
        'minimal_vina_result.json' if kind == 'docking' else 'minimal_scored_pose.json'
    )
    record = json.loads((DATA / filename).read_text())
    if kind == 'standalone':
        return record, record, dmt.audit_pose
    if kind == 'scored_collection':
        record = dmt.DockingResult([dmt.DockingPose.from_dict(record)]).to_dict()
    return record, record['poses'][0], dmt.audit_result


@pytest.mark.parametrize('kind', KINDS)
@pytest.mark.parametrize('rank', [True, False, 0, -1, 1.0, '1', [], np.array([1, 2])])
def test_invalid_current_rank_is_reported_without_coercion(kind, rank):
    record, pose, audit = _records(kind)
    pose['rank'] = rank
    before = repr(record)
    report = audit(record)
    assert report['status'] == 'inconsistent'
    assert any(
        check['status'] == 'inconsistent' and check['path'].endswith('/rank')
        for check in report['checks']
    )
    assert repr(record) == before
    with pytest.raises(ArgumentError):
        dmt.DockingPose.from_dict(pose)


@pytest.mark.parametrize('kind', KINDS)
@pytest.mark.parametrize('field', IDS)
@pytest.mark.parametrize('value', [1, True, [], {}, np.array(['a', 'b'])])
def test_invalid_current_identity_is_bounded_and_field_specific(kind, field, value):
    record, pose, audit = _records(kind)
    pose[field] = value
    before = repr(record)
    report = audit(record)
    assert report['status'] == 'inconsistent'
    assert any(
        check['status'] == 'inconsistent' and check['path'].endswith('/' + field)
        for check in report['checks']
    )
    assert repr(record) == before
    with pytest.raises(ArgumentError):
        dmt.DockingPose.from_dict(pose)


@pytest.mark.parametrize(
    'field,value',
    [
        ('rank', True),
        ('rank', 1.0),
        ('rank', -1),
        ('rank', np.array([1, 2])),
        ('pose_id', 1),
        ('pose_id', []),
        ('pose_id', np.array(['a', 'b'])),
        ('partner_state_id', True),
        ('receptor_state_id', {}),
    ],
)
def test_malformed_history_is_rejected_before_relational_comparison(field, value):
    record, _, audit = _records('docking')
    record['provenance']['ranking_history'][0]['input_order'][0][field] = value
    before = repr(record)
    report = audit(record)
    assert report['status'] == 'inconsistent'
    assert repr(record) == before
    with pytest.raises(ArgumentError):
        dmt.DockingResult.from_dict(record)


@pytest.mark.parametrize('field', IDS)
def test_coordinated_malformed_ids_do_not_become_valid_evidence(field):
    record, pose, audit = _records('docking')
    pose[field] = 1
    record['provenance']['ranking_history'][-1]['input_order'][0][field] = 1
    assert audit(record)['status'] == 'inconsistent'


@pytest.mark.parametrize('kind', KINDS)
def test_numpy_integral_rank_preserves_the_valid_report(kind):
    record, pose, audit = _records(kind)
    pose['rank'] = 1
    baseline = audit(record)
    pose['rank'] = np.int64(pose['rank'])
    assert audit(record) == baseline
    assert type(dmt.DockingPose.from_dict(pose).rank) is int


@pytest.mark.parametrize('collection', [False, True])
@pytest.mark.parametrize('field', ['rank', *IDS])
def test_unknown_optional_declarations_remain_unknown(collection, field):
    pose = dmt.DockingPose(
        puw.quantity([[1, 2, 3]], 'nm'),
        rank=1,
        pose_id='pose',
        partner_state_id='partner',
        receptor_state_id='receptor',
    )
    setattr(pose, field, None)
    wire = pose.to_dict()
    record = dmt.DockingResult([pose]).to_dict() if collection else wire
    before = deepcopy(record)
    report = (dmt.audit_result if collection else dmt.audit_pose)(record)
    assert report['status'] == 'incomplete'
    assert dmt.DockingPose.from_dict(wire).to_dict()[field] is None
    assert record == before


@pytest.mark.parametrize('field', IDS)
@pytest.mark.parametrize('value', ['', ' ', ' padded '])
def test_existing_string_content_admission_is_not_tightened(field, value):
    _, pose, _ = _records('standalone')
    pose[field] = value
    assert dmt.DockingPose.from_dict(pose).to_dict()[field] == value


def test_unknown_historical_identity_and_rank_are_not_invented():
    record, _, audit = _records('docking')
    record = dmt.DockingResult.from_dict(record).to_dict()
    pose = record['poses'][0]
    history = record['provenance']['ranking_history'][-1]
    for field in ['rank', *IDS]:
        history['input_order'][0][field] = None
    for field in IDS:
        pose[field] = None
    before = deepcopy(record)
    assert audit(record)['status'] == 'incomplete'
    assert dmt.DockingResult.from_dict(record).to_dict() == record
    assert record == before


def test_identity_allocation_failure_keeps_its_native_exception():
    failure = MemoryError('identity allocation control')

    class Record(dict):
        def get(self, key, default=None):
            if key == 'pose_id':
                raise failure
            return super().get(key, default)

    record, _, audit = _records('standalone')
    with pytest.raises(MemoryError) as caught:
        audit(Record(record))
    assert caught.value is failure
