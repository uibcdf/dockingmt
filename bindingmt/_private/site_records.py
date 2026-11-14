"""Admission of the first coordinate-free site record; no molecular operations."""

import re
from collections.abc import Mapping
from numbers import Integral

import numpy as np

from bindingmt._private.interface_records import _digest, _require
from bindingmt._private.serialization import json_copy
from bindingmt._private.smonitor import CapabilityMismatchError


def text(value):
    return isinstance(value, str) and bool(value.strip())


def keys(value, expected, field):
    _require(
        isinstance(value, Mapping) and set(value) == set(expected),
        field,
        f'Use exactly these fields: {sorted(expected)}.',
    )


def capability(supported, name):
    if not supported:
        raise CapabilityMismatchError(
            capability=name, engine='bindingmt.site.declaration'
        )


def source_record(source):
    _require(
        isinstance(source, Mapping)
        and {'owner', 'id'} <= source.keys() <= {'owner', 'id', 'revision'}
        and text(source['owner'])
        and text(source['id'])
        and (source.get('revision') is None or text(source['revision'])),
        'source',
        'Declare owner/id and an optional nonempty revision; None means unknown.',
    )
    return json_copy({**source, 'revision': source.get('revision')}, 'source')


def sequence(value, field):
    _require(
        isinstance(value, (list, tuple)), field, 'Supply an ordered list or tuple.'
    )
    return list(value)


def scope_record(source_id, structures, states=None):
    if structures is None:
        _require(
            states is None,
            'chemical_state_indices',
            'States require selected structures.',
        )
        return {'kind': 'independent', 'source_id': source_id}
    structures = sequence(structures, 'structure_indices')
    _require(
        bool(structures) and all(type(i) is int and i >= 0 for i in structures),
        'structure_indices',
        'Declare a nonempty ordered source-structure axis of nonnegative integers.',
    )
    states = (
        [None] * len(structures)
        if states is None
        else sequence(states, 'chemical_state_indices')
    )
    _require(
        len(states) == len(structures)
        and all(i is None or type(i) is int and i >= 0 for i in states),
        'chemical_state_indices',
        'Align explicit nonnegative or unknown states with source-structure occurrences.',
    )
    known = {}
    for structure, state in zip(structures, states):
        if state is not None:
            _require(
                structure not in known or known[structure] == state,
                'chemical_state_indices',
                'Repeated references to one source structure cannot contradict its known state.',
            )
            known[structure] = state
    return {
        'kind': 'source_structures',
        'source_id': source_id,
        'source_structure_indices': structures,
        'occurrence_indices': list(range(len(structures))),
        'chemical_state_indices': states,
    }


def validate_scope(value, source_id):
    _require(isinstance(value, Mapping), 'scope', 'Declare a source scope.')
    if value.get('kind') == 'independent':
        expected = scope_record(source_id, None)
    else:
        capability(value.get('kind') == 'source_structures', 'site structural scope')
        expected = scope_record(
            source_id,
            value.get('source_structure_indices'),
            value.get('chemical_state_indices'),
        )
        occurrences = value.get('occurrence_indices')
        _require(
            isinstance(occurrences, list) and all(type(i) is int for i in occurrences),
            'scope',
            'Occurrence positions require integer values, without bool/float aliases.',
        )
    _require(
        value == expected,
        'scope',
        'Preserve original source scope and occurrence alignment.',
    )


def residue_records(residues):
    entries = []
    for entry in sequence(residues, 'residues'):
        _require(
            isinstance(entry, Mapping)
            and {'chain', 'id'} <= entry.keys() <= {'chain', 'id', 'insertion_code'}
            and (entry['chain'] is None or isinstance(entry['chain'], str))
            and text(entry['id'])
            and (
                entry.get('insertion_code') is None
                or isinstance(entry['insertion_code'], str)
            ),
            'residues',
            'Declare chain (string or unknown), string residue id and optional insertion code.',
        )
        normalized = {**entry, 'insertion_code': entry.get('insertion_code')}
        _require(
            normalized not in entries,
            'residues',
            'Duplicate source addresses are ambiguous.',
        )
        entries.append(normalized)
    return json_copy(entries, 'residues')


