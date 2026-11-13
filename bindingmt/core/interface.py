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
    }
    _fields(value, required, optional, 'analyses')
    _require(_text(value['owner']), 'analyses', 'Name the declared originating owner.')
    _reference(value['reference'], 'analyses')
    _require(
        value['authority'] in ('caller_declared', 'bindingmt_calculated'),
        'analyses',
        'Use declared evidence or the admitted BindingMT native calculation profile.',
    )
    if value['authority'] == 'bindingmt_calculated':
        from bindingmt._private.interface_contacts import validate_calculation

        _require(
            version == '0.2'
            and value['owner'] == 'bindingmt'
            and value['outcome'] == 'completed'
            and 'calculation' in value,
            'analyses',
            'A native calculation needs experimental 0.2 and its complete record.',
        )
        validate_calculation(value['calculation'])
        _require(
            value['reference'] == {'analysis_id': value['calculation']['analysis_id']},
            'analyses',
            'Preserve the exact composed analysis reference.',
        )
        expected = [
            {'analysis_id': value['calculation']['analysis_id'], 'contact_index': i}
            for i in range(len(value['calculation']['local_pairs']))
        ]
        _require(
            value['finding_refs'] == expected,
            'analyses',
            'Findings must retain every calculated contact occurrence.',
        )
    else:
        _require(
            'calculation' not in value,
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
                'source_atom_indices': member['source_atom_indices'],
            }
            for name, member in calculation['participants'].items()
        }
        _require(
            original['participants'] == expected_participants
            and original['grouping'] == [[name] for name in expected_participants]
            and original['contexts'].get('calculation') == calculation['context'],
            'original_claim',
            'The native calculation must retain its original endpoints/context.',
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
        and record['format_version'] in (_VERSION, '0.2')
        and record['experimental'] is True,
        'format_version',
        'Explicit experimental bindingmt.binding_interface version 0.1 or 0.2 is required.',
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
        native_count <= 1 and (record['format_version'] != '0.2' or native_count == 1),
        'analyses',
        'Experimental 0.2 admits exactly one native contact calculation.',
    )
    _require(
        isinstance(record['site_refs'], list),
        'site_refs',
        'Use a list of exact site references.',
    )
    for reference in record['site_refs']:
        _reference(reference, 'site_refs')
    _extensions(record['extensions'])
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
            'Opt in with experimental=True to admit interface format 0.1/0.2.',
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
    def contact_calculation(self):
        """Detached typed native evidence, or None when no such analysis was supplied."""
        return next(
            (
                a['calculation']
                for a in self.analyses.values()
                if a['authority'] == 'bindingmt_calculated'
            ),
            None,
        )

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
        criterion = None
        if calculation:
            from bindingmt._private.interface_contacts import (
                CUTOFF_FIELD,
                length_values,
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
            'calculation_checks': calculation['context']['performed_checks']
            if calculation
            else [],
            'current_assessment': 'not_performed',
            'asset_access': 'not_checked',
            'available_projections': list(calculation['participants'])
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
            'limitations': [
                'MolSysMT geometric calculation; intended identity/state remains caller admitted.'
                if calculation
                else 'Caller-declared evidence; no owner verification, molecular checking or binding inference.',
                'Saved native evidence is historical; no current molecular match or binding strength is inferred.'
                if calculation
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
            and 'calculation' not in analysis,
            'analyses',
            'Use calculate_interface_contacts for new native work or read a complete saved record.',
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
