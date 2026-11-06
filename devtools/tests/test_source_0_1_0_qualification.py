"""Adverse administrative controls; no environment, build or molecular operation."""

import hashlib
import importlib.util
import tomllib
import zipfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    'source_qualification', ROOT / 'devtools/qualify_source_0_1_0.py'
)
caller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(caller)


@pytest.fixture
def archive(tmp_path):
    payload = b'__version__ = "0.1.0"\n'
    license_bytes = b'MIT fixture\n'
    prefix = 'dockingmt-0.1.0.dist-info/'
    files = {
        'dockingmt/__init__.py': payload,
        prefix + 'METADATA': (
            b'Metadata-Version: 2.4\nName: dockingmt\nVersion: 0.1.0\n'
            b'Requires-Python: >=3.11,<3.15\nLicense-Expression: MIT\n'
        ),
        prefix + 'WHEEL': b'Root-Is-Purelib: true\nTag: py3-none-any\n',
        prefix + 'entry_points.txt': (
            b'[molsysviewer.addons]\ndockingmt = molsysviewer_dockingmt\n'
        ),
        prefix + 'licenses/LICENSE': license_bytes,
    }
    frozen = {
        'archive_checks': {
            'runtime_sha256': {
                'dockingmt/__init__.py': hashlib.sha256(payload).hexdigest()
            },
            'python_requires': '>=3.11,<3.15',
            'requires_dist': [],
        },
        'source_input_sha256': {'LICENSE': hashlib.sha256(license_bytes).hexdigest()},
    }
    return tmp_path / 'candidate.whl', files, frozen


def write(path, files):
    with zipfile.ZipFile(path, 'w') as archive:
        for name, value in files.items():
            archive.writestr(name, value)


def test_correct_fixture_contract(archive):
    path, files, frozen = archive
    write(path, files)
    assert (
        caller.wheel_payload(path, frozen) == frozen['archive_checks']['runtime_sha256']
    )


@pytest.mark.parametrize(
    'change', ['runtime', 'extra-source', 'version', 'license', 'tag']
)
def test_corrupted_or_unshipped_inputs_are_rejected(archive, change):
    path, files, frozen = archive
    prefix = 'dockingmt-0.1.0.dist-info/'
    if change == 'runtime':
        files['dockingmt/__init__.py'] += b'changed\n'
    elif change == 'extra-source':
        files['dmt_test_support/__init__.py'] = b''
    elif change == 'version':
        files[prefix + 'METADATA'] = files[prefix + 'METADATA'].replace(
            b'0.1.0', b'0.0.0'
        )
    elif change == 'license':
        files[prefix + 'licenses/LICENSE'] = b'different'
    else:
        files[prefix + 'WHEEL'] = b'Root-Is-Purelib: true\nTag: cp311-linux_x86_64\n'
    write(path, files)
    with pytest.raises(ValueError):
        caller.wheel_payload(path, frozen)


def test_heavy_entry_point_rejects_local_execution(monkeypatch):
    monkeypatch.delenv('GITHUB_ACTIONS', raising=False)
    with pytest.raises(ValueError, match='GitHub-hosted'):
        caller.require_hosted()


def test_frozen_producer_is_not_replaced():
    receipt = caller.frozen_receipt()
    assert receipt['candidate_source'] == caller.CANDIDATE
    assert len(receipt['archive_checks']['runtime_sha256']) == 63


def test_hosted_route_has_no_publisher_and_consumes_same_run_build():
    workflow = yaml.safe_load(
        (ROOT / '.github/workflows/qualify-source-0.1.0.yml').read_text()
    )
    assert workflow['permissions'] == {'contents': 'read', 'actions': 'read'}
    assert not workflow['concurrency']['cancel-in-progress']
    jobs = workflow['jobs']
    assert jobs['installed']['needs'] == 'build'
    assert jobs['installed']['runs-on'] == 'ubuntu-latest'
    assert jobs['installed']['strategy']['matrix']['python'] == ['3.11', '3.13']
    assert jobs['installed']['strategy']['max-parallel'] == 1
    assert jobs['installed']['env']['EXPECTED_WHEEL_SHA256'] == (
        '${{ needs.build.outputs.wheel_sha256 }}'
    )
    checkouts = [
        s
        for s in jobs['installed']['steps']
        if s.get('uses', '').startswith('actions/checkout@')
    ]
    assert all(s['with']['persist-credentials'] is False for s in checkouts)
    assert len([s for s in checkouts if s['with'].get('ref') == caller.CANDIDATE]) == 1
    routes = tomllib.loads((ROOT / 'devtools/dependency_routes.toml').read_text())
    expected = {'uibcdf/' + s['name']: s['commit'] for s in routes['source_routes']}
    actual = {
        s['with']['repository']: s['with']['ref']
        for s in checkouts
        if s['with'].get('repository') in expected
    }
    assert actual == expected