def membership_payload(indices, element):
    """Portable source indices, without a selection, bound check or atom expansion."""
    _require(text(element), 'element', 'Declare a molecular element string.')
    capability(element in ('atom', 'group'), 'site membership element')
    field = f'{element}_indices'
    _require(
        isinstance(indices, (list, tuple))
        or isinstance(indices, np.ndarray)
        and indices.ndim == 1
        and indices.dtype.kind in ('i', 'u'),
        field,
        'Use an ordered list, tuple or one-dimensional integer array.',
    )
    values = list(indices)
    _require(
        all(
            isinstance(i, Integral) and not isinstance(i, (bool, np.bool_)) and i >= 0
            for i in values
        ),
        field,
        'Source membership requires nonnegative integer indices without coercion.',
    )
    values = [int(i) for i in values]
    _require(len(set(values)) == len(values), field, 'Preserve unique source indices.')
    return {
        'element': element,
        'index_space': f'source_{element}_index',
        'source_indices': values,
        'resolution': {'state': 'declared', 'cause': 'source_not_checked'},
    }


def reference(value, current_id, *, definition=False):
    fields = {'record_id', 'content_sha256'} | (
        {'definition_key'} if definition else set()
    )
    keys(value, fields, 'reference')
    _require(
        text(value['record_id'])
        and value['record_id'] != current_id
        and isinstance(value['content_sha256'], str)
        and re.fullmatch('[0-9a-f]{64}', value['content_sha256']) is not None
        and (not definition or value['definition_key'] == 'definition'),
        'reference',
        'Retain an exact non-self original record/content/definition reference.',
    )


