"""Provider partitioning preserves reference trees and retained atom identity."""

import hashlib
import json
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from test_flexible_ligand import _ligand
from test_vina_torsion_matrix import _atom_map, _reference, _source, _source_graph

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation import prepare_ligand
from dockingmt.preparation._temporary_torsions import build_torsion_tree

BASELINE_PATH = (
    Path(__file__).parents[1] / 'devguide/validation/data/fragments/legacy_trees.json'
)
BASELINE = json.loads(BASELINE_PATH.read_text())


@pytest.mark.parametrize('case', BASELINE['cases'], ids=lambda case: case['case'])
def test_original_matrix_preserves_tree_and_consumes_provider(case, monkeypatch):
    molecule = _source(case['case'], case['source_sdf_sha256'])
    source = msm.convert(molecule, to_form='molsysmt.MolSys')
    before_coordinates = np.array(
        puw.get_value(
            msm.get(source, element='atom', coordinates=True), to_unit='angstrom'
        ),
        copy=True,
    )
    before_pairs = np.array(
        msm.get(source, element='bond', bonded_atom_pairs=True), copy=True
    )
    before_ids = list(msm.get(source, element='atom', atom_id=True))
    calls = []
    classifications = []
    provider = msm.topology.get_rigid_fragments
    classifier = msm.topology.get_rotatable_bonds

    def recorded_classification(molecular_system, **kwargs):
        report = classifier(molecular_system, **kwargs)
        assert kwargs == {
            'method': 'conjugation_restricted',
            'chemical_state': 'structure',
            'structure_indices': 0,
        }
        assert report['evaluated_atom_indices'].tolist() == list(range(len(before_ids)))
        classifications.append(report)
        return report

    def recorded_partition(molecular_system, **kwargs):
        report = provider(molecular_system, **kwargs)
        calls.append((kwargs, report))
        assert msm.get(molecular_system, element='system', n_atoms=True) == len(
            before_ids
        )
        return report

    monkeypatch.setattr(msm.topology, 'get_rigid_fragments', recorded_partition)
    monkeypatch.setattr(msm.topology, 'get_rotatable_bonds', recorded_classification)
    prepared = prepare_ligand(
        source, selection='all', active_torsion_bonds=case['active_bonds']
    )
    assert len(calls) == 1
    assert len(classifications) == 1
    decisions = prepared.metadata['torsion_selection']['selected_bonds']
    exceptions = [d for d in decisions if d['decision'] == 'explicit_override']
    assert len(exceptions) == (1 if case['case'] == '1s63_ligand' else 0)
    if exceptions:
        assert exceptions[0]['source_atom_indices'] == [26, 27]
        assert exceptions[0]['provider_exclusion_reasons'] == ['adjacent_triple_bond']
    kwargs, report = calls[0]
    assert kwargs['chemical_state'] == 'structure'
    assert kwargs['structure_indices'] == 0
    assert {frozenset(pair) for pair in report['bonded_atom_pairs']} == {
        frozenset(pair) for pair in case['active_bonds']
    }
    assert report['connectivity_completeness'] == 'complete'
    assert prepared.metadata['retained_atom_indices'] == case['retained_atom_indices']
    assert prepared.pdbqt_atom_indices == case['pdbqt_atom_indices']
    content = prepared.to_pdbqt().encode()
    assert hashlib.sha256(content).hexdigest() == case['generated_pdbqt_sha256']

    reference = _reference(case['case'], case['reference_pdbqt_sha256'])
    _, reference_atoms, _ = _atom_map(reference, molecule)
    _, generated_atoms, unmatched = _atom_map(content, molecule)
    assert unmatched == 0
    reference_bonds, reference_fragments = _source_graph(reference, reference_atoms)
    assert _source_graph(content, generated_atoms) == (
        reference_bonds,
        reference_fragments,
    )
    retained = set(case['retained_atom_indices'])
    packed, offsets = report['fragment_atom_indices'], report['fragment_offsets']
    assert {
        frozenset(int(atom) for atom in packed[start:stop] if int(atom) in retained)
        for start, stop in zip(offsets[:-1], offsets[1:])
    } == reference_fragments
    np.testing.assert_array_equal(
        puw.get_value(
            msm.get(source, element='atom', coordinates=True), to_unit='angstrom'
        ),
        before_coordinates,
    )
    np.testing.assert_array_equal(
        msm.get(source, element='bond', bonded_atom_pairs=True), before_pairs
    )
    assert list(msm.get(source, element='atom', atom_id=True)) == before_ids


