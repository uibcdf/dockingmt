"""Coordinate record reading preserves the declared pose data, including empties."""

from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError


def _record():
    return dmt.DockingPose(
        puw.quantity([[1, 2, 3], [4, 5, 6]], 'nm'),
        scores={'record-metric': 1.0},
        rank=2,
        pose_id='record',
        receptor_state_id='record-receptor',
        partner_state_id='record-partner',
        metadata={'nested': {'values': [1]}},
    ).to_dict()


@pytest.mark.parametrize('route', ['pose', 'result', 'outcome'])
@pytest.mark.parametrize('legacy', [False, True])
def test_empty_pose_record_roundtrips_directly_and_through_containers(route, legacy):
    pose = dmt.DockingPose(
        puw.quantity(np.empty((0, 3)), 'angstrom'),
        pose_id='empty-record',
        metadata={'nested': {'values': []}},
    )
    original = pose
    if route == 'result':
        original = dmt.DockingResult([pose])
    elif route == 'outcome':
        original = dmt.DockingOutcome(
            0, result=dmt.DockingResult([pose]), backend='record'
        )
    expected = original.to_dict()
    record = deepcopy(expected)
    if legacy:
        del record['schema_version']
    before = deepcopy(record)
    restored = type(original).from_dict(record)
    assert restored.to_dict() == expected
    assert record == before
    if route == 'result':
        restored = restored.poses[0]
    elif route == 'outcome':
        restored = restored.result.poses[0]
    assert restored.n_atoms == 0
    assert puw.get_value(restored.coordinates).shape == (0, 3)


@pytest.mark.parametrize('values', [[], (), np.empty((0, 3))])
@pytest.mark.parametrize('unit', ['nm', 'angstrom', 'pm'])
def test_pose_reader_restores_only_the_empty_xyz_axis(values, unit):
    record = _record()
    record['coordinates'] = {'value': values, 'unit': unit}
    restored = dmt.DockingPose.from_dict(record)
    assert restored.n_atoms == 0
    assert puw.get_value(restored.coordinates).shape == (0, 3)
    assert restored.to_dict()['coordinates']['value'] == []
    assert restored.pose_id == 'record' and restored.scores == record['scores']


@pytest.mark.parametrize(
    'values',
    [
        np.empty((0, 4)),
        np.empty((0, 0)),
        np.empty((1, 0)),
        np.empty((0, 3, 1)),
        np.empty((0, 3), dtype=bool),
        np.empty((0, 3), dtype=complex),
        [[]],
    ],
)
def test_pose_reader_does_not_repair_invalid_empty_axes(values):
    record = _record()
    record['coordinates']['value'] = values
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingPose.from_dict(record)
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == 'coordinates'


@pytest.mark.parametrize(
    'coordinates',
    [None, [], 1, 'coordinates', {}, {'value': [[1, 2, 3]]}, {'unit': 'nm'}],
)
def test_pose_reader_requires_complete_coordinate_mapping(coordinates):
    record = _record()
    record['coordinates'] = coordinates
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingPose.from_dict(record)
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == 'coordinates'


def test_pose_reader_requires_coordinates():
    record = _record()
    del record['coordinates']
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingPose.from_dict(record)
    assert caught.value.extra['arg_name'] == 'coordinates'


@pytest.mark.parametrize('unit', ['not-a-unit', [], {}, None, 'ps'])
def test_pose_reader_has_local_unit_diagnostics(unit):
    record = _record()
    record['coordinates']['unit'] = unit
    before = deepcopy(record)
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingPose.from_dict(record)
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == 'coordinates'
    assert record == before


@pytest.mark.parametrize(
    'failure', [ValueError('quantity refused'), MemoryError('interrupted')]
)
def test_pose_reader_preserves_provider_cause_and_resource_identity(
    failure, monkeypatch
):
    record = _record()

    def refused(*args, **kwargs):
        raise failure

    monkeypatch.setattr(puw, 'quantity', refused)
    if isinstance(failure, MemoryError):
        with pytest.raises(MemoryError) as caught:
            dmt.DockingPose.from_dict(record)
        assert caught.value is failure
    else:
        with pytest.raises(ArgumentError) as caught:
            dmt.DockingPose.from_dict(record)
        assert caught.value.extra['arg_name'] == 'coordinates'
        assert caught.value.__cause__ is failure


@pytest.mark.parametrize('unit', ['nm', 'angstrom', 'pm'])
@pytest.mark.parametrize('dtype', [np.int64, np.float32, np.float64])
def test_pose_reader_preserves_numeric_records_units_and_detachment(unit, dtype):
    record = _record()
    values = np.array([[1, 2, 3], [4, 5, 6]], dtype=dtype)
    record['coordinates'] = {'value': values, 'unit': unit}
    before = values.copy()
    restored = dmt.DockingPose.from_dict(record)
    np.testing.assert_allclose(
        puw.get_value(restored.coordinates, to_unit=unit), values
    )
    np.testing.assert_array_equal(values, before)
    assert restored.pose_id == record['pose_id'] and restored.rank == record['rank']
    assert (
        restored.scores == record['scores'] and restored.metadata == record['metadata']
    )
    values[0, 0] = 999
    record['metadata']['nested']['values'].append(2)
    assert puw.get_value(restored.coordinates, to_unit=unit)[0, 0] == pytest.approx(1)
    assert restored.metadata['nested']['values'] == [1]
    assert dmt.DockingPose.from_dict(restored.to_dict()).to_dict() == restored.to_dict()
