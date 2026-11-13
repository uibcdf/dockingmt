"""Immutable, coordinate-free binding-site hypotheses and source annotations."""

import json
from dataclasses import dataclass
from uuid import uuid4

from argdigest import arg_digest

from bindingmt._private.interface_records import _digest, _InterfaceRecordIO, _require
from bindingmt._private.serialization import json_copy
from bindingmt._private.site_records import (
    capability,
    membership_payload,
    residue_records,
    scope_record,
    sequence,
    source_record,
    text,
    validate,
)
from bindingmt._private.smonitor import signal


def _producer(operation):
    from bindingmt import __version__

    return {
        'library': 'bindingmt',
        'bindingmt_version': __version__,
        'operation': operation,
    }


def _record(source, claim, criterion, name, structures, states, extensions, views):
    return {
        'format': 'bindingmt.binding_site',
        'format_version': '0.1',
        'experimental': True,
        'record_id': str(uuid4()),
        'name': name,
        'context': {'source': source},
        'views': views,
        'definition': {
            'key': 'definition',
            'claim': claim,
            'criterion': criterion,
            'participants': [source['id']],
            'views': [v['key'] for v in views],
            'scope': scope_record(source['id'], structures, states),
            'evidence_refs': [],
            'binding_support': 'unknown',
        },
        'evidence': [],
        'realization_coverage': {'state': 'not_requested'},
        'derivation': {'parents': [], 'kind': None, 'reason': None},
        'extensions': {} if extensions is None else extensions,
        'producer': _producer('declaration'),
    }


