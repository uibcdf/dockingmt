"""Consumer complex composition through public molecular tools (#49)."""

from contextlib import nullcontext
from types import SimpleNamespace

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt.preparation import PreparedLigand, PreparedReceptor
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


def _manual_prepared(kind):
    arguments = dict(
        state_id='manual',
        atom_names=['C1', 'C1', 'O1'],
        group_names=['LIG'] * 3,
        group_ids=[7] * 3,
        coordinates=puw.quantity(
            [[0.123456789, 0, 0], [0.2, 0.123456789, 0], [0, 0.2, 0.123456789]],
            'nm',
        ),
        atom_types=['C', 'A', 'OA'],
        charges=[0.123456789, -0.234567891, 0.111111102],
    )
    return (
        PreparedLigand(group_name='LIG', **arguments)
        if kind == 'ligand'
        else PreparedReceptor(**arguments)
    )


@pytest.mark.parametrize('kind', ['ligand', 'receptor'])
@pytest.mark.parametrize('alternate_units', [False, True])
def test_manual_projection_preserves_precision_identity_and_available_mechanics(
    kind, alternate_units, monkeypatch
):
    prepared = _manual_prepared(kind)
    before = puw.get_value(prepared.coordinates, to_unit='nm').copy()
    charges = list(prepared.charges)
    convert = msm.convert
    calls = []

    def recorded(item, **kwargs):
        calls.append((item, kwargs))
        return convert(item, **kwargs)

    monkeypatch.setattr(msm, 'convert', recorded)
    context = (
        puw.context(standard_units=['pm', 'fs']) if alternate_units else nullcontext()
    )
    with context:
        native = prepared.to_molecular_system()
        assert any(
            isinstance(item, str) and item.startswith('pdbqt_text:')
            for item, _ in calls
        )
        np.testing.assert_array_equal(
            msm.get(native, element='atom', atom_name=True), prepared.atom_names
        )
        np.testing.assert_array_equal(
            msm.get(native, element='atom', group_name=True), prepared.group_names
        )
        np.testing.assert_array_equal(
            msm.get(native, element='atom', group_id=True),
            [str(group_id) for group_id in prepared.group_ids],
        )
        np.testing.assert_array_equal(
            msm.get(native, element='atom', atom_type=True), ['C', 'C', 'O']
        )
        np.testing.assert_array_equal(
            msm.get(native, element='atom', atom_ff_type=True), prepared.atom_types
        )
        np.testing.assert_allclose(
            np.asarray(
                msm.get(native, element='atom', partial_charge=True), dtype=float
            ),
            charges,
            rtol=0,
            atol=1e-15,
        )
        np.testing.assert_allclose(
            puw.get_value(msm.get(native, coordinates=True), to_unit='nm')[0],
            before,
            rtol=0,
            atol=1e-15,
        )
        assert not msm.has_attribute(native, 'bond_order')
        assert native.molecular_mechanics.partial_charge_assignment is None
        msm.set(
            native,
            coordinates=puw.quantity((before + 1)[None], 'nm'),
            partial_charge=puw.quantity([0.0] * prepared.n_atoms, 'elementary_charge'),
        )
    np.testing.assert_array_equal(
        puw.get_value(prepared.coordinates, to_unit='nm'), before
    )
    np.testing.assert_array_equal(prepared.charges, charges)


@pytest.mark.parametrize('kind', ['ligand', 'receptor'])
def test_manual_projection_propagates_provider_failure(kind, monkeypatch):
    error = RuntimeError('provider conversion failed')

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm, 'convert', fail)
    with pytest.raises(RuntimeError) as caught:
        _manual_prepared(kind).to_molecular_system()
    assert caught.value is error


@pytest.mark.parametrize('alternate_units', [False, True])
def test_source_free_complex_preserves_prepared_mechanics(alternate_units):
    receptor = _manual_prepared('receptor')
    ligand = _manual_prepared('ligand')
    context = (
        puw.context(standard_units=['pm', 'fs']) if alternate_units else nullcontext()
    )
    with context:
        receptor_system = receptor.to_molecular_system()
        ligand_system = ligand.to_molecular_system()
        poses = []
        for offset in [0.0, 0.2]:
            frame = msm.copy(ligand_system)
            msm.set(
                frame, coordinates=ligand.coordinates[None] + puw.quantity(offset, 'nm')
            )
            poses.append(
                SimpleNamespace(to_molecular_system=lambda partner, f=frame: f)
            )
        result = build_docking_complex_system(receptor_system, poses, ligand)
        np.testing.assert_allclose(
            np.asarray(
                msm.get(result, element='atom', partial_charge=True), dtype=float
            ),
            receptor.charges + ligand.charges,
            rtol=0,
            atol=1e-15,
        )
        np.testing.assert_array_equal(
            msm.get(result, element='atom', atom_ff_type=True),
            receptor.atom_types + ligand.atom_types,
        )
        observed = puw.get_value(msm.get(result, coordinates=True), to_unit='nm')
        expected_rec = puw.get_value(receptor.coordinates, to_unit='nm')
        expected_lig = puw.get_value(ligand.coordinates, to_unit='nm')
        for index, offset in enumerate([0.0, 0.2]):
            np.testing.assert_allclose(
                observed[index, :3], expected_rec, rtol=0, atol=1e-15
            )
            np.testing.assert_allclose(
                observed[index, 3:], expected_lig + offset, rtol=0, atol=1e-15
            )
