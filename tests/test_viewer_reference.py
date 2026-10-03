"""Pose/reference correspondence and observable viewer integration failures."""

from types import SimpleNamespace

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt.core import DockingPose, DockingResult
from dockingmt.core.results import _molecular_atom_keys
from molsysviewer_dockingmt import (
    build_docking_complex_system,
    build_docking_reference_system,
    ensure_runtime,
    render_docking_result,
    set_active_pose,
    set_reference_visibility,
)


@pytest.fixture
def source():
    return msm.convert(
        msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
        to_form='molsysmt.MolSys',
    )


@pytest.fixture
def example(source):
    partner = msm.extract(source, selection=[0, 1, 2])
    coordinates = msm.get(partner, coordinates=True)
    poses = [
        DockingPose(
            coordinates=coordinates[0] + puw.quantity(i, 'angstrom'),
            scores={'control': float(i)},
            rank=i + 1,
            metadata={
                'pose_atom_order': 'verified_pdbqt_order',
                'source_atom_keys': _molecular_atom_keys(partner),
            },
        )
        for i in range(3)
    ]
    return source, partner, DockingResult(poses=poses)


@pytest.mark.parametrize('frames', [1, 3])
def test_reference_frames_are_copied_or_explicitly_repeated(source, frames):
    reference = msm.extract(source, structure_indices=[0] * frames)
    coordinates = msm.get(reference, coordinates=True)
    if frames == 3:
        coordinates[1] += puw.quantity(1, 'angstrom')
        coordinates[2] += puw.quantity(2, 'angstrom')
        msm.set(reference, coordinates=coordinates)
    before = puw.get_value(msm.get(reference, coordinates=True)).copy()
    prepared = build_docking_reference_system(reference, 3)
    actual = puw.get_value(msm.get(prepared, coordinates=True))
    expected = np.repeat(before, 3, axis=0) if frames == 1 else before
    np.testing.assert_allclose(actual, expected)
    assert msm.get(prepared, n_structures=True) == 3
    assert _molecular_atom_keys(prepared) == _molecular_atom_keys(reference)
    msm.set(prepared, coordinates=puw.quantity(actual + 1, puw.get_unit(coordinates)))
    np.testing.assert_allclose(
        puw.get_value(msm.get(reference, coordinates=True)), before
    )
    assert msm.get(reference, n_structures=True) == frames


@pytest.mark.parametrize('count', [0, -1, 1.5, True, '3'])
def test_reference_requires_a_positive_integer_pose_count(source, count):
    with pytest.raises(ValueError, match='positive integer'):
        build_docking_reference_system(source, count)


def test_mismatched_reference_rejected_before_scene_changes(example):
    receptor, partner, result = example
    reference = msm.extract(partner, structure_indices=[0, 0])
    calls = []
    target = SimpleNamespace(load=lambda *args, **kwargs: calls.append(kwargs))
    with pytest.raises(ValueError, match='reference.*1 or 3'):
        render_docking_result(target, result, receptor, partner, reference)
    assert calls == []
    assert ensure_runtime(target).result is None
    assert ensure_runtime(target).event_log == []


def test_multiframe_receptor_is_not_silently_truncated(example):
    receptor, partner, result = example
    receptor = msm.extract(receptor, structure_indices=[0, 0])
    with pytest.raises(ValueError, match='receptor.*one structure'):
        build_docking_complex_system(receptor, result.poses, partner)


def test_multiframe_reconstructed_pose_is_rejected(example):
    receptor, partner, _ = example
    trajectory = msm.extract(partner, structure_indices=[0, 0])
    pose = SimpleNamespace(to_molecular_system=lambda source: trajectory)
    with pytest.raises(ValueError, match='pose.*one structure'):
        build_docking_complex_system(receptor, [pose], partner)


