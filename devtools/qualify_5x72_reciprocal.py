"""Prespecified fixed-P59 intervention: search P69, retain all frozen controls.

Reuse the finite 5X72 public preparation, composition, measurement and scoring
operations. Historical observations remain authenticated baseline evidence.
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import sys
from pathlib import Path

import dockingmt as dmt
from devtools.qualify_5x72_occupancy import (
    ARMS,
    BASELINE_SHA,
    DATA,
    INPUTS,
    ROOT,
    diagnostic_rows,
    fixed_pair,
    load_baseline,
    observe,
    prepare_cases,
    prepare_receptors,
    producer_proof,
    sha,
)
from devtools.qualify_181l_receptor import save

OUTPUT = ROOT / 'devguide/validation/data/5x72_reciprocal/audit_2026-10-09.json.gz'


def proof():
    record = producer_proof()
    record['consumer_source_sha256'][str(Path(__file__).relative_to(ROOT))] = sha(
        Path(__file__).read_bytes()
    )
    return record


def qualify(arm, output):
    authenticated = proof()
    sources, cases = prepare_cases()
    assert cases == load_baseline()['cases']
    preparation = prepare_receptors(companion='p59')
    receptor, order = arm.split('_', 1)
    record = {
        'arm': arm,
        'proof': authenticated,
        'cases': cases,
        'preparation': preparation,
        'runs': [],
        'complete': False,
        'consumer_base_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], text=True
        ).strip(),
    }
    for effort, seed in itertools.product((1, 8), (7, 42, 2026)):
        record['runs'].append(
            observe(
                sources['p69'],
                cases['p69'],
                preparation,
                ligand='p69',
                receptor=receptor,
                order=order,
                seed=seed,
                exhaustiveness=effort,
            )
        )
        record['complete'] = len(record['runs']) == 6
        save(record, output)
        print(f'{arm}: {len(record["runs"])}/6', file=sys.stderr, flush=True)


def assemble(paths):
    import gzip
    import json

    parts = [json.loads(gzip.decompress(p.read_bytes())) for p in paths]
    assert {p['arm'] for p in parts} == set(ARMS) and len(parts) == 4
    authenticated = proof()
    for part in parts:
        assert part['complete'] and len(part['runs']) == 6
        assert part['proof'] == authenticated
        for key in ('cases', 'preparation', 'consumer_base_commit'):
            assert part[key] == parts[0][key]
    runs = [r for part in parts for r in part['runs']]
    assert {
        (
            r['receptor'],
            r['order'],
            r['result']['protocol_info']['parameters']['seed'],
            r['result']['protocol_info']['parameters']['exhaustiveness'],
        )
        for r in runs
    } == set(
        itertools.product(
            ('sham', 'occupied'), ('native', 'first_fixed'), (7, 42, 2026), (1, 8)
        )
    )
    historical = []
    for run in load_baseline()['new_runs']:
        if run['ligand'] != 'p69':
            continue
        control = parts[0]['cases']['p69']['controls'][run['order']]
        historical.append(
            {
                'order': run['order'],
                'protocol': run['result']['protocol_info'],
                'fixed_scores': [
                    fixed_pair(
                        pose,
                        control,
                        {
                            'original': (DATA / '5x72_receptor.pdbqt').read_text(),
                            'sham': parts[0]['preparation']['receptors']['sham'][
                                'pdbqt'
                            ],
                        },
                    )
                    for pose in dmt.DockingResult.from_dict(run['result']).poses
                ],
            }
        )
        print(f'historical scores: {len(historical)}/12', file=sys.stderr, flush=True)
    assert sum(len(r['fixed_scores']) for r in historical) == 49
    return {
        'schema': 'dockingmt.5x72_reciprocal_audit@1',
        'date': '2026-10-09',
        'python': sys.version,
        'interpreter': sys.executable,
        **authenticated,
        'consumer_base_commit': parts[0]['consumer_base_commit'],
        'baseline_sha256': BASELINE_SHA,
        'input_sha256': INPUTS,
        'searched_ligand': 'p69',
        'fixed_companion': 'p59',
        'cases': parts[0]['cases'],
        'preparation': parts[0]['preparation'],
        'new_runs': runs,
        'comparison_rows': diagnostic_rows(runs),
        'historical_serialization_scores': historical,
        'criterion': load_baseline()['criterion'],
        'parts': {str(p): sha(p.read_bytes()) for p in paths},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--arm', choices=ARMS)
    parser.add_argument('--parts', nargs=4, type=Path)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.arm:
        qualify(args.arm, args.output)
    elif args.parts:
        save(assemble(args.parts), args.output)
    else:
        parser.error('Supply --arm or four --parts.')
