"""Explicit docking choices preserve public chemical criteria and source axes."""

import builtins
import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_REC_PDBQT

import dockingmt as dmt
from devtools.qualify_chemical_templates import load_5x72, snapshot
from devtools.qualify_named_types import (
    CHARGE,
    TYPING,
    declared_source,
    explicit_source,
)
from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._temporary_torsions import build_torsion_tree


def typed_source(smiles):
    return msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source(smiles), **CHARGE), **TYPING
    )


@pytest.mark.parametrize(
    'smiles,bond,reasons',
    [
        ('CCCCCC', (1, 2), []),
        ('CC(=O)OCC', (3, 4), []),
        ('CC(=O)OCC', (1, 3), ['restricted_conjugation']),
        ('CC(=O)SCC', (1, 3), ['restricted_conjugation']),
        ('c1ccccc1C#N', (5, 6), ['adjacent_triple_bond']),
        ('CCC#CCC', (1, 2), ['adjacent_triple_bond']),
        ('CCC#CCC', (3, 4), ['adjacent_triple_bond']),
        ('CNCC', (1, 2), []),
    ],
)
def test_independent_explicit_cut_decisions_and_unchanged_source(smiles, bond, reasons):
    source = typed_source(smiles)
    before = snapshot(source)
    requested = [bond]
    prepared = dmt.prepare_ligand(
        source, selection='all', active_torsion_bonds=requested
    )
    report = prepared.metadata['torsion_selection']
    assert report['policy'] == 'explicit_docking_cuts@1'
    assert report['selection'] == 'caller_supplied_bonds'
    assert prepared.torsion_dof == 1
    assert requested == [bond]
    assert snapshot(source) == before
    decision = report['selected_bonds'][0]
    assert decision['source_atom_indices'] == list(bond)
    assert decision['provider_exclusion_reasons'] == reasons
    assert decision['decision'] == (
        'explicit_override' if reasons else 'provider_candidate'
    )
    provider = report['provider_classification']
    assert provider['schema'] == 'molsysmt.rotatable_bonds@1'
    assert provider['rule_version'] == 'conjugation_restricted@1'
    assert provider['chemical_state_index'] == 0
    assert provider['evaluated_atom_indices'] == list(
        range(msm.get(source, n_atoms=True))
    )
    assert provider['software']['molsysmt']
    assert provider['attribution']['items']
    assert report['pdbqt_to_source_atom_indices'] == [
        prepared.metadata['retained_atom_indices'][i]
        for i in prepared.pdbqt_atom_indices
    ]
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    if reasons:
        row = provider['bond_indices'].index(decision['source_bond_index'])
        assert provider['is_rotatable'][row] is False
        assert provider['exclusion_mask'][row] != 0


@pytest.mark.parametrize(
    'smiles,bond',
    [
        ('CC(=O)NCC', (1, 3)),
        ('CC(=S)NCC', (1, 3)),
        ('CC(=N)NCC', (1, 3)),
        ('CC(=O)N(C)CC', (1, 3)),
        ('O=CNCC', (1, 2)),
    ],
)
def test_restricted_c_n_remains_rejected_including_amidine_and_tertiary_amide(
    smiles, bond
):
    source = declared_source(smiles)
    with pytest.raises(ArgumentError, match='restricted C-N'):
        build_torsion_tree(
            source,
            list(range(msm.get(source, n_atoms=True))),
            [bond],
            msm.get(source, element='atom', atom_type=True),
        )


@pytest.mark.parametrize('bonds', [None, []])
def test_rigid_default_does_not_classify_or_invent_active_cuts(bonds, monkeypatch):
    source = typed_source('CC(=O)OCC')

    def forbidden(*args, **kwargs):
        raise AssertionError('Rigid preparation must not calculate a torsion policy.')

    monkeypatch.setattr(msm.topology, 'get_rotatable_bonds', forbidden)
    monkeypatch.setattr(msm.topology, 'get_rigid_fragments', forbidden)
    prepared = dmt.prepare_ligand(source, selection='all', active_torsion_bonds=bonds)
    assert prepared.torsion_dof == 0
    assert 'torsion_selection' not in prepared.metadata
    assert prepared.metadata['active_torsion_bonds'] == []


