"""Portable contact evidence; no molecular operations or geometry kernels."""

from collections.abc import Mapping

import numpy as np
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

from bindingmt._private.interface_records import _names_on_axes, _require

DEFINITION = 'bindingmt.cartesian_atomic_contacts@1'
CUTOFF_FIELD = 'bindingmt.contacts.cutoff'
DISTANCES_FIELD = 'bindingmt.contacts.distances'
DISTANCE_VERIFICATION_RTOL = float(8 * np.finfo(np.float64).eps)


def distance_statuses(distances, cutoff):
    """Verify stored distances; never choose or change owner contact membership."""
    status = []
    for value in distances:
        if value <= cutoff:
            status.append('consistent')
        else:
            _require(
                np.isclose(value, cutoff, rtol=DISTANCE_VERIFICATION_RTOL, atol=0),
                'distances',
                'A recorded contact distance exceeds its declared conversion bound.',
            )
            status.append('within_conversion_roundoff')
    return status


def length_record(quantity, field):
    return QuantityRecord.from_quantity(quantity, field=field).to_dict()


def length_values(record, field):
    quantity = QuantityRecord.from_dict(record).to_quantity(
        field=field, unit='nm', dimensionality={'[L]': 1}, form='pint'
    )
    values = np.asarray(puw.get_value(quantity, to_unit='nm'))
    _require(
        np.isrealobj(values) and np.isfinite(values).all() and (values >= 0).all(),
        field,
        'Use finite nonnegative lengths.',
    )
    return values


def _indices(values):
    return isinstance(values, list) and all(type(v) is int and v >= 0 for v in values)


def participant_order(calculation):
    """Read the endpoint order from saved public contact-call axes."""
    calls = calculation.get('calls')
    _require(
        isinstance(calls, list)
        and bool(calls)
        and isinstance(calls[0], Mapping)
        and isinstance(calls[0].get('options'), Mapping),
        'calls',
        'Preserve the explicit contact operation axes.',
    )
    options = calls[0]['options']
    return _names_on_axes(
        calculation.get('participants'),
        [options.get('selection'), options.get('selection_2')],
    )


