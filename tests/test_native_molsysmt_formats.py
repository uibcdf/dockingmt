"""Consumer acceptance of the prepared-input profile in dockingmt#33."""

import hashlib
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt._private.smonitor import FormatError
from molsysmt.form.file_pdbqt import get_torsion_tree
from molsysmt.form.string_pdbqt_text import get_torsion_tree as string_tree
from test_vina_torsion_matrix import CASES

import dockingmt as dmt

DATA = Path(__file__).parent / 'data/vina_torsions'
PREPARED = [(case[0], case[2], case[3]) for case in CASES] + [
    (
        '1iep_receptor',
        'f13cf3b36f61d87c3b58983e0b8ecf1c3456a685eb86dfe9ccfb139c7bdc2586',
        None,
    )
]


def _atoms(content):
    """Independent fixed-column expectations; no production molecular reader."""
    records = [
        line for line in content.splitlines() if line.startswith(('ATOM', 'HETATM'))
    ]
    return {
        'ids': [line[6:11].strip() for line in records],
        'labels': [line.split()[-1] for line in records],
        'charges': [float(line[70:76]) for line in records],
        'coordinates': [
            [float(line[start : start + 8]) for start in (30, 38, 46)]
            for line in records
        ],
    }


def _snapshot(source):
    data = msm.get(
        source,
        element='atom',
        atom_id=True,
        atom_type=True,
        atom_ff_type=True,
        partial_charge=True,
        coordinates=True,
        output_type='dictionary',
    )
    return {
        **{
            name: np.asarray(data[name]).copy()
            for name in ('atom_id', 'atom_type', 'atom_ff_type', 'partial_charge')
        },
        'coordinates': np.asarray(
            puw.get_value(data['coordinates'], to_unit='angstrom')
        )[0].copy(),
    }


def _tree_ids(tree):
    if tree is None:
        return None
    ids = tree['atom_ids']
    packed = tree['fragment_atom_indices']
    offsets = tree['fragment_offsets']
    return {
        'bonds': {frozenset(ids[pair]) for pair in tree['branch_atom_pairs']},
        'fragments': {
            frozenset(ids[packed[start:stop]])
            for start, stop in zip(offsets[:-1], offsets[1:])
        },
        'torsdof': tree['torsdof'],
    }


@pytest.mark.parametrize('name,digest,branches', PREPARED)
def test_prepared_pdbqt_public_roundtrip_and_vina_admission(
    name, digest, branches, tmp_path
):
    from vina import Vina

    source = DATA / f'{name}.pdbqt'
    original = source.read_bytes()
    assert hashlib.sha256(original).hexdigest() == digest
    expected = _atoms(original.decode())
    assert msm.get_form(source) == 'file:pdbqt'
    payload = msm.convert(source, to_form='string:pdbqt_text')
    assert payload == 'pdbqt_text:' + original.decode()
    tree = get_torsion_tree(source)
    assert _tree_ids(tree) == _tree_ids(string_tree(payload))
    if branches is not None:
        assert len(tree['branch_atom_pairs']) == branches
        assert tree['atom_ids'].tolist() == expected['ids']
        with pytest.raises(FormatError, match='discard_torsion_tree'):
            msm.convert(source, to_form='molsysmt.MolSys')
    else:
        assert tree is None
    native, report = msm.convert(
        payload,
        to_form='molsysmt.MolSys',
        discard_torsion_tree=True,
        return_report=True,
    )
    assert report.outcome == ('equivalent' if branches is None else 'lossy')
    before = _snapshot(native)
    np.testing.assert_array_equal(before['atom_id'], expected['ids'])
    np.testing.assert_array_equal(before['atom_ff_type'], expected['labels'])
    np.testing.assert_allclose(
        before['partial_charge'].astype(float), expected['charges'], atol=1e-12
    )
    np.testing.assert_allclose(
        before['coordinates'], expected['coordinates'], atol=1e-10
    )
    assert 'H' in before['atom_type']
    assert not msm.has_attribute(native, 'bond_order')
    converted = msm.convert(
        native,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        torsion_tree=tree,
    )
    restored = _snapshot(converted)
    # Native tree traversal may reorder atoms: align by retained serial IDs.
    positions = {identity: index for index, identity in enumerate(restored['atom_id'])}
    order = [positions[identity] for identity in before['atom_id']]
    for key in before:
        if key in ('atom_id', 'atom_type', 'atom_ff_type'):
            np.testing.assert_array_equal(restored[key][order], before[key])
        else:
            np.testing.assert_allclose(
                restored[key][order].astype(float),
                before[key].astype(float),
                atol=1e-10,
            )
    assert _tree_ids(string_tree(converted)) == _tree_ids(tree)
    raw = converted.removeprefix('pdbqt_text:')
    engine = Vina(cpu=1, verbosity=0)
    if branches is None:
        output = tmp_path / 'receptor.pdbqt'
        msm.convert(native, to_form=output, typing_scheme='autodock4')
        engine.set_receptor(str(output))
    else:
        engine.set_ligand_from_string(raw)
    after = _snapshot(native)
    for key in before:
        np.testing.assert_array_equal(after[key], before[key])
    assert source.read_bytes() == original


