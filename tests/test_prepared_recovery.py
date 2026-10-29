"""Recovery binds supplied prepared declarations and available submitted bytes."""

import base64
import hashlib
import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError


def _pair():
    values = {
        'atom_names': ['C1', 'C2'],
        'coordinates': puw.quantity([[1, 0, 0], [2, 0, 0]], 'angstrom'),
        'atom_types': ['C', 'C'],
        'charges': [0.0, 0.0],
        'metadata': {'declared_choice': {'model': 'supplied'}},
    }
    receptor = dmt.PreparedReceptor(
        state_id='receptor-A',
        group_names=['REC', 'REC'],
        group_ids=[1, 1],
        **deepcopy(values),
    )
    partner = dmt.PreparedLigand(
        state_id='partner-A', group_name='LIG', **deepcopy(values)
    )
    return receptor, partner


def _saved(receptor, partner, *, captured=True, artifacts=True):
    problem = dmt.DockingProblem(
        receptor,
        partner,
        dmt.BoxRegion(
            center=puw.quantity([0, 0, 0], 'angstrom'),
            size=puw.quantity([10, 10, 10], 'angstrom'),
        ),
    )
    provenance = {'backend': 'vina'}
    if artifacts:
        provenance['backend_artifacts'] = {}
        for role, prepared in [('receptor', receptor), ('partner', partner)]:
            payload = prepared.to_pdbqt().encode()
            record = {'format': 'pdbqt', 'sha256': hashlib.sha256(payload).hexdigest()}
            if captured:
                record['content_base64'] = base64.b64encode(payload).decode('ascii')
            provenance['backend_artifacts'][role] = record
    result = dmt.DockingResult(
        poses=[], problem_info=problem.to_dict(), provenance=provenance
    )
    return dmt.DockingResult.from_dict(json.loads(json.dumps(result.to_dict())))


def _forbidden(*args, **kwargs):
    pytest.fail('Recovery must not calculate, reprepare or use an unneeded writer.')


def _shift(prepared, value):
    coordinates = np.asarray(
        puw.get_value(prepared.coordinates, to_unit='angstrom'), dtype=float
    ).copy()
    coordinates[0, 0] += value
    prepared.coordinates = puw.quantity(coordinates, 'angstrom')


@pytest.mark.parametrize('role', ['receptor', 'partner'])
@pytest.mark.parametrize(
    'field',
    ['state_id', 'charges', 'atom_types', 'atom_names', 'group_ids', 'metadata'],
)
def test_changed_prepared_declaration_rejects_before_writer_and_attachment(
    role, field, monkeypatch
):
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    original = deepcopy(saved.to_dict())
    previous = object()
    saved.problem = previous
    prepared = receptor if role == 'receptor' else partner
    if field == 'state_id':
        prepared.state_id = 'different-state'
    elif field == 'metadata':
        prepared.metadata['declared_choice']['model'] = 'different-model'
    else:
        getattr(prepared, field)[0] = {
            'charges': 0.5,
            'atom_types': 'OA',
            'atom_names': 'X1',
            'group_ids': 2,
        }[field]
    monkeypatch.setattr(dmt.PreparedReceptor, 'to_pdbqt', _forbidden)
    monkeypatch.setattr(dmt.PreparedLigand, 'to_pdbqt', _forbidden)
    with pytest.raises(ArgumentError, match='prepared.*declaration'):
        saved.reconstruct_problem(receptor=receptor, partner=partner)
    assert saved.problem is previous
    assert saved.to_dict() == original


def test_changed_ligand_torsion_declaration_rejects_before_export():
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    partner.torsion_dof = 1
    with pytest.raises(ArgumentError, match='prepared.*declaration'):
        saved.reconstruct_problem(receptor=receptor, partner=partner)
    assert saved.problem is None


@pytest.mark.parametrize('role', ['receptor', 'partner'])
@pytest.mark.parametrize('captured', [False, True])
def test_changed_coordinates_reject_against_recorded_hash_without_native_computation(
    role, captured, monkeypatch
):
    receptor, partner = _pair()
    saved = _saved(receptor, partner, captured=captured)
    prepared = receptor if role == 'receptor' else partner
    _shift(prepared, 0.25)
    monkeypatch.setattr(dmt, 'dock', _forbidden)
    monkeypatch.setattr(dmt, 'score', _forbidden)
    with pytest.raises(ArgumentError, match='PDBQT.*recorded'):
        saved.reconstruct_problem(receptor=receptor, partner=partner)
    assert saved.problem is None


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_matching_recovery_uses_public_native_writer_and_preserves_policy_and_inputs(
    length_unit, monkeypatch
):
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    before = deepcopy(saved.to_dict())
    snapshots = [deepcopy(item.to_dict()) for item in (receptor, partner)]
    coordinates = [
        puw.get_value(item.coordinates).copy() for item in (receptor, partner)
    ]
    convert = msm.convert
    exports = []

    def exported(item, **options):
        if options.get('to_form') == 'string:pdbqt_text' and options.get(
            'return_atom_map'
        ):
            exports.append(item)
        return convert(item, **options)

    monkeypatch.setattr(msm, 'convert', exported)
    monkeypatch.setattr(dmt, 'dock', _forbidden)
    monkeypatch.setattr(dmt, 'score', _forbidden)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        recovered = saved.reconstruct_problem(receptor=receptor, partner=partner)
        assert puw.configure.report() == policy
    assert len(exports) == 2
    assert recovered is saved.problem
    assert recovered.receptor is receptor and recovered.partner is partner
    assert saved.to_dict() == before
    for item, record, xyz in zip((receptor, partner), snapshots, coordinates):
        assert item.to_dict() == record
        np.testing.assert_array_equal(puw.get_value(item.coordinates), xyz)
        assert item.source_molsys is None


