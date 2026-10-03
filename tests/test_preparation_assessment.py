"""Public preparation inspection preserves the provisional/unassessed boundary."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
from argdigest.core.errors import UnknownArgumentError

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError


@pytest.fixture(params=['ligand', 'receptor'])
def prepared(request):
    # No geometry is needed for declaration inspection. A zero charge can be
    # explicitly supplied and is not itself evidence of placeholder chemistry.
    common = dict(
        state_id='declared-state',
        atom_names=['C1'],
        coordinates=None,
        atom_types=['C'],
        charges=[0.0],
    )
    if request.param == 'ligand':
        return dmt.PreparedLigand(group_name='LIG', **common)
    return dmt.PreparedReceptor(group_names=['LIG'], group_ids=[1], **common)


@pytest.mark.parametrize(
    'metadata,codes',
    [
        ({}, []),
        (
            {'charge_source': 'source_partial_charge', 'atom_type_source': 'external'},
            [],
        ),
        ({'charge_source': 'zero_placeholder'}, ['zero_placeholder_charges']),
        (
            {'atom_type_source': 'element_aromaticity_heuristic'},
            ['heuristic_atom_types'],
        ),
        (
            {'charge_source': 'zero_placeholder', 'atom_type_source': 'heuristic'},
            ['zero_placeholder_charges', 'heuristic_atom_types'],
        ),
    ],
)
def test_declared_sources_classify_preparation_without_certifying_it(
    prepared, metadata, codes
):
    prepared.metadata.update(metadata)
    report = dmt.assess_preparation(prepared)
    assert report['assessment'] == ('provisional' if codes else 'unassessed')
    assert report['provisional_reason_codes'] == codes
    assert report['evidence'] == {
        key: metadata.get(key) for key in ('charge_source', 'atom_type_source')
    }
    assert report['scope'] == 'declared_preparation_metadata'
    assert report['schema_version'] == '1.0'
    assert json.loads(json.dumps(report)) == report
    assert prepared.coordinates is None
    assert prepared.charges == [0.0]
    assert prepared.metadata == metadata


def test_assessment_detaches_only_bounded_evidence(prepared):
    prepared.metadata = {
        'charge_source': 'zero_placeholder',
        'atom_type_source': 'heuristic',
        'source_chemistry': {'large_payload': object()},
    }
    report = dmt.assess_preparation(prepared)
    report['evidence']['charge_source'] = 'edited'
    report['provisional_reasons'].clear()
    prepared.metadata['charge_source'] = 'source_partial_charge'
    new_report = dmt.assess_preparation(prepared)
    assert new_report['provisional_reason_codes'] == ['heuristic_atom_types']
    assert len(new_report['provisional_reasons']) == 1
    assert 'source_chemistry' not in new_report['evidence']
    assert json.loads(json.dumps(new_report)) == new_report


@pytest.mark.parametrize(
    'metadata', [None, [], {'charge_source': 0}, {'atom_type_source': ['heuristic']}]
)
def test_mutated_malformed_metadata_fails_with_local_diagnostic(prepared, metadata):
    prepared.metadata = metadata
    with pytest.raises(ArgumentError) as caught:
        dmt.assess_preparation(prepared)
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == 'prepared'


def test_external_inputs_stay_unassessed_without_io(tmp_path):
    class ExternalRenderer:
        metadata = {'charge_source': 'zero_placeholder'}

        def to_pdbqt(self):
            pytest.fail('Assessment must not invoke an external renderer')

    reports = [
        dmt.assess_preparation(value)
        for value in (
            'pdbqt_text:ROOT\nENDROOT\nTORSDOF 0\n',
            tmp_path / 'absent.pdbqt',
            ExternalRenderer(),
        )
    ]
    assert reports[0] == reports[1] == reports[2]
    assert reports[0]['assessment'] == 'unassessed'
    assert reports[0]['evidence'] == {'charge_source': None, 'atom_type_source': None}
    assert not (tmp_path / 'absent.pdbqt').exists()


@pytest.mark.parametrize(
    'value', [None, object(), {'charge_source': 'zero_placeholder'}]
)
def test_unsupported_inputs_are_not_silently_unassessed(value):
    with pytest.raises(ArgumentError) as caught:
        dmt.assess_preparation(value)
    assert caught.value.extra['arg_name'] == 'prepared'


def test_assessment_rejects_unknown_keywords():
    with pytest.raises(UnknownArgumentError):
        dmt.assess_preparation('external.pdbqt', prepare=True)


def test_assessment_works_in_fresh_process_without_optional_engine_or_viewer():
    script = """
import importlib.abc
import sys
class BlockOptional(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('vina', 'molsysviewer'):
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, BlockOptional())
import dockingmt as dmt
ligand = dmt.PreparedLigand(
    'test', ['C1'], 'LIG', None, ['C'], [0],
    metadata={'charge_source': 'zero_placeholder'},
)
report = dmt.assess_preparation(ligand)
assert report['provisional_reason_codes'] == ['zero_placeholder_charges']
assert 'vina' not in sys.modules and 'molsysviewer' not in sys.modules
print(report['assessment'])
"""
    completed = subprocess.run(
        [sys.executable, '-c', script],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == 'provisional'
