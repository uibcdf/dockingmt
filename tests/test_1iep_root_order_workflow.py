"""Frozen-origin order intervention and independent written-axis metrics."""

import gzip
import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_1iep_representation import fixed_score, observe, sha
from devtools.qualify_1iep_root_order import (
    OUTPUT,
    VARIANT,
    comparison_rows,
    fixed_first_control,
    load_baseline,
    prepare_control,
)


@pytest.fixture(scope='module')
def prepared_control():
    # Portable regression inputs; exact historical runtime reuse is a separate
    # scientific gate in the qualification driver.
    return prepare_control()


def test_first_root_atom_and_every_unpermuted_byte_are_preserved(prepared_control):
    _, control, baseline, _ = prepared_control
    native = baseline['controls']['native']['pdbqt'].encode()
    original = native.splitlines(keepends=True)
    changed = control['pdbqt'].encode().splitlines(keepends=True)
    first, last = original.index(b'ROOT\n') + 1, original.index(b'ENDROOT\n')
    assert last - first == 8
    assert changed[: first + 1] == original[: first + 1]
    assert changed[first + 1 : last] == original[first + 1 : last][::-1]
    assert changed[last:] == original[last:]
    assert sorted(changed) == sorted(original)
    assert control['pdbqt_to_source_atom_indices'][:8] == [
        28,
        58,
        34,
        33,
        32,
        31,
        30,
        29,
    ]
    assert control['first_root_source_atom_index'] == 28
    assert control['first_root_record'].encode() == original[first].rstrip(b'\n')
    assert control['rigid_body_origin_angstrom'] == [16.917, 46.907, 20.219]
    assert control['atom_comparison']['matched_atom_type_disagreements'] == 0
    assert control['atom_comparison']['matched_charge_max_absolute_difference_e'] == 0
    assert control['torsion_graph_comparison']['branch_bonds_match']
    assert control['torsion_graph_comparison']['rigid_fragments_match']
    with pytest.raises(ValueError, match='declared native'):
        fixed_first_control(native.replace(b'TORSDOF 7', b'TORSDOF 6'))


def test_fixed_conformation_scoring_preserves_geometry_and_components(prepared_control):
    _, control, baseline, _ = prepared_control
    scored = fixed_score(control, VARIANT)
    native = fixed_score(baseline['controls']['native'], 'native')
    names = tuple(native['scores'])
    np.testing.assert_allclose(
        [scored['scores'][name] for name in names],
        [native['scores'][name] for name in names],
        rtol=0,
        atol=0.001,
    )
    history = scored['metadata']['scoring_history'][0]
    assert history['unused_search_parameters'] == [
        'exhaustiveness',
        'n_poses',
        'energy_range',
    ]
    assert dmt.verify_captured_inputs(history['backend_artifacts'])
    assert history['backend_artifacts']['partner']['sha256'] == control['sha256']
    written = [
        [float(line[start : start + 8]) for start in (30, 38, 46)]
        for line in control['pdbqt'].splitlines()
        if line.startswith('ATOM')
    ]
    np.testing.assert_allclose(
        puw.get_value(
            dmt.DockingPose.from_dict(scored).coordinates, to_unit='angstrom'
        ),
        written,
        rtol=0,
        atol=1e-12,
    )


def assert_observed_geometry(run, xyz, control):
    result = dmt.DockingResult.from_dict(run['result'])
    assert result.poses
    artifacts = result.provenance['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    assert artifacts['partner']['sha256'] == control['sha256']
    assert (
        run['pdbqt_to_source_atom_indices'] == control['pdbqt_to_source_atom_indices']
    )
    indices, heavy = run['pdbqt_to_source_atom_indices'], run['heavy_pdbqt_indices']
    assert sorted(indices[i] for i in heavy) == list(range(37))
    for pose, row, metric in zip(
        result.poses, run['evaluation']['poses'], run['heavy_atom_metrics'], strict=True
    ):
        squared = np.sum(
            (puw.get_value(pose.coordinates, to_unit='angstrom') - xyz[indices]) ** 2,
            axis=-1,
        )
        assert row['rmsd'] == pytest.approx(np.sqrt(squared.mean()), abs=1e-10)
        assert metric['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
            np.sqrt(squared[heavy].mean()), abs=1e-10
        )
        assert row['recovered'] is (row['rmsd'] <= 2.5)


def test_live_fixed_origin_search_retains_mapping_under_pm_fs(prepared_control):
    source, control, _, _ = prepared_control
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        run = observe(source, control, variant=VARIANT, seed=42, exhaustiveness=1)
    assert (
        run['evaluation']['criterion']['atom_correspondence']
        == 'caller_declared_positional'
    )
    assert (
        run['result']['protocol_info']['parameters']['allow_provisional_preparation']
        is False
    )
    assert (
        run['result']['provenance']['preparation']['partner']['assessment']
        == 'unassessed'
    )
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[0]
    assert_observed_geometry(run, xyz, control)


def test_saved_six_cells_preserve_authenticated_baseline_and_actual_geometry():
    record = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    baseline = load_baseline()
    assert record['audit']['source_snapshot'] == baseline['audit']['source_snapshot']
    assert record['baseline']['sha256'] == sha(
        (OUTPUT.parents[4] / record['baseline']['path']).read_bytes()
    )
    assert (
        record['baseline']['published_by'] == 'dd571ef4dd0a1ddc9142e399a6da3683299a1db4'
    )
    assert (
        record['baseline']['original_native_producer']
        == '7b11391e153f77f340fd039bc799352f90da83d3'
    )
    assert record['control']['pdbqt'].encode() == fixed_first_control(
        baseline['controls']['native']['pdbqt'].encode()
    )
    assert len(record['new_runs']) == 6
    assert record['comparison_rows'] == comparison_rows(record, baseline)
    assert len(record['comparison_rows']) == 24
    cells = set()
    xyz = puw.get_value(
        puw.quantity(
            record['audit']['source_snapshot']['structures']['coordinates'], 'nm'
        ),
        to_unit='angstrom',
    )[0]
    for run in record['new_runs']:
        parameters = run['result']['protocol_info']['parameters']
        assert run['variant'] == VARIANT
        cells.add((parameters['seed'], parameters['exhaustiveness']))
        assert_observed_geometry(run, xyz, record['control'])
    assert cells == {(seed, effort) for seed in (7, 42, 2026) for effort in (1, 8)}
    assert (
        record['fixed_conformation_score']['scores']
        == baseline['fixed_conformation_scores']['native']['scores']
    )
