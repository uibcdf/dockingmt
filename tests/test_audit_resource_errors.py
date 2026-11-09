"""Offline audit failures must distinguish resources from inconsistent data."""

import json
from copy import deepcopy
from pathlib import Path

import pytest
import pyunitwizard as puw

import dockingmt as dmt

DATA = Path(__file__).resolve().parents[1] / 'devguide/validation/data/audit'
CASES = (
    [
        pytest.param(kind, boundary, 'coordinate_units', id=f'{kind}-{boundary}')
        for kind in ('standalone', 'docking', 'scored_collection')
        for boundary in ('quantity', 'are_compatible', 'get_value')
    ]
    + [
        pytest.param(kind, 'protocol', 'scoring_protocol', id=f'{kind}-protocol')
        for kind in ('standalone', 'scored_collection')
    ]
    + [
        pytest.param(
            kind, boundary, 'reference_energy_quantity', id=f'{kind}-{boundary}'
        )
        for kind in ('standalone', 'scored_collection')
        for boundary in ('reference_quantity', 'reference_conversion')
    ]
)


def _control(kind, boundary):
    filename = (
        'minimal_vina_result.json' if kind == 'docking' else 'minimal_scored_pose.json'
    )
    record = json.loads((DATA / filename).read_text())
    if boundary.startswith('reference_'):
        # Synthetic declaration for error controls, not a new native observation.
        entry = record['metadata']['scoring_history'][0]
        name = entry['score_name'] + '.lig_intra_best_pose'
        entry['reference_energy'] = {
            'schema_version': '1.0',
            'policy': 'native_current_conformation',
            'score_name': name,
            'value': entry['scores'][name],
            'unit': 'kilocalorie/mole',
        }
        for name in entry['scores']:
            for definitions in (
                entry['score_definitions'],
                record['metadata']['score_definitions'],
            ):
                definitions[name]['context']['reference_energy_policy'] = (
                    'native_current_conformation'
                )
    if kind == 'scored_collection':
        record = dmt.DockingResult([dmt.DockingPose.from_dict(record)]).to_dict()
    return record, dmt.audit_pose if kind == 'standalone' else dmt.audit_result


def _inject(monkeypatch, boundary, failure):
    hits = []

    def fail_once():
        if not hits:
            hits.append(boundary)
            raise failure

    if boundary == 'protocol':
        original = dmt.VinaProtocol.from_dict

        def protocol(cls, record):
            fail_once()
            return original(record)

        monkeypatch.setattr(dmt.VinaProtocol, 'from_dict', classmethod(protocol))
    else:
        function = {
            'reference_quantity': 'quantity',
            'reference_conversion': 'get_value',
        }.get(boundary, boundary)
        original = getattr(puw, function)

        def provider(*args, **kwargs):
            selected = True
            if boundary == 'reference_quantity':
                selected = len(args) > 1 and args[1] == 'kilocalorie/mole'
            elif boundary == 'reference_conversion':
                selected = (
                    kwargs.get('to_unit') == 'kcal/mol'
                    and kwargs.get('value_type') is float
                )
            if selected:
                fail_once()
            return original(*args, **kwargs)

        monkeypatch.setattr(puw, function, provider)
    return hits


@pytest.mark.parametrize('kind,boundary,check', CASES)
@pytest.mark.parametrize(
    'error_type', [MemoryError, KeyboardInterrupt, SystemExit, ValueError]
)
def test_audit_resource_identity_and_ordinary_value_reports(
    monkeypatch, kind, boundary, check, error_type
):
    record, audit = _control(kind, boundary)
    before = deepcopy(record)
    clean_report = audit(record)
    assert clean_report['status'] == (
        'incomplete' if kind == 'scored_collection' else 'consistent'
    )
    failure = error_type('offline audit boundary control')
    with monkeypatch.context() as patch:
        hits = _inject(patch, boundary, failure)
        if error_type is ValueError:
            report = audit(record)
            assert report['status'] == 'inconsistent'
            assert any(
                row['check'] == check and row['status'] == 'inconsistent'
                for row in report['checks']
            )
        else:
            with pytest.raises(error_type) as caught:
                audit(record)
            assert caught.value is failure
            assert not isinstance(caught.value, dmt.exceptions.DockingMTException)
        assert hits == [boundary]
    assert record == before
    assert audit(record) == clean_report
