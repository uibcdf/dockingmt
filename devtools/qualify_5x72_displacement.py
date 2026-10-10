"""Prespecified seven-point rigid translation of two saved 5X72 geometry arms.

Public molecular operations move all 39 atoms without changing internal/H
geometry. All 112 fixed evaluations are retained; no adaptive optimization.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_5x72_contact import OUTPUT as CONTACT
from devtools.qualify_5x72_contact import (
    PROTEIN_COUNT,
    SOURCE_AXIS,
    captured,
    load_inputs,
)
from devtools.qualify_5x72_contact import (
    proof as contact_proof,
)
from devtools.qualify_5x72_occupancy import atom_fields, fixed_pair, frozen_partner
from devtools.qualify_5x72_reference import ROOT, chemical_axis, score_components, sha
from devtools.qualify_5x72_rigid import distances
from devtools.qualify_5x72_root_order import xyz
from devtools.qualify_181l_receptor import save
from devtools.qualify_chemical_templates import detached_record, load_5x72, snapshot

OUTPUT = ROOT / 'devguide/validation/data/5x72_displacement/audit_2026-10-09.json.gz'
CONTACT_SHA = '84ad1212925bd0765f99b5e9a8932d5b7976e887f51a14964ec295b501aa5490'
PLAN = 'https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6094392354'
OFFSETS = [
    [0.0, 0.0, 0.0],
    [-0.25, 0.0, 0.0],
    [0.25, 0.0, 0.0],
    [0.0, -0.25, 0.0],
    [0.0, 0.25, 0.0],
    [0.0, 0.0, -0.25],
    [0.0, 0.0, 0.25],
]
ARMS = ('original_rigid', 'experimental_reference')
UNITS = {
    'coordinates': 'angstrom',
    'translation': 'angstrom',
    'pair_distance': 'angstrom',
    'rmsd': 'angstrom',
    'scores': 'kcal/mol',
}
PAIR_KEYS = {
    'p59': [(16, 'ARG', '61', 'NH1'), (16, 'GLN', '78', 'NE2')],
    'p69': [(4, 'GLN', '116', 'OE1'), (16, 'TYR', '149', 'OH')],
}


def load_contact():
    payload = CONTACT.read_bytes()
    assert sha(payload) == CONTACT_SHA
    record = json.loads(gzip.decompress(payload))
    assert (
        sha(CONTACT.with_name('producer_2026-10-09.py').read_bytes())
        == record['consumer_source_sha256']['devtools/qualify_5x72_contact.py']
    )
    return record


def proof():
    record = contact_proof()
    prior = load_contact()
    for key in (
        'qualified_provider_commit',
        'provider_native_artifacts',
        'producer_versions',
    ):
        assert record[key] == prior[key]
    record['consumer_source_sha256'][str(Path(__file__).relative_to(ROOT))] = sha(
        Path(__file__).read_bytes()
    )
    return record


def read_coordinates(record):
    """Read the old native snapshot's declared fixed-unit coordinate protocol."""
    assert record['structure_units'] == {'coordinates': 'nm', 'box': 'nm', 'time': 'ps'}
    return puw.get_value(
        puw.quantity(record['structures']['coordinates'], 'nm'), to_unit='angstrom'
    )[0]


def base_systems(rigid, reference, archives):
    bases, evidence = {}, {}
    for name in ('p59', 'p69'):
        _, source = load_5x72(name)
        before = snapshot(source)
        construction = rigid['conformers'][name]['construction']
        assert (
            chemical_axis(source)
            == construction['experimental_reference_evidence']['chemical_axis']
        )
        assert (
            msm.get(source, element='atom', atom_name=True)
            == construction['experimental_reference_evidence']['original_atom_names']
        )
        np.testing.assert_allclose(
            xyz(source),
            read_coordinates(archives[name]['cases'][name]['source_snapshot']),
            rtol=0,
            atol=1e-10,
        )
        records = {
            'original_rigid': construction['fitted_snapshot'],
            'experimental_reference': reference['references'][name]['preparation'][
                'placed_reference_snapshot'
            ],
        }
        bases[name] = {}
        for arm, record in records.items():
            base = msm.copy(source)
            msm.set(
                base,
                coordinates=puw.quantity(read_coordinates(record)[None], 'angstrom'),
            )
            after = snapshot(base)
            for key in (
                'topology',
                'chemical_states',
                'structure_chemical_state_indices',
            ):
                assert before[key] == after[key]
            bases[name][arm] = base
        assert snapshot(source) == before
        evidence[name] = {
            'indexed_chemical_axis': chemical_axis(source),
            'source_snapshot': before,
            'source_unchanged': True,
            'base_snapshots': {a: snapshot(b) for a, b in bases[name].items()},
        }
    return bases, detached_record(evidence)


