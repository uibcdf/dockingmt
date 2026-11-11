"""Finite shared test factories relocated from tests/test_native_ligand_export_receiving.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

import molsysmt as msm
import numpy as np
import pytest

import bindingmt as bmt
from bmt_test_support.qualify_chemical_templates import detached_record, snapshot
from bmt_test_support.qualify_named_types import CHARGE, TYPING, explicit_source


@pytest.fixture(params=['rigid', 'one-cut', 'nested'])
def export_case(request):
    """Finite declared docking policies; no molecular correspondence discovery."""
    policy = request.param
    source = explicit_source('CO' if policy == 'rigid' else 'CCCCCC')
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(source, **CHARGE), **TYPING
    )
    cuts = {'rigid': [], 'one-cut': [(1, 2)], 'nested': [(1, 2), (3, 4)]}[policy]
    prepared = bmt.prepare_ligand(source, selection='all', active_torsion_bonds=cuts)
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
