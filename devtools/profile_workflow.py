"""Measure bounded Vina workflows in fresh processes, with paired timing modes.

Usage:
    python devtools/profile_workflow.py --report /tmp/181l-profile.json
    python devtools/profile_workflow.py --manifest /tmp/181l-manifest.json --report /tmp/pdbqt-profile.json

The default case uses existing provisional 181L preparation. A captured manifest
instead supplies verified PDBQT bytes directly, bypassing molecular preparation.
Neither route constitutes scientific qualification of the docking chemistry.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import platform
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


def _sample(collect_timings: bool, manifest_path: Path | None) -> dict[str, Any]:
    """Run one workflow; interpreter startup and OS cache reset are excluded."""
    started = time.perf_counter()
    import molsysmt as msm
    import pyunitwizard as puw

    import dockingmt

    import_seconds = time.perf_counter() - started
    # Import bookkeeping helpers outside the measured scientific phases.
    from devtools.redocking_181l import _source_revision, _verify_captured_inputs

    started = time.perf_counter()
    if manifest_path is None:
        source = Path(msm.systems['T4 lysozyme L99A']['181l.pdb']).resolve()
        problem = dockingmt.DockingProblem.for_redocking(
            complex_system=source,
            receptor_selection="molecule_type=='protein'",
            partner_selection="group_name=='BNZ'",
            padding=puw.quantity(8.0, 'angstrom'),
            metadata={'pdb_id': '181L', 'ligand_name': 'BNZ'},
        )
        protocol = dockingmt.VinaProtocol(
            exhaustiveness=1,
            n_poses=5,
            seed=42,
            cpu=1,
            allow_provisional_preparation=True,
            capture_backend_inputs=True,
            collect_timings=collect_timings,
        )
        input_identity = {
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        }
    else:
        manifest_bytes = manifest_path.read_bytes()
        recorded = dockingmt.DockingResult.from_dict(json.loads(manifest_bytes))
        if recorded.provenance.get('backend') != 'vina':
            raise ValueError('A captured Vina result is required.')
        artifacts = recorded.provenance['backend_artifacts']
        _verify_captured_inputs(artifacts)
        # Reuse explicit captured inputs and domain, without restoring a molecular
        # source or claiming the original source-to-pose atom map in this route.
        problem = dockingmt.DockingProblem(
            receptor=base64.b64decode(artifacts['receptor']['content_base64']).decode(),
            partner=base64.b64decode(artifacts['partner']['content_base64']).decode(),
            search_domain=dockingmt.BoxRegion.from_dict(
                recorded.problem_info['search_domain']
            ),
            constraints=recorded.problem_info.get('constraints', []),
            search_guidance=recorded.problem_info.get('search_guidance', []),
        )
        specification = recorded.protocol_info
        specification['parameters']['collect_timings'] = collect_timings
        protocol = dockingmt.VinaProtocol.from_dict(specification)
        if protocol.seed is None or protocol.cpu != 1:
            raise ValueError('Paired profiling requires an explicit seed and cpu=1.')
        if protocol.active_torsion_bonds:
            raise ValueError(
                'Captured PDBQT already owns its torsions; clear protocol torsions.'
            )
        input_identity = {'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest()}
    input_seconds = time.perf_counter() - started

    started = time.perf_counter()
    result = dockingmt.dock(problem, protocol=protocol, backend='vina')
    dock_seconds = time.perf_counter() - started
    started = time.perf_counter()
    record = result.to_dict()
    export_seconds = time.perf_counter() - started
    started = time.perf_counter()
    encoded = json.dumps(record, sort_keys=True).encode()
    encoding_seconds = time.perf_counter() - started
    with tempfile.TemporaryDirectory(prefix='dockingmt-profile-export-') as directory:
        started = time.perf_counter()
        Path(directory, 'result.json').write_bytes(encoded)
        write_seconds = time.perf_counter() - started

    # Compare actual pose snapshots and submitted inputs, excluding clocks and the
    # diagnostic flag. Equality is a same-host seeded check, not a science gate.
    scientific_output = {
        'poses': record['poses'],
        'backend_box': record['provenance']['backend_box'],
        'backend_artifacts': record['provenance']['backend_artifacts'],
    }
    return {
        'collect_timings': collect_timings,
        'measurements': {
            'import': import_seconds,
            'input_normalization': input_seconds,
            'dock_call': dock_seconds,
            'result_export': export_seconds,
            'json_encoding': encoding_seconds,
            'file_write': write_seconds,
        },
        'adapter_timings': result.provenance.get('timings'),
        'native_elapsed_seconds': result.provenance['elapsed_seconds'],
        'n_poses': len(result),
        'export_bytes': len(encoded),
        'scientific_sha256': hashlib.sha256(
            json.dumps(scientific_output, sort_keys=True).encode()
        ).hexdigest(),
        'input_identity': input_identity,
        'protocol': protocol.to_dict(),
        'environment': {
            'python': platform.python_version(),
            'platform': platform.platform(),
            'versions': {
                name: getattr(sys.modules.get(name), '__version__', 'unknown')
                for name in (
                    'dockingmt',
                    'molsysmt',
                    'pyunitwizard',
                    'numpy',
                    'vina',
                    'argdigest',
                    'depdigest',
                    'smonitor',
                )
            },
        },
        'source_revision': _source_revision(),
        'profiler_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def _summarize(samples: list[dict[str, Any]]) -> dict[str, Any]:
    """Retain raw evidence and describe paired overhead without a speed budget."""
    enabled = [sample for sample in samples if sample['collect_timings']]
    disabled = [sample for sample in samples if not sample['collect_timings']]
    if not enabled or len(enabled) != len(disabled):
        raise ValueError(
            'Equal nonempty timing-enabled and timing-disabled samples are required.'
        )
    measurement_medians = {
        mode: {
            name: statistics.median(sample['measurements'][name] for sample in group)
            for name in group[0]['measurements']
        }
        for mode, group in (('enabled', enabled), ('disabled', disabled))
    }
    phase_medians = {
        name: statistics.median(
            sample['adapter_timings']['phases'][name] for sample in enabled
        )
        for name in enabled[0]['adapter_timings']['phases']
    }
    return {
        'schema_version': '1.0',
        'unit': 'second',
        'clock': 'perf_counter',
        'workload': 'captured_pdbqt'
        if 'manifest_sha256' in samples[0]['input_identity']
        else '181L_provisional',
        'method': (
            'Fresh interpreter per sample; alternating paired modes; same explicit seed and cpu=1; '
            'OS caches retained; startup and report bookkeeping excluded; file writes do not fsync. '
            'Adapter total is contained within dock_call. Native elapsed overlaps native_docking. '
            'Difference of medians includes run-to-run noise and is not a portable timing budget.'
        ),
        'scientific_outputs_match': len(
            {sample['scientific_sha256'] for sample in samples}
        )
        == 1,
        'input_identities_match': all(
            sample['input_identity'] == samples[0]['input_identity']
            for sample in samples
        ),
        'execution_contexts_match': all(
            all(
                sample[field] == samples[0][field]
                for field in (
                    'environment',
                    'source_revision',
                    'profiler_sha256',
                )
            )
            for sample in samples
        ),
        'measurement_medians': measurement_medians,
        'adapter_phase_medians': phase_medians,
        'dock_call_median_difference': measurement_medians['enabled']['dock_call']
        - measurement_medians['disabled']['dock_call'],
        'samples': samples,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--manifest', type=Path)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--sample-output', type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        '--collect-timings', action='store_true', help=argparse.SUPPRESS
    )
    args = parser.parse_args()
    if args.sample_output is not None:
        sample = _sample(args.collect_timings, args.manifest)
        args.sample_output.write_text(json.dumps(sample, indent=2) + '\n')
        return
    if args.report is None or args.repeats < 1:
        parser.error('--report is required and --repeats must be positive.')
    root = Path(__file__).resolve().parents[1]
    samples = []
    with tempfile.TemporaryDirectory(prefix='dockingmt-profile-') as directory:
        for pair in range(args.repeats):
            for enabled in (False, True) if pair % 2 == 0 else (True, False):
                output = Path(directory, 'sample.json')
                command = [
                    sys.executable,
                    '-m',
                    'devtools.profile_workflow',
                    '--sample-output',
                    str(output),
                ]
                if enabled:
                    command.append('--collect-timings')
                if args.manifest is not None:
                    command.extend(['--manifest', str(args.manifest.resolve())])
                subprocess.run(command, cwd=root, check=True)
                samples.append(json.loads(output.read_text()))
    report = _summarize(samples)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    if not all(
        report[field]
        for field in (
            'scientific_outputs_match',
            'input_identities_match',
            'execution_contexts_match',
        )
    ):
        raise SystemExit(
            'Paired profiling changed outputs, inputs, or execution context; inspect the written report.'
        )
    print(
        json.dumps(
            {key: value for key, value in report.items() if key != 'samples'}, indent=2
        )
    )


if __name__ == '__main__':
    main()
