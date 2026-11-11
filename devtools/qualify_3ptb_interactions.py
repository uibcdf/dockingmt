"""Hosted-only receiver for #80's finite 3PTB notebook, never a molecular tool.

The notebook owns this case's composition of public MolSysMT operations. This
caller binds its inputs, installed bytes, budgets and independent saved reader.
The local resource hold is preserved: computational entry points reject local use.
"""

from __future__ import annotations

import argparse
import configparser
import gzip
import hashlib
import importlib.metadata as metadata
import importlib.util
import json
import os
import platform
import re
import shutil
import signal
import subprocess
import sys
import time
import tomllib
import zipfile
from contextlib import nullcontext
from email.parser import BytesParser
from functools import wraps
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    'notebook': (
        'devguide/validation/installed_3ptb_interactions.ipynb',
        '6c43428ea9053dde56039828e16cfb14884a65fc91d9b76eb1e8455000336c01',
    ),
    'preparation': (
        'devguide/validation/installed_3ptb_preparation.ipynb',
        'c6c5a6660b8b5d46df01cde6960129a7bc65db81d551b3ad0a4d763fc0907da9',
    ),
    'source': (
        'devguide/validation/data/3ptb_prospective/3PTB.pdb.gz',
        '75b1b8e73b4c197b7dcb217fbcfdd39c451860c0fd5a86cdef587c4dbd9972be',
    ),
    'declarations': (
        'devguide/validation/data/human_3ptb/admission_2026-10-20.json.gz',
        '79e9283236ebbb645cd75d7c3341d457a8078361466b7a26458c814d8041cd53',
    ),
    'result': (
        'devguide/validation/data/human_3ptb/native_result_2026-10-20.json.gz',
        '4b1f51cdeb135fd6785a181f6bb09a0d0f631ec3d9de7c169c88703748924249',
    ),
}
PROFILES = ('normal', 'pm_fs')
EXPECTED_CALLS = {
    ('retained_pose', 'hbonds'),
    ('retained_pose', 'hydrophobic'),
    ('translated_geometry_control', 'hbonds'),
    ('translated_geometry_control', 'hydrophobic'),
    ('analytic_positive', 'hbonds'),
    ('analytic_adverse', 'hbonds'),
}
FILES = {
    name + '.h5msm'
    for name in (
        'retained_pose',
        'translated_geometry_control',
        'analytic_positive',
        'analytic_adverse',
    )
}
ORIGINAL_RESULT_SHA = 'ed0eeb3ade25e54f8a5829729578fcbec9f0d73d6c0ceb03d146b0c3492d7fac'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    def invalid(value):
        raise ValueError('Nonfinite JSON: ' + value)

    return json.loads(Path(path).read_text(), parse_constant=invalid)


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def hosted():
    if (
        os.environ.get('GITHUB_ACTIONS') != 'true'
        or os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted'
    ):
        raise ValueError('E4 computation is permitted only on GitHub-hosted runners')
    expected = os.environ.get('EXPECTED_SOURCE_SHA', '')
    head = subprocess.check_output(
        ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
    ).strip()
    if (
        not re.fullmatch('[0-9a-f]{40}', expected)
        or expected != os.environ.get('GITHUB_SHA')
        or expected != head
    ):
        raise ValueError('Dispatch, checked-out and expected source must be identical')
    if sys.platform != 'linux' or platform.machine() != 'x86_64':
        raise ValueError('Only the registered Linux x86_64 profile is selected')
    return expected


def task():
    return Path(os.environ['RUNNER_TEMP']).resolve() / 'bindingmt-e4'


def staged_inputs():
    registration = read_json(task() / 'registration.json')
    if registration['source'] != os.environ['GITHUB_SHA'] or registration[
        'inputs'
    ] != verify_inputs(ROOT):
        raise ValueError('Staged registration differs from the exact source')
    for row in registration['inputs'].values():
        if digest(task() / 'inputs' / row['filename']) != row['sha256']:
            raise ValueError('Staged input bytes changed')
    return registration


def verify_inputs(root):
    records = {}
    for name, (relative, expected) in INPUTS.items():
        path = root / relative
        if digest(path) != expected:
            raise ValueError('Registered E4 input changed: ' + name)
        records[name] = {
            'repository_path': relative,
            'sha256': expected,
            'filename': path.name,
        }
    return records