def test_prepared_pdbqt_serialization_uses_explicit_angstrom_under_pm_policy():
    source = DATA / '1iep_ligand.pdbqt'
    expected = _snapshot(source)
    with puw.context(standard_units=['pm', 'fs']):
        native = msm.convert(
            source, to_form='molsysmt.MolSys', discard_torsion_tree=True
        )
        payload = msm.convert(
            native,
            to_form='string:pdbqt_text',
            typing_scheme='autodock4',
            torsion_tree=get_torsion_tree(source),
        )
        actual = _snapshot(payload)
    np.testing.assert_allclose(
        actual['coordinates'], expected['coordinates'], atol=1e-10
    )


@pytest.mark.parametrize('name', ['5x72_ligand_p59', '5x72_ligand_p69'])
def test_supported_native_sdf_preserves_chemistry_and_stereo(name, tmp_path):
    source = DATA / f'{name}H.sdf'
    original = source.read_bytes()
    native, report = msm.convert(
        source,
        to_form='molsysmt.MolSys',
        stereo_engine='rdkit',
        discard_properties=True,
        return_report=True,
    )
    assert report.outcome == 'lossy'
    assert msm.get(native, element='system', n_atoms=True) == 39
    assert msm.get(native, element='system', n_bonds=True) == 42
    elements = msm.get(native, element='atom', atom_type=True)
    assert elements.count('H') == 15
    before = msm.physchem.get_cip_stereochemistry(native)
    assert any(label in ('R', 'S') for label in before['atom_stereochemistry'])
    assert before['atom_stereochemistry'][7] == ('R' if name.endswith('p59') else 'S')
    output = tmp_path / 'roundtrip.sdf'
    msm.convert(native, to_form=output, ctfile_version='V3000', stereo_engine='rdkit')
    restored = msm.convert(output, to_form='molsysmt.MolSys', stereo_engine='rdkit')
    after = msm.physchem.get_cip_stereochemistry(restored)
    np.testing.assert_array_equal(
        before['atom_stereochemistry'], after['atom_stereochemistry']
    )
    for attribute, element in [
        ('atom_type', 'atom'),
        ('formal_charge', 'atom'),
        ('bond_order', 'bond'),
        ('bonded_atom_pairs', 'bond'),
    ]:
        np.testing.assert_array_equal(
            msm.get(native, element=element, **{attribute: True}),
            msm.get(restored, element=element, **{attribute: True}),
        )
    np.testing.assert_allclose(
        puw.get_value(msm.get(native, coordinates=True), to_unit='angstrom'),
        puw.get_value(msm.get(restored, coordinates=True), to_unit='angstrom'),
        atol=1e-4,
    )
    assert source.read_bytes() == original


@pytest.mark.parametrize(
    'name,message',
    [('1iep_ligand', 'Unsupported atom flag'), ('1s63_ligand', 'explicitly versioned')],
)
def test_pinned_sdf_dialects_outside_current_native_profile_fail_explicitly(
    name, message
):
    # Profile gaps reported in molsysmt#215 and dockingmt#33; no normalization.
    with pytest.raises(FormatError, match=message):
        msm.convert(
            DATA / f'{name}.sdf',
            to_form='molsysmt.MolSys',
            stereo_engine='rdkit',
            discard_properties=True,
        )


