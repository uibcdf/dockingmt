"""Source addresses, structural scope and original evidence survive site revisions."""

import json
from copy import deepcopy
from dataclasses import FrozenInstanceError

import pytest
from argdigest import UnknownArgumentError

import bindingmt as bmt
from bindingmt._private.interface_records import _digest

SOURCE = {'owner': 'caller', 'id': 'target-A', 'revision': 'r1'}
ADDRESSES = [
    {'chain': 'A', 'id': '012', 'insertion_code': ''},
    {'chain': 'A', 'id': '12', 'insertion_code': 'A'},
    {'chain': None, 'id': '-1'},
]


def annotation(**options):
    return bmt.BindingSite.from_residues(
        **{
            'source': deepcopy(SOURCE),
            'address_space': 'author_residue',
            'residues': deepcopy(ADDRESSES),
            **options,
        }
    )


def annotate(site, **options):
    return site.with_evidence(
        **{
            'key': 'annotation-7',
            'source': {
                'owner': 'external.curator',
                'id': 'annotation-7',
                'revision': 'v1',
            },
            'observation': {
                'reported_members': 'membership',
                'binding_support': 'unknown',
            },
            'attribution': {'producer': 'original-curator', 'version': '1'},
            **options,
        }
    )


def restore(record):
    record['content_sha256'] = _digest(record)
    return bmt.BindingSite.from_dict(record, experimental=True)


def test_annotation_retains_exact_addresses_unknowns_and_no_molecular_claim():
    site = annotation()
    assert site.views[0]['payload']['entries'] == [
        ADDRESSES[0],
        ADDRESSES[1],
        {**ADDRESSES[2], 'insertion_code': None},
    ]
    assert site.views[0]['scope'] == {'kind': 'independent', 'source_id': 'target-A'}
    report = site.inspect()
    assert report['membership'] == {'state': 'unresolved', 'entry_count': 3}
    assert (
        report['binding_support'] == 'unknown'
        and report['molecular_resolution'] == 'not_performed'
    )
    assert report['realization_coverage'] == {'state': 'not_requested'}
    assert (
        not report['capabilities']['molecular_projection']
        and not report['capabilities']['domain_placement']
    )
    assert (
        site.site_id == site.record_id
        and 'Binding support is unknown' in site.describe()
    )


def test_definition_only_and_declared_empty_annotation_are_different():
    rule = bmt.BindingSite.from_definition(
        source=SOURCE,
        claim='Candidate region',
        criterion={'kind': 'caller_rule', 'rule': 'unevaluated'},
    )
    empty = annotation(residues=[])
    assert rule.views == []
    assert rule.inspect()['membership'] == {
        'state': 'not_supplied',
        'entry_count': None,
    }
    assert empty.inspect()['membership'] == {
        'state': 'declared_empty',
        'entry_count': 0,
    }
    assert all(x.inspect()['binding_support'] == 'unknown' for x in [rule, empty])
    assert rule.definition['evidence_refs'] == [] and rule.evidence == []


def test_unknown_revision_chain_and_insertion_are_not_empty_strings():
    site = annotation(
        source={'owner': 'caller', 'id': 'target-A'},
        residues=[
            {'chain': '', 'id': '12', 'insertion_code': ''},
            {'chain': None, 'id': '12', 'insertion_code': None},
        ],
    )
    assert site.context['source']['revision'] is None
    entries = site.views[0]['payload']['entries']
    assert entries[0]['chain'] == entries[0]['insertion_code'] == ''
    assert entries[1]['chain'] is entries[1]['insertion_code'] is None


def test_repeated_structure_occurrences_and_separate_evidence_scope(tmp_path):
    site = annotation(structure_indices=[2, 0, 2], chemical_state_indices=[1, None, 1])
    scope = site.definition['scope']
    site = annotate(site, structure_indices=[0])
    site.save(tmp_path / 'site.json')
    restored = bmt.BindingSite.read(tmp_path / 'site.json', experimental=True)
    assert restored.definition['scope'] == scope
    assert scope['source_structure_indices'] == [2, 0, 2] and scope[
        'occurrence_indices'
    ] == [0, 1, 2]
    assert scope['chemical_state_indices'] == [1, None, 1]
    assert restored.evidence[0]['scope']['source_structure_indices'] == [0]
    assert (
        restored.inspect()['evidence_count'] == 1
        and restored.inspect()['realization_coverage']['state'] == 'not_requested'
    )


