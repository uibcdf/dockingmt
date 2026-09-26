"""Pinned Vina reference trees with a separate RDKit torsion count baseline."""

import hashlib
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
from rdkit import Chem
from rdkit.Chem import Lipinski, rdMolDescriptors

from devtools.audit_1iep_preparation import _pdbqt_torsion_graph
from dockingmt.preparation import prepare_ligand
from dockingmt.preparation._molsys import autodock_element

FIXTURES = Path(__file__).parent / 'data' / 'vina_torsions'

# Filename, source SHA-256, reference SHA-256, branch count, RDKit Strict,
# RDKit NonStrict, reference-only hydrogen count, fragment sizes.
CASES = [
    (
        '1iep_ligand',
        '051b8742c32adc05c07fb486a4e7c9327f84e131cee33ac4e6a568d07553eb38',
        '15fb35648d8c18c70317842f3a0631b73a19429c710a037ab07310084d579bb8',
        7,
        7,
        8,
        0,
        [1, 2, 4, 6, 6, 6, 7, 8],
    ),
    (
        '1s63_ligand',
        '6eb488b5770df7f132745249e64000fcfe394acf938b45f0e082f44365f59119',
        '04fb28c75bc5a8b32fd7f985ef8ac9a9b4581a40141f4f5b1b3951c2051fb7dc',
        6,
        5,
        5,
        1,
        [1, 1, 2, 5, 6, 7, 8],
    ),
    (
        '5x72_ligand_p59',
        'ef26c05a198a16972efcf8baae644f6b38fd953561f130ee230626088766b08a',
        '67cf462419372e365b8129bc1047f94598f3a1f3c495375781c1c1100e95c92e',
        2,
        2,
        2,
        0,
        [6, 7, 12],
    ),
    (
        '5x72_ligand_p69',
        '637a992134b2038a0ea3cff0c1f8355ea232720c9eae5347100b7186170fcdf1',
        '276a991d56ddc7778ed36c10aba6b7231de00b87294a7f77e2fceb9a96ae08e5',
        2,
        2,
        2,
        0,
        [6, 7, 12],
    ),
]


def _source(case_name, expected_digest):
    suffix = 'H' if case_name.startswith('5x72') else ''
    path = FIXTURES / f'{case_name}{suffix}.sdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_digest
    molecules = list(Chem.SDMolSupplier(str(path), removeHs=False))
    assert len(molecules) == 1 and molecules[0] is not None
    return molecules[0]


def _reference(case_name, expected_digest):
    content = (FIXTURES / f'{case_name}.pdbqt').read_bytes()
    assert hashlib.sha256(content).hexdigest() == expected_digest
    return content


def _atom_map(content, source):
    """Match only unique, same-element source atoms within PDBQT rounding error."""
    coordinates = np.asarray(source.GetConformer().GetPositions())
    elements = [atom.GetSymbol() for atom in source.GetAtoms()]
    coordinate_to_source = {}
    serial_to_source = {}
    used_sources = set()
    unmatched_hydrogens = 0
    for line in content.decode().splitlines():
        if not line.startswith(('ATOM', 'HETATM')):
            continue
        serial = int(line[6:11])
        xyz = tuple(float(line[offset : offset + 8]) for offset in (30, 38, 46))
        element = autodock_element(line.split()[-1])
        distances = np.linalg.norm(coordinates - np.asarray(xyz), axis=1)
        matches = [
            index
            for index, distance in enumerate(distances)
            if distance <= 0.002 and elements[index] == element
        ]
        if not matches and element == 'H':
            unmatched_hydrogens += 1
            coordinate_to_source[xyz] = None
            continue
        assert len(matches) == 1, (serial, xyz, matches)
        source_index = matches[0]
        assert source_index not in used_sources
        assert serial not in serial_to_source and xyz not in coordinate_to_source
        used_sources.add(source_index)
        serial_to_source[serial] = source_index
        coordinate_to_source[xyz] = source_index
    return serial_to_source, coordinate_to_source, unmatched_hydrogens