def stage():
    source = hosted()
    records = verify_inputs(ROOT)
    directory = task()
    directory.mkdir(exist_ok=False)
    (directory / 'inputs').mkdir()
    for row in records.values():
        shutil.copyfile(
            ROOT / row['repository_path'], directory / 'inputs' / row['filename']
        )
    save(
        directory / 'registration.json',
        {
            'source': source,
            'run_id': os.environ['GITHUB_RUN_ID'],
            'run_attempt': os.environ['GITHUB_RUN_ATTEMPT'],
            'inputs': records,
            'profiles': list(PROFILES),
            'maximum_detector_calls': 12,
            'prior_local_interrupted_counter_budget': 'unknown; reserve its full six calls separately',
            'maximum_cumulative_local_unknown_plus_hosted_calls': 18,
            'retries': 0,
            'new_searches_or_energy_calls': 0,
            'logical_cpus': 1,
            'native_workers': 1,
            'hosted_RAM_reserve_bytes': 1024**3,
            'profile_timeout_seconds': 300,
            'reader_timeout_seconds': 120,
            'review': '2026-11-13',
            'local_resource_hold_preserved': True,
            'public_release_or_package': False,
        },
    )


def wheel_contract(wheel, root):
    inventory = tomllib.loads(
        (root / 'devtools/conda-build/resources.toml').read_text()
    )
    required = {p.removeprefix('site-packages/') for p in inventory['required_paths']}
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive member')
        runtime = {
            n: hashlib.sha256(archive.read(n)).hexdigest()
            for n in names
            if not n.endswith('/') and '.dist-info/' not in n
        }
        if set(runtime) != required:
            raise ValueError(
                'Consumer payload differs from the declared BindingMT inventory'
            )
        for name, value in runtime.items():
            if name != 'bindingmt/_version.py' and digest(root / name) != value:
                raise ValueError('Consumer bytes differ from source: ' + name)
        meta_names = [n for n in names if n.endswith('.dist-info/METADATA')]
        if len(meta_names) != 1:
            raise ValueError('One distribution is required')
        prefix = meta_names[0].removesuffix('METADATA')
        message = BytesParser().parsebytes(archive.read(meta_names[0]))
        if message['Name'] != 'bindingmt' or message['License-Expression'] != 'MIT':
            raise ValueError('Wrong BindingMT metadata')
        from packaging.specifiers import SpecifierSet

        if SpecifierSet(message['Requires-Python']) != SpecifierSet('>=3.11,<3.15'):
            raise ValueError('Wrong supported Python range')
        headers = BytesParser().parsebytes(archive.read(prefix + 'WHEEL'))
        if headers['Root-Is-Purelib'] != 'true' or headers.get_all('Tag') != [
            'py3-none-any'
        ]:
            raise ValueError('Unexpected BindingMT platform tag')
        entries = configparser.ConfigParser()
        entries.read_string(archive.read(prefix + 'entry_points.txt').decode())
        if entries['molsysviewer.addons']['bindingmt'] != 'molsysviewer_bindingmt':
            raise ValueError('Wrong addon entry point')
        if archive.read(prefix + 'licenses/LICENSE') != (root / 'LICENSE').read_bytes():
            raise ValueError('License bytes differ')
    return {
        'runtime_sha256': runtime,
        'version': message['Version'],
        'sha256': digest(wheel),
        'filename': wheel.name,
    }


def build():
    source = hosted()
    staged_inputs()
    wheels = task() / 'wheels'
    subprocess.run(
        [
            sys.executable,
            '-m',
            'pip',
            'wheel',
            '--no-deps',
            '--wheel-dir',
            str(wheels),
            str(ROOT),
        ],
        check=True,
    )
    found = list(wheels.glob('*.whl'))
    if len(found) != 1:
        raise ValueError('Exactly one consumer archive is required')
    proof = wheel_contract(found[0], ROOT)
    proof['source'] = source
    save(task() / 'build.json', proof)
    subprocess.run(
        [
            sys.executable,
            '-m',
            'pip',
            'install',
            '--no-index',
            '--no-deps',
            '--no-compile',
            str(found[0]),
        ],
        check=True,
    )
    verify_consumer()


