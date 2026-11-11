"""Recover the original file without changing tested scientific gates or identity."""

import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    'current_recovery', ROOT / 'devtools/current_0_1_0_recovery.py'
)
recovery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recovery)


@pytest.fixture
def receiving(tmp_path, monkeypatch):
    root, task = tmp_path / 'workflow', tmp_path / 'task'
    candidate = task / 'candidate'
    (root / 'devtools').mkdir(parents=True)
    (candidate / 'devtools').mkdir(parents=True)
    archive = (
        ROOT / 'devguide/validation/data/current_source_0_1_0_sdk_admission_2026-11-10'
    )
    original = gzip.decompress(
        (archive / 'qualified/devtools/qualify_current_0_1_0.py.gz').read_bytes()
    )
    assert hashlib.sha256(original).hexdigest() == recovery.HELPER_SHA256
    (candidate / 'devtools/qualify_current_0_1_0.py').write_bytes(original)
    for name in [
        'devtools/qualify_current_0_1_0.py',
        'devtools/qualify_source_0_1_0.py',
        'devtools/source_0_1_0_current.toml',
    ]:
        (root / name).write_bytes((ROOT / name).read_bytes())
        if name != 'devtools/qualify_current_0_1_0.py':
            (candidate / name).write_bytes((ROOT / name).read_bytes())
    (candidate / 'LICENSE').write_bytes((ROOT / 'LICENSE').read_bytes())
    (task / 'wheels').mkdir()
    (task / 'wheels/dockingmt-0.1.0-py3-none-any.whl').write_bytes(b'original-wheel')
    (task / 'evidence').mkdir()
    receipt = {
        'candidate': recovery.CANDIDATE,
        'tree': recovery.TREE,
        'qualification_source': recovery.CANDIDATE,
        'run_id': 42976065511,
        'run_attempt': 1,
        'contract': {
            'source_input_sha256': {'LICENSE': recovery.digest(candidate / 'LICENSE')}
        },
    }
    receipt_path = task / 'evidence/build-receipt.json'
    receipt_path.write_text(json.dumps(receipt))
    wheel_sha = recovery.digest(task / 'wheels/dockingmt-0.1.0-py3-none-any.whl')
    monkeypatch.setattr(recovery, 'WHEEL_SHA256', wheel_sha)
    monkeypatch.setattr(recovery, 'RECEIPT_SHA256', recovery.digest(receipt_path))
    monkeypatch.setattr(recovery, 'sys', SimpleNamespace(version_info=(3, 13, 18)))
    calls = []

    def tree(arguments, *, text):
        assert arguments == ['git', '-C', str(candidate), 'rev-parse', 'HEAD^{tree}']
        assert text
        calls.append(arguments)
        return recovery.TREE + '\n'

    monkeypatch.setattr(recovery, 'subprocess', SimpleNamespace(check_output=tree))
    for key, value in {
        'GITHUB_ACTIONS': 'true',
        'RUNNER_ENVIRONMENT': 'github-hosted',
        'GITHUB_REPOSITORY': 'uibcdf/dockingmt',
        'GITHUB_EVENT_NAME': 'workflow_dispatch',
        'GITHUB_WORKFLOW_REF': 'uibcdf/dockingmt/.github/workflows/recover-current-0.1.0-python313.yml@refs/heads/main',
        'DOCKINGMT_RECOVERY': 'current-010-python313-original-wheel',
        'EXPECTED_PYTHON': '3.13',
        'EXPECTED_WHEEL_SHA256': wheel_sha,
        'GITHUB_SHA': 'b' * 40,
    }.items():
        monkeypatch.setenv(key, value)
    return root, task, candidate, calls


def test_original_file_and_unmodified_scientific_gates_are_admitted(receiving):
    root, task, _, calls = receiving
    recovery.admit(root, task, recovery.CANDIDATE)
    assert len(calls) == 1


@pytest.mark.parametrize(
    'key,value',
    [
        ('GITHUB_ACTIONS', 'false'),
        ('RUNNER_ENVIRONMENT', 'self-hosted'),
        ('GITHUB_REPOSITORY', 'outside/dockingmt'),
        ('GITHUB_EVENT_NAME', 'pull_request'),
        (
            'GITHUB_WORKFLOW_REF',
            'uibcdf/dockingmt/.github/workflows/other.yml@refs/heads/main',
        ),
        ('DOCKINGMT_RECOVERY', 'arbitrary'),
        ('EXPECTED_PYTHON', '3.14'),
        ('EXPECTED_WHEEL_SHA256', '0' * 64),
        ('GITHUB_SHA', 'not-a-commit'),
    ],
)
def test_wrong_recovery_context_stops_before_git_or_execution(
    receiving, monkeypatch, key, value
):
    root, task, _, calls = receiving
    monkeypatch.setenv(key, value)
    with pytest.raises(ValueError, match='declared original-wheel'):
        recovery.admit(root, task, recovery.CANDIDATE)
    assert not calls


