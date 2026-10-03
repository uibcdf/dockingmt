"""Saved scoring-pose evidence is auditable without molecular or engine work."""

import base64
import builtins
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
import pyunitwizard as puw
from argdigest.core.errors import UnknownArgumentError
from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError


@pytest.fixture(scope='module')
def native_record():
    source = (
        Path(__file__).resolve().parents[1]
        / 'devguide/validation/data/audit/minimal_scored_pose.json'
    )
    return json.loads(source.read_text())


def test_fresh_native_scoring_and_rescoring_produce_auditable_evidence():
    problem = dmt.DockingProblem(
        MINIMAL_REC_PDBQT,
        MINIMAL_LIG_PDBQT,
        dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
        metadata={
            'partner_state_id': 'ligand-control',
            'receptor_state_id': 'receptor-control',
        },
    )
    first = dmt.score(
        problem,
        dmt.VinaProtocol(cpu=1, seed=17, capture_backend_inputs=True),
        score_name='vina',
    )
    second = dmt.score(
        problem,
        dmt.VinaProtocol(
            cpu=1, seed=17, capture_backend_inputs=True, scoring='vinardo'
        ),
        pose=first,
        score_name='vinardo',
    )
    record = second.to_dict()
    assert len(record['scores']) == 16
    assert dmt.audit_pose(record)['status'] == 'consistent'


@pytest.fixture
def record(native_record):
    return deepcopy(native_record)


