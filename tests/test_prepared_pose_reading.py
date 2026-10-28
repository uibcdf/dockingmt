"""Production pose reading consumes one actual prepared export through MolSysMT."""

import hashlib
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError, StructuralInconsistencyError
from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT
from test_flexible_reconstruction import _manual
from test_known_source_pose_consumption import _case

import dockingmt as dmt
from devtools.qualify_chemical_templates import snapshot
from dockingmt._private.smonitor import ArgumentError
from dockingmt.engines.vina import _read_staged_poses


def _problem(partner):
    return dmt.DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=partner,
        search_domain=dmt.BoxRegion(
            center=puw.quantity([0, 0, 0], 'angstrom'),
            size=puw.quantity([16, 16, 16], 'angstrom'),
        ),
    )


def _prepared(flexible=False):
    _, native, _, _, _, _ = _case('CCCCCC' if flexible else 'CO')
    return dmt.prepare_ligand(
        native, selection='all', active_torsion_bonds=[(1, 2)] if flexible else None
    )


def _stage(prepared, files):
    return dmt.VinaBackend()._stage_inputs(
        MINIMAL_REC_PDBQT, prepared, dmt.VinaProtocol(), files
    )


def _forbid(*args, **kwargs):
    pytest.fail('Known-source reader must not fall back to local parsing.')


@pytest.mark.parametrize('flexible', [False, True])
@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_production_reader_uses_actual_export_once_and_preserves_written_axis(
    flexible, length_unit, monkeypatch
):
    import dockingmt.engines.vina as adapter

    prepared = _prepared(flexible)
    before = snapshot(prepared.source_molsys)
    source_ids = list(msm.get(prepared.source_molsys, element='atom', atom_id=True))
    convert, read = msm.convert, msm.form.string_pdbqt_text.read_poses
    exports, reads = [], []

    def exported(item, **options):
        value = convert(item, **options)
        if (
            options.get('return_atom_map')
            and options.get('to_form') == 'string:pdbqt_text'
        ):
            exports.append((item, value))
        return value

    def received(item, source, mapping, **options):
        reads.append((item, source, mapping))
        assert source is exports[0][0] and mapping is exports[0][1][1]
        return read(item, source, mapping, **options)

    monkeypatch.setattr(msm, 'convert', exported)
    monkeypatch.setattr(msm.form.string_pdbqt_text, 'read_poses', received)
    monkeypatch.setattr(adapter, '_pdbqt_atom_records', _forbid)
    monkeypatch.setattr(prepared, 'to_molecular_system', _forbid)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        result = dmt.dock(
            _problem(prepared),
            dmt.VinaProtocol(exhaustiveness=1, n_poses=2, seed=321, cpu=1),
        )
        assert puw.configure.report() == policy
    assert len(exports) == len(reads) == 1
    source, (text, mapping) = exports[0]
    # The writer may use an independent value-adjusted view under unit conversion.
    # The reader must receive that actual view, already checked by identity above.
    assert list(mapping['source_atom_ids']) == source_ids
    order = prepared.pdbqt_atom_indices
    if flexible:
        assert order != list(range(prepared.n_atoms))
    reading = result.provenance['backend_output']['pose_reading']
    report = reading['report']
    assert reading['method'] == 'molsysmt.form.string_pdbqt_text.read_poses'
    assert (
        report['export_map']['payload_sha256']
        == result.provenance['backend_artifacts']['partner']['sha256']
    )
    assert (
        report['input_payload_sha256']
        == hashlib.sha256(reads[0][0].removeprefix('pdbqt_text:').encode()).hexdigest()
    )
    assert report['n_input_structures'] == len(result.poses)
    independently_read = read(reads[0][0], source, mapping)
    xyz = puw.get_value(
        msm.get(independently_read, coordinates=True), to_unit='angstrom'
    )
    for index, pose in enumerate(result.poses):
        np.testing.assert_allclose(
            puw.get_value(pose.coordinates, to_unit='angstrom'),
            xyz[index, order],
            rtol=0,
            atol=1e-10,
        )
        assert pose.metadata['prepared_atom_indices'] == order
        assert [key['atom_id'] for key in pose.metadata['source_atom_keys']] == [
            source_ids[i] for i in order
        ]
    assert snapshot(prepared.source_molsys) == before
    restored = dmt.DockingResult.from_dict(result.to_dict())
    assert restored.provenance['backend_output']['pose_reading'] == reading


@pytest.mark.parametrize('kind', ['source_free', 'partial_source', 'external'])
def test_uncovered_profiles_remain_explicit_without_trying_known_source_reader(
    kind, monkeypatch
):
    if kind == 'external':
        partner = MINIMAL_LIG_PDBQT
        expected = 'unmapped_input'
    else:
        partner = _manual()
        expected = 'incomplete_source_connectivity'
        if kind == 'partial_source':
            partner.source_molsys = partner.to_molecular_system()
    monkeypatch.setattr(msm.form.string_pdbqt_text, 'read_poses', _forbid)
    result = dmt.dock(
        _problem(partner),
        dmt.VinaProtocol(exhaustiveness=1, n_poses=1, seed=321, cpu=1),
    )
    assert result.provenance['backend_output']['pose_reading'] == {
        'method': 'legacy_pdbqt_order',
        'reason': expected,
    }
    assert result.poses
    if kind == 'source_free':
        # Existing source-free identity is from the staged written projection.
        assert all(
            key['group_name'] == 'LIG'
            for key in result.top_pose.metadata['source_atom_keys']
        )


