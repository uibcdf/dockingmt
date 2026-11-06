"""Adverse hosted/source/record gates; never import a molecular provider."""

import hashlib
import importlib.util
import json
import tomllib
import zipfile
from copy import deepcopy
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    'e4_caller', ROOT / 'devtools/qualify_3ptb_interactions.py'
)
caller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(caller)


@pytest.mark.parametrize(
    'operation',
    [
        caller.stage,
        caller.build,
        caller.receive,
        lambda: caller.scientific_process('normal'),
    ],
)
def test_local_heavy_execution_is_refused_before_any_setup(monkeypatch, operation):
    monkeypatch.delenv('GITHUB_ACTIONS', raising=False)
    with pytest.raises(ValueError, match='GitHub-hosted'):
        operation()


def test_changed_registered_input_rejects_before_computation(tmp_path, monkeypatch):
    (tmp_path / 'input').write_bytes(b'original')
    monkeypatch.setattr(
        caller, 'INPUTS', {'case': ('input', hashlib.sha256(b'original').hexdigest())}
    )
    assert caller.verify_inputs(tmp_path)['case']['filename'] == 'input'
    (tmp_path / 'input').write_bytes(b'changed')
    with pytest.raises(ValueError, match='input changed'):
        caller.verify_inputs(tmp_path)


@pytest.fixture
def association():
    pose = {
        'pose_id': 'p1',
        'partner_state_id': 'ligand',
        'receptor_state_id': 'receptor',
        'scores': {'empirical': -1.0},
        'coordinates': {'unit': 'nm', 'value': [[1, 2, 3]]},
    }
    original = {
        'poses': [pose],
        'provenance': {
            key: 'declared'
            for key in (
                'dockingmt_version',
                'molsysmt_version',
                'backend',
                'backend_version',
            )
        },
    }
    registration = {
        'inputs': {
            key: {'sha256': key + '-identity'} for key in ('preparation', 'result')
        }
    }
    value = {
        'schema': 'dockingmt.3ptb_interaction_association@1',
        'inputs': {key: row['sha256'] for key, row in registration['inputs'].items()},
        'selected_original_position': 1,
        'original_decoded_result_sha256': caller.ORIGINAL_RESULT_SHA,
        'original_producer': original['provenance'],
        'original_scores': pose['scores'],
        'pose_coordinates_sha256': hashlib.sha256(
            json.dumps(
                pose['coordinates'],
                sort_keys=True,
                separators=(',', ':'),
                allow_nan=False,
            ).encode()
        ).hexdigest(),
        'files': dict.fromkeys(caller.FILES, {}),
        'interaction_detector_calls': 6,
        'analyses': {
            'retained_pose': {'hbonds': 2, 'hydrophobic': 3},
            'translated_geometry_control': {'hbonds': 0, 'hydrophobic': 0},
        },
        'analytic_controls': {'analytic_positive': 1, 'analytic_adverse': 0},
        'existing_ligand_atom_correspondence': [[i, i] for i in range(13)],
        'merged_ligand_atom_indices': dict.fromkeys(
            ('retained_pose', 'translated_geometry_control'), list(range(18))
        ),
        **{
            name: pose[name]
            for name in ('pose_id', 'partner_state_id', 'receptor_state_id')
        },
    }
    journal = [
        {'stage': 'detector', 'case': case, 'family': family, 'status': status}
        for case, family in sorted(caller.EXPECTED_CALLS)
        for status in ('started', 'completed')
    ]
    journal.append({'stage': 'workflow', 'status': 'completed'})
    return value, original, registration, journal


def test_complete_record_bindings_are_accepted_without_molecular_work(association):
    original = deepcopy(association)
    caller.validate_association(*association)
    assert association == original


@pytest.mark.parametrize(
    'damage',
    [
        'input',
        'position',
        'state',
        'coordinates',
        'scores',
        'producer',
        'result',
        'denominator',
        'file',
        'map',
        'axis',
        'missing-events',
        'duplicate-events',
        'unfinished',
        'missing-analysis',
        'invalid-count',
        'adverse-control',
        'positive-control',
        'boolean-control',
    ],
)
def test_record_corruption_and_unknown_completion_are_not_accepted(association, damage):
    record, _, _, journal = association
    if damage == 'input':
        record['inputs']['result'] = 'other'
    elif damage == 'position':
        record['selected_original_position'] = True
    elif damage == 'state':
        record['partner_state_id'] = 'other'
    elif damage == 'coordinates':
        record['pose_coordinates_sha256'] = 'changed'
    elif damage == 'scores':
        record['original_scores'] = {'empirical': -9.0}
    elif damage == 'producer':
        record['original_producer'] = {'backend': 'reader-version'}
    elif damage == 'result':
        record['original_decoded_result_sha256'] = 'changed'
    elif damage == 'denominator':
        record['interaction_detector_calls'] = 5
    elif damage == 'file':
        record['files'].pop('retained_pose.h5msm')
    elif damage == 'map':
        record['existing_ligand_atom_correspondence'][0][1] = 1
    elif damage == 'axis':
        record['merged_ligand_atom_indices']['retained_pose'][0] = True
    elif damage == 'missing-events':
        journal.clear()
    elif damage == 'duplicate-events':
        journal[0] = journal[2]
    elif damage == 'missing-analysis':
        record['analyses'].pop('retained_pose')
    elif damage == 'invalid-count':
        record['analyses']['retained_pose']['hbonds'] = True
    elif damage == 'adverse-control':
        record['analyses']['translated_geometry_control']['hbonds'] = 1
    elif damage == 'positive-control':
        record['analytic_controls']['analytic_positive'] = 0
    elif damage == 'boolean-control':
        record['analytic_controls']['analytic_positive'] = True
    else:
        journal[-1]['status'] = 'started'
    with pytest.raises(ValueError):
        caller.validate_association(*association)


