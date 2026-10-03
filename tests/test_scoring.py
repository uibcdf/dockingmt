"""Public fixed-pose scoring and independent evaluation attachment."""

import base64
import hashlib
import json
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT

import dockingmt as dmt
from dockingmt._private.smonitor import (
    ArgumentError,
    CapabilityMismatchError,
    LibraryNotFoundError,
)


@pytest.fixture
def problem():
    return dmt.DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=MINIMAL_LIG_PDBQT,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
        metadata={'partner_state_id': 'ligand', 'receptor_state_id': 'receptor'},
    )


@pytest.fixture
def pose():
    return dmt.DockingPose(
        puw.quantity([[0, 0, 0], [1.5, 0, 0]], 'angstrom'),
        scores={'prior': -2.5},
        pose_id='original',
        rank=3,
        partner_state_id='ligand',
        receptor_state_id='receptor',
        metadata={'annotations': {'values': [1]}},
    )


def test_with_scores_preserves_prior_evidence_and_detaches(pose):
    before = pose.to_dict()
    definition = {
        'schema_version': '1.0',
        'method': 'external model',
        'method_version': '1',
        'component': 'total',
        'kind': 'dimensionless',
        'unit': 'dimensionless',
        'preferred_direction': 'higher',
        'context': {'model': {'id': 'test'}},
    }
    result = pose.with_scores({'external': np.float64(0.75)}, {'external': definition})
    assert result.scores == {'prior': -2.5, 'external': 0.75}
    assert result.pose_id == 'original' and result.rank == 3
    assert (
        result.partner_state_id == 'ligand' and result.receptor_state_id == 'receptor'
    )
    definition['context']['model']['id'] = 'edited'
    result.metadata['annotations']['values'].append(2)
    puw.get_value(result.coordinates)[0, 0] = 5
    assert result.score_definitions['external']['context']['model']['id'] == 'test'
    assert pose.to_dict() == before


@pytest.mark.parametrize(
    'scores',
    [{'prior': -3}, {'x': True}, {'x': np.nan}, {'x': np.inf}, {'': 1}, None, [1]],
)
def test_with_scores_rejects_bad_additions_atomically(pose, scores):
    before = pose.to_dict()
    with pytest.raises(ArgumentError):
        pose.with_scores(scores)
    assert pose.to_dict() == before


def test_with_scores_revalidates_prior_scores_and_definitions(pose):
    pose.scores['prior'] = np.nan
    with pytest.raises(ArgumentError):
        pose.with_scores({'new': 1})
    pose.scores['prior'] = -2.5
    with pytest.raises(ArgumentError):
        pose.with_scores({'new': 1}, {'prior': {}})
    pose.metadata['score_definitions'] = {'prior': {}}
    with pytest.raises(ArgumentError):
        pose.with_scores({'new': 1})