def verify_consumer():
    proof = read_json(task() / 'build.json')
    if (
        proof['source'] != os.environ['GITHUB_SHA']
        or digest(task() / 'wheels' / proof['filename']) != proof['sha256']
    ):
        raise ValueError('Wrong source/archive binding')
    dist = metadata.distribution('bindingmt')
    direct = json.loads(dist.read_text('direct_url.json') or '{}')
    if (
        dist.version != proof['version']
        or direct.get('archive_info', {}).get('hashes', {}).get('sha256')
        != proof['sha256']
    ):
        raise ValueError('Installed consumer is not the exact same-run archive')
    for name, expected in proof['runtime_sha256'].items():
        if digest(dist.locate_file(name)) != expected:
            raise ValueError('Installed consumer payload changed: ' + name)
    return proof


def artifact_monitor():
    # Reuse the existing member's qualified source-provider snapshot; no copied
    # generic snapshot implementation or scientific package path is introduced.
    path = ROOT / 'devtools/qualify_source_0_1_0.py'
    spec = importlib.util.spec_from_file_location(
        '_dmt_existing_artifact_monitor', path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.snapshot


def validate_association(association, original, registration, journal):
    if association.get('schema') != 'bindingmt.3ptb_interaction_association@1':
        raise ValueError('Wrong association schema')
    expected = {
        name: registration['inputs'][name]['sha256']
        for name in ('preparation', 'result')
    }
    pose = original['poses'][0]
    if (
        association.get('inputs') != expected
        or type(association.get('selected_original_position')) is not int
        or association.get('selected_original_position') != 1
    ):
        raise ValueError('Wrong original input/position association')
    producer = {
        key: original['provenance'][key]
        for key in (
            'bindingmt_version',
            'molsysmt_version',
            'backend',
            'backend_version',
        )
    }
    if (
        association.get('original_decoded_result_sha256') != ORIGINAL_RESULT_SHA
        or association.get('original_producer') != producer
    ):
        raise ValueError('Wrong original producer/result association')
    for name in ('pose_id', 'partner_state_id', 'receptor_state_id'):
        if association.get(name) != pose[name]:
            raise ValueError('Wrong original pose identity: ' + name)
    expected_coords = hashlib.sha256(
        json.dumps(
            pose['coordinates'], sort_keys=True, separators=(',', ':'), allow_nan=False
        ).encode()
    ).hexdigest()
    if (
        association.get('pose_coordinates_sha256') != expected_coords
        or association.get('original_scores') != pose['scores']
    ):
        raise ValueError('Original coordinates or scores disagree')
    if (
        set(association.get('files', {})) != FILES
        or type(association.get('interaction_detector_calls')) is not int
        or association.get('interaction_detector_calls') != 6
    ):
        raise ValueError('Incomplete provider files or detector denominator')
    analyses = association.get('analyses')
    if (
        not isinstance(analyses, dict)
        or set(analyses) != {'retained_pose', 'translated_geometry_control'}
        or any(
            not isinstance(counts, dict)
            or set(counts) != {'hbonds', 'hydrophobic'}
            or any(type(n) is not int or n < 0 for n in counts.values())
            for counts in analyses.values()
        )
        or any(analyses['translated_geometry_control'].values())
        or association.get('analytic_controls')
        != {'analytic_positive': 1, 'analytic_adverse': 0}
        or any(type(n) is not int for n in association['analytic_controls'].values())
    ):
        raise ValueError('Incomplete observation populations or invalid controls')
    for status in ('started', 'completed'):
        rows = [
            r
            for r in journal
            if r.get('stage') == 'detector' and r.get('status') == status
        ]
        if (
            len(rows) != 6
            or {(r.get('case'), r.get('family')) for r in rows} != EXPECTED_CALLS
        ):
            raise ValueError('Incomplete/duplicate detector evidence: ' + status)
    if (
        not journal
        or any(r.get('status') == 'failed' for r in journal)
        or journal[-1] != {'stage': 'workflow', 'status': 'completed'}
    ):
        raise ValueError('Workflow did not complete')
    mapping = association.get('existing_ligand_atom_correspondence')
    if (
        not isinstance(mapping, list)
        or len(mapping) != 13
        or any(
            not isinstance(p, list) or len(p) != 2 or any(type(i) is not int for i in p)
            for p in mapping
        )
    ):
        raise ValueError('Missing explicit provider atom correspondence')
    if (
        [p[0] for p in mapping] != list(range(13))
        or len({p[1] for p in mapping}) != 13
        or any(not 0 <= p[1] < 18 for p in mapping)
    ):
        raise ValueError('Invalid provider atom correspondence')
    for indices in association.get('merged_ligand_atom_indices', {}).values():
        if (
            not isinstance(indices, list)
            or len(indices) != 18
            or any(type(i) is not int or i < 0 for i in indices)
            or len(set(indices)) != 18
        ):
            raise ValueError('Invalid merged ligand axis')
    if set(association.get('merged_ligand_atom_indices', {})) != {
        'retained_pose',
        'translated_geometry_control',
    }:
        raise ValueError('Missing merged-model atom axes')


def scientific_process(profile, reader=False):
    hosted()
    staged_inputs()
    if (
        sys.version_info[:2] != (3, 14)
        or not sys.flags.isolated
        or Path.cwd().resolve().is_relative_to(ROOT)
    ):
        raise ValueError('Use isolated installed Python 3.14 outside source')
    proof = verify_consumer()
    import molsysmt as msm
    import numpy as np
    import pyunitwizard as puw
    import vina
    from IPython.core.interactiveshell import InteractiveShell

    import bindingmt as bmt

    for module in (bmt, msm, puw, vina):
        if (
            not Path(module.__file__)
            .resolve()
            .is_relative_to(Path(sys.prefix).resolve())
        ):
            raise ValueError('Scientific import escaped the installed prefix')
    snapshot = artifact_monitor()
    before = snapshot()
    directory = task() / profile
    state = {
        'profile': profile,
        'reader': reader,
        'source': os.environ['GITHUB_SHA'],
        'consumer': proof,
        'calls': {},
        'forbidden_calls': {},
        'completed_gate': False,
        'python': platform.python_version(),
    }
    receipt_path = directory / ('reader.json' if reader else 'observer.json')

    def checkpoint():
        save(receipt_path, state)

    def forbid(owner, attribute, label):
        if not hasattr(owner, attribute):
            return
        state['forbidden_calls'][label] = 0

        def deny(*args, **kwargs):
            state['forbidden_calls'][label] += 1
            checkpoint()
            raise AssertionError('Outside registered E4 scope: ' + label)

        setattr(owner, attribute, deny)

    def observe(owner, attribute, label):
        original = getattr(owner, attribute)
        state['calls'][label] = {'attempted': 0, 'completed': 0}

        @wraps(original)
        def call(*args, **kwargs):
            if sum(r['attempted'] for r in state['calls'].values()) >= 6:
                raise AssertionError('Registered detector budget exhausted')
            state['calls'][label]['attempted'] += 1
            checkpoint()
            result = original(*args, **kwargs)
            state['calls'][label]['completed'] += 1
            checkpoint()
            return result

        setattr(owner, attribute, call)

    for name in ('dock', 'score', 'evaluate_redocking', 'view', 'show'):
        forbid(bmt, name, 'bindingmt.' + name)
    for name in (
        '__init__',
        'compute_vina_maps',
        'dock',
        'score',
        'optimize',
        'write_poses',
    ):
        forbid(vina.Vina, name, 'Vina.' + name)
    for name in ('view', 'show'):
        forbid(msm, name, 'molsysmt.' + name)
    if reader:
        for name in ('prepare_receptor', 'prepare_ligand'):
            forbid(bmt, name, 'bindingmt.' + name)
        forbid(msm.build, 'add_missing_hydrogens', 'fixed_state_H')
        forbid(msm.interactions.hbonds, 'get_hbonds', 'hbonds')
        forbid(
            msm.interactions.hydrophobic, 'get_hydrophobic_interactions', 'hydrophobic'
        )
    else:
        observe(msm.interactions.hbonds, 'get_hbonds', 'hbonds')
        observe(
            msm.interactions.hydrophobic, 'get_hydrophobic_interactions', 'hydrophobic'
        )
    checkpoint()
    try:
        with (
            puw.context(standard_units=['pm', 'fs'])
            if profile == 'pm_fs'
            else nullcontext()
        ):
            caller = puw.configure.report()
            if reader:
                read_saved(profile, msm, np, puw)
            else:
                shell = InteractiveShell.instance()
                shell.run_line_magic(
                    'run', str(task() / 'inputs' / Path(INPUTS['notebook'][0]).name)
                )
                if 'interaction_association' not in shell.user_ns:
                    raise ValueError('Notebook did not finish')
                if {n: r['completed'] for n, r in state['calls'].items()} != {
                    'hbonds': 4,
                    'hydrophobic': 2,
                }:
                    raise ValueError(
                        'The six registered detector calls did not complete'
                    )
            if caller != puw.configure.report() or any(
                state['forbidden_calls'].values()
            ):
                raise ValueError('Unit policy changed or forbidden work was attempted')
            state['unit_policy_preserved'] = True
        state['completed_gate'] = True
    finally:
        after = snapshot()
        state['runtime_payloads_preserved'] = before == after
        state['runtime_sha256_before'] = before
        state['runtime_sha256_after'] = after
        if before != after:
            state['completed_gate'] = False
            checkpoint()
            raise ValueError('Installed source-provider/consumer bytes changed')
        try:
            verify_consumer()
            staged_inputs()
        except Exception:
            state['completed_gate'] = False
            checkpoint()
            raise
        checkpoint()


def read_saved(profile, msm, np, puw):
    directory = task() / profile / 'interactions'
    association = read_json(directory / 'association.json')
    registration = staged_inputs()
    original = json.loads(
        gzip.decompress(
            (
                task() / 'inputs' / registration['inputs']['result']['filename']
            ).read_bytes()
        )
    )
    journal = [
        json.loads(row)
        for row in (directory / 'progress.jsonl').read_text().splitlines()
    ]
    validate_association(association, original, registration, journal)
    for filename, info in association['files'].items():
        path = directory / filename
        if (
            path.is_symlink()
            or not path.is_file()
            or digest(path) != info['sha256']
            or path.stat().st_size != info['bytes']
        ):
            raise ValueError('Saved provider file identity differs')
        model = msm.convert(path, to_form='molsysmt.MolSys')
        case = filename.removesuffix('.h5msm')
        expected = (
            association['analyses'][case]
            if case in association['analyses']
            else {'hbonds': association['analytic_controls'][case]}
        )
        if set(model.interactions) != set(expected):
            raise ValueError('Saved analysis inventory differs')
        for family, count in expected.items():
            analysis = model.interactions[family]
            if (
                analysis.n_interactions != count
                or analysis.evaluated_structure_indices.tolist() != [0]
            ):
                raise ValueError('Observation count or evaluated coverage differs')
            method, site_definition = (
                ('baker_hubbard', 'elemental_nitrogen_oxygen')
                if family == 'hbonds'
                else ('atom_pair_distance', 'smarts_hydrophobic_atoms')
            )
            if (
                analysis.parameters.get('method') != method
                or analysis.parameters.get('site_definition') != site_definition
                or analysis.parameters.get('pbc') is not False
            ):
                raise ValueError('Saved scientific method/profile/PBC differs')
        if case == 'analytic_positive':
            analysis = model.interactions['hbonds']
            for name, unit, value in [
                ('hydrogen_acceptor_distance', 'nm', 0.18),
                ('dha_angle', 'radian', 3.141592653589793),
            ]:
                quantity = puw.quantity(
                    analysis.measurements[name], analysis.measure_units[name]
                )
                np.testing.assert_allclose(
                    puw.get_value(quantity, to_unit=unit), value, rtol=0, atol=1e-12
                )
        if case in association['analyses']:
            ligand_indices = association['merged_ligand_atom_indices'][case]
            receptor_indices = msm.select(model, selection="molecule_type=='protein'")
            for family, count in expected.items():
                selected_analysis = model.interactions[family].between_selections(
                    ligand_indices, receptor_indices, exclusive=True
                )
                if selected_analysis.n_interactions != count:
                    raise ValueError('Saved ligand/receptor filtering differs')
        if case == 'retained_pose':
            indices = association['merged_ligand_atom_indices'][case]
            selected = [
                indices[pair[1]]
                for pair in association['existing_ligand_atom_correspondence']
            ]
            expected_pose = original['poses'][0]
            for key, attribute in {
                'atom_id': 'atom_id',
                'atom_name': 'atom_name',
                'element': 'atom_type',
                'group_id': 'group_id',
                'group_name': 'group_name',
            }.items():
                actual = [
                    str(v)
                    for v in msm.get(
                        model, selection=selected, element='atom', **{attribute: True}
                    )
                ]
                if actual != [
                    v[key] for v in expected_pose['metadata']['source_atom_keys']
                ]:
                    raise ValueError('Saved pose atom association differs')
            actual = puw.get_value(
                msm.get(model, selection=selected, coordinates=True), to_unit='angstrom'
            )[0]
            expected_coords = puw.get_value(
                puw.quantity(
                    expected_pose['coordinates']['value'],
                    expected_pose['coordinates']['unit'],
                ),
                to_unit='angstrom',
            )
            np.testing.assert_allclose(actual, expected_coords, rtol=0, atol=1e-12)


def receive():
    hosted()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    os.nice(15)
    registration = staged_inputs()
    outcomes = []

    def available():
        return (
            int(
                next(
                    line
                    for line in Path('/proc/meminfo').read_text().splitlines()
                    if line.startswith('MemAvailable:')
                ).split()[1]
            )
            * 1024
        )

    try:
        for profile in PROFILES:
            directory = task() / profile
            directory.mkdir(exist_ok=False)
            env = dict(
                os.environ,
                PYTHONDONTWRITEBYTECODE='1',
                IPYTHONDIR=str(directory / 'ipython'),
                MPLCONFIGDIR=str(directory / 'matplotlib'),
                XDG_CACHE_HOME=str(directory / 'cache'),
            )
            inputs = registration['inputs']
            for role, variable in {
                'source': 'BINDINGMT_3PTB_SOURCE',
                'declarations': 'BINDINGMT_3PTB_DECLARATIONS',
                'result': 'BINDINGMT_INTERACTIONS_RESULT',
                'preparation': 'BINDINGMT_INTERACTIONS_PREPARATION_NOTEBOOK',
            }.items():
                env[variable] = str(task() / 'inputs' / inputs[role]['filename'])
                env[variable + '_SHA256'] = inputs[role]['sha256']
            env['BINDINGMT_3PTB_OUTPUT'] = str(directory / 'preparation')
            env['BINDINGMT_INTERACTIONS_OUTPUT'] = str(directory / 'interactions')
            for operation, timeout in [('profile', 300), ('read', 120)]:
                if available() < registration['hosted_RAM_reserve_bytes']:
                    raise ValueError('Hosted reserve unavailable; no automatic retry')
                start = time.monotonic()
                row = {'profile': profile, 'operation': operation, 'status': 'started'}
                outcomes.append(row)
                save(task() / 'outcomes.json', outcomes)
                with (directory / (operation + '.log')).open('w') as log:
                    child = subprocess.Popen(
                        [
                            sys.executable,
                            '-I',
                            '-B',
                            str(Path(__file__).resolve()),
                            operation,
                            '--profile',
                            profile,
                        ],
                        cwd=directory,
                        env=env,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        start_new_session=True,
                    )
                    stop = None
                    while child.poll() is None:
                        if available() < registration['hosted_RAM_reserve_bytes']:
                            stop = 'hosted RAM reserve threatened'
                        if time.monotonic() - start > timeout:
                            stop = 'registered operation timeout'
                        if (
                            sum(
                                p.stat().st_size
                                for p in directory.rglob('*')
                                if p.is_file()
                            )
                            > 64 * 1024**2
                        ):
                            stop = 'owned output budget exceeded'
                        if stop:
                            os.killpg(child.pid, signal.SIGTERM)
                            try:
                                child.wait(timeout=5)
                            except subprocess.TimeoutExpired:
                                os.killpg(child.pid, signal.SIGKILL)
                                child.wait(timeout=5)
                            break
                        time.sleep(0.2)
                row.update(
                    returncode=child.returncode,
                    seconds=time.monotonic() - start,
                    resource_stop=stop,
                    status='completed'
                    if child.returncode == 0 and not stop
                    else 'failed',
                )
                save(task() / 'outcomes.json', outcomes)
                if row['status'] != 'completed':
                    raise ValueError(
                        'E4 operation failed; retain evidence without retry'
                    )
    finally:
        closure = subprocess.run([sys.executable, '-m', 'pip', 'check']).returncode
        save(
            task() / 'receiving.json',
            {
                'source': os.environ['GITHUB_SHA'],
                'outcomes': outcomes,
                'pip_check_after': closure,
                'completed_gate': closure == 0
                and len(outcomes) == 4
                and all(row['status'] == 'completed' for row in outcomes),
                'public_package_or_scientific_panel_or_live_visual_acceptance': False,
            },
        )
        if closure:
            raise ValueError('Installed Python dependency closure failed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'operation', choices=('stage', 'build', 'receive', 'profile', 'read')
    )
    parser.add_argument('--profile', choices=PROFILES)
    args = parser.parse_args()
    if args.operation in ('profile', 'read'):
        if not args.profile:
            raise ValueError('A registered profile is required')
        return scientific_process(args.profile, args.operation == 'read')
    return {'stage': stage, 'build': build, 'receive': receive}[args.operation]()


if __name__ == '__main__':
    main()
