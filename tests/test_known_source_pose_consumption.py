"""Qualify native mapped poses before retiring legacy preparation/parser routes."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError
from test_engines import MINIMAL_REC_PDBQT
from test_vina_torsion_matrix import CASES, _source

import dockingmt as dmt
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, HYDROGEN, TYPING, explicit_source
from dockingmt.engines.vina import _verify_pose_atom_order

DATA = Path(__file__).parent / 'data/vina_torsions'
OFFSETS = np.array([[0, 0, 0], [10, -2, 1], [-5, 3, 2]])
LABELS = ['9', '2', '51']


def _tree(source, flexible=False):
    """Declare this fixture's ROOT/cut policy using the public writer schema."""
    n_atoms = msm.get(source, n_atoms=True)
    if flexible:
        assert n_atoms == 6
    return {
        'schema_version': 'molsysmt.pdbqt-torsion-tree@1',
        'atom_ids': msm.get(source, element='atom', atom_id=True),
        'fragment_atom_indices': [2, 3, 4, 5, 1, 0]
        if flexible
        else list(reversed(range(n_atoms))),
        'fragment_offsets': [0, 4, 6] if flexible else [0, n_atoms],
        'branch_atom_pairs': [[2, 1]] if flexible else np.empty((0, 2), dtype=int),
        'branch_fragment_pairs': [[0, 1]] if flexible else np.empty((0, 2), dtype=int),
        'root_fragment_index': 0,
        'torsdof': int(flexible),
    }


def _export(source, tree):
    return msm.convert(
        source,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        torsion_tree=tree,
        return_atom_map=True,
    )


def _case(smiles):
    source = explicit_source(smiles)
    msm.set(source, atom_id=list(range(11, 11 + msm.get(source, n_atoms=True))))
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(source, **CHARGE), **TYPING
    )
    projected = msm.build.merge_nonpolar_hydrogens(
        source, typing_scheme='autodock4', return_report=True
    )
    reduced = projected['molecular_system']
    tree = _tree(reduced, flexible=smiles == 'CCCCCC')
    text, mapping = _export(reduced, tree)
    return source, reduced, projected['report'], text, mapping, tree


def _ensemble(source, tree):
    bodies = []
    for label, offset in zip(LABELS, OFFSETS, strict=True):
        frame = msm.copy(source)
        msm.set(
            frame,
            coordinates=msm.get(frame, coordinates=True)
            + puw.quantity(offset, 'angstrom'),
        )
        payload, _ = _export(frame, tree)
        bodies.append(
            f'MODEL {label}\nREMARK VINA RESULT: opaque-control-{label}\n'
            + payload.removeprefix('pdbqt_text:')
            + 'ENDMDL\n'
        )
    return 'pdbqt_text:' + ''.join(bodies)