def test_one_public_native_classification_on_complete_graph_without_optional_typing(
    monkeypatch,
):
    source = explicit_source('CC(=O)OCC')
    calls = []
    actual = msm.topology.get_rotatable_bonds
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split('.')[0] in ('rdkit', 'meeko'):
            raise AssertionError(
                'Native torsion classification imported an optional chemical engine.'
            )
        return original_import(name, *args, **kwargs)

    def observed(system, **options):
        assert system is source
        assert options == {
            'method': 'conjugation_restricted',
            'chemical_state': 'structure',
            'structure_indices': 0,
        }
        report = actual(system, **options)
        calls.append(report)
        return report

    monkeypatch.setattr(builtins, '__import__', guarded_import)
    monkeypatch.setattr(msm.topology, 'get_rotatable_bonds', observed)
    tree = build_torsion_tree(
        source,
        list(range(6)),
        [(1, 3)],
        ['C', 'C', 'O', 'O', 'C', 'C'] + ['H'] * (msm.get(source, n_atoms=True) - 6),
    )
    assert len(calls) == 1
    original = calls[0]
    saved = tree.selection_report['provider_classification']
    assert len(saved['evaluated_atom_indices']) > 6
    original['exclusion_mask'][:] = 0
    original['software']['molsysmt'] = 'changed'
    assert saved['software']['molsysmt'] != 'changed'
    assert any(saved['exclusion_mask'])


@pytest.mark.parametrize(
    'error_class', [msm.StructuralInconsistencyError, RuntimeError]
)
def test_provider_failure_propagates_unchanged_without_fallback(
    error_class, monkeypatch
):
    source = typed_source('CCCCCC')
    error = (
        error_class(reason='missing complete chemistry')
        if error_class is msm.StructuralInconsistencyError
        else error_class('provider failed')
    )

    def fail(*args, **kwargs):
        raise error

    def forbidden(*args, **kwargs):
        raise AssertionError(
            'A provider failure must not trigger partitioning or a fallback.'
        )

    monkeypatch.setattr(msm.topology, 'get_rotatable_bonds', fail)
    monkeypatch.setattr(msm.topology, 'get_rigid_fragments', forbidden)
    with pytest.raises(error_class) as caught:
        dmt.prepare_ligand(source, selection='all', active_torsion_bonds=[(1, 2)])
    assert caught.value is error


def test_unknown_provider_exclusion_is_not_silently_allowed(monkeypatch):
    source = typed_source('CCCCCC')
    actual = msm.topology.get_rotatable_bonds

    def future_reason(system, **options):
        report = actual(system, **options)
        report['exclusion_bits']['future_exclusion'] = 64
        row = next(
            i
            for i, pair in enumerate(report['bonded_atom_pairs'])
            if set(pair) == {1, 2}
        )
        report['exclusion_mask'][row] |= np.uint8(64)
        report['is_rotatable'][row] = False
        return report

    monkeypatch.setattr(msm.topology, 'get_rotatable_bonds', future_reason)
    with pytest.raises(ArgumentError, match='unsupported provider exclusions'):
        dmt.prepare_ligand(source, selection='all', active_torsion_bonds=[(1, 2)])


def test_source_bond_positions_follow_reordered_provider_axis():
    source = declared_source('CCCCCC')
    original_id = msm.get(source, element='bond', bond_id=True)[1]
    state = source.chemical_states._states[0]
    state.bonds = state.bonds.iloc[::-1].reset_index(drop=True)
    before = snapshot(source)
    tree = build_torsion_tree(source, list(range(6)), [(1, 2)], ['C'] * 6)
    decision = tree.selection_report['selected_bonds'][0]
    assert decision['source_atom_indices'] == [1, 2]
    assert decision['source_bond_index'] == 3
    assert decision['source_bond_id'] == original_id
    assert list(tree.atom_order) == [2, 3, 4, 5, 1, 0]
    assert snapshot(source) == before


