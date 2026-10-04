"""Explicit public provider stages and traceability across added ligand atoms."""

import json
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt.native import Structures
from test_engines import MINIMAL_REC_PDBQT

import dockingmt as dmt
from devtools.qualify_chemical_templates import load_181l_benzene, template_options
from dockingmt._private.smonitor import ArgumentError

HYDROGEN = {'mode': 'fixed_chemical_state', 'pH': None, 'engine': 'RDKit'}
CHARGE = {'method': 'gasteiger_marsili'}


def methanol_source():
    # Public MolSysMT conversion owns chemistry; declared synthetic coordinates
    # are supplied through its native Structures/composition APIs. No RDKit API.
    native = msm.convert(
        msm.convert('smiles:CO', to_form='rdkit.Mol'), to_form='molsysmt.MolSys'
    )
    pose = Structures(coordinates=puw.quantity([[[0, 0, 0], [1.4, 0, 0]]], 'angstrom'))
    return msm.convert([native, pose], to_form='molsysmt.MolSys')


def xyz(system):
    return puw.get_value(msm.get(system, coordinates=True), to_unit='angstrom')[0]


def test_polar_workflow_records_original_and_generated_identity_without_moving_source():
    source = methanol_source()
    before = xyz(source).copy()
    ids = list(msm.get(source, element='atom', atom_id=True))
    options = deepcopy(HYDROGEN)
    prepared = dmt.prepare_ligand(
        source, selection='all', hydrogen_options=options, charge_options=CHARGE
    )
    assert options == HYDROGEN
    assert msm.get(source, n_atoms=True) == 2
    assert not msm.has_attribute(source, 'partial_charge')
    np.testing.assert_array_equal(xyz(source), before)
    expanded = prepared.metadata['preparation_workflow']
    assert expanded['input_n_atoms'] == 2
    assert expanded['stages'] == ['hydrogen_addition', 'partial_charge_assignment']
    assert expanded['prepared_to_input_atom_indices'] == [0, 1, None]
    assert expanded['pdbqt_to_input_atom_indices'] == [0, 1, None]
    report = expanded['hydrogen_addition']
    assert report['schema'] == 'molsysmt.hydrogen_addition@1'
    assert report['n_added_hydrogens'] == 4
    assert report['atom_correspondence'] == [[0, 0], [1, 1]]
    assert report['parent_hydrogen_pairs'] == [[0, 2], [0, 3], [0, 4], [1, 5]]
    assert report['coordinate_evidence'] == 'generated_local_geometry'
    assert report['parameters']['optimize'] is False
    assert report['software'] and report['attribution']['items']
    assert report['dropped_attributes'] == []
    assert prepared.metadata['source_n_atoms'] == 6
    assert prepared.n_atoms == 3 and prepared.atom_types == ['C', 'OA', 'HD']
    assert (
        list(msm.get(prepared.source_molsys, element='atom', atom_id=True))[:2] == ids
    )
    np.testing.assert_array_equal(
        puw.get_value(prepared.coordinates, to_unit='angstrom')[:2], before
    )
    audit = dmt.audit_preparation_charges(prepared)
    assert audit['assessment'] == 'consistent'
    assert audit['partial_charge_assignment']['n_atoms'] == 6
    assert audit['total_charge'] == pytest.approx(0, abs=1e-12)
    assert dmt.assess_preparation(prepared)['provisional_reason_codes'] == [
        'heuristic_atom_types'
    ]
    json.dumps(prepared.to_dict(), allow_nan=False)


def test_public_stage_results_match_an_explicit_manual_pipeline_and_are_detached():
    source = methanol_source()
    hydrogenated = msm.build.add_missing_hydrogens(
        source, return_report=True, attribute_policy='strict', **HYDROGEN
    )
    assigned = msm.build.assign_partial_charges(
        hydrogenated['molecular_system'], **CHARGE
    )
    expected = dmt.prepare_ligand(assigned, selection='all')
    actual = dmt.prepare_ligand(
        source, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
    )
    assert actual.charges == expected.charges
    assert actual.to_pdbqt() == expected.to_pdbqt()
    assert (
        actual.metadata['charge_projection'] == expected.metadata['charge_projection']
    )
    raw = actual.to_dict()['metadata']['preparation_workflow']['hydrogen_addition']
    assert raw['software'] == hydrogenated['report']['software']
    assert raw['references'] == hydrogenated['report']['references']
    actual.metadata['preparation_workflow']['hydrogen_addition']['software'][
        'rdkit'
    ] = 'edited'
    assert hydrogenated['report']['software']['rdkit'] != 'edited'