@pytest.fixture(params=['CO', 'CCCCCC'], ids=['methanol-rigid', 'hexane-flexible'])
def pose_case(request):
    return _case(request.param)


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_native_projection_export_and_all_pose_axes(pose_case, length_unit, tmp_path):
    source, reduced, projection, text, mapping, tree = pose_case
    before, reduced_before = snapshot(source), snapshot(reduced)
    assignment = deepcopy(reduced.molecular_mechanics.partial_charge_assignment)
    map_before = detached_record(mapping)
    payload = _ensemble(reduced, tree)
    path = tmp_path / 'poses.pdbqt'
    path.write_text(payload.removeprefix('pdbqt_text:'))
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        result = msm.form.file_pdbqt.read_poses(
            path, reduced, mapping, return_report=True
        )
    native, report = result['molecular_system'], result['report']
    xyz = puw.get_value(msm.get(native, coordinates=True), to_unit='angstrom')
    expected = puw.get_value(msm.get(reduced, coordinates=True), to_unit='angstrom')
    np.testing.assert_allclose(
        xyz, expected + OFFSETS[:, None, :], rtol=0, atol=0.000501
    )
    assert list(msm.get(native, structure_id=True)) == LABELS
    assert report['n_input_structures'] == 3
    assert (
        mapping['payload_sha256']
        == hashlib.sha256(text.removeprefix('pdbqt_text:').encode()).hexdigest()
    )
    assert (
        report['input_payload_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
    )
    assert report['omitted_source_atom_indices'].size == 0
    assert report['source_coordinates_reused'] is False
    assert report['source_interactions_copied'] is False
    assert not native.interactions
    assert native.molecular_mechanics.partial_charge is None
    assert native.molecular_mechanics.atom_ff_type is None
    assert msm.get(native, time=True) is None and msm.get(native, box=True) is None
    for attribute, element in [
        ('atom_id', 'atom'),
        ('atom_name', 'atom'),
        ('atom_type', 'atom'),
        ('formal_charge', 'atom'),
        ('bonded_atom_pairs', 'bond'),
        ('bond_order', 'bond'),
        ('n_explicit_hydrogens', 'atom'),
        ('allows_implicit_hydrogens', 'atom'),
    ]:
        np.testing.assert_array_equal(
            msm.get(native, element=element, **{attribute: True}),
            msm.get(reduced, element=element, **{attribute: True}),
        )
    np.testing.assert_array_equal(
        report['pdbqt_to_output_atom_indices'], mapping['output_to_source_atom_indices']
    )
    # Composition of declared report axes is accounting, not molecular matching.
    full_axis = projection['output_to_source_atom_indices'][
        mapping['output_to_source_atom_indices']
    ]
    assert len(np.unique(full_axis)) == msm.get(reduced, n_atoms=True)
    assert len(full_axis) < msm.get(source, n_atoms=True)
    assert report['charge_unit'] == projection['charge_unit'] == 'elementary_charge'
    assert projection['output_total_charge'] == pytest.approx(
        projection['selected_total_charge'],
        abs=projection['charge_conservation_tolerance'],
    )
    assert assignment['status'] == 'derived'
    assert assignment['source_assignment']['method'] == 'gasteiger_marsili'
    assert snapshot(source) == before and snapshot(reduced) == reduced_before
    assert detached_record(mapping) == map_before
    assert detached_record(
        reduced.molecular_mechanics.partial_charge_assignment
    ) == detached_record(assignment)
    # The JSON report remains independently usable; returned reports are detached.
    restored = msm.form.string_pdbqt_text.read_poses(
        text, reduced, map_before, return_report=True
    )
    assert restored['report']['n_input_structures'] == 1
    report['export_map']['output_to_source_atom_indices'][0] = 999
    assert detached_record(mapping) == map_before


@pytest.mark.parametrize('case', CASES, ids=lambda case: case[0])
def test_original_reference_inputs_keep_known_chemical_graph(case):

    suffix = 'H' if case[0].startswith('5x72') else ''
    path = DATA / f'{case[0]}{suffix}.sdf'
    original = path.read_bytes()
    assert hashlib.sha256(original).hexdigest() == case[1]
    # Reuse the existing explicit RDKit input bridge and fixed-state H stage.
    # Raw SDF admission alone does not declare the projection prerequisites.
    native = msm.build.add_missing_hydrogens(
        msm.convert(_source(case[0], case[1]), to_form='molsysmt.MolSys'), **HYDROGEN
    )
    # Serial IDs are an explicit presentation choice for this staged source.
    msm.set(native, atom_id=list(range(11, 11 + msm.get(native, n_atoms=True))))
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(native, **CHARGE), **TYPING
    )
    before = snapshot(source)
    reduced = msm.build.merge_nonpolar_hydrogens(source, typing_scheme='autodock4')
    text, mapping = _export(reduced, _tree(reduced))
    poses = msm.form.string_pdbqt_text.read_poses(text, reduced, mapping)
    assert msm.get(poses, n_atoms=True) == msm.get(reduced, n_atoms=True)
    assert snapshot(poses)['chemical_states'] == snapshot(reduced)['chemical_states']
    np.testing.assert_allclose(
        puw.get_value(msm.get(poses, coordinates=True), to_unit='angstrom'),
        puw.get_value(msm.get(reduced, coordinates=True), to_unit='angstrom'),
        rtol=0,
        atol=0.000501,
    )
    assert snapshot(source) == before and path.read_bytes() == original


