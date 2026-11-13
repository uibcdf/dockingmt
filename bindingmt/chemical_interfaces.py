"""Binding-specific grouping and pharmacophore composition of native ionic evidence."""

from collections.abc import Mapping
from numbers import Integral
from uuid import uuid4

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest
from depdigest import dep_digest

from bindingmt._private.interface_context import _geometry_digest, _integer
from bindingmt._private.interface_ionic import (
    DEFINITION,
    METHOD,
    PROFILE,
    finding_refs,
    quantity_record,
    quantity_values,
)
from bindingmt._private.interface_records import _digest, _require
from bindingmt._private.serialization import json_copy
from bindingmt._private.smonitor import signal
from bindingmt.core.interface import BindingInterface, characterize_interface


def _scope(
    molecular_system,
    *,
    participants,
    grouping,
    analysis_names,
    structure_index,
    source_id,
    max_source_atoms=4096,
    max_native_occurrences=65536,
):
    import molsysmt as msm

    frame = _integer(structure_index, 'structure_index')
    _require(
        isinstance(source_id, str) and bool(source_id.strip()),
        'source_id',
        'Name the caller-admitted unchanged source.',
    )
    _require(
        msm.get_form(molecular_system) == 'molsysmt.MolSys',
        'molecular_system',
        'Supply the complete native MolSys.',
    )
    count, frames = msm.get(molecular_system, n_atoms=True, n_structures=True)
    _require(
        0 < count <= max_source_atoms
        and isinstance(frames, Integral)
        and frame < frames,
        'molecular_system',
        'Use an existing bounded native source/frame.',
    )
    axes = {
        name: list(map(int, msm.select(molecular_system, selection=selection)))
        for name, selection in participants.items()
    }
    # The existing domain core validates labels/grouping before owner interaction queries.
    declared = characterize_interface(
        question={'kind': 'association'},
        participants={
            name: {'source_id': source_id, 'source_atom_indices': axis}
            for name, axis in axes.items()
        },
        grouping=grouping,
    )
    grouping = declared.grouping
    _require(
        len(grouping) == 2,
        'grouping',
        'This profile admits two sides, including composite sides.',
    )
    flat = [a for axis in axes.values() for a in axis]
    _require(
        all(axis and len(axis) == len(set(axis)) for axis in axes.values())
        and len(flat) == len(set(flat))
        and min(flat) >= 0
        and max(flat) < count,
        'participants',
        'Use nonempty disjoint molecular participants.',
    )
    _require(
        isinstance(analysis_names, (list, tuple))
        and analysis_names
        and all(isinstance(n, str) and n.strip() for n in analysis_names)
        and len(set(analysis_names)) == len(analysis_names),
        'analysis_names',
        'Request a nonempty ordered unique list of named native analyses.',
    )
    full = molecular_system.interactions
    _require(
        all(name in full for name in analysis_names),
        'analysis_names',
        'Every requested analysis must exist; absence is not evaluated zero.',
    )
    _require(
        sum(full[name].n_interactions for name in analysis_names)
        <= max_native_occurrences,
        'max_native_occurrences',
        'The full input occurrence count exceeds the admitted profile.',
    )
    _require(
        len({full[name].source_id for name in analysis_names}) == 1,
        'analysis_names',
        'Native analyses must declare one common source identity, including an unset identity.',
    )
    states = {
        full[name].parameters.get('chemical_state_index') for name in analysis_names
    }
    _require(
        len(states) == 1
        and all(
            isinstance(s, Integral) and not isinstance(s, bool) and s >= 0
            for s in states
        ),
        'analysis_names',
        'Require one explicit common chemical state.',
    )
    state = int(next(iter(states)))
    actual = msm.get(
        molecular_system, structure_indices=[frame], structure_chemical_state_index=True
    )
    _require(
        actual is not None and list(actual) == [state],
        'molecular_system',
        'The source structure must use the observed state.',
    )
    types = list(msm.get(molecular_system, element='atom', atom_type=True))
    charges = msm.get(
        molecular_system, element='atom', chemical_state=state, formal_charge=True
    )
    _require(
        charges is not None and all(isinstance(c, Integral) for c in charges),
        'molecular_system',
        'The admitted source requires known stored formal charges.',
    )
    geometry = _geometry_digest(msm, molecular_system, list(range(count)), frame)
    context = {
        'profile': DEFINITION,
        'source_id': source_id,
        'n_atoms': int(count),
        'n_structures': int(frames),
        'structure_index': frame,
        'chemical_state_index': state,
        'coordinate_policy': 'cartesian',
        'maps': 'identity',
        'exclusive': True,
        'participants': axes,
        'grouping': grouping,
        'geometry_sha256_nm_float64': geometry,
        'atom_types': types,
        'formal_charges': quantity_record(
            puw.quantity(list(charges), 'e', form='pint'), 'source_charge'
        ),
        'caller_preconditions': [
            'same unchanged full source used by each analysis',
            'no concurrent identity/topology/chemistry/coordinate edits',
        ],
        'performed_checks': [
            'owner selections and native axis/state/coverage/profile queries',
            'public owner whole-charge-center selection checks',
            'full selected-frame coordinates/elements/formal charges',
            'owner strict between_selections; original native occurrence references',
        ],
        'limits': {
            'max_source_atoms': max_source_atoms,
            'max_native_occurrences': max_native_occurrences,
        },
    }
    # The reusable owner tool owns whole-center recognition and cut-center refusal.
    for axis in axes.values():
        msm.physchem.get_charge_centers(
            molecular_system,
            selection=axis,
            chemical_state=state,
            structure_indices=[frame],
        )
    sides = [[a for name in group for a in axes[name]] for group in grouping]
    selected, views = {}, {}
    for name in analysis_names:
        native = full[name]
        _require(
            native.method == METHOD
            and native.parameters.get('method_definition') == PROFILE
            and native.parameters.get('pbc') is False
            and np.array_equal(native.atom_source_indices, np.arange(count))
            and np.array_equal(native.structure_source_indices, np.arange(frames))
            and native.n_atoms == count
            and native.n_structures == frames
            and native.source_n_atoms == count
            and native.source_n_structures == frames
            and frame in native.evaluated_structure_indices
            and set(native.relation_types) <= {'ionic_contact'},
            'analysis_names',
            'Require the admitted full native ionic axes/profile and evaluated frame.',
        )
        view = native.between_selections(
            *sides, structure_indices=[frame], exclusive=True
        )
        data = (
            view.to_dict()
        )  # observation inspection only; native persistence stays owner-owned
        _require(
            data['image_vectors'] is None or not np.any(data['image_vectors']),
            'analysis_names',
            'This Cartesian profile admits no nonzero periodic images.',
        )
        rows = []
        for relation, occurrence, structure, evidence in zip(
            data['relation_indices'],
            data['occurrence_indices'],
            data['structure_indices'],
            data['evidence'],
        ):
            relation_data = view.relation(int(relation))
            rows.append(
                {
                    'relation_index': int(relation),
                    'occurrence_index': int(occurrence),
                    'structure_index': int(structure),
                    'evidence': str(evidence),
                    'participants': [
                        {
                            'role': p['role'],
                            'atom_indices': list(map(int, p['atom_indices'])),
                        }
                        for p in relation_data['participants']
                    ],
                }
            )
        parameters = json_copy(native.parameters, 'parameters')
        views[name] = {
            'definition': DEFINITION,
            'analysis_label': name,
            'context': context,
            'method': native.method,
            'parameters': parameters,
            'software': json_copy(native.software, 'software'),
            'source_id': native.source_id,
            'original_count': int(native.n_interactions),
            'evaluated_structure_indices': list(
                map(int, view.evaluated_structure_indices)
            ),
            'threshold': quantity_record(
                puw.quantity(**parameters['distance_threshold'], form='pint'),
                'threshold',
            ),
            'measurements': {
                key: quantity_record(
                    puw.quantity(data['measurements'][key], data['measure_units'][key]),
                    key,
                )
                for key in ('distance', 'positive_charge', 'negative_charge')
            },
            'observations': rows,
        }
        selected[name] = view
    _require(
        _geometry_digest(msm, molecular_system, list(range(count)), frame) == geometry,
        'molecular_system',
        'Source coordinates changed during the operation.',
    )
    return context, views, selected


