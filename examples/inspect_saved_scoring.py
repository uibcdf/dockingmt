"""Inspect a saved scoring pose or result with an ordinary-installed reader.

Copy this example and the input file anywhere. It reads existing evidence;
it does not prepare, score, rank, reconstruct or visualize molecular systems.
"""

import argparse
import hashlib
import importlib.metadata as metadata
import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path


def _captured_summary(artifacts, dmt):
    available = all(
        'content_base64' in artifacts.get(role, {}) for role in ('receptor', 'partner')
    )
    return {
        'captured_inputs': 'verified' if available else 'unavailable',
        'captured_bytes': dmt.verify_captured_inputs(artifacts) if available else None,
    }


def _pose_summary(pose, dmt):
    canonical = pose.to_dict()
    evaluations = []
    for entry in canonical['metadata'].get('scoring_history', []):
        preparation = entry.get('preparation', {})
        evaluations.append(
            {
                'score_name': entry.get('score_name'),
                'backend': entry.get('backend'),
                'backend_version': entry.get('backend_version'),
                'producer_bindingmt_version': entry.get('bindingmt_version'),
                'producer_molsysmt_version': entry.get('molsysmt_version'),
                **_captured_summary(entry.get('backend_artifacts', {}), dmt),
                'recorded_preparation_assessment': {
                    role: preparation.get(role, {})
                    .get('assessment_report', {})
                    .get('assessment')
                    for role in ('receptor', 'partner')
                },
            }
        )
    definitions = pose.score_definitions
    rows = []
    for name, value in pose.scores.items():
        definition = definitions.get(name, {})
        rows.append(
            {
                'name': name,
                'value': value,
                'unit': definition.get('unit'),
                'method': definition.get('method'),
                'method_version': definition.get('method_version'),
                'component': definition.get('component'),
                'kind': definition.get('kind'),
                'preferred_direction': definition.get('preferred_direction'),
            }
        )
    return {
        'pose': {
            key: canonical.get(key)
            for key in ('pose_id', 'partner_state_id', 'receptor_state_id', 'rank')
        },
        'scores': rows,
        'evaluations': evaluations,
    }


def _result_summary(result, dmt):
    provenance = result.provenance
    return {
        'collection': {
            'pose_count': len(result.poses),
            'ranking_policy': deepcopy(provenance.get('ranking_policy')),
            'stored_pose_order': [pose.pose_id for pose in result.poses],
            'ranking_history': [
                {
                    key: entry.get(key)
                    for key in (
                        'evidence',
                        'origin',
                        'score_name',
                        'ascending',
                        'output_order',
                    )
                }
                for entry in result.ranking_history
            ],
            'original_docking_producer': {
                'backend': provenance.get('backend'),
                'backend_version': provenance.get('backend_version'),
                'producer_bindingmt_version': provenance.get('bindingmt_version'),
                'producer_molsysmt_version': provenance.get('molsysmt_version'),
                **_captured_summary(provenance.get('backend_artifacts', {}), dmt),
            },
        },
        'poses': [
            {'index': index, **_pose_summary(pose, dmt)}
            for index, pose in enumerate(result.poses)
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path, help='Caller-owned saved JSON file')
    parser.add_argument(
        '--record-kind',
        choices=('pose', 'result'),
        default='pose',
        help='Explicit record type; default: pose',
    )
    parser.add_argument(
        '--sha256', required=True, help='Independently expected file digest'
    )
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9a-fA-F]{64}', args.sha256):
        parser.error(
            'Provide the independently expected SHA-256 as 64 hexadecimal digits.'
        )
    payload = args.record.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != args.sha256.lower():
        parser.exit(
            1, 'Input digest differs from the independently expected SHA-256.\n'
        )
    record = json.loads(payload)
    required_key = 'coordinates' if args.record_kind == 'pose' else 'poses'
    if not isinstance(record, dict) or required_key not in record:
        parser.exit(1, f'Supply a saved {args.record_kind} record for --record-kind.\n')
    original = deepcopy(record)

    from smonitor.integrations import CatalogException

    import bindingmt as dmt

    distribution = metadata.distribution('bindingmt')
    installation = json.loads(distribution.read_text('direct_url.json') or '{}')
    if (
        installation.get('dir_info', {}).get('editable', False)
        or Path(dmt.__file__).resolve()
        != Path(distribution.locate_file('bindingmt/__init__.py')).resolve()
        or distribution.version != dmt.__version__
    ):
        parser.exit(1, 'Use an ordinary-installed reader without a source overlay.\n')

    audit_name = 'audit_pose' if args.record_kind == 'pose' else 'audit_result'
    model = dmt.DockingPose if args.record_kind == 'pose' else dmt.DockingResult
    try:
        audit = getattr(dmt, audit_name)(record)
        if audit['status'] == 'inconsistent':
            for check in audit['checks']:
                if check['status'] == 'inconsistent':
                    print(f'{check["path"]}: {check["reason"]}', file=sys.stderr)
            parser.exit(
                1,
                f'Saved scoring evidence is inconsistent; inspect {audit_name} checks.\n',
            )
        admitted = model.from_dict(record)
        canonical = admitted.to_dict()
        if model.from_dict(canonical).to_dict() != canonical:
            parser.exit(1, 'The admitted record did not roundtrip independently.\n')
        details = (
            _pose_summary(admitted, dmt)
            if args.record_kind == 'pose'
            else _result_summary(admitted, dmt)
        )
    except CatalogException as error:
        parser.exit(
            1,
            f'BindingMT refused the saved record ({error.code}); inspect its schema and audit checks.\n',
        )

    if record != original:
        parser.exit(1, 'Reading changed the supplied record.\n')
    summary = {
        'scope': (
            'saved_scoring_record_inspection'
            if args.record_kind == 'pose'
            else 'saved_scoring_collection_inspection'
        ),
        'reader': {'bindingmt_version': dmt.__version__, 'ordinary_installed': True},
        'input_sha256': actual,
        'audit': {
            'scope': audit['scope'],
            'status': audit['status'],
            'checks_by_status': dict(Counter(c['status'] for c in audit['checks'])),
        },
        **details,
        'canonical_roundtrip': True,
        'decoded_input_unchanged': True,
        'not_established': [
            'historical software-byte authentication',
            'coordinate correspondence with captured molecular inputs',
            'chemical validity or preparation qualification',
            'score correctness, comparability or binding affinity',
        ],
    }
    if args.record_kind == 'result':
        summary['audit']['incomplete_checks'] = [
            {'path': check['path'], 'reason': check['reason']}
            for check in audit['checks']
            if check['status'] == 'incomplete'
        ]
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
