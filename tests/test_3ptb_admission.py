"""Registered 3PTB admission preserves chemistry and frozen search inputs."""

import gzip
import itertools
import json

import numpy as np
import pytest
import pyunitwizard as puw
from vina import Vina

import dockingmt as dmt
from devtools.qualify_3ptb_admission import (
    DATA,
    DISULFIDES,
    OUTPUT,
    admit,
    registration,
    sha,
)


@pytest.fixture(scope='module')
def pdb(tmp_path_factory):
    directory = tmp_path_factory.mktemp('3ptb-source')
    path = directory / '3PTB.pdb'
    # Generic fixture archive restoration; molecular reading remains MolSysMT's.
    path.write_bytes(gzip.decompress((DATA / '3PTB.pdb.gz').read_bytes()))
    return path


@pytest.fixture(scope='module')
def admission(pdb):
    return admit(pdb)


def test_observed_atoms_disulfides_and_declared_histidines_survive(admission):
    *_, record = admission
    assert record['original_source_unchanged']
    assert record['original_plain_file_unchanged']
    assert record['input_altloc_inventory'] == [' ']
    assert record['receptor']['disulfide_author_pairs'] == [list(p) for p in DISULFIDES]
    states = record['receptor']['declared_group_states']
    assert [states[i] for i in (22, 39, 72)] == ['HIE', 'HID', 'HIE']
    assert states.count('CYX') == 12
    for role, n_observed, n_added in (('receptor', 1629, 1591), ('ligand', 9, 9)):
        expansion = record[role]['expansion']
        report = expansion['hydrogen_report']
        assert report['n_added_hydrogens'] == n_added
        assert report['dropped_attributes'] == ['b_factor', 'occupancy']
        assert (
            expansion['strict_policy_rejection']['exception']
            == 'StructuralInconsistencyError'
        )
        assert len(expansion['original_attributes']['occupancy'][0]) == n_observed
        before = record[role]['observed_snapshot']['structures']['coordinates']
        after = expansion['expanded_snapshot']['structures']['coordinates']
        mapping = np.asarray(report['atom_correspondence'])[:, 1]
        np.testing.assert_allclose(
            np.asarray(after)[:, mapping], before, rtol=0, atol=1e-12
        )


def test_named_projection_and_torsion_arms_keep_source_fields(admission):
    receptor, ligands, _, _, record = admission
    assert receptor.n_atoms == 2011
    assert receptor.metadata['source_n_atoms'] == 3220
    assert sum(receptor.charges) == pytest.approx(6, abs=1e-8)
    for arm, dof in (('rigid', 0), ('flexible', 1)):
        ligand = ligands[arm]
        evidence = record['prepared_inputs'][arm]
        assert ligand.n_atoms == 13 and ligand.torsion_dof == dof
        assert sum(ligand.charges) == pytest.approx(1, abs=1e-8)
        assert ligand.atom_types == ['A'] * 6 + ['C', 'N', 'N'] + ['HD'] * 4
        assert evidence['native_vina_parser_admitted']
        assert evidence['pdbqt_to_full_source_atom_indices'].count(None) == 4
        assert (
            sorted(
                i
                for i in evidence['pdbqt_to_full_source_atom_indices']
                if i is not None
            )
            == record['ligand_full_source_indices']
        )
        assert dmt.assess_preparation(ligand)['provisional_reason_codes'] == []
    np.testing.assert_array_equal(ligands['rigid'].charges, ligands['flexible'].charges)
    np.testing.assert_allclose(
        puw.get_value(ligands['rigid'].coordinates, to_unit='angstrom'),
        puw.get_value(ligands['flexible'].coordinates, to_unit='angstrom'),
        rtol=0,
        atol=1e-12,
    )
    assert ligands['flexible'].metadata['active_torsion_bonds'] == [[0, 6]]
    assert record['ligand']['rigid_fragments']['fragment_offsets'] == [0, 11, 18]
    assert 'BRANCH' not in ligands['rigid'].to_pdbqt()
    assert 'BRANCH' in ligands['flexible'].to_pdbqt()


