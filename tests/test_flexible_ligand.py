import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import VinaProtocol
from dockingmt.core.search_domain import BoxRegion
from dockingmt.engines.vina import VinaBackend
from dockingmt.preparation import prepare_ligand


def _ligand(smiles):
    from rdkit import Chem
    from rdkit.Chem import AllChem

    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    assert AllChem.EmbedMolecule(molecule, randomSeed=7) == 0
    return msm.convert(molecule, to_form='molsysmt.MolSys')


def test_explicit_torsion_writes_one_valid_branch_and_tracks_atom_order():
    ligand = prepare_ligand(
        _ligand('CCCCCC'), selection='all', active_torsion_bonds=[(1, 2)]
    )

    assert ligand.torsion_dof == 1
    assert ligand.pdbqt_atom_indices == [2, 3, 4, 5, 1, 0]
    assert ligand.metadata['active_torsion_bonds'] == [[1, 2]]
    assert ligand.metadata['torsion_policy'] == 'explicit_selected_bonds'
    records = ligand.to_pdbqt().splitlines()
    assert sum(line.startswith('ATOM') for line in records) == 6
    assert sum(line.startswith('BRANCH') for line in records) == 1
    assert sum(line.startswith('ENDBRANCH') for line in records) == 1
    assert records[-1] == 'TORSDOF 1'
    assert ligand.to_dict()['pdbqt_atom_indices'] == ligand.pdbqt_atom_indices


@pytest.mark.parametrize(
    ('smiles', 'bond', 'reason'),
    [
        ('C1CCCCC1', (0, 1), 'ring'),
        ('C=CC', (0, 1), 'single bond order'),
        ('CC(=O)NCC', (1, 3), 'amide C-N'),
        ('CCCC', (0, 1), 'terminal heavy-atom side'),
    ],
)
def test_nonrotatable_bond_is_rejected(smiles, bond, reason):
    with pytest.raises(ArgumentError, match=reason):
        prepare_ligand(_ligand(smiles), selection='all', active_torsion_bonds=[bond])


def test_vina_protocol_records_selected_bonds_and_rejects_invalid_shape():
    protocol = VinaProtocol(active_torsion_bonds=[(1, 2)])
    assert 'flexible_ligand' in protocol.required_capabilities
    assert protocol.parameters['active_torsion_bonds'] == [[1, 2]]
    assert VinaProtocol.from_dict(protocol.to_dict()).active_torsion_bonds == [(1, 2)]
    with pytest.raises(ArgumentError, match='integer atom indices'):
        VinaProtocol(active_torsion_bonds=[(True, 2)])


def test_vina_accepts_flexible_ligand_and_pose_reconstructs_source_identity():
    pytest.importorskip('vina')
    source = _ligand('CCCCCC')
    receptor = (
        'ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00     0.000 N\n'
        'ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00  0.00     0.000 C\n'
        'ATOM      3  C   ALA A   1       2.009   1.428   0.000  1.00  0.00     0.000 C\n'
        'ATOM      4  O   ALA A   1       1.246   2.392   0.000  1.00  0.00     0.000 OA\n'
    )
    problem = DockingProblem(
        receptor=receptor,
        partner=source,
        search_domain=BoxRegion(
            center=puw.quantity([0, 0, 0], 'angstrom'),
            size=puw.quantity([20, 20, 20], 'angstrom'),
        ),
    )
    protocol = VinaProtocol(
        exhaustiveness=1,
        n_poses=1,
        seed=17,
        cpu=1,
        active_torsion_bonds=[(1, 2)],
        allow_provisional_preparation=True,
    )

    with pytest.raises(ArgumentError, match='heuristic AutoDock atom types'):
        VinaBackend().dock(
            problem,
            VinaProtocol(active_torsion_bonds=[(1, 2)], cpu=1),
        )

    result = VinaBackend().dock(problem, protocol)

    assert len(result.poses) == 1
    pose = result.poses[0]
    assert pose.metadata['prepared_atom_indices'] == [2, 3, 4, 5, 1, 0]
    assert result.provenance['preparation']['partner']['metadata'][
        'active_torsion_bonds'
    ] == [[1, 2]]
    restored = pose.to_molecular_system(source)
    restored_coordinates = puw.get_value(
        msm.get(restored, element='atom', coordinates=True)[0], to_unit='angstrom'
    )
    pose_coordinates = puw.get_value(pose.coordinates, to_unit='angstrom')
    for pose_index, source_index in enumerate(pose.metadata['selected_atom_indices']):
        np.testing.assert_allclose(
            restored_coordinates[source_index], pose_coordinates[pose_index], atol=1e-3
        )

    prepared = prepare_ligand(source, selection='all', active_torsion_bonds=[(1, 2)])
    prepared_problem = DockingProblem(
        receptor=receptor,
        partner=prepared,
        search_domain=problem.search_domain,
    )
    prepared_result = VinaBackend().dock(
        prepared_problem,
        VinaProtocol(
            exhaustiveness=1,
            n_poses=1,
            seed=17,
            cpu=1,
            allow_provisional_preparation=True,
        ),
    )
    assert len(prepared_result.poses) == 1
    assert (
        msm.get(
            prepared_result.poses[0].to_molecular_system(prepared),
            element='system',
            n_atoms=True,
        )
        == 6
    )
