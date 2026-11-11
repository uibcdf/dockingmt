"""Current milestone controls preserve historical routes and refuse unsafe input."""

import ast
import gzip
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tomllib
import zipfile
from pathlib import Path

import pytest
import yaml
from versioningit import get_version

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    'current_source_qualification', ROOT / 'devtools/qualify_current_0_1_0.py'
)
caller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(caller)


def document():
    return yaml.safe_load(
        (ROOT / '.github/workflows/qualify-current-0.1.0.yml').read_text()
    )


def test_current_checkpoint_is_manual_read_only_and_same_archive_for_all_minors():
    data = document()
    assert data['permissions'] == {'contents': 'read', 'actions': 'read'}
    assert set(data.get('on', data.get(True))) == {'workflow_dispatch'}
    assert not data['concurrency']['cancel-in-progress']
    job = data['jobs']['installed']
    assert job['strategy']['matrix']['python'] == caller.profile()['python_minors']
    assert job['strategy']['max-parallel'] == 1
    assert job['needs'] == 'build'
    assert (
        job['env']['EXPECTED_WHEEL_SHA256'] == '${{ needs.build.outputs.wheel_sha256 }}'
    )
    assert all('secrets' not in j for j in data['jobs'].values())
    assert all('publish' not in key for key in data['jobs'])
    for key in ['OMP_NUM_THREADS', 'RAYON_NUM_THREADS', 'CARGO_BUILD_JOBS']:
        assert data['env'][key] == '1'


def test_current_profile_checkout_and_context_identities_agree_without_moving_old_sources():
    expected = caller.profile()['sources']
    job = document()['jobs']['installed']
    checkouts = [
        s['with']
        for s in job['steps']
        if s.get('uses', '').startswith('actions/checkout@')
    ]
    assert all(row['persist-credentials'] is False for row in checkouts)
    actual = {
        row['repository'].split('/')[1]: row['ref']
        for row in checkouts
        if row.get('repository', '').split('/')[-1] in expected
    }
    assert actual == expected
    inventory = tomllib.loads((ROOT / 'devtools/dependency_routes.toml').read_text())
    sources = {row['id']: row for row in inventory['source_routes']}
    for minor in caller.profile()['python_minors']:
        context = next(
            row for row in inventory['contexts'] if row['name'] == 'source-010-' + minor
        )
        assert {
            sources[key]['name']: sources[key]['commit'] for key in context['sources']
        } == expected
        assert set(context['overlays']) == {'smonitor', 'depdigest', 'pyunitwizard'}
        assert context['overlay_reason']
    assert (
        sources['molsysmt-source']['commit']
        == 'efbe67e1c6042078144bce1db24aa80bb565dbd2'
    )
    assert (
        sources['e4-molsysmt-20261105']['commit']
        == '00abb958fb93649131d5ce5fe5e12e90cf4900e9'
    )


def test_local_execution_is_refused_before_checkout_or_build(monkeypatch):
    monkeypatch.delenv('GITHUB_ACTIONS', raising=False)
    with pytest.raises(ValueError, match='GitHub-hosted'):
        caller.require_hosted()


def test_source_admission_refuses_an_ignored_preexisting_native_file(
    tmp_path, monkeypatch
):
    source = tmp_path / 'molsysmt'
    source.mkdir()
    (source / '_rust.abi3.so').write_bytes(b'pre-existing binary')
    monkeypatch.setattr(caller, 'TASK', tmp_path)
    monkeypatch.setattr(caller, 'require_hosted', lambda: tmp_path / 'candidate')
    monkeypatch.setattr(caller, 'profile', lambda: {'sources': {'molsysmt': 'a' * 40}})
    monkeypatch.setattr(
        caller,
        'git',
        lambda path, *args: 'a' * 40 if args == ('rev-parse', 'HEAD') else '',
    )
    original = Path.read_text

    def memory(path, *args, **kwargs):
        if str(path) == '/proc/meminfo':
            return 'MemTotal: 8388608 kB\nMemAvailable: 7340032 kB\n'
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'read_text', memory)
    monkeypatch.setattr(caller.os, 'sched_getaffinity', lambda pid: {0})
    monkeypatch.setattr(caller.os, 'getpriority', lambda which, who: 10)
    with pytest.raises(ValueError, match='pre-existing native binary'):
        caller.sources()


@pytest.mark.parametrize('value', ['', 'main', '9d84c0a', 'g' * 40, 'a' * 41])
def test_mutable_or_malformed_candidate_refs_are_refused(monkeypatch, value):
    monkeypatch.setenv('GITHUB_ACTIONS', 'true')
    monkeypatch.setenv('RUNNER_ENVIRONMENT', 'github-hosted')
    monkeypatch.setenv('CANDIDATE_SHA', value)
    with pytest.raises(ValueError, match='full candidate commit'):
        caller.require_hosted()