@pytest.mark.parametrize('selection', [[2, 0, 2], []])
def test_pose_selection_preserves_positions_and_repeats(pose_case, selection):
    _, reduced, _, _, mapping, tree = pose_case
    result = msm.form.string_pdbqt_text.read_poses(
        _ensemble(reduced, tree),
        reduced,
        mapping,
        structure_indices=selection,
        return_report=True,
    )
    native, report = result['molecular_system'], result['report']
    assert list(report['input_structure_indices']) == selection
    assert list(report['model_ids']) == [LABELS[i] for i in selection]
    if selection:
        assert list(msm.get(native, structure_id=True)) == [
            LABELS[i] for i in selection
        ]
    else:
        assert msm.get(native, structure_id=True) is None
    actual = puw.get_value(msm.get(native, coordinates=True), to_unit='angstrom')
    expected = puw.get_value(msm.get(reduced, coordinates=True), to_unit='angstrom')
    assert actual.shape == (len(selection), msm.get(reduced, n_atoms=True), 3)
    if selection:
        np.testing.assert_allclose(
            actual, expected + OFFSETS[selection, None, :], rtol=0, atol=0.000501
        )


@pytest.mark.parametrize(
    'mutation', ['missing-end', 'duplicate-model', 'charge', 'type', 'nonfinite']
)
def test_all_models_are_validated_before_pose_selection(mutation):
    source, reduced, _, _, mapping, tree = _case('CO')
    before, reduced_before = snapshot(source), snapshot(reduced)
    payload = _ensemble(reduced, tree)
    if mutation == 'missing-end':
        payload = payload.rsplit('ENDMDL', 1)[0]
    elif mutation == 'duplicate-model':
        payload = payload.replace('MODEL 51', 'MODEL 9')
    else:
        lines = payload.splitlines()
        index = max(i for i, line in enumerate(lines) if line.startswith('ATOM'))
        line = lines[index]
        if mutation == 'charge':
            lines[index] = line[:70] + ' 9.999' + line[76:]
        elif mutation == 'type':
            lines[index] = line[:77] + 'NA'
        else:
            lines[index] = line[:30] + '     nan' + line[38:]
        payload = '\n'.join(lines) + '\n'
    with pytest.raises(FormatError):
        msm.form.string_pdbqt_text.read_poses(
            payload, reduced, mapping, structure_indices=[0]
        )
    assert snapshot(source) == before and snapshot(reduced) == reduced_before


@pytest.mark.parametrize('mutation', ['legacy-map', 'duplicate-map', 'stale-identity'])
def test_incomplete_or_stale_maps_are_not_repaired(mutation):
    _, reduced, _, text, mapping, _ = _case('CO')
    mapping = deepcopy(mapping)
    if mutation == 'legacy-map':
        mapping = {'retained_atom_indices': [0, 1, 5]}
    elif mutation == 'duplicate-map':
        mapping['output_to_source_atom_indices'][1] = mapping[
            'output_to_source_atom_indices'
        ][0]
    else:
        msm.set(reduced, selection=[0], atom_name='EDIT')
    before = snapshot(reduced)
    with pytest.raises(FormatError):
        msm.form.string_pdbqt_text.read_poses(text, reduced, mapping)
    assert snapshot(reduced) == before


