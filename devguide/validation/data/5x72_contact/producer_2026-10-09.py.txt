"""Finite distance contrasts of authenticated 5X72 scoring inputs.

MolSysMT owns PDBQT projection and cross-system distances. Fixture-specific
reducers describe proximity without assigning contacts an energy or cause.
No molecular preparation, new scoring or search is performed.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_occupancy import atom_fields
from devtools.qualify_5x72_reference import (
    ROOT,
    detached_record,
    load_archives,
    score_components,
    sha,
    snapshot,
    xyz,
)
from devtools.qualify_5x72_rigid import OUTPUT as RIGID
from devtools.qualify_5x72_rigid import load_reference
from devtools.qualify_5x72_rigid import proof as rigid_proof
from devtools.qualify_181l_receptor import save

OUTPUT = ROOT / 'devguide/validation/data/5x72_contact/audit_2026-10-09.json.gz'
RIGID_SHA = 'f0e91b99793bc61403aedf660016f532e1a46c5815f92441f511dbac8ffb4179'
PLAN = 'https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6094190056'
THRESHOLDS = (1.5, 2.0, 2.5, 3.0, 4.0, 5.0)
SOURCE_AXIS = [*range(24), 29]
PROTEIN_COUNT = 1481
H_TYPES = {'H', 'HD', 'HS'}
PAIR_CLASSES = (
    'heavy_heavy',
    'ligand_H_receptor_heavy',
    'ligand_heavy_receptor_H',
    'H_H',
)


def load_inputs():
    payload = RIGID.read_bytes()
    assert sha(payload) == RIGID_SHA
    rigid = json.loads(gzip.decompress(payload))
    original = RIGID.with_name('producer_2026-10-09.py.txt').read_bytes()
    assert (
        sha(original)
        == rigid['consumer_source_sha256']['devtools/qualify_5x72_rigid.py']
    )
    archives, identities = load_archives()
    return rigid, load_reference(), archives, identities


def proof():
    record = rigid_proof()
    prior = load_inputs()[0]
    for key in (
        'qualified_provider_commit',
        'provider_native_artifacts',
        'producer_versions',
    ):
        assert record[key] == prior[key], key
    provider = Path(msm.__file__).resolve().parents[1]
    for relative in (
        'molsysmt/form/string_pdbqt_text/to_molsysmt_MolSys.py',
        'molsysmt/_private/pdbqt_adapter.py',
        'molsysmt/structure/get_distances.py',
    ):
        expected = subprocess.check_output(
            [
                'git',
                '-C',
                str(ROOT.parent / 'molsysmt'),
                'show',
                f'{record["qualified_provider_commit"]}:{relative}',
            ]
        )
        assert (provider / relative).read_bytes() == expected
        record['provider_source_sha256'][relative] = sha(expected)
    record['consumer_source_sha256'][str(Path(__file__).relative_to(ROOT))] = sha(
        Path(__file__).read_bytes()
    )
    return record


def captured(record, expected_map, receptor):
    """Admit the exact saved native-order input using explicit source indices."""
    mapping = record['metadata']['pdbqt_to_source_atom_indices']
    assert mapping == expected_map and sorted(mapping) == SOURCE_AXIS
    histories = record['metadata']['scoring_history']
    assert len(histories) == 1 and histories[0]['operation'] == 'score'
    artifacts = histories[0]['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    texts = {
        key: base64.b64decode(value['content_base64']).decode()
        for key, value in artifacts.items()
    }
    assert texts['receptor'] == receptor
    table = atom_fields(texts['partner'])
    assert len(table) == 25 and len({a['id'] for a in table}) == 25
    rows = [mapping.index(i) for i in SOURCE_AXIS]
    canonical = [
        {**table[row], 'source_atom_index': source}
        for source, row in zip(SOURCE_AXIS, rows, strict=True)
    ]
    assert [a['source_atom_index'] for a in canonical if a['type'] in H_TYPES] == [29]
    # The stored pose remains unrounded. Distances use submitted PDBQT below.
    pose = dmt.DockingPose.from_dict(record)
    np.testing.assert_allclose(
        puw.get_value(pose.coordinates, to_unit='angstrom'),
        [a['coordinates'] for a in table],
        rtol=0,
        atol=0.000500001,
    )
    return {
        'texts': texts,
        'artifacts': artifacts,
        'canonical_atoms': canonical,
        'projection_rows': rows,
        'scores_kcal_mol': score_components(record),
    }


def admit_orders(arm, case, receptors):
    admitted = {}
    for context, receptor in receptors.items():
        orders = {
            order: captured(
                data[context],
                case['controls'][order]['pdbqt_to_source_atom_indices'],
                receptor,
            )
            for order, data in arm['fixed_scores'].items()
        }
        assert set(orders) == {'native', 'first_fixed'}
        assert (
            orders['native']['canonical_atoms']
            == orders['first_fixed']['canonical_atoms']
        )
        assert (
            orders['native']['scores_kcal_mol']
            == orders['first_fixed']['scores_kcal_mol']
        )
        admitted[context] = orders
    assert (
        admitted['sham']['native']['texts']['partner']
        == admitted['occupied']['native']['texts']['partner']
    )
    return admitted


def matrix(admission):
    """Measure exact prepared projections with the public rectangular API."""
    ligand = msm.convert(
        'pdbqt_text:' + admission['texts']['partner'],
        to_form='molsysmt.MolSys',
        discard_torsion_tree=True,
    )
    receptor = msm.convert(
        'pdbqt_text:' + admission['texts']['receptor'], to_form='molsysmt.MolSys'
    )
    before = [snapshot(system) for system in (ligand, receptor)]
    receptor_atoms = atom_fields(admission['texts']['receptor'])
    coordinates = [
        np.asarray([a['coordinates'] for a in atoms])
        for atoms in (admission['canonical_atoms'], receptor_atoms)
    ]
    np.testing.assert_allclose(
        xyz(ligand)[admission['projection_rows']], coordinates[0], rtol=0, atol=1e-10
    )
    np.testing.assert_allclose(xyz(receptor), coordinates[1], rtol=0, atol=1e-10)
    values = puw.get_value(
        msm.structure.get_distances(
            ligand,
            selection=admission['projection_rows'],
            molecular_system_2=receptor,
            selection_2=list(range(len(receptor_atoms))),
            pairs=False,
            pbc=False,
            use_gpu=False,
            heavy_mode='off',
        ),
        to_unit='angstrom',
    )[0]
    assert values.shape == (25, len(receptor_atoms)) and np.isfinite(values).all()
    independent = np.linalg.norm(
        coordinates[0][:, None] - coordinates[1][None, :], axis=2
    )
    np.testing.assert_allclose(values, independent, rtol=0, atol=1e-10)
    assert [snapshot(system) for system in (ligand, receptor)] == before
    return values, receptor_atoms


def proximity(values):
    """Strict, prespecified distance bins; no physical interaction classification."""
    values = np.asarray(values)
    return {
        'pairs': int(values.size),
        'minimum_angstrom': float(values.min()) if values.size else None,
        'strict_threshold_counts': [
            int(np.count_nonzero(values < t)) for t in THRESHOLDS
        ],
    }


def classes(atoms):
    receptor_h = np.array([a['type'] in H_TYPES for a in atoms])
    ligand_h = np.array([i == 29 for i in SOURCE_AXIS])
    return {
        PAIR_CLASSES[0]: ~ligand_h[:, None] & ~receptor_h[None, :],
        PAIR_CLASSES[1]: ligand_h[:, None] & ~receptor_h[None, :],
        PAIR_CLASSES[2]: ~ligand_h[:, None] & receptor_h[None, :],
        PAIR_CLASSES[3]: ligand_h[:, None] & receptor_h[None, :],
    }


def summarize(values, atoms):
    masks = classes(atoms)
    partitions = {
        'protein': np.arange(len(atoms)) < PROTEIN_COUNT,
        'companion': np.arange(len(atoms)) >= PROTEIN_COUNT,
    }
    populations = {
        partition: {
            'all': proximity(values[:, selected]),
            **{
                kind: proximity(values[mask & selected[None, :]])
                for kind, mask in masks.items()
            },
        }
        for partition, selected in partitions.items()
    }
    per_atom = []
    for i, source in enumerate(SOURCE_AXIS):
        per_atom.append(
            {
                'source_atom_index': source,
                'partitions': {
                    p: proximity(values[i, selected])
                    for p, selected in partitions.items()
                },
            }
        )
    groups = {}
    for j, atom in enumerate(atoms):
        partition = 'protein' if j < PROTEIN_COUNT else 'companion'
        key = (partition, atom['chain'], atom['group_id'], atom['group'])
        groups.setdefault(key, []).append(j)
    per_group = []
    for key, rows in groups.items():
        selected = np.zeros(len(atoms), dtype=bool)
        selected[rows] = True
        per_group.append(
            {
                'partition': key[0],
                'chain': key[1],
                'group_id': key[2],
                'group': key[3],
                'receptor_rows': rows,
                'all': proximity(values[:, rows]),
                **{
                    kind: proximity(values[mask & selected[None, :]])
                    for kind, mask in masks.items()
                },
            }
        )
    assert sum(p['all']['pairs'] for p in populations.values()) == values.size
    assert (
        sum(populations[p][k]['pairs'] for p in populations for k in PAIR_CLASSES)
        == values.size
    )
    return {
        'populations': populations,
        'per_source_atom': per_atom,
        'per_receptor_group': per_group,
    }


def compare(reference, rigid, atoms):
    masks = classes(atoms)
    rows = []
    for i, j in zip(*np.nonzero((reference < 5.0) | (rigid < 5.0)), strict=True):
        kind = next(k for k, mask in masks.items() if mask[i, j])
        rows.append(
            {
                'source_atom_index': SOURCE_AXIS[i],
                'receptor_row': int(j),
                'receptor_serial': atoms[j]['id'],
                'partition': 'protein' if j < PROTEIN_COUNT else 'companion',
                'pair_class': kind,
                'experimental_reference_angstrom': float(reference[i, j]),
                'original_rigid_angstrom': float(rigid[i, j]),
                'rigid_minus_reference_angstrom': float(rigid[i, j] - reference[i, j]),
            }
        )
    return rows


def analyze(rigid, reference, archives):
    result = {}
    for name in ('p59', 'p69'):
        archive = archives[name]
        receptors = {
            k: v['pdbqt'] for k, v in archive['preparation']['receptors'].items()
        }
        receptor_tables = {k: atom_fields(v) for k, v in receptors.items()}
        assert len(receptor_tables['sham']) == PROTEIN_COUNT
        assert len(receptor_tables['occupied']) == PROTEIN_COUNT + 25
        assert receptor_tables['sham'] == receptor_tables['occupied'][:PROTEIN_COUNT]
        arms = {
            'original_rigid': admit_orders(
                rigid['conformers'][name], archive['cases'][name], receptors
            ),
            'experimental_reference': admit_orders(
                reference['references'][name], archive['cases'][name], receptors
            ),
        }
        for context in receptors:
            left, right = (arms[a][context]['native']['canonical_atoms'] for a in arms)
            assert [
                {k: v for k, v in atom.items() if k != 'coordinates'} for atom in left
            ] == [
                {k: v for k, v in atom.items() if k != 'coordinates'} for atom in right
            ]
        measured = {}
        for arm, contexts in arms.items():
            measured[arm] = {}
            for context, orders in contexts.items():
                values, atoms = matrix(orders['native'])
                measured[arm][context] = {
                    'matrix_angstrom': values,
                    'summary': summarize(values, atoms),
                    'canonical_ligand_atoms': orders['native']['canonical_atoms'],
                    'receptor_atoms': atoms,
                    'native_projection_rows': orders['native']['projection_rows'],
                    'root_input_identities': {
                        o: v['artifacts'] for o, v in orders.items()
                    },
                    'saved_scores_kcal_mol': orders['native']['scores_kcal_mol'],
                    'projection_inputs_unchanged': True,
                }
            np.testing.assert_allclose(
                measured[arm]['sham']['matrix_angstrom'],
                measured[arm]['occupied']['matrix_angstrom'][:, :PROTEIN_COUNT],
                rtol=0,
                atol=1e-10,
            )
        contrasts = {
            c: compare(
                measured['experimental_reference'][c]['matrix_angstrom'],
                measured['original_rigid'][c]['matrix_angstrom'],
                receptor_tables[c],
            )
            for c in receptors
        }
        result[name] = {
            'arms': measured,
            'near_pair_contrasts': contrasts,
            'root_order_exact_on_source_axis': True,
            'protein_prefix_exact': True,
        }
    return detached_record(result)


def qualify():
    authenticated = proof()
    rigid, reference, archives, identities = load_inputs()
    result = analyze(rigid, reference, archives)
    assert proof() == authenticated
    matrices = [
        entry['matrix_angstrom']
        for ligand in result.values()
        for arm in ligand['arms'].values()
        for entry in arm.values()
    ]
    assert len(matrices) == 8 and sum(np.asarray(m).size for m in matrices) == 298700
    return {
        'schema': 'dockingmt.5x72_contact_audit@1',
        'date': '2026-10-09',
        'python': sys.version,
        'interpreter': sys.executable,
        **authenticated,
        'consumer_base_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'plan': PLAN,
        'rigid_archive_sha256': RIGID_SHA,
        'reference_archive_sha256': rigid['experimental_reference_archive_sha256'],
        'historical_archives': identities,
        'new_searches': 0,
        'new_fixed_evaluations': 0,
        'distance_matrices': 8,
        'distance_entries': 298700,
        'strict_thresholds_angstrom': THRESHOLDS,
        'canonical_ligand_source_axis': SOURCE_AXIS,
        'protein_rows': PROTEIN_COUNT,
        'ligands': result,
        'interpretation': 'Distance associations only; no energy decomposition or cause. Original versus generated H, omitted H and incomplete PDBQT chemistry remain explicit limits.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    save(qualify(), args.output)
