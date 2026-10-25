"""Receive completed preparation correspondence through MolSysMT (#49)."""

import json
from copy import deepcopy

import molsysmt as msm
import pytest
import pyunitwizard as puw
from molecular_fixtures import declared_methanol
from molsysmt.native import Structures
from test_ligand_preparation_stages import CHARGE, HYDROGEN, methanol_source

import dockingmt as dmt
from devtools.qualify_chemical_templates import snapshot
from devtools.qualify_named_types import TYPING


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_generated_h_lineage_consumes_real_reports_and_stays_detached(
    length_unit, monkeypatch
):
    source = methanol_source()
    before = snapshot(source)
    compose = msm.compose_atom_maps
    hydrogenate = msm.build.add_missing_hydrogens
    calls = []
    hydrogen_results = []

    def observed_hydrogens(*args, **kwargs):
        result = hydrogenate(*args, **kwargs)
        hydrogen_results.append(result)
        return result

    def observed(reports):
        inputs = deepcopy(reports)
        result = compose(reports)
        assert reports == inputs
        calls.append((reports, result))
        return result

    monkeypatch.setattr(msm, 'compose_atom_maps', observed)
    monkeypatch.setattr(msm.build, 'add_missing_hydrogens', observed_hydrogens)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb']):
        prepared = dmt.prepare_ligand(
            source,
            selection='all',
            hydrogen_options=HYDROGEN,
            charge_options=CHARGE,
            typing_options=TYPING,
        )
    assert len(calls) == 1
    reports, result = calls[0]
    workflow = prepared.metadata['preparation_workflow']
    assert reports == [
        workflow['hydrogen_addition'],
        prepared.metadata['molecular_projection'],
    ]
    mapped = workflow['atom_map']
    assert mapped['schema'] == 'molsysmt.atom_map@1'
    assert mapped['n_source_atoms'] == 2 and mapped['n_output_atoms'] == 3
    assert mapped['output_to_source_atom_indices'] == [0, 1, -1]
    assert mapped['source_to_output_atom_indices'] == [0, 1]
    assert mapped['source_to_representative_atom_indices'] == [0, 1]
    assert mapped['generated_output_atom_indices'] == [2]
    assert mapped['source_atom_status'] == ['retained', 'retained']
    assert [stage['origin_schema'] for stage in mapped['stages']] == [
        'molsysmt.hydrogen_addition@1',
        'molsysmt.atom_projection@1',
    ]
    assert mapped['stages'][0]['parent_atom_pairs'] == [[0, 2], [0, 3], [0, 4], [1, 5]]
    assert mapped['stages'][1]['merged_source_atom_pairs'] == [[2, 0], [3, 0], [4, 0]]
    assert mapped['stages'][1]['charge_unit'] == 'elementary_charge'
    assert mapped['stages'][0]['attribution'] == reports[0]['attribution']
    assert workflow['prepared_to_input_atom_indices'] == [0, 1, None]
    assert workflow['pdbqt_to_input_atom_indices'] == [0, 1, None]
    assert workflow['generated_atom_marker'] is None
    assert workflow['index_scope'] == 'selected_input_before_requested_stages'
    serialized = json.loads(json.dumps(prepared.to_dict(), allow_nan=False))
    assert serialized['metadata']['preparation_workflow']['atom_map'] == mapped
    assert snapshot(source) == before
    result['output_to_source_atom_indices'][0] = 999
    result['stages'][0]['parent_atom_pairs'][0, 0] = 999
    hydrogen_results[0]['report']['atom_correspondence'][0][0] = 999
    assert mapped['output_to_source_atom_indices'] == [0, 1, -1]
    assert mapped['stages'][0]['parent_atom_pairs'][0] == [0, 2]
    assert workflow['hydrogen_addition']['atom_correspondence'][0] == [0, 0]


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_no_h_stage_uses_projection_and_selected_input_axis(prepare, monkeypatch):
    source = msm.merge([declared_methanol(), declared_methanol()])
    before = snapshot(source)
    compose = msm.compose_atom_maps
    calls = []

    def observed(reports):
        calls.append(deepcopy(reports))
        return compose(reports)

    monkeypatch.setattr(msm, 'compose_atom_maps', observed)
    prepared = prepare(
        source,
        selection=list(range(6, 12)),
        charge_options=CHARGE,
        typing_options=TYPING,
    )
    assert calls == [[prepared.metadata['molecular_projection']]]
    workflow = prepared.metadata['preparation_workflow']
    assert workflow['input_n_atoms'] == 6
    assert workflow['hydrogen_addition'] is None
    mapped = workflow['atom_map']
    assert mapped['n_source_atoms'] == 6 and mapped['n_output_atoms'] == 3
    assert mapped['output_to_source_atom_indices'] == [0, 1, 5]
    assert mapped['source_to_output_atom_indices'] == [0, 1, -1, -1, -1, 2]
    assert mapped['source_to_representative_atom_indices'] == [0, 1, 0, 0, 0, 2]
    assert mapped['source_atom_status'] == [
        'retained',
        'retained',
        'merged',
        'merged',
        'merged',
        'retained',
    ]
    assert mapped['generated_output_atom_indices'] == []
    assert workflow['prepared_to_input_atom_indices'] == [0, 1, 5]
    assert workflow['pdbqt_to_input_atom_indices'] == [0, 1, 5]
    assert snapshot(source) == before