def test_revisions_preserve_original_claim_and_observation():
    original = annotation()
    observed = annotate(original)
    evidence = observed.evidence
    assert evidence[0]['original_claim_ref'] == original.definition_ref
    assert observed.definition['evidence_refs'] == ['annotation-7']
    revised = observed.with_definition(
        claim='Annotation only',
        criterion=observed.definition['criterion'],
        reason='Revise interpretation',
    )
    assert revised.evidence == evidence and revised.definition['evidence_refs'] == []
    assert revised.record_id not in (original.record_id, observed.record_id)
    assert revised.to_dict()['derivation']['parents'] == [
        {k: v for k, v in observed.definition_ref.items() if k != 'definition_key'}
    ]
    cited = revised.with_definition(
        claim='Cite original annotation',
        criterion=revised.definition['criterion'],
        evidence_refs=['annotation-7'],
        reason='New interpretation without a new observation',
    )
    assert cited.evidence == evidence and cited.definition['evidence_refs'] == [
        'annotation-7'
    ]
    assert (
        cited.inspect()['evidence_count'] == 1
        and cited.inspect()['binding_support'] == 'unknown'
    )
    assert original.evidence == [] and original.definition['evidence_refs'] == []


def test_independent_definition_with_structure_specific_evidence_stays_independent():
    site = annotate(annotation(), structure_indices=[2, 0, 2])
    assert site.definition['scope']['kind'] == 'independent'
    assert site.evidence[0]['scope']['occurrence_indices'] == [0, 1, 2]
    assert site.inspect()['realization_coverage']['state'] == 'not_requested'


def test_inputs_properties_and_exact_references_are_detached(tmp_path):
    addresses = deepcopy(ADDRESSES)
    source = deepcopy(SOURCE)
    site = annotation(source=source, residues=addresses)
    saved = site.to_dict()
    source['id'] = 'edited'
    addresses[0]['id'] = 'edited'
    for value in [
        site.context,
        site.views,
        site.definition,
        site.definition_ref,
        site.evidence,
        site.inspect(),
        site.to_dict(),
    ]:
        if isinstance(value, list):
            value.append('edited')
        else:
            value['edited'] = True
    assert site.to_dict() == saved and site.copy().to_dict() == saved
    site.save(tmp_path / 'site.json')
    assert (
        bmt.BindingSite.read(tmp_path / 'site.json', experimental=True).to_dict()
        == saved
    )
    with pytest.raises(FrozenInstanceError):
        site._json = '{}'


def test_optional_extension_is_preserved_without_lookup(tmp_path):
    opaque = {
        'topomt.future': {
            'required': False,
            'payload': {'uri': '/absent/owner.output', 'opaque': [2, 0, 2]},
        }
    }
    site = annotation(extensions=opaque)
    site.save(tmp_path / 'site.json')
    assert (
        bmt.BindingSite.read(tmp_path / 'site.json', experimental=True).to_dict()[
            'extensions'
        ]
        == opaque
    )
    assert site.inspect()['asset_access'] == 'not_checked'
    opaque['topomt.future']['payload']['uri'] = 'edited'
    assert site.to_dict()['extensions'] != opaque


@pytest.mark.parametrize(
    'source',
    [
        None,
        {},
        {'id': 'A'},
        {'owner': 'caller', 'id': ''},
        {'owner': 'caller', 'id': 1},
        {'owner': 'caller', 'id': 'A', 'revision': ''},
        {'owner': 'caller', 'id': 'A', 'extra': True},
    ],
)
def test_invalid_sources_are_not_guessed(source):
    with pytest.raises(bmt.exceptions.ArgumentError):
        annotation(source=source)


@pytest.mark.parametrize(
    'residues',
    [
        None,
        'A:12',
        {1, 2},
        [{'chain': 'A', 'id': 12}],
        [{'chain': True, 'id': '12'}],
        [{'chain': 'A', 'id': '12', 'insertion_code': 1}],
        [{'chain': 'A', 'id': '12', 'group_index': 0}],
        [ADDRESSES[0], ADDRESSES[0]],
    ],
)
def test_addresses_are_not_coerced_or_duplicated(residues):
    with pytest.raises(bmt.exceptions.ArgumentError):
        annotation(residues=residues)


@pytest.mark.parametrize(
    'options',
    [
        {'structure_indices': []},
        {'structure_indices': True},
        {'structure_indices': [-1]},
        {'structure_indices': [True]},
        {'structure_indices': [0.0]},
        {'chemical_state_indices': [0]},
        {'structure_indices': [2, 0, 2], 'chemical_state_indices': [1, 0, 2]},
        {'structure_indices': [2, 0], 'chemical_state_indices': [0]},
        {'structure_indices': [2], 'chemical_state_indices': [True]},
    ],
)
def test_invalid_or_contradictory_structure_scope_refuses(options):
    with pytest.raises(bmt.exceptions.ArgumentError):
        annotation(**options)


