"""Independent native materialization preserves unchanged canonical geometry."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bmt_test_support.qualify_chemical_templates import snapshot
from bmt_test_support.qualify_named_types import CHARGE, TYPING, explicit_source


def prepared_control(prepare):
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source('CCCCCC'), **CHARGE), **TYPING
    )
    options = (
        {'active_torsion_bonds': [(1, 2)]} if prepare is bmt.prepare_ligand else {}
    )
    return prepare(source, selection='all', **options)


@pytest.mark.parametrize('prepare', [bmt.prepare_ligand, bmt.prepare_receptor])
@pytest.mark.parametrize('preparation_unit', ['nm', 'angstrom', 'pm'])
@pytest.mark.parametrize('reconstruction_unit', ['nm', 'angstrom', 'pm'])
def test_native_copy_preserves_unchanged_bits_and_transports_explicit_edits(
    prepare, preparation_unit, reconstruction_unit, monkeypatch
):
    with puw.context(standard_units=[preparation_unit, 'fs', 'coulomb', 'kJ/mol']):
        prepared = prepared_control(prepare)
    source = prepared.source_molsys
    original = snapshot(source)
    record = deepcopy(prepared.to_dict())
    set_values = msm.set
    seen = []

    def recorded(system, **kwargs):
        seen.append((system, kwargs))
        return set_values(system, **kwargs)

    monkeypatch.setattr(msm, 'set', recorded)
    with puw.context(standard_units=[reconstruction_unit, 'ps', 'e', 'kcal/mol']):
        policy = puw.configure.report()
        returned = prepared.to_molecular_system()
        assert puw.configure.report() == policy
    assert returned is not source and snapshot(returned) == original
    assert seen == []
    assert snapshot(source) == original and prepared.to_dict() == record

    coordinates = puw.get_value(prepared.coordinates).copy()
    index = np.flatnonzero(coordinates)[0]
    coordinates.flat[index] = np.nextafter(coordinates.flat[index], np.inf)
    prepared.coordinates = puw.quantity(coordinates, puw.get_unit(prepared.coordinates))
    with puw.context(standard_units=[reconstruction_unit, 'ps', 'e', 'kcal/mol']):
        policy = puw.configure.report()
        edited = prepared.to_molecular_system()
        assert puw.configure.report() == policy
    assert edited is not source and edited is not returned
    assert len(seen) == 1 and seen[0][0] is edited
    np.testing.assert_array_equal(
        puw.get_value(seen[0][1]['coordinates'])[0], coordinates
    )
    np.testing.assert_array_equal(
        puw.get_value(edited.structures.get_coordinates(), to_unit='nm')[0],
        puw.get_value(prepared.coordinates, to_unit='nm'),
    )
    assert snapshot(source) == original and snapshot(returned) == original


@pytest.mark.parametrize('prepare', [bmt.prepare_ligand, bmt.prepare_receptor])
@pytest.mark.parametrize('operation', ['copy', 'read', 'set'])
def test_native_materialization_keeps_provider_failure_identity(
    prepare, operation, monkeypatch
):
    prepared = prepared_control(prepare)
    source = prepared.source_molsys
    original = snapshot(source)
    failure = MemoryError('native materialization ' + operation + ' failure')

    def fail(*args, **kwargs):
        raise failure

    if operation == 'read':
        monkeypatch.setattr(type(source.structures), 'get_coordinates', fail)
    else:
        if operation == 'set':
            prepared.coordinates = prepared.coordinates + puw.quantity(1, 'angstrom')
        monkeypatch.setattr(msm, operation, fail)
    with puw.context(standard_units=['angstrom', 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        with pytest.raises(MemoryError) as caught:
            prepared.to_molecular_system()
        assert caught.value is failure and puw.configure.report() == policy
    # The read-failure hook also affects snapshot(), so restore it first.
    monkeypatch.undo()
    assert snapshot(source) == original
