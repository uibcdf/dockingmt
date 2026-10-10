"""Consumer requirements for retiring the prepared PDBQT writers (#49).

Exercise the supported serializer separately from the still-pending molecular
projection (#223). These controls do not provide a production projection bridge.
"""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_flexible_ligand import _ligand
from test_named_partial_charges import METHANOL, atom_charges
from vina import Vina

from devtools.qualify_named_types import TYPING
from dockingmt import prepare_ligand, prepare_receptor


def _atoms(payload):
    # Inspect actual fixed columns independently of the native reader.
    return [line for line in payload.splitlines() if line.startswith('ATOM')]


@pytest.fixture
def assigned_methanol():
    source = msm.convert(METHANOL, to_form='molsysmt.MolSys')
    return msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(source, method='gasteiger_marsili'),
        **TYPING,
    )


@pytest.mark.parametrize('prepare', [prepare_ligand, prepare_receptor])
@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_native_writer_requires_prepared_values_after_h_projection(
    assigned_methanol, prepare, length_unit, tmp_path
):
    source = assigned_methanol
    original_charges = atom_charges(source).astype(float)
    original_assignment = deepcopy(source.molecular_mechanics.partial_charge_assignment)
    original_types = deepcopy(source.molecular_mechanics.atom_type_assignment)
    prepared = prepare(source, selection='all')
    assert prepared.n_atoms == 3
    assert prepared.atom_types == ['C', 'OA', 'HD']
    assert prepared.charges == pytest.approx(
        [0.19000057917, -0.39963024356, 0.20962966439], abs=1e-10
    )
    assert sum(prepared.charges) == pytest.approx(sum(original_charges), abs=1e-12)
    assert {
        (transfer['omitted_source_atom_index'], transfer['recipient_source_atom_index'])
        for transfer in prepared.metadata['charge_projection']['transfers']
    } == {(2, 0), (3, 0), (4, 0)}
    # A serializer is not a united-atom preparation operation: all six explicit
    # input atoms survive. Passing the source directly is not this consumer's
    # three-atom export, even though both payloads parse successfully.
    full = msm.convert(source, to_form='string:pdbqt_text', typing_scheme='autodock4')
    assert len(_atoms(full)) == 6
    assert sum(line[77:].strip() == 'H' for line in _atoms(full)) == 3

    native = msm.copy(prepared.source_molsys)
    retained_charges = atom_charges(native).astype(float)
    # The current saved source is an extraction, not the charge-aggregated
    # molecular output requested from #223. Conservation alone cannot replace
    # atom-resolved values and transfer recipients.
    np.testing.assert_allclose(retained_charges, original_charges[[0, 1, 5]])
    assert retained_charges[0] != pytest.approx(prepared.charges[0])
    coordinates = puw.convert(prepared.coordinates, to_unit=length_unit)
    msm.set(
        native,
        element='atom',
        atom_id=[1, 2, 3],
        coordinates=puw.quantity(
            np.expand_dims(puw.get_value(coordinates), 0), length_unit
        ),
        partial_charge=puw.quantity(prepared.charges, 'elementary_charge'),
    )
    tree = None
    if prepare is prepare_ligand:
        tree = {
            'schema_version': 'molsysmt.pdbqt-torsion-tree@1',
            'atom_ids': ['1', '2', '3'],
            'fragment_atom_indices': [0, 1, 2],
            'fragment_offsets': [0, 3],
            'branch_atom_pairs': np.empty((0, 2), dtype=int),
            'branch_fragment_pairs': np.empty((0, 2), dtype=int),
            'root_fragment_index': 0,
            'torsdof': 0,
        }
    with puw.context(standard_units=['pm', 'coulomb']):
        payload = msm.convert(
            native,
            to_form='string:pdbqt_text',
            typing_scheme='autodock4',
            torsion_tree=tree,
        ).removeprefix('pdbqt_text:')
    atoms = _atoms(payload)
    assert [int(line[6:11]) for line in atoms] == [1, 2, 3]
    assert [line[77:].strip() for line in atoms] == prepared.atom_types
    assert [float(line[70:76]) for line in atoms] == [0.190, -0.400, 0.210]
    written_coordinates = [
        [float(line[i : i + 8]) for i in (30, 38, 46)] for line in atoms
    ]
    np.testing.assert_allclose(
        written_coordinates,
        puw.get_value(prepared.coordinates, to_unit='angstrom'),
        atol=0.000501,
        rtol=0,
    )
    engine = Vina(cpu=1, verbosity=0)
    if tree is None:
        path = tmp_path / 'receptor.pdbqt'
        path.write_text(payload)
        engine.set_receptor(str(path))
    else:
        engine.set_ligand_from_string(payload)
    # Setting derived values deliberately removes the native calculation report;
    # it must not present the transform as a fresh Gasteiger calculation.
    assert native.molecular_mechanics.partial_charge_assignment is None
    assert 'REMARK MOLSYSMT_PARTIAL_CHARGES' not in payload
    np.testing.assert_equal(
        source.molecular_mechanics.partial_charge_assignment, original_assignment
    )
    np.testing.assert_equal(
        source.molecular_mechanics.atom_type_assignment, original_types
    )
    np.testing.assert_array_equal(
        atom_charges(source),
        original_charges,
    )
    np.testing.assert_array_equal(
        atom_charges(prepared.source_molsys),
        retained_charges,
    )


def test_native_writer_preserves_declared_flexible_prepared_axis():
    prepared = prepare_ligand(
        _ligand('CCCCCC'), selection='all', active_torsion_bonds=[(1, 2)]
    )
    assert prepared.pdbqt_atom_indices == [2, 3, 4, 5, 1, 0]
    native = msm.copy(prepared.source_molsys)
    before_ids = msm.get(native, element='atom', atom_id=True)
    # This fixture declares a known tree/serial axis explicitly; it neither
    # discovers correspondence nor adds a consumer molecular reorder operation.
    msm.set(native, element='atom', atom_id=[6, 5, 1, 2, 3, 4])
    msm.set(native, element='atom', partial_charge=puw.quantity(prepared.charges, 'e'))
    tree = {
        'schema_version': 'molsysmt.pdbqt-torsion-tree@1',
        'atom_ids': ['6', '5', '1', '2', '3', '4'],
        'fragment_atom_indices': [2, 3, 4, 5, 1, 0],
        'fragment_offsets': [0, 4, 6],
        'branch_atom_pairs': [[2, 1]],
        'branch_fragment_pairs': [[0, 1]],
        'root_fragment_index': 0,
        'torsdof': 1,
    }
    payload = msm.convert(
        native,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        torsion_tree=tree,
    ).removeprefix('pdbqt_text:')
    atoms = _atoms(payload)
    assert [int(line[6:11]) for line in atoms] == [1, 2, 3, 4, 5, 6]
    assert [line[12:16].strip() for line in atoms] == [
        prepared.atom_names[i] for i in prepared.pdbqt_atom_indices
    ]
    assert [line for line in payload.splitlines() if 'BRANCH' in line] == [
        'BRANCH 1 5',
        'ENDBRANCH 1 5',
    ]
    assert payload.endswith('TORSDOF 1\n')
    Vina(cpu=1, verbosity=0).set_ligand_from_string(payload)
    assert msm.get(prepared.source_molsys, element='atom', atom_id=True) == before_ids
    # RDKit's native source has no groups. The serializer preserves that absence;
    # it does not invent DockingMT's explicit LIG/1 presentation metadata.
    assert all(line[17:26].strip() == '' for line in atoms)
    assert prepared.group_names == ['LIG'] * 6
