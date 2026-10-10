"""Fixed translation, authenticated score inputs and complete finite populations."""

import gzip
import itertools
import json
from contextlib import nullcontext
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pandas as pd
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_displacement import (
    ARMS,
    OFFSETS,
    OUTPUT,
    UNITS,
    assess_scores,
    base_systems,
    load_contact,
    load_inputs,
    selected_pair_distances,
    sha,
    snapshot,
    summarize,
    translated_point,
    xyz,
)
from devtools.qualify_5x72_occupancy import fixed_pair
from devtools.qualify_5x72_reference import score_components

ARCHIVE_SHA = 'afb8bfa4092abc78f8cd2daf33da7248fe39fbd1856b23e24a192f4813fb72a8'
JSON_SHA = '0bbf5990234cec5b739d7f32f00e035ada42d9bd3277932eab831c9f3545226c'
PRODUCER_SHA = 'ed2db70e65c8248e6502169c8043f3f7e0dbe5b8b278af6b0c0eb44370fd9e23'
POLICY = ['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'degrees']


@pytest.fixture(scope='module')
def inputs():
    return load_inputs()[:3]


@pytest.fixture(scope='module')
def saved():
    payload = OUTPUT.read_bytes()
    assert sha(payload) == ARCHIVE_SHA
    assert sha(gzip.decompress(payload)) == JSON_SHA
    return json.loads(gzip.decompress(payload))


def _point(record, name, arm, offset):
    return next(
        p
        for p in record['points']
        if (p['ligand'], p['geometry_arm'], p['offset_index']) == (name, arm, offset)
    )


@pytest.mark.parametrize('policy', ['current', 'pm_fs_inferred'])
def test_public_translation_preserves_all39_geometry_and_saved_axes(
    inputs, saved, monkeypatch, policy
):
    def forbidden(*args, **kwargs):
        pytest.fail('Geometry qualification must not invoke scoring or search.')

    monkeypatch.setattr(dmt, 'score', forbidden)
    monkeypatch.setattr(dmt, 'dock', forbidden)
    units = puw.context(standard_units=POLICY) if policy != 'current' else nullcontext()
    strings = (
        pd.option_context('future.infer_string', True)
        if policy != 'current'
        else nullcontext()
    )
    before_inputs = deepcopy(inputs)
    with units, strings:
        bases, _ = base_systems(*inputs)
        for name in ('p59', 'p69'):
            case = inputs[2][name]['cases'][name]
            for arm in ARMS:
                base = bases[name][arm]
                before = snapshot(base)
                for offset in range(7):
                    moved, poses, geometry = translated_point(
                        base, offset, name, arm, case
                    )
                    prior = _point(saved, name, arm, offset)
                    assert snapshot(base) == before
                    np.testing.assert_allclose(
                        xyz(moved),
                        prior['geometry']['full39_coordinates_angstrom'],
                        rtol=0,
                        atol=1e-10,
                    )
                    assert (
                        geometry['all741_pair_indices']
                        == prior['geometry']['all741_pair_indices']
                    )
                    assert geometry['heavy_positional_rmsd_angstrom'] == pytest.approx(
                        prior['geometry']['heavy_positional_rmsd_angstrom'], abs=1e-10
                    )
                    for order, pose in poses.items():
                        original = dmt.DockingPose.from_dict(prior['poses'][order])
                        np.testing.assert_allclose(
                            puw.get_value(pose.coordinates, to_unit='angstrom'),
                            puw.get_value(original.coordinates, to_unit='angstrom'),
                            rtol=0,
                            atol=1e-10,
                        )
                        assert pose.rank is None and pose.scores == {}
                        assert (
                            pose.metadata['pdbqt_to_source_atom_indices']
                            == (original.metadata['pdbqt_to_source_atom_indices'])
                        )
    assert inputs == before_inputs


@pytest.mark.parametrize('offset', [-1, 7, True])
def test_invalid_displacement_index_fails_before_molecular_work(
    inputs, monkeypatch, offset
):
    def forbidden(*args, **kwargs):
        pytest.fail('Invalid offsets must fail before provider translation.')

    monkeypatch.setattr(msm.structure, 'translate', forbidden)
    with pytest.raises(AssertionError):
        translated_point(None, offset, 'p69', ARMS[0], inputs[2]['p69']['cases']['p69'])


@pytest.mark.parametrize('drift', ['source_map', 'receptor', 'zero_score'])
def test_saved_score_admission_rejects_mapping_receptor_and_anchor_drift(
    inputs, saved, drift
):
    point = deepcopy(_point(saved, 'p69', ARMS[0], 0))
    case = inputs[2]['p69']['cases']['p69']
    receptors = {
        c: r['pdbqt'] for c, r in inputs[2]['p69']['preparation']['receptors'].items()
    }
    if drift == 'source_map':
        point['fixed_scores']['native']['sham']['metadata'][
            'pdbqt_to_source_atom_indices'
        ].reverse()
    elif drift == 'receptor':
        receptors['sham'] += '\n'
    else:
        # Frozen comparisons consume the recorded calculation history.
        point['fixed_scores']['native']['sham']['metadata']['scoring_history'][0][
            'scores'
        ]['fixed'] += 0.001
    before = deepcopy(point)
    with pytest.raises(AssertionError):
        assess_scores(
            {o: dmt.DockingPose.from_dict(p) for o, p in point['poses'].items()},
            case,
            receptors,
            point['fixed_scores'],
            inputs[0]['conformers']['p69'],
            0,
        )
    assert point == before


def test_live_fixed_score_slice_preserves_inputs_and_native_measurements(
    inputs, saved, monkeypatch
):
    import vina

    def forbidden(*args, **kwargs):
        pytest.fail('This fixed-score slice authorizes no search or optimization.')

    monkeypatch.setattr(dmt, 'dock', forbidden)
    monkeypatch.setattr(vina.Vina, 'dock', forbidden)
    monkeypatch.setattr(vina.Vina, 'optimize', forbidden)
    with (
        puw.context(standard_units=POLICY),
        pd.option_context('future.infer_string', True),
    ):
        bases, _ = base_systems(*inputs)
        case = inputs[2]['p69']['cases']['p69']
        _, poses, _ = translated_point(bases['p69'][ARMS[0]], 1, 'p69', ARMS[0], case)
        before = {o: p.to_dict() for o, p in poses.items()}
        receptors = {
            c: r['pdbqt']
            for c, r in inputs[2]['p69']['preparation']['receptors'].items()
        }
        scores = {
            o: fixed_pair(pose, case['controls'][o], receptors)
            for o, pose in poses.items()
        }
        admitted, agreement = assess_scores(
            poses, case, receptors, scores, inputs[0]['conformers']['p69'], 1
        )
        assert all(v == 0 for row in agreement.values() for v in row.values())
        original = _point(saved, 'p69', ARMS[0], 1)
        for context, orders in admitted.items():
            for order, result in orders.items():
                assert result['scores_kcal_mol'] == score_components(
                    original['fixed_scores'][order][context]
                )
                assert dmt.verify_captured_inputs(result['artifacts'])
            observed = selected_pair_distances(orders['native'], 'p69')
            np.testing.assert_allclose(
                observed['rectangular_distances_angstrom'],
                original['selected_pair_distances'][context][
                    'rectangular_distances_angstrom'
                ],
                rtol=0,
                atol=1e-10,
            )
        assert {o: p.to_dict() for o, p in poses.items()} == before


def test_all_saved_geometry_captures_components_and_matched_anchor_deltas(
    inputs, saved
):
    assert saved['unit_contract'] == UNITS
    assert saved['offsets_angstrom'] == OFFSETS
    assert saved['new_fixed_evaluations'] == 112
    assert saved['fresh_zero_anchor_evaluations'] == 16
    assert saved['new_nonzero_translation_evaluations'] == 96
    assert saved['new_searches'] == saved['new_optimizations'] == 0
    assert (
        sha(OUTPUT.with_name('producer_2026-10-09.py.txt').read_bytes()) == PRODUCER_SHA
    )
    assert (
        saved['consumer_source_sha256']['devtools/qualify_5x72_displacement.py']
        == PRODUCER_SHA
    )
    assert load_contact()['schema'] == 'dockingmt.5x72_contact_audit@1'
    assert summarize(saved['points']) == saved['summaries']
    pairs = np.asarray(list(itertools.combinations(range(39), 2)))
    evaluations = 0
    for point in saved['points']:
        name, arm, offset = (
            point['ligand'],
            point['geometry_arm'],
            point['offset_index'],
        )
        geometry = point['geometry']
        coordinates = np.asarray(geometry['full39_coordinates_angstrom'])
        zero = np.asarray(
            _point(saved, name, arm, 0)['geometry']['full39_coordinates_angstrom']
        )
        np.testing.assert_allclose(
            coordinates - zero,
            np.broadcast_to(OFFSETS[offset], (39, 3)),
            rtol=0,
            atol=1e-10,
        )
        np.testing.assert_array_equal(geometry['all741_pair_indices'], pairs)
        np.testing.assert_allclose(
            geometry['all741_translated_distances_angstrom'],
            np.linalg.norm(coordinates[pairs[:, 0]] - coordinates[pairs[:, 1]], axis=1),
            rtol=0,
            atol=1e-10,
        )
        np.testing.assert_allclose(
            geometry['all741_original_distances_angstrom'],
            geometry['all741_translated_distances_angstrom'],
            rtol=0,
            atol=1e-10,
        )
        assert geometry['max_full_pair_distance_change_angstrom'] <= 1e-10
        volumes = geometry['original_and_translated_signed_volume_angstrom_cubed']
        assert abs(volumes[0]) > 1e-9
        assert volumes[1] == pytest.approx(volumes[0], abs=1e-10)
        case = inputs[2][name]['cases'][name]
        reference = np.asarray(case['reference_coordinates_angstrom'])
        rmsd = np.sqrt(np.mean(np.sum((coordinates[:24] - reference) ** 2, axis=1)))
        assert geometry['heavy_positional_rmsd_angstrom'] == pytest.approx(
            rmsd, abs=1e-10
        )
        assert geometry['within_original_2_5_angstrom_criterion'] == (rmsd <= 2.5)
        poses = {o: dmt.DockingPose.from_dict(p) for o, p in point['poses'].items()}
        receptors = {
            c: r['pdbqt']
            for c, r in inputs[2][name]['preparation']['receptors'].items()
        }
        old = (
            inputs[0]['conformers'][name]
            if arm == ARMS[0]
            else inputs[1]['references'][name]
        )
        admitted, agreement = assess_scores(
            poses, case, receptors, point['fixed_scores'], old, offset
        )
        assert agreement == point['root_order_component_difference_kcal_mol']
        assert all(v == 0 for row in agreement.values() for v in row.values())
        for context, orders in admitted.items():
            for order, entry in orders.items():
                assert len(entry['scores_kcal_mol']) == 8
                assert 'vina' not in point['fixed_scores'][order][context]['scores']
                assert poses[order].rank is None and poses[order].scores == {}
                evaluations += 1
            table = point['selected_pair_distances'][context]
            left = np.asarray(
                [
                    next(
                        a['coordinates']
                        for a in orders['native']['canonical_atoms']
                        if a['source_atom_index'] == s
                    )
                    for s in table['ligand_source_rows']
                ]
            )
            right = np.asarray(
                [row['receptor_atom']['coordinates'] for row in table['declared_pairs']]
            )
            np.testing.assert_allclose(
                table['rectangular_distances_angstrom'],
                np.linalg.norm(left[:, None] - right[None, :], axis=2),
                rtol=0,
                atol=1e-10,
            )
        assert (
            point['selected_pair_distances']['sham']
            == point['selected_pair_distances']['occupied']
        )
    assert len(saved['points']) == 28 and evaluations == 112
    for row in saved['summaries']:
        values = np.asarray(row['seven_totals_kcal_mol'])
        assert row['finite_minimum_offset_index'] == int(np.argmin(values))
        assert row['finite_maximum_offset_index'] == int(np.argmax(values))
        assert row['nonzero_offsets_with_strictly_lower_reported_total'] == int(
            np.sum(values[1:] < values[0])
        )
