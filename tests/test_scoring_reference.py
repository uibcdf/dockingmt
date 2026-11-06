"""Reference declarations over detached records; no new molecular observations."""

import builtins
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError


@pytest.fixture
def legacy_record():
    path = (
        Path(__file__).resolve().parents[1]
        / 'devguide/validation/data/audit/minimal_scored_pose.json'
    )
    return json.loads(path.read_text())


@pytest.fixture
def record(legacy_record):
    # Synthetic declaration for audit controls, not a new producer for old data.
    entry = legacy_record['metadata']['scoring_history'][0]
    name = entry['score_name'] + '.lig_intra_best_pose'
    entry['reference_energy'] = {
        'schema_version': '1.0',
        'policy': 'native_current_conformation',
        'score_name': name,
        'value': entry['scores'][name],
        'unit': 'kcal/mol',
    }
    for name in entry['scores']:
        for definitions in (
            entry['score_definitions'],
            legacy_record['metadata']['score_definitions'],
        ):
            definitions[name]['context']['reference_energy_policy'] = (
                'native_current_conformation'
            )
    return legacy_record


def test_legacy_reference_stays_uninterpreted(legacy_record):
    before = deepcopy(legacy_record)
    report = dmt.audit_pose(legacy_record)
    assert report['status'] == 'consistent'
    # Canonical report retained by #76; new optional evidence must not relabel it.
    encoded = json.dumps(report, sort_keys=True, separators=(',', ':'), allow_nan=False)
    assert hashlib.sha256(encoded.encode()).hexdigest() == (
        'c3ef8215c6283c15bc9db2fb763cad7aa6fc30036082823afb23aadee8cbe7ec'
    )
    assert legacy_record == before


def test_explicit_reference_matches_component_and_collection_path(record):
    report = dmt.audit_pose(record)
    assert report['status'] == 'consistent'
    assert any(check['check'] == 'reference_energy_value' for check in report['checks'])
    collection = dmt.DockingResult([dmt.DockingPose.from_dict(record)]).to_dict()
    result = dmt.audit_result(collection)
    assert result['status'] == 'incomplete'  # Collection provenance is absent.
    checks = [
        check
        for check in result['checks']
        if check['check'] == 'reference_energy_value'
    ]
    assert len(checks) == 1 and checks[0]['status'] == 'consistent'
    assert checks[0]['path'].startswith('/poses/0/metadata/scoring_history/0/')


@pytest.mark.parametrize(
    'change', ['policy', 'value', 'name', 'dimension', 'schema', 'context', 'container']
)
def test_reference_contradictions_are_not_silently_accepted(record, change):
    entry = record['metadata']['scoring_history'][0]
    reference = entry['reference_energy']
    if change == 'policy':
        reference['policy'] = 'shared_external_reference'
    elif change == 'value':
        reference['value'] += 1
    elif change == 'name':
        reference['score_name'] = entry['score_name'] + '.lig_intra'
    elif change == 'dimension':
        reference['unit'] = 'nm'
    elif change == 'schema':
        reference['schema_version'] = '99'
    elif change == 'container':
        entry['reference_energy'] = []
    else:
        for name in entry['scores']:
            for definitions in (
                entry['score_definitions'],
                record['metadata']['score_definitions'],
            ):
                definitions[name]['context']['reference_energy_policy'] = 'other'
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


@pytest.mark.parametrize('value', [True, '0', float('nan'), float('inf'), [0]])
def test_reference_quantity_requires_finite_real_wire_value(record, value):
    record['metadata']['scoring_history'][0]['reference_energy']['value'] = value
    assert dmt.audit_pose(record)['status'] == 'inconsistent'


@pytest.mark.parametrize('field', ['policy', 'score_name'])
def test_reference_declaration_rejects_non_scalar_mapping_fields(record, field):
    record['metadata']['scoring_history'][0]['reference_energy'][field] = np.array(
        ['first', 'second']
    )
    report = dmt.audit_pose(record)
    assert report['status'] == 'inconsistent'
    assert any(
        check['reason'] == 'invalid_reference_declaration' for check in report['checks']
    )


@pytest.mark.parametrize(
    'missing', ['record', 'empty', 'value', 'unit', 'policy', 'score_context']
)
def test_absent_reference_evidence_remains_incomplete(record, missing):
    entry = record['metadata']['scoring_history'][0]
    if missing == 'record':
        del entry['reference_energy']
    elif missing == 'empty':
        entry['reference_energy'] = {}
    elif missing == 'score_context':
        for name in entry['scores']:
            for definitions in (
                entry['score_definitions'],
                record['metadata']['score_definitions'],
            ):
                del definitions[name]['context']['reference_energy_policy']
    else:
        del entry['reference_energy'][missing]
    assert dmt.audit_pose(record)['status'] == 'incomplete'


def test_reference_energy_conversion_keeps_application_policy(record):
    entry = record['metadata']['scoring_history'][0]
    reference = entry['reference_energy']
    name = reference['score_name']
    entry['scores'][name] = record['scores'][name] = 2.5
    reference['value'] = puw.get_value(
        puw.quantity(2.5, 'kcal/mol'), to_unit='kJ/mol', value_type=float
    )
    reference['unit'] = 'kJ/mol'
    before = deepcopy(record)
    with puw.context(standard_units=['pm', 'fs', 'kJ/mol']):
        policy = puw.configure.report()
        assert dmt.audit_pose(record)['status'] == 'consistent'
        assert puw.configure.report() == policy
    assert record == before


def test_reference_report_is_detached_and_does_not_request_external_work(
    record, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Reference audit attempted external work.')

    for name in ('get', 'convert', 'select', 'extract', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    original_import = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name.split('.')[0] in (
            'molsysmt',
            'vina',
            'molsysviewer',
            'rdkit',
            'openmm',
        ):
            forbidden()
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded)
    monkeypatch.setattr(builtins, 'open', forbidden)
    before = deepcopy(record)
    report = dmt.audit_pose(record)
    assert report == dmt.audit_pose(record)
    assert (
        record == before and json.loads(json.dumps(report, allow_nan=False)) == report
    )
    report['checks'][0]['status'] = 'changed'
    assert dmt.audit_pose(record)['checks'][0]['status'] != 'changed'


def test_reference_declaration_does_not_relax_comparison_contexts(record):
    first = dmt.DockingPose.from_dict(record)
    other = deepcopy(record)
    other['metadata']['score_definitions']['vina']['context']['partner_sha256'] = (
        '0' * 64
    )
    result = dmt.DockingResult([first, dmt.DockingPose.from_dict(other)])
    with pytest.raises(ArgumentError):
        result.rank_by('vina')
