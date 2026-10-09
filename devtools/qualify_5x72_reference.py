"""Finite experimental-reference scores and rigid-fragment geometry diagnostic.

No search or optimization. Reuse all authenticated returned populations and
their saved fixed evaluations; public molecular operations own preparation,
coordinate placement, distances, explicit cuts and tree serialization.
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
import pandas as pd
import pyunitwizard as puw
from molsysmt.form.string_pdbqt_text import get_torsion_tree
from rdkit import Chem

import dockingmt as dmt
from devtools.qualify_5x72_occupancy import (
    DATA,
    ROOT,
    atom_fields,
    fixed_pair,
    frozen_partner,
    load_baseline,
    prepare_cases,
    sha,
    xyz,
)
from devtools.qualify_5x72_reciprocal import proof as reciprocal_proof
from devtools.qualify_5x72_root_order import CUTS
from devtools.qualify_181l_receptor import save
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, HYDROGEN, TYPING

OUTPUT = ROOT / 'devguide/validation/data/5x72_reference/audit_2026-10-09.json.gz'
ARCHIVES = {
    'p59': (
        '5x72_occupancy',
        '5f698db8afee0df5d4323e30991d7f9061cc6ddd783d09fdeec148dc45e9db20',
        '5fee9c2e5e99eb26ddc98bae529a511eb9d4ea60',
    ),
    'p69': (
        '5x72_reciprocal',
        '323a5cb7a826368eb4914219c3a29c2fdf440956a792f9ebf7812e2cc228083d',
        '3b8258f8a34fbb32dc8d5d09207553bff4b47bf5',
    ),
}
PLAN = 'https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6089648793'
ADDENDUM = 'https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6089744224'


def load_archives(*, authenticate_sources=False):
    """Authenticate saved bytes; original source admission is production-only."""
    records, identities = {}, {}
    for name, (directory, digest, commit) in ARCHIVES.items():
        path = (
            ROOT / 'devguide/validation/data' / directory / 'audit_2026-10-09.json.gz'
        )
        payload = path.read_bytes()
        assert sha(payload) == digest
        records[name] = json.loads(gzip.decompress(payload))
        tracked, generated = {}, {}
        for relative, expected in records[name]['consumer_source_sha256'].items():
            if not authenticate_sources:
                continue
            route = f'{commit}:{relative}'
            probe = subprocess.run(
                ['git', 'cat-file', '-e', route], capture_output=True
            )
            if probe.returncode == 0:
                content = subprocess.check_output(['git', 'show', route])
                tracked[relative] = expected
            else:
                assert relative == 'dockingmt/_version.py'
                content = (ROOT / relative).read_bytes()
                generated[relative] = expected
            assert sha(content) == expected, relative
        identities[name] = {
            'path': str(path.relative_to(ROOT)),
            'gzip_sha256': digest,
            'json_sha256': sha(gzip.decompress(payload)),
            'producer_commit': commit,
            'original_sources_verified': authenticate_sources,
            'tracked_source_git_blob_sha256': tracked,
            'separately_preserved_generated_sha256': generated,
        }
    return records, identities


def proof():
    record = reciprocal_proof()
    provider = Path(msm.__file__).resolve().parents[1]
    for relative in (
        'molsysmt/basic/copy.py',
        'molsysmt/form/molsysmt_MolSys/copy.py',
        'molsysmt/structure/get_distances.py',
        'molsysmt/topology/get_rigid_fragments.py',
        'molsysmt/topology/_chemical_graph.py',
        'molsysmt/_private/rust_backend.py',
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


def chemical_axis(system):
    """Indexed evidence for these two fixtures; nullable orders stay unknown."""
    record = {}
    for element, attributes in (
        (
            'atom',
            ('atom_type', 'formal_charge', 'atom_stereochemistry', 'atom_is_aromatic'),
        ),
        ('bond', ('bond_order',)),
    ):
        for attribute in attributes:
            record[attribute] = [
                None if pd.isna(v) else v
                for v in msm.get(system, element=element, **{attribute: True})
            ]
    pairs = np.asarray(msm.get(system, element='bond', bonded_atom_pairs=True))
    record['bonded_atom_pairs'] = pairs.tolist()
    record['hydrogen_parent_pairs'] = sorted(
        [int(max(a, b)), int(min(a, b))] for a, b in pairs if max(a, b) >= 24
    )
    assert len(pairs) == 42 and len(record['hydrogen_parent_pairs']) == 15
    return detached_record(record)


def prepare_reference(name, source, case):
    """Preserve original identity on an independently verified reference axis."""
    before = snapshot(source)
    heavy = msm.convert(
        next(
            iter(
                Chem.SDMolSupplier(
                    str(DATA / f'5x72_ligand_{name}.sdf'), removeHs=False
                )
            )
        ),
        to_form='molsysmt.MolSys',
    )
    heavy_before = snapshot(heavy)
    # Compare chemistry exactly and fixed-unit geometry within roundoff. A pm
    # policy changes the last binary digits during the RDKit/native conversion.
    expected = case['reference_snapshot']
    for key in heavy_before:
        if key != 'structures':
            assert heavy_before[key] == expected[key]
    for key, value in heavy_before['structures'].items():
        if key == 'coordinates':
            np.testing.assert_allclose(
                value, expected['structures'][key], rtol=0, atol=1e-13
            )
        else:
            assert value == expected['structures'][key]
    addition = msm.build.add_missing_hydrogens(heavy, return_report=True, **HYDROGEN)
    generated = addition['molecular_system']
    axis = chemical_axis(source)
    assert chemical_axis(generated) == axis
    assert [29, 8] in axis['hydrogen_parent_pairs']
    np.testing.assert_allclose(xyz(generated)[:24], xyz(heavy), rtol=0, atol=1e-12)
    assert snapshot(heavy) == heavy_before
    placed = msm.copy(source)
    msm.set(placed, coordinates=puw.quantity(xyz(generated)[None], 'angstrom'))
    placed_before = snapshot(placed)
    for key in ('topology', 'chemical_states', 'structure_chemical_state_indices'):
        assert placed_before[key] == before[key]
    np.testing.assert_allclose(xyz(placed), xyz(generated), rtol=0, atol=1e-12)
    prepared = dmt.prepare_ligand(
        placed,
        selection='all',
        active_torsion_bonds=CUTS,
        charge_options=CHARGE,
        typing_options=TYPING,
    )
    mapping = [
        prepared.metadata['retained_atom_indices'][i]
        for i in prepared.pdbqt_atom_indices
    ]
    assert mapping == case['controls']['native']['pdbqt_to_source_atom_indices']
    original = case['controls']['native']['pdbqt']
    for a, b in zip(
        atom_fields(original), atom_fields(prepared.to_pdbqt()), strict=True
    ):
        for field in ('id', 'name', 'group', 'group_id', 'chain', 'charge_e', 'type'):
            assert a[field] == b[field], (name, field)
    assert detached_record(
        get_torsion_tree('pdbqt_text:' + original)
    ) == detached_record(get_torsion_tree('pdbqt_text:' + prepared.to_pdbqt()))
    poses = {}
    for order, control in case['controls'].items():
        pose = dmt.DockingPose(
            puw.quantity(
                xyz(placed)[control['pdbqt_to_source_atom_indices']], 'angstrom'
            ),
            metadata={
                'reference_kind': 'experimental_heavy_generated_H',
                'ligand': name,
                'pdbqt_to_source_atom_indices': control['pdbqt_to_source_atom_indices'],
                'hydrogen_parent_pairs': axis['hydrogen_parent_pairs'],
            },
        )
        assert pose.rank is None and pose.scores == {}
        frozen_partner(control, pose)
        poses[order] = pose
    assert snapshot(source) == before and snapshot(placed) == placed_before
    return (
        placed,
        poses,
        detached_record(
            {
                'chemical_axis': axis,
                'original_source_snapshot': before,
                'reference_snapshot': heavy_before,
                'generated_reference_snapshot': snapshot(generated),
                'placed_reference_snapshot': placed_before,
                'hydrogen_addition': addition['report'],
                'original_atom_names': msm.get(source, element='atom', atom_name=True),
                'generated_atom_names': msm.get(
                    generated, element='atom', atom_name=True
                ),
                'placement': 'Public detached copy; set coordinates on independently checked identical indexed chemical/H axis. No renaming.',
                'direct_preparation_admission': 'Rejected before scoring: generated reference names differ from original controls. See prescoring addendum.',
                'prepared': prepared.to_dict(),
                'charge_audit': dmt.audit_preparation_charges(prepared),
                'source_unchanged': True,
            }
        ),
    )


def geometry_diagnostic(source, reference):
    before = [snapshot(system) for system in (source, reference)]
    pairs = np.asarray(msm.get(source, element='bond', bonded_atom_pairs=True))
    cut_indices = [
        next(i for i, pair in enumerate(pairs) if sorted(pair) == sorted(cut))
        for cut in CUTS
    ]
    fragments = msm.topology.get_rigid_fragments(source, bond_indices=cut_indices)
    assert detached_record(
        msm.topology.get_rigid_fragments(reference, bond_indices=cut_indices)
    ) == detached_record(fragments)
    labels = fragments['atom_fragment_indices'][:24]
    distances, coordinates = [], []
    for system in (source, reference):
        coords = xyz(system)[:24]
        public = puw.get_value(
            msm.structure.get_distances(
                system, selection=list(range(24)), pbc=False, use_gpu=False
            ),
            to_unit='angstrom',
        )[0]
        independent = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=2)
        np.testing.assert_allclose(public, independent, rtol=0, atol=1e-10)
        distances.append(public)
        coordinates.append(coords.tolist())
    bonds = {tuple(sorted(pair)) for pair in pairs if max(pair) < 24}
    rows = []
    for i, j in itertools.combinations(range(24), 2):
        rows.append(
            {
                'source_atom_pair': [i, j],
                'heavy_bond': (i, j) in bonds,
                'fragment_indices': [int(labels[i]), int(labels[j])],
                'within_fragment': bool(labels[i] == labels[j]),
                'prepared_distance_angstrom': float(distances[0][i, j]),
                'reference_distance_angstrom': float(distances[1][i, j]),
                'reference_minus_prepared_angstrom': float(
                    distances[1][i, j] - distances[0][i, j]
                ),
            }
        )
    assert len(rows) == 276 and sum(r['heavy_bond'] for r in rows) == 27
    summaries = []
    for label in ('all', *sorted(set(int(v) for v in labels))):
        selected = (
            rows
            if label == 'all'
            else [r for r in rows if r['fragment_indices'] == [label, label]]
        )
        delta = np.array([r['reference_minus_prepared_angstrom'] for r in selected])
        summaries.append(
            {
                'fragment': label,
                'heavy_atom_indices': list(range(24))
                if label == 'all'
                else np.flatnonzero(labels == label).tolist(),
                'pairs': len(selected),
                'rms_distance_difference_angstrom': float(np.sqrt(np.mean(delta**2))),
                'max_absolute_distance_difference_angstrom': float(
                    np.max(np.abs(delta))
                ),
            }
        )
    assert [snapshot(system) for system in (source, reference)] == before
    return detached_record(
        {
            'explicit_cut_source_bond_indices': cut_indices,
            'fragments': fragments,
            'source_heavy_coordinates_angstrom': coordinates[0],
            'reference_heavy_coordinates_angstrom': coordinates[1],
            'pairs': rows,
            'summaries': summaries,
            'interpretation': 'Pair-distance congruence diagnostic; no fitting, chemical tolerance, affinity or proof of global reachability.',
        }
    )


def score_components(data):
    return data['metadata']['scoring_history'][-1]['scores']


def compare_saved(name, archive, references):
    rows, cells = [], []
    for cell_index, run in enumerate(archive['new_runs']):
        order = run['order']
        parameters = run['result']['protocol_info']['parameters']
        result = dmt.DockingResult.from_dict(run['result'])
        for receptor in ('sham', 'occupied'):
            reference = score_components(references[order][receptor])
            selected = []
            for pose_index, (pose, metric, pair) in enumerate(
                zip(
                    result.poses,
                    run['heavy_atom_metrics'],
                    run['fixed_scores'],
                    strict=True,
                )
            ):
                saved = pair[receptor]
                scored = dmt.DockingPose.from_dict(saved)
                assert (
                    scored.rank == pose.rank
                    and scored.scores['vina'] == pose.scores['vina']
                )
                np.testing.assert_array_equal(
                    puw.get_value(scored.coordinates, to_unit='angstrom'),
                    puw.get_value(pose.coordinates, to_unit='angstrom'),
                )
                artifacts = scored.metadata['scoring_history'][-1]['backend_artifacts']
                assert dmt.verify_captured_inputs(artifacts)
                assert (
                    artifacts['receptor']['sha256']
                    == archive['preparation']['receptors'][receptor]['sha256']
                )
                components = score_components(saved)
                assert set(components) == set(reference) and len(components) == 8
                row = {
                    'ligand': name,
                    'cell_index': cell_index,
                    'pose_index': pose_index,
                    'search_receptor': run['receptor'],
                    'score_receptor': receptor,
                    'order': order,
                    'seed': parameters['seed'],
                    'exhaustiveness': parameters['exhaustiveness'],
                    'original_rank': pose.rank,
                    'recovered': metric['recovered'],
                    'heavy_rmsd_angstrom': metric[
                        'heavy_atom_positional_rmsd_angstrom'
                    ],
                    'source_atom_indices': archive['cases'][name]['controls'][order][
                        'pdbqt_to_source_atom_indices'
                    ],
                    'pose_fixed_components_kcal_mol': components,
                    'reference_fixed_components_kcal_mol': reference,
                    'pose_minus_reference_kcal_mol': {
                        k: components[k] - reference[k] for k in reference
                    },
                }
                rows.append(row)
                selected.append(row)
            minimum = min(
                selected,
                key=lambda r: (
                    r['pose_fixed_components_kcal_mol']['fixed'],
                    r['original_rank'],
                ),
            )
            closest = min(
                selected, key=lambda r: (r['heavy_rmsd_angstrom'], r['original_rank'])
            )
            cells.append(
                {
                    'ligand': name,
                    'cell_index': cell_index,
                    'search_receptor': run['receptor'],
                    'score_receptor': receptor,
                    'order': order,
                    'seed': parameters['seed'],
                    'exhaustiveness': parameters['exhaustiveness'],
                    'poses': len(selected),
                    'reference_total_kcal_mol': reference['fixed'],
                    'pose_totals_below_reference': sum(
                        r['pose_minus_reference_kcal_mol']['fixed'] < 0
                        for r in selected
                    ),
                    'pose_totals_equal_reference': sum(
                        r['pose_minus_reference_kcal_mol']['fixed'] == 0
                        for r in selected
                    ),
                    'first': selected[0],
                    'minimum_fixed': minimum,
                    'closest_reference': closest,
                }
            )
    assert len(rows) == 156 and len(cells) == 48
    return rows, cells


def qualify():
    authenticated = proof()
    archives, identities = load_archives(authenticate_sources=True)
    sources, cases = prepare_cases()
    assert cases == load_baseline()['cases']
    record = {
        'schema': 'dockingmt.5x72_reference_audit@1',
        'date': '2026-10-09',
        'python': sys.version,
        'interpreter': sys.executable,
        **authenticated,
        'consumer_base_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'plan': PLAN,
        'admission_addendum': ADDENDUM,
        'historical_archives': identities,
        'references': {},
        'comparison_rows': [],
        'cell_summaries': [],
        'new_searches': 0,
        'new_fixed_evaluations': 8,
        'saved_poses_reused': 156,
        'saved_fixed_evaluations_reused': 312,
    }
    for name in ('p59', 'p69'):
        archive = archives[name]
        assert archive['cases'] == cases
        placed, poses, preparation = prepare_reference(name, sources[name], cases[name])
        # Strict production also authenticates freshly generated H placement.
        companion_archive = archives['p69' if name == 'p59' else 'p59']
        assert (
            preparation['generated_reference_snapshot']
            == companion_archive['preparation']['companion_generated_source_snapshot']
        )
        receptors = {
            k: v['pdbqt'] for k, v in archive['preparation']['receptors'].items()
        }
        scores = {
            order: fixed_pair(pose, cases[name]['controls'][order], receptors)
            for order, pose in poses.items()
        }
        agreement = {
            context: {
                key: score_components(scores['first_fixed'][context])[key] - value
                for key, value in score_components(scores['native'][context]).items()
            }
            for context in receptors
        }
        record['references'][name] = {
            'preparation': preparation,
            'poses': {k: detached_record(v.to_dict()) for k, v in poses.items()},
            'fixed_scores': scores,
            'root_order_component_difference_kcal_mol': agreement,
            'root_order_agrees_at_0_001_kcal_mol': all(
                abs(v) <= 0.001
                for differences in agreement.values()
                for v in differences.values()
            ),
            'geometry': geometry_diagnostic(sources[name], placed),
        }
        rows, cells = compare_saved(name, archive, scores)
        record['comparison_rows'].extend(rows)
        record['cell_summaries'].extend(cells)
        print(
            f'{name}: four reference scores, 78 saved poses and 276 indexed heavy pairs',
            file=sys.stderr,
            flush=True,
        )
    assert len(record['comparison_rows']) == 312 and len(record['cell_summaries']) == 96
    assert proof() == authenticated
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    save(qualify(), args.output)
