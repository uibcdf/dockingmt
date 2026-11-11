"""Project the seven historical 5X72 controls without molecular/scoring imports."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'devguide/validation/data'
OUTPUT = DATA / '5x72_synthesis_2026-11-05'
INPUTS = {
    'root_order': '2129d7eed2b73bcf90737b2a6c722e3b8e9269abeba0ca3b1444df51f046634e',
    'occupancy': '5f698db8afee0df5d4323e30991d7f9061cc6ddd783d09fdeec148dc45e9db20',
    'reciprocal': '323a5cb7a826368eb4914219c3a29c2fdf440956a792f9ebf7812e2cc228083d',
    'reference': '8b53aac76447951737e0f477124fa11b074c8e0d6ae4244eac686968d471c1d3',
    'rigid': 'f0e91b99793bc61403aedf660016f532e1a46c5815f92441f511dbac8ffb4179',
    'contact': '84ad1212925bd0765f99b5e9a8932d5b7976e887f51a14964ec295b501aa5490',
    'displacement': 'afb8bfa4092abc78f8cd2daf33da7248fe39fbd1856b23e24a192f4813fb72a8',
}
CRITERION = {
    'alignment': False,
    'atom_population': '24_experimental_heavy_atoms',
    'cutoff_angstrom': 2.5,
    'metric': 'positional_rmsd',
    'symmetry_correction': False,
}
ORDERS = ('native', 'first_fixed')
SEEDS = (7, 42, 2026)
EFFORTS = (1, 8)
EXPECTED = {
    'root_order': (24, 99, 0),
    'occupancy': (24, 78, 256),
    'reciprocal': (24, 78, 254),
    'reference': (0, 0, 8),
    'rigid': (0, 0, 8),
    'contact': (0, 0, 0),
    'displacement': (0, 0, 112),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_json(value):
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n'


def digest(value):
    return hashlib.sha256(text_json(value).encode()).hexdigest()


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_archive(name, data=DATA):
    relative = f'5x72_{name}/audit_2026-10-09.json.gz'
    payload = (Path(data) / relative).read_bytes()
    require(
        hashlib.sha256(payload).hexdigest() == INPUTS[name],
        f'Input hash mismatch: {name}',
    )
    decoded = gzip.decompress(payload)
    return json.loads(decoded), {
        'path': relative,
        'sha256': INPUTS[name],
        'json_sha256': hashlib.sha256(decoded).hexdigest(),
    }


def source_links(name, document, previous):
    required = {
        'root_order': (),
        'occupancy': ('baseline_sha256',),
        'reciprocal': ('baseline_sha256',),
        'reference': (),
        'rigid': ('experimental_reference_archive_sha256',),
        'contact': ('reference_archive_sha256', 'rigid_archive_sha256'),
        'displacement': ('contact_archive_sha256',),
    }
    require(
        all(field in document for field in required[name]), 'Missing archive dependency'
    )
    if name in ('reference', 'rigid', 'contact', 'displacement'):
        require(
            set(document.get('historical_archives', {})) == {'p59', 'p69'},
            'Incomplete historical dependencies',
        )
    links = []
    for field, target in (
        ('baseline_sha256', 'root_order'),
        ('experimental_reference_archive_sha256', 'reference'),
        ('reference_archive_sha256', 'reference'),
        ('rigid_archive_sha256', 'rigid'),
        ('contact_archive_sha256', 'contact'),
    ):
        if field in document:
            require(
                document[field] == previous[target]['sha256'],
                f'Changed archive link: {name}/{field}',
            )
            links.append({'target': target, 'field': field, 'sha256': document[field]})
    for ligand, historical in document.get('historical_archives', {}).items():
        require(ligand in ('p59', 'p69'), 'Unexpected historical ligand')
        target = 'occupancy' if ligand == 'p59' else 'reciprocal'
        require(
            historical['gzip_sha256'] == previous[target]['sha256']
            and historical['json_sha256'] == previous[target]['json_sha256'],
            'Historical archive identity mismatch',
        )
        require(
            type(historical['original_sources_verified']) is bool,
            'Unknown historical proof status',
        )
        links.append(
            {
                'target': target,
                'field': f'historical_archives/{ligand}',
                'sha256': historical['gzip_sha256'],
                'producer_commit': historical['producer_commit'],
                'original_sources_verified': historical['original_sources_verified'],
                'original_proof_record_sha256': digest(historical),
            }
        )
    return links


def recovery_groups(name, document):
    require(document['criterion'] == CRITERION, 'Changed recovery criterion')
    cells = document['comparison_rows']
    contexts = ('protein_only',) if name == 'root_order' else ('sham', 'occupied')
    ligands = (
        ('p59', 'p69')
        if name == 'root_order'
        else ('p59',)
        if name == 'occupancy'
        else ('p69',)
    )

    def key(row):
        return (
            row['ligand'],
            row.get('receptor', 'protein_only'),
            row['order'],
            row['seed'],
            row['exhaustiveness'],
        )

    indexed = {key(row): row for row in cells}
    expected = set(itertools.product(ligands, contexts, ORDERS, SEEDS, EFFORTS))
    require(
        len(cells) == len(indexed) == 24 and set(indexed) == expected,
        'Incomplete or duplicate search cells',
    )
    actual = {}
    for run in document['new_runs']:
        parameters = run['result']['protocol_info']['parameters']
        cell = (
            run['ligand'],
            run.get('receptor', 'protein_only'),
            run['order'],
            parameters['seed'],
            parameters['exhaustiveness'],
        )
        require(cell not in actual, 'Duplicate retained result')
        actual[cell] = len(run['result']['poses'])
    require(set(actual) == expected, 'Retained results do not match comparison cells')
    for cell, row in indexed.items():
        require(
            type(row['poses']) is int and 0 < row['poses'] == actual[cell] <= 5,
            'Changed returned-pose count',
        )
        for flag, metric in (
            ('first_recovered', 'first_heavy_rmsd_angstrom'),
            ('returned_set_recovered', 'closest_heavy_rmsd_angstrom'),
        ):
            value = row[metric]
            require(
                type(value) in (int, float)
                and math.isfinite(value)
                and value >= 0
                and type(row[flag]) is bool
                and row[flag] == (value <= 2.5),
                'Invalid recorded recovery',
            )
        for fixed in row.get('fixed_score_lowest', {}).values():
            rmsd = fixed['heavy_rmsd_angstrom']
            require(
                type(rmsd) in (int, float)
                and math.isfinite(rmsd)
                and rmsd >= 0
                and type(fixed['recovered']) is bool
                and fixed['recovered'] == (rmsd <= 2.5),
                'Invalid fixed-score recovery',
            )
    groups = []
    for ligand, context, order in itertools.product(ligands, contexts, ORDERS):
        selected = [
            indexed[ligand, context, order, seed, effort]
            for seed, effort in itertools.product(SEEDS, EFFORTS)
        ]
        groups.append(
            {
                'ligand': ligand,
                'search_receptor': context,
                'order': order,
                'evaluated_runs': 6,
                'returned_poses': sum(row['poses'] for row in selected),
                'first_recovered': sum(row['first_recovered'] for row in selected),
                'any_returned_recovered': sum(
                    row['returned_set_recovered'] for row in selected
                ),
                'recorded_minimum_fixed_recovered': None
                if name == 'root_order'
                else {
                    score_context: sum(
                        row['fixed_score_lowest'][score_context]['recovered']
                        for row in selected
                    )
                    for score_context in ('sham', 'occupied')
                },
            }
        )
    return groups


def project(name, document, previous):
    links = source_links(name, document, previous)
    counts = {
        'original_new_searches': 0,
        'original_returned_poses': 0,
        'original_new_fixed_evaluations': 0,
        'previous_saved_poses_reused': None,
        'previous_fixed_evaluations_reused': None,
    }
    facts = {}
    if name in ('root_order', 'occupancy', 'reciprocal'):
        groups = recovery_groups(name, document)
        counts.update(
            original_new_searches=len(document['new_runs']),
            original_returned_poses=sum(g['returned_poses'] for g in groups),
        )
        facts['search_recovery'] = groups
        if name != 'root_order':
            new_pose_scores = sum(
                len(pair)
                for run in document['new_runs']
                for pair in run['fixed_scores']
            )
            historical_scores = sum(
                len(pair)
                for run in document['historical_serialization_scores']
                for pair in run['fixed_scores']
            )
            counts.update(
                original_new_fixed_evaluations=new_pose_scores + historical_scores,
                previous_saved_poses_reused=sum(
                    len(run['fixed_scores'])
                    for run in document['historical_serialization_scores']
                ),
            )
            facts['fixed_evaluations_on_new_search_poses'] = new_pose_scores
            facts['fixed_serialization_evaluations_on_historical_poses'] = (
                historical_scores
            )
    elif name in ('reference', 'rigid'):
        field = 'references' if name == 'reference' else 'conformers'
        count = sum(
            len(contexts)
            for ligand in document[field].values()
            for contexts in ligand['fixed_scores'].values()
        )
        require(
            document['new_searches'] == 0
            and document['new_fixed_evaluations'] == count == 8,
            'Changed fixed-control population',
        )
        require(
            document['saved_poses_reused'] == 156
            and document['saved_fixed_evaluations_reused']
            == len(document['comparison_rows'])
            == 312,
            'Changed reuse population',
        )
        counts.update(
            original_new_fixed_evaluations=count,
            previous_saved_poses_reused=156,
            previous_fixed_evaluations_reused=312,
        )
        facts['saved_comparison_rows'] = len(document['comparison_rows'])
        facts['saved_cell_summaries'] = len(document['cell_summaries'])
        facts['recorded_root_order_agreement'] = {
            ligand: row['root_order_agrees_at_0_001_kcal_mol']
            for ligand, row in document[field].items()
        }
    elif name == 'contact':
        require(
            document['new_searches'] == document['new_fixed_evaluations'] == 0,
            'Contact stage gained scientific executions',
        )
        require(
            document['distance_matrices'] == 8
            and document['distance_entries'] == 298700,
            'Changed saved distance inventory',
        )
        facts.update(
            distance_matrices=document['distance_matrices'],
            distance_entries=document['distance_entries'],
            strict_thresholds_angstrom=document['strict_thresholds_angstrom'],
            recorded_geometry_flags={
                ligand: {
                    key: row[key]
                    for key in (
                        'protein_prefix_exact',
                        'root_order_exact_on_source_axis',
                    )
                }
                for ligand, row in document['ligands'].items()
            },
        )
    else:
        require(
            name == 'displacement'
            and document['new_searches'] == document['new_optimizations'] == 0,
            'Changed displacement operation',
        )
        require(
            len(document['points']) == 28
            and len(document['offsets_angstrom']) == 7
            and len(document['summaries']) == 16,
            'Incomplete displacement population',
        )
        counts['original_new_fixed_evaluations'] = document['new_fixed_evaluations']
        require(
            document['fresh_zero_anchor_evaluations'] == 16
            and document['new_nonzero_translation_evaluations'] == 96,
            'Changed zero/nonzero populations',
        )
        facts.update(
            constructed_points=28,
            fresh_zero_anchor_evaluations=16,
            nonzero_fixed_evaluations=96,
            offsets_angstrom=document['offsets_angstrom'],
            original_unit_contract=document['unit_contract'],
            saved_summary_rows=[
                {
                    key: row[key]
                    for key in (
                        'ligand',
                        'geometry_arm',
                        'context',
                        'order',
                        'nonzero_offsets_with_strictly_lower_reported_total',
                        'finite_minimum_minus_zero_kcal_mol',
                        'finite_maximum_minus_zero_kcal_mol',
                    )
                }
                for row in document['summaries']
            ],
        )
    require(
        tuple(
            counts[k]
            for k in (
                'original_new_searches',
                'original_returned_poses',
                'original_new_fixed_evaluations',
            )
        )
        == EXPECTED[name],
        f'Changed original operation counts: {name}',
    )
    return {
        'stage': name,
        'original_schema': document['schema'],
        'original_producer': {
            'consumer_base_commit': document['consumer_base_commit'],
            'consumer_source_record_sha256': digest(document['consumer_source_sha256']),
            'qualified_provider_commit': document['qualified_provider_commit'],
            'recorded_versions': document['producer_versions'],
        },
        'dependencies': links,
        'operation_counts': counts,
        'recorded_facts': facts,
    }


def build(data=DATA):
    rows, inputs = [], {}
    for name in INPUTS:
        document, receipt = read_archive(name, data)
        rows.append(project(name, document, inputs))
        inputs[name] = receipt
        del document
    return {
        'schema': 'bindingmt.5x72_control_synthesis@1',
        'owner': 'uibcdf/bindingmt#70',
        'date': '2026-11-05',
        'presentation_producer': {
            'module': 'bmt_test_support/synthesize_5x72_controls.py',
            'sha256': checksum(__file__),
            'scope': 'retrospective saved-record projection; not an original scientific producer',
        },
        'inputs': inputs,
        'stages': rows,
        'score_modes': {
            'docking': {'provider_call': 'Vina.energies', 'unit': 'kilocalorie / mole'},
            'fixed': {'provider_call': 'Vina.score', 'unit': 'kilocalorie / mole'},
        },
        'limits': [
            'No pooled recovery probability or independent-complex count.',
            'Reused geometries/evaluations and equivalent sham trajectories remain dependent.',
            'Original source-proof flags are retained, not reverified or upgraded.',
            'No molecular operation, geometry measurement, search, scoring, optimization or reranking.',
        ],
    }


def tables(record):
    lines = [
        '| Original stage | New searches then | Returned poses then | New fixed evaluations then | Saved poses / fixed evaluations reused |',
        '| --- | ---: | ---: | ---: | --- |',
    ]
    for row in record['stages']:
        c = row['operation_counts']
        reused = ' / '.join(
            '—' if c[k] is None else str(c[k])
            for k in (
                'previous_saved_poses_reused',
                'previous_fixed_evaluations_reused',
            )
        )
        lines.append(
            f'| {row["stage"]} | {c["original_new_searches"]} | {c["original_returned_poses"]} | {c["original_new_fixed_evaluations"]} | {reused} |'
        )
    lines += [
        '',
        'These are original per-stage operations; this synthesis executes none. Dashes denote inapplicable/not separately projected reuse, not missing successes.',
        '',
        '| Stage / ligand / search receptor / ROOT | Runs | Returned poses | First recovered | Any returned recovered | Recorded minimum fixed: sham | Recorded minimum fixed: occupied |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |',
    ]
    for row in record['stages']:
        for g in row['recorded_facts'].get('search_recovery', []):
            fixed = g['recorded_minimum_fixed_recovered']
            lines.append(
                f'| {row["stage"]} / {g["ligand"]} / {g["search_receptor"]} / {g["order"]} | 6 | {g["returned_poses"]} | {g["first_recovered"]}/6 | {g["any_returned_recovered"]}/6 | {str(fixed["sham"]) + "/6" if fixed else "—"} | {str(fixed["occupied"]) + "/6" if fixed else "—"} |'
            )
    return '\n'.join(lines) + '\n'


def verify_outputs(record, output):
    expected = {'summary.json': text_json(record), 'tables.md': tables(record)}
    for name, value in expected.items():
        require((output / name).read_text() == value, f'Stale synthesis output: {name}')
    manifest = json.loads((output / 'manifest.json').read_text())
    require(
        manifest['inputs'] == record['inputs']
        and manifest['presentation_producer'] == record['presentation_producer'],
        'Synthesis provenance mismatch',
    )
    require(set(manifest['files']) == set(expected), 'Incomplete output manifest')
    for name, sha in manifest['files'].items():
        require(checksum(output / name) == sha, f'Output hash mismatch: {name}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, default=DATA)
    parser.add_argument('--output-dir', type=Path, default=OUTPUT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    record = build(args.data_root)
    if not args.check:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, value in {
            'summary.json': text_json(record),
            'tables.md': tables(record),
        }.items():
            (args.output_dir / name).write_text(value)
        manifest = {
            'inputs': record['inputs'],
            'presentation_producer': record['presentation_producer'],
            'files': {
                name: checksum(args.output_dir / name)
                for name in ('summary.json', 'tables.md')
            },
        }
        (args.output_dir / 'manifest.json').write_text(text_json(manifest))
    verify_outputs(record, args.output_dir)
    print(
        'Verified seven historical 5X72 stages; no new molecular/scientific execution or pooled population.'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