def validate_calculation(value):
    required = {
        'definition',
        'analysis_id',
        'context',
        'participants',
        'cutoff',
        'distances',
        'local_pairs',
        'source_pairs',
        'group_pairs',
        'group_contributors',
        'group_coverage',
        'distance_consistency',
        'calls',
        'producer',
        'resources',
        'attribution',
    }
    _require(
        isinstance(value, Mapping) and set(value) == required,
        'calculation',
        'Use the complete admitted contact calculation record.',
    )
    _require(
        value['definition'] == DEFINITION,
        'definition',
        'Unsupported contact definition.',
    )
    _require(
        isinstance(value['analysis_id'], str) and bool(value['analysis_id']),
        'analysis_id',
        'Name the composed calculation.',
    )
    context = value['context']
    _require(
        isinstance(context, Mapping)
        and context.get('coordinate_policy') == 'cartesian'
        and context.get('pbc') is False
        and isinstance(context.get('source_id'), str)
        and bool(context['source_id']),
        'context',
        'Preserve the source and Cartesian context.',
    )
    for key in ('structure_index', 'source_structure_index'):
        _require(
            type(context.get(key)) is int and context[key] >= 0,
            'context',
            'Preserve structure correspondence.',
        )
    participants = value['participants']
    _require(
        isinstance(participants, Mapping) and len(participants) == 2,
        'participants',
        'Preserve two exact endpoint axes.',
    )
    axes = []
    source_axes = []
    mappings = []
    groups = []
    names = participant_order(value)
    for name in names:
        participant = participants[name]
        _require(
            isinstance(name, str) and bool(name), 'participants', 'Use named endpoints.'
        )
        _require(
            isinstance(participant, Mapping)
            and set(participant)
            == {'local_atom_indices', 'source_atom_indices', 'group_indices'},
            'participants',
            'Preserve exact local/source/group axes.',
        )
        local, source, group = (
            participant[k]
            for k in ('local_atom_indices', 'source_atom_indices', 'group_indices')
        )
        _require(
            _indices(local)
            and local
            and len(set(local)) == len(local)
            and _indices(source)
            and len(set(source)) == len(source)
            and len(source) == len(local)
            and isinstance(group, list)
            and len(group) == len(local)
            and all(g is None or type(g) is int and g >= 0 for g in group),
            'participants',
            'Use unique aligned atom axes and actual optional group indices.',
        )
        axes.append(set(local))
        source_axes.append(set(source))
        mappings.append(dict(zip(local, source)))
        groups.append(dict(zip(local, group)))
    _require(
        not axes[0] & axes[1] and not source_axes[0] & source_axes[1],
        'participants',
        'Endpoint populations must be disjoint.',
    )
    cutoff = length_values(value['cutoff'], CUTOFF_FIELD)
    distances = length_values(value['distances'], DISTANCES_FIELD)
    _require(cutoff.shape == (), 'cutoff', 'Use one scalar cutoff.')
    pairs, originals = value['local_pairs'], value['source_pairs']
    _require(
        isinstance(pairs, list)
        and isinstance(originals, list)
        and len(pairs) == len(originals)
        and distances.shape == (len(pairs),),
        'calculation',
        'Pairs, distances and original labels must align.',
    )
    seen = set()
    expected_groups = {}
    for index, (pair, original) in enumerate(zip(pairs, originals)):
        _require(
            _indices(pair)
            and len(pair) == 2
            and _indices(original)
            and len(original) == 2,
            'calculation',
            'Use two exact endpoint indices per pair.',
        )
        a, b = pair
        _require(
            a in axes[0] and b in axes[1] and tuple(pair) not in seen,
            'calculation',
            'Every contact is one unique cross-participant pair.',
        )
        _require(
            original == [mappings[0][a], mappings[1][b]],
            'calculation',
            'Source labels disagree with the declared map.',
        )
        seen.add(tuple(pair))
        group_pair = (groups[0][a], groups[1][b])
        if None not in group_pair:
            expected_groups.setdefault(group_pair, []).append(index)
    _require(
        value['group_pairs'] == [list(p) for p in expected_groups]
        and value['group_contributors'] == list(expected_groups.values()),
        'group_pairs',
        'Group reduction must retain every admitted atomic witness.',
    )
    _require(
        value['distance_consistency']
        == {
            'relative_bound': DISTANCE_VERIFICATION_RTOL,
            'status': distance_statuses(distances, cutoff),
            'changes_contact_membership': False,
        },
        'distance_consistency',
        'Preserve raw distances and the separate unit-conversion verification bound.',
    )
    complete_groups = all(
        g is not None for p in participants.values() for g in p['group_indices']
    )
    _require(
        value['group_coverage'] == ('complete' if complete_groups else 'partial'),
        'group_coverage',
        'Unknown group correspondence is not completed zero.',
    )
    _require(
        isinstance(value['calls'], list)
        and len(value['calls']) == 2
        and all(isinstance(c, Mapping) for c in value['calls'])
        and [c.get('operation') for c in value['calls']]
        == ['molsysmt.structure.get_contacts', 'molsysmt.structure.get_distances'],
        'calls',
        'Preserve the actual required molecular operations.',
    )
    for call in value['calls']:
        options = call.get('options', {})
        _require(
            options.get('pairs') is False
            and options.get('pbc') is False
            and options.get('use_gpu') is False
            and options.get('parallel') is False
            and options.get('num_threads') == 1,
            'calls',
            'Unsupported execution profile.',
        )
        endpoints = [participants[name] for name in names]
        _require(
            options.get('selection') == endpoints[0]['local_atom_indices']
            and options.get('selection_2') == endpoints[1]['local_atom_indices']
            and options.get('structure_indices') == [context['structure_index']],
            'calls',
            'Calculation options disagree with the retained axes.',
        )
    _require(
        value['calls'][0]['options'].get('cell_list') is False
        and value['calls'][0]['options'].get('threshold_record') == value['cutoff'],
        'calls',
        'Preserve the actual dense route and its cutoff.',
    )
    for field in ('producer', 'resources', 'attribution'):
        _require(
            isinstance(value[field], Mapping) and bool(value[field]),
            field,
            'Preserve calculation provenance.',
        )
    resources = value['resources']
    candidate_count = len(endpoints[0]['local_atom_indices']) * len(
        endpoints[1]['local_atom_indices']
    )
    _require(
        resources.get('candidate_pairs') == candidate_count
        and type(resources.get('max_dense_pairs')) is int
        and candidate_count <= resources['max_dense_pairs']
        and resources.get('route') == 'explicit_dense_cartesian_cpu_one'
        and resources.get('is_ram_reservation') is False,
        'resources',
        'Preserve candidate counts and the actual admitted route.',
    )


def footprint_payload(calculation, participant):
    """Reduce actual pair evidence, preserving canonical source/aligned local axes."""
    names = participant_order(calculation)
    _require(
        participant in names, 'participant', 'Select a calculated participant name.'
    )
    side = names.index(participant)
    witnesses = {}
    for index, (source, local) in enumerate(
        zip(calculation['source_pairs'], calculation['local_pairs'])
    ):
        entry = witnesses.setdefault(
            source[side], {'local': local[side], 'contributors': []}
        )
        entry['contributors'].append(index)
    source_indices = sorted(witnesses)
    return {
        'participant': participant,
        'source_atom_indices': source_indices,
        'local_atom_indices': [witnesses[i]['local'] for i in source_indices],
        'contributors': [witnesses[i]['contributors'] for i in source_indices],
        'value_state': 'evaluated_nonempty' if source_indices else 'evaluated_empty',
    }
