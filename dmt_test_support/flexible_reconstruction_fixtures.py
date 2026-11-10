"""Finite shared test factories relocated from tests/test_flexible_reconstruction.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

import pyunitwizard as puw

import dockingmt as dmt
from dockingmt.preparation._temporary_torsions import Branch, TorsionTree


def _manual(nested=False):
    """Finite partial representation, with duplicate names and known traversal."""
    tree = (
        TorsionTree(
            (0, 1),
            (Branch(1, 2, (2, 3), (Branch(3, 4, (4, 5), ()),)),),
            (0, 1, 2, 3, 4, 5),
            ((1, 2), (3, 4)),
            {},
        )
        if nested
        else TorsionTree(
            (2, 3, 4, 5),
            (Branch(2, 1, (1, 0), ()),),
            (2, 3, 4, 5, 1, 0),
            ((1, 2),),
            {},
        )
    )
    return dmt.PreparedLigand(
        state_id='declared_partial_control',
        atom_names=['C1', 'O1', 'N1', 'C1', 'Cl23', 'H1'],
        group_name='LIG',
        group_names=['LIG'] * 6,
        group_ids=[7] * 6,
        coordinates=puw.quantity(
            [
                [0.123456789, 0, 0],
                [0.2, 0.123456789, 0],
                [0, 0.2, 0.123456789],
                [0.314159265, 0.1, 0],
                [-0.1, 0.271828182, 0.1],
                [0.2, 0.1, -0.161803399],
            ],
            'nm',
        ),
        atom_types=['C', 'OA', 'NA', 'A', 'Cl', 'HD'],
        charges=[0.123456789, -0.234567891, 0.111111102, -0.012345678, 0.02, -0.01],
        torsion_dof=len(tree.active_bonds),
        _torsion_tree=tree,
    )
