"""Reference admission, immutable fixed scores and complete saved diagnostics."""

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
from devtools.qualify_5x72_reference import (
    OUTPUT,
    chemical_axis,
    compare_saved,
    geometry_diagnostic,
    load_archives,
    prepare_cases,
    prepare_reference,
    score_components,
    sha,
    snapshot,
    xyz,
)

UNITS = ['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']


@pytest.fixture(scope='module')
def inputs():
    sources, cases = prepare_cases()
    return sources, cases, load_archives()[0]


def assert_reference_evaluation(data, original, control, receptor):
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
    assert set(scored.scores) == set(history['scores'])
    for name, value in history['scores'].items():
        descriptor = scored.score_definitions[name]
        assert descriptor['kind'] == 'empirical'
        assert descriptor['context']['stage'] == 'scoring'
        assert puw.get_value(
            puw.quantity(scored.scores[name], descriptor['unit']), to_unit='kcal/mol'
        ) == pytest.approx(value)


@pytest.mark.parametrize('policy', ['current', 'inferred'])
def test_reference_admission_keeps_original_chemical_identity_and_generated_h(policy):
    context = (
        pd.option_context('future.infer_string', True)
        if policy == 'inferred'
        else nullcontext()
    )
    with context:
        sources, cases = prepare_cases()
        for name in ('p59', 'p69'):
            before = snapshot(sources[name])
            placed, poses, evidence = prepare_reference(
                name, sources[name], cases[name]
            )
            assert snapshot(sources[name]) == before
            assert evidence['chemical_axis'] == chemical_axis(placed)
            assert [29, 8] in evidence['chemical_axis']['hydrogen_parent_pairs']
            assert evidence['original_atom_names'] != evidence['generated_atom_names']
            assert evidence['hydrogen_addition']['n_added_hydrogens'] == 15
            assert evidence['hydrogen_addition']['parameters']['optimize'] is False
            assert (
                evidence['hydrogen_addition']['original_coordinates_preserved'] is True
            )
            assert evidence['charge_audit']['assessment'] == 'consistent'
            np.testing.assert_allclose(
                xyz(placed)[:24],
                cases[name]['reference_coordinates_angstrom'],
                rtol=0,
                atol=1e-12,
            )
            assert set(poses) == {'native', 'first_fixed'}


@pytest.mark.parametrize('name', ['p59', 'p69'])
def test_both_reference_trees_and_distances_under_pm_fs(inputs, name):
    sources, cases, _ = inputs
    with puw.context(standard_units=UNITS):
        placed, poses, _ = prepare_reference(name, sources[name], cases[name])
        for order, pose in poses.items():
            original = atom_fields(cases[name]['controls'][order]['pdbqt'])
            written = atom_fields(frozen_partner(cases[name]['controls'][order], pose))
            for a, b in zip(original, written, strict=True):
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
                xyz(placed)[
                    cases[name]['controls'][order]['pdbqt_to_source_atom_indices']
                ],
                rtol=0,
                atol=0.000500001,
            )
        geometry = geometry_diagnostic(sources[name], placed)
    assert len(geometry['pairs']) == 276
    assert sum(r['heavy_bond'] for r in geometry['pairs']) == 27
    assert [len(r['heavy_atom_indices']) for r in geometry['summaries'][1:]] == [
        7,
        11,
        6,
    ]


def test_admission_refuses_changed_indexed_chemistry(inputs):
    sources, cases, _ = inputs
    changed = msm.copy(sources['p69'])
    msm.set(changed, element='atom', selection=[7], formal_charge=[1])
    before = snapshot(changed)
    with pytest.raises(AssertionError):
        prepare_reference('p69', changed, cases['p69'])
    assert snapshot(changed) == before


def test_live_reference_fixed_scores_keep_unranked_geometry_under_pm_fs(inputs):
    sources, cases, archives = inputs
    _, poses, _ = prepare_reference('p69', sources['p69'], cases['p69'])
    pose = poses['first_fixed']
    before = pose.to_dict()
    receptors = {
        k: v['pdbqt'] for k, v in archives['p69']['preparation']['receptors'].items()
    }
    with puw.context(standard_units=UNITS):
        scores = fixed_pair(pose, cases['p69']['controls']['first_fixed'], receptors)
        for context, data in scores.items():
            assert_reference_evaluation(
                data, pose, cases['p69']['controls']['first_fixed'], receptors[context]
            )
    assert pose.to_dict() == before


def test_saved_references_all_156_poses_and_552_indexed_distances(inputs):
    sources, cases, archives = inputs
    payload = OUTPUT.read_bytes()
    checkpoint = json.loads(OUTPUT.with_name('checkpoint_2026-10-09.json').read_text())
    assert sha(payload) == checkpoint['producer_archive']['gzip_sha256']
    record = json.loads(gzip.decompress(payload))
    producer = OUTPUT.with_name('producer_2026-10-09.py')
    assert (
        sha(producer.read_bytes())
        == record['consumer_source_sha256']['devtools/qualify_5x72_reference.py']
    )
    assert record['new_searches'] == 0 and record['new_fixed_evaluations'] == 8
    assert (
        record['saved_poses_reused'] == 156
        and record['saved_fixed_evaluations_reused'] == 312
    )
    rows, cells, evaluations = [], [], 0
    with puw.context(standard_units=UNITS):
        for name in ('p59', 'p69'):
            saved = record['references'][name]
            placed, poses, _ = prepare_reference(name, sources[name], cases[name])
            geometry = geometry_diagnostic(sources[name], placed)
            for current, original in zip(
                geometry['pairs'], saved['geometry']['pairs'], strict=True
            ):
                for key in (
                    'source_atom_pair',
                    'heavy_bond',
                    'fragment_indices',
                    'within_fragment',
                ):
                    assert current[key] == original[key]
                for key in (
                    'prepared_distance_angstrom',
                    'reference_distance_angstrom',
                    'reference_minus_prepared_angstrom',
                ):
                    assert current[key] == pytest.approx(original[key], abs=1e-10)
            for order, current in poses.items():
                original = dmt.DockingPose.from_dict(saved['poses'][order])
                indices = cases[name]['controls'][order]['heavy_pdbqt_indices']
                np.testing.assert_allclose(
                    puw.get_value(original.coordinates, to_unit='angstrom')[indices],
                    puw.get_value(current.coordinates, to_unit='angstrom')[indices],
                    rtol=0,
                    atol=1e-12,
                )
                for context, data in saved['fixed_scores'][order].items():
                    assert_reference_evaluation(
                        data,
                        original,
                        cases[name]['controls'][order],
                        archives[name]['preparation']['receptors'][context]['pdbqt'],
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
    assert evaluations == 8 and len(rows) == 312 and len(cells) == 96
    assert rows == record['comparison_rows'] and cells == record['cell_summaries']
