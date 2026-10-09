"""Experimental identity and saved/live heavy-atom 5X72 boundary guards."""

import base64
import gzip
import itertools
import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_root_order import (
    DATA,
    INPUTS,
    NAMES,
    OUTPUT,
    comparison_rows,
    measure,
    observe,
    prepare_cases,
    reference_box,
    sha,
    xyz,
)


@pytest.fixture(scope='module')
def cases():
    return prepare_cases()


def assert_metrics(run, case):
    """Recompute the declared crystal correspondence without fitting any pose."""
    control = case['controls'][run['order']]
    result = dmt.DockingResult.from_dict(run['result'])
    artifacts = result.provenance['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    assert artifacts['partner']['sha256'] == control['sha256']
    assert (
        base64.b64decode(artifacts['partner']['content_base64'])
        == control['pdbqt'].encode()
    )
    assert artifacts['receptor']['sha256'] == INPUTS['5x72_receptor.pdbqt']
    assert (
        base64.b64decode(artifacts['receptor']['content_base64'])
        == (DATA / '5x72_receptor.pdbqt').read_bytes()
    )
    heavy = control['heavy_pdbqt_indices']
    mapping = control['heavy_pdbqt_to_reference_atom_indices']
    assert len(heavy) == 24 and sorted(mapping) == list(range(24))
    assert mapping == [control['pdbqt_to_source_atom_indices'][i] for i in heavy]
    expected = np.array(case['reference_coordinates_angstrom'])[mapping]
    measured = measure(result, case, control)
    for pose, saved, actual in zip(
        result.poses, run['heavy_atom_metrics'], measured, strict=True
    ):
        assert pose.n_atoms == 25
        assert pose.metadata['pose_atom_order'] == 'verified_pdbqt_order'
        coordinates = puw.get_value(pose.coordinates, to_unit='angstrom')[heavy]
        independent = np.sqrt(np.mean(np.sum((coordinates - expected) ** 2, axis=-1)))
        assert saved['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
            independent, abs=1e-10
        )
        assert actual['heavy_atom_positional_rmsd_angstrom'] == pytest.approx(
            independent, abs=1e-10
        )
        assert saved['recovered'] is bool(independent <= 2.5)
        assert saved['vina_score_kcal_mol'] == pose.scores['vina']
    return result


def test_crystal_references_and_fixed_first_orders_under_pm_fs(cases):
    sources, default = cases
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        alternate_sources, alternate = prepare_cases()
        box = reference_box()
        np.testing.assert_allclose(
            puw.get_value(box.center, to_unit='angstrom'), [-15, 15, 129]
        )
        np.testing.assert_allclose(
            puw.get_value(box.size, to_unit='angstrom'), [30, 24, 24]
        )
    assert default['p59']['reference_stereochemistry'] == 'R'
    assert default['p69']['reference_stereochemistry'] == 'S'
    for name in ('p59', 'p69'):
        case, other = default[name], alternate[name]
        np.testing.assert_allclose(
            xyz(sources[name]), xyz(alternate_sources[name]), rtol=0, atol=1e-12
        )
        np.testing.assert_allclose(
            case['reference_coordinates_angstrom'],
            other['reference_coordinates_angstrom'],
            rtol=0,
            atol=1e-12,
        )
        assert case['reference_pdb_atom_names_in_source_order'] == NAMES
        assert case['source_to_reference_heavy_atom_indices'] == list(range(24))
        assert case['charge_audit']['assessment'] == 'consistent'
        assert case['preparation_assessment']['assessment'] == 'unassessed'
        assert (
            np.linalg.norm(
                np.mean(xyz(sources[name])[:24], axis=0)
                - np.mean(case['reference_coordinates_angstrom'], axis=0)
            )
            > 100
        )
        native = case['controls']['native']['pdbqt'].splitlines(keepends=True)
        fixed = case['controls']['first_fixed']['pdbqt'].splitlines(keepends=True)
        first, last = native.index('ROOT\n') + 1, native.index('ENDROOT\n')
        assert last - first == 12
        assert (
            fixed
            == native[: first + 1] + native[first + 1 : last][::-1] + native[last:]
        )
        for order, control in case['controls'].items():
            new = other['controls'][order]
            assert control['first_root_source_atom_index'] == 7
            assert (
                control['pdbqt_to_source_atom_indices']
                == new['pdbqt_to_source_atom_indices']
            )
            old_lines, new_lines = (
                control['pdbqt'].splitlines(),
                new['pdbqt'].splitlines(),
            )
            for a, b in zip(old_lines, new_lines, strict=True):
                if a.startswith('ATOM'):
                    assert a[:30] + a[54:] == b[:30] + b[54:]
                    np.testing.assert_allclose(
                        [float(a[i : i + 8]) for i in (30, 38, 46)],
                        [float(b[i : i + 8]) for i in (30, 38, 46)],
                        rtol=0,
                        atol=0.001001,
                    )
                else:
                    assert a == b
        assert (
            case['controls']['native']['rigid_body_origin_angstrom']
            == case['controls']['first_fixed']['rigid_body_origin_angstrom']
        )


@pytest.mark.parametrize('name', ['p59', 'p69'])
def test_live_single_ligand_evaluation_uses_its_experimental_reference(cases, name):
    sources, prepared = cases
    run = observe(
        sources[name],
        prepared[name],
        name=name,
        order='native',
        seed=42,
        exhaustiveness=1,
    )
    result = assert_metrics(run, prepared[name])
    assert result.protocol_info['parameters']['cpu'] == 1
    assert result.provenance['preparation']['receptor']['assessment'] == 'unassessed'
    assert result.provenance['preparation']['partner']['assessment'] == 'unassessed'
    # Search recovery is an observation; no portable stochastic success promise.


def test_all_24_saved_cells_against_correct_crystal_reference_under_pm_fs():
    record = json.loads(gzip.decompress(OUTPUT.read_bytes()))
    assert record['criterion'] == {
        'metric': 'positional_rmsd',
        'atom_population': '24_experimental_heavy_atoms',
        'cutoff_angstrom': 2.5,
        'alignment': False,
        'symmetry_correction': False,
    }
    assert record['input_sha256'] == INPUTS
    for name, expected in INPUTS.items():
        assert sha((DATA / name).read_bytes()) == expected
    cells = set()
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'radians']
    ):
        for run in record['new_runs']:
            result = assert_metrics(run, record['cases'][run['ligand']])
            parameters = result.protocol_info['parameters']
            cells.add(
                (
                    run['ligand'],
                    run['order'],
                    parameters['seed'],
                    parameters['exhaustiveness'],
                )
            )
            assert parameters['cpu'] == 1 and parameters['n_poses'] == 5
    assert len(record['new_runs']) == 24
    assert cells == set(
        itertools.product(
            ('p59', 'p69'), ('native', 'first_fixed'), (7, 42, 2026), (1, 8)
        )
    )
    assert comparison_rows(record['new_runs']) == record['comparison_rows']


def test_runtime_version_remarks_do_not_require_historical_metadata(cases, monkeypatch):
    monkeypatch.setattr(msm, '__version__', '1.0.0')
    _, current = prepare_cases()
    for name, case in current.items():
        control = case['controls']['native']
        assert '"molsysmt":"1.0.0"' in control['pdbqt']
        assert (
            control['pdbqt_to_source_atom_indices']
            == cases[1][name]['controls']['native']['pdbqt_to_source_atom_indices']
        )
        assert (
            case['reference_coordinates_angstrom']
            == cases[1][name]['reference_coordinates_angstrom']
        )
