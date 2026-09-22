import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation import (
    PreparedLigand,
    PreparedReceptor,
    prepare_ligand,
    prepare_receptor,
)


def test_prepare_receptor_and_ligand_181l():
    pdb_path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(pdb_path, to_form='molsysmt.MolSys')

    rec = prepare_receptor(
        molsys, selection="molecule_type=='protein'", state_id='rec_181L'
    )
    assert isinstance(rec, PreparedReceptor)
    assert rec.state_id == 'rec_181L'
    assert rec.n_atoms > 1000
    assert msm.get_form(rec.source_molsys) == 'molsysmt.MolSys'
    assert (
        msm.get(rec.to_molecular_system(), element='system', n_atoms=True)
        == rec.n_atoms
    )
    assert 'ATOM' in rec.to_pdbqt()
    assert rec.to_dict()['schema_version'] == '1.0'

    lig = prepare_ligand(molsys, selection="group_name=='BNZ'", state_id='lig_BNZ')
    assert isinstance(lig, PreparedLigand)
    assert lig.state_id == 'lig_BNZ'
    assert lig.n_atoms == 6
    assert msm.get_form(lig.source_molsys) == 'molsysmt.MolSys'
    assert (
        msm.get(lig.to_molecular_system(), element='system', n_atoms=True)
        == lig.n_atoms
    )
    assert lig.group_name == 'BNZ'
    assert lig.metadata['source_chemistry'] == {
        'connectivity_completeness': ['partial'],
        'bond_order_available': False,
    }
    pdbqt = lig.to_pdbqt()
    assert 'ROOT' in pdbqt
    assert 'ENDROOT' in pdbqt
    assert 'TORSDOF' in pdbqt
    assert lig.to_dict()['schema_version'] == '1.0'


def test_prepare_empty_selection_raises():
    pdb_path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    with pytest.raises(ArgumentError) as exc:
        prepare_receptor(pdb_path, selection="group_name=='NONEXISTENT_RES'")
    assert 'selection' in str(exc.value)

    with pytest.raises(ArgumentError) as exc:
        prepare_ligand(pdb_path, selection="group_name=='NONEXISTENT_LIG'")
    assert 'selection' in str(exc.value)


def test_rdkit_ligand_without_groups_preserves_available_chemistry():
    rdkit = pytest.importorskip('rdkit')
    from rdkit import Chem
    from rdkit.Chem import AllChem

    assert rdkit is not None
    molecule = Chem.AddHs(Chem.MolFromSmiles('c1ccccc1'))
    assert AllChem.EmbedMolecule(molecule, randomSeed=7) == 0
    AllChem.ComputeGasteigerCharges(molecule)
    ligand = prepare_ligand(molecule, selection='all')

    assert ligand.group_name == 'LIG'
    assert ligand.n_atoms == 6
    assert ligand.atom_types == ['A'] * 6
    assert np.sum(ligand.charges) == pytest.approx(0.0, abs=1e-6)
    assert ligand.metadata['charge_source'] == 'source_partial_charge'
    assert ligand.metadata['merged_hydrogen_charges'] is True
    assert ligand.metadata['hydrogen_policy'] == 'retain_polar_merge_nonpolar'
    assert ligand.metadata['omitted_hydrogen_indices'] == list(range(6, 12))
    assert ligand.metadata['torsion_policy'] == 'rigid_only'
    assert ligand.metadata['atom_map_status'] == 'hydrogen_subset_mapped'
    assert ligand.metadata['source_chemistry'] == {
        'connectivity_completeness': ['complete'],
        'bond_order_available': True,
    }


def test_prepared_molsys_uses_current_coordinates():
    molsys = msm.convert(
        msm.systems['T4 lysozyme L99A']['181l.pdb'],
        to_form='molsysmt.MolSys',
    )
    ligand = prepare_ligand(molsys, selection="group_name=='BNZ'")
    receptor = prepare_receptor(molsys, selection="molecule_type=='protein'")
    for prepared in (ligand, receptor):
        old = np.asarray(puw.get_value(prepared.coordinates))
        prepared.coordinates = puw.quantity(
            old + 1.0, puw.get_unit(prepared.coordinates)
        )
        restored = msm.get(
            prepared.to_molecular_system(),
            element='atom',
            coordinates=True,
        )[0]
        np.testing.assert_allclose(
            puw.get_value(
                puw.convert(restored, to_unit=puw.get_unit(prepared.coordinates))
            ),
            old + 1.0,
        )


def test_manual_prepared_ligand_recovers_elements_from_autodock_types():
    ligand = PreparedLigand(
        state_id='manual',
        atom_names=['C1', 'O1'],
        group_name='LIG',
        coordinates=puw.quantity([[0.0, 0.0, 0.0], [0.1, 0.0, 0.0]], 'nm'),
        atom_types=['C', 'OA'],
        charges=[0.0, 0.0],
    )
    assert msm.get(ligand.to_molecular_system(), element='atom', atom_type=True) == [
        'C',
        'O',
    ]


def test_ligand_writer_rejects_torsion_count_without_branch_tree():
    path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    with pytest.raises(ArgumentError, match='ROOT/BRANCH tree'):
        prepare_ligand(path, selection="group_name=='BNZ'", torsion_dof=1)

    ligand = PreparedLigand(
        state_id='rigid',
        atom_names=['C1'],
        group_name='LIG',
        coordinates=puw.quantity([[0.0, 0.0, 0.0]], 'nm'),
        atom_types=['C'],
        charges=[0.0],
    )
    ligand.torsion_dof = 1
    with pytest.raises(ArgumentError, match='ROOT/BRANCH tree'):
        ligand.to_pdbqt()
