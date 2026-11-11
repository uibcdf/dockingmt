"""Receive the current source-only 0.1.0 candidate on fresh hosted runners.

Component-owned profile for #74. Shared SDKs own dependency/source validation,
installed support and runtime-origin checks. This entry point never publishes.
"""

import ast
import gzip
import hashlib
import importlib.abc
import importlib.metadata as metadata
import importlib.util
import json
import os
import platform
import re
import resource
import shutil
import subprocess
import sys
import tomllib
import types
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / '.molsyssuite/current-0.1.0-hosted'
PROFILE = ROOT / 'devtools/source_0_1_0_current.toml'
VERSION = '0.1.0'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def git(path, *arguments):
    return subprocess.check_output(
        ['git', '-C', str(path), *arguments], text=True
    ).strip()


def profile():
    data = tomllib.loads(PROFILE.read_text())
    if data['version'] != VERSION or len(data['sources']) != 6:
        raise ValueError('Use the reviewed current 0.1.0 source profile')
    if any(not re.fullmatch('[0-9a-f]{40}', sha) for sha in data['sources'].values()):
        raise ValueError('Source identities must be full immutable commits')
    return data


def require_hosted():
    if (
        os.environ.get('GITHUB_ACTIONS') != 'true'
        or os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted'
    ):
        raise ValueError('Heavy qualification requires a GitHub-hosted runner')
    candidate_sha = os.environ.get('CANDIDATE_SHA', '')
    if not re.fullmatch('[0-9a-f]{40}', candidate_sha):
        raise ValueError('Select one reviewed full candidate commit')
    if candidate_sha != os.environ.get('GITHUB_SHA'):
        raise ValueError('Qualification source must be the exact selected candidate')
    candidate = TASK / 'candidate'
    if git(candidate, 'rev-parse', 'HEAD') != candidate_sha:
        raise ValueError('Candidate checkout does not match the selected commit')
    if git(candidate, 'status', '--porcelain', '--untracked-files=no'):
        raise ValueError('Candidate tracked inputs must remain clean before receiving')
    if sys.platform != 'linux' or platform.machine() != 'x86_64':
        raise ValueError('This profile receives Linux x86_64 only')
    if (candidate / 'devtools/source_0_1_0_current.toml').read_bytes() != (
        PROFILE.read_bytes()
    ):
        raise ValueError('Qualification and candidate source profiles differ')
    return candidate


def save(name, value):
    path = TASK / 'evidence' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def identity(candidate):
    return {
        'candidate': git(candidate, 'rev-parse', 'HEAD'),
        'tree': git(candidate, 'rev-parse', 'HEAD^{tree}'),
        'qualification_source': os.environ['GITHUB_SHA'],
        'version': VERSION,
        'profile_sha256': digest(PROFILE),
        'run_id': int(os.environ['GITHUB_RUN_ID']),
        'run_attempt': int(os.environ['GITHUB_RUN_ATTEMPT']),
        'python': platform.python_version(),
        'platform': platform.platform(),
        'public_package_or_github_release': False,
    }


def candidate_contract(candidate):
    """Derive expected wheel inputs from the selected source, before building."""
    project = tomllib.loads((candidate / 'pyproject.toml').read_text())['project']
    paths = git(
        candidate, 'ls-files', 'dockingmt', 'molsysviewer_dockingmt'
    ).splitlines()
    runtime = {name: digest(candidate / name) for name in paths}
    stamp = '__version__ = "0.1.0"\n'.encode()
    runtime['dockingmt/_version.py'] = hashlib.sha256(stamp).hexdigest()
    requirements = list(project['dependencies'])
    for extra, dependencies in project.get('optional-dependencies', {}).items():
        for dependency in dependencies:
            req = Requirement(dependency)
            marker = f'({req.marker}) and ' if req.marker else ''
            req.marker = None
            requirements.append(f'{req}; {marker}extra == "{extra}"')
    return {
        'archive_checks': {
            'runtime_sha256': runtime,
            'python_requires': project['requires-python'],
            'requires_dist': requirements,
        },
        'source_input_sha256': {
            name: digest(candidate / name)
            for name in [
                'LICENSE',
                'README.md',
                'pyproject.toml',
                'devtools/conda-build/resources.toml',
                'devtools/source_0_1_0_current.toml',
            ]
        },
    }


