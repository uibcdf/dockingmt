"""Typed portable surface evidence and binding-specific arithmetic; no geometry."""

from collections.abc import Mapping

import numpy as np
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

from bindingmt._private.interface_contacts import length_record, length_values
from bindingmt._private.interface_records import _names_on_axes, _require

DEFINITION = 'bindingmt.cartesian_sasa_burial@1'
PROBE_FIELD = 'bindingmt.burial.probe_radius'
RADII_FIELD = 'bindingmt.burial.atomic_radii'
AREA_FIELD = 'bindingmt.burial.area'
VERIFICATION_RTOL = float(32 * np.finfo(np.float64).eps)


def area_record(values):
    return length_record(
        puw.quantity(np.asarray(values, dtype=float), 'nm**2'), AREA_FIELD
    )


def area_values(record):
    quantity = QuantityRecord.from_dict(record).to_quantity(
        field=AREA_FIELD, unit='nm**2', dimensionality={'[L]': 2}, form='pint'
    )
    values = np.asarray(puw.get_value(quantity, to_unit='nm**2'), dtype=float)
    _require(np.isfinite(values).all(), 'area', 'Use finite signed areas.')
    return values


def loss_statuses(isolated, losses):
    return [
        'nonnegative'
        if loss >= 0
        else 'negative_within_roundoff'
        if -loss <= VERIFICATION_RTOL * reference
        else 'inconsistent_negative'
        for reference, loss in zip(isolated, losses)
    ]


def group_contributions(groups, losses):
    members = {}
    for i, group in enumerate(groups):
        if group is not None:
            members.setdefault(group, []).append(i)
    return [
        {
            'group_index': group,
            'atom_positions': positions,
            'loss': area_record(float(np.sum(losses[positions]))),
        }
        for group, positions in members.items()
    ]


def _same(actual, expected, field):
    _require(
        actual.shape == expected.shape
        and np.allclose(actual, expected, rtol=VERIFICATION_RTOL, atol=0),
        field,
        'Stored areas disagree with their admitted arithmetic.',
    )


def participant_order(calculation):
    """Read isolated-side order from explicit saved SASA operation axes."""
    calls = calculation.get('calls')
    _require(
        isinstance(calls, list)
        and len(calls) >= 2
        and all(isinstance(c, Mapping) for c in calls[:2]),
        'calls',
        'Preserve the isolated public SASA operation axes.',
    )
    return _names_on_axes(
        calculation.get('participants'),
        [c.get('input_atom_indices') for c in calls[:2]],
    )


