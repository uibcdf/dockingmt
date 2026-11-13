"""Binding-owned portable ionic observation views; no native interaction codec."""

from collections.abc import Mapping

import numpy as np
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

from bindingmt._private.interface_records import _digest, _require
from bindingmt._private.serialization import json_copy

DEFINITION = 'bindingmt.native_ionic_scope@1'
METHOD = 'molsysmt.interactions.ionic.get_ionic_interactions'
PROFILE = 'molsysmt.ionic.minimum_distance.native@1'
FIELDS = {
    'distance': 'nm',
    'positive_charge': 'e',
    'negative_charge': 'e',
    'threshold': 'nm',
    'source_charge': 'e',
    'radius': 'nm',
    'center': 'nm',
}


def quantity_record(quantity, field):
    canonical = puw.convert(quantity, to_unit=FIELDS[field], to_form='pint')
    return QuantityRecord.from_quantity(
        canonical, field='bindingmt.ionic.' + field
    ).to_dict()


def quantity_values(record, field):
    unit = FIELDS[field]
    quantity = QuantityRecord.from_dict(record).to_quantity(
        field='bindingmt.ionic.' + field,
        unit=unit,
        dimensionality=puw.get_dimensionality(puw.unit(unit, form='pint')),
        form='pint',
    )
    values = np.asarray(puw.get_value(quantity, to_unit=unit), dtype=float)
    _require(np.isfinite(values).all(), field, 'Use finite physical values.')
    return values


def finding_refs(observation):
    return [
        {
            'analysis_label': observation['analysis_label'],
            'relation_index': row['relation_index'],
            'occurrence_index': row['occurrence_index'],
        }
        for row in observation['observations']
    ]


