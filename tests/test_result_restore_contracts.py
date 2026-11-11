"""Restoration detaches owners while preserving declared context relationships."""

from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt


def _record():
    pose = bmt.DockingPose(
        puw.quantity([[1, 2, 3]], 'angstrom'),
        pose_id='restoration-control',
        metadata={'annotations': ['original']},
    )
    return bmt.DockingResult([pose]).to_dict()


@pytest.mark.parametrize('extension', [False, True])
def test_repeated_poses_and_shared_context_keep_distinct_owners(extension):
    class ExtensionResult(bmt.DockingResult):
        __module__ = 'consumer_extension.models'

    model = ExtensionResult if extension else bmt.DockingResult
    record = _record()
    shared = {'array': np.array([1, 2]), 'tuple': ([3], {'tag'})}
    for field in ('problem_info', 'protocol_info', 'provenance'):
        record[field]['payload'] = shared
    record['poses'][0]['metadata']['payload'] = shared
    record['poses'].append(record['poses'][0])
    restored = model.from_dict(record)
    assert isinstance(restored, model)
    assert [pose.pose_id for pose in restored] == ['restoration-control'] * 2
    context = restored.problem_info['payload']
    assert context is restored.protocol_info['payload']
    assert context is restored.provenance['payload']
    first, second = [pose.metadata['payload'] for pose in restored]
    assert context is not shared and first is not second
    for value in (context, first, second):
        assert not np.shares_memory(value['array'], shared['array'])
        assert value['tuple'] == ([3], {'tag'})
    assert not np.shares_memory(first['array'], second['array'])
    context['array'][0] = 42
    context['tuple'][0].append(4)
    first['array'][0] = 17
    first['tuple'][1].add('first')
    puw.get_value(restored[0].coordinates)[0, 0] = 999
    assert second['array'].tolist() == [1, 2]
    assert second['tuple'] == ([3], {'tag'})
    assert shared['array'].tolist() == [1, 2]
    assert shared['tuple'] == ([3], {'tag'})
    assert record['poses'][0]['coordinates']['value'][0][0] == pytest.approx(0.1)
    assert puw.get_value(restored[1].coordinates)[0, 0] == pytest.approx(0.1)
    shared['array'][0] = 77
    assert context['array'].tolist() == [42, 2]
    assert first['array'].tolist() == [17, 2]
    assert second['array'].tolist() == [1, 2]


def test_custom_root_mapping_copy_semantics_remain_supported():
    class Record(dict):
        def __deepcopy__(self, memo):
            value = deepcopy(dict(self), memo)
            value['provenance']['extension'] = {'labels': ['root-hook']}
            return value

    record = Record(_record())
    restored = bmt.DockingResult.from_dict(record)
    assert restored.provenance['extension'] == {'labels': ['root-hook']}
    assert 'extension' not in record['provenance']


def test_custom_pose_mapping_copy_semantics_remain_supported():
    class Record(dict):
        def __deepcopy__(self, memo):
            value = deepcopy(dict(self), memo)
            value['metadata']['extension'] = {'labels': ['pose-hook']}
            return value

    record = _record()
    record['poses'][0] = Record(record['poses'][0])
    restored = bmt.DockingResult.from_dict(record)
    assert restored[0].metadata['extension'] == {'labels': ['pose-hook']}
    assert 'extension' not in record['poses'][0]['metadata']


@pytest.mark.parametrize(
    'field', ['problem_info', 'protocol_info', 'provenance', 'unknown_extension']
)
def test_copy_resource_failures_keep_the_original_exception(field):
    failure = MemoryError('restoration copy control')

    class Payload:
        def __deepcopy__(self, memo):
            raise failure

    record = _record()
    if field == 'unknown_extension':
        record[field] = Payload()
    else:
        record[field]['payload'] = Payload()
    with pytest.raises(MemoryError) as caught:
        bmt.DockingResult.from_dict(record)
    assert caught.value is failure


def test_nested_custom_mapping_keeps_its_existing_copy_semantics():
    class Annotation(dict):
        def __deepcopy__(self, memo):
            copied = type(self)(deepcopy(dict(self), memo))
            copied['history'].append('snapshot')
            return copied

    record = _record()
    original = Annotation(history=['source'])
    record['poses'][0]['metadata']['annotation'] = original
    restored = bmt.DockingResult.from_dict(record)
    assert restored[0].metadata['annotation']['history'] == [
        'source',
        'snapshot',
        'snapshot',
    ]
    assert original['history'] == ['source']
