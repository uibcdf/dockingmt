"""Receive prepared native values without claiming legacy writer compatibility."""

import hashlib
import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError
from vina import Vina

import dockingmt as dmt
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING, explicit_source


@pytest.fixture(params=['rigid', 'one-cut', 'nested'])
def export_case(request):
    """Finite declared docking policies; no molecular correspondence discovery."""
    policy = request.param
    source = explicit_source('CO' if policy == 'rigid' else 'CCCCCC')
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(source, **CHARGE), **TYPING
    )
    cuts = {'rigid': [], 'one-cut': [(1, 2)], 'nested': [(1, 2), (3, 4)]}[policy]
    prepared = dmt.prepare_ligand(source, selection='all', active_torsion_bonds=cuts)
    native = msm.copy(prepared.source_molsys)
    before = snapshot(native)
    assignment = detached_record(native.molecular_mechanics.to_dict())
    order = prepared.pdbqt_atom_indices
    serials = [order.index(atom) + 1 for atom in range(prepared.n_atoms)]
    # Serial numbering is this fixture's explicit output policy. Public setters
    # preserve chemistry/attribution; the source object is not changed.
    msm.set(native, element='atom', atom_id=serials)
    expected_order = {
        'rigid': [0, 1, 2],
        'one-cut': [2, 3, 4, 5, 1, 0],
        'nested': [0, 1, 2, 3, 4, 5],
    }[policy]
    assert order == expected_order
    tree = {
        'schema_version': 'molsysmt.pdbqt-torsion-tree@1',
        'atom_ids': [str(value) for value in serials],
        'fragment_atom_indices': order,
        'fragment_offsets': {
            'rigid': [0, 3],
            'one-cut': [0, 4, 6],
            'nested': [0, 2, 4, 6],
        }[policy],
        'branch_atom_pairs': {
            'rigid': np.empty((0, 2), dtype=int),
            'one-cut': [[2, 1]],
            'nested': [[1, 2], [3, 4]],
        }[policy],
        'branch_fragment_pairs': {
            'rigid': np.empty((0, 2), dtype=int),
            'one-cut': [[0, 1]],
            'nested': [[0, 1], [1, 2]],
        }[policy],
        'root_fragment_index': 0,
        'torsdof': len(cuts),
    }
    assert detached_record(native.molecular_mechanics.to_dict()) == assignment
    return prepared, native, tree, before


def _export(native, tree):
    text, mapping = msm.convert(
        native,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        torsion_tree=tree,
        return_atom_map=True,
    )
    return text.removeprefix('pdbqt_text:'), mapping


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_actual_prepared_values_export_with_bound_map_and_declared_tree(
    export_case, length_unit
):
    prepared, native, tree, original = export_case
    before = snapshot(native)
    mechanics = detached_record(native.molecular_mechanics.to_dict())
    charge_assignment = detached_record(
        native.molecular_mechanics.partial_charge_assignment
    )
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        payload, mapping = _export(native, tree)
        assert puw.configure.report() == policy
    assert mapping['payload_sha256'] == hashlib.sha256(payload.encode()).hexdigest()
    order = prepared.pdbqt_atom_indices
    assert list(mapping['output_to_source_atom_indices']) == order
    forward = list(mapping['source_to_output_atom_indices'])
    assert [forward[atom] for atom in order] == list(range(prepared.n_atoms))
    atoms = [line for line in payload.splitlines() if line.startswith('ATOM')]
    assert [int(line[6:11]) for line in atoms] == list(range(1, prepared.n_atoms + 1))
    assert [line[12:16].strip() for line in atoms] == [
        prepared.atom_names[i] for i in order
    ]
    assert [line[77:].strip() for line in atoms] == [
        prepared.atom_types[i] for i in order
    ]
    expected_xyz = puw.get_value(prepared.coordinates, to_unit='angstrom')[order]
    actual_xyz = [[float(line[i : i + 8]) for i in (30, 38, 46)] for line in atoms]
    np.testing.assert_allclose(actual_xyz, expected_xyz, atol=0.000501, rtol=0)
    assert [float(line[70:76]) for line in atoms] == [
        float(f'{prepared.charges[i]:.3f}') for i in order
    ]
    assert mapping['charge_unit'] == 'elementary_charge'
    np.testing.assert_array_equal(
        mapping['partial_charge_before_rounding'],
        np.asarray(prepared.charges)[order],
    )
    assert payload.endswith(f'TORSDOF {prepared.torsion_dof}\n')
    assert sum(line.startswith('BRANCH ') for line in payload.splitlines()) == (
        prepared.torsion_dof
    )
    assert charge_assignment['status'] == 'derived'
    assert charge_assignment == prepared.metadata['projected_partial_charge_assignment']
    Vina(cpu=1, verbosity=0).set_ligand_from_string(payload)
    assert snapshot(native) == before
    assert snapshot(prepared.source_molsys) == original
    assert detached_record(native.molecular_mechanics.to_dict()) == mechanics
    # A source without hierarchy stays without hierarchy. DockingMT's LIG/A/1
    # presentation is a separate, unresolved output-policy choice, not chemistry.
    assert msm.get(native, n_groups=True) == 0
    assert all(line[17:26].strip() == '' for line in atoms)
    assert prepared.group_names == ['LIG'] * prepared.n_atoms
    # Public maps remain usable as detached finite JSON, not mutable live state.
    restored = json.loads(json.dumps(detached_record(mapping), allow_nan=False))
    assert restored['payload_sha256'] == mapping['payload_sha256']


def test_caller_remarks_cannot_reuse_the_native_payload_identity(export_case):
    prepared, native, tree, _ = export_case
    payload, mapping = _export(native, tree)
    before = deepcopy(mapping)
    remarks = [
        line for line in prepared.to_pdbqt().splitlines() if line.startswith('REMARK ')
    ]
    assert any(line.startswith('REMARK DOCKINGMT_PARTIAL_CHARGES ') for line in remarks)
    assert any(line.startswith('REMARK DOCKINGMT_ATOM_TYPES ') for line in remarks)
    decorated = '\n'.join([*remarks, payload])
    assert hashlib.sha256(decorated.encode()).hexdigest() != mapping['payload_sha256']
    assert detached_record(mapping) == detached_record(before)
    # This observation is not a new completed map, reader refusal, or wire API.
    # Runtime export keeps its existing route until the provider-owned output
    # contract includes the requested presentation/remarks or policy changes.


@pytest.mark.parametrize('name', ['', 'ABCDE'])
def test_provider_rejects_unrepresentable_names_without_mutating_prepared_source(name):
    source = explicit_source('CO')
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(source, **CHARGE), **TYPING
    )
    prepared = dmt.prepare_ligand(source, selection='all')
    before = snapshot(prepared.source_molsys)
    native = msm.copy(prepared.source_molsys)
    msm.set(native, atom_id=[1, 2, 3])
    msm.set(native, selection=[0], atom_name=name)
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
    with pytest.raises(FormatError):
        _export(native, tree)
    assert snapshot(prepared.source_molsys) == before
