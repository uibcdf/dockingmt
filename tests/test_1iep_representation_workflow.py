"""Frozen representation inputs, actual pose maps and independent RMSDs."""

import gzip
import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_1iep_representation import (
    OUTPUT,
    fixed_score,
    observe,
    prepare_controls,
    root_order_control,
)


@pytest.fixture(scope='module')
def prepared_controls():
    # Regression guards do not claim qualification of this runtime against a
    # historical producer. Scientific reuse separately requires verify_profile.
    return prepare_controls()


def test_order_control_preserves_every_line_and_root_membership(prepared_controls):
    _, controls, _, _ = prepared_controls
    original = controls['native']['pdbqt'].encode()
    reordered = controls['native_root_reversed']['pdbqt'].encode()
    lines = original.splitlines(keepends=True)
    changed = reordered.splitlines(keepends=True)
    first, last = lines.index(b'ROOT\n') + 1, lines.index(b'ENDROOT\n')
    assert len(lines[first:last]) == 8
    assert changed[:first] == lines[:first]
    assert changed[first:last] == lines[first:last][::-1]
    assert changed[last:] == lines[last:]
    assert sorted(lines) == sorted(changed)
    mapping = controls['native']['pdbqt_to_source_atom_indices']
    assert controls['native_root_reversed']['pdbqt_to_source_atom_indices'] == (
        mapping[:8][::-1] + mapping[8:]
    )
    assert mapping[:8] == [28, 29, 30, 31, 32, 33, 34, 58]
    assert controls['published']['pdbqt_to_source_atom_indices'][:4] == [19, 20, 35, 47]
    for control in controls.values():
        assert sorted(control['pdbqt_to_source_atom_indices']) == list(range(37)) + [
            43,
            47,
            58,
        ]
        assert control['atom_comparison']['matched_atom_type_disagreements'] == 0
        assert (
            control['atom_comparison']['matched_charge_max_absolute_difference_e'] == 0
        )
        assert control['torsion_graph_comparison']['branch_bonds_match']
        assert control['torsion_graph_comparison']['rigid_fragments_match']
    with pytest.raises(ValueError, match='declared native'):
        root_order_control(original.replace(b'TORSDOF 7', b'TORSDOF 6'))


def test_equivalent_input_conformation_scores_without_search(prepared_controls):
    _, controls, _, _ = prepared_controls
    scored = {name: fixed_score(control, name) for name, control in controls.items()}
    names = tuple(scored['native']['scores'])
    for name, pose in scored.items():
        np.testing.assert_allclose(
            [pose['scores'][key] for key in names],
            [scored['native']['scores'][key] for key in names],
            rtol=0,
            atol=0.001,
        )
        history = pose['metadata']['scoring_history'][0]
        assert history['unused_search_parameters'] == [
            'exhaustiveness',
            'n_poses',
            'energy_range',
        ]
        assert dmt.verify_captured_inputs(history['backend_artifacts'])
        assert (
            history['backend_artifacts']['partner']['sha256']
            == controls[name]['sha256']
        )
        written = [
            [float(line[start : start + 8]) for start in (30, 38, 46)]
            for line in controls[name]['pdbqt'].splitlines()
            if line.startswith('ATOM')
        ]
        np.testing.assert_allclose(
            puw.get_value(
                dmt.DockingPose.from_dict(pose).coordinates, to_unit='angstrom'
            ),
            written,
            rtol=0,
            atol=1e-12,
        )


def assert_geometry(run, source_xyz):
    result = dmt.DockingResult.from_dict(run['result'])
    assert result.poses
    assert dmt.verify_captured_inputs(result.provenance['backend_artifacts'])
    indices = run['pdbqt_to_source_atom_indices']
    heavy = run['heavy_pdbqt_indices']
    assert sorted(indices[i] for i in heavy) == list(range(37))
    for pose, row, metric in zip(
        result.poses, run['evaluation']['poses'], run['heavy_atom_metrics'], strict=True
    ):
        xyz = puw.get_value(pose.coordinates, to_unit='angstrom')
        squared = np.sum((xyz - source_xyz[indices]) ** 2, axis=-1)
        assert row['rmsd'] == pytest.approx(np.sqrt(squared.mean()), abs=1e-10)
        assert metric['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
            np.sqrt(squared[heavy].mean()), abs=1e-10
        )
        assert row['recovered'] is (row['rmsd'] <= 2.5)


@pytest.mark.parametrize('variant', ['published', 'native_root_reversed'])
def test_live_representation_retains_actual_written_order(prepared_controls, variant):
    source, controls, _, _ = prepared_controls
    run = observe(source, controls[variant], variant=variant, seed=42, exhaustiveness=1)
    assert (
        run['result']['protocol_info']['parameters']['allow_provisional_preparation']
        is False
    )
    assert (
        run['result']['provenance']['preparation']['partner']['assessment']
        == 'unassessed'
    )
    assert (
        run['evaluation']['criterion']['atom_correspondence']
        == 'caller_declared_positional'
    )
    source_xyz = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[0]
    assert_geometry(run, source_xyz)


def test_saved_matched_matrix_retains_each_original_producer():
    record = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    assert len(record['original_native_runs']) == 6
    assert len(record['new_runs']) == 12
    assert (
        record['baseline']['source_producer']
        == '7b11391e153f77f340fd039bc799352f90da83d3'
    )
    original = json.loads(
        gzip.decompress((OUTPUT.parents[4] / record['baseline']['path']).read_bytes())
    )
    assert record['original_native_runs'] == [
        run for run in original['redocking_runs'] if run['variant'] == 'flexible'
    ]

    def params(run):
        return run['result']['protocol_info']['parameters']

    assert {
        (run['variant'], params(run)['seed'], params(run)['exhaustiveness'])
        for run in record['new_runs']
    } == {
        (variant, seed, effort)
        for variant in ('published', 'native_root_reversed')
        for seed in (7, 42, 2026)
        for effort in (1, 8)
    }
    source_xyz = puw.get_value(
        puw.quantity(
            record['audit']['source_snapshot']['structures']['coordinates'], 'nm'
        ),
        to_unit='angstrom',
    )[0]
    for run in (
        record['original_native_runs'] + record['new_runs'] + [record['native_repeat']]
    ):
        assert_geometry(run, source_xyz)
    assert (
        record['native_repeat']['result']['provenance']['backend_artifacts']['partner'][
            'sha256'
        ]
        == record['controls']['native']['sha256']
    )
