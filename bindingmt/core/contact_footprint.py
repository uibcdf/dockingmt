"""Independent, immutable footprint of a completed native contact calculation."""

import json
from dataclasses import dataclass

from argdigest import arg_digest

from bindingmt._private.interface_contacts import (
    footprint_payload,
    validate_calculation,
)
from bindingmt._private.interface_records import _digest, _InterfaceRecordIO, _require
from bindingmt._private.serialization import json_copy


@dataclass(frozen=True, init=False, repr=False)
class ContactFootprint(_InterfaceRecordIO):
    """Detached source-ordered members and all atomic witnesses, not a binding site."""

    _json: str

    @arg_digest(config='bindingmt._argdigest')
    def __init__(self, record, *, experimental=False):
        _require(
            experimental is True,
            'experimental',
            'Opt in to experimental footprint 0.1.',
        )
        required = {
            'format',
            'format_version',
            'experimental',
            'record_id',
            'content_sha256',
            'parent_record_id',
            'calculation',
            'footprint',
        }
        _require(
            set(record) == required
            and record['format'] == 'bindingmt.contact_footprint'
            and record['format_version'] == '0.1'
            and record['experimental'] is True,
            'record',
            'Use a complete experimental contact footprint 0.1 record.',
        )
        _require(
            all(
                isinstance(record[k], str) and record[k]
                for k in ('record_id', 'parent_record_id')
            ),
            'record_id',
            'Preserve footprint and parent identities.',
        )
        _require(
            record['record_id'] != record['parent_record_id'],
            'parent_record_id',
            'A footprint cannot name itself as its parent.',
        )
        snapshot = json_copy(record, 'record')
        validate_calculation(snapshot['calculation'])
        payload = snapshot['footprint']
        _require(
            isinstance(payload, dict)
            and payload
            == footprint_payload(snapshot['calculation'], payload.get('participant')),
            'footprint',
            'Footprint members, order/maps and contributors disagree with the calculation.',
        )
        _require(
            snapshot['content_sha256'] == _digest(snapshot),
            'content_sha256',
            'Footprint content digest mismatch.',
        )
        object.__setattr__(self, '_json', json.dumps(snapshot, allow_nan=False))

    @property
    def source_atom_indices(self):
        return self.to_dict()['footprint']['source_atom_indices']

    @property
    def local_atom_indices(self):
        return self.to_dict()['footprint']['local_atom_indices']

    def summary(self):
        record = self.to_dict()
        return {
            **record['footprint'],
            'record_id': record['record_id'],
            'parent_record_id': record['parent_record_id'],
            'analysis_id': record['calculation']['analysis_id'],
            'context': record['calculation']['context'],
            'current_assessment': 'not_performed',
        }
