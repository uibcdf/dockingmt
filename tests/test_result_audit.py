import base64
import builtins
import json
from copy import deepcopy
from pathlib import Path

import pytest
from argdigest.core.errors import UnknownArgumentError

from dockingmt import DockingResult, audit_result, verify_captured_inputs
from dockingmt._private.smonitor import ArgumentError

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / 'devguide/validation/data/audit/minimal_vina_result.json'
)


@pytest.fixture
def record():
    return json.loads(FIXTURE.read_text())


def test_saved_native_control_is_consistent_without_live_dependencies(
    record, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        raise AssertionError('Offline audit attempted an external operation.')

    for name in ('get', 'select', 'extract', 'convert', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split('.')[0] in ('vina', 'molsysviewer', 'molsysmt', 'rdkit'):
            forbidden()
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded_import)
    monkeypatch.setattr(builtins, 'open', forbidden)
    before = deepcopy(record)
    report = audit_result(record)
    assert report['status'] == 'consistent'
    assert report == audit_result(record)
    assert record == before
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert 'content_base64' not in json.dumps(report)
    report['checks'][0]['status'] = 'changed'
    assert audit_result(record)['status'] == 'consistent'
    assert verify_captured_inputs(record['provenance']['backend_artifacts']) == {
        role: len(base64.b64decode(artifact['content_base64']))
        for role, artifact in record['provenance']['backend_artifacts'].items()
    }


@pytest.mark.parametrize('role', ['receptor', 'partner'])
@pytest.mark.parametrize('change', ['content', 'base64', 'digest', 'format'])
def test_captured_byte_contradictions_are_shared_with_replay(record, role, change):
    artifact = record['provenance']['backend_artifacts'][role]
    if change == 'content':
        artifact['content_base64'] = base64.b64encode(b'changed bytes').decode()
    elif change == 'base64':
        artifact['content_base64'] = 'not base64!'
    elif change == 'digest':
        artifact['sha256'] = 'not a digest'
    else:
        artifact['format'] = 'pdb'
    assert audit_result(record)['status'] == 'inconsistent'
    with pytest.raises(ArgumentError):
        verify_captured_inputs(record['provenance']['backend_artifacts'])


@pytest.mark.parametrize('field', ['content_base64', 'sha256'])
def test_missing_captured_evidence_is_incomplete(record, field):
    del record['provenance']['backend_artifacts']['partner'][field]
    report = audit_result(record)
    assert report['status'] == 'incomplete'
    with pytest.raises(ArgumentError):
        verify_captured_inputs(record['provenance']['backend_artifacts'])


def test_invalid_asserted_bytes_take_precedence_over_missing_hash(record):
    artifact = record['provenance']['backend_artifacts']['partner']
    del artifact['sha256']
    artifact['content_base64'] = 'invalid base64!'
    assert audit_result(record)['status'] == 'inconsistent'


def test_unrecorded_artifact_format_is_incomplete(record):
    del record['provenance']['backend_artifacts']['partner']['format']
    assert audit_result(record)['status'] == 'incomplete'


@pytest.mark.parametrize(
    'field,value',
    [
        ('backend', 'other-engine'),
        ('backend_version', 'different-version'),
        (
            'backend_box',
            {'center': [99, 0, 0], 'size': [10, 10, 10], 'unit': 'angstrom'},
        ),
    ],
)
def test_native_score_provenance_contradictions(record, field, value):
    record['provenance'][field] = value
    assert audit_result(record)['status'] == 'inconsistent'


@pytest.mark.parametrize(
    'field,value',
    [
        ('method', 'AutoDock Vina/vinardo'),
        ('component', 'other component'),
        ('unit', 'kJ/mol'),
        ('preferred_direction', 'higher'),
    ],
)
def test_native_score_claim_contradictions(record, field, value):
    record['poses'][0]['metadata']['score_definitions']['vina'][field] = value
    assert audit_result(record)['status'] == 'inconsistent'


@pytest.mark.parametrize(
    'field,value',
    [
        ('stage', 'other-stage'),
        ('partner_sha256', '0' * 64),
        ('preparation_assessment', {'partner': 'qualified', 'receptor': 'unassessed'}),
        ('grid_spacing', {'value': -1, 'unit': 'angstrom'}),
        ('grid_spacing', {'value': 1, 'unit': 'unknown-unit'}),
        ('weights', [True]),
    ],
)
def test_native_context_contradictions(record, field, value):
    record['poses'][0]['metadata']['score_definitions']['vina']['context'][field] = (
        value
    )
    assert audit_result(record)['status'] == 'inconsistent'


@pytest.mark.parametrize('value', [float('nan'), True, '-5', None, []])
def test_invalid_scores_are_reported_instead_of_raising(record, value):
    record['poses'][0]['scores']['vina'] = value
    assert audit_result(record)['status'] == 'inconsistent'


@pytest.mark.parametrize('unit', ['seconds', 'unknown-unit', None, 1])
def test_invalid_coordinate_units_are_reported(record, unit):
    record['poses'][0]['coordinates']['unit'] = unit
    assert audit_result(record)['status'] == 'inconsistent'


def test_compatible_explicit_length_units_agree(record):
    box = record['provenance']['backend_box']
    box['unit'] = 'nm'
    box['center'] = [value / 10 for value in box['center']]
    box['size'] = [value / 10 for value in box['size']]
    assert audit_result(record)['status'] == 'consistent'


@pytest.mark.parametrize(
    'field',
    ['score_definitions', 'coordinates_unit', 'ranking_history', 'backend_version'],
)
def test_absent_evidence_is_not_invented(record, field):
    if field == 'score_definitions':
        for pose in record['poses']:
            del pose['metadata'][field]
    elif field == 'coordinates_unit':
        del record['poses'][0]['coordinates']['unit']
    else:
        del record['provenance'][field]
    assert audit_result(record)['status'] == 'incomplete'


@pytest.mark.parametrize(
    'change',
    ['policy', 'order', 'membership', 'value', 'identity', 'rank', 'descriptor'],
)
def test_latest_ranking_contradictions(record, change):
    if change == 'policy':
        record['provenance']['ranking_policy']['ascending'] = False
    elif change == 'order':
        record['poses'].reverse()
    elif change == 'membership':
        record['poses'].pop()
    elif change == 'value':
        record['poses'][0]['scores']['vina'] += 1
    elif change == 'identity':
        record['poses'][0]['partner_state_id'] = 'other-state'
    elif change == 'rank':
        record['poses'][0]['rank'] = 9
    else:
        record['poses'][0]['metadata']['score_definitions']['vina']['context'][
            'weights'
        ][0] += 1
    assert audit_result(record)['status'] == 'inconsistent'


def test_explicit_reranking_preserves_auditable_history(record):
    result = DockingResult.from_dict(record)
    ranked = result.rank_by('inter', ascending=False).rank_by('vina')
    assert audit_result(ranked.to_dict())['status'] == 'consistent'


def test_ranking_history_membership_cannot_change_silently(record):
    ranked = DockingResult.from_dict(record).rank_by('vina').to_dict()
    ranked['provenance']['ranking_history'][0]['input_order'][0]['pose_id'] = (
        'different-pose'
    )
    report = audit_result(ranked)
    assert report['status'] == 'inconsistent'
    assert any(
        check['check'] == 'ranking_continuity' and check['status'] == 'inconsistent'
        for check in report['checks']
    )


def test_stable_ties_are_part_of_rank_by_evidence(record):
    result = DockingResult.from_dict(record)
    for pose in result:
        pose.scores['vina'] = -1
    ranked = result.rank_by('vina').to_dict()
    assert audit_result(ranked)['status'] == 'consistent'
    ranked['provenance']['ranking_history'][-1]['output_order'].reverse()
    assert audit_result(ranked)['status'] == 'inconsistent'


def test_protocol_snapshots_must_agree(record):
    record['protocol_info']['parameters']['seed'] += 1
    assert audit_result(record)['status'] == 'inconsistent'


def test_history_order_must_follow_explicit_direction(record):
    ranked = DockingResult.from_dict(record).rank_by('vina').to_dict()
    initial = ranked['provenance']['ranking_history'][0]
    initial['input_order'][0]['value'] = -10
    initial['input_order'][1]['value'] = -1
    initial['ascending'] = False
    assert audit_result(ranked)['status'] == 'inconsistent'


@pytest.mark.parametrize('value', [None, {}, 'history', [None]])
def test_malformed_history_is_reported(record, value):
    record['provenance']['ranking_history'] = value
    assert audit_result(record)['status'] == 'inconsistent'


def test_legacy_policy_only_and_unknown_scores_stay_incomplete(record):
    record.pop('schema_version')
    record['provenance'].pop('ranking_history')
    for pose in record['poses']:
        pose['metadata'].pop('score_definitions')
    legacy = DockingResult.from_dict(record).rank_by('vina').to_dict()
    assert (
        legacy['provenance']['ranking_history'][0]['evidence'] == 'legacy_policy_only'
    )
    assert audit_result(legacy)['status'] == 'incomplete'


def test_contradictions_take_precedence_over_missing_evidence(record):
    del record['provenance']['backend_artifacts']['partner']['content_base64']
    record['poses'][0]['scores']['vina'] = float('inf')
    report = audit_result(record)
    assert report['status'] == 'inconsistent'
    assert {'incomplete', 'inconsistent'} <= {
        check['status'] for check in report['checks']
    }


def test_unsupported_schema_is_not_interpreted():
    report = audit_result({'schema_version': '99', 'poses': object()})
    assert report['status'] == 'inconsistent'
    assert len(report['checks']) == 1


@pytest.mark.parametrize(
    'record', [{}, {'poses': [], 'provenance': {}}, {'schema_version': '1.0'}]
)
def test_incomplete_result_containers(record):
    assert audit_result(record)['status'] == 'incomplete'


@pytest.mark.parametrize('function', [audit_result, verify_captured_inputs])
def test_public_audit_argument_admission(function):
    with pytest.raises(ArgumentError):
        function('path.json')
    with pytest.raises(UnknownArgumentError):
        function({}, unknown=True)
