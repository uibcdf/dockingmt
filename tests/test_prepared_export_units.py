"""Readonly prepared export must survive caller unit changes without copying."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bmt_test_support.qualify_chemical_templates import snapshot
from bmt_test_support.qualify_named_types import CHARGE, TYPING, explicit_source
from bmt_test_support.resource_fixtures import UnavailableResource


@pytest.mark.parametrize('prepare', [bmt.prepare_ligand, bmt.prepare_receptor])
@pytest.mark.parametrize('preparation_unit', ['nm', 'angstrom', 'pm'])
@pytest.mark.parametrize('export_unit', ['nm', 'angstrom', 'pm'])
def test_readonly_export_and_one_ulp_edits_follow_actual_prepared_values(
    prepare, preparation_unit, export_unit
):
    with puw.context(standard_units=[preparation_unit, 'fs', 'coulomb', 'kJ/mol']):
        source = msm.build.assign_autodock_atom_types(
            msm.build.assign_partial_charges(explicit_source('CO'), **CHARGE), **TYPING
        )
        prepared = prepare(source, selection='all')
    native = prepared.source_molsys
    original = snapshot(native)
    record = deepcopy(prepared.to_dict())
    native.unavailable_resource = UnavailableResource()
    with puw.context(standard_units=[export_unit, 'ps', 'e', 'kcal/mol']):
        policy = puw.configure.report()
        assert 'ATOM' in prepared.to_pdbqt()
        assert puw.configure.report() == policy
    assert prepared.to_dict() == record and snapshot(native) == original

    # A real edit of one representable float must still require an independent
    # native copy. Approximate coordinate equality would hide this edit.
    coordinates = puw.get_value(prepared.coordinates).copy()
    index = np.flatnonzero(coordinates)[0]
    coordinates.flat[index] = np.nextafter(coordinates.flat[index], np.inf)
    prepared.coordinates = puw.quantity(coordinates, puw.get_unit(prepared.coordinates))
    with puw.context(standard_units=[export_unit, 'ps', 'e', 'kcal/mol']):
        policy = puw.configure.report()
        with pytest.raises(RuntimeError, match='test resource cannot be copied'):
            prepared.to_pdbqt()
        assert puw.configure.report() == policy
    assert snapshot(native) == original


@pytest.mark.parametrize('prepare', [bmt.prepare_ligand, bmt.prepare_receptor])
def test_native_coordinate_read_failure_keeps_original_exception(prepare, monkeypatch):
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source('CO'), **CHARGE), **TYPING
    )
    prepared = prepare(source, selection='all')
    original = deepcopy(prepared.to_dict())
    failure = MemoryError('native prepared-coordinate read failure')

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(
        type(prepared.source_molsys.structures), 'get_coordinates', fail
    )
    with puw.context(standard_units=['angstrom', 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        with pytest.raises(MemoryError) as caught:
            prepared.to_pdbqt()
        assert caught.value is failure and puw.configure.report() == policy
    assert prepared.to_dict() == original