def translated_point(base, offset_index, name, arm, case):
    assert type(offset_index) is int and 0 <= offset_index < len(OFFSETS)
    offset = np.asarray(OFFSETS[offset_index])
    before = snapshot(base)
    original = xyz(base)
    moved = msm.structure.translate(
        base,
        translation=puw.quantity(offset[None, None], 'angstrom'),
        selection='all',
        in_place=False,
    )
    assert snapshot(base) == before
    after = snapshot(moved)
    for key in ('topology', 'chemical_states', 'structure_chemical_state_indices'):
        assert before[key] == after[key]
    coordinates = xyz(moved)
    assert coordinates.shape == (39, 3)
    np.testing.assert_allclose(
        coordinates - original,
        np.broadcast_to(offset, coordinates.shape),
        rtol=0,
        atol=1e-10,
    )
    before_distances, after_distances = distances(base), distances(moved)
    np.testing.assert_allclose(before_distances, after_distances, rtol=0, atol=1e-10)
    pairs = np.asarray(list(itertools.combinations(range(39), 2)))
    volumes = [
        float(np.linalg.det(c[[6, 8, 17]] - c[28])) for c in (original, coordinates)
    ]
    assert np.sign(volumes[0]) == np.sign(volumes[1]) and abs(volumes[0]) > 1e-9
    np.testing.assert_allclose(volumes[0], volumes[1], rtol=0, atol=1e-10)
    reference = np.asarray(case['reference_coordinates_angstrom'])
    rmsd = float(
        puw.get_value(
            msm.structure.get_rmsd(
                moved,
                selection=list(range(24)),
                reference_molecular_system=puw.quantity(reference[None], 'angstrom'),
                reference_selection=list(range(24)),
                use_gpu=False,
            ),
            to_unit='angstrom',
        ).reshape(-1)[0]
    )
    np.testing.assert_allclose(
        rmsd,
        np.sqrt(np.mean(np.sum((coordinates[:24] - reference) ** 2, axis=1))),
        rtol=0,
        atol=1e-10,
    )
    poses = {
        order: dmt.DockingPose(
            puw.quantity(
                coordinates[control['pdbqt_to_source_atom_indices']], 'angstrom'
            ),
            metadata={
                'ligand': name,
                'geometry_arm': arm,
                'offset_index': offset_index,
                'offset_angstrom': offset.tolist(),
                'pdbqt_to_source_atom_indices': control['pdbqt_to_source_atom_indices'],
            },
        )
        for order, control in case['controls'].items()
    }
    assert all(p.rank is None and p.scores == {} for p in poses.values())
    return (
        moved,
        poses,
        detached_record(
            {
                'offset_index': offset_index,
                'offset_angstrom': offset,
                'full39_coordinates_angstrom': coordinates,
                'heavy_positional_rmsd_angstrom': rmsd,
                'within_original_2_5_angstrom_criterion': rmsd <= 2.5,
                'all741_pair_indices': pairs,
                'all741_original_distances_angstrom': before_distances[
                    pairs[:, 0], pairs[:, 1]
                ],
                'all741_translated_distances_angstrom': after_distances[
                    pairs[:, 0], pairs[:, 1]
                ],
                'max_full_pair_distance_change_angstrom': np.max(
                    np.abs(before_distances - after_distances)
                ),
                'original_and_translated_signed_volume_angstrom_cubed': volumes,
                'input_unchanged': True,
                'translated_snapshot': after,
            }
        ),
    )