def validate_calculation(value):
    _require(
        isinstance(value, Mapping)
        and set(value)
        == {
            'definition',
            'analysis_id',
            'context',
            'participants',
            'probe_radius',
            'n_sphere_points',
            'hydrogen_policy',
            'totals',
            'numerical',
            'calls',
            'producer',
            'resources',
            'attribution',
            'model_resources',
        }
        and value['definition'] == DEFINITION,
        'calculation',
        'Use the complete admitted surface calculation record.',
    )
    _require(
        isinstance(value['analysis_id'], str) and bool(value['analysis_id']),
        'analysis_id',
        'Name the composed analysis.',
    )
    probe = length_values(value['probe_radius'], PROBE_FIELD)
    _require(probe.shape == (), 'probe_radius', 'Use a scalar length.')
    n = value['n_sphere_points']
    _require(
        type(n) is int and n > 0 and value['hydrogen_policy'] == 'as_supplied',
        'calculation',
        'Preserve explicit density and supplied-H policy.',
    )
    context = value['context']
    _require(
        isinstance(context, Mapping)
        and context.get('pbc') is False
        and context.get('coordinate_policy') == 'cartesian'
        and context.get('environment') == 'selected_A_union_B'
        and isinstance(context.get('source_id'), str)
        and bool(context['source_id']),
        'context',
        'Preserve the fixed Cartesian source/environment.',
    )
    for key in ('structure_index', 'source_structure_index'):
        _require(
            type(context.get(key)) is int and context[key] >= 0,
            'context',
            'Preserve explicit structure correspondence.',
        )
    participants = value['participants']
    _require(
        isinstance(participants, Mapping) and len(participants) == 2,
        'participants',
        'Preserve two named sides.',
    )
    axes, originals, statuses, sums = [], [], {}, []
    for name in participant_order(value):
        side = participants[name]
        _require(
            isinstance(name, str)
            and bool(name)
            and isinstance(side, Mapping)
            and set(side)
            == {
                'local_atom_indices',
                'source_atom_indices',
                'group_indices',
                'radii',
                'isolated_area',
                'combined_area',
                'atomic_loss',
                'side_loss',
                'group_contributions',
                'group_coverage',
            },
            'participants',
            'Preserve aligned atoms and their surface evidence.',
        )
        local, source, groups = (
            side[k]
            for k in ('local_atom_indices', 'source_atom_indices', 'group_indices')
        )
        _require(
            isinstance(local, list)
            and local
            and all(type(i) is int and i >= 0 for i in local)
            and local == sorted(set(local))
            and isinstance(source, list)
            and len(source) == len(local)
            and all(type(i) is int and i >= 0 for i in source)
            and len(set(source)) == len(source)
            and isinstance(groups, list)
            and len(groups) == len(local)
            and all(g is None or type(g) is int and g >= 0 for g in groups),
            'participants',
            'Use unique aligned local/source/optional group axes.',
        )
        axes.append(local)
        originals.append(source)
        radius = length_values(side['radii'], RADII_FIELD)
        isolated, combined, loss = (
            area_values(side[k])
            for k in ('isolated_area', 'combined_area', 'atomic_loss')
        )
        _require(
            radius.shape
            == isolated.shape
            == combined.shape
            == loss.shape
            == (len(local),)
            and (radius > 0).all()
            and (isolated >= 0).all()
            and (combined >= 0).all(),
            'participants',
            'Use positive radii and nonnegative owner surfaces.',
        )
        _same(loss, isolated - combined, 'atomic_loss')
        total = np.asarray(float(np.sum(loss)))
        _same(area_values(side['side_loss']), total, 'side_loss')
        expected_groups = group_contributions(groups, loss)
        entries = side['group_contributions']
        _require(
            isinstance(entries, list) and len(entries) == len(expected_groups),
            'group_contributions',
            'Retain all available group contributions.',
        )
        for entry, expected in zip(entries, expected_groups):
            _require(
                isinstance(entry, Mapping)
                and set(entry) == set(expected)
                and entry['group_index'] == expected['group_index']
                and entry['atom_positions'] == expected['atom_positions'],
                'group_contributions',
                'Retain the exact atomic witnesses.',
            )
            _same(
                area_values(entry['loss']),
                area_values(expected['loss']),
                'group_contributions',
            )
        _require(
            side['group_coverage'] == ('complete' if None not in groups else 'partial'),
            'group_coverage',
            'Unknown groups are not completed zero.',
        )
        sums.append(float(total))
        statuses[name] = loss_statuses(isolated, loss)
    _require(
        not set(axes[0]) & set(axes[1]) and not set(originals[0]) & set(originals[1]),
        'participants',
        'Side populations must be disjoint.',
    )
    _require(
        isinstance(value['totals'], Mapping)
        and set(value['totals']) == {'total', 'mean_side'},
        'totals',
        'Name the sum and half-sum conventions separately.',
    )
    for key, expected in (('total', sum(sums)), ('mean_side', sum(sums) / 2)):
        _same(area_values(value['totals'][key]), np.asarray(expected), 'totals')
    usable = all('inconsistent_negative' not in s for s in statuses.values())
    _require(
        value['numerical']
        == {
            'relative_bound': VERIFICATION_RTOL,
            'absolute_bound_nm2': 0.0,
            'atomic_loss_status': statuses,
            'burial_usable': usable,
            'clamped': False,
        },
        'numerical',
        'Preserve signed losses and their separate numerical assessment.',
    )
    union = sorted(axes[0] + axes[1])
    projections = context.get('projections')
    calls = value['calls']
    _require(
        isinstance(projections, list)
        and isinstance(calls, list)
        and len(projections) == len(calls) == 3,
        'calls',
        'Preserve three independently extracted owner contexts.',
    )
    for call, projection, axis in zip(calls, projections, [*axes, union]):
        _require(
            isinstance(projection, Mapping)
            and projection.get('input_atom_indices') == axis
            and projection.get('input_structure_index') == context['structure_index']
            and projection.get('local_structure_index') == 0
            and projection.get('chemical_state_index')
            == context.get('structure_chemical_state_index')
            and projection.get('owner_comparison')
            == {'atom_type': True, 'coordinates': True}
            and projection.get('transport_verified') is True,
            'context',
            'Preserve actually checked extraction correspondence.',
        )
        _require(
            isinstance(call, Mapping)
            and call.get('operation') == 'molsysmt.physchem.get_sasa'
            and call.get('input_atom_indices') == axis
            and call.get('options')
            == {
                'element': 'atom',
                'selection': 'all',
                'structure_indices': [0],
                'engine': 'MolSysMT',
                'pbc': False,
                'use_gpu': False,
                'use_cell_list': False,
                'parallel': False,
                'num_threads': 1,
                'n_sphere_points': n,
                'probe_radius_record': value['probe_radius'],
            },
            'calls',
            'Preserve the exact public surface route/options.',
        )
    work = sum(len(a) ** 2 for a in [*axes, union]) * n
    resources = value['resources']
    _require(
        isinstance(resources, Mapping)
        and resources.get('surface_evaluations_bound') == work
        and type(resources.get('max_surface_evaluations')) is int
        and work <= resources['max_surface_evaluations']
        and resources.get('route') == 'explicit_bruteforce_cartesian_cpu_one'
        and resources.get('is_ram_reservation') is False,
        'resources',
        'Preserve the admitted work budget and route.',
    )
    for field in ('producer', 'attribution', 'model_resources'):
        _require(
            isinstance(value[field], Mapping) and bool(value[field]),
            field,
            'Preserve implementation/model provenance.',
        )
