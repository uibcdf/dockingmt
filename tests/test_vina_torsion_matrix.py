"""Pinned Vina reference trees with a separate RDKit torsion count baseline."""

import molsysmt as msm
import pytest
from rdkit import Chem
from rdkit.Chem import Lipinski, rdMolDescriptors

from bindingmt.preparation import prepare_ligand
from bmt_test_support.audit_1iep_preparation import _pdbqt_torsion_graph
from bmt_test_support.qualify_named_types import CHARGE, HYDROGEN, TYPING
from bmt_test_support.torsion_reference_fixtures import (
    CASES as CASES,
)
from bmt_test_support.torsion_reference_fixtures import (
    FIXTURES as FIXTURES,
)
from bmt_test_support.torsion_reference_fixtures import (
    _atom_map as _atom_map,
)
from bmt_test_support.torsion_reference_fixtures import (
    _reference as _reference,
)
from bmt_test_support.torsion_reference_fixtures import (
    _source as _source,
)
from bmt_test_support.torsion_reference_fixtures import (
    _source_graph as _source_graph,
)

# Filename, source SHA-256, reference SHA-256, branch count, RDKit Strict,
# RDKit NonStrict, reference-only hydrogen count, fragment sizes.


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

    molsys = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(
            msm.build.add_missing_hydrogens(
                msm.convert(source, to_form='molsysmt.MolSys'), **HYDROGEN
            ),
            **CHARGE,
        ),
        **TYPING,
    )
    prepared = prepare_ligand(
        molsys, selection='all', active_torsion_bonds=selected_bonds
    )
    native = prepared.to_pdbqt().encode()
    native_serials, native_atoms, native_unmatched_hydrogens = _atom_map(native, source)
    # The neutral 1S63 SDF has no donor H. The independent reference includes
    # one extra HD; its chemical preparation is not reproduced by this test.
    assert native_unmatched_hydrogens == 0
    assert set(native_serials.values()) == set(reference_serials.values())
    reference_bonds, reference_fragments = _source_graph(reference, reference_atoms)
    native_bonds, native_fragments = _source_graph(native, native_atoms)
    assert native_bonds == reference_bonds
    assert native_fragments == reference_fragments
    retained_sources = set(reference_serials.values())
    provider_blocks = msm.chemical_states.get_covalent_blocks(
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
        assert nitrile_axis in reference_bonds  # Aryl–C≡N, bindingmt#17.
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
