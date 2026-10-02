"""Benchmark existing result snapshots without docking or molecular operations.

Usage:
    python -m devtools.benchmark_result_export --report /tmp/export-before.json --memory --profile
    python -m devtools.benchmark_result_export --report /tmp/export-after.json --reference /tmp/export-before.json --memory --profile

Imports, fixture construction, hashing, GC between trials and snapshot disposal
are outside elapsed samples. Memory/profile runs are separate from time samples.
Synthetic records exercise coordinate volume and existing atom-map metadata;
they do not claim campaign capacity, docking quality or portable timing budgets.
"""

from __future__ import annotations

import argparse
import base64
import cProfile
import gc
import hashlib
import json
import platform
import pstats
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dockingmt import DockingResult

CASES = {
    'small_mapped': (9, 64, True),
    'many_small': (256, 32, False),
    'large_coordinates': (256, 1024, False),
    'many_poses': (1024, 32, False),
    'large_mapped': (256, 1024, True),
}


def _synthetic_result(count: int, atoms: int, mapped: bool) -> DockingResult:
    """Build a deterministic serialization fixture, with explicit length units."""
    import numpy as np
    import pyunitwizard as puw

    from dockingmt import DockingPose, DockingResult, VinaProtocol

    atom_indices = list(range(atoms))
    metadata = {
        'pose_atom_order': 'synthetic_serialization_fixture',
        'annotations': {'labels': ['benchmark'], 'values': [1, 2, 3]},
    }
    if mapped:
        metadata.update(
            {
                'prepared_atom_indices': atom_indices,
                'selected_atom_indices': atom_indices,
                'source_atom_indices': atom_indices,
                'selected_partner_n_atoms': atoms,
                'source_atom_keys': [
                    {
                        'atom_id': str(index),
                        'atom_name': f'C{index}',
                        'element': 'C',
                        'group_id': '1',
                        'group_name': 'LIG',
                    }
                    for index in atom_indices
                ],
            }
        )
    coordinates = np.arange(atoms * 3, dtype=float).reshape(atoms, 3) * 0.001
    poses = [
        DockingPose(
            puw.quantity(coordinates + index * 0.00001, 'nm'),
            scores={
                'vina': -8 + index * 0.001,
                'inter': -9.0,
                'intra': 0.0,
                'torsion': 1.0,
            },
            rank=index + 1,
            pose_id=f'pose_{index + 1}',
            partner_state_id='ligand_state',
            receptor_state_id='receptor_state',
            metadata=metadata,
        )
        for index in range(count)
    ]
    artifact_bytes = b'synthetic serialization payload\n' * 128
    return DockingResult(
        poses,
        problem_info={
            'metadata': {'case': 'synthetic_serialization_only'},
            'molecular_inputs': {'partner': {'atom_indices': atom_indices}},
        },
        protocol_info=VinaProtocol(seed=42, cpu=1).to_dict(),
        provenance={
            'assessment': 'synthetic_serialization_only',
            'backend_artifacts': {
                'partner': {
                    'format': 'synthetic',
                    'sha256': hashlib.sha256(artifact_bytes).hexdigest(),
                    'content_base64': base64.b64encode(artifact_bytes).decode(),
                }
            },
        },
    )


def _measure(
    result: DockingResult, repeats: int, memory: bool, profile: bool
) -> dict[str, Any]:
    seconds = []
    for _ in range(repeats):
        gc.collect()
        started = time.perf_counter()
        record = result.to_dict()
        seconds.append(time.perf_counter() - started)
        del record
    record = result.to_dict()
    encoded = json.dumps(record, sort_keys=True, allow_nan=False).encode()
    measurement = {
        'seconds': seconds,
        'median_seconds': statistics.median(seconds),
        'n_poses': len(result),
        'atoms_per_pose': [pose.n_atoms for pose in result],
        'json_bytes': len(encoded),
        'record_sha256': hashlib.sha256(encoded).hexdigest(),
    }
    del record, encoded
    if memory:
        gc.collect()
        tracemalloc.start()
        try:
            record = result.to_dict()
            measurement['python_peak_bytes'] = tracemalloc.get_traced_memory()[1]
            del record
        finally:
            tracemalloc.stop()
    if profile:
        profiler = cProfile.Profile()
        record = profiler.runcall(result.to_dict)
        stats = pstats.Stats(profiler).stats
        measurement['profile_top_cumulative'] = [
            {
                'function': f'{Path(filename).name}:{line}:{name}',
                'primitive_calls': primitive,
                'total_calls': total,
                'self_seconds': own,
                'cumulative_seconds': cumulative,
            }
            for (filename, line, name), (
                primitive,
                total,
                own,
                cumulative,
                _,
            ) in sorted(stats.items(), key=lambda item: item[1][3], reverse=True)[:8]
        ]
        del record
    return measurement


