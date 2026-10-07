"""Independent geometry and report semantics for public redocking evaluation."""

import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.results import _molecular_atom_keys


@pytest.fixture
def reference():
    return msm.extract(
        msm.convert(
            msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
            to_form='molsysmt.MolSys',
        ),
        selection=[0, 1, 2],
    )


def make_pose(reference, distance, *, rank=None, pose_id=None, order=None):
    keys = _molecular_atom_keys(reference)
    coordinates = puw.get_value(
        msm.get(reference, coordinates=True), to_unit='angstrom'
    )[0].copy()
    coordinates[:, 0] += distance
    if order is not None:
        coordinates = coordinates[order]
        keys = [keys[index] for index in order]
    return dmt.DockingPose(
        puw.quantity(coordinates, 'angstrom'),
        rank=rank,
        pose_id=pose_id,
        scores={'control': -100 + distance},
        metadata={'pose_atom_order': 'verified_pdbqt_order', 'source_atom_keys': keys},
    )


def evaluate(result, reference, **kwargs):
    return dmt.evaluate_redocking(
        result, reference, rmsd_cutoff=puw.quantity(2, 'angstrom'), **kwargs
    )


def test_translation_first_position_closest_and_top_n(reference):
    poses = [
        make_pose(reference, 4, rank=1, pose_id='far'),
        make_pose(reference, 1, rank=2, pose_id='near'),
    ]
    result = dmt.DockingResult(poses)
    report = evaluate(result, reference, top_n=(1, 2, 5))
    np.testing.assert_allclose(
        [row['rmsd'] for row in report['poses']], [4, 1], atol=1e-12
    )
    assert report['first_pose']['pose_id'] == 'far'
    assert report['closest_pose']['pose_id'] == 'near'
    assert report['top_n'] == [
        {'requested': 1, 'considered': 1, 'recovered': False},
        {'requested': 2, 'considered': 2, 'recovered': True},
        {'requested': 5, 'considered': 2, 'recovered': True},
    ]
    assert report['criterion']['alignment'] == 'none'
    assert report['criterion']['symmetry_correction'] == 'none'
    assert report['criterion']['atom_correspondence'] == 'verified_source_atom_keys'
    assert report['criterion']['top_n_basis'] == 'result_order'
    assert result.poses == poses


def test_permuted_pose_mapping_and_tied_closest_keep_input_order(reference):
    result = dmt.DockingResult(
        [make_pose(reference, 0, order=[2, 0, 1]), make_pose(reference, 0)]
    )
    report = evaluate(result, reference)
    assert [row['rmsd'] for row in report['poses']] == pytest.approx([0, 0])
    assert report['closest_pose']['position'] == 1


def test_reordered_molecular_reference_uses_verified_identity(reference):
    pose = make_pose(reference, 0)
    reordered = msm.extract(reference, selection=[2, 0, 1])
    assert evaluate(dmt.DockingResult([pose]), reordered)['poses'][0][
        'rmsd'
    ] == pytest.approx(0)


def test_current_positions_are_independent_of_declared_ranks(reference):
    result = dmt.DockingResult(
        [make_pose(reference, 5, rank=9), make_pose(reference, 0, rank=1)]
    )
    report = evaluate(result, reference)
    assert report['first_pose']['rank'] == 9
    assert report['top_n'][0]['recovered'] is False
    assert result.top_pose.rank == 1


def test_report_is_finite_json_detached_and_excludes_captured_payloads(reference):
    result = dmt.DockingResult(
        [make_pose(reference, 0)],
        problem_info={
            'metadata': {'case': ['original']},
            'receptor': {'value': 'large payload'},
        },
        protocol_info={'seed': 42},
        provenance={
            'preparation': {'partner': {'assessment': 'provisional'}},
            'backend_artifacts': {
                'partner': {'sha256': 'a' * 64, 'content_base64': 'large payload'}
            },
        },
    )
    info = {'uri': 'caller:reference', 'declared': ['original']}
    before = result.to_dict()
    report = evaluate(result, reference, reference_info=info)
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert result.to_dict() == before
    assert 'receptor' not in report['context']['problem_info']
    assert report['context']['input_artifacts']['partner'] == {'sha256': 'a' * 64}
    report['context']['problem_info']['metadata']['case'].append('changed')
    report['reference']['declared_info']['declared'].append('changed')
    report['first_pose']['scores']['control'] = 42
    assert result.to_dict() == before
    assert info['declared'] == ['original']
    assert report['poses'][0]['scores']['control'] != 42


def test_nondefault_unit_policy_has_explicit_fixed_unit_output(reference):
    result = dmt.DockingResult([make_pose(reference, 3)])
    with puw.context(standard_units=['pm', 'fs']):
        report = dmt.evaluate_redocking(
            result, reference, rmsd_cutoff=puw.quantity(0.2, 'nm')
        )
        assert report['criterion']['unit'] == 'angstrom'
        assert report['criterion']['cutoff'] == pytest.approx(2)
        assert report['poses'][0]['rmsd'] == pytest.approx(3)
        assert report['reference']['coordinates']['unit'] == 'angstrom'
        assert not report['poses'][0]['recovered']


