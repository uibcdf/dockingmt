"""Original rigid geometry, independent fit, captured scores and all populations."""

import base64
import gzip
import json
from contextlib import nullcontext

import molsysmt as msm
import numpy as np
import pandas as pd
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_occupancy import atom_fields, fixed_pair, frozen_partner
from devtools.qualify_5x72_rigid import (
    OUTPUT,
    QUARTETS,
    admit_geometry,
    angles,
    compare_saved,
    construct,
    load_archives,
    load_reference,
    prepare_cases,
    prepare_reference,
    score_components,
    sha,
    snapshot,
    xyz,
)

UNITS = ['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'degrees']


@pytest.fixture(scope='module')
def inputs():
    sources, cases = prepare_cases()
    return sources, cases, load_archives()[0]


def assert_score(data, original, control, receptor):
    scored = dmt.DockingPose.from_dict(data)
    assert original.rank is None and original.scores == {} and scored.rank is None
    assert 'vina' not in scored.scores
    np.testing.assert_array_equal(
        puw.get_value(scored.coordinates, to_unit='angstrom'),
        puw.get_value(original.coordinates, to_unit='angstrom'),
    )
    history = scored.metadata['scoring_history'][-1]
    assert history['operation'] == 'score' and len(history['scores']) == 8
    assert dmt.verify_captured_inputs(history['backend_artifacts'])
    assert history['backend_artifacts']['receptor']['sha256'] == sha(receptor.encode())
    text = base64.b64decode(
        history['backend_artifacts']['partner']['content_base64']
    ).decode()
    assert text == frozen_partner(control, original)
    for key, value in history['scores'].items():
        descriptor = scored.score_definitions[key]
        assert (
            descriptor['kind'] == 'empirical'
            and descriptor['context']['stage'] == 'scoring'
        )
        assert puw.get_value(
            puw.quantity(scored.scores[key], descriptor['unit']), to_unit='kcal/mol'
        ) == pytest.approx(value)


@pytest.mark.parametrize('policy', ['current', 'inferred'])
def test_current_reference_torsions_preserve_original_chemistry_and_all_h(policy):
    context = (
        pd.option_context('future.infer_string', True)
        if policy == 'inferred'
        else nullcontext()
    )
    with context:
        sources, cases = prepare_cases()
        for name in ('p59', 'p69'):
            before = snapshot(sources[name])
            fitted, poses, evidence = construct(name, sources[name], cases[name])
            assert snapshot(sources[name]) == before
            assert (
                evidence['source_unchanged']
                and evidence['charge_audit']['assessment'] == 'consistent'
            )
            assert len(evidence['geometry']['pairs']) == 741
            assert (
                sum(r['within_fragment'] for r in evidence['geometry']['pairs']) == 246
            )
            assert sum(r['bond'] for r in evidence['geometry']['pairs']) == 42
            np.testing.assert_allclose(
                angles(fitted), evidence['target_angles_radians'], rtol=0, atol=1e-9
            )
            assert len(evidence['torsion_steps']) == 2
            assert [
                step['quartet'] for step in evidence['torsion_steps']
            ] == QUARTETS.tolist()
            assert set(poses) == {'native', 'first_fixed'}
            assert all(
                pose.metadata['H_policy'].startswith('All original H')
                for pose in poses.values()
            )


@pytest.mark.parametrize('name', ['p59', 'p69'])
def test_rigid_placement_both_trees_and_degree_policy_under_pm_fs(inputs, name):
    sources, cases, _ = inputs
    with puw.context(standard_units=UNITS):
        fitted, poses, evidence = construct(name, sources[name], cases[name])
        geometry = evidence['geometry']
        assert geometry['max_within_fragment_distance_change_angstrom'] <= 1e-9
        assert geometry['max_bond_length_change_angstrom'] <= 1e-9
        for order, pose in poses.items():
            control = cases[name]['controls'][order]
            old, written = (
                atom_fields(control['pdbqt']),
                atom_fields(frozen_partner(control, pose)),
            )
            for a, b in zip(old, written, strict=True):
                for field in (
                    'id',
                    'name',
                    'group',
                    'group_id',
                    'chain',
                    'charge_e',
                    'type',
                ):
                    assert a[field] == b[field]
            np.testing.assert_allclose(
                [a['coordinates'] for a in written],
                xyz(fitted)[control['pdbqt_to_source_atom_indices']],
                rtol=0,
                atol=0.000500001,
            )


@pytest.mark.parametrize('change', ['cut_bond', 'fragment', 'reflection'])
def test_rigid_admission_refuses_bond_distortion_fragment_change_or_mirror(
    inputs, change
):
    sources, cases, _ = inputs
    source = sources['p69']
    fitted, _, evidence = construct('p69', source, cases['p69'])
    reference = prepare_reference('p69', source, cases['p69'])[0]
    changed = msm.copy(fitted)
    coordinates = xyz(changed).copy()
    if change == 'cut_bond':
        indices = np.flatnonzero(
            np.asarray(evidence['geometry']['fragments']['atom_fragment_indices']) == 0
        )
        direction = coordinates[6] - coordinates[7]
        coordinates[indices] += 0.2 * direction / np.linalg.norm(direction)
    elif change == 'fragment':
        coordinates[10, 0] += 0.02
    else:
        coordinates[:, 0] *= -1
    msm.set(changed, coordinates=puw.quantity(coordinates[None], 'angstrom'))
    before = snapshot(changed)
    with pytest.raises(AssertionError):
        admit_geometry(source, changed, reference)
    assert snapshot(changed) == before


def test_live_original_h_geometry_scores_both_contexts_under_pm_fs(inputs):
    sources, cases, archives = inputs
    _, poses, _ = construct('p69', sources['p69'], cases['p69'])
    pose = poses['first_fixed']
    before = pose.to_dict()
    receptors = {
        k: v['pdbqt'] for k, v in archives['p69']['preparation']['receptors'].items()
    }
    with puw.context(standard_units=UNITS):
        scores = fixed_pair(pose, cases['p69']['controls']['first_fixed'], receptors)
        for context, data in scores.items():
            assert_score(
                data, pose, cases['p69']['controls']['first_fixed'], receptors[context]
            )
    assert pose.to_dict() == before


def test_saved_1482_full_atom_pairs_eight_scores_and_all_156_poses(inputs):
    sources, cases, archives = inputs
    payload = OUTPUT.read_bytes()
    checkpoint = json.loads(OUTPUT.with_name('checkpoint_2026-10-09.json').read_text())
    assert sha(payload) == checkpoint['producer_archive']['gzip_sha256']
    record = json.loads(gzip.decompress(payload))
    assert (
        sha(OUTPUT.with_name('producer_2026-10-09.py.txt').read_bytes())
        == record['consumer_source_sha256']['devtools/qualify_5x72_rigid.py']
    )
    references = load_reference()
    assert record['new_searches'] == 0 and record['new_fixed_evaluations'] == 8
    assert (
        record['saved_poses_reused'] == 156
        and record['saved_fixed_evaluations_reused'] == 312
    )
    rows, cells, evaluations, pairs = [], [], 0, 0
    with puw.context(standard_units=UNITS):
        for name in ('p59', 'p69'):
            saved = record['conformers'][name]
            fitted, poses, construction = construct(name, sources[name], cases[name])
            geometry = construction['geometry']
            old_geometry = saved['construction']['geometry']
            assert geometry['heavy_positional_rmsd_angstrom'] == pytest.approx(
                old_geometry['heavy_positional_rmsd_angstrom'], abs=1e-9
            )
            for current, prior in zip(
                geometry['pairs'], old_geometry['pairs'], strict=True
            ):
                for key in (
                    'source_atom_pair',
                    'fragment_indices',
                    'within_fragment',
                    'bond',
                    'heavy_pair',
                ):
                    assert current[key] == prior[key]
                for key in (
                    'original_distance_angstrom',
                    'fitted_distance_angstrom',
                    'experimental_reference_distance_angstrom',
                    'fitted_minus_original_angstrom',
                ):
                    assert current[key] == pytest.approx(prior[key], abs=1e-9)
                pairs += 1
            for order, current in poses.items():
                original = dmt.DockingPose.from_dict(saved['poses'][order])
                np.testing.assert_allclose(
                    puw.get_value(original.coordinates, to_unit='angstrom'),
                    puw.get_value(current.coordinates, to_unit='angstrom'),
                    rtol=0,
                    atol=1e-9,
                )
                for context, data in saved['fixed_scores'][order].items():
                    assert_score(
                        data,
                        original,
                        cases[name]['controls'][order],
                        archives[name]['preparation']['receptors'][context]['pdbqt'],
                    )
                    contrast = {
                        key: value
                        - score_components(
                            references['references'][name]['fixed_scores'][order][
                                context
                            ]
                        )[key]
                        for key, value in score_components(data).items()
                    }
                    assert (
                        contrast
                        == saved['prepared_minus_experimental_reference_kcal_mol'][
                            order
                        ][context]
                    )
                    evaluations += 1
            agreement = {
                context: {
                    key: score_components(
                        saved['fixed_scores']['first_fixed'][context]
                    )[key]
                    - value
                    for key, value in score_components(
                        saved['fixed_scores']['native'][context]
                    ).items()
                }
                for context in ('sham', 'occupied')
            }
            assert agreement == saved['root_order_component_difference_kcal_mol']
            assert saved['root_order_agrees_at_0_001_kcal_mol'] == all(
                abs(v) <= 0.001
                for values in agreement.values()
                for v in values.values()
            )
            compared, summarized = compare_saved(
                name, archives[name], saved['fixed_scores']
            )
            rows.extend(compared)
            cells.extend(summarized)
    assert evaluations == 8 and pairs == 1482 and len(rows) == 312 and len(cells) == 96
    assert rows == record['comparison_rows'] and cells == record['cell_summaries']