def test_explicit_h_inventory_is_idempotent_and_existing_h_coordinates_are_preserved():
    source = msm.build.add_missing_hydrogens(
        methanol_source(), attribute_policy='strict', **HYDROGEN
    )
    before = xyz(source).copy()
    prepared = dmt.prepare_ligand(
        source, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
    )
    workflow = prepared.metadata['preparation_workflow']
    assert workflow['hydrogen_addition']['n_added_hydrogens'] == 0
    assert workflow['hydrogen_addition']['status'] == 'unchanged'
    assert workflow['prepared_to_input_atom_indices'] == [0, 1, 5]
    np.testing.assert_array_equal(
        puw.get_value(prepared.coordinates, to_unit='angstrom'), before[[0, 1, 5]]
    )
    np.testing.assert_array_equal(xyz(source), before)


def test_explicit_h_sdf_without_stored_inventory_is_not_silently_reinterpreted():
    source = msm.convert(
        Path(__file__).parent / 'data/charges/methanol.sdf', to_form='molsysmt.MolSys'
    )
    before = xyz(source).copy()
    with pytest.raises(
        msm.StructuralInconsistencyError, match='missing_stored_hydrogen_counts'
    ):
        dmt.prepare_ligand(
            source, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
        )
    np.testing.assert_array_equal(xyz(source), before)


def test_request_order_is_hydrogens_then_charges_and_default_preserves_legacy(
    monkeypatch,
):
    source = methanol_source()
    calls = []
    hydrogen = msm.build.add_missing_hydrogens
    charges = msm.build.assign_partial_charges

    def h(system, **kwargs):
        calls.append(('H', msm.get(system, n_atoms=True), kwargs))
        return hydrogen(system, **kwargs)

    def q(system, **kwargs):
        calls.append(('Q', msm.get(system, n_atoms=True), kwargs))
        return charges(system, **kwargs)

    monkeypatch.setattr(msm.build, 'add_missing_hydrogens', h)
    monkeypatch.setattr(msm.build, 'assign_partial_charges', q)
    legacy = dmt.prepare_ligand(source, selection='all')
    assert calls == [] and 'preparation_workflow' not in legacy.metadata
    dmt.prepare_ligand(
        source, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
    )
    assert [(stage, count) for stage, count, _ in calls] == [('H', 2), ('Q', 6)]
    assert calls[0][2]['attribute_policy'] == 'strict'
    assert calls[0][2]['return_report'] is True


def test_h_only_is_provisional_and_charge_only_retains_input_mapping():
    h_only = dmt.prepare_ligand(
        methanol_source(), selection='all', hydrogen_options=HYDROGEN
    )
    assert dmt.assess_preparation(h_only)['provisional_reason_codes'] == [
        'zero_placeholder_charges',
        'heuristic_atom_types',
    ]
    assert h_only.metadata['preparation_workflow']['charge_assignment_record'] is None
    source = msm.convert(
        Path(__file__).parent / 'data/charges/methanol.sdf', to_form='molsysmt.MolSys'
    )
    charge_only = dmt.prepare_ligand(source, selection='all', charge_options=CHARGE)
    assert charge_only.metadata['preparation_workflow']['hydrogen_addition'] is None
    assert charge_only.metadata['preparation_workflow'][
        'prepared_to_input_atom_indices'
    ] == [0, 1, 5]


@pytest.mark.parametrize(
    'options',
    [
        {'hydrogen_options': {}},
        {'hydrogen_options': {'engine': 'RDKit'}},
        {'hydrogen_options': {**HYDROGEN, 'pH': 7.4}},
        {'hydrogen_options': {**HYDROGEN, 'mode': 'pH'}},
        {'hydrogen_options': {**HYDROGEN, 'engine': ''}},
        {'hydrogen_options': {**HYDROGEN, 'skip_digestion': True}},
        {'hydrogen_options': {**HYDROGEN, 'return_report': False}},
        {'hydrogen_options': {**HYDROGEN, 'molecular_system': 'different'}},
        {'hydrogen_options': {**HYDROGEN, 1: 2}},
        {'charge_options': {}},
        {'charge_options': {'method': None}},
        {'charge_options': {**CHARGE, 'return_report': True}},
        {'hydrogen_options': True},
        {'charge_options': []},
    ],
)
def test_incomplete_choices_fail_before_molecular_conversion(options, monkeypatch):
    def forbid(*args, **kwargs):
        raise AssertionError('Do not perform molecular work before option admission.')

    monkeypatch.setattr(msm, 'convert', forbid)
    with pytest.raises(ArgumentError):
        dmt.prepare_ligand('input', **options)


