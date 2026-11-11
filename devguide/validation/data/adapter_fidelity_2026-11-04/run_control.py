"""Dated 3PTB adapter/direct Vina differential control; not a campaign tool.

Reuses authenticated captured backend bytes, without molecular interpretation.
Native calculations require a clean, explicitly registered producer commit.
"""

import argparse
import base64
import gzip
import hashlib
import importlib.metadata
import inspect
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
import warnings
from functools import wraps
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
INPUT = ROOT / 'devguide/validation/data/human_3ptb/native_result_2026-10-20.json.gz'
INPUT_SHA256 = '4b1f51cdeb135fd6785a181f6bb09a0d0f631ec3d9de7c169c88703748924249'
ROLE_SHA256 = {
    'receptor': 'edeff77e6222c5c5ab1aa6be2354efc323c0ffe8a7884366069ee0addbf7b970',
    'partner': 'a36bd740cc47045c2f2f6756bd8c11b41cbcc960a76ce42c2f2114b3c4b7be46',
}
CONSTRUCTOR = {
    'sf_name': 'vina',
    'cpu': 1,
    'seed': 7,
    'no_refine': False,
    'verbosity': 0,
}
MAPS = {
    'center': [-1.759111, 14.461, 16.915778],
    'box_size': [20.0, 20.0, 20.0],
    'spacing': 0.375,
    'force_even_voxels': False,
}
DOCK = {'exhaustiveness': 1, 'n_poses': 9, 'min_rmsd': 1.0, 'max_evals': 0}
OUTPUT = {'n_poses': 9, 'energy_range': 3.0}
METHODS = (
    '__init__',
    'set_receptor',
    'set_ligand_from_file',
    'set_ligand_from_string',
    'compute_vina_maps',
    'dock',
    'poses',
    'energies',
)


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def write(path, record):
    path.write_text(
        json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + '\n'
    )


def inputs():
    payload = INPUT.read_bytes()
    assert sha(payload) == INPUT_SHA256
    original = json.loads(gzip.decompress(payload))
    roles = {}
    for role, checksum in ROLE_SHA256.items():
        item = original['provenance']['backend_artifacts'][role]
        roles[role] = base64.b64decode(item['content_base64'], validate=True)
        assert sha(roles[role]) == item['sha256'] == checksum
    return roles


def git(root, *arguments):
    return subprocess.check_output(
        ['git', '-C', str(root), *arguments], text=True
    ).strip()


def environment():
    import dockingmt
    import molsysmt
    import vina

    assert Path(dockingmt.__file__).resolve().parent == ROOT / 'dockingmt'
    assert vina.__version__ == '1.2.7'
    modules = {}
    for name in (
        'dockingmt',
        'molsysmt',
        'vina',
        'numpy',
        'pyunitwizard',
        'argdigest',
        'depdigest',
        'smonitor',
    ):
        module = __import__(name)
        modules[name] = {
            'distribution_version': importlib.metadata.version(name),
            'reported_version': getattr(module, '__version__', None),
            'entry_sha256': sha(Path(module.__file__).read_bytes()),
        }
    provider_root = Path(molsysmt.__file__).resolve().parents[1]
    assert not git(provider_root, 'status', '--porcelain')
    check = subprocess.run(
        [sys.executable, '-m', 'pip', 'check'], text=True, capture_output=True
    )
    vina_root = Path(vina.__file__).resolve().parent
    return {
        'python': platform.python_version(),
        'system': platform.system(),
        'machine': platform.machine(),
        'consumer_installation': 'editable_source',
        'modules': modules,
        'molsysmt_source': git(provider_root, 'rev-parse', 'HEAD'),
        'runtime_sha256': {
            p.relative_to(ROOT).as_posix(): sha(p.read_bytes())
            for p in sorted((ROOT / 'dockingmt').rglob('*.py'))
        },
        'vina_payload_sha256': {
            p.relative_to(vina_root).as_posix(): sha(p.read_bytes())
            for p in sorted(vina_root.rglob('*'))
            if p.is_file() and p.suffix in ('.py', '.so')
        },
        'native_signatures': {
            name: str(inspect.signature(getattr(vina.Vina, name))) for name in METHODS
        },
        'pip_check': {
            'exit': check.returncode,
            'diagnostics': check.stdout.splitlines(),
        },
    }


