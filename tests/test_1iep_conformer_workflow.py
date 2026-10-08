"""Original-reference and input-identity guards for torsion-perturbed redocking."""

import base64
import gzip
import json

import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_1iep_conformers import (
    BASELINE,
    BASELINE_SHA256,
    OUTPUT,
    comparison_rows,
    load_baseline,
    prepare_cases,
    score_observation,
    xyz,
)
from devtools.qualify_1iep_representation import fixed_score, observe, sha
from devtools.qualify_1iep_root_order import load_baseline as load_representation


@pytest.fixture(scope='module')
def cases():
    return prepare_cases()


def assert_metrics(run, reference_xyz, control):
    """Independently measure every saved pose against the ORIGINAL reference."""
    result = dmt.DockingResult.from_dict(run['result'])
    artifacts = result.provenance['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    assert artifacts['partner']['sha256'] == control['sha256']
    assert (
        base64.b64decode(artifacts['partner']['content_base64'])
        == control['pdbqt'].encode()
    )
    indices = control['pdbqt_to_source_atom_indices']
    heavy = control['heavy_pdbqt_indices']
    assert run['pdbqt_to_source_atom_indices'] == indices
    assert sorted(indices[i] for i in heavy) == list(range(37))
    for pose, evaluated, metric in zip(
        result.poses, run['evaluation']['poses'], run['heavy_atom_metrics'], strict=True
    ):
        coordinates = puw.get_value(pose.coordinates, to_unit='angstrom')
        squared = np.sum((coordinates - reference_xyz[indices]) ** 2, axis=-1)
        assert evaluated['rmsd'] == pytest.approx(np.sqrt(squared.mean()), abs=1e-10)
        assert metric['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
            np.sqrt(squared[heavy].mean()), abs=1e-10
        )
        assert evaluated['recovered'] is (evaluated['rmsd'] <= 2.5)
    return result


def test_public_geometry_keeps_chemistry_and_original_reference_under_pm_fs(cases):
    source, default, *_ = cases
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        shifted_source, alternate, *_ = prepare_cases()
    np.testing.assert_allclose(xyz(source), xyz(shifted_source), rtol=0, atol=1e-10)
    for name, case in alternate.items():
        assert case['heavy_input_positional_rmsd_angstrom'] > 2.5
        assert case['max_bond_length_change_angstrom'] < 1e-10
        assert case['max_bond_angle_change_degree'] < 1e-8
        assert case['max_signed_volume_change_angstrom3'] < 1e-9
        before = np.array(case['dihedrals_before_degree'])
        after = np.array(case['dihedrals_after_degree'])
        delta = (after - before + 180) % 360 - 180
        expected = np.zeros(7)
        expected[2] = 60 if name == 'plus60' else -60
        np.testing.assert_allclose(delta, expected, rtol=0, atol=1e-8)
        for order, control in case['controls'].items():
            reference = default[name]['controls'][order]
            assert (
                control['pdbqt_to_source_atom_indices']
                == reference['pdbqt_to_source_atom_indices']
            )
            written = np.array(
                [
                    [float(line[i : i + 8]) for i in (30, 38, 46)]
                    for line in control['pdbqt'].splitlines()
                    if line.startswith('ATOM')
                ]
            )
            original_written = np.array(
                [
                    [float(line[i : i + 8]) for i in (30, 38, 46)]
                    for line in reference['pdbqt'].splitlines()
                    if line.startswith('ATOM')
                ]
            )
            np.testing.assert_allclose(written, original_written, rtol=0, atol=0.001001)
        native = case['controls']['native']['pdbqt'].splitlines(keepends=True)
        fixed = case['controls']['first_fixed']['pdbqt'].splitlines(keepends=True)
        start, end = native.index('ROOT\n') + 1, native.index('ENDROOT\n')
        assert fixed[: start + 1] == native[: start + 1]
        assert fixed[start + 1 : end] == native[start + 1 : end][::-1]
        assert fixed[end:] == native[end:]


def test_same_perturbed_geometry_scores_equally_for_both_written_orders(cases):
    _, prepared, *_ = cases
    case = prepared['plus60']
    scores = {
        order: fixed_score(control, f'plus60_{order}')
        for order, control in case['controls'].items()
    }
    np.testing.assert_allclose(
        list(scores['native']['scores'].values()),
        list(scores['first_fixed']['scores'].values()),
        rtol=0,
        atol=0.001,
    )
    for order, pose in scores.items():
        history = pose['metadata']['scoring_history'][0]
        assert dmt.verify_captured_inputs(history['backend_artifacts'])
        assert (
            history['backend_artifacts']['partner']['sha256']
            == case['controls'][order]['sha256']
        )
    for order, control in prepared['minus60']['controls'].items():
        refused = score_observation(control, f'minus60_{order}')
        assert refused['status'] == 'rejected_outside_grid'
        assert refused['submitted_partner_sha256'] == control['sha256']
        assert 'outside the grid box' in refused['message']


def test_live_perturbed_search_uses_original_reference_and_captured_input(cases):
    source, prepared, *_ = cases
    control = prepared['minus60']['controls']['native']
    run = observe(source, control, variant='minus60_native', seed=42, exhaustiveness=1)
    result = assert_metrics(run, xyz(source), control)
    assert result.provenance['preparation']['partner']['assessment'] == 'unassessed'
    assert (
        run['evaluation']['criterion']['atom_correspondence']
        == 'caller_declared_positional'
    )
    moved = (
        np.array(prepared['minus60']['source_snapshot']['structures']['coordinates'])[0]
        * 10
    )
    indices = control['pdbqt_to_source_atom_indices']
    returned = puw.get_value(result.poses[0].coordinates, to_unit='angstrom')
    perturbed_rmsd = np.sqrt(np.mean(np.sum((returned - moved[indices]) ** 2, axis=-1)))
    assert abs(perturbed_rmsd - run['evaluation']['poses'][0]['rmsd']) > 0.01


def test_saved_24_cells_preserve_reference_producers_and_each_geometry():
    record = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    baseline, representation = load_baseline(), load_representation()
    assert sha(BASELINE.read_bytes()) == record['baseline']['sha256'] == BASELINE_SHA256
    assert record['audit']['source_snapshot'] == baseline['audit']['source_snapshot']
    assert (
        record['baseline']['native_producer']
        == '7b11391e153f77f340fd039bc799352f90da83d3'
    )
    assert (
        record['baseline']['fixed_first_producer']
        == '2f2ee8f7cebe9b07e5ac240937896dfaf9df197e'
    )
    assert record['comparison_rows'] == comparison_rows(
        record, baseline, representation
    )
    assert len(record['comparison_rows']) == 36
    original = (
        np.array(record['audit']['source_snapshot']['structures']['coordinates'])[0]
        * 10
    )
    cells = set()
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        for run in record['new_runs']:
            geometry, order = run['geometry'], run['order']
            p = run['result']['protocol_info']['parameters']
            cells.add((geometry, order, p['seed'], p['exhaustiveness']))
            assert_metrics(run, original, record['cases'][geometry]['controls'][order])
    assert len(record['new_runs']) == 24
    assert cells == {
        (g, o, s, e)
        for g in ('plus60', 'minus60')
        for o in ('native', 'first_fixed')
        for s in (7, 42, 2026)
        for e in (1, 8)
    }
    for geometry, scores in record['fixed_conformation_scores'].items():
        assert scores['native']['status'] == scores['first_fixed']['status']
        if geometry == 'plus60':
            assert scores['native']['status'] == 'scored'
            assert (
                scores['native']['pose']['scores']
                == scores['first_fixed']['pose']['scores']
            )
        else:
            assert scores['native']['status'] == 'rejected_outside_grid'
