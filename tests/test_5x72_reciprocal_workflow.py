"""Reciprocal occupant identity, frozen trees and complete saved populations."""

import base64
import gzip
import itertools
import json
from contextlib import nullcontext

import numpy as np
import pandas as pd
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_occupancy import (
    DATA,
    atom_fields,
    diagnostic_rows,
    fixed_pair,
    frozen_partner,
    load_baseline,
    measure,
    prepare_cases,
    prepare_receptors,
    reference_box,
    sha,
)
from devtools.qualify_5x72_reciprocal import ARMS, BASELINE_SHA, OUTPUT

UNITS = ['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']


@pytest.fixture(scope='module')
def prepared():
    cases = prepare_cases()[1]
    return cases['p69'], prepare_receptors(
        companion='p59', reference_snapshot=cases['p59']['reference_snapshot']
    )


def assert_evaluation(data, original, receptor):
    pose = dmt.DockingPose.from_dict(data)
    history = pose.metadata['scoring_history'][-1]
    artifacts = history['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    assert (
        base64.b64decode(artifacts['receptor']['content_base64']) == receptor.encode()
    )
    assert pose.rank == original.rank and pose.scores['vina'] == original.scores['vina']
    np.testing.assert_allclose(
        puw.get_value(pose.coordinates, to_unit='angstrom'),
        puw.get_value(original.coordinates, to_unit='angstrom'),
        rtol=0,
        atol=1e-12,
    )
    atoms = atom_fields(
        base64.b64decode(artifacts['partner']['content_base64']).decode()
    )
    np.testing.assert_allclose(
        [a['coordinates'] for a in atoms],
        puw.get_value(original.coordinates, to_unit='angstrom'),
        rtol=0,
        atol=0.000500001,
    )
    assert len(history['scores']) == 8 and history['operation'] == 'score'
    return history['scores']


@pytest.mark.parametrize('string_policy', ['current', 'inferred'])
def test_fixed_p59_preserves_current_reference_and_original_protein(string_policy):
    policy = (
        pd.option_context('future.infer_string', True)
        if string_policy == 'inferred'
        else nullcontext()
    )
    with policy:
        cases = prepare_cases()[1]
        preparation = prepare_receptors(
            companion='p59', reference_snapshot=cases['p59']['reference_snapshot']
        )
    sham = atom_fields(preparation['receptors']['sham']['pdbqt'])
    occupied = atom_fields(preparation['receptors']['occupied']['pdbqt'])
    assert len(sham) == 1481 and len(occupied) == 1506
    assert (
        occupied[:1481]
        == sham
        == atom_fields((DATA / '5x72_receptor.pdbqt').read_text())
    )
    np.testing.assert_allclose(
        [a['coordinates'] for a in occupied[1481:1505]],
        cases['p59']['reference_coordinates_angstrom'],
        rtol=0,
        atol=0.000501,
    )
    addition = preparation['hydrogen_addition']
    assert addition['n_added_hydrogens'] == 15
    assert addition['original_coordinates_preserved'] is True
    assert addition['parameters']['optimize'] is False
    assert addition['mode'] == 'fixed_chemical_state'
    assert preparation['companion_charge_audit']['assessment'] == 'consistent'
    assert preparation['companion_assessment']['assessment'] == 'unassessed'
    assert preparation['companion_pdbqt_to_generated_source'] == [*range(24), 29]
    assert preparation['explicit_chain_map']['chain_ids'] == ['A', 'A']


@pytest.mark.parametrize('order', ['native', 'first_fixed'])
def test_saved_p69_geometry_keeps_its_tree_under_pm_fs(prepared, order):
    case, _ = prepared
    run = next(
        r
        for r in load_baseline()['new_runs']
        if r['ligand'] == 'p69' and r['order'] == order
    )
    original = dmt.DockingResult.from_dict(run['result']).poses[0]
    with puw.context(standard_units=UNITS):
        written = frozen_partner(case['controls'][order], original)
        atoms = atom_fields(written)
        assert [a['id'] for a in atoms] == [
            a['id'] for a in atom_fields(case['controls'][order]['pdbqt'])
        ]
        np.testing.assert_allclose(
            [a['coordinates'] for a in atoms],
            puw.get_value(original.coordinates, to_unit='angstrom'),
            rtol=0,
            atol=0.000500001,
        )


