"""Source-free reconstruction applies the known axis through MolSysMT (#49)."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bmt_test_support.flexible_reconstruction_fixtures import (
    _manual as _manual,
)
from bmt_test_support.pdbqt_fixtures import MINIMAL_REC_PDBQT
from bmt_test_support.qualify_chemical_templates import detached_record, snapshot
from bmt_test_support.qualify_named_types import CHARGE, TYPING, explicit_source


@pytest.mark.parametrize('nested', [False, True])
@pytest.mark.parametrize('length_unit', ['nm', 'pm'])
def test_source_free_flexible_reconstruction_delegates_and_preserves_actual_values(
    nested, length_unit, monkeypatch
):
    prepared = _manual(nested)
    before = deepcopy(prepared.to_dict())
    coordinates = puw.get_value(prepared.coordinates, to_unit='nm').copy()
    permute = msm.permute_atoms
    convert = msm.convert
    calls, converted = [], []

    def observed_convert(item, **kwargs):
        if not isinstance(item, str):
            return convert(item, **kwargs)
        assert isinstance(item, str) and item.startswith('pdbqt_text:')
        assert kwargs == {
            'to_form': 'molsysmt.MolSys',
            'discard_torsion_tree': True,
        }
        result = convert(item, **kwargs)
        converted.append((result, snapshot(result)))
        return result

    def observed_permute(item, **kwargs):
        expected = [0, 1, 2, 3, 4, 5] if nested else [5, 4, 0, 1, 2, 3]
        assert kwargs == {'atom_indices': expected}
        calls.append(item)
        return permute(item, **kwargs)

    monkeypatch.setattr(msm, 'convert', observed_convert)
    monkeypatch.setattr(msm, 'permute_atoms', observed_permute)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        native = prepared.to_molecular_system()
        assert puw.configure.report() == policy
        assert len(converted) == 1
        assert snapshot(converted[0][0]) == converted[0][1]
    assert len(calls) == 1 and len(converted) == 1
    assert calls[0] is converted[0][0]
    assert native is not converted[0][0]
    assert list(msm.get(native, element='atom', atom_name=True)) == prepared.atom_names
    assert (
        list(msm.get(native, element='atom', atom_ff_type=True)) == prepared.atom_types
    )
    assert list(msm.get(native, element='atom', atom_type=True)) == [
        'C',
        'O',
        'N',
        'C',
        'Cl',
        'H',
    ]
    expected_ids = (
        ['1', '2', '3', '4', '5', '6'] if nested else ['6', '5', '1', '2', '3', '4']
    )
    assert list(msm.get(native, element='atom', atom_id=True)) == expected_ids
    assert (
        list(msm.get(native, element='atom', group_name=True)) == prepared.group_names
    )
    assert list(msm.get(native, element='atom', group_id=True)) == ['7'] * 6
    np.testing.assert_allclose(
        puw.get_value(msm.get(native, coordinates=True), to_unit='nm')[0],
        coordinates,
        atol=1e-15,
        rtol=0,
    )
    np.testing.assert_allclose(
        np.asarray(msm.get(native, element='atom', partial_charge=True), dtype=float),
        prepared.charges,
        atol=1e-15,
        rtol=0,
    )
    assert not msm.has_attribute(native, 'bond_order')
    assert native.molecular_mechanics.partial_charge_assignment is None
    assert prepared.source_molsys is None
    assert prepared.to_dict() == before
    np.testing.assert_array_equal(
        puw.get_value(prepared.coordinates, to_unit='nm'), coordinates
    )


def test_permutation_failure_propagates_without_local_reconstruction(monkeypatch):
    prepared = _manual()
    before = deepcopy(prepared.to_dict())
    error = RuntimeError('controlled native permutation refusal')

    def refuse(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm, 'permute_atoms', refuse)
    with pytest.raises(RuntimeError) as caught:
        prepared.to_molecular_system()
    assert caught.value is error
    assert prepared.to_dict() == before


def test_conversion_failure_propagates_before_permutation(monkeypatch):
    error = RuntimeError('controlled public conversion refusal')

    def refuse(*args, **kwargs):
        raise error

    def forbidden(*args, **kwargs):
        pytest.fail('Permutation cannot precede successful public conversion.')

    monkeypatch.setattr(msm, 'convert', refuse)
    monkeypatch.setattr(msm, 'permute_atoms', forbidden)
    with pytest.raises(RuntimeError) as caught:
        _manual().to_molecular_system()
    assert caught.value is error


def _prepared():
    return bmt.prepare_ligand(
        msm.build.assign_autodock_atom_types(
            msm.build.assign_partial_charges(explicit_source('CCCCCC'), **CHARGE),
            **TYPING,
        ),
        selection='all',
        active_torsion_bonds=[(1, 2)],
    )


def test_source_backed_flexible_reconstruction_keeps_native_copy_route(monkeypatch):
    prepared = _prepared()
    before = snapshot(prepared.source_molsys)

    def forbidden(*args, **kwargs):
        pytest.fail(
            'Native source-backed reconstruction does not need conversion/order.'
        )

    with monkeypatch.context() as scope:
        scope.setattr(msm, 'convert', forbidden)
        scope.setattr(msm, 'permute_atoms', forbidden)
        result = prepared.to_molecular_system()
    assert snapshot(prepared.source_molsys) == before
    assert snapshot(result) == before
    assert result is not prepared.source_molsys


def test_actual_vina_pose_reconstructs_source_free_prepared_axis():
    prepared = _prepared()
    prepared.source_molsys = None
    before = detached_record(prepared.to_dict())
    problem = bmt.DockingProblem(
        receptor='pdbqt_text:' + MINIMAL_REC_PDBQT,
        partner=prepared,
        search_domain=bmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'),
            puw.quantity([16, 16, 16], 'angstrom'),
        ),
    )
    result = bmt.dock(
        problem,
        bmt.VinaProtocol(
            cpu=1,
            seed=17,
            exhaustiveness=1,
            n_poses=1,
            allow_provisional_preparation=True,
        ),
    )
    assert len(result.poses) == 1
    pose = result.poses[0]
    native = pose.to_molecular_system(prepared)
    xyz = puw.get_value(msm.get(native, coordinates=True), to_unit='angstrom')[0]
    np.testing.assert_allclose(
        xyz[prepared.pdbqt_atom_indices],
        puw.get_value(pose.coordinates, to_unit='angstrom'),
        atol=1e-10,
        rtol=0,
    )
    assert (
        list(msm.get(native, element='atom', atom_ff_type=True)) == prepared.atom_types
    )
    np.testing.assert_allclose(
        np.asarray(msm.get(native, element='atom', partial_charge=True), dtype=float),
        prepared.charges,
        atol=1e-15,
        rtol=0,
    )
    assert not msm.has_attribute(native, 'bond_order')
    assert detached_record(prepared.to_dict()) == before
