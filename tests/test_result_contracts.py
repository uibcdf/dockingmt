import json

import numpy as np
import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

from dockingmt import DockingPose, DockingResult
from dockingmt._private.smonitor import ArgumentError


@pytest.fixture
def coordinates():
    return puw.quantity([[0, 0, 0]], 'nm')


@pytest.mark.parametrize(
    'value', [float('nan'), float('inf'), -float('inf'), True, '-8', None, 1j, [1]]
)
def test_pose_rejects_invalid_named_score(value, coordinates):
    with pytest.raises(ArgumentError) as caught:
        DockingPose(coordinates, scores={'vina': value})
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == 'scores'
    assert caught.value.extra['score_name'] == 'vina'


@pytest.mark.parametrize(
    'scores', [{1: -8}, {'': -8}, {' ': -8}, [('vina', -8)], 'vina']
)
def test_pose_requires_named_score_mapping(scores, coordinates):
    with pytest.raises(ArgumentError):
        DockingPose(coordinates, scores=scores)


def test_numpy_scores_normalize_for_json_and_ranking(coordinates):
    pose = DockingPose(
        coordinates, scores={'vina': np.float32(-8), 'count': np.int64(2)}
    )
    record = json.loads(json.dumps(pose.to_dict(), allow_nan=False))
    assert record['scores'] == {'vina': -8, 'count': 2}
    assert all(isinstance(value, float) for value in pose.scores.values())


@pytest.mark.parametrize('value', [float('nan'), float('inf'), True, '-8', None])
def test_ranking_rechecks_scores_after_rescoring_edits(value, coordinates):
    valid = DockingPose(coordinates, scores={'vina': -8}, pose_id='valid')
    edited = DockingPose(coordinates, scores={'vina': -9}, pose_id='edited')
    result = DockingResult([edited, valid])
    edited.scores['vina'] = value
    with pytest.raises(ArgumentError) as caught:
        result.rank_by('vina')
    assert caught.value.extra['score_name'] == 'vina'
    assert caught.value.extra['pose_index'] == 0
    assert [pose.pose_id for pose in result] == ['edited', 'valid']
    assert all(pose.rank is None for pose in result)
    with pytest.raises(ArgumentError):
        edited.to_dict()


@pytest.mark.parametrize('direction', ['False', 0, 1, None])
def test_ranking_direction_requires_bool(direction, coordinates):
    result = DockingResult([DockingPose(coordinates, scores={'vina': -8})])
    with pytest.raises(ArgumentError) as caught:
        result.rank_by('vina', ascending=direction)
    assert caught.value.extra['arg_name'] == 'ascending'


@pytest.mark.parametrize('name', [None, '', ' ', 1, []])
def test_ranking_score_name_requires_nonempty_string(name, coordinates):
    result = DockingResult([DockingPose(coordinates, scores={'vina': -8})])
    with pytest.raises(ArgumentError) as caught:
        result.rank_by(name)
    assert caught.value.extra['arg_name'] == 'score_name'


def test_ranking_unknown_keyword_uses_argdigest(coordinates):
    result = DockingResult([DockingPose(coordinates, scores={'vina': -8})])
    with pytest.raises(UnknownArgumentError):
        result.rank_by('vina', ascendng=False)


@pytest.mark.parametrize(
    'ascending,expected',
    [
        (True, ['low', 'tie-a', 'tie-b']),
        (False, ['tie-a', 'tie-b', 'low']),
    ],
)
def test_ranking_preserves_tie_order_identity_and_explicit_policy(
    ascending, expected, coordinates
):
    poses = [
        DockingPose(
            coordinates,
            scores={'metric': score},
            pose_id=identity,
            partner_state_id='ligand',
            receptor_state_id='receptor',
        )
        for identity, score in [('tie-a', 1), ('low', 0), ('tie-b', 1)]
    ]
    result = DockingResult(poses)
    ranked = result.rank_by('metric', ascending=ascending)
    assert [pose.pose_id for pose in ranked] == expected
    assert [pose.rank for pose in ranked] == [1, 2, 3]
    assert all(
        pose.partner_state_id == 'ligand' and pose.receptor_state_id == 'receptor'
        for pose in ranked
    )
    assert [pose.pose_id for pose in result] == ['tie-a', 'low', 'tie-b']
    assert all(pose.rank is None for pose in result)
    assert ranked.provenance['ranking_policy'] == {
        'score_name': 'metric',
        'ascending': ascending,
    }
    assert DockingResult([]).rank_by('metric', ascending=ascending).top_pose is None


