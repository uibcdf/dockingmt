import builtins
import json
from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt import DockingPose, DockingResult
from dockingmt._private.smonitor import ArgumentError


@pytest.fixture
def definition():
    return {
        'schema_version': '1.0',
        'method': 'declared-example',
        'method_version': '1',
        'component': 'pose preference',
        'kind': 'dimensionless',
        'unit': 'dimensionless',
        'preferred_direction': 'higher',
        'context': {'receptor': 'same-source', 'preparation': {'id': 'same-input'}},
    }


def pose(identity, value, definition=None):
    return DockingPose(
        puw.quantity([[1, 2, 3]], 'angstrom'),
        scores={'metric': value, 'other': 1 - value},
        pose_id=identity,
        partner_state_id='ligand',
        receptor_state_id='receptor',
        score_definitions={'metric': definition} if definition is not None else None,
    )


@pytest.mark.parametrize(
    'field,value',
    [
        ('schema_version', '2.0'),
        ('method', ''),
        ('method_version', None),
        ('component', ' '),
        ('kind', 'physical'),
        ('kind', []),
        ('preferred_direction', True),
        ('unit', 'kcal/mol'),
        ('context', {}),
        ('context', {'x': float('nan')}),
        ('context', {1: 'non-string key'}),
        ('context', {'x': np.array([1])}),
        ('context', {'x': (1, 2)}),
    ],
)
def test_descriptor_rejects_malformed_meaning(field, value, definition):
    definition[field] = value
    with pytest.raises(ArgumentError):
        pose('a', 0.1, definition)


@pytest.mark.parametrize(
    'change', ['missing', 'unknown', 'absent-score', 'not-mapping']
)
def test_descriptor_requires_exact_fields_and_existing_score(change, definition):
    if change == 'missing':
        del definition['unit']
    elif change == 'unknown':
        definition['typo'] = True
    definitions = {'metric': definition}
    if change == 'absent-score':
        definitions = {'absent': definition}
    elif change == 'not-mapping':
        definitions = [definition]
    with pytest.raises(ArgumentError):
        DockingPose(
            puw.quantity([[0, 0, 0]], 'nm'),
            scores={'metric': 1},
            score_definitions=definitions,
        )


@pytest.mark.parametrize('unit', ['nm', 'undefined_score_unit', '', None])
def test_empirical_definition_requires_energy_like_unit(unit, definition):
    definition.update(kind='empirical', unit=unit)
    with pytest.raises(ArgumentError):
        pose('a', -8, definition)


def test_descriptor_roundtrip_owns_context_and_preserves_unit_policy(definition):
    definition.update(kind='empirical', unit='kcal/mol', preferred_direction='lower')
    with puw.context(standard_units=['angstrom', 'fs', 'kJ/mol']):
        source = pose('a', -8, definition)
        definition['context']['preparation']['id'] = 'changed'
        descriptor = source.score_definitions['metric']
        assert descriptor['context']['preparation']['id'] == 'same-input'
        assert puw.are_compatible(puw.quantity(1, descriptor['unit']), 'kcal/mol')
        assert (
            puw.get_value(puw.quantity(-8, descriptor['unit']), to_unit='kcal/mol')
            == -8
        )
        restored = DockingPose.from_dict(json.loads(json.dumps(source.to_dict())))
        assert restored.to_dict() == source.to_dict()
        assert restored.scores['metric'] == -8
        np.testing.assert_allclose(
            puw.get_value(restored.coordinates), [[0.1, 0.2, 0.3]]
        )
        descriptor['context']['preparation']['id'] = 'edited-export'
        assert (
            source.score_definitions['metric']['context']['preparation']['id']
            == 'same-input'
        )


@pytest.mark.parametrize(
    'change',
    [
        'method',
        'version',
        'component',
        'unit',
        'kind',
        'direction',
        'context',
        'state',
        'missing',
        'bool-context',
    ],
)
def test_ranking_rejects_incompatible_meaning(change, definition):
    first = pose('a', 0.1, definition)
    second = pose('b', 0.2, definition)
    modified = second.metadata['score_definitions']['metric']
    if change == 'method':
        modified['method'] = 'other'
    elif change == 'version':
        modified['method_version'] = '2'
    elif change == 'component':
        modified['component'] = 'different metric'
    elif change in ('unit', 'kind'):
        modified.update(kind='empirical', unit='kJ/mol')
    elif change == 'direction':
        modified['preferred_direction'] = 'lower'
    elif change == 'context':
        modified['context']['receptor'] = 'different-input'
    elif change == 'state':
        second.receptor_state_id = 'different-state'
    elif change == 'bool-context':
        first.metadata['score_definitions']['metric']['context']['flag'] = True
        modified['context']['flag'] = 1
    else:
        del second.metadata['score_definitions']
    result = DockingResult([first, second])
    original = result.to_dict()
    with pytest.raises(ArgumentError):
        result.rank_by('metric')
    assert result.to_dict() == original


def test_ranking_rechecks_mutated_descriptors(definition):
    source = pose('a', 0.1, definition)
    source.metadata['score_definitions']['metric']['unit'] = 'nm'
    with pytest.raises(ArgumentError):
        DockingResult([source]).rank_by('metric')
    with pytest.raises(ArgumentError):
        source.to_dict()