def test_changed_qualification_head_is_not_a_receipt_for_the_candidate(monkeypatch):
    monkeypatch.setenv('GITHUB_ACTIONS', 'true')
    monkeypatch.setenv('RUNNER_ENVIRONMENT', 'github-hosted')
    monkeypatch.setenv('CANDIDATE_SHA', 'a' * 40)
    monkeypatch.setenv('GITHUB_SHA', 'b' * 40)
    with pytest.raises(ValueError, match='exact selected candidate'):
        caller.require_hosted()


def test_lightweight_numeric_tag_drives_the_real_version_configuration(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'pyproject.toml').write_bytes((ROOT / 'pyproject.toml').read_bytes())
    (source / 'dockingmt').mkdir()
    (source / 'dockingmt/__init__.py').write_text('')
    env = os.environ.copy()
    env.update(
        GIT_AUTHOR_NAME='Qualification',
        GIT_AUTHOR_EMAIL='qualification@example.invalid',
        GIT_COMMITTER_NAME='Qualification',
        GIT_COMMITTER_EMAIL='qualification@example.invalid',
    )
    for args in [
        ['init', '-q'],
        ['add', '.'],
        ['-c', 'commit.gpgSign=false', 'commit', '-qm', 'fixture'],
        ['-c', 'tag.gpgSign=false', 'tag', '0.1.0'],
    ]:
        subprocess.run(['git', '-C', str(source), *args], env=env, check=True)
    assert caller.git(source, 'cat-file', '-t', 'refs/tags/0.1.0') == 'commit'
    assert get_version(source, write=False) == '0.1.0'
    assert not (source / 'dockingmt/_version.py').exists()
    assert caller.git(source, 'remote') == ''


def test_directory_install_retains_its_original_wheel_without_rebuilding(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    (source / 'cache_fixture').mkdir()
    payload = b'VALUE = "original source payload"\n'
    (source / 'cache_fixture/__init__.py').write_bytes(payload)
    (source / 'pyproject.toml').write_text(
        '[build-system]\nrequires=["setuptools"]\nbuild-backend="setuptools.build_meta"\n'
        '[project]\nname="dmt-qualification-cache-fixture"\nversion="0.0.1"\n'
    )
    scratch = tmp_path / 'scratch'
    scratch.mkdir()
    installed = tmp_path / 'installed'
    env = os.environ.copy()
    env.update(TMPDIR=str(scratch), PIP_CACHE_DIR=str(tmp_path / 'pip-cache'))
    result = subprocess.run(
        [
            sys.executable,
            '-m',
            'pip',
            'install',
            '--no-deps',
            '--no-build-isolation',
            '--no-index',
            '--no-clean',
            '--no-compile',
            '--target',
            str(installed),
            str(source),
        ],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    wheels = list(scratch.glob('pip-ephem-wheel-cache-*/wheels/**/*.whl'))
    assert len(wheels) == 1
    with zipfile.ZipFile(wheels[0]) as archive:
        assert archive.read('cache_fixture/__init__.py') == payload
    assert (installed / 'cache_fixture/__init__.py').read_bytes() == payload


def test_milestone_workflow_bytes_remain_registered():
    inventory = tomllib.loads((ROOT / 'devtools/dependency_routes.toml').read_text())
    path = '.github/workflows/qualify-current-0.1.0.yml'
    row = next(row for row in inventory['workflows'] if row['path'] == path)
    assert row['sha256'] == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def test_storage_program_and_observation_oracle_keep_the_original_receiving():
    base = ROOT / 'devguide/validation/data/h5msm_v10_and_comparison_2026-11-10'
    original_manifest = base / 'manifest.json'
    assert (
        caller.digest(original_manifest)
        == '73e8d385c763ebf4c85bcb86099b3785a69445c57c0ff3b30ec44283c8bf22fe'
    )
    manifest = json.loads(original_manifest.read_text())
    oracle = next(
        row
        for row in manifest['files']
        if row['original_path'] == 'producer/oracle.py.txt'
    )
    old = ast.parse(gzip.decompress((base / oracle['path']).read_bytes()))
    current = ast.parse((ROOT / 'dmt_test_support/h5msm_client_oracle.py').read_bytes())
    for kind in [(ast.FunctionDef,), (ast.Import, ast.ImportFrom)]:
        assert {
            ast.dump(n, include_attributes=False)
            for n in old.body
            if isinstance(n, kind)
        } == {
            ast.dump(n, include_attributes=False)
            for n in current.body
            if isinstance(n, kind)
        }
    steps = document()['jobs']['installed']['steps']
    storage = next(
        i
        for i, step in enumerate(steps)
        if step.get('name')
        == 'Receive the original explicit H5MSM 1.0 client under both policies'
    )
    installed = next(
        i
        for i, step in enumerate(steps)
        if step.get('name') == 'Run the complete candidate installed selection'
    )
    assert storage < installed
    assert 'storage-normal' in steps[storage]['run']
    assert 'storage-pm-fs' in steps[storage]['run']