@pytest.mark.parametrize('role', ['receptor', 'partner'])
@pytest.mark.parametrize('damage', ['bytes', 'digest', 'format', 'container'])
def test_corrupt_recorded_artifact_rejects_before_rendering(role, damage, monkeypatch):
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    artifacts = saved.provenance['backend_artifacts']
    if damage == 'bytes':
        artifacts[role]['content_base64'] = base64.b64encode(b'changed').decode('ascii')
    elif damage == 'digest':
        artifacts[role]['sha256'] = 'not-a-digest'
    elif damage == 'format':
        artifacts[role]['format'] = 'other'
    else:
        artifacts[role] = []
    monkeypatch.setattr(dmt.PreparedReceptor, 'to_pdbqt', _forbidden)
    monkeypatch.setattr(dmt.PreparedLigand, 'to_pdbqt', _forbidden)
    with pytest.raises(ArgumentError):
        saved.reconstruct_problem(receptor=receptor, partner=partner)
    assert saved.problem is None


def test_provider_export_failure_propagates_without_attaching_a_problem(monkeypatch):
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    before = deepcopy(saved.to_dict())

    def refuse(*args, **kwargs):
        raise RuntimeError('provider export refused')

    monkeypatch.setattr(msm, 'convert', refuse)
    with pytest.raises(RuntimeError, match='provider export refused'):
        saved.reconstruct_problem(receptor=receptor, partner=partner)
    assert saved.problem is None and saved.to_dict() == before


def test_legacy_missing_artifacts_recovers_declared_values_without_export(monkeypatch):
    receptor, partner = _pair()
    saved = _saved(receptor, partner, artifacts=False)
    monkeypatch.setattr(dmt.PreparedReceptor, 'to_pdbqt', _forbidden)
    monkeypatch.setattr(dmt.PreparedLigand, 'to_pdbqt', _forbidden)
    assert (
        saved.reconstruct_problem(receptor=receptor, partner=partner).partner is partner
    )


def test_missing_digest_cannot_establish_coordinate_identity(monkeypatch):
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    for artifact in saved.provenance['backend_artifacts'].values():
        artifact.pop('sha256')
        artifact.pop('content_base64')
    _shift(partner, 0.25)
    monkeypatch.setattr(dmt.PreparedReceptor, 'to_pdbqt', _forbidden)
    monkeypatch.setattr(dmt.PreparedLigand, 'to_pdbqt', _forbidden)
    assert (
        saved.reconstruct_problem(receptor=receptor, partner=partner).partner is partner
    )


def test_absent_legacy_prepared_snapshot_does_not_invent_declarations():
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    for role in ('receptor', 'partner'):
        saved.problem_info[role] = {'type': 'external', 'value': None}
    assert (
        saved.reconstruct_problem(receptor=receptor, partner=partner).partner is partner
    )


def test_subprecision_coordinate_edit_can_retain_identical_submitted_bytes():
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    _shift(partner, 1e-6)
    assert (
        saved.reconstruct_problem(receptor=receptor, partner=partner).partner is partner
    )


@pytest.mark.parametrize('bad', [float('nan'), object()])
def test_invalid_prepared_json_declaration_rejects_without_writer(bad, monkeypatch):
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    partner.metadata['invalid'] = bad
    monkeypatch.setattr(dmt.PreparedReceptor, 'to_pdbqt', _forbidden)
    monkeypatch.setattr(dmt.PreparedLigand, 'to_pdbqt', _forbidden)
    with pytest.raises(ArgumentError, match='prepared.*declaration'):
        saved.reconstruct_problem(receptor=receptor, partner=partner)


def test_native_prepared_coordinate_refusal_preserves_source_and_assignment_reports():
    from molecular_fixtures import named_181l_pair

    from devtools.qualify_chemical_templates import snapshot

    receptor, partner = named_181l_pair()
    saved = _saved(receptor, partner)
    source_before = snapshot(partner.source_molsys)
    declaration = deepcopy(partner.to_dict())
    _shift(partner, 0.25)
    with pytest.raises(ArgumentError, match='PDBQT.*recorded'):
        saved.reconstruct_problem(receptor=receptor, partner=partner)
    assert snapshot(partner.source_molsys) == source_before
    assert partner.to_dict() == declaration
    assert saved.problem is None


def test_recovery_requires_no_engine_viewer_or_chemical_preparation(monkeypatch):
    import builtins

    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    original_import = builtins.__import__

    def import_without_runtime(name, *args, **kwargs):
        if name.split('.')[0] in ('vina', 'molsysviewer'):
            pytest.fail('Prepared recovery must not import an engine or viewer')
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', import_without_runtime)
    for name in ('dock', 'score', 'prepare_ligand', 'prepare_receptor'):
        monkeypatch.setattr(dmt, name, _forbidden)
    assert (
        saved.reconstruct_problem(receptor=receptor, partner=partner).partner is partner
    )


@pytest.mark.parametrize('role', ['receptor', 'partner'])
def test_backend_text_cannot_bypass_a_recorded_object_declaration(role):
    receptor, partner = _pair()
    saved = _saved(receptor, partner)
    values = {'receptor': receptor, 'partner': partner}
    values[role] = values[role].to_pdbqt()
    with pytest.raises(ArgumentError, match='prepared.*declaration'):
        saved.reconstruct_problem(**values)
    assert saved.problem is None