def _source_graph(content, coordinate_to_source):
    graph = _pdbqt_torsion_graph(content)
    bonds = {
        frozenset(coordinate_to_source[xyz] for xyz in pair) for pair in graph['bonds']
    }
    assert all(None not in bond and len(bond) == 2 for bond in bonds)
    fragments = {
        frozenset(
            source_index
            for xyz in fragment
            if (source_index := coordinate_to_source[xyz]) is not None
        )
        for fragment in graph['fragments']
    }
    assert all(fragments)
    return bonds, fragments


@pytest.mark.parametrize(
    (
        'case_name',
        'source_digest',
        'reference_digest',
        'branch_count',
        'strict_count',
        'non_strict_count',
        'reference_hydrogens',
        'fragment_sizes',
    ),
    CASES,
    ids=['1iep', '1s63', '5x72-p59', '5x72-p69'],
)
def test_pinned_vina_torsion_tree_matches_source_fragments(
    case_name,
    source_digest,
    reference_digest,
    branch_count,
    strict_count,
    non_strict_count,
    reference_hydrogens,
    fragment_sizes,
):
    source = _source(case_name, source_digest)
    reference = _reference(case_name, reference_digest)
    reference_serials, reference_atoms, unmatched_hydrogens = _atom_map(
        reference, source
    )
    assert unmatched_hydrogens == reference_hydrogens
    assert len(reference_serials) + unmatched_hydrogens == sum(
        line.startswith((b'ATOM', b'HETATM')) for line in reference.splitlines()
    )
    selected_bonds = [
        tuple(reference_serials[int(serial)] for serial in line.split()[1:3])
        for line in reference.decode().splitlines()
        if line.startswith('BRANCH')
    ]
    assert len(selected_bonds) == branch_count

    molsys = msm.convert(source, to_form='molsysmt.MolSys')
    prepared = prepare_ligand(
        molsys, selection='all', active_torsion_bonds=selected_bonds
    )
    native = prepared.to_pdbqt().encode()
    native_serials, native_atoms, native_unmatched_hydrogens = _atom_map(native, source)
    assert native_unmatched_hydrogens == 0
    assert set(native_serials.values()) == set(reference_serials.values())
    reference_bonds, reference_fragments = _source_graph(reference, reference_atoms)
    native_bonds, native_fragments = _source_graph(native, native_atoms)
    assert native_bonds == reference_bonds
    assert native_fragments == reference_fragments
    retained_sources = set(reference_serials.values())
    provider_blocks = msm.topology.get_covalent_blocks(
        molsys, remove_bonds=selected_bonds, output_type='sets'
    )
    assert native_fragments == {
        frozenset(block & retained_sources) for block in provider_blocks
    }
    assert (
        sorted(map(len, _pdbqt_torsion_graph(reference)['fragments'])) == fragment_sizes
    )
    assert prepared.torsion_dof == branch_count

    heavy_source = Chem.RemoveHs(source)
    assert (
        rdMolDescriptors.CalcNumRotatableBonds(
            heavy_source, rdMolDescriptors.NumRotatableBondsOptions.Strict
        )
        == strict_count
    )
    assert (
        rdMolDescriptors.CalcNumRotatableBonds(
            heavy_source, rdMolDescriptors.NumRotatableBondsOptions.NonStrict
        )
        == non_strict_count
    )
    if case_name == '1s63_ligand':
        nitrile_axis = frozenset((26, 27))
        assert nitrile_axis in reference_bonds  # Aryl–C≡N, dockingmt#17.
        rdkit_candidates = {
            frozenset(pair)
            for pair in heavy_source.GetSubstructMatches(Lipinski.RotatableBondSmarts)
        }
        assert rdkit_candidates == reference_bonds - {nitrile_axis}

    try:
        import vina
    except ImportError:
        pass  # Vina is an optional runtime dependency; graph checks still run.
    else:
        vina.Vina(verbosity=0).set_ligand_from_string(native.decode())


def test_5x72_pair_has_same_connectivity_and_opposite_stereochemistry():
    p59 = Chem.RemoveHs(_source('5x72_ligand_p59', CASES[2][1]))
    p69 = Chem.RemoveHs(_source('5x72_ligand_p69', CASES[3][1]))
    assert Chem.MolToSmiles(p59, isomericSmiles=False) == Chem.MolToSmiles(
        p69, isomericSmiles=False
    )
    assert Chem.MolToSmiles(p59) != Chem.MolToSmiles(p69)