def test_live_reciprocal_search_and_both_frozen_contexts_under_pm_fs(prepared):
    case, preparation = prepared
    control = case['controls']['first_fixed']
    receptors = {k: v['pdbqt'] for k, v in preparation['receptors'].items()}
    with puw.context(standard_units=UNITS):
        result = dmt.dock(
            dmt.DockingProblem(
                receptors['occupied'], control['pdbqt'], reference_box()
            ),
            dmt.VinaProtocol(
                cpu=1, seed=42, exhaustiveness=1, n_poses=1, capture_backend_inputs=True
            ),
        )
        assert len(result.poses) == 1 and result.poses[0].n_atoms == 25
        assert dmt.verify_captured_inputs(result.provenance['backend_artifacts'])
        assert len(measure(result, case, control)) == 1
        original = result.poses[0]
        before = original.to_dict()
        for name, data in fixed_pair(original, control, receptors).items():
            assert_evaluation(data, original, receptors[name])
        assert original.to_dict() == before
    # Software guard: no stochastic recovery or score-value promise.


def test_saved_reciprocal_matrix_and_all_historical_serialization_controls():
    checkpoint = json.loads((OUTPUT.parent / 'checkpoint_2026-10-09.json').read_text())
    assert sha(OUTPUT.read_bytes()) == checkpoint['producer_archive']['gzip_sha256']
    record = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    assert record['baseline_sha256'] == BASELINE_SHA
    assert record['searched_ligand'] == 'p69' and record['fixed_companion'] == 'p59'
    assert record['criterion'] == load_baseline()['criterion']
    baseline = [r for r in load_baseline()['new_runs'] if r['ligand'] == 'p69']
    historical = record['historical_serialization_scores']
    assert len(baseline) == len(historical) == 12
    cells = set()
    pose_count = 0
    with puw.context(standard_units=UNITS):
        for run in record['new_runs']:
            assert run['ligand'] == 'p69'
            parameters = run['result']['protocol_info']['parameters']
            cells.add(
                (
                    f'{run["receptor"]}_{run["order"]}',
                    parameters['seed'],
                    parameters['exhaustiveness'],
                )
            )
            result = dmt.DockingResult.from_dict(run['result'])
            case = record['cases']['p69']
            measured = measure(result, case, case['controls'][run['order']])
            for current, saved in zip(measured, run['heavy_atom_metrics'], strict=True):
                for key in ('rank', 'recovered', 'vina_score_kcal_mol'):
                    assert current[key] == saved[key]
                assert current['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
                    saved['heavy_atom_positional_rmsd_angstrom'], abs=1e-10
                )
            artifacts = result.provenance['backend_artifacts']
            assert dmt.verify_captured_inputs(artifacts)
            assert (
                artifacts['receptor']['sha256']
                == record['preparation']['receptors'][run['receptor']]['sha256']
            )
            assert len(run['fixed_scores']) == len(result.poses)
            for original, pair in zip(result.poses, run['fixed_scores'], strict=True):
                assert set(pair) == {'sham', 'occupied'}
                for name, data in pair.items():
                    assert_evaluation(
                        data,
                        original,
                        record['preparation']['receptors'][name]['pdbqt'],
                    )
            pose_count += len(result.poses)
            if run['receptor'] == 'sham':
                prior = next(
                    r
                    for r in baseline
                    if r['order'] == run['order']
                    and r['result']['protocol_info']['parameters'] == parameters
                )
                for old, new in zip(
                    dmt.DockingResult.from_dict(prior['result']).poses,
                    result.poses,
                    strict=True,
                ):
                    np.testing.assert_array_equal(
                        puw.get_value(old.coordinates, to_unit='angstrom'),
                        puw.get_value(new.coordinates, to_unit='angstrom'),
                    )
                    assert old.scores == new.scores
        assert cells == set(itertools.product(ARMS, (7, 42, 2026), (1, 8)))
        assert len(record['new_runs']) == 24
        assert pose_count == checkpoint['new_returned_poses']
        assert record['comparison_rows'] == diagnostic_rows(record['new_runs'])
        prior_count = 0
        for prior, observed in zip(baseline, historical, strict=True):
            assert (
                observed['order'] == prior['order']
                and observed['protocol'] == prior['result']['protocol_info']
            )
            for original, pair in zip(
                dmt.DockingResult.from_dict(prior['result']).poses,
                observed['fixed_scores'],
                strict=True,
            ):
                a = assert_evaluation(
                    pair['original'],
                    original,
                    (DATA / '5x72_receptor.pdbqt').read_text(),
                )
                b = assert_evaluation(
                    pair['sham'],
                    original,
                    record['preparation']['receptors']['sham']['pdbqt'],
                )
                assert a == b
                prior_count += 1
        assert prior_count == 49