@dataclass(frozen=True, init=False, repr=False)
class BindingSite(_InterfaceRecordIO):
    """A declared hypothesis; source addresses are unresolved molecular membership."""

    _json: str

    @arg_digest(config='bindingmt._argdigest')
    def __init__(self, record, *, experimental=False):
        _require(
            experimental is True, 'experimental', 'Opt in to experimental site 0.1/0.2.'
        )
        snapshot = json_copy(record, 'record')
        validate(snapshot)
        object.__setattr__(self, '_json', json.dumps(snapshot, allow_nan=False))

    @classmethod
    @signal(tags=['api', 'site', 'declaration'])
    @arg_digest(config='bindingmt._argdigest')
    def from_residues(
        cls,
        *,
        source,
        address_space,
        residues,
        name=None,
        role='annotated_members',
        structure_indices=None,
        chemical_state_indices=None,
        extensions=None,
    ):
        """Declare ordered source addresses without coordinates, mapping or evidence."""
        source = source_record(source)
        _require(
            text(address_space) and text(role),
            'address_space',
            'Declare address space and role strings.',
        )
        capability(address_space == 'author_residue', 'site residue address space')
        capability(role == 'annotated_members', 'site annotation role')
        views = [
            {
                'key': 'membership',
                'kind': 'residue_annotation',
                'role': role,
                'scope': scope_record(
                    source['id'], structure_indices, chemical_state_indices
                ),
                'payload': {
                    'address_space': address_space,
                    'entries': residue_records(residues),
                    'resolution': {
                        'state': 'unresolved',
                        'cause': 'no_correspondence_supplied',
                    },
                },
            }
        ]
        record = _record(
            source,
            'Candidate association region; binding support unknown',
            {'kind': 'annotation_membership', 'rule': 'exact_listed_entries'},
            name,
            structure_indices,
            chemical_state_indices,
            extensions,
            views,
        )
        record = json_copy(record, 'record')
        record['content_sha256'] = _digest(record)
        return cls(record, experimental=True)

    @classmethod
    @signal(tags=['api', 'site', 'declaration'])
    @arg_digest(config='bindingmt._argdigest')
    def from_definition(
        cls,
        *,
        source,
        claim,
        criterion,
        name=None,
        structure_indices=None,
        chemical_state_indices=None,
        extensions=None,
    ):
        """Declare an unevaluated criterion, without an invented empty membership."""
        record = _record(
            source_record(source),
            claim,
            criterion,
            name,
            structure_indices,
            chemical_state_indices,
            extensions,
            [],
        )
        record = json_copy(record, 'definition')
        record['content_sha256'] = _digest(record)
        return cls(record, experimental=True)

    @classmethod
    def _from_members(
        cls, source, indices, element, name, role, structures, states, extensions
    ):
        source = source_record(source)
        _require(text(role), 'role', 'Declare a membership role string.')
        capability(role == 'declared_members', 'site membership role')
        views = [
            {
                'key': 'membership',
                'kind': 'molecular_membership',
                'role': role,
                'scope': scope_record(source['id'], structures, states),
                'payload': membership_payload(indices, element),
            }
        ]
        record = _record(
            source,
            'Candidate association region; binding support unknown',
            {
                'kind': 'explicit_source_membership',
                'rule': 'exact_listed_indices',
                'element': element,
            },
            name,
            structures,
            states,
            extensions,
            views,
        )
        record['format_version'] = '0.2'
        record = json_copy(record, 'record')
        record['content_sha256'] = _digest(record)
        return cls(record, experimental=True)

    @classmethod
    @signal(tags=['api', 'site', 'declaration'])
    @arg_digest(config='bindingmt._argdigest')
    def from_atoms(
        cls,
        *,
        source,
        atom_indices,
        name=None,
        role='declared_members',
        structure_indices=None,
        chemical_state_indices=None,
        extensions=None,
    ):
        """Declare source atom indices; no source bound or geometry is checked."""
        return cls._from_members(
            source,
            atom_indices,
            'atom',
            name,
            role,
            structure_indices,
            chemical_state_indices,
            extensions,
        )

    @classmethod
    @signal(tags=['api', 'site', 'declaration'])
    @arg_digest(config='bindingmt._argdigest')
    def from_groups(
        cls,
        *,
        source,
        group_indices,
        name=None,
        role='declared_members',
        structure_indices=None,
        chemical_state_indices=None,
        extensions=None,
    ):
        """Declare source group indices; no residue-ID parsing or atom expansion."""
        return cls._from_members(
            source,
            group_indices,
            'group',
            name,
            role,
            structure_indices,
            chemical_state_indices,
            extensions,
        )

    @property
    def site_id(self):
        return self.record_id

    @property
    def context(self):
        return self.to_dict()['context']

    @property
    def views(self):
        return self.to_dict()['views']

    @property
    def definition(self):
        return self.to_dict()['definition']

    @property
    def evidence(self):
        return self.to_dict()['evidence']

    @property
    def definition_ref(self):
        record = self.to_dict()
        return {
            'record_id': record['record_id'],
            'content_sha256': record['content_sha256'],
            'definition_key': 'definition',
        }

    def _derive(self, record, kind, reason):
        _require(text(reason), 'reason', 'Record why this declaration is derived.')
        record['record_id'] = str(uuid4())
        record['derivation'] = {
            'parents': [
                {k: v for k, v in self.definition_ref.items() if k != 'definition_key'}
            ],
            'kind': kind,
            'reason': reason,
        }
        record['producer'] = _producer(kind)
        record = json_copy(record, 'record')
        record['content_sha256'] = _digest(record)
        return type(self)(record, experimental=True)

    @signal(tags=['api', 'site', 'interpretation'])
    @arg_digest(config='bindingmt._argdigest')
    def with_definition(self, *, claim, criterion, reason, evidence_refs=()):
        """Revise interpretation; preserve observations and their original claim refs."""
        record = self.to_dict()
        record['definition'].update(
            claim=claim,
            criterion=criterion,
            evidence_refs=sequence(evidence_refs, 'evidence_refs'),
        )
        return self._derive(record, 'definition_revision', reason)

    @signal(tags=['api', 'site', 'annotation'])
    @arg_digest(config='bindingmt._argdigest')
    def with_evidence(
        self,
        *,
        key,
        source,
        observation,
        attribution,
        structure_indices=None,
        chemical_state_indices=None,
    ):
        """Add an attributed annotation and explicitly cite it, without new measurement."""
        record = self.to_dict()
        record['evidence'].append(
            {
                'key': key,
                'kind': 'source_annotation',
                'source': source_record(source),
                'observation': observation,
                'attribution': attribution,
                'participants': record['definition']['participants'],
                'views': record['definition']['views'],
                'scope': scope_record(
                    record['context']['source']['id'],
                    structure_indices,
                    chemical_state_indices,
                ),
                'original_claim_ref': self.definition_ref,
            }
        )
        record['definition']['evidence_refs'].append(key)
        return self._derive(
            record,
            'evidence_addition',
            'Explicitly cite an attributed source annotation',
        )

    def inspect(self):
        """Report declared meaning and missing prerequisites without resolving sources."""
        record = self.to_dict()
        payload = record['views'][0]['payload'] if record['views'] else None
        molecular = (
            payload is not None and record['views'][0]['kind'] == 'molecular_membership'
        )
        entries = (
            None
            if payload is None
            else payload['source_indices']
            if molecular
            else payload['entries']
        )
        membership = {
            'state': 'not_supplied'
            if entries is None
            else 'declared_empty'
            if not entries
            else 'declared'
            if molecular
            else 'unresolved',
            'entry_count': None if entries is None else len(entries),
        }
        if molecular:
            membership.update(
                element=payload['element'], index_space=payload['index_space']
            )
        return {
            'record_id': self.record_id,
            'name': record['name'],
            'definition_ref': self.definition_ref,
            'source': record['context']['source'],
            'definition_scope': record['definition']['scope'],
            'membership': membership,
            'binding_support': 'unknown',
            'evidence_count': len(record['evidence']),
            'current_evidence_refs': record['definition']['evidence_refs'],
            'evidence_scopes': {e['key']: e['scope'] for e in record['evidence']},
            'realization_coverage': record['realization_coverage'],
            'molecular_resolution': 'not_performed',
            'asset_access': 'not_checked',
            'capabilities': {
                'declaration': True,
                'persistence': True,
                'molecular_projection': False,
                'domain_placement': False,
            },
        }

    def describe(self):
        report = self.inspect()
        return (
            f'BindingSite {report["name"] or report["record_id"]}: {report["membership"]["state"]} '
            f'membership; {report["evidence_count"]} attributed observations. '
            'Binding support is unknown; molecular resolution is not performed.'
        )
