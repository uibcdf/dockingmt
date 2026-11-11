"""Finite shared test factories relocated from tests/test_flexible_ligand.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

import molsysmt as msm


def _ligand(smiles):
    from rdkit import Chem
    from rdkit.Chem import AllChem

    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    assert AllChem.EmbedMolecule(molecule, randomSeed=7) == 0
    return msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(
            msm.convert(molecule, to_form='molsysmt.MolSys'),
            method='gasteiger_marsili',
        ),
        typing_scheme='autodock4',
        method='chemical_environment',
    )
