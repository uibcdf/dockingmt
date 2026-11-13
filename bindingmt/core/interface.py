"""Immutable declared/native interface evidence and offline persistence.

Only explicit calculation entry points perform molecular work. Stored native
records retain original execution context without authenticating their producer.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from uuid import uuid4

from argdigest import arg_digest

from bindingmt._private.interface_records import _digest, _InterfaceRecordIO, _require
from bindingmt._private.serialization import json_copy
from bindingmt._private.smonitor import signal

_FORMAT = 'bindingmt.binding_interface'
_VERSION = '0.1'


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _fields(value, required, optional, field):
    _require(isinstance(value, Mapping), field, 'Supply a mapping.')
    _require(
        required <= value.keys() <= required | optional,
        field,
        f'Required fields: {sorted(required)}; optional fields: {sorted(optional)}.',
    )


def _reference(value, field):
    _require(
        isinstance(value, Mapping) and bool(value),
        field,
        'Supply a nonempty exact reference mapping; it is preserved, not resolved.',
    )


def _claim(question, participants, grouping, contexts):
    _fields(question, {'kind'}, {'description'}, 'question')
    _require(
        question['kind'] == 'association',
        'question',
        'Only the association question kind is admitted.',
    )
    if 'description' in question:
        _require(
            _text(question['description']), 'question', 'Use a nonempty description.'
        )
    _require(
        isinstance(participants, Mapping) and len(participants) >= 2,
        'participants',
        'Declare at least two named participant references.',
    )
    for name, reference in participants.items():
        _require(_text(name), 'participants', 'Use nonempty local participant names.')
        _reference(reference, 'participants')
    _require(
        isinstance(grouping, list) and len(grouping) >= 2,
        'grouping',
        'Declare at least two nonempty ordered groups.',
    )
    members = []
    for group in grouping:
        _require(
            isinstance(group, list) and bool(group),
            'grouping',
            'Each group must be a nonempty list of participant names.',
        )
        for name in group:
            _require(
                _text(name) and name in participants,
                'grouping',
                'Use known participant names.',
            )
            members.append(name)
    _require(
        len(set(members)) == len(members) and set(members) == set(participants),
        'grouping',
        'Use each declared participant exactly once.',
    )
    _require(isinstance(contexts, Mapping), 'contexts', 'Use named declared contexts.')
    for name, context in contexts.items():
        _require(_text(name), 'contexts', 'Use nonempty local context names.')
        _reference(context, 'contexts')


def _extensions(value):
    _require(isinstance(value, Mapping), 'extensions', 'Use a namespaced mapping.')
    _require(
        all(_text(key) and ('.' in key or ':' in key) for key in value),
        'extensions',
        'Namespace each opaque extension key with . or :.',
    )


def _analysis(value, version):
    required = {
        'owner',
        'reference',
        'outcome',
        'finding_refs',
        'authority',
        'original_claim',
    }
    optional = {
        'criterion',
        'coverage',
        'context_refs',
        'asset_refs',
        'historical_checks',
        'failure',
        'extensions',
        'calculation',
        'native_observation',
    }
    _fields(value, required, optional, 'analyses')
    _require(_text(value['owner']), 'analyses', 'Name the declared originating owner.')
    _reference(value['reference'], 'analyses')
    _require(
        value['authority']
        in ('caller_declared', 'bindingmt_calculated', 'molsysmt_native'),
        'analyses',
        'Use declared evidence or the admitted BindingMT native calculation profile.',
    )
    if value['authority'] == 'bindingmt_calculated':
        from bindingmt._private import interface_burial, interface_contacts

        _require(
            version in ('0.2', '0.3')
            and value['owner'] == 'bindingmt'
            and value['outcome'] == 'completed'
            and 'calculation' in value,
            'analyses',
            'A native calculation needs experimental 0.2/0.3 and its complete record.',
        )
        _require(
            'native_observation' not in value,
            'analyses',
            'Use one explicit analysis authority.',
        )
        surface = version == '0.3'
        validator = interface_burial if surface else interface_contacts
        validator.validate_calculation(value['calculation'])
        _require(
            value['reference'] == {'analysis_id': value['calculation']['analysis_id']},
            'analyses',
            'Preserve the exact composed analysis reference.',
        )
        expected = (
            [
                {
                    'analysis_id': value['calculation']['analysis_id'],
                    'result_kind': 'sasa_burial',
                }
            ]
            if surface
            else [
                {'analysis_id': value['calculation']['analysis_id'], 'contact_index': i}
                for i in range(len(value['calculation']['local_pairs']))
            ]
        )
        _require(
            value['finding_refs'] == expected,
            'analyses',
            'Retain exact contact occurrences or the completed surface-result reference.',
        )
    elif value['authority'] == 'molsysmt_native':
        from bindingmt._private.interface_ionic import (
            finding_refs,
            validate_observation,
        )

        _require(
            version in ('0.4', '0.5')
            and value['owner'] == 'molsysmt'
            and value['outcome'] == 'completed'
            and 'native_observation' in value
            and 'calculation' not in value,
            'analyses',
            'Require the complete experimental native observation profile.',
        )
        observation = value['native_observation']
        validate_observation(observation)
        _require(
            value['reference'] == {'analysis_label': observation['analysis_label']}
            and value['finding_refs'] == finding_refs(observation),
            'analyses',
            'Preserve every original analysis-qualified occurrence reference.',
        )
    else:
        _require(
            'calculation' not in value and 'native_observation' not in value,
            'analyses',
            'Declared evidence cannot impersonate native calculation.',
        )
    outcome = value['outcome']
    _require(
        outcome in ('unknown', 'completed', 'failed'),
        'analyses',
        'Use unknown, completed or failed for the original outcome.',
    )
    findings = value['finding_refs']
    if outcome == 'completed':
        _require(
            isinstance(findings, list),
            'analyses',
            'A completed analysis requires explicit finding_refs, including [].',
        )
        for reference in findings:
            _reference(reference, 'analyses')
    else:
        _require(
            findings is None,
            'analyses',
            'Unknown or failed is not a successful empty finding list.',
        )
    failure = value.get('failure')
    if outcome == 'failed':
        _require(
            isinstance(failure, Mapping) and _text(failure.get('stage')),
            'analyses',
            'A failed analysis requires its declared failure stage.',
        )
    else:
        _require(
            failure is None, 'analyses', 'Failure metadata requires failed outcome.'
        )
    original = value['original_claim']
    _fields(
        original,
        {'question', 'participants', 'grouping', 'contexts'},
        set(),
        'original_claim',
    )
    _claim(**original)
    if value['authority'] == 'bindingmt_calculated':
        calculation = value['calculation']
        expected_participants = {
            name: {
                'source_id': calculation['context']['source_id'],
                'source_atom_indices': calculation['participants'][name][
                    'source_atom_indices'
                ],
            }
            for name in validator.participant_order(calculation)
        }
        _require(
            original['participants'] == expected_participants
            and original['grouping'] == [[name] for name in expected_participants]
            and original['contexts'].get('calculation') == calculation['context'],
            'original_claim',
            'The native calculation must retain its original endpoints/context.',
        )
    if value['authority'] == 'molsysmt_native':
        context = value['native_observation']['context']
        _require(
            original['participants']
            == {
                name: {'source_id': context['source_id'], 'source_atom_indices': axis}
                for name, axis in context['participants'].items()
            }
            and original['grouping'] == context['grouping']
            and original['contexts'].get('native_interactions') == context,
            'original_claim',
            'Preserve the native scope and original molecular context.',
        )
    refs = value.get('context_refs', [])
    _require(
        isinstance(refs, list), 'analyses', 'Use a list of original context names.'
    )
    _require(
        all(_text(name) and name in original['contexts'] for name in refs),
        'analyses',
        'Reference contexts of the original claim.',
    )
    for field in ('asset_refs', 'historical_checks'):
        items = value.get(field, [])
        _require(isinstance(items, list), 'analyses', f'Use a list for {field}.')
        for item in items:
            _reference(item, 'analyses')
    if 'extensions' in value:
        _extensions(value['extensions'])


def _validate(record):
    required = {
        'format',
        'format_version',
        'experimental',
        'record_id',
        'content_sha256',
        'question',
        'participants',
        'grouping',
        'contexts',
        'claim_status',
        'analyses',
        'site_refs',
        'assurance_scope',
        'context_policy',
        'derivation',
        'extensions',
    }
    _fields(record, required, set(), 'record')
    _require(
        record['format'] == _FORMAT
        and record['format_version'] in (_VERSION, '0.2', '0.3', '0.4', '0.5')
        and record['experimental'] is True,
        'format_version',
        'Explicit experimental bindingmt.binding_interface version 0.1, 0.2, 0.3, 0.4 or 0.5 is required.',
    )
    _require(_text(record['record_id']), 'record_id', 'Use a nonempty record identity.')
    _claim(
        *(record[key] for key in ('question', 'participants', 'grouping', 'contexts'))
    )
    _require(
        record['claim_status'] in ('declared', 'inferred'),
        'claim_status',
        'Use declared or inferred; this is not evidence of binding.',
    )
    _require(
        record['assurance_scope'] == 'preserved_evidence',
        'assurance_scope',
        'Only preserved_evidence is implemented; stronger guarantees are unsupported.',
    )
    _require(
        record['context_policy'] in (None, 'require_match'),
        'context_policy',
        'Use None or require_match; preservation performs no molecular check.',
    )
    _require(isinstance(record['analyses'], Mapping), 'analyses', 'Use named analyses.')
    for name, analysis in record['analyses'].items():
        _require(_text(name), 'analyses', 'Use nonempty local analysis names.')
        _analysis(analysis, record['format_version'])
    native_count = sum(
        a['authority'] == 'bindingmt_calculated' for a in record['analyses'].values()
    )
    _require(
        native_count <= 1
        and (record['format_version'] in ('0.1', '0.4', '0.5') or native_count == 1),
        'analyses',
        'Experimental 0.2/0.3 admits exactly one corresponding native calculation.',
    )
    observations = {
        name: a['native_observation']
        for name, a in record['analyses'].items()
        if a['authority'] == 'molsysmt_native'
    }
    _require(
        not observations or record['format_version'] in ('0.4', '0.5'),
        'analyses',
        'Native observation views require experimental 0.4/0.5.',
    )
    if record['format_version'] in ('0.4', '0.5'):
        _require(
            bool(observations)
            and len(observations) == len(record['analyses'])
            and native_count == 0
            and all(
                name == view['analysis_label'] for name, view in observations.items()
            )
            and all(
                view['context'] == next(iter(observations.values()))['context']
                for view in observations.values()
            ),
            'analyses',
            'Preserve a named common-context native ionic collection.',
        )
    if record['format_version'] == '0.4':
        context = next(iter(observations.values()))['context']
        _require(
            'analysis_names' not in context,
            'format_version',
            'Explicit native analysis order requires experimental 0.5.',
        )
    if record['format_version'] == '0.5':
        from bindingmt._private.interface_ionic import validate_analysis_order

        context = next(iter(observations.values()))['context']
        validate_analysis_order(context.get('analysis_names'), observations)
    _require(
        isinstance(record['site_refs'], list),
        'site_refs',
        'Use a list of exact site references.',
    )
    for reference in record['site_refs']:
        _reference(reference, 'site_refs')
    if observations:
        from bindingmt._private.interface_ionic import (
            analysis_order,
            validate_site_reference,
        )

        order = analysis_order(record)
        for reference in record['site_refs']:
            validate_site_reference(reference, observations, order)
    _extensions(record['extensions'])
    if 'bindingmt.interface_characterizations' in record['extensions']:
        from bindingmt._private.interface_annotations import KEY, validate_annotation

        validate_annotation(record['extensions'][KEY], record)
    derivation = record['derivation']
    _fields(derivation, {'parents', 'reason'}, set(), 'derivation')
    parents = derivation['parents']
    _require(
        isinstance(parents, list) and len(parents) <= 1,
        'derivation',
        'This profile retains at most one immediate parent, without embedded history.',
    )
    if parents:
        _require(
            _text(parents[0])
            and parents[0] != record['record_id']
            and _text(derivation['reason']),
            'derivation',
            'Use a distinct parent identity and an explicit revision reason.',
        )
    else:
        _require(
            derivation['reason'] is None, 'derivation', 'A root has no revision reason.'
        )


@dataclass(frozen=True, init=False, repr=False)
class BindingInterface(_InterfaceRecordIO):
    """Immutable experimental interface evidence; accessors return detached snapshots.

    Use ``characterize_interface`` to declare, or ``from_dict/read`` with
    ``experimental=True`` to admit a saved 0.1/0.2 record explicitly. The format is
    not a stable interchange promise. No provider object is accepted by this profile.
    """

    _json: str

    @arg_digest(config='bindingmt._argdigest')
    def __init__(self, record, *, experimental=False):
        _require(
            experimental is True,
            'experimental',
            'Opt in with experimental=True to admit interface format 0.1/0.2/0.3/0.4/0.5.',
        )
        _validate(record)
        snapshot = json_copy(record, 'record')
        _require(
            snapshot['content_sha256'] == _digest(snapshot),
            'content_sha256',
            'The declared core content digest does not match; this is not authentication.',
        )
        object.__setattr__(
            self, '_json', json.dumps(snapshot, allow_nan=False, ensure_ascii=True)
        )

    @property
    def question(self):
        return self.to_dict()['question']

    @property
    def participants(self):
        return self.to_dict()['participants']

    @property
    def grouping(self):
        return self.to_dict()['grouping']

    @property
    def analyses(self):
        return self.to_dict()['analyses']

    @arg_digest(config='bindingmt._argdigest')
    def revise(self, *, question, reason):
        """Reinterpret the question; retain each analysis's original claim/context."""
        _require(_text(reason), 'reason', 'Record why the question is revised.')
        record = self.to_dict()
        record['question'] = question
        record['record_id'] = str(uuid4())
        record['derivation'] = {'parents': [self.record_id], 'reason': reason}
        record['content_sha256'] = _digest(record)
        return type(self)(record, experimental=True)

    @property
    def interaction_analyses(self):
        """Detached scoped native observation references; not a native analysis codec."""
        return {
            name: value['native_observation']
            for name, value in self.analyses.items()
            if value['authority'] == 'molsysmt_native'
        }

    @property
    def interaction_analysis_order(self):
        """Explicit saved native order, or None where an old record lacks evidence."""
        from bindingmt._private.interface_ionic import analysis_order

        return analysis_order(self.to_dict()) if self.interaction_analyses else None

    @arg_digest(config='bindingmt._argdigest')
    def with_pharmacophore(self, *, hypothesis, hypothesis_ref, participant):
        """Associate exact saved native hypothesis/site references in a new record."""
        from bindingmt.chemical_interfaces import link_pharmacophore

        return link_pharmacophore(self, hypothesis, hypothesis_ref, participant)

    @property
    def characterizations(self):
        """Detached original participant evidence; saved checks remain historical."""
        from bindingmt._private.interface_annotations import KEY

        annotation = self.to_dict()['extensions'].get(KEY)
        return {} if annotation is None else annotation['characterizations']

    @arg_digest(config='bindingmt._argdigest')
    def with_characterizations(
        self, molecular_system, *, characterizations, participant, query_ref=None
    ):
        """Associate contact/surface evidence on checked source facts; touch no query."""
        from bindingmt._private.interface_annotations import with_characterizations

        return with_characterizations(
            self, molecular_system, characterizations, participant, query_ref
        )

    @property
    def contact_calculation(self):
        """Detached typed native evidence, or None when no such analysis was supplied."""
        return next(
            (
                a['calculation']
                for a in self.analyses.values()
                if a['authority'] == 'bindingmt_calculated'
                and a['calculation']['definition']
                == 'bindingmt.cartesian_atomic_contacts@1'
            ),
            None,
        )

    @property
    def surface_calculation(self):
        """Detached original surface evidence, without reassessing any source asset."""
        return next(
            (
                a['calculation']
                for a in self.analyses.values()
                if a['authority'] == 'bindingmt_calculated'
                and a['calculation']['definition']
                == 'bindingmt.cartesian_sasa_burial@1'
            ),
            None,
        )

    @property
    def burial_areas(self):
        """Named side/sum/half-sum quantities; signed raw values are never clamped."""
        import pyunitwizard as puw

        from bindingmt._private.interface_burial import area_values, participant_order

        calculation = self.surface_calculation
        if calculation is None:
            return None
        return {
            'sides': {
                name: puw.quantity(
                    area_values(calculation['participants'][name]['side_loss']), 'nm**2'
                )
                for name in participant_order(calculation)
            },
            **{
                name: puw.quantity(area_values(value), 'nm**2')
                for name, value in calculation['totals'].items()
            },
        }

    @arg_digest(config='bindingmt._argdigest')
    def project_footprint(self, *, participant):
        """Project saved atomic witnesses; perform no molecular operation or new detection."""
        from bindingmt._private.interface_contacts import footprint_payload
        from bindingmt.core.contact_footprint import ContactFootprint

        calculation = self.contact_calculation
        _require(
            calculation is not None,
            'participant',
            'No native contact calculation is available.',
        )
        record = {
            'format': 'bindingmt.contact_footprint',
            'format_version': '0.1',
            'experimental': True,
            'record_id': str(uuid4()),
            'parent_record_id': self.record_id,
            'calculation': calculation,
            'footprint': footprint_payload(calculation, participant),
        }
        record['content_sha256'] = _digest(record)
        return ContactFootprint(record, experimental=True)

    def summary(self):
        """Inspect declared outcomes; saved checks remain history, never active checks."""
        record = self.to_dict()
        calculation = self.contact_calculation
        surface = self.surface_calculation
        observations = self.interaction_analyses
        native_context = (
            (calculation or surface)['context']
            if calculation or surface
            else next(iter(observations.values()))['context']
            if observations
            else None
        )
        criterion = None
        if calculation:
            from bindingmt._private.interface_contacts import (
                CUTOFF_FIELD,
                length_values,
                participant_order,
            )

            criterion = f'distance <= {float(length_values(calculation["cutoff"], CUTOFF_FIELD))!r} nm'
        return {
            'record_id': record['record_id'],
            'question': record['question'],
            'claim_status': record['claim_status'],
            'grouping': record['grouping'],
            'analysis_presence': 'supplied' if record['analyses'] else 'not_supplied',
            'analyses': {
                name: {
                    'owner': value['owner'],
                    'reference': value['reference'],
                    'authority': value['authority'],
                    'original_outcome': value['outcome'],
                    'finding_count': len(value['finding_refs'])
                    if value['finding_refs'] is not None
                    else None,
                    'coverage': value.get('coverage'),
                    'failure': value.get('failure'),
                    'historical_checks': value.get('historical_checks', []),
                }
                for name, value in record['analyses'].items()
            },
            'assurance_scope': 'preserved_evidence',
            'requested_context_policy': record['context_policy'],
            'context_policy_applicability': 'not_applicable',
            'molecular_correspondence': 'not_required',
            'calculation_checks': native_context['performed_checks']
            if native_context
            else [],
            'current_assessment': 'not_performed',
            'asset_access': 'not_checked',
            'available_projections': participant_order(calculation)
            if calculation
            else [],
            'native_contacts': {
                'atomic_pair_count': len(calculation['local_pairs']),
                'group_pair_count': len(calculation['group_pairs'])
                if calculation['group_coverage'] == 'complete'
                else None,
                'group_coverage': calculation['group_coverage'],
                'definition': calculation['definition'],
                'criterion': criterion,
            }
            if calculation
            else None,
            'characterizations': {
                label: {
                    'record_id': entry['record_id'],
                    'definition': entry['definition'],
                    'current_assessment': 'not_performed',
                    'scope': 'participant_evidence',
                }
                for label, entry in self.characterizations.items()
            },
            'native_analysis_order': self.interaction_analysis_order,
            'native_interactions': {
                name: {
                    'occurrence_count': len(view['observations']),
                    'original_count': view['original_count'],
                    'evaluated_structure_indices': view['evaluated_structure_indices'],
                    'definition': view['definition'],
                }
                for name, view in observations.items()
            }
            or None,
            'native_surface': {
                'definition': surface['definition'],
                'burial_usable': surface['numerical']['burial_usable'],
                'result_count': 1,
                'positive_interface_finding': 'not_assessed',
                'area_conventions': ['side_losses', 'total_sum', 'mean_side_half_sum'],
                'group_coverage': {
                    name: p['group_coverage']
                    for name, p in surface['participants'].items()
                },
            }
            if surface
            else None,
            'limitations': [
                'Native ionic evidence under caller-admitted unchanged full-source context.'
                if observations
                else 'MolSysMT geometric calculation; intended identity/state remains caller admitted.'
                if calculation or surface
                else 'Caller-declared evidence; no owner verification, molecular checking or binding inference.',
                'Saved native evidence is historical; no current molecular match or binding strength is inferred.'
                if calculation or surface or observations
                else 'Native calculation, recovery and footprint projection are not implemented by this profile.',
            ],
        }