def validate_observation(value):
    _require(
        isinstance(value, Mapping)
        and set(value)
        == {
            'definition',
            'analysis_label',
            'context',
            'method',
            'parameters',
            'software',
            'threshold',
            'measurements',
            'observations',
            'evaluated_structure_indices',
            'source_id',
            'original_count',
        },
        'native_observation',
        'Use the complete admitted ionic observation view.',
    )
    _require(
        value['definition'] == DEFINITION
        and value['method'] == METHOD
        and isinstance(value['analysis_label'], str)
        and bool(value['analysis_label']),
        'native_observation',
        'Preserve the supported owner and named native analysis.',
    )
    context = value['context']
    _require(
        isinstance(context, Mapping)
        and context.get('profile') == DEFINITION
        and context.get('coordinate_policy') == 'cartesian'
        and context.get('maps') == 'identity'
        and context.get('exclusive') is True,
        'context',
        'Preserve the admitted Cartesian identity-axis scope.',
    )
    for key in ('n_atoms', 'n_structures', 'structure_index', 'chemical_state_index'):
        _require(
            type(context.get(key)) is int
            and context[key] >= (1 if key in ('n_atoms', 'n_structures') else 0),
            'context',
            'Preserve explicit source axes/frame/state.',
        )
    _require(
        context['structure_index'] < context['n_structures']
        and isinstance(context.get('source_id'), str)
        and bool(context['source_id'])
        and isinstance(context.get('geometry_sha256_nm_float64'), str)
        and len(context['geometry_sha256_nm_float64']) == 64,
        'context',
        'Preserve the original source/frame and geometry fingerprint.',
    )
    members = context.get('participants')
    groups = context.get('grouping')
    _require(
        isinstance(members, Mapping)
        and len(members) >= 2
        and isinstance(groups, list)
        and len(groups) == 2
        and all(isinstance(g, list) and g for g in groups),
        'context',
        'Declare binary grouping of named molecular participants.',
    )
    flattened = [name for group in groups for name in group]
    _require(
        len(flattened) == len(set(flattened)) and set(flattened) == set(members),
        'context',
        'Each participant belongs to one side.',
    )
    all_atoms = []
    for name, atoms in members.items():
        _require(
            isinstance(name, str)
            and bool(name)
            and isinstance(atoms, list)
            and atoms
            and all(type(a) is int and 0 <= a < context['n_atoms'] for a in atoms)
            and len(set(atoms)) == len(atoms),
            'context',
            'Use resolved nonempty unique participant axes.',
        )
        all_atoms.extend(atoms)
    _require(
        len(set(all_atoms)) == len(all_atoms),
        'context',
        'Participant axes must be disjoint.',
    )
    _require(
        isinstance(context.get('atom_types'), list)
        and len(context['atom_types']) == context['n_atoms']
        and quantity_values(context['formal_charges'], 'source_charge').shape
        == (context['n_atoms'],),
        'context',
        'Preserve inspected full-source element/charge context.',
    )
    parameters = value['parameters']
    _require(
        isinstance(parameters, Mapping)
        and parameters.get('method_definition') == PROFILE
        and parameters.get('recognition_rule_version') == 'formal_charge_centers@1'
        and parameters.get('chemical_state_index') == context['chemical_state_index']
        and parameters.get('pbc') is False
        and parameters.get('recognition_scope') == 'full_source_chemical_state',
        'parameters',
        'Preserve the actual formal-charge ionic profile/state.',
    )
    threshold = quantity_values(value['threshold'], 'threshold')
    original = puw.quantity(**parameters['distance_threshold'], form='pint')
    _require(
        threshold.shape == ()
        and threshold > 0
        and np.isclose(
            threshold,
            puw.get_value(original, to_unit='nm'),
            rtol=8 * np.finfo(float).eps,
            atol=0,
        ),
        'threshold',
        'Preserve the original owner criterion and units.',
    )
    frame = context['structure_index']
    _require(
        value['evaluated_structure_indices'] == [frame],
        'coverage',
        'The selected frame must have evaluated coverage, including zero.',
    )
    rows = value['observations']
    _require(
        isinstance(rows, list)
        and type(value['original_count']) is int
        and value['original_count'] >= len(rows),
        'observations',
        'Preserve original/scoped counts.',
    )
    sides = [set(a for name in g for a in members[name]) for g in groups]
    occurrences = set()
    for row in rows:
        _require(
            isinstance(row, Mapping)
            and set(row)
            == {
                'relation_index',
                'occurrence_index',
                'structure_index',
                'evidence',
                'participants',
            }
            and all(
                type(row[k]) is int and row[k] >= 0
                for k in ('relation_index', 'occurrence_index')
            )
            and row['structure_index'] == frame
            and isinstance(row['evidence'], str),
            'observations',
            'Preserve exact original occurrence/relation/frame evidence.',
        )
        _require(
            row['occurrence_index'] not in occurrences,
            'observations',
            'Occurrences must be unique within each analysis.',
        )
        occurrences.add(row['occurrence_index'])
        parts = row['participants']
        _require(
            isinstance(parts, list)
            and len(parts) == 2
            and all(
                isinstance(p, Mapping) and set(p) == {'role', 'atom_indices'}
                for p in parts
            )
            and {p['role'] for p in parts} == {'positive', 'negative'},
            'observations',
            'Preserve both owner-defined whole charge participants.',
        )
        atoms = []
        for part in parts:
            axis = part['atom_indices']
            _require(
                isinstance(axis, list)
                and axis
                and all(type(a) is int and a >= 0 for a in axis)
                and len(set(axis)) == len(axis),
                'observations',
                'Use exact whole participant atoms.',
            )
            atoms.extend(axis)
        _require(
            len(atoms) == len(set(atoms))
            and set(atoms) <= set(all_atoms)
            and all(set(atoms) & side for side in sides),
            'observations',
            'Retain only the owner-qualified cross-side scope.',
        )
    _require(
        isinstance(value['measurements'], Mapping)
        and set(value['measurements'])
        == {'distance', 'positive_charge', 'negative_charge'},
        'measurements',
        'Retain the three interpreted native measurements.',
    )
    arrays = {
        key: quantity_values(record, key)
        for key, record in value['measurements'].items()
    }
    _require(
        all(v.shape == (len(rows),) for v in arrays.values())
        and (arrays['distance'] >= 0).all()
        and (arrays['positive_charge'] > 0).all()
        and (arrays['negative_charge'] < 0).all(),
        'measurements',
        'Align physical measurements to original occurrences.',
    )
    _require(
        isinstance(value['software'], Mapping) and bool(value['software']),
        'software',
        'Preserve original producer declarations.',
    )
    json_copy(value, 'native_observation')