def observed_class(original, calls, native, output):
    """Observe public calls/results unchanged; do not parse molecular records."""

    def observe(name):
        function = getattr(original, name)

        @wraps(function)
        def invoke(self, *args, **kwargs):
            bound = inspect.signature(function).bind(self, *args, **kwargs)
            bound.apply_defaults()
            arguments = dict(bound.arguments)
            del arguments['self']
            if name == 'set_receptor':
                assert arguments['flex_pdbqt_filename'] is None
                arguments['rigid_pdbqt_filename'] = {
                    'sha256': sha(Path(arguments['rigid_pdbqt_filename']).read_bytes())
                }
            elif name == 'set_ligand_from_file':
                arguments['pdbqt_filename'] = {
                    'sha256': sha(Path(arguments['pdbqt_filename']).read_bytes())
                }
            elif name == 'set_ligand_from_string':
                arguments['pdbqt_string'] = {
                    'sha256': sha(arguments['pdbqt_string'].encode())
                }
            calls.append({'method': name, 'arguments': arguments})
            write(output / 'calls.json', calls)
            if name == 'dock':
                assert sum(c['method'] == 'dock' for c in calls) == 1
            value = function(self, *args, **kwargs)
            if name == 'poses':
                key = 'coordinates' if arguments['coordinates_only'] else 'poses_pdbqt'
                native[key] = value.tolist() if arguments['coordinates_only'] else value
            elif name == 'energies':
                native['energies'] = value.tolist()
            if name in ('poses', 'energies'):
                native['engine_info'] = {
                    key: val
                    for key, val in self.info().items()
                    if key not in ('receptor_rigid', 'receptor_flex', 'ligands')
                }
                write(output / 'native.json', native)
            return value

        return invoke

    return type('ObservedVina', (original,), {name: observe(name) for name in METHODS})


def run_route(route, output, expected_head):
    assert git(ROOT, 'rev-parse', 'HEAD') == expected_head
    assert not git(ROOT, 'status', '--porcelain')
    roles = inputs()
    actual_environment = environment()
    assert actual_environment == json.loads((HERE / 'preflight.json').read_text())
    output.mkdir(exist_ok=False)
    write(
        output / 'identity.json',
        {
            'source': expected_head,
            'producer_sha256': sha(Path(__file__).read_bytes()),
            'environment': actual_environment,
        },
    )
    import dockingmt as dmt
    import pyunitwizard as puw
    import vina

    calls, native = [], {}
    original = vina.Vina
    observer = observed_class(original, calls, native, output)
    started = time.perf_counter()
    diagnostics = []
    with (
        warnings.catch_warnings(),
        tempfile.TemporaryDirectory(prefix='dmt-fidelity-inputs-') as directory,
    ):
        warnings.simplefilter('always')
        original_showwarning = warnings.showwarning

        def showwarning(message, category, *args, **kwargs):
            diagnostics.append({'category': category.__name__, 'message': str(message)})
            write(output / 'warnings.json', diagnostics)
            original_showwarning(message, category, *args, **kwargs)

        warnings.showwarning = showwarning
        paths = {}
        for role, payload in roles.items():
            paths[role] = Path(directory, role + '.pdbqt')
            paths[role].write_bytes(payload)
        if route == 'adapter':
            vina.Vina = observer
            try:
                result = dmt.dock(
                    dmt.DockingProblem(
                        str(paths['receptor']),
                        str(paths['partner']),
                        dmt.BoxRegion(
                            center=puw.quantity(MAPS['center'], 'angstrom'),
                            size=puw.quantity(MAPS['box_size'], 'angstrom'),
                        ),
                    ),
                    dmt.VinaProtocol(
                        cpu=1,
                        seed=7,
                        exhaustiveness=1,
                        n_poses=9,
                        capture_backend_inputs=True,
                    ),
                )
            finally:
                vina.Vina = original
            write(
                output / 'normalized.json',
                {
                    'n_poses': len(result),
                    'scores': [pose.scores for pose in result.poses],
                    'ranks': [pose.rank for pose in result.poses],
                    'score_definitions': result.poses[0].score_definitions
                    if result.poses
                    else {},
                    'recorded_energies': result.provenance['backend_output'][
                        'energies'
                    ],
                    'recorded_calls': result.provenance['backend_output'][
                        'resolved_calls'
                    ],
                    'backend_box': result.provenance['backend_box'],
                    'input_sha256': {
                        role: item['sha256']
                        for role, item in result.provenance['backend_artifacts'].items()
                    },
                    'pose_reading': result.provenance['backend_output'].get(
                        'pose_reading'
                    ),
                },
            )
        else:
            engine = observer(**CONSTRUCTOR)
            engine.set_receptor(rigid_pdbqt_filename=str(paths['receptor']))
            engine.set_ligand_from_file(str(paths['partner']))
            engine.compute_vina_maps(**MAPS)
            engine.dock(**DOCK)
            engine.poses(**OUTPUT, coordinates_only=True)
            engine.energies(**OUTPUT)
            engine.poses(**OUTPUT, coordinates_only=False)
        assert all(
            sha(path.read_bytes()) == ROLE_SHA256[role] for role, path in paths.items()
        )
    write(
        output / 'completion.json',
        {
            'completed': True,
            'seconds': time.perf_counter() - started,
            'warnings': diagnostics,
            'staged_inputs_retired': not Path(directory).exists(),
        },
    )