def test_reference_preserves_declared_time_box_and_units(source):
    reference = msm.extract(source, structure_indices=[0, 0, 0])
    times = puw.quantity([0, 1, 2], 'ps')
    boxes = puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), 'nm')
    msm.set(reference, time=times, box=boxes)
    before = msm.get(reference, coordinates=True)
    with puw.context(standard_units=['pm', 'fs']):
        prepared = build_docking_reference_system(reference, 3)
        np.testing.assert_allclose(
            puw.get_value(msm.get(prepared, time=True), to_unit='ps'), [0, 1, 2]
        )
        np.testing.assert_allclose(
            puw.get_value(msm.get(prepared, box=True), to_unit='nm'),
            puw.get_value(boxes, to_unit='nm'),
        )
        np.testing.assert_allclose(
            puw.get_value(msm.get(prepared, coordinates=True), to_unit='nm'),
            puw.get_value(before, to_unit='nm'),
        )


@pytest.mark.parametrize('signature', ['legacy', 'pairing', 'kwargs'])
def test_pairing_only_when_explicitly_advertised_and_reload_replaces(
    example, signature
):
    receptor, partner, result = example
    calls = []

    def legacy(system, *, label, mode):
        calls.append((label, mode, None))

    def pairing(system, *, label, mode, structure_pairing=None):
        calls.append((label, mode, structure_pairing))

    def kwargs(system, *, label, mode, **options):
        calls.append((label, mode, options))

    target = SimpleNamespace(
        load={'legacy': legacy, 'pairing': pairing, 'kwargs': kwargs}[signature]
    )
    render_docking_result(target, result, receptor, partner, partner)
    render_docking_result(target, result, receptor, partner, partner)
    expected = (
        'by_index'
        if signature == 'pairing'
        else ({} if signature == 'kwargs' else None)
    )
    assert (
        calls
        == [
            ('docking_complex', 'replace', None if signature != 'kwargs' else {}),
            ('reference_ligand', 'add', expected),
        ]
        * 2
    )


@pytest.mark.parametrize('phase', ['complex', 'reference', 'player'])
@pytest.mark.parametrize('error_type', [RuntimeError, TypeError])
def test_provider_failure_propagates_without_retry_or_success_state(
    example, phase, error_type
):
    receptor, partner, result = example
    error = error_type('provider failure')
    calls = []

    def load(system, *, label, mode, structure_pairing=None):
        calls.append(label)
        if label == {'complex': 'docking_complex', 'reference': 'reference_ligand'}.get(
            phase
        ):
            raise error

    def move(index):
        raise error

    target = SimpleNamespace(load=load, player=SimpleNamespace(go_to_structure=move))
    runtime = ensure_runtime(target)
    previous = object()
    runtime.result = previous
    with pytest.raises(error_type) as caught:
        render_docking_result(target, result, receptor, partner, partner)
    assert caught.value is error
    assert calls == (
        ['docking_complex']
        if phase == 'complex'
        else ['docking_complex', 'reference_ligand']
    )
    assert runtime.result is previous
    assert runtime.event_log == []


@pytest.mark.parametrize('reference_frames', [1, 3])
def test_real_viewer_reference_regions_frames_visibility_and_reload(
    example, reference_frames
):
    import molsysviewer as msv

    receptor, partner, result = example
    reference = msm.extract(partner, structure_indices=[0] * reference_frames)
    target = msv.MolSysView(debug_js=True)
    for _ in range(2):
        render_docking_result(target, result, receptor, partner, reference)
        assert target.regions.contains('reference_ligand')
        assert target.player.n_structures == 3
        assert (
            msm.get(target._molsys, n_atoms=True) == msm.get(receptor, n_atoms=True) + 6
        )
        region = target.regions.get('reference_ligand')
        coordinates = region.get(element='atom', coordinates=True)
        expected = puw.get_value(
            msm.get(reference, coordinates=True), to_unit='angstrom'
        )
        if reference_frames == 1:
            expected = np.repeat(expected, 3, axis=0)
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit='angstrom'), expected
        )
        for rank in [3, 1, 2]:
            set_active_pose(target, rank)
            assert target.player.index == rank - 1
            assert ensure_runtime(target).active_pose_rank == rank
        set_reference_visibility(target, False)
        assert ensure_runtime(target).reference_visible is False
        set_reference_visibility(target, True)
        assert ensure_runtime(target).reference_visible is True
