"""Receive provider-owned output presentation before replacing local writers."""

import hashlib
import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
import test_native_ligand_export_receiving as native_ligands
from molecular_fixtures import named_181l_pair
from test_engines import MINIMAL_REC_PDBQT
from vina import Vina

from devtools.qualify_chemical_templates import detached_record, snapshot
from dockingmt.engines.vina import _verify_pose_atom_order
from dockingmt.preparation._typing import type_remark
from dockingmt.preparation.charges import _charge_remark

export_case = native_ligands.export_case


def _presentation(prepared):
    """The existing DockingMT display policy on the prepared atom axis."""
    return {
        'atom_serials': 'consecutive',
        'atom_names': prepared.atom_names,
        'group_names': prepared.group_names,
        'group_ids': [str(value) for value in prepared.group_ids],
        'chain_ids': 'A',
        'occupancy': 1.0,
        'b_factor': puw.quantity(0.0, 'angstrom**2'),
    }


def _remarks(prepared):
    return _charge_remark(prepared) + type_remark(prepared)


def _export(prepared, tree, **kwargs):
    return msm.convert(
        prepared.source_molsys,
        to_form='string:pdbqt_text',
        structure_indices=0,
        typing_scheme='autodock4',
        torsion_tree=tree,
        output_presentation=_presentation(prepared),
        remarks=_remarks(prepared),
        return_atom_map=True,
        **kwargs,
    )


def _atom_fields(payload):
    """Independent fixed-column inspection; no molecular reconstruction."""
    return [
        (
            line[6:11].strip(),
            line[12:16].strip(),
            line[17:20].strip(),
            line[21],
            line[22:26].strip(),
            line[30:54],
            line[54:66],
            line[70:76],
            line[77:].strip(),
        )
        for line in payload.splitlines()
        if line.startswith('ATOM')
    ]


@pytest.fixture
def prepared_case(export_case):
    prepared, _, tree, _ = export_case
    # The old receiving fixture renumbers a separate copy. The new contract
    # must instead bind the unchanged original native IDs to output serials.
    tree = deepcopy(tree)
    tree['atom_ids'] = msm.get(prepared.source_molsys, element='atom', atom_id=True)
    return prepared, tree


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_prepared_ligand_presentation_preserves_fields_and_original_axes(
    prepared_case, length_unit, tmp_path
):
    prepared, tree = prepared_case
    native = prepared.source_molsys
    before = snapshot(native)
    mechanics = detached_record(native.molecular_mechanics.to_dict())
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        text, mapping = _export(prepared, tree)
        assert puw.configure.report() == policy
    payload = text.removeprefix('pdbqt_text:')
    assert _atom_fields(payload) == _atom_fields(prepared.to_pdbqt())
    assert [line.split() for line in payload.splitlines() if 'BRANCH' in line] == [
        line.split() for line in prepared.to_pdbqt().splitlines() if 'BRANCH' in line
    ]
    assert payload.endswith(f'TORSDOF {prepared.torsion_dof}\n')
    assert all(line in payload.splitlines() for line in _remarks(prepared))
    assert mapping['payload_sha256'] == hashlib.sha256(payload.encode()).hexdigest()
    assert list(mapping['source_atom_ids']) == list(
        msm.get(native, element='atom', atom_id=True)
    )
    assert list(mapping['output_atom_ids']) == [
        str(i + 1) for i in range(prepared.n_atoms)
    ]
    np.testing.assert_array_equal(
        mapping['output_to_source_atom_indices'], prepared.pdbqt_atom_indices
    )
    composed = msm.compose_atom_maps(
        [prepared.metadata['molecular_projection'], mapping]
    )
    expected = [
        prepared.metadata['retained_atom_indices'][i]
        for i in prepared.pdbqt_atom_indices
    ]
    assert list(composed['output_to_source_atom_indices']) == expected
    for prefix, assignment in [
        ('PARTIAL_CHARGES', native.molecular_mechanics.partial_charge_assignment),
        ('ATOM_TYPES', native.molecular_mechanics.atom_type_assignment),
    ]:
        line_prefix = 'REMARK MOLSYSMT_' + prefix + ' '
        remark = json.loads(
            next(
                line[len(line_prefix) :]
                for line in payload.splitlines()
                if line.startswith(line_prefix)
            )
        )
        assert remark['status'] == assignment['status'] == 'derived'
        assert remark['method'] == assignment['method']
    path = tmp_path / 'ligand.pdbqt'
    filename, file_map = msm.convert(
        native,
        to_form='file:pdbqt',
        output_filename=path,
        typing_scheme='autodock4',
        torsion_tree=tree,
        output_presentation=_presentation(prepared),
        remarks=_remarks(prepared),
        return_atom_map=True,
    )
    assert str(filename) == str(path)
    assert path.read_bytes() == payload.encode()
    assert file_map['payload_sha256'] == mapping['payload_sha256']
    Vina(cpu=1, verbosity=0).set_ligand_from_string(payload)
    assert msm.get(native, n_groups=True) == msm.get(native, n_chains=True) == 0
    assert snapshot(native) == before
    assert detached_record(native.molecular_mechanics.to_dict()) == mechanics
    json.dumps(detached_record(composed), allow_nan=False)


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_presented_known_source_poses_restore_original_labels(
    prepared_case, length_unit
):
    prepared, tree = prepared_case
    native = prepared.source_molsys
    before = snapshot(native)
    options = _presentation(prepared)
    options['atom_names'] = [f'X{i}' for i in range(prepared.n_atoms)]
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        text, mapping = msm.convert(
            native,
            to_form='string:pdbqt_text',
            typing_scheme='autodock4',
            torsion_tree=tree,
            output_presentation=options,
            remarks=_remarks(prepared),
            return_atom_map=True,
        )
        body = text.removeprefix('pdbqt_text:')
        ensemble = 'pdbqt_text:' + ''.join(
            f'MODEL {label}\n{body}ENDMDL\n' for label in ('7', '2')
        )
        received = msm.form.string_pdbqt_text.read_poses(
            ensemble, native, mapping, return_report=True
        )
        composed = msm.compose_atom_maps(
            [prepared.metadata['molecular_projection'], mapping, received['report']]
        )
    restored = received['molecular_system']
    assert list(msm.get(restored, element='atom', atom_id=True)) == list(
        msm.get(native, element='atom', atom_id=True)
    )
    assert list(msm.get(restored, element='atom', atom_name=True)) == list(
        msm.get(native, element='atom', atom_name=True)
    )
    assert list(msm.get(restored, structure_id=True)) == ['7', '2']
    np.testing.assert_allclose(
        puw.get_value(msm.get(restored, coordinates=True), to_unit='angstrom'),
        np.repeat(
            puw.get_value(prepared.coordinates, to_unit='angstrom')[None], 2, axis=0
        ),
        rtol=0,
        atol=0.000501,
    )
    assert (
        list(composed['output_to_source_atom_indices'])
        == (prepared.metadata['retained_atom_indices'])
    )
    assert snapshot(native) == before


