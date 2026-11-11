"""Finite shared test factories relocated from tests/test_named_partial_charges.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

METHANOL = Path(__file__).resolve().parents[1] / 'tests/data/charges/methanol.sdf'


def atom_charges(system):
    values = msm.get(system, partial_charge=True)
    if puw.is_quantity(values):
        values = puw.get_value(values, to_unit='elementary_charge')
    return np.asarray(values)