@pytest.mark.parametrize(
    'stage,error_type',
    [('hydrogen', ImportError), ('hydrogen', RuntimeError), ('charges', RuntimeError)],
)
def test_provider_failure_identity_is_preserved_and_no_fallback_occurs(
    stage, error_type, monkeypatch
):
    source = methanol_source()
    before = xyz(source).copy()
    error = error_type('provider fixture failure')

    def fail(*args, **kwargs):
        raise error

    target = (
        'add_missing_hydrogens' if stage == 'hydrogen' else 'assign_partial_charges'
    )
    monkeypatch.setattr(msm.build, target, fail)
    with pytest.raises(error_type) as exc:
        dmt.prepare_ligand(
            source, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
        )
    assert exc.value is error
    np.testing.assert_array_equal(xyz(source), before)
    assert not msm.has_attribute(source, 'partial_charge')


def test_original_181l_declared_template_remains_rejected_for_missing_bond_aromaticity():
    source, template, _ = load_181l_benzene()
    options = template_options(
        template,
        np.column_stack((np.arange(6), np.arange(6))),
        identity='Explicit heavy-only benzene SMILES template',
        uri='smiles:c1ccccc1',
        hydrogen_policy='stored_counts',
    )
    applied = msm.physchem.apply_chemical_template(source, **options)[
        'molecular_system'
    ]
    before = xyz(applied).copy()
    with pytest.raises(msm.StructuralInconsistencyError, match='order and aromaticity'):
        dmt.prepare_ligand(
            applied,
            selection='all',
            hydrogen_options={**HYDROGEN, 'attribute_policy': 'intersection'},
            charge_options=CHARGE,
        )
    np.testing.assert_array_equal(xyz(applied), before)
    assert not msm.has_attribute(applied, 'partial_charge')


def test_nondefault_units_and_strict_attribute_loss():
    source = methanol_source()
    with puw.context(standard_units=['pm', 'fs', 'coulomb']):
        before = xyz(source).copy()
        prepared = dmt.prepare_ligand(
            source, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
        )
        np.testing.assert_array_equal(
            puw.get_value(prepared.coordinates, to_unit='angstrom')[:2], before
        )
        assert prepared.charges == pytest.approx(
            [0.19000057917, -0.39963024356, 0.20962966439], abs=1e-10
        )
    source.structures.b_factor = puw.quantity([[1.0, 2.0]], 'angstrom**2')
    with pytest.raises(msm.StructuralInconsistencyError, match='b_factor'):
        dmt.prepare_ligand(source, selection='all', hydrogen_options=HYDROGEN)
    allowed = dmt.prepare_ligand(
        source,
        selection='all',
        hydrogen_options={**HYDROGEN, 'attribute_policy': 'intersection'},
        charge_options=CHARGE,
    )
    assert allowed.metadata['preparation_workflow']['hydrogen_addition'][
        'dropped_attributes'
    ] == ['b_factor']
    assert source.structures.b_factor is not None


def test_real_vina_result_retains_stage_reports_without_lifting_typing_gate():
    prepared = dmt.prepare_ligand(
        methanol_source(),
        selection='all',
        hydrogen_options=HYDROGEN,
        charge_options=CHARGE,
    )
    problem = dmt.DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=prepared,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
    )
    with pytest.raises(ArgumentError, match='heuristic'):
        dmt.dock(problem, dmt.VinaProtocol(cpu=1))
    result = dmt.dock(
        problem,
        dmt.VinaProtocol(
            cpu=1,
            seed=17,
            n_poses=1,
            exhaustiveness=1,
            allow_provisional_preparation=True,
            capture_backend_inputs=True,
        ),
    )
    restored = dmt.DockingResult.from_dict(
        json.loads(json.dumps(result.to_dict(), allow_nan=False))
    )
    workflow = restored.provenance['preparation']['partner']['metadata'][
        'preparation_workflow'
    ]
    assert workflow == prepared.metadata['preparation_workflow']
    assert restored.provenance['preparation']['partner']['assessment'] == 'provisional'
    assert len(restored.poses) == 1