@pytest.fixture(scope='module')
def protein():
    return named_181l_pair()[0]


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_real_receptor_presentation_composes_without_source_renumbering(
    protein, length_unit, tmp_path
):
    native = protein.source_molsys
    before = snapshot(native)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        text, mapping = _export(protein, None)
        composed = msm.compose_atom_maps(
            [protein.metadata['preparation_workflow']['atom_map'], mapping]
        )
    payload = text.removeprefix('pdbqt_text:')
    assert _atom_fields(payload) == _atom_fields(protein.to_pdbqt())
    assert mapping['payload_sha256'] == hashlib.sha256(payload.encode()).hexdigest()
    assert list(mapping['source_atom_ids']) != list(mapping['output_atom_ids'])
    assert list(mapping['source_atom_ids']) == list(
        msm.get(native, element='atom', atom_id=True)
    )
    assert composed['n_source_atoms'] == 2603 and composed['n_output_atoms'] == 1615
    assert list(composed['source_atom_status']).count('merged') == 988
    assert (
        list(composed['output_to_source_atom_indices'])
        == (protein.metadata['retained_atom_indices'])
    )
    assert all(line in payload.splitlines() for line in _remarks(protein))
    path = tmp_path / 'receptor.pdbqt'
    path.write_text(payload)
    Vina(cpu=1, verbosity=0).set_receptor(str(path))
    assert snapshot(native) == before


def test_actual_vina_poses_follow_presented_flexible_map(tmp_path):
    from test_known_source_pose_consumption import _case

    _, native, projection, _, _, tree = _case('CCCCCC')
    before = snapshot(native)
    text, mapping = msm.convert(
        native,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        torsion_tree=tree,
        output_presentation={
            'atom_serials': 'consecutive',
            'atom_names': [f'X{i}' for i in range(6)],
            'group_names': 'LIG',
            'group_ids': '1',
            'chain_ids': 'A',
        },
        remarks=['REMARK DOCKINGMT_RECEIVING presented-flexible-control'],
        return_atom_map=True,
    )
    receptor = tmp_path / 'minimal-receptor.pdbqt'
    receptor.write_text(MINIMAL_REC_PDBQT)
    engine = Vina(cpu=1, seed=321, verbosity=0)
    engine.set_receptor(str(receptor))
    engine.set_ligand_from_string(text.removeprefix('pdbqt_text:'))
    engine.compute_vina_maps(center=[0, 0, 0], box_size=[15, 15, 15])
    engine.dock(exhaustiveness=1, n_poses=2)
    output = engine.poses(n_poses=2)
    received = msm.form.string_pdbqt_text.read_poses(
        'pdbqt_text:' + output, native, mapping, return_report=True
    )
    coordinates = puw.get_value(
        msm.get(received['molecular_system'], coordinates=True), to_unit='angstrom'
    )
    raw = np.asarray(engine.poses(n_poses=2, coordinates_only=True))
    # The existing engine guard checks Vina's numeric-array coherence and
    # returns written order; native identity restoration belongs to MolSysMT.
    order = mapping['output_to_source_atom_indices']
    checked = _verify_pose_atom_order(text.removeprefix('pdbqt_text:'), output, raw)
    np.testing.assert_allclose(coordinates[:, order], checked, rtol=0, atol=1e-10)
    composed = msm.compose_atom_maps([projection, mapping, received['report']])
    assert composed['n_output_atoms'] == 6
    assert snapshot(native) == before
