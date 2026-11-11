"""Finite shared test factories relocated from tests/test_ligand_preparation_stages.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

import molsysmt as msm
import pyunitwizard as puw
from molsysmt.native import Structures

HYDROGEN = {'mode': 'fixed_chemical_state', 'pH': None, 'engine': 'RDKit'}


CHARGE = {'method': 'gasteiger_marsili'}


def methanol_source():
    # Public MolSysMT conversion owns chemistry; declared synthetic coordinates
    # are supplied through its native Structures/composition APIs. No RDKit API.
    native = msm.convert(
        msm.convert('smiles:CO', to_form='rdkit.Mol'), to_form='molsysmt.MolSys'
    )
    pose = Structures(coordinates=puw.quantity([[[0, 0, 0], [1.4, 0, 0]]], 'angstrom'))
    return msm.convert([native, pose], to_form='molsysmt.MolSys')