@pytest.mark.parametrize(
    'damage', [None, 'payload', 'extra', 'license', 'python', 'tag', 'entry-point']
)
def test_installed_archive_cannot_substitute_source_or_contract(tmp_path, damage):
    root = tmp_path / 'source'
    (root / 'dockingmt').mkdir(parents=True)
    (root / 'devtools/conda-build').mkdir(parents=True)
    payload = b'fixture = True\n'
    (root / 'dockingmt/__init__.py').write_bytes(payload)
    (root / 'LICENSE').write_bytes(b'MIT fixture')
    (root / 'devtools/conda-build/resources.toml').write_text(
        'required_paths = ["site-packages/dockingmt/__init__.py"]\n'
    )
    prefix = 'dockingmt-0.1.1.dev1.dist-info/'
    files = {
        'dockingmt/__init__.py': payload,
        prefix
        + 'METADATA': b'Name: dockingmt\nVersion: 0.1.1.dev1\nLicense-Expression: MIT\nRequires-Python: >=3.11,<3.15\n',
        prefix + 'WHEEL': b'Root-Is-Purelib: true\nTag: py3-none-any\n',
        prefix
        + 'entry_points.txt': b'[molsysviewer.addons]\ndockingmt = molsysviewer_dockingmt\n',
        prefix + 'licenses/LICENSE': b'MIT fixture',
    }
    if damage == 'payload':
        files['dockingmt/__init__.py'] = b'other source'
    elif damage == 'extra':
        files['dmt_test_support/__init__.py'] = b'not shipped'
    elif damage == 'license':
        files[prefix + 'licenses/LICENSE'] = b'other'
    elif damage == 'python':
        files[prefix + 'METADATA'] = files[prefix + 'METADATA'].replace(
            b'<3.15', b'<3.14'
        )
    elif damage == 'tag':
        files[prefix + 'WHEEL'] = b'Root-Is-Purelib: false\nTag: cp314-linux_x86_64\n'
    elif damage == 'entry-point':
        files[prefix + 'entry_points.txt'] += b'dockingmt = other\n'
    path = tmp_path / 'consumer.whl'
    with zipfile.ZipFile(path, 'w') as archive:
        for name, value in files.items():
            archive.writestr(name, value)
    if damage is None:
        assert caller.wheel_contract(path, root)['runtime_sha256'] == {
            'dockingmt/__init__.py': hashlib.sha256(payload).hexdigest()
        }
    else:
        with pytest.raises((ValueError, caller.configparser.DuplicateOptionError)):
            caller.wheel_contract(path, root)


def test_manual_route_is_read_only_serial_and_uses_reviewed_sources():
    workflow = yaml.safe_load(
        (ROOT / '.github/workflows/qualify-3ptb-interactions.yml').read_text()
    )
    assert workflow['permissions'] == {'contents': 'read'}
    assert workflow['concurrency']['cancel-in-progress'] is False
    job = workflow['jobs']['receive']
    assert job['runs-on'] == 'ubuntu-latest'
    assert 'strategy' not in job
    assert job['env']['EXPECTED_SOURCE_SHA'] == '${{ inputs.expected_source_sha }}'
    checkouts = [
        s for s in job['steps'] if s.get('uses', '').startswith('actions/checkout@')
    ]
    assert all(s['with']['persist-credentials'] is False for s in checkouts)
    routes = tomllib.loads((ROOT / 'devtools/dependency_routes.toml').read_text())
    expected = {
        'uibcdf/' + row['name']: row['commit'] for row in routes['source_routes']
    }
    actual = {
        s['with']['repository']: s['with']['ref']
        for s in checkouts
        if s['with'].get('repository') in expected
    }
    assert actual == expected
    assert any(
        'Retain original outcomes' in s.get('name', '')
        and s['if'] == '${{ !cancelled() }}'
        for s in job['steps']
    )