def test_empty_result_has_no_best_pose_or_recovery(reference):
    report = evaluate(dmt.DockingResult([]), reference)
    assert report['n_poses'] == 0
    assert report['first_pose'] is None and report['closest_pose'] is None
    assert all(
        row['considered'] == 0 and not row['recovered'] for row in report['top_n']
    )


def test_explicit_coordinate_reference_is_labelled_positional():
    coordinates = puw.quantity([[0, 0, 0], [1, 0, 0]], 'angstrom')
    pose = dmt.DockingPose(coordinates)
    report = evaluate(dmt.DockingResult([pose]), coordinates)
    assert report['criterion']['atom_correspondence'] == 'caller_declared_positional'
    assert report['poses'][0]['atom_keys'] is None
    assert report['reference']['atom_keys'] is None
    assert report['poses'][0]['recovered']


def test_same_pose_reference_uses_verified_map(reference):
    pose = make_pose(reference, 0)
    assert evaluate(dmt.DockingResult([pose]), pose)['poses'][0][
        'rmsd'
    ] == pytest.approx(0)


@pytest.mark.parametrize(
    'cutoff',
    [
        2,
        True,
        puw.quantity(-1, 'nm'),
        puw.quantity(float('nan'), 'nm'),
        puw.quantity([1], 'nm'),
        puw.quantity(1, 'ps'),
    ],
)
def test_invalid_cutoff_rejected(reference, cutoff):
    with pytest.raises(ArgumentError):
        dmt.evaluate_redocking(dmt.DockingResult([]), reference, rmsd_cutoff=cutoff)


@pytest.mark.parametrize('top_n', [0, (0,), (True,), (1.5,), (), (1, 1), '1'])
def test_invalid_top_positions_rejected(reference, top_n):
    with pytest.raises(ArgumentError):
        evaluate(dmt.DockingResult([]), reference, top_n=top_n)


@pytest.mark.parametrize(
    'info', [{'bad': float('inf')}, {1: 'bad'}, {'bad': object()}, {'bad': (1, 2)}]
)
def test_reference_declarations_require_strict_finite_json(reference, info):
    with pytest.raises(ArgumentError):
        evaluate(dmt.DockingResult([]), reference, reference_info=info)


def test_conflicting_known_states_are_not_aggregated(reference):
    poses = [make_pose(reference, 0), make_pose(reference, 1)]
    poses[0].partner_state_id = 'one'
    poses[1].partner_state_id = 'another'
    with pytest.raises(ArgumentError, match='Conflicting'):
        evaluate(dmt.DockingResult(poses), reference)


def test_different_atom_populations_are_not_aggregated(reference):
    poses = [
        make_pose(reference, 0),
        make_pose(msm.extract(reference, selection=[0, 1]), 0),
    ]
    with pytest.raises(ArgumentError, match='population'):
        evaluate(dmt.DockingResult(poses), reference)


def test_unmapped_pose_against_molecular_reference_is_rejected(reference):
    pose = dmt.DockingPose(puw.quantity(np.zeros((3, 3)), 'angstrom'))
    with pytest.raises(ArgumentError, match='verified source atom map'):
        evaluate(dmt.DockingResult([pose]), reference)


def test_multiframe_reference_rejected(reference):
    reference = msm.extract(reference, structure_indices=[0, 0])
    with pytest.raises(ArgumentError, match='one reference'):
        evaluate(dmt.DockingResult([]), reference)


def test_coordinate_reference_count_and_single_frame_are_required():
    pose = dmt.DockingPose(puw.quantity(np.zeros((2, 3)), 'angstrom'))
    with pytest.raises(ArgumentError, match='atom count'):
        evaluate(dmt.DockingResult([pose]), puw.quantity(np.zeros((3, 3)), 'angstrom'))
    with pytest.raises(ArgumentError, match='one nonempty'):
        evaluate(
            dmt.DockingResult([pose]), puw.quantity(np.zeros((2, 2, 3)), 'angstrom')
        )


def test_nonfinite_pose_is_not_a_failed_recovery(reference):
    pose = make_pose(reference, 0)
    pose.coordinates[0, 0] = puw.quantity(float('nan'), 'nm')
    with pytest.raises(ArgumentError, match='finite'):
        evaluate(dmt.DockingResult([pose]), reference)


def test_complex_coordinate_reference_is_not_silently_cast_to_real():
    coordinates = puw.quantity([[0, 0, 1j]], 'angstrom')
    with pytest.raises(ArgumentError, match='real lengths'):
        evaluate(dmt.DockingResult([]), coordinates)


def test_provider_error_propagates_and_inclusive_cutoff_is_literal(
    reference, monkeypatch
):
    result = dmt.DockingResult([make_pose(reference, 0)])
    monkeypatch.setattr(
        result, 'get_rmsds', lambda **kwargs: [puw.quantity(2, 'angstrom')]
    )
    assert evaluate(result, reference)['poses'][0]['recovered']
    error = RuntimeError('RMSD provider failed')

    def fail(**kwargs):
        raise error

    monkeypatch.setattr(result, 'get_rmsds', fail)
    with pytest.raises(RuntimeError) as caught:
        evaluate(result, reference)
    assert caught.value is error