def selected_pair_distances(admission, name):
    table = atom_fields(admission['texts']['receptor'])
    rows = []
    identities = []
    for source, group, group_id, atom_name in PAIR_KEYS[name]:
        matches = [
            i
            for i, atom in enumerate(table[:PROTEIN_COUNT])
            if (atom['chain'], atom['group'], atom['group_id'], atom['name'])
            == ('A', group, group_id, atom_name)
        ]
        assert len(matches) == 1
        j = matches[0]
        rows.append(j)
        identities.append(
            {
                'source_atom_index': source,
                'receptor_row': j,
                'receptor_serial': table[j]['id'],
                'receptor_atom': table[j],
            }
        )
    ligand = msm.convert(
        'pdbqt_text:' + admission['texts']['partner'],
        to_form='molsysmt.MolSys',
        discard_torsion_tree=True,
    )
    receptor = msm.convert(
        'pdbqt_text:' + admission['texts']['receptor'], to_form='molsysmt.MolSys'
    )
    before = [snapshot(s) for s in (ligand, receptor)]
    sources = sorted({p[0] for p in PAIR_KEYS[name]})
    selection = [admission['projection_rows'][SOURCE_AXIS.index(s)] for s in sources]
    values = puw.get_value(
        msm.structure.get_distances(
            ligand,
            selection=selection,
            molecular_system_2=receptor,
            selection_2=rows,
            pairs=False,
            pbc=False,
            use_gpu=False,
            heavy_mode='off',
        ),
        to_unit='angstrom',
    )[0]
    left = np.asarray(
        [
            admission['canonical_atoms'][SOURCE_AXIS.index(s)]['coordinates']
            for s in sources
        ]
    )
    right = np.asarray([table[j]['coordinates'] for j in rows])
    np.testing.assert_allclose(
        values,
        np.linalg.norm(left[:, None] - right[None, :], axis=2),
        rtol=0,
        atol=1e-10,
    )
    assert [snapshot(s) for s in (ligand, receptor)] == before
    for j, identity in enumerate(identities):
        identity['distance_angstrom'] = float(
            values[sources.index(identity['source_atom_index']), j]
        )
    return detached_record(
        {
            'ligand_source_rows': sources,
            'receptor_rows': rows,
            'rectangular_distances_angstrom': values,
            'declared_pairs': identities,
            'input_projections_unchanged': True,
        }
    )


def assess_scores(poses, case, receptors, scores, old_arm, offset_index):
    admitted = {
        context: {
            order: captured(
                data[context],
                case['controls'][order]['pdbqt_to_source_atom_indices'],
                receptor,
            )
            for order, data in scores.items()
        }
        for context, receptor in receptors.items()
    }
    agreement = {}
    for context, orders in admitted.items():
        assert (
            orders['native']['canonical_atoms']
            == orders['first_fixed']['canonical_atoms']
        )
        agreement[context] = {
            k: orders['first_fixed']['scores_kcal_mol'][k] - v
            for k, v in orders['native']['scores_kcal_mol'].items()
        }
        for order, admission in orders.items():
            assert admission['texts']['partner'] == frozen_partner(
                case['controls'][order], poses[order]
            )
            if offset_index == 0:
                old = captured(
                    old_arm['fixed_scores'][order][context],
                    case['controls'][order]['pdbqt_to_source_atom_indices'],
                    receptors[context],
                )
                assert admission['texts'] == old['texts']
                assert admission['scores_kcal_mol'] == old['scores_kcal_mol']
    assert (
        admitted['sham']['native']['canonical_atoms']
        == admitted['occupied']['native']['canonical_atoms']
    )
    return admitted, agreement


def summarize(points):
    rows = []
    for name in ('p59', 'p69'):
        for arm in ARMS:
            population = [
                p for p in points if p['ligand'] == name and p['geometry_arm'] == arm
            ]
            assert [p['offset_index'] for p in population] == list(range(7))
            anchor = population[0]
            for context in ('sham', 'occupied'):
                for order in ('native', 'first_fixed'):
                    zero = score_components(anchor['fixed_scores'][order][context])
                    totals = [
                        score_components(p['fixed_scores'][order][context])['fixed']
                        for p in population
                    ]
                    best = min(range(7), key=lambda i: (totals[i], i))
                    worst = max(range(7), key=lambda i: (totals[i], -i))
                    rows.append(
                        {
                            'ligand': name,
                            'geometry_arm': arm,
                            'context': context,
                            'order': order,
                            'zero_total_kcal_mol': zero['fixed'],
                            'seven_totals_kcal_mol': totals,
                            'nonzero_offsets_with_strictly_lower_reported_total': sum(
                                v < zero['fixed'] for v in totals[1:]
                            ),
                            'finite_minimum_offset_index': best,
                            'finite_minimum_total_kcal_mol': totals[best],
                            'finite_minimum_minus_zero_kcal_mol': totals[best]
                            - zero['fixed'],
                            'finite_maximum_offset_index': worst,
                            'finite_maximum_total_kcal_mol': totals[worst],
                            'finite_maximum_minus_zero_kcal_mol': totals[worst]
                            - zero['fixed'],
                            'all_component_deltas_kcal_mol': [
                                {
                                    k: v - zero[k]
                                    for k, v in score_components(
                                        p['fixed_scores'][order][context]
                                    ).items()
                                }
                                for p in population
                            ],
                        }
                    )
    return detached_record(rows)