@signal(tags=['api', 'interface', 'native-interactions'])
@arg_digest(config='bindingmt._argdigest')
def characterize_interface_interactions(
    molecular_system,
    *,
    participants,
    grouping,
    analysis_names,
    structure_index,
    source_id,
    max_source_atoms=4096,
    max_native_occurrences=65536,
):
    """Characterize a binary grouping using existing full native ionic analyses.

    Molecular selection/whole-center recognition and observation scoping are public
    MolSysMT operations. The caller admits the unchanged complete source. This
    identity-map Cartesian profile invokes no detector and infers no binding strength.
    Full observations remain in the MolSys; this record is a domain view/reference.
    """
    context, views, _ = _scope(
        molecular_system,
        participants=participants,
        grouping=grouping,
        analysis_names=analysis_names,
        structure_index=structure_index,
        source_id=source_id,
        max_source_atoms=max_source_atoms,
        max_native_occurrences=max_native_occurrences,
    )
    declared = characterize_interface(
        question={'kind': 'association'},
        participants={
            name: {'source_id': source_id, 'source_atom_indices': axis}
            for name, axis in context['participants'].items()
        },
        grouping=context['grouping'],
        contexts={'native_interactions': context},
    )
    record = declared.to_dict()
    record['format_version'] = '0.4'
    record['analyses'] = {
        name: {
            'owner': 'molsysmt',
            'reference': {'analysis_label': name},
            'authority': 'molsysmt_native',
            'outcome': 'completed',
            'finding_refs': finding_refs(view),
            'original_claim': {
                key: record[key]
                for key in ('question', 'participants', 'grouping', 'contexts')
            },
            'context_refs': ['native_interactions'],
            'native_observation': view,
        }
        for name, view in views.items()
    }
    record['content_sha256'] = _digest(record)
    return BindingInterface(record, experimental=True)