def test_flexible_legacy_order_does_not_fabricate_a_completed_export_map():
    heavy = msm.convert(
        msm.convert('smiles:CCCCCO', to_form='rdkit.Mol'), to_form='molsysmt.MolSys'
    )
    pose = Structures(
        coordinates=puw.quantity(
            [
                [
                    [0, 0, 0],
                    [1.4, 0, 0],
                    [2.2, 1.2, 0],
                    [3.6, 1.2, 0],
                    [4.4, 2.4, 0],
                    [5.8, 2.4, 0],
                ]
            ],
            'angstrom',
        )
    )
    source = msm.convert([heavy, pose], to_form='molsysmt.MolSys')
    before = snapshot(source)
    prepared = dmt.prepare_ligand(
        source,
        selection='all',
        hydrogen_options=HYDROGEN,
        charge_options=CHARGE,
        typing_options=TYPING,
        active_torsion_bonds=[(1, 2), (3, 4)],
    )
    workflow = prepared.metadata['preparation_workflow']
    mapped = workflow['atom_map']
    assert mapped['output_to_source_atom_indices'] == [0, 1, 2, 3, 4, 5, -1]
    assert workflow['prepared_to_input_atom_indices'] == [0, 1, 2, 3, 4, 5, None]
    assert prepared.pdbqt_atom_indices != list(range(7))
    assert workflow['pdbqt_to_input_atom_indices'] == [
        workflow['prepared_to_input_atom_indices'][i]
        for i in prepared.pdbqt_atom_indices
    ]
    assert workflow['pdbqt_to_input_atom_indices'] == [4, 5, None, 3, 2, 1, 0]
    assert len(mapped['stages']) == 2
    assert all(
        stage['origin_schema'] != 'molsysmt.atom_export@1' for stage in mapped['stages']
    )
    assert snapshot(source) == before


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_composition_failure_propagates_without_local_fallback(prepare, monkeypatch):
    source = declared_methanol()
    before = snapshot(source)
    error = RuntimeError('provider atom-map fixture refusal')

    def refuse(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm, 'compose_atom_maps', refuse)
    with pytest.raises(RuntimeError) as caught:
        prepare(source, selection='all', charge_options=CHARGE, typing_options=TYPING)
    assert caught.value is error
    assert snapshot(source) == before


def test_inconsistent_h_correspondence_is_rejected_by_provider(monkeypatch):
    hydrogenate = msm.build.add_missing_hydrogens

    def corrupt(*args, **kwargs):
        result = hydrogenate(*args, **kwargs)
        result['report']['atom_correspondence'][1][1] = 0
        return result

    monkeypatch.setattr(msm.build, 'add_missing_hydrogens', corrupt)
    with pytest.raises(
        msm.StructuralInconsistencyError, match='Creation correspondence'
    ):
        dmt.prepare_ligand(
            methanol_source(),
            selection='all',
            hydrogen_options=HYDROGEN,
            charge_options=CHARGE,
            typing_options=TYPING,
        )
