import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt import DockingPose, DockingResult
from dockingmt._private.smonitor import ArgumentError


def test_docking_pose_creation_and_attributes():
    coords = puw.quantity([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]], 'nm')
    scores = {'vina': -8.2, 'vinardo': -6.5}

    pose = DockingPose(
        coordinates=coords,
        scores=scores,
        rank=1,
        pose_id='pose_001',
        partner_state_id='ligand_neutral',
        receptor_state_id='receptor_conformation_A',
        metadata={'cluster_id': 0},
    )

    assert pose.n_atoms == 2
    assert pose.rank == 1
    assert pose.scores['vina'] == -8.2
    assert pose.partner_state_id == 'ligand_neutral'
    assert pose.receptor_state_id == 'receptor_conformation_A'
    assert pose.metadata['cluster_id'] == 0


def test_docking_pose_dimensional_validation():
    # Dimensionless coordinates
    with pytest.raises(
        ArgumentError, match="'coordinates' must be a physical quantity"
    ):
        DockingPose(coordinates=[[0.0, 0.0, 0.0]])

    # Incompatible unit
    with pytest.raises(ArgumentError, match='not compatible with length'):
        DockingPose(coordinates=puw.quantity([[0.0, 0.0, 0.0]], 'kJ/mol'))


def test_docking_result_collection_and_ranking():
    coords = puw.quantity([[0.0, 0.0, 0.0]], 'nm')

    p1 = DockingPose(
        coordinates=coords, scores={'vina': -6.5, 'gnina': 0.8}, pose_id='p1'
    )
    p2 = DockingPose(
        coordinates=coords, scores={'vina': -9.1, 'gnina': 0.4}, pose_id='p2'
    )
    p3 = DockingPose(
        coordinates=coords, scores={'vina': -7.8, 'gnina': 0.95}, pose_id='p3'
    )

    result = DockingResult(
        poses=[p1, p2, p3],
        problem_info={'receptor': 'protein_1'},
        provenance={'backend': 'mock_engine'},
    )

    assert len(result) == 3
    assert [p.pose_id for p in result] == ['p1', 'p2', 'p3']

    # Rank by Vina score (ascending=True: more negative is better)
    ranked_vina = result.rank_by('vina', ascending=True)
    assert len(ranked_vina) == 3
    assert [p.pose_id for p in ranked_vina] == ['p2', 'p3', 'p1']
    assert [p.rank for p in ranked_vina] == [1, 2, 3]
    assert ranked_vina.top_pose.pose_id == 'p2'
    assert ranked_vina.provenance['ranking_policy']['score_name'] == 'vina'

    # Rank by GNINA score (ascending=False: higher probability is better)
    ranked_gnina = result.rank_by('gnina', ascending=False)
    assert [p.pose_id for p in ranked_gnina] == ['p3', 'p1', 'p2']
    assert [p.rank for p in ranked_gnina] == [1, 2, 3]
    assert ranked_gnina.top_pose.pose_id == 'p3'


def test_docking_result_ranking_missing_score():
    coords = puw.quantity([[0.0, 0.0, 0.0]], 'nm')
    p1 = DockingPose(coordinates=coords, scores={'vina': -7.0})
    result = DockingResult(poses=[p1])

    with pytest.raises(ArgumentError, match="does not have score 'nonexistent'"):
        result.rank_by('nonexistent')


def test_docking_result_serialization_roundtrip():
    coords = puw.quantity([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]], 'nm')
    p1 = DockingPose(
        coordinates=coords,
        scores={'vina': -7.5},
        rank=1,
        pose_id='pose_1',
        partner_state_id='lig_A',
    )
    result = DockingResult(
        poses=[p1],
        problem_info={'system': '1UYD'},
        protocol_info={'exhaustiveness': 8},
        provenance={'backend': 'vina', 'version': '1.2.5'},
    )

    serialized = result.to_dict()
    assert serialized['schema_version'] == '1.0'
    assert len(serialized['poses']) == 1

    recovered = DockingResult.from_dict(serialized)
    assert len(recovered) == 1
    assert recovered.problem_info['system'] == '1UYD'
    assert recovered.protocol_info['exhaustiveness'] == 8
    assert recovered.provenance['backend'] == 'vina'

    rec_pose = recovered[0]
    assert rec_pose.pose_id == 'pose_1'
    assert rec_pose.rank == 1
    assert rec_pose.partner_state_id == 'lig_A'
    assert rec_pose.scores['vina'] == -7.5
    np.testing.assert_allclose(
        puw.get_value(rec_pose.coordinates),
        puw.get_value(p1.coordinates),
    )