def validate(record):
    keys(
        record,
        {
            'format',
            'format_version',
            'experimental',
            'record_id',
            'content_sha256',
            'name',
            'context',
            'views',
            'definition',
            'evidence',
            'realization_coverage',
            'derivation',
            'extensions',
            'producer',
        },
        'record',
    )
    _require(
        record['format'] == 'bindingmt.binding_site'
        and record['format_version'] in ('0.1', '0.2', '0.3')
        and record['experimental'] is True,
        'format_version',
        'Explicit experimental bindingmt.binding_site version 0.1, 0.2 or 0.3 is required.',
    )
    _require(
        text(record['record_id']), 'record_id', 'Declare a nonempty record identity.'
    )
    _require(
        record['name'] is None or text(record['name']),
        'name',
        'Use a nonempty name or None.',
    )
    keys(record['context'], {'source'}, 'context')
    source = record['context']['source']
    _require(
        source == source_record(source),
        'source',
        'Preserve explicit source revision availability.',
    )
    source_id = source['id']
    views = record['views']
    _require(
        isinstance(views, list) and len(views) <= 1,
        'views',
        'Admit one source view or an unevaluated definition.',
    )
    _require(
        record['format_version'] not in ('0.2', '0.3') or len(views) == 1,
        'views',
        'Experimental 0.2/0.3 requires one explicit membership or geometry view.',
    )
    for view in views:
        keys(view, {'key', 'kind', 'role', 'scope', 'payload'}, 'view')
        capability(
            view['kind']
            in ('residue_annotation', 'molecular_membership', 'sphere', 'box'),
            'site view kind',
        )
        _require(
            (record['format_version'] == '0.1' and view['kind'] == 'residue_annotation')
            or (
                record['format_version'] == '0.2'
                and view['kind'] == 'molecular_membership'
            )
            or (
                record['format_version'] == '0.3' and view['kind'] in ('sphere', 'box')
            ),
            'format_version',
            'Residues require 0.1, source-index membership 0.2 and geometry 0.3.',
        )
        _require(
            view['key']
            == ('geometry' if record['format_version'] == '0.3' else 'membership'),
            'views',
            'Use the admitted membership/geometry view key.',
        )
        validate_scope(view['scope'], source_id)
        payload = view['payload']
        if record['format_version'] == '0.3':
            from bindingmt._private.site_geometry import validate_geometry

            capability(view['role'] == 'declared_geometry', 'site geometry role')
            validate_geometry(view['kind'], payload, view['scope'])
            continue
        if view['kind'] == 'molecular_membership':
            capability(view['role'] == 'declared_members', 'site view role')
            keys(
                payload,
                {'element', 'index_space', 'source_indices', 'resolution'},
                'payload',
            )
            _require(
                payload
                == membership_payload(payload['source_indices'], payload['element']),
                'membership',
                'Preserve element, original source index space, order and declared resolution.',
            )
            continue
        capability(view['role'] == 'annotated_members', 'site view role')
        keys(payload, {'address_space', 'entries', 'resolution'}, 'payload')
        capability(
            payload['address_space'] == 'author_residue', 'site residue address space'
        )
        _require(
            payload['entries'] == residue_records(payload['entries']),
            'residues',
            'Preserve explicit address fields.',
        )
        _require(
            payload['resolution']
            == {'state': 'unresolved', 'cause': 'no_correspondence_supplied'},
            'resolution',
            'Do not claim molecular resolution from annotations.',
        )
    definition = record['definition']
    keys(
        definition,
        {
            'key',
            'claim',
            'criterion',
            'participants',
            'views',
            'scope',
            'evidence_refs',
            'binding_support',
        },
        'definition',
    )
    _require(
        definition['key'] == 'definition'
        and text(definition['claim'])
        and isinstance(definition['criterion'], Mapping)
        and text(definition['criterion'].get('kind'))
        and definition['participants'] == [source_id]
        and definition['views'] == [v['key'] for v in views]
        and definition['binding_support'] == 'unknown',
        'definition',
        'Declare the claim/criterion without inferred binding support or molecular membership.',
    )
    validate_scope(definition['scope'], source_id)
    _require(
        all(v['scope'] == definition['scope'] for v in views),
        'scope',
        'Keep annotation and definition scope aligned in this profile.',
    )
    evidence = record['evidence']
    _require(isinstance(evidence, list), 'evidence', 'Use an ordered evidence list.')
    evidence_keys = []
    for item in evidence:
        keys(
            item,
            {
                'key',
                'kind',
                'source',
                'observation',
                'attribution',
                'participants',
                'views',
                'scope',
                'original_claim_ref',
            },
            'evidence',
        )
        _require(
            text(item['key']) and item['key'] not in evidence_keys,
            'evidence',
            'Evidence keys must be unique and nonempty.',
        )
        evidence_keys.append(item['key'])
        capability(item['kind'] == 'source_annotation', 'site evidence kind')
        _require(
            item['source'] == source_record(item['source']),
            'evidence',
            'Preserve original annotation source.',
        )
        _require(
            all(
                isinstance(item[k], Mapping) and bool(item[k])
                for k in ('observation', 'attribution')
            )
            and item['participants'] == [source_id]
            and item['views'] == definition['views'],
            'evidence',
            'Preserve declared observations, attribution and admitted view/participant scope.',
        )
        validate_scope(item['scope'], source_id)
        reference(item['original_claim_ref'], record['record_id'], definition=True)
    refs = definition['evidence_refs']
    _require(
        isinstance(refs, list)
        and all(text(k) for k in refs)
        and len(set(refs)) == len(refs)
        and set(refs) <= set(evidence_keys),
        'evidence_refs',
        'Cite known observations explicitly and without duplicates.',
    )
    _require(
        record['realization_coverage'] == {'state': 'not_requested'},
        'realization_coverage',
        'Declaration is not an evaluated realization or ensemble.',
    )
    derivation = record['derivation']
    keys(derivation, {'parents', 'kind', 'reason'}, 'derivation')
    parents = derivation['parents']
    _require(
        isinstance(parents, list) and len(parents) <= 1,
        'derivation',
        'Preserve at most one immediate parent.',
    )
    for parent in parents:
        reference(parent, record['record_id'])
    _require(
        (
            bool(parents)
            and derivation['kind'] in ('definition_revision', 'evidence_addition')
            and text(derivation['reason'])
        )
        or (
            not parents and derivation['kind'] is None and derivation['reason'] is None
        ),
        'derivation',
        'Retain the explicit derivation kind and reason with its parent.',
    )
    _require(
        isinstance(record['extensions'], Mapping),
        'extensions',
        'Use named optional extensions.',
    )
    for name, extension in record['extensions'].items():
        _require(
            text(name) and ('.' in name or ':' in name),
            'extensions',
            'Namespace optional owner data.',
        )
        keys(extension, {'required', 'payload'}, 'extensions')
        capability(extension['required'] is False, 'required site extension semantics')
    keys(record['producer'], {'library', 'bindingmt_version', 'operation'}, 'producer')
    _require(
        record['producer']['library'] == 'bindingmt'
        and all(
            text(record['producer'][k]) for k in ('bindingmt_version', 'operation')
        ),
        'producer',
        'Preserve the original declaration writer identity.',
    )
    _require(
        record['content_sha256'] == _digest(record),
        'content_sha256',
        'Site content digest mismatch.',
    )
