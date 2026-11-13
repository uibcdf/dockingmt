"""Optional native characterization annotations and their offline semantics."""

from collections.abc import Mapping
from uuid import uuid4

import numpy as np
import pyunitwizard as puw

from bindingmt._private.interface_burial import RADII_FIELD
from bindingmt._private.interface_burial import participant_order as surface_order
from bindingmt._private.interface_contacts import length_values
from bindingmt._private.interface_contacts import participant_order as contact_order
from bindingmt._private.interface_context import _geometry_digest, source_metadata
from bindingmt._private.interface_records import _digest, _require
from bindingmt._private.serialization import json_copy

KEY = 'bindingmt.interface_characterizations'
DEFINITION = 'bindingmt.native_characterization_annotation@1'


def _context(record):
    views = [
        a['native_observation']
        for a in record['analyses'].values()
        if a['authority'] == 'molsysmt_native'
    ]
    _require(
        record['format_version'] in ('0.4', '0.5') and bool(views),
        'characterizations',
        'Use the admitted native ionic recipient profile.',
    )
    return views[0]['context']


def _evidence(record, context, participant):
    """Validate owner-derived axes and compose witness references; do no geometry."""
    from bindingmt.core.interface import BindingInterface

    _require(
        isinstance(record, Mapping) and record.get('format_version') in ('0.2', '0.3'),
        'characterizations',
        'Supply native contact/surface results, not nested annotation profiles.',
    )
    result = BindingInterface.from_dict(record, experimental=True)
    contact = result.contact_calculation
    calculation = contact or result.surface_calculation
    _require(
        calculation is not None,
        'characterizations',
        'A complete native calculation is required.',
    )
    native = calculation['context']
    members = calculation['participants']
    _require(
        isinstance(participant, str) and bool(participant),
        'participant',
        'Select a named recipient participant.',
    )
    _require(
        participant in context['participants'] and participant in members,
        'participant',
        'Retain the same explicit target label in every characterization.',
    )
    group = next(group for group in context['grouping'] if participant in group)
    _require(
        group == [participant],
        'participant',
        'The target must be a whole binary side in this profile.',
    )
    expected = [
        a
        for group in context['grouping']
        if participant not in group
        for name in group
        for a in context['participants'][name]
    ]
    target = members[participant]
    other = next(p for name, p in members.items() if name != participant)
    _require(
        set(target['source_atom_indices']) == set(context['participants'][participant])
        and set(other['source_atom_indices']) == set(expected)
        and all(
            p['local_atom_indices'] == p['source_atom_indices']
            for p in members.values()
        )
        and native['source_id'] == context['source_id']
        and native['structure_index']
        == native['source_structure_index']
        == context['structure_index']
        and native['structure_chemical_state_index'] == context['chemical_state_index'],
        'characterizations',
        'Require the same admitted identity axes, grouping, source/frame/state.',
    )
    if not contact:
        _require(
            calculation['numerical']['burial_usable'] is True,
            'characterizations',
            'Inconsistent burial is inspectable but not admitted as usable annotation.',
        )
    side = (
        contact_order(calculation).index(participant)
        if contact
        else surface_order(calculation).index(participant)
    )
    witnesses = []
    for position, (local, source) in enumerate(
        zip(target['local_atom_indices'], target['source_atom_indices'])
    ):
        refs = (
            [
                i
                for i, pair in enumerate(calculation['source_pairs'])
                if pair[side] == source
            ]
            if contact
            else [position]
        )
        witnesses.append(
            {
                'source_atom_index': source,
                'local_atom_index': local,
                'witness_indices': refs,
            }
        )
    return calculation, {
        'kind': 'contact_pair' if contact else 'atomic_loss_position',
        'atoms': witnesses,
    }