def test_native_numeric_coherence_accepts_permuted_array_and_refuses_disagreement(
    tmp_path, monkeypatch
):
    prepared = _prepared()
    files = []
    staged = _stage(prepared, files)
    try:
        raw = puw.get_value(
            msm.get(staged['partner_export'].molecular_system, coordinates=True),
            to_unit='angstrom',
        )
        raw = np.round(raw[:, prepared.pdbqt_atom_indices], 3)
        reordered = raw[:, ::-1].copy()
        monkeypatch.setattr('dockingmt.engines.vina._pdbqt_atom_records', _forbid)
        actual, _ = _read_staged_poses(staged, staged['partner_string'], reordered)
        np.testing.assert_allclose(actual, raw, rtol=0, atol=1e-10)
        reordered[0, 0, 0] += 0.1
        with pytest.raises(ArgumentError, match='atom order or coordinates differ'):
            _read_staged_poses(staged, staged['partner_string'], reordered)
    finally:
        for path in files:
            Path(path).unlink(missing_ok=True)


@pytest.mark.parametrize('damage', ['charge', 'type', 'model'])
def test_native_reader_validates_later_pose_without_local_recovery(damage, monkeypatch):
    prepared = _prepared()
    files = []
    staged = _stage(prepared, files)
    try:
        payload = staged['partner_string']
        lines = payload.splitlines()
        atom = next(i for i, line in enumerate(lines) if line.startswith('ATOM'))
        if damage == 'charge':
            lines[atom] = lines[atom][:70] + ' 9.000' + lines[atom][76:]
        elif damage == 'type':
            lines[atom] = lines[atom][:77] + 'OA'
        changed = '\n'.join(lines) + '\n'
        text = 'MODEL 1\n' + payload + 'ENDMDL\nMODEL 2\n' + changed
        if damage != 'model':
            text += 'ENDMDL\n'
        monkeypatch.setattr('dockingmt.engines.vina._pdbqt_atom_records', _forbid)
        with pytest.raises(FormatError):
            _read_staged_poses(staged, text, np.zeros((2, prepared.n_atoms, 3)))
    finally:
        for path in files:
            Path(path).unlink(missing_ok=True)


def test_actual_staged_payload_must_match_completed_map(monkeypatch):
    files = []
    staged = _stage(_prepared(), files)
    try:
        staged['partner_pdbqt'] += b'REMARK changed after export\n'
        monkeypatch.setattr(msm.form.string_pdbqt_text, 'read_poses', _forbid)
        with pytest.raises(ArgumentError, match='does not bind the staged'):
            _read_staged_poses(staged, '', np.zeros((1, 3, 3)))
    finally:
        for path in files:
            Path(path).unlink(missing_ok=True)


def test_changed_source_cannot_switch_a_staged_known_source_profile_to_legacy(
    monkeypatch,
):
    files = []
    staged = _stage(_prepared(), files)
    try:
        # Explicitly damaged native test state; this is not a consumer repair.
        staged['partner_export'].molecular_system.chemical_states._states[
            0
        ].connectivity_completeness = 'partial'
        assert staged['pose_reading_mode'] == 'molsysmt_known_source'
        monkeypatch.setattr('dockingmt.engines.vina._pdbqt_atom_records', _forbid)
        with pytest.raises(StructuralInconsistencyError, match='complete'):
            _read_staged_poses(staged, staged['partner_string'], np.zeros((1, 3, 3)))
    finally:
        for path in files:
            Path(path).unlink(missing_ok=True)


def test_production_reader_failure_propagates_and_cleans_staging(monkeypatch):
    prepared = _prepared()
    captured = []
    original = dmt.VinaBackend._stage_inputs

    def staged(self, *args):
        result = original(self, *args)
        captured.append(deepcopy(args[-1]))
        return result

    def refuse(*args, **kwargs):
        raise RuntimeError('public pose reader refusal')

    monkeypatch.setattr(dmt.VinaBackend, '_stage_inputs', staged)
    monkeypatch.setattr(msm.form.string_pdbqt_text, 'read_poses', refuse)
    monkeypatch.setattr('dockingmt.engines.vina._pdbqt_atom_records', _forbid)
    with pytest.raises(RuntimeError, match='public pose reader refusal'):
        dmt.dock(
            _problem(prepared),
            dmt.VinaProtocol(exhaustiveness=1, n_poses=1, cpu=1, seed=321),
        )
    assert captured and all(not Path(path).exists() for path in captured[0])


def test_manual_values_bind_reader_to_the_actual_export_copy(monkeypatch):
    prepared = _prepared()
    prepared.metadata = {}
    prepared.charges[0] += 0.123456
    before = snapshot(prepared.source_molsys)
    read = msm.form.string_pdbqt_text.read_poses
    seen = []

    def observed(item, source, mapping, **options):
        assert source is not prepared.source_molsys
        values = msm.get(source, element='atom', partial_charge=True)
        if puw.is_quantity(values):
            values = puw.get_value(values, to_unit='elementary_charge')
        np.testing.assert_allclose(values, prepared.charges, rtol=0, atol=1e-12)
        seen.append(mapping)
        return read(item, source, mapping, **options)

    monkeypatch.setattr(msm.form.string_pdbqt_text, 'read_poses', observed)
    monkeypatch.setattr('dockingmt.engines.vina._pdbqt_atom_records', _forbid)
    result = dmt.dock(
        _problem(prepared),
        dmt.VinaProtocol(exhaustiveness=1, n_poses=1, seed=321, cpu=1),
    )
    assert len(seen) == 1 and result.poses
    assert snapshot(prepared.source_molsys) == before
