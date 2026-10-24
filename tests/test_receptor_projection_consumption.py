"""Receptor H reduction and actual native charges belong to MolSysMT (#49)."""

from math import fsum

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molecular_fixtures import declared_methanol
from test_engines import MINIMAL_LIG_PDBQT
from test_named_partial_charges import METHANOL, atom_charges

import dockingmt as dmt
from devtools.qualify_181l_receptor import prepare_case
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING


@pytest.fixture
def source():
    return msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(declared_methanol(), **CHARGE), **TYPING
    )


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_receptor_consumes_native_projection_and_actual_derived_values(
    source, length_unit, monkeypatch
):
    before = snapshot(source)
    mechanics = detached_record(source.molecular_mechanics.to_dict())
    original = atom_charges(source).astype(float)
    actual = msm.build.merge_nonpolar_hydrogens
    calls = []

    def observed(system, **kwargs):
        assert kwargs == {
            'typing_scheme': 'autodock4',
            'selection': 'all',
            'chemical_state': 'structure',
            'structure_indices': 0,
            'return_report': True,
        }
        result = actual(system, **kwargs)
        calls.append(result)
        return result

    def forbidden(*args, **kwargs):
        pytest.fail('H reduction must not choose or calculate a preparation model.')

    monkeypatch.setattr(msm.build, 'merge_nonpolar_hydrogens', observed)
    for name in (
        'add_missing_hydrogens',
        'assign_partial_charges',
        'assign_autodock_atom_types',
    ):
        monkeypatch.setattr(msm.build, name, forbidden)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        prepared = dmt.prepare_receptor(source, selection='all')
        assert puw.configure.report() == policy
    assert len(calls) == 1
    expected = [fsum(original[[0, 2, 3, 4]]), original[1], original[5]]
    np.testing.assert_allclose(prepared.charges, expected, rtol=0, atol=1e-12)
    np.testing.assert_allclose(
        atom_charges(prepared.source_molsys).astype(float), expected, rtol=0, atol=1e-12
    )
    np.testing.assert_allclose(
        atom_charges(prepared.to_molecular_system()).astype(float),
        expected,
        rtol=0,
        atol=1e-12,
    )
    assert prepared.atom_types == ['C', 'OA', 'HD']
    assert prepared.metadata['retained_atom_indices'] == [0, 1, 5]
    assert prepared.metadata['omitted_hydrogen_indices'] == [2, 3, 4]
    projection = prepared.metadata['molecular_projection']
    assert projection['schema'] == 'molsysmt.atom_projection@1'
    assert projection['output_to_source_atom_indices'] == [0, 1, 5]
    assert projection['source_to_output_atom_indices'] == [0, 1, -1, -1, -1, 2]
    assert projection['merged_source_atom_pairs'] == [[2, 0], [3, 0], [4, 0]]
    assert projection['charge_unit'] == 'elementary_charge'
    assert msm.get(
        prepared.source_molsys, selection=[0], n_explicit_hydrogens=True
    ) == [3]
    assert msm.get(
        prepared.source_molsys, selection=[0], n_implicit_hydrogens=True
    ) == [0]
    assert msm.get(
        prepared.source_molsys, selection=[0], allows_implicit_hydrogens=True
    ) == [False]
    derived = prepared.metadata['projected_partial_charge_assignment']
    assert derived['status'] == 'derived'
    assert derived['method'] == 'nonpolar_hydrogen_charge_aggregation'
    assert (
        derived['source_assignment'] == prepared.metadata['partial_charge_assignment']
    )
    assert prepared.metadata['projected_atom_type_assignment']['status'] == 'derived'
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'
    calls[0]['report']['output_to_source_atom_indices'][0] = 999
    assert projection['output_to_source_atom_indices'] == [0, 1, 5]
    assert snapshot(source) == before
    assert detached_record(source.molecular_mechanics.to_dict()) == mechanics


def test_receptor_projection_failure_propagates_without_local_fallback(
    source, monkeypatch
):
    before = snapshot(source)
    failure = RuntimeError('controlled public receptor projection refusal')

    def refuse(*args, **kwargs):
        raise failure

    monkeypatch.setattr(msm.build, 'merge_nonpolar_hydrogens', refuse)
    with pytest.raises(RuntimeError) as raised:
        dmt.prepare_receptor(source, selection='all')
    assert raised.value is failure
    assert snapshot(source) == before


def _unassessed():
    return msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(
            msm.convert(METHANOL, to_form='molsysmt.MolSys'), **CHARGE
        ),
        **TYPING,
    )


def test_receptor_unknown_inventory_is_not_assumed_zero_or_repaired():
    source = _unassessed()
    before = snapshot(source)
    assert msm.physchem.get_hydrogen_inventory(source)['status'] == 'unassessed'
    with pytest.raises(
        msm.StructuralInconsistencyError, match='known virtual explicit H'
    ):
        dmt.prepare_receptor(source, selection='all')
    assert snapshot(source) == before


@pytest.mark.parametrize('allow_provisional', [False, True])
def test_receptor_unknown_inventory_rejects_before_engine(
    allow_provisional, monkeypatch
):
    import vina

    source = _unassessed()
    before = snapshot(source)
    problem = dmt.DockingProblem(
        receptor=source,
        receptor_selection='all',
        partner='pdbqt_text:' + MINIMAL_LIG_PDBQT,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
    )

    def forbidden(*args, **kwargs):
        pytest.fail('Unassessed receptor inventory must reject before the engine.')

    monkeypatch.setattr(vina, 'Vina', forbidden)
    with pytest.raises(
        msm.StructuralInconsistencyError, match='known virtual explicit H'
    ):
        dmt.dock(
            problem,
            dmt.VinaProtocol(cpu=1, allow_provisional_preparation=allow_provisional),
        )
    assert snapshot(source) == before


def test_declared_181l_protein_consumes_actual_public_projection(monkeypatch):
    actual = msm.build.merge_nonpolar_hydrogens
    protein_calls = []

    def observed(source, **kwargs):
        n_atoms = msm.get(source, n_atoms=True)
        before = snapshot(source) if n_atoms == 2603 else None
        result = actual(source, **kwargs)
        if before is not None:
            assert snapshot(source) == before
            protein_calls.append(result)
        return result

    monkeypatch.setattr(msm.build, 'merge_nonpolar_hydrogens', observed)
    prepared, *_ = prepare_case()
    assert len(protein_calls) == 1
    assert prepared.n_atoms == 1615
    projection = prepared.metadata['molecular_projection']
    assert len(projection['merged_source_atom_pairs']) == 988
    assert len(projection['output_to_source_atom_indices']) == 1615
    assert projection['n_source_atoms'] == 2603
    assert fsum(prepared.charges) == pytest.approx(8, abs=1e-8)
    np.testing.assert_allclose(
        atom_charges(prepared.source_molsys).astype(float),
        prepared.charges,
        rtol=0,
        atol=1e-12,
    )
    assert (
        prepared.metadata['projected_partial_charge_assignment']['status'] == 'derived'
    )
    assert (
        prepared.metadata['projected_partial_charge_assignment']['source_assignment']
        == (prepared.metadata['partial_charge_assignment'])
    )
    assert dmt.assess_preparation(prepared)['assessment'] == 'unassessed'