@pytest.mark.parametrize('scoring', ['vina', 'vinardo'])
def test_native_scoring_matches_direct_engine_and_preserves_pose(
    problem, pose, scoring, tmp_path
):
    from vina import Vina

    receptor = tmp_path / 'receptor.pdbqt'
    receptor.write_text(MINIMAL_REC_PDBQT)
    native = Vina(sf_name=scoring, cpu=1, seed=17, verbosity=0)
    native.set_receptor(str(receptor))
    native.set_ligand_from_string(MINIMAL_LIG_PDBQT)
    native.compute_vina_maps(center=[0, 0, 0], box_size=[10, 10, 10])
    expected = native.score()
    before = pose.to_dict()
    with puw.context(standard_units=['pm', 'fs', 'kJ/mol']):
        units = deepcopy(puw.configure.get_standard_units())
        result = dmt.score(
            problem,
            dmt.VinaProtocol(
                scoring=scoring,
                cpu=1,
                seed=17,
                capture_backend_inputs=True,
                collect_timings=True,
            ),
            pose=pose,
            score_name=scoring,
        )
        assert puw.configure.get_standard_units() == units
        np.testing.assert_array_equal(
            puw.get_value(result.coordinates), puw.get_value(pose.coordinates)
        )
    components = [
        'total',
        'lig_inter',
        'flex_inter',
        'other_inter',
        'flex_intra',
        'lig_intra',
        'torsions',
        'lig_intra_best_pose',
    ]
    names = [scoring] + [f'{scoring}.{component}' for component in components[1:]]
    np.testing.assert_allclose(
        [result.scores[name] for name in names], expected, rtol=0, atol=0
    )
    assert result.scores['prior'] == -2.5
    assert result.rank == 3 and result.pose_id == 'original'
    assert pose.to_dict() == before
    evaluation = result.metadata['scoring_history'][0]
    assert evaluation['backend_version'] == __import__('vina').__version__
    assert evaluation['unused_search_parameters'] == [
        'exhaustiveness',
        'n_poses',
        'energy_range',
    ]
    assert evaluation['geometry_check']['state_checks'] == {
        'partner': 'matched',
        'receptor': 'matched',
    }
    assert sum(evaluation['timings']['phases'].values()) == pytest.approx(
        evaluation['timings']['total']
    )
    for role, content in [
        ('receptor', MINIMAL_REC_PDBQT),
        ('partner', MINIMAL_LIG_PDBQT),
    ]:
        artifact = evaluation['backend_artifacts'][role]
        assert base64.b64decode(artifact['content_base64']) == content.encode()
        assert artifact['sha256'] == hashlib.sha256(content.encode()).hexdigest()
    for name, component in zip(names, components):
        descriptor = result.score_definitions[name]
        assert descriptor['component'] == component
        assert descriptor['kind'] == 'empirical'
        assert puw.are_compatible(puw.quantity(1, descriptor['unit']), 'kcal/mol')
        assert descriptor['context']['stage'] == 'scoring'
        assert descriptor['preferred_direction'] == (
            'lower' if component == 'total' else None
        )
    record = json.loads(json.dumps(result.to_dict(), allow_nan=False))
    restored = dmt.DockingPose.from_dict(record)
    assert restored.to_dict() == result.to_dict()


def test_successive_scoring_retains_independent_histories(problem):
    first = dmt.score(problem, dmt.VinaProtocol(cpu=1, seed=17), score_name='vina')
    before = first.to_dict()
    second = dmt.score(
        problem,
        dmt.VinaProtocol(cpu=1, scoring='vinardo', seed=17),
        pose=first,
        score_name='vinardo',
    )
    assert len(second.scores) == 16
    assert len(second.metadata['scoring_history']) == 2
    assert second.rank is None
    assert first.to_dict() == before
    second.metadata['scoring_history'][0]['scores']['vina'] = 0
    assert (
        first.metadata['scoring_history'][0]['scores']['vina'] == first.scores['vina']
    )
    assert len(second.metadata['scoring_history'][1]['score_definitions']) == 8


@pytest.fixture
def no_engine(monkeypatch):
    import vina

    def forbidden(*args, **kwargs):
        pytest.fail('Invalid scoring request reached the native engine.')

    monkeypatch.setattr(vina, 'Vina', forbidden)


@pytest.mark.parametrize(
    'change',
    [
        'coordinates',
        'count',
        'state',
        'collision',
        'history',
        'descriptor',
        'atom_identity',
    ],
)
def test_invalid_pose_rejected_before_native_setup(problem, pose, no_engine, change):
    if change == 'coordinates':
        puw.get_value(pose.coordinates)[0, 0] += 0.001
    elif change == 'count':
        pose = dmt.DockingPose(puw.quantity([[0, 0, 0]], 'nm'))
    elif change == 'state':
        pose.partner_state_id = 'other'
    elif change == 'collision':
        pose.scores['score.lig_intra'] = 1
    elif change == 'history':
        pose.metadata['scoring_history'] = {}
    elif change == 'descriptor':
        pose.metadata['score_definitions'] = {'prior': {}}
    else:
        pose.metadata.update(
            pose_atom_order='verified_pdbqt_order',
            source_atom_keys=[
                {'atom_id': str(i), 'atom_name': 'wrong', 'element': 'C'}
                for i in range(2)
            ],
        )
    with pytest.raises(ArgumentError):
        dmt.score(problem, pose=pose)


