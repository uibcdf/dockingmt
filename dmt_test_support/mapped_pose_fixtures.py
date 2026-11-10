"""Finite shared test factories relocated from tests/test_known_source_pose_consumption.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

import molsysmt as msm
import numpy as np

from dmt_test_support.qualify_named_types import CHARGE, TYPING, explicit_source


def _tree(source, flexible=False):
    """Declare this fixture's ROOT/cut policy using the public writer schema."""
    n_atoms = msm.get(source, n_atoms=True)
    if flexible:
        assert n_atoms == 6
    return {
        'schema_version': 'molsysmt.pdbqt-torsion-tree@1',
        'atom_ids': msm.get(source, element='atom', atom_id=True),
        'fragment_atom_indices': [2, 3, 4, 5, 1, 0]
        if flexible
        else list(reversed(range(n_atoms))),
        'fragment_offsets': [0, 4, 6] if flexible else [0, n_atoms],
        'branch_atom_pairs': [[2, 1]] if flexible else np.empty((0, 2), dtype=int),
        'branch_fragment_pairs': [[0, 1]] if flexible else np.empty((0, 2), dtype=int),
        'root_fragment_index': 0,
        'torsdof': int(flexible),
    }


def _export(source, tree):
    return msm.convert(
        source,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        torsion_tree=tree,
        return_atom_map=True,
    )


def _case(smiles):
    source = explicit_source(smiles)
    msm.set(source, atom_id=list(range(11, 11 + msm.get(source, n_atoms=True))))
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(source, **CHARGE), **TYPING
    )
    projected = msm.build.merge_nonpolar_hydrogens(
        source, typing_scheme='autodock4', return_report=True
    )
    reduced = projected['molecular_system']
    tree = _tree(reduced, flexible=smiles == 'CCCCCC')
    text, mapping = _export(reduced, tree)
    return source, reduced, projected['report'], text, mapping, tree