@pytest.mark.parametrize(
    ('retained', 'cut', 'root', 'order', 'endpoints'),
    [
        ([5, 1, 0, 4, 3, 2], (1, 2), (0, 3, 4, 5), (0, 3, 4, 5, 1, 2), (5, 1)),
        ([5, 4, 3, 2, 1, 0], (2, 3), (0, 1, 2), (0, 1, 2, 3, 4, 5), (2, 3)),
    ],
)
def test_nonmonotonic_retained_axis_preserves_root_and_branch_endpoints(
    retained, cut, root, order, endpoints, monkeypatch
):
    source = _ligand('CCCCCC')
    provider = msm.topology.get_rigid_fragments

    def same_source(molecular_system, **kwargs):
        assert molecular_system is source  # Partitioning makes no molecular copy.
        return provider(molecular_system, **kwargs)

    monkeypatch.setattr(msm.topology, 'get_rigid_fragments', same_source)
    tree = build_torsion_tree(
        source, retained, [cut], msm.get(source, element='atom', atom_type=True)
    )
    assert tree.root_atoms == root
    assert tree.atom_order == order
    assert len(tree.branches) == 1
    branch = tree.branches[0]
    assert (branch.parent_atom, branch.child_atom) == endpoints
    assert set(branch.atoms) == set(range(6)) - set(root)


@pytest.mark.parametrize('completeness', ['partial', 'unavailable'])
def test_incomplete_chemical_graph_propagates_provider_rejection(completeness):
    source = _ligand('CCCCCC')
    # Native fixture construction follows the provider's graph-evidence tests.
    source.topology._chemical_states[0].connectivity_completeness = completeness
    with pytest.raises(StructuralInconsistencyError, match='complete'):
        build_torsion_tree(
            source,
            list(range(6)),
            [(1, 2)],
            msm.get(source, element='atom', atom_type=True),
        )


def test_partition_uses_structure_assigned_chemical_state():
    source = _ligand('CCCCCC')
    assigned = source.topology._append_chemical_state(state_id='assigned-complete')
    source.topology._set_chemical_state_bonds(
        source.topology.bonds.copy(), state_index=assigned
    )
    source.topology._chemical_states[assigned].connectivity_completeness = 'complete'
    source.topology._chemical_states[0].connectivity_completeness = 'partial'
    source._set_structure_chemical_state_indices([assigned])
    tree = build_torsion_tree(
        source,
        list(range(6)),
        [(1, 2)],
        msm.get(source, element='atom', atom_type=True),
    )
    assert tree.root_atoms == (2, 3, 4, 5)
    assert tree.atom_order == (2, 3, 4, 5, 1, 0)


@pytest.mark.parametrize(
    ('retained', 'cuts', 'reason'),
    [
        (list(range(6)), [(1, 2), (2, 1)], 'Duplicate'),
        (list(range(6)), [(0, 5)], 'not a source'),
        ([1, 2, 3, 4, 5], [(0, 1)], 'hydrogen projection'),
        ([0, 1, 4, 5], [(0, 1)], 'connected retained'),
    ],
)
def test_invalid_consumer_selection_is_rejected(retained, cuts, reason):
    source = _ligand('CCCCCC')
    with pytest.raises(ArgumentError, match=reason):
        build_torsion_tree(
            source, retained, cuts, msm.get(source, element='atom', atom_type=True)
        )
