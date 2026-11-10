"""Finite shared test factories relocated from tests/test_molecular_delegation.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

import pyunitwizard as puw

from dockingmt.preparation import PreparedLigand, PreparedReceptor


def _manual_prepared(kind):
    arguments = dict(
        state_id='manual',
        atom_names=['C1', 'C1', 'O1'],
        group_names=['LIG'] * 3,
        group_ids=[7] * 3,
        coordinates=puw.quantity(
            [[0.123456789, 0, 0], [0.2, 0.123456789, 0], [0, 0.2, 0.123456789]],
            'nm',
        ),
        atom_types=['C', 'A', 'OA'],
        charges=[0.123456789, -0.234567891, 0.111111102],
    )
    return (
        PreparedLigand(group_name='LIG', **arguments)
        if kind == 'ligand'
        else PreparedReceptor(**arguments)
    )