def check_wheel(wheel, expected):
    """Reuse the original component's tested wheel boundary, not its candidate."""
    path = ROOT / 'devtools/qualify_source_0_1_0.py'
    spec = importlib.util.spec_from_file_location('_dmt_historical_wheel_guard', path)
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    return guard.wheel_payload(wheel, expected)


def build():
    candidate = require_hosted()
    if git(candidate, 'status', '--porcelain', '--untracked-files=no'):
        raise ValueError('Candidate tracked inputs must be clean')
    expected = candidate_contract(candidate)
    for remote in git(candidate, 'remote').splitlines():
        subprocess.run(
            ['git', '-C', str(candidate), 'remote', 'remove', remote], check=True
        )
    subprocess.run(
        [
            'git',
            '-C',
            str(candidate),
            '-c',
            'tag.gpgSign=false',
            'tag',
            VERSION,
            os.environ['CANDIDATE_SHA'],
        ],
        check=True,
    )
    if git(candidate, 'cat-file', '-t', 'refs/tags/' + VERSION) != 'commit':
        raise ValueError('The private validation tag must be lightweight')
    subprocess.run(
        [
            sys.executable,
            '-m',
            'build',
            '--wheel',
            '--no-isolation',
            '--outdir',
            str(TASK / 'wheels'),
            str(candidate),
        ],
        check=True,
    )
    wheel = TASK / 'wheels/dockingmt-0.1.0-py3-none-any.whl'
    runtime = check_wheel(wheel, expected)
    if git(candidate, 'status', '--porcelain', '--untracked-files=no'):
        raise ValueError('Build changed tracked candidate inputs')
    receipt = identity(candidate)
    receipt.update(
        wheel_sha256=digest(wheel),
        runtime_sha256=runtime,
        contract=expected,
        private_lightweight_tag_only=True,
        build_tools={
            name: metadata.version(name)
            for name in ['build', 'setuptools', 'wheel', 'versioningit', 'packaging']
        },
    )
    save('build-receipt.json', receipt)
    with Path(os.environ['GITHUB_OUTPUT']).open('a') as output:
        output.write('wheel_sha256=' + receipt['wheel_sha256'] + '\n')


