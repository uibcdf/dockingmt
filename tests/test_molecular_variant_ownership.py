"""Consumer ownership across public preparation, reconstruction and failed copies."""

from contextlib import nullcontext
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_named_partial_charges import METHANOL, atom_charges

import dockingmt as dmt
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING
from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.results import _molecular_atom_keys


@pytest.fixture(params=[False, True], ids=['default', 'pm-coulomb'])
def unit_policy(request):
    context = (
        puw.context(standard_units=['pm', 'fs', 'coulomb', 'kJ/mol'])
        if request.param
        else nullcontext()
    )
    with context:
        yield


@pytest.fixture
def source(unit_policy):
    original = msm.convert(METHANOL, to_form='molsysmt.MolSys')
    charged = msm.build.assign_partial_charges(original, **CHARGE)
    return msm.build.assign_autodock_atom_types(charged, **TYPING)


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_prepared_variants_keep_independent_molecular_domains(source, prepare):
    original = snapshot(source)
    original_mechanics = detached_record(source.molecular_mechanics.to_dict())
    first = prepare(source, selection='all')
    second = prepare(source, selection='all')
    first_record, second_record = deepcopy(first.to_dict()), deepcopy(second.to_dict())
    first_text, second_text = first.to_pdbqt(), second.to_pdbqt()
    first_source = snapshot(first.source_molsys)
    second_source = snapshot(second.source_molsys)
    native = first.to_molecular_system()
    sibling = second.to_molecular_system()
    sibling_before = snapshot(sibling)
    sibling_charges = atom_charges(sibling).copy()

    # Public setters edit the returned variant, never the stored preparation.
    coordinates = msm.get(native, coordinates=True)
    msm.set(native, coordinates=coordinates + puw.quantity(5, 'angstrom'))
    msm.set(native, partial_charge=puw.quantity([0.5] * first.n_atoms, 'e'))
    msm.set(native, selection=[0], formal_charge=1)
    assert snapshot(source) == original
    assert detached_record(source.molecular_mechanics.to_dict()) == original_mechanics
    assert snapshot(first.source_molsys) == first_source
    assert snapshot(second.source_molsys) == second_source
    assert snapshot(sibling) == sibling_before
    np.testing.assert_array_equal(atom_charges(sibling), sibling_charges)
    assert first.to_dict() == first_record and second.to_dict() == second_record
    assert first.to_pdbqt() == first_text and second.to_pdbqt() == second_text

    # Editing the original input cannot reach already prepared or returned systems.
    native_after = snapshot(native)
    native_charges = atom_charges(native).copy()
    msm.set(
        source,
        coordinates=msm.get(source, coordinates=True) + puw.quantity(9, 'angstrom'),
    )
    msm.set(
        source, partial_charge=puw.quantity([0.25] * msm.get(source, n_atoms=True), 'e')
    )
    msm.set(source, selection=[0], formal_charge=-1)
    assert snapshot(first.source_molsys) == first_source
    assert snapshot(second.source_molsys) == second_source
    assert snapshot(native) == native_after
    np.testing.assert_array_equal(atom_charges(native), native_charges)
    assert snapshot(sibling) == sibling_before
    assert first.to_pdbqt() == first_text and second.to_pdbqt() == second_text


def test_reconstructed_poses_are_independent_of_each_other_and_retained_result(source):
    prepared = dmt.prepare_ligand(source, selection='all')
    metadata = {
        'pose_atom_order': 'verified_pdbqt_order',
        'source_atom_keys': _molecular_atom_keys(prepared.source_molsys),
    }
    poses = [
        dmt.DockingPose(
            prepared.coordinates + puw.quantity(shift, 'angstrom'),
            scores={'control': float(shift)},
            rank=index + 1,
            metadata=metadata,
        )
        for index, shift in enumerate([0, 2])
    ]
    result = dmt.DockingResult(poses)
    original_result = result.to_dict()
    original_preparation = deepcopy(prepared.to_dict())
    original_source = snapshot(prepared.source_molsys)
    first, second = [pose.to_molecular_system(prepared) for pose in poses]
    second_before = snapshot(second)
    second_charges = atom_charges(second).copy()
    for pose, system in zip(poses, [first, second], strict=True):
        assert _molecular_atom_keys(system) == metadata['source_atom_keys']
        np.testing.assert_allclose(
            puw.get_value(msm.get(system, coordinates=True), to_unit='angstrom')[0],
            puw.get_value(pose.coordinates, to_unit='angstrom'),
            rtol=0,
            atol=1e-12,
        )
    msm.set(
        first,
        coordinates=msm.get(first, coordinates=True) + puw.quantity(4, 'angstrom'),
    )
    msm.set(first, partial_charge=puw.quantity([0.0] * prepared.n_atoms, 'e'))
    msm.set(first, selection=[0], formal_charge=1)
    assert snapshot(second) == second_before
    np.testing.assert_array_equal(atom_charges(second), second_charges)
    assert snapshot(prepared.source_molsys) == original_source
    assert prepared.to_dict() == original_preparation
    assert result.to_dict() == original_result

    # A source identity change must reject a new reconstruction, leaving old results.
    msm.set(prepared.source_molsys, selection=[0], atom_name='EDIT')
    with pytest.raises(ArgumentError, match='identities differ'):
        poses[0].to_molecular_system(prepared)
    assert snapshot(second) == second_before
    assert result.to_dict() == original_result


class UnavailableResource:
    def __deepcopy__(self, memo):
        raise RuntimeError('test resource cannot be copied')


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_failed_native_copy_does_not_publish_or_mutate_prepared_variants(
    source, prepare
):
    prepared = prepare(source, selection='all')
    prior = prepared.to_molecular_system()
    prior_before = snapshot(prior)
    prepared_before = deepcopy(prepared.to_dict())
    submitted_before = prepared.to_pdbqt()
    owned_before = snapshot(prepared.source_molsys)
    # Native extension data follows its own copy protocol. No resource reopening
    # or consumer fallback is permitted when the provider refuses the snapshot.
    prepared.source_molsys.unavailable_resource = UnavailableResource()
    with pytest.raises(RuntimeError, match='test resource cannot be copied'):
        prepared.to_molecular_system()
    assert snapshot(prepared.source_molsys) == owned_before
    assert prepared.to_dict() == prepared_before
    assert prepared.to_pdbqt() == submitted_before
    assert snapshot(prior) == prior_before
    msm.set(
        prepared.source_molsys,
        coordinates=msm.get(prepared.source_molsys, coordinates=True)
        + puw.quantity(1, 'angstrom'),
    )
    assert snapshot(prior) == prior_before