def validate_annotation(annotation, record):
    """Validate optional binding evidence without native/asset lookup or imports."""
    _require(
        isinstance(annotation, Mapping)
        and set(annotation)
        == {
            'definition',
            'source_interface_record_id',
            'source_context_sha256',
            'participant',
            'characterizations',
            'query_reference',
            'scope',
            'query_semantics',
            'source_assessment',
        },
        KEY,
        'Use the complete optional characterization annotation.',
    )
    context = _context(record)
    _require(
        annotation['definition'] == DEFINITION
        and annotation['scope'] == 'participant_evidence'
        and annotation['query_semantics'] == 'unchanged'
        and annotation['source_assessment'] == 'historical_checked_at_annotation'
        and annotation['source_context_sha256'] == _digest(context)
        and isinstance(annotation['source_interface_record_id'], str)
        and bool(annotation['source_interface_record_id'])
        and annotation['source_interface_record_id'] != record['record_id'],
        KEY,
        'Preserve the original annotation identity, scope and historical checks.',
    )
    entries = annotation['characterizations']
    _require(
        isinstance(entries, Mapping) and bool(entries),
        KEY,
        'Retain nonempty named characterization evidence.',
    )
    for label, entry in entries.items():
        _require(
            isinstance(label, str)
            and bool(label.strip())
            and isinstance(entry, Mapping)
            and set(entry)
            == {'record', 'record_id', 'content_sha256', 'definition', 'contributors'},
            KEY,
            'Retain exact original records, definitions and contributor references.',
        )
        calculation, refs = _evidence(
            entry['record'], context, annotation['participant']
        )
        _require(
            entry['record_id'] == entry['record']['record_id']
            and entry['content_sha256'] == entry['record']['content_sha256']
            and entry['definition'] == calculation['definition']
            and entry['contributors'] == refs,
            KEY,
            'Keep all source-aligned atomic witnesses, including evaluated-zero members.',
        )
    query = annotation['query_reference']
    if query is not None:
        _require(
            isinstance(query, Mapping)
            and set(query) == {'authority', 'reference', 'context_assessment'}
            and query['authority'] == 'caller_declared'
            and query['context_assessment'] == 'not_performed',
            KEY,
            'A supplied query reference gains no new construction/context authority.',
        )
        ref = query['reference']
        _require(
            isinstance(ref, Mapping)
            and set(ref) == {'uri', 'sha256'}
            and isinstance(ref['uri'], str)
            and bool(ref['uri'].strip())
            and isinstance(ref['sha256'], str)
            and len(ref['sha256']) == 64
            and all(c in '0123456789abcdef' for c in ref['sha256']),
            KEY,
            'Use an exact caller-owned saved query reference; no file lookup occurs.',
        )


def _check_source(msm, molecular_system, calculation, context):
    members = calculation['participants']
    names = (
        surface_order(calculation)
        if 'numerical' in calculation
        else contact_order(calculation)
    )
    axes = [members[name]['local_atom_indices'] for name in names]
    _, groups, state, _ = source_metadata(
        msm,
        molecular_system,
        axes,
        context['structure_index'],
        context['n_atoms'],
        None,
        None,
    )
    _require(
        groups == [members[name]['group_indices'] for name in names]
        and state == context['chemical_state_index'],
        'molecular_system',
        'Current group/state correspondence differs from the characterization.',
    )
    selected = [a for axis in axes for a in axis]
    surface = 'numerical' in calculation
    if surface:
        selected.sort()
        for p in members.values():
            radii = msm.physchem.get_atomic_radius(
                molecular_system, selection=p['local_atom_indices'], definition='vdw'
            )
            _require(
                np.array_equal(
                    np.asarray(puw.get_value(radii, to_unit='nm')),
                    length_values(p['radii'], RADII_FIELD),
                ),
                'molecular_system',
                'Current public radii differ from the recorded surface model.',
            )
    _require(
        _geometry_digest(msm, molecular_system, selected, context['structure_index'])
        == calculation['context']['geometry_sha256_nm_float64'],
        'molecular_system',
        'Current selected geometry differs from the characterization.',
    )


def with_characterizations(
    interface, molecular_system, characterizations, participant, query_ref
):
    """Check admitted source facts and compose native evidence without query access."""
    import molsysmt as msm

    from bindingmt.chemical_interfaces import _recheck

    _require(
        isinstance(characterizations, Mapping)
        and bool(characterizations)
        and all(isinstance(k, str) and bool(k.strip()) for k in characterizations),
        'characterizations',
        'Supply a nonempty named mapping of native results.',
    )
    record = interface.to_dict()
    _require(
        KEY not in record['extensions'],
        KEY,
        'Start from an unannotated recipient; replacement is not admitted.',
    )
    context, _ = _recheck(interface, molecular_system)
    entries = {}
    for label, result in characterizations.items():
        from bindingmt.core.interface import BindingInterface

        _require(
            isinstance(result, BindingInterface),
            'characterizations',
            'Supply actual native BindingInterface results.',
        )
        original = result.to_dict()
        calculation, refs = _evidence(original, context, participant)
        _check_source(msm, molecular_system, calculation, context)
        entries[label] = {
            'record': original,
            'record_id': result.record_id,
            'content_sha256': original['content_sha256'],
            'definition': calculation['definition'],
            'contributors': refs,
        }
    _recheck(interface, molecular_system)
    for entry in entries.values():
        calculation, _ = _evidence(entry['record'], context, participant)
        _check_source(msm, molecular_system, calculation, context)
    annotation = {
        'definition': DEFINITION,
        'source_interface_record_id': interface.record_id,
        'source_context_sha256': _digest(context),
        'participant': participant,
        'characterizations': entries,
        'query_reference': None
        if query_ref is None
        else {
            'authority': 'caller_declared',
            'reference': json_copy(query_ref, 'query_ref'),
            'context_assessment': 'not_performed',
        },
        'scope': 'participant_evidence',
        'query_semantics': 'unchanged',
        'source_assessment': 'historical_checked_at_annotation',
    }
    record['extensions'][KEY] = annotation
    record['record_id'] = str(uuid4())
    record['derivation'] = {
        'parents': [interface.record_id],
        'reason': 'annotate participant characterization evidence without changing query semantics',
    }
    record['content_sha256'] = _digest(record)
    return type(interface)(record, experimental=True)