@pytest.mark.parametrize(
    'where,relative,reason',
    [
        (
            'candidate',
            'devtools/qualify_current_0_1_0.py',
            'Original qualification helper',
        ),
        ('root', 'devtools/qualify_current_0_1_0.py', 'outside admission'),
        ('root', 'devtools/source_0_1_0_current.toml', 'frozen profile'),
        ('root', 'devtools/qualify_source_0_1_0.py', 'frozen profile'),
        (
            'task',
            'wheels/dockingmt-0.1.0-py3-none-any.whl',
            'original receipt and wheel',
        ),
        ('task', 'evidence/build-receipt.json', 'original receipt and wheel'),
        ('candidate', 'LICENSE', 'build input changed'),
    ],
)
def test_changed_original_inputs_are_refused(receiving, where, relative, reason):
    root, task, candidate, _ = receiving
    path = {'root': root, 'task': task, 'candidate': candidate}[where] / relative
    addition = '\nUNEXPECTED = True\n' if relative.endswith('.py') else '\nchanged\n'
    path.write_bytes(path.read_bytes() + addition.encode())
    with pytest.raises(ValueError, match=reason):
        recovery.admit(root, task, recovery.CANDIDATE)


def test_other_candidate_tree_and_interpreter_are_refused(receiving, monkeypatch):
    root, task, _, _ = receiving
    with pytest.raises(ValueError, match='declared original-wheel'):
        recovery.admit(root, task, 'a' * 40)
    monkeypatch.setattr(
        recovery, 'subprocess', SimpleNamespace(check_output=lambda *a, **k: 'a' * 40)
    )
    with pytest.raises(ValueError, match='candidate tree'):
        recovery.admit(root, task, recovery.CANDIDATE)
    monkeypatch.setattr(recovery, 'sys', SimpleNamespace(version_info=(3, 14, 10)))
    with pytest.raises(ValueError, match='declared original-wheel'):
        recovery.admit(root, task, recovery.CANDIDATE)


def test_partial_retry_downloads_the_actual_producer_artifact():
    data = yaml.safe_load(
        (ROOT / '.github/workflows/qualify-current-0.1.0.yml').read_text()
    )
    producer = data['jobs']['build']
    upload = next(step for step in producer['steps'] if step.get('id') == 'archive')
    assert upload['uses'] == 'actions/upload-artifact@v4'
    assert (
        producer['outputs']['wheel_artifact_id']
        == '${{ steps.archive.outputs.artifact-id }}'
    )
    download = next(
        step['with']
        for step in data['jobs']['installed']['steps']
        if step.get('uses') == 'actions/download-artifact@v4'
    )
    assert download['artifact-ids'] == '${{ needs.build.outputs.wheel_artifact_id }}'
    assert download['merge-multiple'] is True and 'name' not in download
    assert 'run_attempt' not in download['artifact-ids']
    steps = data['jobs']['installed']['steps']
    scratch = next(
        i
        for i, step in enumerate(steps)
        if step.get('name') == 'Prepare owned scratch and record host allocation'
    )
    acquisition = next(
        i
        for i, step in enumerate(steps)
        if step.get('uses') == 'actions/download-artifact@v4'
    )
    assert scratch < acquisition


def test_recovery_preserves_all_original_scientific_steps_and_sources():
    main = yaml.safe_load(
        (ROOT / '.github/workflows/qualify-current-0.1.0.yml').read_text()
    )
    data = yaml.safe_load(
        (ROOT / '.github/workflows/recover-current-0.1.0-python313.yml').read_text()
    )
    assert set(data.get('on', data.get(True))) == {'workflow_dispatch'}
    assert data['permissions'] == {'contents': 'read', 'actions': 'read'}
    assert list(data['jobs']) == ['installed']
    job = data['jobs']['installed']
    assert job['strategy']['matrix']['python'] == ['3.13']
    assert job['strategy']['max-parallel'] == 1 and 'needs' not in job
    assert job['env']['EXPECTED_WHEEL_SHA256'] == recovery.WHEEL_SHA256
    assert data['env']['CANDIDATE_SHA'] == recovery.CANDIDATE
    original = {
        s['name']: s
        for s in main['jobs']['installed']['steps']
        if s.get('shell') == 'bash -l {0}'
    }
    observed = {s['name']: s for s in job['steps'] if s.get('shell') == 'bash -l {0}'}
    assert observed == original and len(observed) == 5
    original_sources = [
        s['with']
        for s in main['jobs']['installed']['steps']
        if s.get('with', {}).get('repository')
    ]
    assert [
        s['with'] for s in job['steps'] if s.get('with', {}).get('repository')
    ] == original_sources
    download = next(
        s['with']
        for s in job['steps']
        if s.get('uses') == 'actions/download-artifact@v4'
    )
    assert (
        download['artifact-ids'] == '13835014036'
        and download['run-id'] == '42976065511'
    )
    assert (
        download['github-token'] == '${{ github.token }}' and download['merge-multiple']
    )