def test_frozen_domains_and_population_precede_every_search(admission):
    *_, record = admission
    rows = record['population']
    assert len(rows) == 24
    assert [
        (
            r['arm'],
            r['domain'],
            r['protocol']['parameters']['seed'],
            r['protocol']['parameters']['exhaustiveness'],
        )
        for r in rows
    ] == list(
        itertools.product(
            ('rigid', 'flexible'), ('native', 'negative'), (7, 42, 2026), (1, 8)
        )
    )
    assert all(r['status'] == 'not_attempted' for r in rows)
    assert (
        record['docking_searches_executed'] == record['fixed_evaluations_executed'] == 0
    )
    for domain, expected in (('native', True), ('negative', False)):
        box = record['boxes'][domain]
        assert box['native_heavy_containment'] == [expected] * 9
        assert box['backend_projection']['size'] == [20, 20, 20]
        assert box['submitted'] is False
    np.testing.assert_allclose(
        np.subtract(
            record['boxes']['negative']['unrounded']['center'],
            record['boxes']['native']['unrounded']['center'],
        ),
        [60, 0, 0],
        rtol=0,
        atol=1e-12,
    )


def test_nondefault_units_reproduce_inputs_without_native_evaluation(
    pdb, admission, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail('Admission must not calculate maps, scores or docking poses')

    for name in ('compute_vina_maps', 'score', 'optimize', 'dock'):
        monkeypatch.setattr(Vina, name, forbidden)
    monkeypatch.setattr(dmt, 'score', forbidden)
    monkeypatch.setattr(dmt, 'dock', forbidden)
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'degrees']
    ):
        *_, other = admit(pdb)
    original = admission[-1]
    for role in ('receptor', 'rigid', 'flexible'):
        assert (
            original['prepared_inputs'][role]['pdbqt']
            == other['prepared_inputs'][role]['pdbqt']
        )
        np.testing.assert_allclose(
            original['prepared_inputs'][role]['coordinates'],
            other['prepared_inputs'][role]['coordinates'],
            rtol=0,
            atol=1e-10,
        )
    assert original['population'] == other['population']
    for domain in ('native', 'negative'):
        assert (
            original['boxes'][domain]['backend_projection']
            == other['boxes'][domain]['backend_projection']
        )
        for field in ('center', 'size'):
            np.testing.assert_allclose(
                original['boxes'][domain]['unrounded'][field],
                other['boxes'][domain]['unrounded'][field],
                rtol=0,
                atol=1e-10,
            )


def test_changed_source_is_rejected_before_molecular_reading(
    pdb, tmp_path, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('A changed original source must be rejected before conversion')

    monkeypatch.setattr(msm, 'convert', forbidden)
    changed = tmp_path / '3PTB.pdb'
    changed.write_bytes(pdb.read_bytes() + b'\n')
    with pytest.raises(ValueError, match='registered original'):
        admit(changed)


def test_saved_admission_retains_registration_and_original_producer():
    payload = OUTPUT.read_bytes()
    record = json.loads(gzip.decompress(payload))
    checkpoint = json.loads(OUTPUT.with_name('checkpoint_2026-10-10.json').read_text())
    assert sha(payload) == checkpoint['original_producer']['archive_sha256']
    assert (
        sha(gzip.decompress(payload)) == checkpoint['original_producer']['json_sha256']
    )
    producer = OUTPUT.with_name('producer_2026-10-10.py.txt')
    assert (
        sha(producer.read_bytes())
        == record['original_producer']['consumer_driver_sha256']
    )
    assert record['registration'] == registration()
    assert record['status'] == 'plain_input_admitted'
    assert record['direct_compressed_input_admitted'] is False
    assert len(record['population']) == 24
    assert record['docking_searches_executed'] == 0