def test_omitted_h_is_explicit_subsystem_not_projected_chemistry():
    source, reduced, projection, _, _, _ = _case('CO')
    retained = projection['output_to_source_atom_indices'].tolist()
    selected = msm.extract(source, selection=retained)
    text, mapping = msm.convert(
        source,
        to_form='string:pdbqt_text',
        selection=retained,
        typing_scheme='autodock4',
        torsion_tree=_tree(selected),
        return_atom_map=True,
    )
    with pytest.raises(FormatError, match='omitted source atoms'):
        msm.form.string_pdbqt_text.read_poses(text, source, mapping)
    out = msm.form.string_pdbqt_text.read_poses(
        text, source, mapping, missing_atoms='omit', return_report=True
    )
    assert out['report']['omitted_source_atom_indices'].tolist() == [2, 3, 4]
    assert msm.get(
        out['molecular_system'], selection=[0], n_explicit_hydrogens=True
    ) == [0]
    assert msm.get(reduced, selection=[0], n_explicit_hydrogens=True) == [3]


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_real_dockingmt_vina_output_matches_native_pose_reader(
    length_unit, monkeypatch, tmp_path
):
    import vina

    _, reduced, projection, text, mapping, tree = _case('CCCCCC')
    before = snapshot(reduced)
    observed = []
    original = vina.Vina

    class RecordedVina(original):
        def poses(self, *args, **kwargs):
            value = super().poses(*args, **kwargs)
            if kwargs.get('coordinates_only') is False:
                observed.append(value)
            return value

    monkeypatch.setattr(vina, 'Vina', RecordedVina)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        problem = dmt.DockingProblem(
            receptor='pdbqt_text:' + MINIMAL_REC_PDBQT,
            partner=text,
            search_domain=dmt.BoxRegion(
                center=puw.quantity([0, 0, 0], 'angstrom'),
                size=puw.quantity([16, 16, 16], 'angstrom'),
            ),
        )
        result = dmt.dock(
            problem,
            protocol=dmt.VinaProtocol(
                exhaustiveness=1, n_poses=2, seed=14, cpu=1, capture_backend_inputs=True
            ),
        )
        assert len(observed) == 1
        received = msm.form.string_pdbqt_text.read_poses(
            'pdbqt_text:' + observed[0], reduced, mapping, return_report=True
        )
    native, report = received['molecular_system'], received['report']
    assert 1 <= len(result.poses) <= 2
    assert report['n_input_structures'] == len(result.poses)
    assert (
        result.provenance['backend_artifacts']['partner']['sha256']
        == mapping['payload_sha256']
    )
    assert (
        report['input_payload_sha256']
        == hashlib.sha256(observed[0].encode()).hexdigest()
    )
    actual = puw.get_value(msm.get(native, coordinates=True), to_unit='angstrom')
    written = actual[:, report['pdbqt_to_output_atom_indices']]
    expected = np.asarray(
        [puw.get_value(pose.coordinates, to_unit='angstrom') for pose in result.poses]
    )
    np.testing.assert_allclose(written, expected, rtol=0, atol=1e-10)
    assert snapshot(reduced) == before
    assert all(
        pose.metadata['pose_atom_order'] == 'verified_pdbqt_order'
        for pose in result.poses
    )
    assert result.provenance['preparation']['partner']['assessment'] == 'unassessed'
    assert all(pose.scores for pose in result.poses)
    # The existing engine-boundary check remains the independent comparator.
    np.testing.assert_allclose(
        _verify_pose_atom_order(text.removeprefix('pdbqt_text:'), observed[0], written),
        written,
        rtol=0,
        atol=1e-10,
    )
    payload = {
        'scope': 'synthetic receptor/hexane software control; not biological redocking',
        'native_report': detached_record(report),
        'projection_report': detached_record(projection),
        'result': result.to_dict(),
        'source_unchanged': True,
        'native_source_axis_coordinates': actual.tolist(),
        'coordinate_unit': 'angstrom',
    }
    (tmp_path / 'receiving.json').write_text(json.dumps(payload, indent=2) + '\n')
    (tmp_path / 'poses.pdbqt').write_text(observed[0])


def test_legacy_preparation_does_not_acquire_a_native_export_map():
    _, reduced, _, _, mapping, _ = _case('CO')
    before = snapshot(reduced)
    # Preserve this historical guard's selector. The prepared producer now uses
    # native writing too, but its explicit presentation still differs from the
    # independently exported default axis bound by this particular map.
    prepared = dmt.prepare_ligand(reduced, selection='all')
    assert prepared.n_atoms == 3
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'
    legacy = prepared.to_pdbqt()
    assert hashlib.sha256(legacy.encode()).hexdigest() != mapping['payload_sha256']
    with pytest.raises(FormatError, match='serial IDs'):
        msm.form.string_pdbqt_text.read_poses('pdbqt_text:' + legacy, reduced, mapping)
    assert prepared.to_pdbqt() == legacy
    assert snapshot(reduced) == before