@pytest.mark.parametrize(
    'protocol',
    [dmt.VinaProtocol(scoring='ad4'), dmt.VinaProtocol(active_torsion_bonds=[(0, 1)])],
)
def test_unsupported_protocol_rejected_early(problem, protocol, no_engine):
    with pytest.raises((ArgumentError, CapabilityMismatchError)):
        dmt.score(problem, protocol)


def test_scoring_rejects_unprepared_inputs_and_guidance(problem, no_engine):
    native = msm.convert(
        'pdbqt_text:' + MINIMAL_LIG_PDBQT,
        to_form='molsysmt.MolSys',
        discard_torsion_tree=True,
    )
    unprepared = dmt.DockingProblem(
        receptor=problem.receptor, partner=native, search_domain=problem.search_domain
    )
    with pytest.raises(ArgumentError, match='already prepared'):
        dmt.score(unprepared)
    guided = dmt.DockingProblem(
        receptor=problem.receptor,
        partner=problem.partner,
        search_domain=problem.search_domain,
        search_guidance={'request': 'unsupported'},
    )
    with pytest.raises(CapabilityMismatchError):
        dmt.score(guided)


@pytest.mark.parametrize('failure', ['native', 'shape', 'nonfinite', 'geometry'])
def test_scoring_failures_cleanup_staged_files(
    problem, pose, monkeypatch, tmp_path, failure
):
    import vina

    files = {}
    for role, text in [('receptor', MINIMAL_REC_PDBQT), ('partner', MINIMAL_LIG_PDBQT)]:
        path = tmp_path / f'{role}.pdbqt'
        path.write_text(text)
        files[role] = path
    problem = dmt.DockingProblem(
        **files, search_domain=problem.search_domain, metadata=problem.metadata
    )
    paths = []
    original = dmt.VinaBackend._stage_inputs

    def stage(self, receptor, partner, protocol, temp_files):
        result = original(self, receptor, partner, protocol, temp_files)
        paths.extend(temp_files)
        return result

    class FakeVina:
        def __init__(self, **kwargs):
            assert failure != 'geometry'

        def set_receptor(self, **kwargs):
            pass

        def set_ligand_from_file(self, path):
            pass

        def compute_vina_maps(self, **kwargs):
            pass

        def score(self):
            if failure == 'native':
                raise RuntimeError('native failure')
            return [0] * 7 if failure == 'shape' else [np.nan] * 8

    monkeypatch.setattr(dmt.VinaBackend, '_stage_inputs', stage)
    monkeypatch.setattr(vina, 'Vina', FakeVina)
    if failure == 'geometry':
        puw.get_value(pose.coordinates)[0, 0] += 1
    with pytest.raises((RuntimeError, ArgumentError)):
        dmt.score(problem, pose=pose)
    assert len(paths) == 2
    assert all(not Path(path).exists() for path in paths)
    assert all(getattr(problem, role).exists() for role in ('receptor', 'partner'))


def test_absent_vina_reports_local_dependency_error(problem, monkeypatch):
    from depdigest.core import checker

    monkeypatch.setattr(checker, 'is_installed', lambda name: False)
    with pytest.raises(LibraryNotFoundError):
        dmt.score(problem)


def test_score_component_mapping_never_calls_search_and_snapshots_files(
    problem, monkeypatch, tmp_path
):
    import vina

    receptor = tmp_path / 'rec.pdbqt'
    ligand = tmp_path / 'lig.pdbqt'
    receptor.write_text(MINIMAL_REC_PDBQT)
    ligand.write_text(MINIMAL_LIG_PDBQT)
    problem = dmt.DockingProblem(receptor, ligand, problem.search_domain)

    class FixedEngine:
        def __init__(self, **kwargs):
            # Mutating caller files after projection must not change submitted bytes.
            receptor.write_text('changed')
            ligand.write_text('changed')

        def set_receptor(self, rigid_pdbqt_filename):
            assert Path(rigid_pdbqt_filename).read_text() == MINIMAL_REC_PDBQT

        def set_ligand_from_file(self, path):
            assert Path(path).read_text() == MINIMAL_LIG_PDBQT

        def compute_vina_maps(self, **kwargs):
            pass

        def score(self):
            return np.arange(8, dtype=float) + 0.5

        def info(self):
            return {'weights': [1.0], 'box_spacing': 0.375, 'seed': 17}

        # No dock(), optimize(), randomize(), poses() or energies().

    monkeypatch.setattr(vina, 'Vina', FixedEngine)
    result = dmt.score(problem, dmt.VinaProtocol(cpu=1, capture_backend_inputs=True))
    assert list(result.scores.values()) == [i + 0.5 for i in range(8)]
    assert list(
        result.score_definitions[name]['component'] for name in result.scores
    ) == [
        'total',
        'lig_inter',
        'flex_inter',
        'other_inter',
        'flex_intra',
        'lig_intra',
        'torsions',
        'lig_intra_best_pose',
    ]
    artifacts = result.metadata['scoring_history'][0]['backend_artifacts']
    assert (
        base64.b64decode(artifacts['partner']['content_base64'])
        == MINIMAL_LIG_PDBQT.encode()
    )


