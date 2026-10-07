"""Real paired ligand preparation and independent mapped geometry controls."""

import gzip
import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.audit_1iep_preparation import _compare_pdbqt, _compare_torsion_graphs
from devtools.qualify_1iep_flexibility import CUTS, OUTPUT, prepare_case, redock


@pytest.fixture(scope='module')
def prepared_case():
    return prepare_case()


def test_only_selected_torsions_change_between_real_preparations(prepared_case):
    source, preparations, audit = prepared_case
    rigid, flexible = preparations.values()
    assert rigid.torsion_dof == 0
    assert flexible.torsion_dof == 7
    assert flexible.metadata['active_torsion_bonds'] == [list(pair) for pair in CUTS]
    assert all(
        bond['decision'] == 'provider_candidate'
        for bond in flexible.metadata['torsion_selection']['selected_bonds']
    )
    assert rigid.atom_types == flexible.atom_types
    assert rigid.charges == flexible.charges
    assert rigid.metadata['retained_atom_indices'] == list(range(37)) + [43, 47, 58]
    assert audit['source_unchanged']
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[0]
    for ligand in preparations.values():
        np.testing.assert_allclose(
            puw.get_value(ligand.coordinates, to_unit='angstrom'),
            xyz[ligand.metadata['retained_atom_indices']],
            rtol=0,
            atol=1e-12,
        )
        assert ligand.atom_types.count('HD') == 3
        charge = dmt.audit_preparation_charges(ligand)
        assert charge['total_charge'] == pytest.approx(1, abs=1e-10)
        assert len(charge['charge_projection']['transfers']) == 29
        assert charge['pdbqt']['total_charge'] == pytest.approx(0.999, abs=1e-10)
        assert dmt.assess_preparation(ligand)['assessment'] == 'unassessed'


def test_paired_preparation_preserves_nondefault_unit_policy(prepared_case):
    _, preparations, audit = prepared_case
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        _, other, observed = prepare_case()
    assert audit['decisions'] == observed['decisions']
    for name in preparations:
        first, second = preparations[name], other[name]
        np.testing.assert_allclose(
            puw.get_value(first.coordinates, to_unit='angstrom'),
            puw.get_value(second.coordinates, to_unit='angstrom'),
            rtol=0,
            atol=1e-12,
        )
        np.testing.assert_allclose(first.charges, second.charges, rtol=0, atol=1e-12)
        assert first.atom_types == second.atom_types
        assert first.pdbqt_atom_indices == second.pdbqt_atom_indices
        assert (
            first.metadata['retained_atom_indices']
            == second.metadata['retained_atom_indices']
        )

        # This original SDF includes half-millangstrom coordinates. Conversion
        # roundoff can choose either neighboring three-decimal text value.
        def written_xyz(ligand):
            return np.asarray(
                [
                    [float(line[start : start + 8]) for start in (30, 38, 46)]
                    for line in ligand.to_pdbqt().splitlines()
                    if line.startswith('ATOM')
                ]
            )

        np.testing.assert_allclose(
            written_xyz(first), written_xyz(second), rtol=0, atol=0.001000000001
        )


def assert_independent_geometry(run, source_xyz):
    """Every written-order pose uses the explicit original-source axis."""
    restored = dmt.DockingResult.from_dict(run['result'])
    source_indices = run['pdbqt_to_source_atom_indices']
    heavy = run['heavy_pdbqt_indices']
    assert len(set(source_indices)) == 40
    assert sorted(source_indices[index] for index in heavy) == list(range(37))
    report = run['evaluation']
    assert report['criterion']['atom_correspondence'] == 'verified_source_atom_keys'
    assert report['criterion']['alignment'] == 'none'
    assert report['criterion']['symmetry_correction'] == 'none'
    for pose, row, heavy_row in zip(
        restored.poses, report['poses'], run['heavy_atom_metrics'], strict=True
    ):
        xyz = puw.get_value(pose.coordinates, to_unit='angstrom')
        squared = np.sum((xyz - source_xyz[source_indices]) ** 2, axis=1)
        assert row['rmsd'] == pytest.approx(np.sqrt(squared.mean()), abs=1e-10)
        assert row['recovered'] is (row['rmsd'] <= 2.5)
        assert heavy_row['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
            np.sqrt(squared[heavy].mean()), abs=1e-10
        )
        assert heavy_row['vina_score_kcal_per_mol'] == pose.scores['vina']
        assert all(
            int(key['atom_id']) == index
            for key, index in zip(row['atom_keys'], source_indices, strict=True)
        )


@pytest.mark.parametrize('variant', ['rigid', 'flexible'])
def test_default_vina_pairs_keep_maps_and_actual_geometry(prepared_case, variant):
    source, preparations, audit = prepared_case
    run = redock(
        source,
        preparations[variant],
        audit['decisions'],
        variant=variant,
        seed=42,
        exhaustiveness=1,
    )
    assert (
        run['result']['protocol_info']['parameters']['allow_provisional_preparation']
        is False
    )
    assert (
        run['result']['provenance']['preparation']['partner']['assessment']
        == 'unassessed'
    )
    assert dmt.verify_captured_inputs(run['result']['provenance']['backend_artifacts'])
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[0]
    assert_independent_geometry(run, xyz)


def test_retained_paired_matrix_keeps_original_geometry_and_input_bytes():
    record = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    checkpoint = json.loads(OUTPUT.with_name('checkpoint_2026-10-07.json').read_text())
    reference_path = OUTPUT.parents[4] / 'tests/data/vina_torsions/1iep_ligand.pdbqt'
    native = record['audit']['preparations']['flexible']['pdbqt'].encode()
    reference = reference_path.read_bytes()
    comparison = _compare_pdbqt(native, reference)
    assert comparison == checkpoint['reference_comparison']['atom_comparison']
    assert comparison['coordinate_matched_atoms'] == 40
    assert comparison['matched_atom_type_disagreements'] == 0
    assert comparison['matched_charge_max_absolute_difference_e'] == 0
    tree = _compare_torsion_graphs(native, reference)
    assert tree == checkpoint['reference_comparison']['torsion_graph_comparison']
    assert tree['branch_bonds_match'] and tree['rigid_fragments_match']
    runs = record['redocking_runs']
    assert len(runs) == 12
    cells = {
        (
            run['variant'],
            run['result']['protocol_info']['parameters']['seed'],
            run['result']['protocol_info']['parameters']['exhaustiveness'],
        )
        for run in runs
    }
    assert cells == {
        (variant, seed, effort)
        for variant in ('rigid', 'flexible')
        for seed in (7, 42, 2026)
        for effort in (1, 8)
    }
    xyz = np.asarray(record['audit']['source_snapshot']['structures']['coordinates'])[0]
    source_xyz = puw.get_value(puw.quantity(xyz, 'nm'), to_unit='angstrom')
    for run in runs:
        artifacts = run['result']['provenance']['backend_artifacts']
        assert dmt.verify_captured_inputs(artifacts)
        assert (
            artifacts['receptor']['sha256']
            == record['input_sha256']['1iep_receptor.pdbqt']
        )
        assert (
            artifacts['partner']['sha256']
            == record['audit']['preparations'][run['variant']]['pdbqt_sha256']
        )
        assert_independent_geometry(run, source_xyz)