def _compare(report: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    """Compare only matching payloads/settings/environment; retain noisy timings."""
    if reference.get('schema_version') != '1.0' or reference.get('unit') != 'second':
        raise ValueError('Expected a version 1.0 benchmark report with second units.')
    if any(
        reference.get(field) != report.get(field)
        for field in ('clock', 'method', 'memory_unit')
    ):
        raise ValueError('Reference measurement definitions differ.')
    if (
        reference['environment'] != report['environment']
        or reference['repeats'] != report['repeats']
    ):
        raise ValueError('Reference environment or repeat count differs.')
    if reference['cases'].keys() != report['cases'].keys():
        raise ValueError('Reference case selection differs.')
    comparison = {}
    for name, current in report['cases'].items():
        previous = reference['cases'][name]
        if current['record_sha256'] != previous['record_sha256']:
            raise ValueError(f'{name}: serialized content differs from the reference.')
        comparison[name] = {
            'records_match': True,
            'reference_median_seconds': previous['median_seconds'],
            'current_median_seconds': current['median_seconds'],
            'median_ratio': current['median_seconds'] / previous['median_seconds'],
        }
    return comparison


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--reference', type=Path)
    parser.add_argument(
        '--manifest',
        type=Path,
        help='Also benchmark an existing DockingResult JSON record.',
    )
    parser.add_argument('--case', choices=CASES, action='append')
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--memory', action='store_true')
    parser.add_argument('--profile', action='store_true')
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error('--repeats must be positive.')
    from devtools.redocking_181l import _source_revision
    from dockingmt import DockingResult

    cases = {
        name: _measure(
            _synthetic_result(*CASES[name]), args.repeats, args.memory, args.profile
        )
        for name in (args.case or CASES)
    }
    if args.manifest is not None:
        content = args.manifest.read_bytes()
        result = DockingResult.from_dict(json.loads(content))
        cases['manifest'] = _measure(result, args.repeats, args.memory, args.profile)
        cases['manifest']['manifest_sha256'] = hashlib.sha256(content).hexdigest()
    report = {
        'schema_version': '1.0',
        'unit': 'second',
        'clock': 'perf_counter',
        'memory_unit': 'byte',
        'repeats': args.repeats,
        'method': 'One process per report; imports/construction/GC/hash/disposal excluded; '
        'tracemalloc peak Python allocations and cProfile collected in separate calls; '
        'cumulative profile times overlap; OS caches retained; no portable budget.',
        'environment': {
            'python': platform.python_version(),
            'platform': platform.platform(),
            'versions': {
                name: getattr(sys.modules[name], '__version__', 'unknown')
                for name in (
                    'numpy',
                    'pyunitwizard',
                    'argdigest',
                    'depdigest',
                    'smonitor',
                )
            },
        },
        'source_revision': _source_revision(),
        'benchmark_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'cases': cases,
    }
    if args.reference is not None:
        report['comparison'] = _compare(report, json.loads(args.reference.read_text()))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(
        json.dumps(
            {
                name: {
                    key: value
                    for key, value in case.items()
                    if key in ('median_seconds', 'json_bytes', 'python_peak_bytes')
                }
                for name, case in cases.items()
            },
            indent=2,
        )
    )


if __name__ == '__main__':
    main()