@pytest.fixture
def result(coordinates):
    pose = DockingPose(
        coordinates, scores={'vina': -8}, metadata={'nested': {'values': ['original']}}
    )
    return DockingResult(
        [pose],
        problem_info={'source': {'ids': ['original']}},
        protocol_info={'parameters': {'seed': 42}},
        provenance={'artifacts': {'hashes': ['original']}},
    )


def test_pose_export_is_independent_snapshot(result):
    pose = result[0]
    record = pose.to_dict()
    record['scores']['vina'] = 0
    record['metadata']['nested']['values'][0] = 'edited'
    record['coordinates']['value'][0][0] = 5
    assert pose.scores == {'vina': -8}
    assert pose.metadata['nested']['values'] == ['original']
    assert puw.get_value(pose.coordinates)[0, 0] == 0
    pose.metadata['nested']['values'].append('new')
    assert record['metadata']['nested']['values'] == ['edited']


def test_result_export_is_independent_snapshot(result):
    record = result.to_dict()
    record['problem_info']['source']['ids'][0] = 'edited'
    record['protocol_info']['parameters']['seed'] = 0
    record['provenance']['artifacts']['hashes'][0] = 'edited'
    record['poses'][0]['metadata']['nested']['values'].append('edited')
    assert result.problem_info['source']['ids'] == ['original']
    assert result.protocol_info['parameters']['seed'] == 42
    assert result.provenance['artifacts']['hashes'] == ['original']
    assert result[0].metadata['nested']['values'] == ['original']
    result.provenance['artifacts']['hashes'].append('new')
    assert record['provenance']['artifacts']['hashes'] == ['edited']


def test_pose_reconstruction_does_not_share_input_record(result):
    record = result[0].to_dict()
    restored = DockingPose.from_dict(record)
    record['metadata']['nested']['values'].append('edited')
    assert restored.metadata['nested']['values'] == ['original']
    restored.metadata['nested']['values'].append('new')
    assert record['metadata']['nested']['values'] == ['original', 'edited']


def test_result_reconstruction_and_json_round_trip_are_independent(result):
    record = json.loads(json.dumps(result.to_dict(), allow_nan=False))
    restored = DockingResult.from_dict(record)
    assert restored.to_dict() == record
    record['problem_info']['source']['ids'].append('edited')
    record['protocol_info']['parameters']['seed'] = 0
    record['provenance']['artifacts']['hashes'].append('edited')
    record['poses'][0]['metadata']['nested']['values'].append('edited')
    assert restored.problem_info['source']['ids'] == ['original']
    assert restored.protocol_info['parameters']['seed'] == 42
    assert restored.provenance['artifacts']['hashes'] == ['original']
    assert restored[0].metadata['nested']['values'] == ['original']
    restored.provenance['artifacts']['hashes'].append('new')
    assert record['provenance']['artifacts']['hashes'] == ['original', 'edited']


def test_result_operations_do_not_request_molecular_or_viewer_operations(
    result, monkeypatch
):
    import builtins

    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Ranking or result serialization requested a molecular operation')

    for name in ('get', 'select', 'extract', 'convert', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    actual_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name == 'molsysviewer' or name.startswith('molsysviewer.'):
            pytest.fail('Result operations imported the viewer')
        return actual_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded_import)
    ranked = result.rank_by('vina')
    restored = DockingResult.from_dict(
        json.loads(json.dumps(ranked.to_dict(), allow_nan=False))
    )
    assert restored.top_pose.scores == {'vina': -8}
