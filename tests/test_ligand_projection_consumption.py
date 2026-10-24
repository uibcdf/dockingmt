"""Native ligand reduction owns chemistry; DockingMT retains docking accounting."""

from math import fsum

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molecular_fixtures import declared_methanol
from test_named_partial_charges import METHANOL, atom_charges

import dockingmt as dmt
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING


@pytest.fixture
def source():
    return msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(declared_methanol(), **CHARGE),
        **TYPING,
    )


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_preparation_consumes_native_projection_and_derived_molecular_values(
    source, length_unit, monkeypatch
):
    before = snapshot(source)
    mechanics = detached_record(source.molecular_mechanics.to_dict())
    original_charges = atom_charges(source).astype(float)
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
        pytest.fail('Projection must not select or calculate a new parameter model.')

    monkeypatch.setattr(msm.build, 'merge_nonpolar_hydrogens', observed)
    for name in (
        'add_missing_hydrogens',
        'assign_partial_charges',
        'assign_autodock_atom_types',
    ):
        monkeypatch.setattr(msm.build, name, forbidden)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        prepared = dmt.prepare_ligand(source, selection='all')
        assert puw.configure.report() == policy
    assert len(calls) == 1
    expected = [
        fsum(original_charges[[0, 2, 3, 4]]),
        original_charges[1],
        original_charges[5],
    ]
    np.testing.assert_allclose(prepared.charges, expected, rtol=0, atol=1e-12)
    np.testing.assert_allclose(
        atom_charges(prepared.source_molsys).astype(float), expected, rtol=0, atol=1e-12
    )
    reconstructed = prepared.to_molecular_system()
    np.testing.assert_allclose(
        atom_charges(reconstructed).astype(float), expected, rtol=0, atol=1e-12
    )
    assert prepared.metadata['retained_atom_indices'] == [0, 1, 5]
    assert prepared.metadata['omitted_hydrogen_indices'] == [2, 3, 4]
    assert prepared.atom_types == ['C', 'OA', 'HD']
    assert msm.get(
        prepared.source_molsys, selection=[0], n_explicit_hydrogens=True
    ) == [3]
    assert msm.get(
        prepared.source_molsys, selection=[0], n_implicit_hydrogens=True
    ) == [0]
    assert msm.get(
        prepared.source_molsys, selection=[0], allows_implicit_hydrogens=True
    ) == [False]
    projection = prepared.metadata['molecular_projection']
    assert projection['schema'] == 'molsysmt.atom_projection@1'
    assert projection['output_to_source_atom_indices'] == [0, 1, 5]
    assert projection['source_to_output_atom_indices'] == [0, 1, -1, -1, -1, 2]
    assert projection['merged_source_atom_pairs'] == [[2, 0], [3, 0], [4, 0]]
    assert projection['charge_unit'] == 'elementary_charge'
    assert projection['output_total_charge'] == pytest.approx(
        projection['selected_total_charge'],
        abs=projection['charge_conservation_tolerance'],
    )
    derived = prepared.metadata['projected_partial_charge_assignment']
    assert derived['status'] == 'derived'
    assert derived['method'] == 'nonpolar_hydrogen_charge_aggregation'
    assert (
        derived['source_assignment'] == prepared.metadata['partial_charge_assignment']
    )
    assert prepared.metadata['projected_atom_type_assignment']['status'] == 'derived'
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'
    assert [
        float(line[70:76])
        for line in prepared.to_pdbqt().splitlines()
        if line.startswith('ATOM')
    ] == [0.190, -0.400, 0.210]
    assert snapshot(source) == before
    assert detached_record(source.molecular_mechanics.to_dict()) == mechanics
    # Public return reports and preparation evidence must not share mutable JSON.
    calls[0]['report']['output_to_source_atom_indices'][0] = 999
    assert projection['output_to_source_atom_indices'] == [0, 1, 5]


def test_projection_failure_propagates_without_a_local_transform(source, monkeypatch):
    before = snapshot(source)
    mechanics = detached_record(source.molecular_mechanics.to_dict())
    failure = RuntimeError('controlled public projection refusal')

    def refuse(*args, **kwargs):
        raise failure

    monkeypatch.setattr(msm.build, 'merge_nonpolar_hydrogens', refuse)
    with pytest.raises(RuntimeError) as raised:
        dmt.prepare_ligand(source, selection='all')
    assert raised.value is failure
    assert snapshot(source) == before
    assert detached_record(source.molecular_mechanics.to_dict()) == mechanics


def test_receptor_is_a_separate_migration(source, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('This slice does not migrate receptor projection.')

    monkeypatch.setattr(msm.build, 'merge_nonpolar_hydrogens', forbidden)
    prepared = dmt.prepare_receptor(source, selection='all')
    assert prepared.n_atoms == 3
    assert 'molecular_projection' not in prepared.metadata


def test_unassessed_virtual_inventory_is_not_repaired_or_assumed_zero(monkeypatch):
    raw = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(
            msm.convert(METHANOL, to_form='molsysmt.MolSys'), **CHARGE
        ),
        **TYPING,
    )
    before = snapshot(raw)
    mechanics = detached_record(raw.molecular_mechanics.to_dict())
    assert msm.physchem.get_hydrogen_inventory(raw)['status'] == 'unassessed'

    def forbidden(*args, **kwargs):
        pytest.fail('No unrequested inventory repair or parameter calculation.')

    for name in (
        'add_missing_hydrogens',
        'assign_partial_charges',
        'assign_autodock_atom_types',
    ):
        monkeypatch.setattr(msm.build, name, forbidden)
    with pytest.raises(
        msm.StructuralInconsistencyError, match='known virtual explicit H'
    ):
        dmt.prepare_ligand(raw, selection='all')
    assert snapshot(raw) == before
    assert detached_record(raw.molecular_mechanics.to_dict()) == mechanics


@pytest.mark.parametrize('allow_provisional', [False, True])
def test_unassessed_inventory_rejects_before_engine_even_with_opt_in(
    allow_provisional, monkeypatch
):
    import vina
    from test_engines import MINIMAL_REC_PDBQT

    raw = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(
            msm.convert(METHANOL, to_form='molsysmt.MolSys'), **CHARGE
        ),
        **TYPING,
    )
    problem = dmt.DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=raw,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
    )
    before = snapshot(raw)

    def forbidden(*args, **kwargs):
        pytest.fail('Unassessed inventory must reject before engine construction.')

    monkeypatch.setattr(vina, 'Vina', forbidden)
    with pytest.raises(
        msm.StructuralInconsistencyError, match='known virtual explicit H'
    ):
        dmt.dock(
            problem,
            dmt.VinaProtocol(cpu=1, allow_provisional_preparation=allow_provisional),
        )
    assert snapshot(raw) == before
