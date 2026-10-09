"""Rigid co-occupant identity, frozen geometry and complete saved populations."""

import base64
import gzip
import itertools
import json

import numpy as np
import pandas as pd
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_occupancy import (
    ARMS,
    BASELINE_SHA,
    DATA,
    OUTPUT,
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


@pytest.fixture(scope='module')
def prepared():
    cases = prepare_cases()[1]
    return cases['p59'], prepare_receptors(
        reference_snapshot=cases['p69']['reference_snapshot']
    )


def assert_score(evaluation, original, receptor):
    pose = dmt.DockingPose.from_dict(evaluation)
    history = pose.metadata['scoring_history'][-1]
    artifacts = history['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    assert (
        base64.b64decode(artifacts['receptor']['content_base64']) == receptor.encode()
    )
    assert pose.rank == original.rank
    assert pose.scores['vina'] == original.scores['vina']
    np.testing.assert_allclose(
        puw.get_value(pose.coordinates, to_unit='angstrom'),
        puw.get_value(original.coordinates, to_unit='angstrom'),
        rtol=0,
        atol=1e-12,
    )
    written = atom_fields(
        base64.b64decode(artifacts['partner']['content_base64']).decode()
    )
    np.testing.assert_allclose(
        [a['coordinates'] for a in written],
        puw.get_value(original.coordinates, to_unit='angstrom'),
        rtol=0,
        atol=0.000500001,
    )
    assert len(history['scores']) == 8
    assert history['operation'] == 'score'
    return pose


def test_fixed_p69_preserves_protein_and_experimental_heavy_coordinates(prepared):
    _, preparation = prepared
    sham = atom_fields(preparation['receptors']['sham']['pdbqt'])
    occupied = atom_fields(preparation['receptors']['occupied']['pdbqt'])
    assert len(sham) == 1481 and len(occupied) == 1506
    assert sham == atom_fields((DATA / '5x72_receptor.pdbqt').read_text())
    assert occupied[:1481] == sham
    assert preparation['protein_atom_field_changes'] == []
    assert preparation['companion_charge_audit']['assessment'] == 'consistent'
    assert preparation['companion_assessment']['assessment'] == 'unassessed'
    addition = preparation['hydrogen_addition']
    assert addition['n_added_hydrogens'] == 15
    assert addition['original_coordinates_preserved'] is True
    assert addition['parameters']['optimize'] is False
    assert addition['mode'] == 'fixed_chemical_state'
    assert preparation['companion_pdbqt_to_generated_source'] == [*range(24), 29]
    bound = np.asarray(
        load_baseline()['cases']['p69']['reference_coordinates_angstrom']
    )
    np.testing.assert_allclose(
        [a['coordinates'] for a in occupied[1481:1505]], bound, rtol=0, atol=0.000501
    )
    assert preparation['explicit_chain_map']['chain_ids'] == ['A', 'A']


def test_current_string_dtype_annotations_do_not_replace_historical_identity():
    with pd.option_context('future.infer_string', True):
        cases = prepare_cases()[1]
        reference = cases['p69']['reference_snapshot']
        historical = load_baseline()['cases']['p69']['reference_snapshot']
        assert reference != historical
        # The scientific producer still refuses a different historical profile.
        with pytest.raises(AssertionError):
            prepare_receptors()
        preparation = prepare_receptors(reference_snapshot=reference)
        assert atom_fields(preparation['receptors']['sham']['pdbqt']) == atom_fields(
            (DATA / '5x72_receptor.pdbqt').read_text()
        )
        bound = cases['p69']['reference_coordinates_angstrom']
        occupied = atom_fields(preparation['receptors']['occupied']['pdbqt'])
        np.testing.assert_allclose(
            [a['coordinates'] for a in occupied[1481:1505]],
            bound,
            rtol=0,
            atol=0.000501,
        )


def test_both_saved_root_orders_keep_frozen_tree_and_geometry_under_pm_fs(prepared):
    case, _ = prepared
    baseline = load_baseline()
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        for order in ('native', 'first_fixed'):
            run = next(
                r
                for r in baseline['new_runs']
                if r['ligand'] == 'p59' and r['order'] == order
            )
            pose = dmt.DockingResult.from_dict(run['result']).poses[0]
            written = frozen_partner(case['controls'][order], pose)
            atoms = atom_fields(written)
            assert [a['id'] for a in atoms] == [
                a['id'] for a in atom_fields(case['controls'][order]['pdbqt'])
            ]
            np.testing.assert_allclose(
                [a['coordinates'] for a in atoms],
                puw.get_value(pose.coordinates, to_unit='angstrom'),
                rtol=0,
                atol=0.000500001,
            )


def test_live_fixed_companion_search_and_frozen_scores_under_pm_fs(prepared):
    case, preparation = prepared
    control = case['controls']['first_fixed']
    receptors = {k: v['pdbqt'] for k, v in preparation['receptors'].items()}
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
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
        before = result.poses[0].to_dict()
        scored = fixed_pair(result.poses[0], control, receptors)
        for receptor, evaluation in scored.items():
            assert_score(evaluation, result.poses[0], receptors[receptor])
        assert result.poses[0].to_dict() == before
    # These are software guards, not a stochastic experimental recovery promise.


def test_all_saved_cells_and_frozen_scores_use_complete_declared_populations():
    checkpoint = json.loads((OUTPUT.parent / 'checkpoint_2026-10-09.json').read_text())
    assert sha(OUTPUT.read_bytes()) == checkpoint['producer_archive']['gzip_sha256']
    record = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    assert record['baseline_sha256'] == BASELINE_SHA
    preparation = record['preparation']
    assert record['criterion'] == load_baseline()['criterion']
    cells = set()
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        for run in record['new_runs']:
            parameters = run['result']['protocol_info']['parameters']
            cells.add(
                (
                    f'{run["receptor"]}_{run["order"]}',
                    parameters['seed'],
                    parameters['exhaustiveness'],
                )
            )
            result = dmt.DockingResult.from_dict(run['result'])
            case = record['cases']['p59']
            metrics = measure(result, case, case['controls'][run['order']])
            for measured, saved in zip(metrics, run['heavy_atom_metrics'], strict=True):
                assert measured['rank'] == saved['rank']
                assert measured['recovered'] == saved['recovered']
                assert measured['vina_score_kcal_mol'] == saved['vina_score_kcal_mol']
                assert measured['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
                    saved['heavy_atom_positional_rmsd_angstrom'], abs=1e-10
                )
            artifacts = result.provenance['backend_artifacts']
            assert dmt.verify_captured_inputs(artifacts)
            receptor = preparation['receptors'][run['receptor']]
            assert (
                artifacts['receptor']['sha256']
                == receptor['sha256']
                == sha(receptor['pdbqt'].encode())
            )
            assert len(run['fixed_scores']) == len(result.poses)
            for original, pair in zip(result.poses, run['fixed_scores'], strict=True):
                assert set(pair) == {'sham', 'occupied'}
                for name, scored in pair.items():
                    assert_score(
                        scored, original, preparation['receptors'][name]['pdbqt']
                    )
    assert cells == set(itertools.product(ARMS, (7, 42, 2026), (1, 8)))
    assert record['comparison_rows'] == diagnostic_rows(record['new_runs'])
    historical = [r for r in load_baseline()['new_runs'] if r['ligand'] == 'p59']
    assert len(record['historical_serialization_scores']) == len(historical) == 12
    for prior, observed in zip(
        historical, record['historical_serialization_scores'], strict=True
    ):
        assert (
            observed['order'] == prior['order']
            and observed['protocol'] == prior['result']['protocol_info']
        )
        assert len(observed['fixed_scores']) == len(prior['heavy_atom_metrics'])
        for original, pair in zip(
            dmt.DockingResult.from_dict(prior['result']).poses,
            observed['fixed_scores'],
            strict=True,
        ):
            a = assert_score(
                pair['original'], original, (DATA / '5x72_receptor.pdbqt').read_text()
            )
            b = assert_score(
                pair['sham'], original, preparation['receptors']['sham']['pdbqt']
            )
            np.testing.assert_allclose(
                [v for k, v in a.scores.items() if k.startswith('fixed')],
                [v for k, v in b.scores.items() if k.startswith('fixed')],
                rtol=0,
                atol=1e-12,
            )