def qualify():
    authenticated = proof()
    rigid, reference, archives, identities = load_inputs()
    contacts = load_contact()
    bases, base_evidence = base_systems(rigid, reference, archives)
    points = []
    for offset_index in range(len(OFFSETS)):
        for name in ('p59', 'p69'):
            archive = archives[name]
            case = archive['cases'][name]
            receptors = {
                k: v['pdbqt'] for k, v in archive['preparation']['receptors'].items()
            }
            for arm in ARMS:
                _, poses, geometry = translated_point(
                    bases[name][arm], offset_index, name, arm, case
                )
                old_arm = (
                    rigid['conformers'][name]
                    if arm == 'original_rigid'
                    else reference['references'][name]
                )
                scores = {
                    order: fixed_pair(pose, case['controls'][order], receptors)
                    for order, pose in poses.items()
                }
                admitted, agreement = assess_scores(
                    poses, case, receptors, scores, old_arm, offset_index
                )
                pair_data = {
                    c: selected_pair_distances(v['native'], name)
                    for c, v in admitted.items()
                }
                assert pair_data['sham'] == pair_data['occupied']
                if offset_index == 0:
                    for pair in pair_data['sham']['declared_pairs']:
                        row = next(
                            x
                            for x in contacts['ligands'][name]['near_pair_contrasts'][
                                'sham'
                            ]
                            if x['source_atom_index'] == pair['source_atom_index']
                            and x['receptor_row'] == pair['receptor_row']
                        )
                        expected = row[
                            'original_rigid_angstrom'
                            if arm == 'original_rigid'
                            else 'experimental_reference_angstrom'
                        ]
                        np.testing.assert_allclose(
                            pair['distance_angstrom'], expected, rtol=0, atol=1e-10
                        )
                points.append(
                    {
                        'ligand': name,
                        'geometry_arm': arm,
                        'offset_index': offset_index,
                        'geometry': geometry,
                        'poses': {
                            o: detached_record(p.to_dict()) for o, p in poses.items()
                        },
                        'fixed_scores': scores,
                        'selected_pair_distances': pair_data,
                        'root_order_component_difference_kcal_mol': agreement,
                        'zero_anchor_matches_original_bytes_and_components': offset_index
                        == 0,
                    }
                )
                print(
                    f'{name}/{arm}/offset{offset_index}: four fixed scores; all39 geometry preserved',
                    file=sys.stderr,
                    flush=True,
                )
    assert len(points) == 28 and proof() == authenticated
    return {
        'schema': 'dockingmt.5x72_displacement_audit@1',
        'date': '2026-10-09',
        'unit_contract': UNITS,
        'python': sys.version,
        'interpreter': sys.executable,
        **authenticated,
        'consumer_base_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'plan': PLAN,
        'offsets_angstrom': OFFSETS,
        'contact_archive_sha256': CONTACT_SHA,
        'historical_archives': identities,
        'new_fixed_evaluations': 112,
        'fresh_zero_anchor_evaluations': 16,
        'new_nonzero_translation_evaluations': 96,
        'new_searches': 0,
        'new_optimizations': 0,
        'base_admission': base_evidence,
        'points': points,
        'summaries': summarize(points),
        'interpretation': 'Finite positional sensitivity, not optimization, returned-pose recovery, pair-energy decomposition or causal attribution. H is fixed within each arm and remains different between arms.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    save(qualify(), args.output)
