import molsysmt as msm
import pytest

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
    assert 'ATOM' in rec.to_pdbqt()
    assert rec.to_dict()['schema_version'] == '1.0'

    lig = prepare_ligand(molsys, selection="group_name=='BNZ'", state_id='lig_BNZ')
    assert isinstance(lig, PreparedLigand)
    assert lig.state_id == 'lig_BNZ'
    assert lig.n_atoms == 6
    assert lig.group_name == 'BNZ'
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
