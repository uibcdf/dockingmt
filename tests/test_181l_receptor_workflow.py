"""Real protein/ligand composition protects observed geometry and provenance."""

import json

import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_181l_receptor import prepare_case, redock


@pytest.fixture(scope='module')
def prepared_case():
    return prepare_case()


@pytest.fixture(scope='module')
def saved_run(prepared_case):
    receptor, ligand, reference, audit = prepared_case
    return redock(
        receptor, ligand, reference, audit['decisions'], seed=42, exhaustiveness=1
    )


def test_real_receptor_retains_observed_identity_and_geometry(prepared_case):
    receptor, ligand, _, audit = prepared_case
    mapping = audit['decisions']['source_to_repaired_atom_indices']
    before = audit['original_receptor_snapshot']
    after = audit['expanded_receptor_snapshot']
    assert len(mapping) == 1289
    assert len(set(mapping)) == 1289
    np.testing.assert_allclose(
        np.asarray(after['structures']['coordinates'])[:, mapping],
        before['structures']['coordinates'],
        rtol=0,
        atol=1e-12,
    )
    assert audit['original_source_unchanged']
    assert audit['decisions']['repaired_to_full_source_atom_indices'].count(None) == 1
    assert audit['hydrogen_report']['n_added_hydrogens'] == 1313
    assert receptor.metadata['source_n_atoms'] == 2603
    assert ligand.n_atoms == 6
    assert ligand.atom_types == ['A'] * 6
    assert audit['decisions']['histidine_group_indices'] == [30]
    assert audit['decisions']['declared_residue_states'][30] == 'HIE'
    assert audit['decisions']['pH'] is None


def test_real_protein_projection_conserves_declared_charge(prepared_case):
    receptor, ligand, _, audit = prepared_case
    charge = audit['receptor_charge_audit']
    assert charge['assessment'] == 'consistent'
    assert charge['total_charge'] == pytest.approx(8, abs=1e-8)
    assert sum(receptor.charges) == pytest.approx(8, abs=1e-8)
    assert audit['ligand_charge_audit']['total_charge'] == pytest.approx(0, abs=1e-8)
    assert receptor.metadata['atom_type_assignment']['coverage'] == 'complete'
    assert receptor.metadata['atom_type_assignment']['n_atoms'] == 2603
    assert 'HD' in receptor.atom_types
    for prepared in (receptor, ligand):
        assert dmt.assess_preparation(prepared)['assessment'] == 'unassessed'
        assert dmt.assess_preparation(prepared)['provisional_reason_codes'] == []


def test_real_workflow_is_independent_of_session_length_units(prepared_case):
    receptor, ligand, reference, audit = prepared_case
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        other_receptor, other_ligand, other_reference, other = prepare_case()
    for first, second in ((receptor, other_receptor), (ligand, other_ligand)):
        np.testing.assert_allclose(
            puw.get_value(first.coordinates, to_unit='nm'),
            puw.get_value(second.coordinates, to_unit='nm'),
            rtol=0,
            atol=1e-12,
        )
        assert first.to_pdbqt() == second.to_pdbqt()
    assert audit['decisions'] == other['decisions']
    assert reference is not other_reference


def test_default_real_vina_retains_declared_choices_and_submitted_bytes(saved_run):
    restored = dmt.DockingResult.from_dict(json.loads(json.dumps(saved_run['result'])))
    assert len(restored) > 0
    assert (
        restored.protocol_info['parameters']['allow_provisional_preparation'] is False
    )
    assert dmt.verify_captured_inputs(restored.provenance['backend_artifacts'])
    assert restored.problem_info['metadata']['preparation_decisions'][
        'water_policy'
    ] == ('exclude_all_observed_waters')
    for role in ('receptor', 'partner'):
        assert restored.provenance['preparation'][role]['assessment'] == 'unassessed'
    assert all(pose.n_atoms == 6 for pose in restored)
    assert (
        saved_run['evaluation']['criterion']['atom_correspondence']
        == 'verified_source_atom_keys'
    )


def test_saved_real_result_re_evaluates_with_original_atom_identity(
    saved_run, prepared_case
):
    _, _, reference, _ = prepared_case
    restored = dmt.DockingResult.from_dict(json.loads(json.dumps(saved_run['result'])))
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        report = dmt.evaluate_redocking(
            restored, reference, rmsd_cutoff=puw.quantity(250, 'pm')
        )
    assert report['criterion'] == saved_run['evaluation']['criterion']
    for actual, expected in zip(report['poses'], saved_run['evaluation']['poses']):
        np.testing.assert_allclose(actual['rmsd'], expected['rmsd'], rtol=0, atol=1e-12)
        assert {k: v for k, v in actual.items() if k != 'rmsd'} == {
            k: v for k, v in expected.items() if k != 'rmsd'
        }
    assert report['criterion']['symmetry_correction'] == 'none'
    assert report['criterion']['alignment'] == 'none'
