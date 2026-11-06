"""Inspect a saved scoring pose with an ordinary-installed DockingMT reader.

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pose', type=Path, help='Caller-owned DockingPose JSON file')
    parser.add_argument(
        '--sha256', required=True, help='Independently expected file digest'
    )
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9a-fA-F]{64}', args.sha256):
        parser.error(
            'Provide the independently expected SHA-256 as 64 hexadecimal digits.'
        )
    payload = args.pose.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != args.sha256.lower():
        parser.exit(
            1, 'Input digest differs from the independently expected SHA-256.\n'
        )
    record = json.loads(payload)
    original = deepcopy(record)

    from smonitor.integrations import CatalogException

    import dockingmt as dmt

    distribution = metadata.distribution('dockingmt')
    installation = json.loads(distribution.read_text('direct_url.json') or '{}')
    if (
        installation.get('dir_info', {}).get('editable', False)
        or Path(dmt.__file__).resolve()
        != Path(distribution.locate_file('dockingmt/__init__.py')).resolve()
        or distribution.version != dmt.__version__
    ):
        parser.exit(1, 'Use an ordinary-installed reader without a source overlay.\n')

    try:
        audit = dmt.audit_pose(record)
        if audit['status'] == 'inconsistent':
            for check in audit['checks']:
                if check['status'] == 'inconsistent':
                    print(f'{check["path"]}: {check["reason"]}', file=sys.stderr)
            parser.exit(
                1,
                'Saved scoring evidence is inconsistent; inspect audit_pose checks.\n',
            )
        pose = dmt.DockingPose.from_dict(record)
        canonical = pose.to_dict()
        if dmt.DockingPose.from_dict(canonical).to_dict() != canonical:
            parser.exit(1, 'The admitted pose did not roundtrip independently.\n')
        evaluations = []
        for entry in canonical['metadata'].get('scoring_history', []):
            captures = entry.get('backend_artifacts', {})
            available = all(
                'content_base64' in captures.get(role, {})
                for role in ('receptor', 'partner')
            )
            sizes = dmt.verify_captured_inputs(captures) if available else None
            preparation = entry.get('preparation', {})
            evaluations.append(
                {
                    'score_name': entry.get('score_name'),
                    'backend': entry.get('backend'),
                    'backend_version': entry.get('backend_version'),
                    'producer_dockingmt_version': entry.get('dockingmt_version'),
                    'producer_molsysmt_version': entry.get('molsysmt_version'),
                    'captured_inputs': 'verified' if available else 'unavailable',
                    'captured_bytes': sizes,
                    'recorded_preparation_assessment': {
                        role: preparation.get(role, {})
                        .get('assessment_report', {})
                        .get('assessment')
                        for role in ('receptor', 'partner')
                    },
                }
            )
    except CatalogException as error:
        parser.exit(
            1,
            f'DockingMT refused the saved record ({error.code}); inspect its schema and audit checks.\n',
        )

    if record != original:
        parser.exit(1, 'Reading changed the supplied record.\n')
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
    summary = {
        'scope': 'saved_scoring_record_inspection',
        'reader': {'dockingmt_version': dmt.__version__, 'ordinary_installed': True},
        'input_sha256': actual,
        'audit': {
            'scope': audit['scope'],
            'status': audit['status'],
            'checks_by_status': dict(Counter(c['status'] for c in audit['checks'])),
        },
        'pose': {
            key: canonical.get(key)
            for key in ('pose_id', 'partner_state_id', 'receptor_state_id', 'rank')
        },
        'scores': rows,
        'evaluations': evaluations,
        'canonical_roundtrip': True,
        'decoded_input_unchanged': True,
        'not_established': [
            'historical software-byte authentication',
            'coordinate correspondence with captured molecular inputs',
            'chemical validity or preparation qualification',
            'score correctness, comparability or binding affinity',
        ],
    }
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
