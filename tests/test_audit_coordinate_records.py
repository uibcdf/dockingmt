"""Offline audits and pose readers agree on the existing xyz wire contract."""

import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError

DATA = Path(__file__).resolve().parents[1] / 'devguide/validation/data/audit'
KINDS = ['standalone', 'docking', 'scored_collection']


def _records(kind):
    name = (
        'minimal_vina_result.json' if kind == 'docking' else 'minimal_scored_pose.json'
    )
    record = json.loads((DATA / name).read_text())
    if kind == 'standalone':
        return record, record, bmt.audit_pose
    if kind == 'scored_collection':
        record = bmt.DockingResult([bmt.DockingPose.from_dict(record)]).to_dict()
    return record, record['poses'][0], bmt.audit_result


@pytest.mark.parametrize('kind', KINDS)
@pytest.mark.parametrize('value', [True, False, '1.0', None, 1 + 1j, float('inf')])
def test_invalid_coordinate_scalars_are_inconsistent_without_coercion(kind, value):
    record, pose, audit = _records(kind)
    pose['coordinates']['value'][0][0] = value
    before = repr(record)
    report = audit(record)
    assert report['status'] == 'inconsistent'
    assert any(
        check['check'] == 'coordinate_units' and check['status'] == 'inconsistent'
        for check in report['checks']
    )
    assert repr(record) == before
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingPose.from_dict(pose)
    assert caught.value.extra['arg_name'] == 'coordinates'


@pytest.mark.parametrize('collection', [False, True])
@pytest.mark.parametrize('unit', ['nm', 'angstrom'])
def test_canonical_empty_pose_snapshot_has_valid_coordinates(collection, unit):
    pose = bmt.DockingPose(puw.quantity(np.empty((0, 3)), unit))
    wire = pose.to_dict()
    assert wire['coordinates']['value'] == []
    assert bmt.DockingPose.from_dict(wire).n_atoms == 0
    record = bmt.DockingResult([pose]).to_dict() if collection else wire
    before = deepcopy(record)
    report = (bmt.audit_result if collection else bmt.audit_pose)(record)
    assert report['status'] == 'incomplete'
    assert not any(check['status'] == 'inconsistent' for check in report['checks'])
    assert any(
        check['check'] == 'coordinate_units' and check['status'] == 'consistent'
        for check in report['checks']
    )
    assert record == before


@pytest.mark.parametrize('kind', KINDS)
@pytest.mark.parametrize('unit', ['nm', 'angstrom'])
def test_valid_numeric_coordinates_keep_units_and_detached_reports(kind, unit):
    record, pose, audit = _records(kind)
    pose['coordinates']['value'][0] = [1, 2.5, -3]
    pose['coordinates']['unit'] = unit
    before = deepcopy(record)
    report = audit(record)
    assert report['status'] == (
        'incomplete' if kind == 'scored_collection' else 'consistent'
    )
    assert record == before
    assert report == audit(record)
    report['checks'][0]['status'] = 'changed'
    assert audit(record)['checks'][0]['status'] != 'changed'


@pytest.mark.parametrize('collection', [False, True])
@pytest.mark.parametrize('unit', [None, 'seconds', 'unknown-unit'])
def test_empty_coordinates_still_require_length_units(collection, unit):
    record = bmt.DockingPose(puw.quantity(np.empty((0, 3)), 'nm')).to_dict()
    record['coordinates']['unit'] = unit
    if collection:
        record = {'schema_version': '1.0', 'poses': [record], 'provenance': {}}
    report = (bmt.audit_result if collection else bmt.audit_pose)(record)
    assert report['status'] == 'inconsistent'
    assert any(
        check['check'] == 'coordinate_units' and check['status'] == 'inconsistent'
        for check in report['checks']
    )


@pytest.mark.parametrize('values', [[1, 2, 3], [[1, 2]], [[], []], [[[1, 2, 3]]]])
def test_other_empty_or_malformed_shapes_remain_inconsistent(values):
    record, pose, audit = _records('standalone')
    pose['coordinates']['value'] = values
    assert audit(record)['status'] == 'inconsistent'


@pytest.mark.parametrize('empty', [False, True])
def test_missing_coordinate_unit_stays_incomplete(empty):
    record, pose, audit = _records('standalone')
    if empty:
        pose['coordinates']['value'] = []
    del pose['coordinates']['unit']
    report = audit(record)
    assert report['status'] == 'incomplete'
    assert any(
        check['check'] == 'coordinate_units' and check['status'] == 'incomplete'
        for check in report['checks']
    )


def test_coordinate_allocation_failure_propagates_unchanged():
    failure = MemoryError('allocation control')

    class Values:
        def __array__(self, dtype=None, copy=None):
            raise failure

    record, pose, audit = _records('standalone')
    pose['coordinates']['value'] = Values()
    with pytest.raises(MemoryError) as caught:
        audit(record)
    assert caught.value is failure