def test_prepared_ligand_rounding_mapping_and_provisional_policy(problem):
    native = msm.convert(
        'pdbqt_text:' + MINIMAL_LIG_PDBQT,
        to_form='molsysmt.MolSys',
        discard_torsion_tree=True,
    )
    coordinates = puw.quantity([[0.0004, 0, 0], [1.5004, 0, 0]], 'angstrom')
    prepared = dmt.PreparedLigand(
        'ligand',
        ['C1', 'C2'],
        'LIG',
        coordinates,
        ['C', 'C'],
        [0, 0],
        source_molsys=native,
        metadata={'charge_source': 'zero_placeholder'},
    )
    problem = dmt.DockingProblem(
        problem.receptor, prepared, problem.search_domain, metadata=problem.metadata
    )
    before = prepared.to_dict()
    with pytest.raises(ArgumentError, match='provisional'):
        dmt.score(problem)
    scored = dmt.score(
        problem, dmt.VinaProtocol(cpu=1, allow_provisional_preparation=True)
    )
    np.testing.assert_allclose(
        puw.get_value(scored.coordinates, to_unit='angstrom'),
        puw.get_value(coordinates, to_unit='angstrom'),
        rtol=0,
        atol=1e-12,
    )
    assert prepared.to_dict() == before
    assert scored.metadata['source_atom_keys'][0]['atom_name'] == 'C1'
    assert (
        scored.metadata['scoring_history'][0]['geometry_check']['identity_check']
        == 'names_and_elements'
    )
    assert (
        scored.metadata['scoring_history'][0]['preparation']['partner'][
            'assessment_report'
        ]['assessment']
        == 'provisional'
    )


def test_flexible_external_input_retains_tree_and_record_order():
    data = Path(__file__).parent / 'data/vina_torsions'
    ligand = data / '1iep_ligand.pdbqt'
    original = ligand.read_bytes()
    xyz = msm.get(ligand, element='atom', coordinates=True)[0]
    center = np.mean(puw.get_value(xyz, to_unit='angstrom'), axis=0)
    problem = dmt.DockingProblem(
        data / '1iep_receptor.pdbqt',
        ligand,
        dmt.BoxRegion(
            puw.quantity(center, 'angstrom'), puw.quantity([30, 30, 30], 'angstrom')
        ),
    )
    scored = dmt.score(
        problem, dmt.VinaProtocol(cpu=1, seed=17, capture_backend_inputs=True)
    )
    np.testing.assert_array_equal(
        puw.get_value(scored.coordinates, to_unit='angstrom'),
        puw.get_value(xyz, to_unit='angstrom'),
    )
    artifact = scored.metadata['scoring_history'][0]['backend_artifacts']['partner']
    assert base64.b64decode(artifact['content_base64']) == original
    assert ligand.read_bytes() == original
    assert scored.scores['score.torsions'] != 0


def test_docking_only_backends_remain_compatible(problem):
    class DockingOnly(dmt.DockingBackend):
        name = 'docking_only'
        capabilities = set()
        is_available = True

        def dock(self, problem, protocol=None):
            return dmt.DockingResult([])

    backend = DockingOnly()
    assert len(dmt.dock(problem, backend=backend)) == 0
    with pytest.raises(CapabilityMismatchError, match='pose_scoring'):
        dmt.score(problem, backend=backend)
