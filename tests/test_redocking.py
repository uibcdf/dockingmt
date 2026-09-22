import molsysmt as msm
import pytest
import pyunitwizard as puw

import dockingmt
from dockingmt import (
    BoxRegion,
    DockingProblem,
    DockingResult,
    VinaProtocol,
    dock,
    prepare_ligand,
    prepare_receptor,
)
from dockingmt.engines.vina import VinaBackend


def test_redocking_benchmark_181l():
    """Exercise the provisional 181L redocking path and its identity/RMSD contracts.

    This is an end-to-end software check, not scientific validation of C1/C2.
    It exercises:
    1. Extracts protein and ligand using MolSysMT.
    2. Prepares receptor and ligand states retaining atomic identities.
    3. Derives search domain from native crystallographic ligand with padding.
    4. Executes Vina docking calculation behind adapter boundaries.
    5. Normalizes candidate poses with plural named scores.
    6. Measures RMSD against the native crystallographic ligand using MolSysMT.
    """
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    pdb_path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(pdb_path, to_form='molsysmt.MolSys')

    # Native reference ligand for RMSD calculation
    native_benzene = msm.extract(molsys, selection="group_name=='BNZ'")

    # Gate C1: Preparation
    prepared_rec = prepare_receptor(
        molsys,
        selection="molecule_type=='protein'",
        state_id='181l_protein_state',
    )
    prepared_lig = prepare_ligand(
        molsys,
        selection="group_name=='BNZ'",
        state_id='181l_bnz_state',
    )

    assert prepared_rec.n_atoms > 1000
    assert prepared_lig.n_atoms == 6

    # Search domain derived from native ligand selection
    search_domain = BoxRegion.from_selection(
        molsys,
        selection="group_name=='BNZ'",
        padding=puw.quantity(8.0, 'angstrom'),
    )

    # Gate C2: Problem & Protocol
    problem = DockingProblem(
        receptor=prepared_rec,
        partner=prepared_lig,
        search_domain=search_domain,
        metadata={
            'system': 'T4 lysozyme L99A',
            'pdb_id': '181L',
            'ligand_name': 'BNZ',
        },
    )

    protocol = VinaProtocol(
        exhaustiveness=8,
        n_poses=5,
        energy_range=puw.quantity(3.0, 'kcal/mol'),
        seed=42,
        allow_provisional_preparation=True,
    )

    # Execution
    result = dock(problem, protocol=protocol, backend='vina')

    # Validations on DockingResult
    assert isinstance(result, DockingResult)
    assert len(result) > 0

    top_pose = result.top_pose
    assert top_pose is not None
    assert top_pose.rank == 1
    assert 'vina' in top_pose.scores
    assert top_pose.scores['vina'] < 0.0  # favorable binding affinity
    assert top_pose.partner_state_id == '181l_bnz_state'
    assert top_pose.receptor_state_id == '181l_protein_state'

    # Gate C2: Calculate RMSD against native ligand
    rmsds = result.get_rmsds(reference=native_benzene)
    assert len(rmsds) == len(result)

    top_rmsd_ang = puw.get_value(puw.convert(rmsds[0], to_unit='angstrom'))
    # Regression bound for this provisional test case, not a validation threshold.
    assert top_rmsd_ang < 2.5

    # Provenance and serialization
    assert result.provenance['backend'] == 'vina'
    d = result.to_dict()
    assert d['schema_version'] == '1.0'
    reconstructed = DockingResult.from_dict(d)
    assert len(reconstructed) == len(result)
    assert reconstructed.top_pose.scores['vina'] == top_pose.scores['vina']

    # Gate C6: MolSysViewer integration
    view = dockingmt.view(result=result, reference=native_benzene)
    assert view.shapes.contains('dockingmt:search_domain')
    assert view.player.n_structures == len(result)
    assert view.addons.dockingmt.active_pose_rank == 1
    assert 'reference_ligand' in [r.tag for r in view.regions.values()]


def test_direct_molsysmt_input_reaches_vina():
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    molsys = msm.convert(path, to_form='molsysmt.MolSys')
    search_domain = BoxRegion.from_selection(
        molsys,
        selection="group_name=='BNZ'",
        padding=puw.quantity(8.0, 'angstrom'),
    )
    problem = DockingProblem(
        receptor=path,
        partner=molsys,
        search_domain=search_domain,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
        metadata={
            'receptor_state_id': '181l_protein',
            'partner_state_id': '181l_bnz',
        },
    )

    result = dock(
        problem,
        protocol=VinaProtocol(
            exhaustiveness=1,
            n_poses=1,
            seed=42,
            cpu=1,
            allow_provisional_preparation=True,
        ),
        backend=backend,
    )

    assert len(result) > 0
    assert result.problem is problem
    assert result.top_pose.receptor_state_id == '181l_protein'
    assert result.top_pose.partner_state_id == '181l_bnz'
    assert result.provenance['preparation']['receptor']['mode'] == 'automatic'
    assert result.provenance['preparation']['partner']['mode'] == 'automatic'
    assert result.provenance['preparation']['partner']['assessment'] == 'provisional'
    assert (
        result.provenance['preparation']['partner']['metadata']['hydrogen_policy']
        == 'retain_polar_merge_nonpolar'
    )
    assert (
        result.provenance['preparation']['partner']['metadata']['torsion_policy']
        == 'rigid_only'
    )
    assert len(result.provenance['backend_artifacts']['partner']['sha256']) == 64
    assert (
        result.provenance['protocol']['parameters']['allow_provisional_preparation']
        is True
    )
    assert result.top_pose.metadata['pose_atom_order'] == 'verified_pdbqt_order'
    assert result.problem_info['molecular_inputs']['partner']['atom_indices'] == [
        1299,
        1300,
        1301,
        1302,
        1303,
        1304,
    ]