@pytest.mark.parametrize(
    'change', ['duplicate-id', 'unbalanced-tree', 'flexible-receptor']
)
def test_malformed_or_unsupported_pdbqt_is_rejected(change, tmp_path):
    content = (DATA / '1iep_ligand.pdbqt').read_text()
    if change == 'duplicate-id':
        lines = content.splitlines()
        atoms = [i for i, line in enumerate(lines) if line.startswith('ATOM')]
        lines[atoms[1]] = (
            lines[atoms[1]][:6] + lines[atoms[0]][6:11] + lines[atoms[1]][11:]
        )
        content = '\n'.join(lines) + '\n'
    elif change == 'unbalanced-tree':
        content = '\n'.join(
            line for line in content.splitlines() if not line.startswith('ENDBRANCH')
        )
    else:
        content = 'BEGIN_RES ALA A 1\n' + content + '\nEND_RES ALA A 1\n'
    source = tmp_path / 'unsupported.pdbqt'
    source.write_text(content)
    with pytest.raises(FormatError):
        msm.convert(source, to_form='molsysmt.MolSys', discard_torsion_tree=True)
    assert source.read_text() == content


def test_stale_tree_rejected_before_destination_mutation(tmp_path):
    source = DATA / '1iep_ligand.pdbqt'
    native = msm.convert(source, to_form='molsysmt.MolSys', discard_torsion_tree=True)
    tree = get_torsion_tree(source)
    tree['atom_ids'] = tree['atom_ids'][::-1].copy()
    output = tmp_path / 'keep.pdbqt'
    output.write_text('keep original')
    with pytest.raises(FormatError):
        msm.convert(
            native, to_form=output, typing_scheme='autodock4', torsion_tree=tree
        )
    assert output.read_text() == 'keep original'


def test_native_fragment_cuts_match_temporary_bridge_on_5x72():
    from dockingmt.preparation._temporary_torsions import build_torsion_tree

    source = msm.convert(
        DATA / '5x72_ligand_p59H.sdf',
        to_form='molsysmt.MolSys',
        stereo_engine='rdkit',
        discard_properties=True,
    )
    pairs = np.asarray(msm.get(source, element='bond', bonded_atom_pairs=True))
    # Explicit published heavy-atom cuts mapped by coordinates/element below.
    reference = _snapshot(DATA / '5x72_ligand_p59.pdbqt')
    coordinates = np.asarray(
        puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')
    )[0]
    elements = msm.get(source, element='atom', atom_type=True)
    mapping = []
    for xyz, element in zip(reference['coordinates'], reference['atom_type']):
        matches = [
            i
            for i in range(len(elements))
            if elements[i] == element and np.linalg.norm(coordinates[i] - xyz) <= 0.002
        ]
        assert len(matches) == 1
        mapping.append(matches[0])
    assert len(mapping) == len(set(mapping))
    tree = get_torsion_tree(DATA / '5x72_ligand_p59.pdbqt')
    cuts = [tuple(mapping[i] for i in pair) for pair in tree['branch_atom_pairs']]
    indices = [
        next(i for i, pair in enumerate(pairs) if set(pair) == set(cut)) for cut in cuts
    ]
    provider = msm.topology.get_rigid_fragments(source, bond_indices=indices)
    packed, offsets = provider['fragment_atom_indices'], provider['fragment_offsets']
    retained = set(mapping)
    fragments = {
        frozenset(retained.intersection(packed[start:stop]))
        for start, stop in zip(offsets[:-1], offsets[1:])
    }
    bridge = build_torsion_tree(source, mapping, cuts, elements)
    bridge_fragments = {frozenset(mapping[i] for i in bridge.root_atoms)}

    def visit(branches):
        for branch in branches:
            bridge_fragments.add(frozenset(mapping[i] for i in branch.atoms))
            visit(branch.children)

    visit(bridge.branches)
    assert bridge_fragments == fragments


def test_molsysmt_explicit_strings_reach_vina_without_format_prefix():
    from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT

    problem = dmt.DockingProblem(
        receptor='pdbqt_text:' + MINIMAL_REC_PDBQT,
        partner='pdbqt_text:' + MINIMAL_LIG_PDBQT,
        search_domain=dmt.BoxRegion(
            center=puw.quantity([0, 0, 0], 'angstrom'),
            size=puw.quantity([10, 10, 10], 'angstrom'),
        ),
    )
    result = dmt.dock(
        problem,
        protocol=dmt.VinaProtocol(
            cpu=1, seed=123, n_poses=2, exhaustiveness=1, capture_backend_inputs=True
        ),
    )
    assert result.poses
    for role, content in [
        ('receptor', MINIMAL_REC_PDBQT),
        ('partner', MINIMAL_LIG_PDBQT),
    ]:
        assert (
            result.provenance['backend_artifacts'][role]['sha256']
            == hashlib.sha256(content.encode()).hexdigest()
        )
        assert result.provenance['preparation'][role]['assessment'] == 'unassessed'
