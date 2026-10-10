"""Exact captured axes, public rectangular distances and descriptive thresholds."""

import gzip
import json
from contextlib import nullcontext
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_contact import (
    OUTPUT,
    PAIR_CLASSES,
    PROTEIN_COUNT,
    SOURCE_AXIS,
    THRESHOLDS,
    analyze,
    captured,
    load_inputs,
    proximity,
    sha,
)

UNITS = ['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'degrees']


@pytest.fixture(scope='module')
def inputs():
    return load_inputs()[:3]


@pytest.mark.parametrize('policy', ['current', 'pm_fs_inferred'])
def test_public_cross_system_distances_use_captured_axis_without_scoring(
    inputs, monkeypatch, policy
):
    def forbidden(*args, **kwargs):
        raise AssertionError('Saved-input geometry must not invoke search or scoring.')

    monkeypatch.setattr(dmt, 'score', forbidden)
    monkeypatch.setattr(dmt, 'dock', forbidden)
    units = puw.context(standard_units=UNITS) if policy != 'current' else nullcontext()
    strings = (
        pd.option_context('future.infer_string', True)
        if policy != 'current'
        else nullcontext()
    )
    before = deepcopy(inputs)
    with units, strings:
        result = analyze(*inputs)
    assert inputs == before
    saved = json.loads(gzip.decompress(OUTPUT.read_bytes()))['ligands']
    for name, ligand in result.items():
        assert (
            ligand['root_order_exact_on_source_axis'] and ligand['protein_prefix_exact']
        )
        for arm, contexts in ligand['arms'].items():
            for context, entry in contexts.items():
                expected = saved[name]['arms'][arm][context]
                assert (
                    entry['canonical_ligand_atoms']
                    == expected['canonical_ligand_atoms']
                )
                assert entry['receptor_atoms'] == expected['receptor_atoms']
                assert (
                    entry['saved_scores_kcal_mol'] == expected['saved_scores_kcal_mol']
                )
                np.testing.assert_allclose(
                    entry['matrix_angstrom'],
                    expected['matrix_angstrom'],
                    rtol=0,
                    atol=1e-10,
                )
                for partition in ('protein', 'companion'):
                    for kind in ('all', *PAIR_CLASSES):
                        actual = entry['summary']['populations'][partition][kind]
                        original = expected['summary']['populations'][partition][kind]
                        assert actual['pairs'] == original['pairs']
                        assert (
                            actual['strict_threshold_counts']
                            == original['strict_threshold_counts']
                        )
        for context, rows in ligand['near_pair_contrasts'].items():
            expected = saved[name]['near_pair_contrasts'][context]
            assert len(rows) == len(expected)
            for actual, original in zip(rows, expected, strict=True):
                for key in actual:
                    if key.endswith('_angstrom'):
                        assert actual[key] == pytest.approx(original[key], abs=1e-10)
                    else:
                        assert actual[key] == original[key]


@pytest.mark.parametrize('drift', ['wrong_map', 'duplicate_source', 'wrong_receptor'])
def test_saved_admission_refuses_mapping_and_receptor_drift(inputs, drift):
    rigid, _, archives = inputs
    record = deepcopy(rigid['conformers']['p69']['fixed_scores']['native']['occupied'])
    expected = archives['p69']['cases']['p69']['controls']['native'][
        'pdbqt_to_source_atom_indices'
    ]
    receptor = archives['p69']['preparation']['receptors']['occupied']['pdbqt']
    if drift == 'wrong_map':
        expected = list(reversed(expected))
    elif drift == 'duplicate_source':
        record['metadata']['pdbqt_to_source_atom_indices'][0] = record['metadata'][
            'pdbqt_to_source_atom_indices'
        ][1]
    else:
        receptor += '\n'
    before = deepcopy(record)
    with pytest.raises(AssertionError):
        captured(record, expected, receptor)
    assert record == before


def test_occupied_prefix_drift_is_rejected_before_any_distance(inputs, monkeypatch):
    from devtools import qualify_5x72_contact as driver

    altered = deepcopy(inputs)
    text = altered[2]['p59']['preparation']['receptors']['occupied']['pdbqt']
    # Keep a valid atom field but drift the exact recorded serial.
    lines = text.splitlines(keepends=True)
    i = next(i for i, line in enumerate(lines) if line.startswith(('ATOM', 'HETATM')))
    lines[i] = lines[i][:6] + ' 9999' + lines[i][11:]
    altered[2]['p59']['preparation']['receptors']['occupied']['pdbqt'] = ''.join(lines)

    def forbidden(*args, **kwargs):
        raise RuntimeError('A drifted receptor must fail before geometry execution.')

    monkeypatch.setattr(driver, 'matrix', forbidden)
    with pytest.raises(AssertionError):
        driver.analyze(*altered)


def test_proximity_thresholds_are_strict_and_empty_populations_stay_empty():
    result = proximity([1.49, 1.5, 1.99, 2, 2.49, 2.5, 2.99, 3, 3.99, 4, 4.99, 5])
    assert result['strict_threshold_counts'] == [1, 3, 5, 7, 9, 11]
    assert result['pairs'] == 12 and result['minimum_angstrom'] == 1.49
    assert proximity([]) == {
        'pairs': 0,
        'minimum_angstrom': None,
        'strict_threshold_counts': [0] * 6,
    }


def test_saved_all_distances_original_captures_and_proximity_populations_are_complete():
    payload = OUTPUT.read_bytes()
    record = json.loads(gzip.decompress(payload))
    checkpoint = json.loads(OUTPUT.with_name('checkpoint_2026-10-09.json').read_text())
    assert sha(payload) == checkpoint['producer_archive']['gzip_sha256']
    assert (
        sha(gzip.decompress(payload)) == checkpoint['producer_archive']['json_sha256']
    )
    assert (
        sha(OUTPUT.with_name('producer_2026-10-09.py').read_bytes())
        == record['consumer_source_sha256']['devtools/qualify_5x72_contact.py']
    )
    assert record['new_searches'] == record['new_fixed_evaluations'] == 0
    assert record['strict_thresholds_angstrom'] == list(THRESHOLDS)
    entries = matrices = 0
    for ligand in record['ligands'].values():
        for arm in ligand['arms'].values():
            for context, entry in arm.items():
                values = np.asarray(entry['matrix_angstrom'])
                assert values.shape == (
                    25,
                    PROTEIN_COUNT + (25 if context == 'occupied' else 0),
                )
                assert [
                    a['source_atom_index'] for a in entry['canonical_ligand_atoms']
                ] == SOURCE_AXIS
                left = np.asarray(
                    [a['coordinates'] for a in entry['canonical_ligand_atoms']]
                )
                right = np.asarray([a['coordinates'] for a in entry['receptor_atoms']])
                np.testing.assert_allclose(
                    values,
                    np.linalg.norm(left[:, None] - right[None, :], axis=2),
                    rtol=0,
                    atol=1e-10,
                )
                for artifacts in entry['root_input_identities'].values():
                    assert dmt.verify_captured_inputs(artifacts)
                assert (
                    sum(
                        g['all']['pairs']
                        for g in entry['summary']['per_receptor_group']
                    )
                    == values.size
                )
                assert (
                    sum(
                        p['all']['pairs']
                        for p in entry['summary']['populations'].values()
                    )
                    == values.size
                )
                entries += values.size
                matrices += 1
        for arm in ligand['arms'].values():
            np.testing.assert_allclose(
                np.asarray(arm['occupied']['matrix_angstrom'])[:, :PROTEIN_COUNT],
                arm['sham']['matrix_angstrom'],
                rtol=0,
                atol=1e-10,
            )
    assert entries == record['distance_entries'] == 298700
    assert matrices == record['distance_matrices'] == 8