def sources():
    """Observe clean source inputs and absent native files before construction."""
    candidate = require_hosted()
    memory = {
        key.rstrip(':'): int(value.split()[0]) * 1024
        for key, value in (
            line.split(':', 1)
            for line in Path('/proc/meminfo').read_text().splitlines()
        )
        if key in {'MemTotal', 'MemAvailable'}
    }
    reserve = max(memory['MemTotal'] // 5, 1536 * 1024**2)
    if memory['MemAvailable'] < reserve + 2 * 1024**3:
        raise ValueError(
            'Hosted source construction lacks its conservative memory margin'
        )
    if len(os.sched_getaffinity(0)) != 1 or os.getpriority(os.PRIO_PROCESS, 0) < 10:
        raise ValueError('Source construction requires one low-priority logical CPU')
    observed = {}
    for name, sha in profile()['sources'].items():
        source = TASK / name
        if git(source, 'rev-parse', 'HEAD') != sha or git(
            source, 'status', '--porcelain', '--untracked-files=no'
        ):
            raise ValueError('Source checkout is not the clean selected input: ' + name)
        native_files = [str(p.relative_to(source)) for p in source.rglob('*.so')]
        if native_files:
            raise ValueError(
                'Source admission found a pre-existing native binary: ' + name
            )
        build_inputs = git(
            source,
            'ls-files',
            'pyproject.toml',
            'setup.py',
            'Cargo.toml',
            'Cargo.lock',
            'rust',
            'rust-toolchain.toml',
        ).splitlines()
        observed[name] = {
            'source': sha,
            'tree': git(source, 'rev-parse', 'HEAD^{tree}'),
            'native_files_before_build': native_files,
            'build_input_sha256': {
                path: digest(source / path) for path in build_inputs
            },
        }
    receipt = identity(candidate)
    receipt.update(
        sources=observed,
        memory_before=memory,
        available_reserve_bytes=reserve,
        expected_build_rss_bytes=2 * 1024**3,
        process_address_space_limit=resource.getrlimit(resource.RLIMIT_AS)[0],
        logical_cpus=sorted(os.sched_getaffinity(0)),
        workers=1,
    )
    save('source-admission.json', receipt)


def providers():
    candidate = require_hosted()
    observed = {}
    prefix = Path(sys.prefix).resolve()
    admitted = json.loads((TASK / 'evidence/source-admission.json').read_text())
    if admitted['candidate'] != os.environ['CANDIDATE_SHA']:
        raise ValueError('Source admission belongs to another candidate')
    for name, sha in profile()['sources'].items():
        source = TASK / name
        if git(source, 'rev-parse', 'HEAD') != sha or git(
            source, 'status', '--porcelain', '--untracked-files=no'
        ):
            raise ValueError('Provider source identity changed: ' + name)
        dist = metadata.distribution(name)
        direct = json.loads(dist.read_text('direct_url.json'))
        if direct.get('url') != source.as_uri() or direct.get('dir_info', {}).get(
            'editable'
        ):
            raise ValueError(
                'Provider is not ordinarily installed from its source: ' + name
            )
        native = {}
        for item in dist.files or []:
            if str(item).endswith('.so'):
                path = Path(dist.locate_file(item)).resolve()
                if not path.is_relative_to(prefix):
                    raise ValueError('Native provider escaped the isolated prefix')
                native[str(path.relative_to(prefix))] = digest(path)
        built_wheels = []
        for wheel in (TASK / 'tmp').glob('pip-ephem-wheel-cache-*/wheels/**/*.whl'):
            wheel_name, wheel_version, _, _ = parse_wheel_filename(wheel.name)
            if (
                wheel_name != canonicalize_name(name)
                or str(wheel_version) != dist.version
            ):
                continue
            with zipfile.ZipFile(wheel) as archive:
                if not all(
                    Path(dist.locate_file(member)).is_file()
                    and hashlib.sha256(archive.read(member)).hexdigest()
                    == digest(dist.locate_file(member))
                    for member in archive.namelist()
                    if not member.endswith(('/', '.dist-info/RECORD'))
                ):
                    continue
            built_wheels.append(wheel)
        if len({digest(wheel) for wheel in built_wheels}) != 1:
            raise ValueError('Retain the original installed source wheel: ' + name)
        original_wheel = built_wheels[0]
        retained = TASK / 'provider-wheels' / original_wheel.name
        retained.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(original_wheel, retained)
        observed[name] = {
            'source': sha,
            'tree': git(source, 'rev-parse', 'HEAD^{tree}'),
            'version': dist.version,
            'direct_url': direct,
            'native_sha256': native,
            'pyproject_sha256': digest(source / 'pyproject.toml'),
            'wheel': original_wheel.name,
            'wheel_sha256': digest(retained),
        }
        if name == 'molsysmt':
            observed[name]['cargo_lock_path'] = 'rust/Cargo.lock'
            observed[name]['cargo_lock_sha256'] = digest(source / 'rust/Cargo.lock')
            if len(native) != 1:
                raise ValueError('Receive exactly the freshly built MolSysMT extension')
            for path, value in admitted['sources'][name]['build_input_sha256'].items():
                if digest(source / path) != value:
                    raise ValueError('Native build inputs changed: ' + path)
            observed[name]['native_linkage'] = {
                path: subprocess.check_output(['ldd', str(prefix / path)], text=True)
                for path in native
            }
            if any(
                'not found' in text
                for text in observed[name]['native_linkage'].values()
            ):
                raise ValueError(
                    'Fresh native provider has an unresolved shared library'
                )
    tools = {
        name: subprocess.check_output(
            [name, '--version'], cwd=TASK / 'molsysmt', text=True
        ).strip()
        for name in ['rustc', 'cargo', '/usr/bin/gcc']
    }
    receipt = identity(candidate)
    receipt.update(
        sources=observed,
        native_build_tools=tools,
        python_build_tools={
            name: metadata.version(name)
            for name in ['setuptools', 'setuptools-rust', 'wheel', 'versioningit']
        },
        build_route='fresh hosted checkout and ordinary no-deps directory installation',
        bitwise_native_rebuild_claim=False,
    )
    save('provider-build-receipt.json', receipt)


def bounds():
    require_hosted()
    names = ['dockingmt', *profile()['sources'], 'vina']
    for name in names:
        for text in metadata.requires(name) or []:
            req = Requirement(text)
            if req.marker and not req.marker.evaluate():
                continue
            if Version(metadata.version(req.name)) not in req.specifier:
                raise ValueError(
                    'Installed dependency requirement is unsatisfied: ' + text
                )


def snapshot():
    prefix = Path(sys.prefix).resolve()
    result = {}
    names = ['dockingmt', *profile()['sources'], 'vina']
    for name in names:
        dist = metadata.distribution(name)
        for item in dist.files or []:
            if str(item).endswith('.pyc'):
                continue
            path = Path(dist.locate_file(item)).resolve()
            if not path.is_relative_to(prefix):
                raise ValueError('Installed runtime escapes the fresh prefix')
            if path.is_file():
                result[str(path.relative_to(prefix))] = digest(path)
    return result


def admit_installed_sdk(candidate):
    sdk = TASK / 'installed-sdk'
    if git(sdk, 'rev-parse', 'HEAD') != profile()['installed_sdk'] or git(
        sdk, 'status', '--porcelain'
    ):
        raise ValueError('Use the clean pinned installed-test SDK')
    sys.path[:0] = [str(sdk), str(candidate / '.molsyssuite-tools')]


def storage(policy):
    """Repeat the unchanged ten-case explicit-1.0 client program on fresh bytes."""
    candidate = require_hosted()
    admit_installed_sdk(candidate)
    import pytest
    from devtools.scripts.installed_imports import check_installed_imports
    from devtools.scripts.installed_test_support import staged_support
    from pytest_receptor import read_artifact

    evidence = TASK / 'evidence' / ('storage-' + policy)
    evidence.mkdir(exist_ok=False)
    inventory = tomllib.loads(
        (candidate / 'devtools/conda-build/resources.toml').read_text()
    )
    receipt = identity(candidate)
    before = snapshot()
    native_path = Path(
        metadata.distribution('molsysmt').locate_file('molsysmt/_rust.abi3.so')
    ).resolve()
    builds = json.loads((TASK / 'evidence/provider-build-receipt.json').read_text())
    if (
        digest(native_path)
        not in builds['sources']['molsysmt']['native_sha256'].values()
    ):
        raise ValueError(
            'Storage receiver must load the freshly authenticated extension'
        )
    forbidden = []

    class BlockOptional(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.split('.')[0] in {'vina', 'rdkit', 'openmm', 'ackredit'}:
                forbidden.append(fullname)
                raise AssertionError(
                    'Storage client attempted optional work: ' + fullname
                )

    sys.meta_path.insert(0, BlockOptional())
    spec = importlib.util.spec_from_file_location('molsysmt._rust', native_path)
    native = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = native
    spec.loader.exec_module(native)
    operation = native.get_component_index_from_bonded_atom_pairs

    def reject(*args, **kwargs):
        forbidden.append('unregistered native/viewer/preparation operation')
        raise AssertionError(forbidden[-1])

    for name in dir(native):
        if not name.startswith('_') and callable(getattr(native, name)):
            setattr(native, name, reject)
    native_calls = []

    def component_indices(pairs, count):
        assert count == 1 and pairs.shape == (0, 2) and str(pairs.dtype) == 'int64'
        assert len(native_calls) < 2
        result = operation(pairs, count)
        assert result.tolist() == [0]
        native_calls.append(
            {'n_atoms': int(count), 'pairs': pairs.tolist(), 'result': result.tolist()}
        )
        return result

    native.get_component_index_from_bonded_atom_pairs = component_indices
    import pyunitwizard as puw

    units = (
        ['nm', 'ps', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
        if policy == 'normal'
        else ['pm', 'fs', 'K', 'mole', 'dalton', 'coulomb', 'J/mol', 'radians']
    )
    roots = ('dockingmt', 'molsysviewer_dockingmt', *profile()['sources'])
    with puw.context(default_form='pint', default_parser='pint', standard_units=units):
        caller = puw.configure.report()
        import molsysmt as msm
        import molsysviewer as viewer

        import dockingmt as dmt

        assert dmt.__version__ == VERSION
        viewer.MolSysView = reject
        for name in [
            'assign_partial_charges',
            'assign_autodock_atom_types',
            'add_missing_hydrogens',
            'merge_nonpolar_hydrogens',
        ]:
            setattr(msm.build, name, reject)
        declaration = inventory['installed_tests']['support']
        binding = {
            'candidate_sha': os.environ['CANDIDATE_SHA'],
            'provider_sha': profile()['installed_sdk'],
            'sha256': os.environ['EXPECTED_WHEEL_SHA256'],
        }
        with staged_support(candidate, declaration, roots, context=binding) as stage:
            import dmt_test_support.h5msm_client_oracle as oracle

            data = stage.root / 'tests/data/h5msm_client'
            primary = json.loads((data / 'primary-manifest.json').read_text())
            if (
                digest(data / 'primary-manifest.json')
                != '73e8d385c763ebf4c85bcb86099b3785a69445c57c0ff3b30ec44283c8bf22fe'
            ):
                raise ValueError('Original P6 source manifest changed')
            rows = {row['original_path']: row for row in primary['files']}
            original = ast.parse(
                gzip.decompress((data / 'original-oracle.py.gz').read_bytes())
            )
            current = ast.parse(Path(oracle.__file__).read_bytes())
            for kind in [(ast.FunctionDef,), (ast.Import, ast.ImportFrom)]:
                assert {
                    ast.dump(n, include_attributes=False)
                    for n in original.body
                    if isinstance(n, kind)
                } == {
                    ast.dump(n, include_attributes=False)
                    for n in current.body
                    if isinstance(n, kind)
                }
            packet = evidence / 'packet'
            packet.mkdir()
            for source in sorted((data / 'packet').glob('*.gz')):
                raw = gzip.decompress(source.read_bytes())
                name = source.name.removesuffix('.gz')
                assert (
                    hashlib.sha256(raw).hexdigest()
                    == rows['packet/' + name]['decoded_sha256']
                )
                (packet / name).write_bytes(raw)
            assert len(list(packet.iterdir())) == 11
            program = gzip.decompress((data / 'client_cases.py.gz').read_bytes())
            assert (
                hashlib.sha256(program).hexdigest()
                == rows['producer/client_cases.py.txt']['decoded_sha256']
            )
            test_file = evidence / 'test_original_p6_client.py'
            test_file.write_bytes(program)
            output = evidence / 'outputs'
            output.mkdir()
            context = types.ModuleType('p6_case_context')
            context.msm, context.puw, context.oracle = msm, puw, oracle
            context.packet, context.output, context.sha = packet, output, digest
            context.save = lambda path, value: path.write_text(
                json.dumps(value, indent=2, allow_nan=False) + '\n'
            )
            sys.modules[context.__name__] = context
            selected = []

            class Collection:
                @pytest.hookimpl(trylast=True)
                def pytest_collection_finish(self, session):
                    selected.extend(item.nodeid for item in session.items)
                    assert len(selected) == 10

            status = int(
                pytest.main(
                    [
                        '--receptor=ci',
                        '--receptor-events=' + str(evidence / 'events.jsonl'),
                        '--junitxml=' + str(evidence / 'tests.xml'),
                        '--import-mode=importlib',
                        '-o',
                        'pythonpath=',
                        '-o',
                        'cache_dir=' + str(evidence / 'pytest-cache'),
                        '--basetemp=' + str(evidence / 'pytest-work'),
                        str(test_file),
                    ],
                    plugins=[Collection()],
                )
            )
            for key in ['default_form', 'default_parser', 'standard_units']:
                assert caller[key] == puw.configure.report()[key]
            stage.check()
        events = read_artifact(evidence / 'events.jsonl')
        receipt.update(
            profile=policy,
            pytest_exit=status,
            nodes=selected,
            receptor_final=events.final.data if events.complete else None,
            native_sha256=digest(native_path),
            native_calls=native_calls,
            support=stage.receipt,
            forbidden_operations=forbidden,
            installed_origins=check_installed_imports(
                roots, Path(sys.prefix), candidate
            ),
            caller_policy=caller,
            completed_gate=False,
        )
        if status or not events.complete or events.final.data['counts']['passed'] != 10:
            save('storage-' + policy + '/receipt.json', receipt)
            raise ValueError('Original complete storage client selection did not pass')
        if (
            events.final.data['counts']['skipped']
            or len(native_calls) != 2
            or forbidden
            or before != snapshot()
        ):
            raise ValueError('Storage profile identity/native/input controls failed')
        assert stage.receipt['resources_retired'] and stage.receipt['imports_retired']
        receipt['completed_gate'] = True
        save('storage-' + policy + '/receipt.json', receipt)


def receive():
    candidate = require_hosted()
    minor = f'{sys.version_info.major}.{sys.version_info.minor}'
    if (
        minor not in profile()['python_minors']
        or minor != os.environ['EXPECTED_PYTHON']
    ):
        raise ValueError('Wrong Python minor for this declared cell')
    if not sys.flags.isolated or Path.cwd().resolve().is_relative_to(ROOT):
        raise ValueError('Use isolated Python outside qualification/source roots')
    admit_installed_sdk(candidate)
    wheel = TASK / 'wheels/dockingmt-0.1.0-py3-none-any.whl'
    if digest(wheel) != os.environ['EXPECTED_WHEEL_SHA256']:
        raise ValueError('Installed qualification must consume the same-run wheel')
    build_receipt = json.loads((TASK / 'evidence/build-receipt.json').read_text())
    if build_receipt['candidate'] != os.environ['CANDIDATE_SHA']:
        raise ValueError('Wheel producer belongs to another candidate')
    for name, value in build_receipt['contract']['source_input_sha256'].items():
        if digest(candidate / name) != value:
            raise ValueError('Candidate source inputs differ from the build: ' + name)
    runtime = check_wheel(wheel, build_receipt['contract'])
    dist = metadata.distribution('dockingmt')
    direct = json.loads(dist.read_text('direct_url.json'))
    if dist.version != VERSION or direct.get('archive_info', {}).get('hashes', {}).get(
        'sha256'
    ) != digest(wheel):
        raise ValueError('Consumer is not the ordinarily installed versioned wheel')
    for name, value in runtime.items():
        if digest(dist.locate_file(name)) != value:
            raise ValueError('Installed wheel payload changed: ' + name)
    for namespace in ['dockingmt', 'molsysviewer_dockingmt']:
        shutil.rmtree(candidate / namespace)
    from devtools.scripts.installed_imports import check_installed_imports
    from devtools.scripts.installed_noarch import run_tests

    import dockingmt as dmt

    addon = importlib.import_module('molsysviewer_dockingmt.addon')
    import pytest
    from pytest_receptor import read_artifact

    if dmt.__version__ != VERSION or addon.addon.version != VERSION:
        raise ValueError('Actual consumer/addon version attribution differs')
    for name in profile()['sources']:
        importlib.import_module(name)
    roots = ('dockingmt', 'molsysviewer_dockingmt', *profile()['sources'], 'vina')
    origins = check_installed_imports(roots, Path(sys.prefix), candidate)
    before = snapshot()
    selected = []
    deselected = []

    class Collection:
        def pytest_deselected(self, items):
            deselected.extend(item.nodeid for item in items)

        @pytest.hookimpl(trylast=True)
        def pytest_collection_finish(self, session):
            selected.extend(item.nodeid for item in session.items)
            save('collection.json', {'selected': selected, 'deselected': deselected})
            if not selected or deselected:
                raise ValueError('Require the complete original candidate selection')

    original_main = pytest.main

    def observed_main(*args, **kwargs):
        kwargs['plugins'] = [*kwargs.get('plugins', []), Collection()]
        return original_main(*args, **kwargs)

    pytest.main = observed_main
    inventory = tomllib.loads(
        (candidate / 'devtools/conda-build/resources.toml').read_text()
    )
    inventory['import_name'] = 'dockingmt'
    evidence = TASK / 'evidence'
    inventory['installed_tests']['pytest_args'] += [
        '--receptor=ci',
        '--receptor-events=' + str(evidence / 'events.jsonl'),
        '--junitxml=' + str(evidence / 'installed-tests.xml'),
        '--basetemp=' + str(TASK / 'pytest-scratch'),
    ]
    receipt = identity(candidate)
    receipt.update(
        wheel_sha256=digest(wheel),
        installed_origins_before=origins,
        runtime_sha256_before=before,
        completed_gate=False,
        support_rows=len(inventory['installed_tests']['support']['files']),
    )
    try:
        status = int(
            run_tests(
                candidate,
                inventory,
                support_output=evidence / 'support.json',
                support_context={
                    'candidate_sha': os.environ['CANDIDATE_SHA'],
                    'qualification_sha': os.environ['GITHUB_SHA'],
                    'provider_sha': profile()['installed_sdk'],
                    'sha256': digest(wheel),
                },
            )
        )
        receipt['pytest_exit'] = status
        events = read_artifact(evidence / 'events.jsonl')
        receipt['receptor_final'] = events.final.data if events.complete else None
        receipt['runtime_sha256_after'] = snapshot()
        receipt['installed_origins_after'] = check_installed_imports(
            roots, Path(sys.prefix), candidate
        )
        if before != receipt['runtime_sha256_after']:
            raise ValueError('Installed runtime bytes changed during qualification')
        counts = {
            k: sum(
                int(row.get(k, 0))
                for row in ET.parse(evidence / 'installed-tests.xml')
                .getroot()
                .iter('testsuite')
            )
            for k in ['tests', 'failures', 'errors', 'skipped']
        }
        receipt['junit'] = counts
        support = json.loads((evidence / 'support.json').read_text())
        if (
            status
            or not events.complete
            or any(counts[k] for k in ['failures', 'errors', 'skipped'])
        ):
            raise ValueError('Complete candidate installed selection did not pass')
        if events.final.data['counts']['executed'] != len(selected) or deselected:
            raise ValueError('Collection and executed test identities differ')
        if not support['resources_retired'] or not support['imports_retired']:
            raise ValueError('Installed support was not retired')
        subprocess.run([sys.executable, '-m', 'pip', 'check'], check=True)
        receipt['completed_gate'] = True
        return status
    finally:
        pytest.main = original_main
        save('installed-receipt.json', receipt)


def main():
    stages = {
        'build': build,
        'sources': sources,
        'providers': providers,
        'bounds': bounds,
        'storage-normal': lambda: storage('normal'),
        'storage-pm-fs': lambda: storage('pm_fs'),
        'receive': receive,
    }
    if len(sys.argv) != 2 or sys.argv[1] not in stages:
        raise SystemExit('Select build, sources, providers, bounds or receive')
    result = stages[sys.argv[1]]()
    return 0 if result is None else result


if __name__ == '__main__':
    raise SystemExit(main())