@pytest.mark.parametrize(
    'options',
    [
        {'address_space': 'unrecognized'},
        {'role': 'binding_proven'},
        {'extensions': {'owner.critical': {'required': True, 'payload': {}}}},
    ],
)
def test_unsupported_semantics_refuse_without_silent_downgrade(options):
    with pytest.raises(bmt.exceptions.CapabilityMismatchError):
        annotation(**options)


@pytest.mark.parametrize(
    'claim,criterion',
    [
        ('', {'kind': 'rule'}),
        ('claim', {}),
        ('claim', {'kind': ''}),
        ('claim', {'kind': 'rule', 'value': float('nan')}),
        ('claim', {'kind': 'rule', 'opaque': object()}),
    ],
)
def test_invalid_or_nonfinite_definition_data_refuses(claim, criterion):
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingSite.from_definition(source=SOURCE, claim=claim, criterion=criterion)


def test_unknown_citations_duplicate_evidence_and_empty_attribution_refuse():
    site = annotate(annotation())
    with pytest.raises(bmt.exceptions.ArgumentError):
        annotate(site)
    for refs in [['missing'], ['annotation-7', 'annotation-7'], 'annotation-7']:
        with pytest.raises(bmt.exceptions.ArgumentError):
            site.with_definition(
                claim='new',
                criterion={'kind': 'rule'},
                reason='explicit',
                evidence_refs=refs,
            )
    with pytest.raises(bmt.exceptions.ArgumentError):
        annotate(annotation(), attribution={})
    with pytest.raises(bmt.exceptions.ArgumentError):
        site.with_definition(claim='new', criterion={'kind': 'rule'}, reason='')


@pytest.mark.parametrize('style', ['sorted', 'reversed'])
def test_object_key_order_is_not_scientific_order(style):
    original = annotate(annotation(structure_indices=[2, 0, 2]))
    raw = original.to_dict()
    if style == 'sorted':
        changed = json.loads(json.dumps(raw, sort_keys=True))
    else:

        def reverse(value):
            if isinstance(value, dict):
                return {k: reverse(v) for k, v in reversed(list(value.items()))}
            if isinstance(value, list):
                return [reverse(v) for v in value]
            return value

        changed = reverse(raw)
    assert bmt.BindingSite.from_dict(changed, experimental=True).to_dict() == raw


@pytest.mark.parametrize(
    'field,value',
    [
        ('format', 'unknown'),
        ('format_version', None),
        ('format_version', '1.0'),
        ('experimental', False),
        ('record_id', ''),
        ('realization_coverage', {'state': 'evaluated'}),
        ('coordinates', []),
        ('content_sha256', '0' * 64),
    ],
)
def test_missing_tampered_and_unsupported_record_fields_refuse(field, value):
    record = annotation().to_dict()
    record[field] = value
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingSite.from_dict(record, experimental=True)


@pytest.mark.parametrize(
    'path,value',
    [
        (('definition', 'evidence_refs'), ['absent']),
        (('definition', 'binding_support'), 'confirmed'),
        (('definition', 'participants'), ['other']),
        (('definition', 'scope', 'source_id'), 'other'),
        (('definition', 'scope', 'occurrence_indices'), [False, True, 2]),
        (('evidence', 0, 'original_claim_ref', 'definition_key'), 'latest'),
        (('views', 0, 'payload', 'entries'), [{'chain': 'A', 'id': '12'}]),
    ],
)
def test_recomputed_digest_does_not_hide_semantic_inconsistency(path, value):
    record = annotate(annotation(structure_indices=[2, 0, 2])).to_dict()
    target = record
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(bmt.exceptions.ArgumentError):
        restore(record)


def test_opt_in_duplicate_keys_and_exclusive_file_lifecycle(tmp_path):
    site = annotation()
    path = tmp_path / 'site.json'
    site.save(path)
    raw = path.read_bytes()
    with pytest.raises(FileExistsError):
        site.save(path)
    assert path.read_bytes() == raw
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingSite.read(path)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingSite.from_dict(site.to_dict())
    record = site.to_dict()
    record.pop('format_version')
    with pytest.raises(bmt.exceptions.ArgumentError):
        restore(record)
    duplicate = tmp_path / 'duplicate.json'
    duplicate.write_text('{"format":"one","format":"two"}')
    with pytest.raises(bmt.exceptions.ArgumentError, match='Duplicate'):
        bmt.BindingSite.read(duplicate, experimental=True)
    with pytest.raises(UnknownArgumentError):
        annotation(unknown_option=True)