def validate_site_reference(reference, observations):
    _require(
        isinstance(reference, Mapping)
        and set(reference)
        == {
            'owner',
            'definition',
            'reference',
            'source_record_id',
            'participant',
            'construction',
            'sites',
        }
        and reference['owner'] == 'pharmacophoremt'
        and reference['definition'] == 'bindingmt.observed_ionic_hypothesis@1',
        'site_refs',
        'Use the exact native observed-hypothesis association.',
    )
    context = next(iter(observations.values()))['context']
    marker = reference['construction']
    _require(
        isinstance(marker, Mapping)
        and marker.get('record_id') == reference['source_record_id']
        and marker.get('participant') == reference['participant']
        and reference['participant'] in context['participants']
        and marker.get('context_sha256') == _digest(context)
        and marker.get('analysis_names') == list(observations)
        and marker.get('duplicate_policy') in ('same_participant', 'keep'),
        'site_refs',
        'Preserve the exact original construction context.',
    )
    asset = reference['reference']
    _require(
        isinstance(asset, Mapping)
        and set(asset) == {'uri', 'sha256'}
        and isinstance(asset['uri'], str)
        and bool(asset['uri'])
        and isinstance(asset['sha256'], str)
        and len(asset['sha256']) == 64
        and all(c in '0123456789abcdef' for c in asset['sha256']),
        'site_refs',
        'Retain the caller-owned native saved-asset reference.',
    )
    radius = quantity_values(marker['radius'], 'radius')
    _require(
        radius.shape == () and radius > 0,
        'site_refs',
        'Retain the positive matching radius.',
    )
    allowed = {
        (name, row['relation_index'], row['occurrence_index'])
        for name, view in observations.items()
        for row in view['observations']
        if any(
            set(p['atom_indices'])
            & set(context['participants'][reference['participant']])
            for p in row['participants']
        )
    }
    consumed = set()
    sites = reference['sites']
    _require(
        isinstance(sites, list), 'site_refs', 'Retain exact output-site references.'
    )
    for index, site in enumerate(sites):
        _require(
            isinstance(site, Mapping)
            and set(site)
            == {
                'site_index',
                'feature_name',
                'essential',
                'weight',
                'center',
                'radius',
                'contributors',
            }
            and site['site_index'] == index
            and site['essential'] is True
            and site['weight'] == 1
            and site['feature_name'] in ('positive charge', 'negative charge')
            and quantity_values(site['center'], 'center').shape == (3,)
            and np.array_equal(quantity_values(site['radius'], 'radius'), radius),
            'site_refs',
            'Preserve original native site constraints and physical geometry.',
        )
        refs = site['contributors']
        _require(
            isinstance(refs, list) and bool(refs),
            'site_refs',
            'Each site requires its contributing observations.',
        )
        for row in refs:
            _require(
                isinstance(row, Mapping)
                and set(row) == {'analysis_label', 'relation_index', 'occurrence_index'}
                and (
                    row['analysis_label'],
                    row['relation_index'],
                    row['occurrence_index'],
                )
                in allowed,
                'site_refs',
                'Contributors must name exact scoped native observations.',
            )
            consumed.add(
                (row['analysis_label'], row['relation_index'], row['occurrence_index'])
            )
    _require(
        consumed == allowed,
        'site_refs',
        'Every selected observation retains its output-site link.',
    )