def test_evaluation_of_saved_coordinates_needs_no_engine_or_viewer():
    program = """
import sys
import dockingmt as dmt
import pyunitwizard as puw
coordinates = puw.quantity([[0, 0, 0]], 'nm')
saved = dmt.DockingResult([dmt.DockingPose(coordinates)]).to_dict()
restored = dmt.DockingResult.from_dict(saved)
report = dmt.evaluate_redocking(restored, coordinates, rmsd_cutoff=puw.quantity(1, 'angstrom'))
assert report['poses'][0]['recovered']
assert 'vina' not in sys.modules and 'molsysviewer' not in sys.modules and 'meeko' not in sys.modules
"""
    subprocess.run(
        [sys.executable, '-c', program], check=True, capture_output=True, text=True
    )


def test_native_181l_external_1iep_and_displaced_box_reports(monkeypatch):
    from devtools.qualify_redocking_evaluation import qualify

    # A seed records the search choice, not a portable recovery guarantee.
    # Independently check the report against every actual returned geometry.
    results = []
    dock = dmt.dock

    def recorded_dock(*args, **kwargs):
        result = dock(*args, **kwargs)
        results.append(result)
        return result

    monkeypatch.setattr(dmt, 'dock', recorded_dock)
    reports = qualify()
    assert len(results) == len(reports) == 3
    for (name, report), result in zip(reports.items(), results):
        assert report['n_poses'] == len(result) > 0, name
        assert dmt.verify_captured_inputs(result.provenance['backend_artifacts'])
        assert report['criterion']['cutoff'] == 2.5
        reference = np.asarray(report['reference']['coordinates']['value'])
        reference_keys = report['reference']['atom_keys']
        for row, pose in zip(report['poses'], result.poses):
            if reference_keys is None:
                target = reference
            else:
                keys = [json.dumps(key, sort_keys=True) for key in reference_keys]
                target = reference[
                    [
                        keys.index(json.dumps(key, sort_keys=True))
                        for key in row['atom_keys']
                    ]
                ]
            coordinates = puw.get_value(pose.coordinates, to_unit='angstrom')
            measured = float(
                np.sqrt(np.mean(np.sum((coordinates - target) ** 2, axis=-1)))
            )
            assert row['rmsd'] == pytest.approx(measured, abs=1e-10), name
            assert row['recovered'] is (row['rmsd'] <= 2.5), (name, row)
        assert report['first_pose'] == report['poses'][0]
        assert report['closest_pose']['rmsd'] == min(
            row['rmsd'] for row in report['poses']
        )
    control = reports['1iep_displaced_domain']
    assert control['n_poses'] > 0
    assert not any(row['recovered'] for row in control['poses'])
    assert control['closest_pose']['rmsd'] > 20
    assert json.loads(json.dumps(reports, allow_nan=False)) == reports


def test_retained_native_positive_and_displaced_observations():
    reports = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / 'devguide/validation/data/redocking_evaluation/cases.json'
        ).read_text()
    )
    assert reports['181l_provisional']['first_pose']['recovered']
    assert reports['1iep_external']['first_pose']['recovered']
    assert not any(
        row['recovered'] for row in reports['1iep_displaced_domain']['poses']
    )


@pytest.mark.parametrize(
    'measurement',
    [
        puw.quantity(float('nan'), 'angstrom'),
        puw.quantity(np.asarray(True), 'angstrom'),
        puw.quantity(1j, 'angstrom'),
        puw.quantity(-1, 'angstrom'),
        puw.quantity([1, 2], 'angstrom'),
    ],
)
def test_invalid_provider_measurement_is_rejected(reference, monkeypatch, measurement):
    result = dmt.DockingResult([make_pose(reference, 0)])
    monkeypatch.setattr(result, 'get_rmsds', lambda **kwargs: [measurement])
    with pytest.raises(ArgumentError, match='scalar length'):
        evaluate(result, reference)


def test_coordinate_comparison_rejects_conflicting_known_atom_order(reference):
    poses = [make_pose(reference, 0), make_pose(reference, 0, order=[2, 0, 1])]
    with pytest.raises(ArgumentError, match='population'):
        evaluate(dmt.DockingResult(poses), msm.get(reference, coordinates=True))


def test_reference_selection_is_resolved_and_does_not_filter_pose_atoms(reference):
    pose = make_pose(reference, 0)
    report = evaluate(dmt.DockingResult([pose]), reference, selection=[0, 1, 2])
    assert report['reference']['selected_atom_indices'] == [0, 1, 2]
    with pytest.raises(ArgumentError, match='Reference atoms'):
        evaluate(dmt.DockingResult([pose]), reference, selection=[0, 1])


def test_unknown_states_remain_unknown(reference):
    poses = [make_pose(reference, 0), make_pose(reference, 1)]
    poses[1].partner_state_id = 'declared'
    report = evaluate(dmt.DockingResult(poses), reference)
    assert report['poses'][0]['partner_state_id'] is None
    assert report['poses'][1]['partner_state_id'] == 'declared'