def _recheck(interface, molecular_system):
    _require(
        isinstance(interface, BindingInterface)
        and bool(interface.interaction_analyses),
        'interface',
        'Supply the admitted native ionic characterization.',
    )
    views = interface.interaction_analyses
    context = next(iter(views.values()))['context']
    _, current, selected = _scope(
        molecular_system,
        participants=context['participants'],
        grouping=context['grouping'],
        analysis_names=list(views),
        structure_index=context['structure_index'],
        source_id=context['source_id'],
        **context['limits'],
    )
    _require(
        current == views,
        'molecular_system',
        'Current scoped source/observations differ from the original characterization.',
    )
    return context, selected


def _hypothesis_digest(model):
    return _digest(
        {
            'sites': [
                {
                    'feature': site.feature_name,
                    'shape': site.shape_name,
                    'essential': bool(site.essential),
                    'weight': float(site.weight),
                    'center': quantity_record(site.center, 'center'),
                    'radius': quantity_record(site.radius, 'radius'),
                    'metadata': json_copy(site.metadata, 'hypothesis'),
                }
                for site in model.interaction_sites
            ]
        }
    )


@signal(tags=['api', 'interface', 'pharmacophore'])
@arg_digest(config='bindingmt._argdigest')
@dep_digest('pharmacophoremt')
def build_interface_pharmacophore(
    interface, molecular_system, *, participant, radius, duplicate_policy
):
    """Build an observed-participant hypothesis through PharmacophoreMT explicitly."""
    from pharmacophoremt.modeler import from_interaction_collection

    context, selected = _recheck(interface, molecular_system)
    _require(
        participant in context['participants'],
        'participant',
        'Select one characterized participant.',
    )
    _require(
        duplicate_policy in ('same_participant', 'keep'),
        'duplicate_policy',
        'Select an explicit native composition policy.',
    )
    model = from_interaction_collection(
        molecular_system,
        selected,
        context['participants'][participant],
        structure_index=context['structure_index'],
        radius=radius,
        duplicate_policy=duplicate_policy,
    )
    model.metadata['bindingmt_interface'] = {
        'record_id': interface.record_id,
        'participant': participant,
        'context_sha256': _digest(context),
        'analysis_names': list(selected),
        'radius': quantity_record(
            puw.ensure_quantity(
                radius, dimensionality={'[L]': 1}, to_unit='nm', standardized=False
            ),
            'radius',
        ),
        'duplicate_policy': duplicate_policy,
        'native_sites_sha256': _hypothesis_digest(model),
    }
    _recheck(interface, molecular_system)
    return model