def compare(output):
    def read(route, name):
        return json.loads((output / route / (name + '.json')).read_text())

    expected = [
        {'method': '__init__', 'arguments': CONSTRUCTOR},
        {
            'method': 'set_receptor',
            'arguments': {
                'rigid_pdbqt_filename': {'sha256': ROLE_SHA256['receptor']},
                'flex_pdbqt_filename': None,
            },
        },
        {
            'method': 'set_ligand_from_file',
            'arguments': {'pdbqt_filename': {'sha256': ROLE_SHA256['partner']}},
        },
        {'method': 'compute_vina_maps', 'arguments': MAPS},
        {'method': 'dock', 'arguments': DOCK},
        {'method': 'poses', 'arguments': {**OUTPUT, 'coordinates_only': True}},
        {'method': 'energies', 'arguments': OUTPUT},
        {'method': 'poses', 'arguments': {**OUTPUT, 'coordinates_only': False}},
    ]
    adapter, direct = read('adapter', 'native'), read('direct', 'native')
    normalized = read('adapter', 'normalized')
    n_poses = len(direct['energies'])
    checks = {
        'prescribed_adapter_calls': read('adapter', 'calls') == expected,
        'prescribed_direct_calls': read('direct', 'calls') == expected,
        'same_native_energies': adapter['energies'] == direct['energies'],
        'same_native_coordinate_array': adapter['coordinates'] == direct['coordinates'],
        'same_native_pdbqt_bytes': adapter['poses_pdbqt'] == direct['poses_pdbqt'],
        'same_engine_info': adapter['engine_info'] == direct['engine_info'],
        'nonempty_consistent_pose_counts': 0
        < n_poses
        == normalized['n_poses']
        == len(adapter['coordinates'])
        == len(direct['coordinates'])
        <= OUTPUT['n_poses'],
        'recorded_full_energy_matrix': normalized['recorded_energies']
        == direct['energies'],
        'normalized_four_score_columns': normalized['scores']
        == [
            dict(zip(('vina', 'inter', 'intra', 'torsion'), row[:4], strict=True))
            for row in direct['energies']
        ],
        'normalized_score_units': set(normalized['score_definitions'])
        == {'vina', 'inter', 'intra', 'torsion'}
        and all(
            value['unit'] == 'kcal/mol'
            for value in normalized['score_definitions'].values()
        ),
        'normalized_ranks': normalized['ranks'] == list(range(1, n_poses + 1)),
        'recorded_resolved_calls': normalized['recorded_calls']
        == {'compute_vina_maps': MAPS, 'dock': DOCK, 'energies': OUTPUT},
        'recorded_input_hashes': normalized['input_sha256'] == ROLE_SHA256,
        'recorded_box': normalized['backend_box']
        == {
            'center': MAPS['center'],
            'size': MAPS['box_size'],
            'unit': 'angstrom',
            'rounding_decimals': 6,
        },
    }
    for route in ('adapter', 'direct'):
        checks[route + '_completed_once'] = (
            read(route, 'completion')['completed']
            and sum(c['method'] == 'dock' for c in read(route, 'calls')) == 1
        )
    return {
        'scope': 'same_host_exact_input_adapter_fidelity',
        'n_new_search_attempts': 2,
        'n_returned_poses_per_route': n_poses,
        'checks': checks,
        'passed': all(checks.values()),
        'geometry_identity_and_physical_validity': 'not_assessed',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--route', choices=('adapter', 'direct'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expected-head')
    args = parser.parse_args()
    if args.check:
        roles = inputs()
        print(
            json.dumps(
                {
                    'authenticated_input_bytes': {k: len(v) for k, v in roles.items()},
                    'native_calls': 0,
                }
            )
        )
        return
    if not args.output or not args.expected_head:
        parser.error('--output and --expected-head are required for execution')
    if args.route:
        run_route(args.route, args.output, args.expected_head)
        return
    args.output.mkdir(exist_ok=False)
    try:
        for route in ('adapter', 'direct'):
            with tempfile.TemporaryDirectory(prefix='dmt-fidelity-cache-') as cache:
                env = dict(os.environ, XDG_CACHE_HOME=cache, TMPDIR=cache)
                with (args.output / (route + '.log')).open('wb') as stream:
                    process = subprocess.run(
                        [
                            sys.executable,
                            '-I',
                            '-B',
                            str(Path(__file__).resolve()),
                            '--route',
                            route,
                            '--output',
                            str((args.output / route).resolve()),
                            '--expected-head',
                            args.expected_head,
                        ],
                        env=env,
                        stdout=stream,
                        stderr=subprocess.STDOUT,
                        timeout=300,
                    )
            if (
                sum(p.stat().st_size for p in args.output.rglob('*') if p.is_file())
                > 32 * 1024**2
            ):
                raise RuntimeError(
                    'Evidence ceiling exceeded; stop and retain observations'
                )
            if process.returncode:
                raise RuntimeError(
                    f'{route} worker exited {process.returncode}; no retry'
                )
        summary = compare(args.output)
        write(args.output / 'summary.json', summary)
        if not summary['passed']:
            raise RuntimeError('Differential mismatch; no tolerance change or retry')
    except Exception as exc:
        write(
            args.output / 'failure.json',
            {'type': type(exc).__name__, 'message': str(exc)},
        )
        raise
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
