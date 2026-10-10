"""Consumer complex composition through public molecular tools (#49)."""

from contextlib import nullcontext
from types import SimpleNamespace

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

from molsysviewer_dockingmt.adapters.complex import build_docking_complex_system


@pytest.mark.parametrize('alternate_units', [False, True])
def test_complex_frames_delegate_composition_and_preserve_source_geometry(
    alternate_units, monkeypatch
):
    source = msm.convert(
        msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
        to_form='molsysmt.MolSys',
    )
    ligand = msm.extract(source, selection=[0, 1, 2])
    rec_before = puw.get_value(msm.get(source, coordinates=True), to_unit='nm').copy()
    ligand_before = puw.get_value(
        msm.get(ligand, coordinates=True), to_unit='nm'
    ).copy()
    frames = []
    for offset in [0.0, 0.1, -0.2]:
        frame = msm.copy(ligand)
        msm.set(frame, coordinates=puw.quantity(ligand_before + offset, 'nm'))
        frames.append(frame)
    poses = [
        SimpleNamespace(to_molecular_system=lambda partner, f=f: f) for f in frames
    ]
    merge = msm.merge
    calls = []

    def recorded(items, **kwargs):
        calls.append(items)
        return merge(items, **kwargs)

    monkeypatch.setattr(msm, 'merge', recorded)
    context = (
        puw.context(standard_units=['pm', 'fs']) if alternate_units else nullcontext()
    )
    with context:
        result = build_docking_complex_system(source, poses, ligand)
        values = puw.get_value(msm.get(result, coordinates=True), to_unit='nm')
    assert len(calls) == 3
    n_rec = rec_before.shape[1]
    for index, offset in enumerate([0.0, 0.1, -0.2]):
        np.testing.assert_allclose(values[index, :n_rec], rec_before[0])
        np.testing.assert_allclose(values[index, n_rec:], ligand_before[0] + offset)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit='nm'), rec_before
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(ligand, coordinates=True), to_unit='nm'), ligand_before
    )


def test_later_frame_composition_failure_propagates(monkeypatch):
    source = msm.convert(
        msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
        to_form='molsysmt.MolSys',
    )
    merge = msm.merge
    error = RuntimeError('second frame composition failed')
    calls = []

    def fail_second(items, **kwargs):
        calls.append(items)
        if len(calls) == 2:
            raise error
        return merge(items, **kwargs)

    monkeypatch.setattr(msm, 'merge', fail_second)
    poses = [SimpleNamespace(to_molecular_system=lambda partner: source)] * 2
    with pytest.raises(RuntimeError) as caught:
        build_docking_complex_system(source, poses, source)
    assert caught.value is error
    assert len(calls) == 2