def test_native_rescoring_record_is_consistent_without_external_operations(
    record, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Offline pose audit attempted external work.')

    for name in ('get', 'convert', 'select', 'extract', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    original = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name.split('.')[0] in ('vina', 'molsysviewer', 'molsysmt', 'rdkit'):
            forbidden()
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded)
    monkeypatch.setattr(builtins, 'open', forbidden)
    before = deepcopy(record)
    report = dmt.audit_pose(record)
    assert report['status'] == 'consistent'
    assert report['scope'] == 'saved_pose_internal_consistency'
    assert report == dmt.audit_pose(record)
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert 'content_base64' not in json.dumps(report)
    assert record == before
    report['checks'][0]['status'] = 'changed'
    assert dmt.audit_pose(record)['status'] == 'consistent'


@pytest.mark.parametrize(
    'field',
    [
        'value',
        'definition',
        'state',
        'duplicate',
        'content',
        'backend',
        'box',
        'score_name',
        'component',
        'applied',
        'unused',
        'operation',
        'geometry',
        'preparation',
    ],
)
def test_recorded_scoring_contradictions_are_reported(record, field):
    entry = record['metadata']['scoring_history'][0]
    if field == 'value':
        record['scores']['vina'] += 1
    elif field == 'definition':
        record['metadata']['score_definitions']['vina']['context']['weights'][0] += 1
    elif field == 'state':
        record['partner_state_id'] = 'other-state'
    elif field == 'duplicate':
        record['metadata']['scoring_history'].append(deepcopy(entry))
    elif field == 'content':
        entry['backend_artifacts']['partner']['content_base64'] = base64.b64encode(
            b'changed'
        ).decode()
    elif field == 'backend':
        entry['backend_version'] = 'other-version'
    elif field == 'box':
        entry['backend_box']['center'][0] = 20
    elif field == 'score_name':
        entry['score_name'] = 'other-label'
    elif field == 'component':
        entry['score_definitions']['vina.lig_intra']['component'] = 'flex_intra'
    elif field == 'applied':
        entry['applied_parameters']['scoring'] = 'vinardo'
    elif field == 'unused':
        entry['unused_search_parameters'] = []
    elif field == 'operation':
        entry['operation'] = 'dock'
    elif field == 'geometry':
        entry['geometry_check']['coordinate_tolerance']['unit'] = 'seconds'
    else:
        entry['preparation']['partner']['assessment_report']['assessment'] = 'qualified'
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


@pytest.mark.parametrize(
    'field',
    [
        'score_name',
        'backend_box',
        'protocol',
        'applied_parameters',
        'backend_artifacts',
        'geometry_check',
        'preparation',
    ],
)
def test_missing_evaluation_evidence_stays_incomplete(record, field):
    del record['metadata']['scoring_history'][0][field]
    assert dmt.audit_pose(record)['status'] == 'incomplete'


@pytest.mark.parametrize(
    'value',
    [None, {}, 'history', [None], [{'schema_version': '99', 'scores': object()}]],
)
def test_malformed_or_future_history_is_bounded(record, value):
    record['metadata']['scoring_history'] = value
    report = dmt.audit_pose(record)
    assert report['status'] == 'inconsistent'
    assert json.loads(json.dumps(report)) == report


@pytest.mark.parametrize('value', [True, np.nan, np.inf, '-1'])
def test_invalid_current_and_historical_scores(record, value):
    record['metadata']['scoring_history'][0]['scores']['vina'] = value
    assert dmt.audit_pose(record)['status'] == 'inconsistent'
    record['scores']['vina'] = value
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


def test_no_capture_and_unknown_state_are_incomplete(record):
    for entry in record['metadata']['scoring_history']:
        for artifact in entry['backend_artifacts'].values():
            artifact.pop('content_base64')
        entry['protocol']['parameters']['capture_backend_inputs'] = False
        entry['applied_parameters']['capture_backend_inputs'] = False
    assert dmt.audit_pose(record)['status'] == 'incomplete'
    for entry in record['metadata']['scoring_history']:
        entry['preparation']['partner']['state_id'] = None
        entry['geometry_check']['state_checks']['partner'] = 'unknown'
    record['partner_state_id'] = None
    assert dmt.audit_pose(record)['status'] == 'incomplete'


def test_pose_without_history_and_external_scores_keep_unknown_origin(record):
    standalone = {key: value for key, value in record.items() if key != 'metadata'}
    assert dmt.audit_pose(standalone)['status'] == 'incomplete'
    record['scores']['review'] = 0.75
    assert dmt.audit_pose(record)['status'] == 'incomplete'


def test_explicit_compatible_units_preserve_user_policy(record):
    for entry in record['metadata']['scoring_history']:
        entry['backend_box']['unit'] = 'nm'
        for key in ('center', 'size'):
            entry['backend_box'][key] = [
                value / 10 for value in entry['backend_box'][key]
            ]
    with puw.context(standard_units=['pm', 'fs', 'kJ/mol']):
        units = deepcopy(puw.configure.get_standard_units())
        assert dmt.audit_pose(record)['status'] == 'consistent'
        assert puw.configure.get_standard_units() == units


def test_unsupported_pose_schema_is_not_interpreted():
    report = dmt.audit_pose({'schema_version': '99', 'metadata': object()})
    assert report['status'] == 'inconsistent'
    assert len(report['checks']) == 1


def test_public_pose_audit_admission():
    with pytest.raises(ArgumentError):
        dmt.audit_pose('pose.json')
    with pytest.raises(UnknownArgumentError):
        dmt.audit_pose({}, unknown=True)


def test_retained_descriptor_context_uses_strict_json_semantics(record):
    historical = record['metadata']['scoring_history'][0]['score_definitions']['vina']
    current = record['metadata']['score_definitions']['vina']
    historical['context']['flag'] = 1
    current['context']['flag'] = True
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


def test_historical_score_cannot_disappear_from_current_pose(record):
    del record['scores']['vina']
    del record['metadata']['score_definitions']['vina']
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


@pytest.mark.parametrize(
    'parameters',
    [
        {'cpu': True},
        {'seed': True},
        {'scoring': 'ad4'},
        {'energy_range': {'value': True, 'unit': 'kcal/mol'}},
    ],
)
def test_invalid_resolved_protocol_is_reported(record, parameters):
    record['metadata']['scoring_history'][0]['protocol']['parameters'].update(
        parameters
    )
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


def test_missing_resolved_parameter_is_not_defaulted(record):
    del record['metadata']['scoring_history'][0]['protocol']['parameters']['cpu']
    assert dmt.audit_pose(record)['status'] == 'incomplete'


def test_legacy_scoring_record_is_readable_with_missing_independent_evidence(record):
    for entry in record['metadata']['scoring_history']:
        del entry['score_name']
        del entry['backend_box']
    assert dmt.DockingPose.from_dict(record).to_dict() == record
    assert dmt.audit_pose(record)['status'] == 'incomplete'


def test_stored_geometry_is_validated_but_input_match_is_not_replayed(record):
    record['coordinates']['value'][0][0] += 10
    assert dmt.audit_pose(record)['status'] == 'consistent'
    record['coordinates']['unit'] = 'seconds'
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


def test_unknown_state_and_different_hash_are_not_replaced(record):
    before = deepcopy(record)
    entry = record['metadata']['scoring_history'][0]
    entry['backend_artifacts']['partner'].pop('content_base64')
    entry['score_definitions']['vina']['context']['partner_sha256'] = '0' * 64
    report = dmt.audit_pose(record)
    assert report['status'] == 'inconsistent'
    assert {'incomplete', 'inconsistent'} <= {
        item['status'] for item in report['checks']
    }
    assert before['partner_state_id'] == record['partner_state_id']


def test_saved_control_audits_in_fresh_process_without_optional_providers(
    record, tmp_path
):
    source = tmp_path / 'pose.json'
    source.write_text(json.dumps(record))
    script = """
import importlib.abc
import json
import sys
class BlockOptional(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('vina', 'molsysviewer', 'rdkit'):
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, BlockOptional())
import dockingmt as dmt
with open(sys.argv[1]) as stream:
    record = json.load(stream)
report = dmt.audit_pose(record)
assert report['status'] == 'consistent'
assert 'vina' not in sys.modules and 'molsysviewer' not in sys.modules
print(report['status'])
"""
    completed = subprocess.run(
        [sys.executable, '-c', script, str(source)],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == 'consistent'
