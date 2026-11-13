"""Declared molecular axes keep source identity, order and historical evidence."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
from argdigest import UnknownArgumentError

import bindingmt as bmt
from bindingmt._private.interface_records import _digest

SOURCE = {'owner': 'caller', 'id': 'native-source', 'revision': 'r1'}
FROZEN = Path(__file__).parent / 'data/site_membership_compat/bb3dbfc'


def declare(element, indices=(5, 1, 3), **options):
    factory = getattr(
        bmt.BindingSite, 'from_atoms' if element == 'atom' else 'from_groups'
    )
    return factory(
        **{'source': deepcopy(SOURCE), f'{element}_indices': indices, **options}
    )


@pytest.mark.parametrize('element', ['atom', 'group'])
@pytest.mark.parametrize(
    'indices', [[5, 1, 3], (5, 1, 3), np.asarray([5, 1, 3], dtype=np.int32)]
)
def test_ordered_portable_source_membership_round_trip(element, indices, tmp_path):
    site = declare(
        element, indices, name='candidate members', structure_indices=[2, 0, 2]
    )
    raw = site.to_dict()
    payload = site.views[0]['payload']
    assert raw['format_version'] == '0.2'
    assert payload == {
        'element': element,
        'index_space': f'source_{element}_index',
        'source_indices': [5, 1, 3],
        'resolution': {'state': 'declared', 'cause': 'source_not_checked'},
    }
    assert all(type(i) is int for i in payload['source_indices'])
    assert site.inspect()['membership'] == {
        'state': 'declared',
        'entry_count': 3,
        'element': element,
        'index_space': f'source_{element}_index',
    }
    assert site.inspect()['molecular_resolution'] == 'not_performed'
    assert site.definition['scope']['source_structure_indices'] == [2, 0, 2]
    site.save(tmp_path / 'members.json')
    changed = json.loads(json.dumps(raw, sort_keys=True))
    (tmp_path / 'sorted.json').write_text(json.dumps(changed))
    assert bmt.BindingSite.from_dict(changed, experimental=True).to_dict() == raw
    assert (
        bmt.BindingSite.read(tmp_path / 'sorted.json', experimental=True).to_dict()
        == raw
    )
    assert (
        bmt.BindingSite.read(tmp_path / 'members.json', experimental=True).to_dict()
        == raw
    )


@pytest.mark.parametrize('element', ['atom', 'group'])
def test_empty_declared_membership_is_not_a_negative_finding_or_missing_view(element):
    site = declare(element, [])
    assert site.inspect()['membership']['state'] == 'declared_empty'
    assert site.inspect()['membership']['entry_count'] == 0
    assert len(site.views) == 1 and site.definition['binding_support'] == 'unknown'
    assert site.inspect()['realization_coverage'] == {'state': 'not_requested'}
    assert site.inspect()['molecular_resolution'] == 'not_performed'


@pytest.mark.parametrize('element', ['atom', 'group'])
@pytest.mark.parametrize(
    'indices',
    [
        None,
        2,
        'index 2',
        {2, 1},
        [True],
        [np.bool_(False)],
        [1.0],
        [-1],
        [2, 2],
        [[1, 2]],
        np.asarray([[1, 2]]),
        np.asarray([1.0, 2.0]),
        np.asarray([], dtype=float),
        np.asarray([], dtype=bool),
        np.asarray([1, 2], dtype=object),
    ],
)
def test_invalid_or_coercible_indices_are_refused(element, indices):
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare(element, indices)


@pytest.mark.parametrize('element', ['atom', 'group'])
def test_arrays_are_detached_and_source_bounds_are_not_guessed(element):
    indices = np.asarray([999, 1], dtype=np.int64)
    source = deepcopy(SOURCE)
    site = declare(element, indices, source=source)
    before = site.to_dict()
    indices[0] = 0
    source['id'] = 'edited'
    assert site.to_dict() == before
    assert site.views[0]['payload']['source_indices'] == [999, 1]
    assert site.context['source'] == SOURCE
    assert site.inspect()['asset_access'] == 'not_checked'


@pytest.mark.parametrize('element', ['atom', 'group'])
def test_evidence_revisions_preserve_original_index_view_and_claim(element):
    initial = declare(element)
    observed = initial.with_evidence(
        key='original',
        source={'owner': 'curator', 'id': 'annotation'},
        observation={'reported_members': 'membership'},
        attribution={'producer': 'curator'},
        structure_indices=[0],
    )
    revised = observed.with_definition(
        claim='A new interpretation',
        criterion={'kind': 'manual_rule'},
        reason='Do not retarget old observations',
    )
    assert observed.evidence[0]['original_claim_ref'] == initial.definition_ref
    assert (
        revised.evidence == observed.evidence
        and revised.definition['evidence_refs'] == []
    )
    assert revised.views == initial.views
    assert revised.to_dict()['format_version'] == '0.2'
    assert revised.inspect()['binding_support'] == 'unknown'
    assert initial.evidence == [] and initial.definition['evidence_refs'] == []


@pytest.mark.parametrize('element', ['atom', 'group'])
@pytest.mark.parametrize(
    'path,value',
    [
        (('payload', 'index_space'), 'local_atom_index'),
        (('payload', 'resolution'), {'state': 'resolved'}),
        (('payload', 'element'), 'residue'),
        (('payload', 'source_indices'), [True]),
        (('payload', 'source_indices'), [1.0]),
        (('role',), 'confirmed_binding'),
    ],
)
def test_recomputed_digest_preserves_semantic_admission(element, path, value):
    record = declare(element).to_dict()
    target = record['views'][0]
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    record['content_sha256'] = _digest(record)
    with pytest.raises(
        (bmt.exceptions.ArgumentError, bmt.exceptions.CapabilityMismatchError)
    ):
        bmt.BindingSite.from_dict(record, experimental=True)


@pytest.mark.parametrize('element', ['atom', 'group'])
def test_membership_cannot_be_disguised_as_01_or_an_empty_02_definition(element):
    record = declare(element).to_dict()
    record['format_version'] = '0.1'
    record['content_sha256'] = _digest(record)
    with pytest.raises(bmt.exceptions.ArgumentError, match='0.2'):
        bmt.BindingSite.from_dict(record, experimental=True)
    record = declare(element).to_dict()
    record['views'] = []
    record['definition']['views'] = []
    record['content_sha256'] = _digest(record)
    with pytest.raises(bmt.exceptions.ArgumentError, match='one explicit'):
        bmt.BindingSite.from_dict(record, experimental=True)


@pytest.mark.parametrize('name', ['S0.json', 'S3.json', 'rule.json'])
@pytest.mark.parametrize('style', ['original', 'sorted'])
def test_actual_original_01_records_keep_producer_and_history(name, style):
    manifest = json.loads((FROZEN / 'manifest.json').read_text())
    path = FROZEN / name
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == manifest['records'][name]['sha256']
    record = json.loads(raw)
    if style == 'sorted':
        record = json.loads(json.dumps(record, sort_keys=True))
    restored = bmt.BindingSite.from_dict(record, experimental=True)
    assert restored.to_dict() == record
    assert (
        restored.to_dict()['producer'] == manifest['records'][name]['original_producer']
    )
    assert restored.to_dict()['format_version'] == '0.1'
    assert restored.copy().to_dict() == record and path.read_bytes() == raw


@pytest.mark.parametrize('element', ['atom', 'group'])
def test_closed_signatures_and_admitted_role(element):
    with pytest.raises(UnknownArgumentError):
        declare(element, unknown_choice=True)
    with pytest.raises(bmt.exceptions.CapabilityMismatchError):
        declare(element, role='observed_binding')