@signal(tags=['api', 'interface', 'declaration'])
@arg_digest(config='bindingmt._argdigest')
def characterize_interface(
    *,
    question,
    participants,
    grouping,
    analyses=None,
    contexts=None,
    site_refs=None,
    claim_status='declared',
    assurance_scope='preserved_evidence',
    context_policy=None,
    extensions=None,
):
    """Compose caller-declared interface evidence without molecular or provider work.

    Participants map local labels to declared reference mappings. Grouping uses
    each label once in at least two groups. Analyses map names to declared owner,
    reference, original outcome and finding references. Completed ``[]`` differs
    from unknown/failed ``None``. Physical observable fields are not admitted yet;
    opaque namespaced extensions are preserved without interpretation.
    """
    # Grouping alone accepts tuples as a convenient public spelling.
    _require(isinstance(grouping, (list, tuple)), 'grouping', 'Use ordered groups.')
    groups = []
    for group in grouping:
        _require(isinstance(group, (list, tuple)), 'grouping', 'Use ordered groups.')
        groups.append(list(group))
    original = json_copy(
        {
            'question': question,
            'participants': participants,
            'grouping': groups,
            'contexts': {} if contexts is None else contexts,
        },
        'question',
    )
    declared = json_copy({} if analyses is None else analyses, 'analyses')
    _require(isinstance(declared, Mapping), 'analyses', 'Use named declared analyses.')
    for analysis in declared.values():
        _require(
            isinstance(analysis, Mapping), 'analyses', 'Use declared analysis mappings.'
        )
        _require(
            analysis.get('authority', 'caller_declared') == 'caller_declared'
            and 'calculation' not in analysis
            and 'native_observation' not in analysis,
            'analyses',
            'Use the explicit contact/burial entry points for new native work or read a complete saved record.',
        )
        analysis.setdefault('authority', 'caller_declared')
        analysis.setdefault('original_claim', original)
    record = json_copy(
        {
            'format': _FORMAT,
            'format_version': _VERSION,
            'experimental': True,
            'record_id': str(uuid4()),
            **original,
            'claim_status': claim_status,
            'analyses': declared,
            'site_refs': [] if site_refs is None else site_refs,
            'assurance_scope': assurance_scope,
            'context_policy': context_policy,
            'derivation': {'parents': [], 'reason': None},
            'extensions': {} if extensions is None else extensions,
        },
        'record',
    )
    record['content_sha256'] = _digest(record)
    return BindingInterface(record, experimental=True)