def test_classification_uses_assigned_state_instead_of_reference_chemistry():
    source = declared_source('CCCCCC')
    assigned = source.topology._append_chemical_state(state_id='assigned-double')
    bonds = source.topology.bonds.copy()
    bonds.loc[1, 'bond_order'] = 2.0
    source.topology._set_chemical_state_bonds(bonds, state_index=assigned)
    source.topology._chemical_states[assigned].connectivity_completeness = 'complete'
    source._set_structure_chemical_state_indices([assigned])
    with pytest.raises(ArgumentError, match='single bond order'):
        build_torsion_tree(source, list(range(6)), [(1, 2)], ['C'] * 6)


@pytest.mark.parametrize('defect', ['partial', 'order', 'aromatic_bridge'])
def test_full_graph_evidence_is_required_even_outside_requested_pair(defect):
    source = declared_source('CCCCCC')
    state = source.topology._chemical_states[0]
    if defect == 'partial':
        state.connectivity_completeness = 'partial'
    elif defect == 'order':
        state.bonds.loc[4, 'bond_order'] = float('nan')
    else:
        state.bonds.loc[4, 'is_aromatic'] = True
    with pytest.raises(msm.StructuralInconsistencyError):
        build_torsion_tree(source, list(range(6)), [(1, 2)], ['C'] * 6)


def test_default_automatic_vina_retains_named_torsion_reports_and_pose_identity():
    _, source = load_5x72('p59')
    charged = msm.build.assign_partial_charges(source, **CHARGE)
    typed = msm.build.assign_autodock_atom_types(charged, **TYPING)
    before = snapshot(typed)
    bonds = [(6, 7), (17, 18)]
    prepared = dmt.prepare_ligand(typed, selection='all', active_torsion_bonds=bonds)
    coordinates = puw.get_value(msm.get(typed, coordinates=True), to_unit='angstrom')[0]
    with puw.context(standard_units=['pm', 'fs']):
        problem = dmt.DockingProblem(
            receptor=MINIMAL_REC_PDBQT,
            partner=typed,
            search_domain=dmt.BoxRegion(
                puw.quantity(coordinates.mean(axis=0), 'angstrom'),
                puw.quantity([20, 20, 20], 'angstrom'),
            ),
        )
        result = dmt.dock(
            problem,
            dmt.VinaProtocol(
                cpu=1,
                seed=17,
                exhaustiveness=1,
                n_poses=1,
                active_torsion_bonds=bonds,
                capture_backend_inputs=True,
            ),
        )
        restored = dmt.DockingResult.from_dict(
            json.loads(json.dumps(result.to_dict(), allow_nan=False))
        )
        assert len(restored.poses) == 1
        metadata = restored.provenance['preparation']['partner']['metadata']
        assert metadata['torsion_selection'] == prepared.metadata['torsion_selection']
        assert (
            restored.provenance['preparation']['partner']['assessment'] == 'unassessed'
        )
        assert dmt.verify_captured_inputs(restored.provenance['backend_artifacts'])
        pose = restored.poses[0]
        recovered = pose.to_molecular_system(typed)
        recovered_xyz = puw.get_value(
            msm.get(recovered, coordinates=True), to_unit='angstrom'
        )[0]
        observed = puw.get_value(pose.coordinates, to_unit='angstrom')
        recovered_ids = [
            str(i) for i in msm.get(recovered, element='atom', atom_id=True)
        ]
        assert len(set(recovered_ids)) == pose.n_atoms
        lookup = {atom_id: i for i, atom_id in enumerate(recovered_ids)}
        keys = pose.metadata['source_atom_keys']
        source_ids = msm.get(typed, element='atom', atom_id=True)
        assert [key['atom_id'] for key in keys] == [
            str(source_ids[i]) for i in pose.metadata['selected_atom_indices']
        ]
        np.testing.assert_allclose(
            recovered_xyz[[lookup[key['atom_id']] for key in keys]],
            observed,
            rtol=0,
            atol=1e-3,
        )
    assert snapshot(typed) == before