@dep_digest('pharmacophoremt')
def link_pharmacophore(interface, hypothesis, hypothesis_ref, participant):
    from pharmacophoremt import Pharmacophore

    _require(
        isinstance(hypothesis, Pharmacophore),
        'hypothesis',
        'Supply the native constructed hypothesis.',
    )
    marker = hypothesis.metadata.get('bindingmt_interface', {})
    views = interface.interaction_analyses
    _require(
        bool(views), 'interface', 'Require the admitted native ionic characterization.'
    )
    context = next(iter(views.values()))['context']
    _require(
        marker.get('native_sites_sha256') == _hypothesis_digest(hypothesis)
        and marker.get('record_id') == interface.record_id
        and marker.get('participant') == participant
        and marker.get('context_sha256') == _digest(context)
        and marker.get('analysis_names') == list(views),
        'hypothesis',
        'The hypothesis must retain this exact original characterization context.',
    )
    _require(
        isinstance(hypothesis_ref, Mapping)
        and set(hypothesis_ref) == {'uri', 'sha256'}
        and isinstance(hypothesis_ref['uri'], str)
        and bool(hypothesis_ref['uri'])
        and isinstance(hypothesis_ref['sha256'], str)
        and len(hypothesis_ref['sha256']) == 64
        and all(c in '0123456789abcdef' for c in hypothesis_ref['sha256']),
        'hypothesis_ref',
        'Declare the exact saved native asset reference; no asset lookup is performed.',
    )
    sites = []
    allowed = {
        (name, row['relation_index'], row['occurrence_index'])
        for name, view in views.items()
        for row in view['observations']
        if any(
            set(p['atom_indices']) & set(context['participants'][participant])
            for p in row['participants']
        )
    }
    consumed = set()
    for index, site in enumerate(hypothesis.interaction_sites):
        refs = [
            {
                'analysis_label': row['component'],
                'relation_index': int(row['relation_index']),
                'occurrence_index': int(row['occurrence_index']),
            }
            for row in site.metadata.get('observations', [])
        ]
        keys = {
            (row['analysis_label'], row['relation_index'], row['occurrence_index'])
            for row in refs
        }
        _require(
            keys
            and keys <= allowed
            and site.shape_name == 'sphere'
            and site.feature_name in ('positive charge', 'negative charge')
            and bool(site.essential)
            and float(site.weight) == 1,
            'hypothesis',
            'Retain supported native positive-site constraints and all observation references.',
        )
        _require(
            np.array_equal(
                puw.get_value(site.radius, to_unit='nm'),
                quantity_values(marker['radius'], 'radius'),
            ),
            'hypothesis',
            'The matching radius differs from its recorded construction policy.',
        )
        consumed.update(keys)
        sites.append(
            {
                'site_index': index,
                'feature_name': site.feature_name,
                'essential': bool(site.essential),
                'weight': float(site.weight),
                'center': quantity_record(site.center, 'center'),
                'radius': quantity_record(site.radius, 'radius'),
                'contributors': refs,
            }
        )
    _require(
        consumed == allowed,
        'hypothesis',
        'Every selected target observation needs its original output-site link.',
    )
    record = interface.to_dict()
    record['record_id'] = str(uuid4())
    record['derivation'] = {
        'parents': [interface.record_id],
        'reason': 'associate exact native observed-participant hypothesis',
    }
    record['site_refs'].append(
        {
            'owner': 'pharmacophoremt',
            'definition': 'bindingmt.observed_ionic_hypothesis@1',
            'reference': json_copy(hypothesis_ref, 'hypothesis_ref'),
            'source_record_id': interface.record_id,
            'participant': participant,
            'construction': json_copy(marker, 'hypothesis'),
            'sites': sites,
        }
    )
    record['content_sha256'] = _digest(record)
    return BindingInterface(record, experimental=True)