def test_repeated_rankings_retain_independent_scalar_evidence(definition):
    result = DockingResult(
        [
            pose('a', 0.3, definition),
            pose('b', 0.1, definition),
            pose('c', 0.3, definition),
        ]
    )
    original = result.to_dict()
    first = result.rank_by('metric', ascending=False)
    second = first.rank_by('other')
    assert [p.pose_id for p in first] == ['a', 'c', 'b']
    assert [p.pose_id for p in second] == ['a', 'c', 'b']
    history = second.ranking_history
    assert len(history) == 2
    assert history[0]['output_order'] == [0, 2, 1]
    assert history[1]['output_order'] == [0, 1, 2]
    assert [item['value'] for item in history[0]['input_order']] == [0.3, 0.1, 0.3]
    assert history[0]['score_definition'] == definition
    assert history[1]['score_definition'] is None
    assert second.provenance['ranking_policy'] == {
        'score_name': 'other',
        'ascending': True,
    }
    assert all(
        'coordinates' not in item for entry in history for item in entry['input_order']
    )
    second[0].scores['metric'] = 100
    second[0].metadata['score_definitions']['metric']['context']['receptor'] = 'edited'
    second.provenance['ranking_history'][0]['input_order'][0]['value'] = 999
    history[0]['score_definition']['context']['receptor'] = 'edited-snapshot'
    assert first.ranking_history[0]['input_order'][0]['value'] == 0.3
    assert first[0].score_definitions['metric'] == definition
    assert result.to_dict() == original


def test_explicit_direction_is_preserved_despite_preference(definition):
    result = DockingResult([pose('a', 0.1, definition), pose('b', 0.2, definition)])
    assert result.rank_by('metric').top_pose.pose_id == 'a'
    assert result.rank_by('metric', ascending=False).top_pose.pose_id == 'b'


def test_ranking_requires_matching_declared_units_and_accepts_unit_aliases(definition):
    definition.update(kind='empirical', unit='kcal/mol')
    first = pose('a', -8, definition)
    alias = deepcopy(definition)
    alias['unit'] = 'kilocalorie / mole'
    second = pose('b', -7, alias)
    assert DockingResult([first, second]).rank_by('metric').top_pose.pose_id == 'a'
    second.metadata['score_definitions']['metric']['unit'] = 'kJ/mol'
    with pytest.raises(ArgumentError):
        DockingResult([first, second]).rank_by('metric')


def test_ranked_context_and_exported_history_are_independent(definition):
    result = DockingResult(
        [pose('a', 0.1, definition)],
        problem_info={'ids': ['source']},
        protocol_info={'settings': {'seed': 42}},
    )
    ranked = result.rank_by('metric')
    ranked.problem_info['ids'].append('edited')
    ranked.protocol_info['settings']['seed'] = 0
    exported = ranked.to_dict()
    exported['provenance']['ranking_history'][0]['score_definition']['context'][
        'receptor'
    ] = 'edited'
    assert result.problem_info['ids'] == ['source']
    assert result.protocol_info['settings']['seed'] == 42
    assert ranked.ranking_history[0]['score_definition'] == definition


def test_legacy_policy_is_retained_without_invented_observations():
    result = DockingResult(
        [pose(None, 0.3), pose(None, 0.1)],
        provenance={'ranking_policy': {'score_name': 'other', 'ascending': False}},
    )
    restored = DockingResult.from_dict(result.to_dict())
    ranked = restored.rank_by('metric')
    history = ranked.ranking_history
    assert history[0]['evidence'] == 'legacy_policy_only'
    assert history[0]['policy'] == result.provenance['ranking_policy']
    assert 'input_order' not in history[0]
    assert history[1]['output_order'] == [1, 0]
    assert history[1]['score_definition'] is None
    assert len(ranked.rank_by('other').ranking_history) == 3
    assert (
        DockingResult.from_dict(json.loads(json.dumps(ranked.to_dict()))).to_dict()
        == ranked.to_dict()
    )


@pytest.mark.parametrize(
    'change',
    [
        'not-list',
        'version',
        'missing-values',
        'permutation',
        'nonfinite-value',
        'direction',
    ],
)
def test_reader_rejects_malformed_ranking_history(change):
    record = DockingResult([pose('a', 0.1), pose('b', 0.2)]).rank_by('metric').to_dict()
    entry = record['provenance']['ranking_history'][0]
    if change == 'not-list':
        record['provenance']['ranking_history'] = {}
    elif change == 'version':
        entry['schema_version'] = '2.0'
    elif change == 'missing-values':
        del entry['input_order'][0]['value']
    elif change == 'permutation':
        entry['output_order'] = [0, 0]
    elif change == 'nonfinite-value':
        entry['input_order'][0]['value'] = float('inf')
    else:
        entry['ascending'] = 1
    with pytest.raises(ArgumentError):
        DockingResult.from_dict(record)


def test_offline_semantics_and_ranking_do_not_request_providers(
    monkeypatch, definition
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Offline score operations requested molecular work')

    for name in ('get', 'select', 'extract', 'convert', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    actual_import = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name.split('.')[0] in ('vina', 'molsysviewer', 'rdkit'):
            pytest.fail('Offline score operations imported an optional provider')
        return actual_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded)
    result = DockingResult([pose('a', 0.1, definition), pose('b', 0.2, definition)])
    saved = json.loads(
        json.dumps(result.rank_by('metric', ascending=False).rank_by('other').to_dict())
    )
    restored = DockingResult.from_dict(deepcopy(saved))
    assert restored.to_dict() == saved
    assert len(restored.ranking_history) == 2
