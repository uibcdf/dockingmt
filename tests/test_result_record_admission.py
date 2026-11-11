"""A result's pose axis is explicit, ordered and never silently repaired."""

from collections.abc import Set
from copy import deepcopy

import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError


def _pose(label):
    return bmt.DockingPose(
        puw.quantity([[1, 2, 3]], 'nm'),
        scores={'record-metric': 1.0},
        pose_id=label,
        metadata={'nested': {'labels': [label]}},
    )


def _record():
    return bmt.DockingResult(
        [_pose('first'), _pose('second')],
        provenance={'nested': {'labels': ['producer']}},
    ).to_dict()


@pytest.mark.parametrize(
    'axis', [None, False, 0, '', 'poses', b'', bytearray(), {}, set(), frozenset()]
)
def test_result_reader_rejects_invalid_collection_field(axis):
    record = _record()
    record['poses'] = axis
    before = repr(record)
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult.from_dict(record)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == 'poses'
    assert record['poses'] is axis and repr(record) == before


@pytest.mark.parametrize('position', [0, 1])
@pytest.mark.parametrize('member', [None, True, 1, 'pose', [], ()])
def test_result_reader_identifies_invalid_member_position(position, member):
    record = _record()
    record['poses'][position] = member
    before = deepcopy(record)
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult.from_dict(record)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == 'poses'
    assert caught.value.extra['pose_index'] == position
    assert record == before


def test_result_reader_rejects_iterator_before_consumption():
    events = []

    def axis():
        events.append('iterated')
        yield _pose('unreached').to_dict()

    values = axis()
    try:
        with pytest.raises(ArgumentError) as caught:
            bmt.DockingResult.from_dict({'poses': values})
        assert caught.value.extra['arg_name'] == 'poses'
        assert events == []
    finally:
        values.close()


def test_invalid_axis_is_rejected_before_payload_copy():
    class CopySentinel:
        def __deepcopy__(self, memo):
            pytest.fail('Invalid pose axis reached payload copying')

    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult.from_dict(
            {'poses': {}, 'provenance': {'payload': CopySentinel()}}
        )
    assert caught.value.extra['arg_name'] == 'poses'


def test_invalid_later_member_is_rejected_before_copy_or_pose_conversion(monkeypatch):
    class CopySentinel:
        def __deepcopy__(self, memo):
            pytest.fail('Invalid member reached payload copying')

    def forbidden(*args, **kwargs):
        pytest.fail('Invalid member reached pose conversion')

    first = _pose('first').to_dict()
    first['metadata']['payload'] = CopySentinel()
    monkeypatch.setattr(bmt.DockingPose, 'from_dict', forbidden)
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult.from_dict({'poses': [first, None]})
    assert caught.value.extra['arg_name'] == 'poses'
    assert caught.value.extra['pose_index'] == 1


@pytest.mark.parametrize('axis', [None, {}, ''])
def test_root_schema_priority_is_preserved(axis):
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult.from_dict({'schema_version': '999.0', 'poses': axis})
    assert caught.value.extra['arg_name'] == 'schema_version'
    assert caught.value.extra['record_type'] == 'DockingResult'


def test_nested_schema_priority_is_preserved_before_copy():
    class CopySentinel:
        def __deepcopy__(self, memo):
            pytest.fail('Unsupported nested version reached copy')

    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult.from_dict(
            {
                'poses': [{'schema_version': '999.0'}],
                'provenance': {'payload': CopySentinel()},
            }
        )
    assert caught.value.extra['arg_name'] == 'schema_version'
    assert caught.value.extra['record_type'] == 'DockingPose'


@pytest.mark.parametrize('kind', [set, frozenset])
@pytest.mark.parametrize('populated', [False, True])
def test_live_result_rejects_unordered_collections(kind, populated):
    values = kind([_pose('first')]) if populated else kind()
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult(values)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == 'poses'


def test_live_unordered_collection_is_rejected_before_iteration():
    class Unordered(Set):
        def __contains__(self, value):
            return False

        def __len__(self):
            return 0

        def __iter__(self):
            pytest.fail('Unordered collection was consumed')

    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult(Unordered())
    assert caught.value.extra['arg_name'] == 'poses'


@pytest.mark.parametrize('kind', ['list', 'tuple', 'generator'])
def test_live_ordered_inputs_keep_order_identity_and_single_consumption(kind):
    poses = [_pose('second'), _pose('first')]
    events = []

    def source():
        for pose in poses:
            events.append(pose.pose_id)
            yield pose

    values = (
        source() if kind == 'generator' else (poses if kind == 'list' else tuple(poses))
    )
    restored = bmt.DockingResult(values)
    assert [pose.pose_id for pose in restored] == ['second', 'first']
    assert restored[0] is poses[0] and restored[1] is poses[1]
    if kind == 'generator':
        assert events == ['second', 'first']
        restored.to_dict()
        assert events == ['second', 'first']


@pytest.mark.parametrize('kind', [list, tuple])
@pytest.mark.parametrize('legacy', [False, True])
def test_result_reader_preserves_order_multiplicity_and_detachment(kind, legacy):
    record = _record()
    first, second = record['poses']
    record['poses'] = kind([second, first, second])
    expected = deepcopy(record)
    expected['poses'] = list(expected['poses'])
    if legacy:
        del record['schema_version']
    before = deepcopy(record)
    restored = bmt.DockingResult.from_dict(record)
    assert [pose.pose_id for pose in restored] == ['second', 'first', 'second']
    assert restored.to_dict() == expected and record == before
    assert restored[0] is not restored[2]
    restored[0].metadata['nested']['labels'].append('changed')
    assert restored[2].metadata['nested']['labels'] == ['second']
    assert record['poses'][0]['metadata']['nested']['labels'] == ['second']
    record['provenance']['nested']['labels'].append('caller')
    assert restored.provenance['nested']['labels'] == ['producer']


@pytest.mark.parametrize('record', [{}, {'poses': []}, {'poses': ()}])
def test_valid_empty_and_omitted_legacy_axes_remain_supported(record):
    restored = bmt.DockingResult.from_dict(record)
    assert len(restored) == 0 and restored.to_dict()['poses'] == []


def test_outcome_rejects_invalid_nested_result_axis():
    record = bmt.DockingOutcome(0, result=bmt.DockingResult([])).to_dict()
    record['result']['poses'] = {}
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingOutcome.from_dict(record)
    assert caught.value.extra['arg_name'] == 'poses'


def test_resource_failures_preserve_identity_for_ordered_live_input():
    first = _pose('first')
    error = MemoryError('source interrupted')

    def source():
        yield first
        raise error

    with pytest.raises(MemoryError) as caught:
        bmt.DockingResult(source())
    assert caught.value is error


def test_resource_failure_during_record_copy_preserves_identity():
    error = MemoryError('record copy interrupted')

    class CopyInterrupted:
        def __deepcopy__(self, memo):
            raise error

    record = _record()
    record['provenance']['payload'] = CopyInterrupted()
    with pytest.raises(MemoryError) as caught:
        bmt.DockingResult.from_dict(record)
    assert caught.value is error
