"""Case-specific retrospective reading of frozen 3PTB/5X72 search records.

Only saved numerical observations are read. No scientific runtime is imported.
Figures are rendered only on an explicit write run, using Matplotlib.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'devguide/validation/data'
OUTPUT = DATA / 'saved_search_variability_2026-11-05'
INPUTS = {
    'search': (
        '3ptb_search/audit_2026-10-10.json.gz',
        '97104903c93b3f7a729a5a6ac196cdb7b59d686e318efdcf324f70131abba1f2',
    ),
    'receiving': (
        '3ptb_search/evaluation_2026-10-10.json.gz',
        '8351d4db25b2ad25de413158a8d3dc0a5e4fee31678ea06649994a1832fa53af',
    ),
    'root_order': (
        '5x72_root_order/audit_2026-10-09.json.gz',
        '2129d7eed2b73bcf90737b2a6c722e3b8e9269abeba0ca3b1444df51f046634e',
    ),
}
SEEDS = (7, 42, 2026)
EFFORTS = (1, 8)
ARMS = {
    'registered_3ptb': (
        'rigid/native',
        'rigid/negative',
        'flexible/native',
        'flexible/negative',
    ),
    'root_order_5x72': (
        'p59/native',
        'p59/first_fixed',
        'p69/native',
        'p69/first_fixed',
    ),
}
FIGURES = ('top_n.png', 'top_n.svg', 'effort_differences.png', 'effort_differences.svg')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_json(value):
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n'


def digest(value):
    return hashlib.sha256(text_json(value).encode()).hexdigest()


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def finite(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def load_inputs(data=DATA):
    documents = {}
    for name, (relative, expected) in INPUTS.items():
        payload = (Path(data) / relative).read_bytes()
        require(
            hashlib.sha256(payload).hexdigest() == expected,
            f'Input hash mismatch: {relative}',
        )
        documents[name] = json.loads(gzip.decompress(payload))
    return documents


def protocol(result, requested):
    declaration = result['protocol_info']
    require(declaration['protocol_type'] == 'VinaProtocol', 'Unsupported protocol')
    values = declaration['parameters']
    require(type(values['seed']) is int and values['seed'] in SEEDS, 'Unexpected seed')
    require(
        type(values['exhaustiveness']) is int and values['exhaustiveness'] in EFFORTS,
        'Unexpected effort',
    )
    require(
        values['n_poses'] == requested
        and values['cpu'] == 1
        and values['scoring'] == 'vina',
        'Changed search prescription',
    )
    return declaration


def context(result, reference):
    provenance = result['provenance']
    require(
        provenance['backend'] == 'vina' and provenance['backend_version'] == '1.2.7',
        'Changed backend context',
    )
    artifacts = provenance['backend_artifacts']
    return {
        'backend': provenance['backend'],
        'backend_version': provenance['backend_version'],
        'backend_box': provenance['backend_box'],
        'submitted_input_sha256': {
            role: artifacts[role]['sha256'] for role in ('receptor', 'partner')
        },
        'preparation_sha256': digest(provenance['preparation']),
        'reference_record_sha256': reference,
    }


def run_record(
    population, arm, result, metrics, cutoff, n_atoms, requested, reference, pointers
):
    declaration = protocol(result, requested)
    poses = result['poses']
    require(
        0 < len(poses) == len(metrics) <= requested,
        'Missing or inconsistent pose population',
    )
    observations = []
    for position, (pose, metric) in enumerate(zip(poses, metrics, strict=True), 1):
        rank = pose['rank']
        require(rank is None or type(rank) is int and rank > 0, 'Invalid declared rank')
        require(metric['rank'] == rank, 'Saved metric/result rank mismatch')
        require(finite(metric['rmsd']), 'RMSD must be finite, nonnegative and real')
        require(
            type(metric['recovered']) is bool
            and metric['recovered'] == (metric['rmsd'] <= cutoff),
            'Recovery contradicts saved RMSD',
        )
        observations.append(
            {
                'position': position,
                'rank': rank,
                'pose_id': pose['pose_id'],
                'rmsd_angstrom': metric['rmsd'],
                'recovered': metric['recovered'],
            }
        )
    closest = min(observations, key=lambda row: row['rmsd_angstrom'])
    recovered = next((row for row in observations if row['recovered']), None)
    parameters = declaration['parameters']
    return {
        'population': population,
        'arm': arm,
        'seed': parameters['seed'],
        'exhaustiveness': parameters['exhaustiveness'],
        'protocol': declaration,
        'input_context': context(result, reference),
        'source_pointers': pointers,
        'result_record_sha256': digest(result),
        'criterion': {
            'metric': 'positional_rmsd',
            'unit': 'angstrom',
            'cutoff': cutoff,
            'n_heavy_atoms': n_atoms,
            'alignment': 'none',
            'symmetry_correction': 'none',
            'position_basis': 'saved_result_order',
        },
        'n_requested': requested,
        'n_returned': len(poses),
        'poses': observations,
        'first_rmsd_angstrom': observations[0]['rmsd_angstrom'],
        'closest_rmsd_angstrom': closest['rmsd_angstrom'],
        'closest_position': closest['position'],
        'closest_rank': closest['rank'],
        'first_recovered_position': recovered['position'] if recovered else None,
        'first_recovered_rank': recovered['rank'] if recovered else None,
    }


def read_3ptb(original, received):
    require(
        received['search_archive_sha256'] == INPUTS['search'][1],
        'Receiver bound to another source',
    )
    require(
        received['new_searches_executed'] == 0
        and received['registered_criterion_changed'] is False,
        'Receiving executed or changed the experiment',
    )
    require(
        len(original['runs']) == len(received['runs']) == 24,
        'Incomplete 3PTB population',
    )
    source = {r['index']: (i, r) for i, r in enumerate(original['runs'])}
    require(len(source) == 24, 'Duplicate original run index')
    require(
        len({r['index'] for r in received['runs']}) == 24,
        'Duplicate receiving run index',
    )
    rows = []
    for receiving_index, receipt in enumerate(received['runs']):
        require(receipt['index'] in source, 'Unknown receiving run index')
        source_index, run = source[receipt['index']]
        require(
            run['status'] == receipt['original_status'] == 'evaluation_failed'
            and receipt['status'] == 'evaluated',
            'Changed original/receiving status',
        )
        for key in (
            'arm',
            'domain',
            'protocol',
            'execution_protocol',
            'backend_box',
            'receptor_pdbqt_sha256',
            'partner_pdbqt_sha256',
        ):
            require(
                run[key] == receipt[key], f'Source/receiver association mismatch: {key}'
            )
        result, report = run['result'], receipt['evaluation']['report']
        require(
            result['protocol_info'] == run['execution_protocol'],
            'Executed protocol/result mismatch',
        )
        expected = {
            'metric': 'positional_rmsd',
            'unit': 'angstrom',
            'cutoff': 2.0,
            'comparison': '<=',
            'alignment': 'none',
            'symmetry_correction': 'none',
            'coordinate_frame': 'caller_declared_shared_receptor_frame',
            'atom_scope': 'retained_pose_atoms',
            'atom_correspondence': 'verified_source_atom_keys',
            'top_n_basis': 'result_order',
        }
        require(report['criterion'] == expected, 'Changed 3PTB criterion/unit')
        require(
            report['n_poses'] == len(result['poses']) == len(report['poses']),
            '3PTB pose count mismatch',
        )
        metrics = []
        for position, (pose, metric) in enumerate(
            zip(result['poses'], report['poses'], strict=True), 1
        ):
            require(
                metric['position'] == position and metric['n_atoms'] == 9,
                'Invalid reported position/atom population',
            )
            for key in ('pose_id', 'rank', 'partner_state_id', 'receptor_state_id'):
                require(
                    pose[key] == metric[key], f'3PTB pose association mismatch: {key}'
                )
            metrics.append(
                {
                    'rank': metric['rank'],
                    'rmsd': metric['rmsd'],
                    'recovered': metric['recovered'],
                }
            )
        require(
            report['first_pose'] == report['poses'][0]
            and report['closest_pose']
            == min(report['poses'], key=lambda row: row['rmsd']),
            'Inconsistent saved first/closest summaries',
        )
        row = run_record(
            'registered_3ptb',
            f'{run["arm"]}/{run["domain"]}',
            result,
            metrics,
            2.0,
            9,
            9,
            report['reference']['snapshot_sha256'],
            {
                'search': f'/runs/{source_index}/result',
                'receiving': f'/runs/{receiving_index}/evaluation/report',
                'recorded_run_index': run['index'],
            },
        )
        for role in ('receptor', 'partner'):
            require(
                row['input_context']['submitted_input_sha256'][role]
                == run[f'{role}_pdbqt_sha256'],
                'Submitted input association mismatch',
            )
        for entry in report['top_n']:
            n = entry['requested']
            require(
                type(n) is int
                and n > 0
                and entry['considered'] == min(n, len(metrics)),
                'Invalid saved top-N count',
            )
            require(
                entry['recovered'] == any(p['recovered'] for p in metrics[:n]),
                'Invalid saved top-N recovery',
            )
        rows.append(row)
    return rows


def read_5x72(document):
    expected = {
        'alignment': False,
        'atom_population': '24_experimental_heavy_atoms',
        'cutoff_angstrom': 2.5,
        'metric': 'positional_rmsd',
        'symmetry_correction': False,
    }
    require(document['criterion'] == expected, 'Changed 5X72 criterion/unit')
    require(
        len(document['new_runs']) == len(document['comparison_rows']) == 24,
        'Incomplete 5X72 population',
    )
    comparisons = {
        (r['ligand'], r['order'], r['seed'], r['exhaustiveness']): r
        for r in document['comparison_rows']
    }
    require(len(comparisons) == 24, 'Duplicate comparison cell')
    rows = []
    for index, run in enumerate(document['new_runs']):
        result, metrics = run['result'], run['heavy_atom_metrics']
        parameters = protocol(result, 5)['parameters']
        key = (
            run['ligand'],
            run['order'],
            parameters['seed'],
            parameters['exhaustiveness'],
        )
        require(key in comparisons, 'Unknown 5X72 comparison cell')
        case = document['cases'][run['ligand']]
        normalized = [
            {
                'rank': p['rank'],
                'rmsd': p['heavy_atom_positional_rmsd_angstrom'],
                'recovered': p['recovered'],
            }
            for p in metrics
        ]
        row = run_record(
            'root_order_5x72',
            f'{run["ligand"]}/{run["order"]}',
            result,
            normalized,
            2.5,
            24,
            5,
            digest(case['reference_snapshot']),
            {'root_order': f'/new_runs/{index}', 'comparison_cell': list(key)},
        )
        require(
            row['input_context']['submitted_input_sha256']['partner']
            == case['controls'][run['order']]['sha256'],
            'Changed ROOT-order input association',
        )
        saved = comparisons[key]
        require(
            saved['poses'] == row['n_returned']
            and saved['first_heavy_rmsd_angstrom'] == row['first_rmsd_angstrom']
            and saved['closest_heavy_rmsd_angstrom'] == row['closest_rmsd_angstrom'],
            'Inconsistent 5X72 comparison observations',
        )
        require(
            saved['first_recovered'] == normalized[0]['recovered']
            and saved['returned_set_recovered']
            == any(p['recovered'] for p in normalized),
            'Inconsistent 5X72 comparison recovery',
        )
        rows.append(row)
    return rows


def summarize(rows):
    keyed = {
        (r['population'], r['arm'], r['seed'], r['exhaustiveness']): r for r in rows
    }
    expected = {
        (pop, arm, seed, effort)
        for pop, arms in ARMS.items()
        for arm, seed, effort in itertools.product(arms, SEEDS, EFFORTS)
    }
    require(len(keyed) == len(rows), 'Duplicate run/cell')
    require(set(keyed) == expected, 'Incomplete or unexpected seed/effort cells')
    ordered, groups, pairs = [], [], []
    for population, arms in ARMS.items():
        for arm in arms:
            arm_rows = [
                keyed[population, arm, seed, effort]
                for effort, seed in itertools.product(EFFORTS, SEEDS)
            ]
            baselines = set()
            for row in arm_rows:
                parameters = dict(row['protocol']['parameters'])
                parameters.pop('seed')
                parameters.pop('exhaustiveness')
                baselines.add(
                    digest(
                        {
                            'parameters': parameters,
                            'inputs': row['input_context'],
                            'criterion': row['criterion'],
                        }
                    )
                )
            require(len(baselines) == 1, 'Uncontrolled context variation within an arm')
            ordered.extend(arm_rows)
            for effort in EFFORTS:
                selected = [keyed[population, arm, seed, effort] for seed in SEEDS]
                groups.append(
                    {
                        'population': population,
                        'arm': arm,
                        'exhaustiveness': effort,
                        'seeds': list(SEEDS),
                        'n_evaluated_runs': len(selected),
                        'n_returned_poses': sum(r['n_returned'] for r in selected),
                        'top_n': [
                            {
                                'requested': n,
                                'n_recovered': sum(
                                    any(p['recovered'] for p in r['poses'][:n])
                                    for r in selected
                                ),
                                'n_evaluated_runs': len(selected),
                                'considered_pose_counts': [
                                    min(n, r['n_returned']) for r in selected
                                ],
                            }
                            for n in range(1, selected[0]['n_requested'] + 1)
                        ],
                    }
                )
            for seed in SEEDS:
                low, high = (keyed[population, arm, seed, effort] for effort in EFFORTS)
                pairs.append(
                    {
                        'population': population,
                        'arm': arm,
                        'seed': seed,
                        'comparison': 'effort_8_minus_effort_1',
                        'unit': 'angstrom',
                        'first_rmsd_difference': high['first_rmsd_angstrom']
                        - low['first_rmsd_angstrom'],
                        'closest_rmsd_difference': high['closest_rmsd_angstrom']
                        - low['closest_rmsd_angstrom'],
                        'first_recovered_positions': [
                            low['first_recovered_position'],
                            high['first_recovered_position'],
                        ],
                    }
                )
    return ordered, groups, pairs


def build(documents):
    rows = read_3ptb(documents['search'], documents['receiving']) + read_5x72(
        documents['root_order']
    )
    rows, groups, pairs = summarize(rows)
    require(
        sum(r['n_returned'] for r in rows if r['population'] == 'registered_3ptb')
        == 167,
        'Changed 3PTB returned population',
    )
    require(
        sum(r['n_returned'] for r in rows if r['population'] == 'root_order_5x72')
        == 99,
        'Changed 5X72 returned population',
    )
    producers = {}
    for name, field in (
        ('search', 'original_producer'),
        ('receiving', 'receiving_producer'),
    ):
        source = documents[name][field]
        producers[name] = {
            'consumer_base_commit': source['consumer_base_commit'],
            'driver_sha256': source['consumer_driver_sha256'],
            'qualified_provider_commit': source['qualified_provider_commit'],
            'original_producer_record_sha256': digest(source),
        }
    root = documents['root_order']
    producers['root_order'] = {
        'consumer_base_commit': root['consumer_base_commit'],
        'consumer_source_record_sha256': digest(root['consumer_source_sha256']),
        'qualified_provider_commit': root['qualified_provider_commit'],
    }
    return {
        'schema': 'bindingmt.saved_search_variability@1',
        'owner': 'uibcdf/bindingmt#67',
        'date': '2026-11-05',
        'analysis_producer': {
            'module': 'bmt_test_support/saved_search_variability.py',
            'sha256': checksum(__file__),
            'prescription_source_commit': 'd1435ff8662787afa29798fc0824ac30d9d0c6b6',
        },
        'inputs': {
            k: {'path': path, 'sha256': sha} for k, (path, sha) in INPUTS.items()
        },
        'original_producers': producers,
        'original_3ptb_reporting': {
            'searches': 24,
            'original_evaluation_failures': 24,
            'later_saved_evaluations': 24,
            'new_searches_in_receiving': 0,
        },
        'runs': rows,
        'arm_effort_groups': groups,
        'within_seed_effort_comparisons': pairs,
        'limits': [
            'Retrospective descriptive analysis of two separate frozen campaigns.',
            'Seeds and poses are within-case observations, not independent complexes.',
            'No molecular operation, RMSD recomputation, search, scoring or reranking.',
            'No pooled recovery probability, affinity, significance or general accuracy claim.',
        ],
    }


def run_table(record):
    lines = [
        '| Population / arm | Seed | Effort | Requested / returned | First RMSD (Å) | Closest RMSD (Å) | First recovered position (rank) | Closest position (rank) |',
        '| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |',
    ]

    def identity(position, rank):
        return (
            '—'
            if position is None
            else f'{position} ({rank if rank is not None else "unknown"})'
        )

    for r in record['runs']:
        lines.append(
            f'| {r["population"]} / {r["arm"]} | {r["seed"]} | {r["exhaustiveness"]} | {r["n_requested"]} / {r["n_returned"]} | {r["first_rmsd_angstrom"]:.6f} | {r["closest_rmsd_angstrom"]:.6f} | {identity(r["first_recovered_position"], r["first_recovered_rank"])} | {identity(r["closest_position"], r["closest_rank"])} |'
        )
    return '\n'.join(lines) + '\n'


def render_figures(record, output):
    import matplotlib

    matplotlib.use('Agg')
    from matplotlib import pyplot as plt

    settings = {
        'font.family': 'DejaVu Sans',
        'font.size': 10,
        'svg.hashsalt': 'bindingmt-saved-search-2026-11-05',
    }
    with plt.rc_context(settings):
        for kind in ('top_n', 'effort_differences'):
            fig, axes = plt.subplots(4, 2, figsize=(12, 12))
            for col, (population, arms) in enumerate(ARMS.items()):
                for row, arm in enumerate(arms):
                    ax = axes[row, col]
                    ax.set_title(f'{"3PTB" if col == 0 else "5X72"} · {arm}')
                    ax.grid(alpha=0.2)
                    if kind == 'top_n':
                        for effort, color, marker in (
                            (1, '#0072B2', 'o'),
                            (8, '#D55E00', 's'),
                        ):
                            group = next(
                                g
                                for g in record['arm_effort_groups']
                                if (g['population'], g['arm'], g['exhaustiveness'])
                                == (population, arm, effort)
                            )
                            ax.plot(
                                [g['requested'] for g in group['top_n']],
                                [g['n_recovered'] for g in group['top_n']],
                                marker=marker,
                                color=color,
                                markersize=9 if effort == 1 else 5,
                                markerfacecolor='none' if effort == 1 else color,
                                markeredgewidth=1.5,
                                linestyle='-' if effort == 1 else '--',
                                label=f'Effort {effort}',
                            )
                        ax.set_ylim(-0.1, 3.2)
                        ax.set_yticks(range(4))
                        ax.set_xticks(range(1, 10 if col == 0 else 6))
                        ax.set_xlabel('Returned collection position N')
                        ax.set_ylabel('Recovered saved runs / 3')
                    else:
                        selected = [
                            p
                            for p in record['within_seed_effort_comparisons']
                            if (p['population'], p['arm']) == (population, arm)
                        ]
                        for field, offset, color, marker, label in (
                            (
                                'first_rmsd_difference',
                                -0.04,
                                '#D55E00',
                                'o',
                                'First returned',
                            ),
                            (
                                'closest_rmsd_difference',
                                0.04,
                                '#0072B2',
                                's',
                                'Closest returned',
                            ),
                        ):
                            ax.scatter(
                                [i + offset for i in range(3)],
                                [p[field] for p in selected],
                                color=color,
                                marker=marker,
                                label=label,
                                s=48,
                                zorder=3,
                            )
                        ax.axhline(0, color='#333333', linewidth=0.8)
                        ax.set_xticks(range(3), [str(s) for s in SEEDS])
                        ax.set_xlabel('Recorded seed')
                        ax.set_ylabel('RMSD difference (8 − 1), Å')
            title = (
                'Cumulative recovery in saved returned sets'
                if kind == 'top_n'
                else 'Within-seed differences in saved RMSD'
            )
            fig.suptitle(
                title
                + '\n3PTB: 2 Å / 9 heavy atoms     |     5X72: 2.5 Å / 24 heavy atoms',
                fontsize=14,
            )
            handles, labels = axes[0, 0].get_legend_handles_labels()
            fig.legend(
                handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.025), ncol=2
            )
            fig.text(
                0.5,
                0.008,
                'Retrospective within-case observations; independent panel scales; no pooled success probability.',
                ha='center',
                fontsize=9,
            )
            fig.tight_layout(rect=(0, 0.06, 1, 0.94))
            fig.savefig(
                output / f'{kind}.png',
                dpi=160,
                metadata={'Software': 'BindingMT saved-search analysis #67'},
            )
            fig.savefig(
                output / f'{kind}.svg',
                metadata={
                    'Date': None,
                    'Creator': 'BindingMT saved-search analysis #67',
                },
            )
            svg = output / f'{kind}.svg'
            svg.write_text(
                '\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n'
            )
            plt.close(fig)
    return {'matplotlib': matplotlib.__version__}


def verify_outputs(record, output):
    expected = {'summary.json': text_json(record), 'runs.md': run_table(record)}
    for name, text in expected.items():
        require((output / name).read_text() == text, f'Stale derived output: {name}')
    manifest = json.loads((output / 'artifacts.json').read_text())
    require(
        manifest['inputs'] == record['inputs']
        and manifest['analysis_producer'] == record['analysis_producer'],
        'Artifact provenance mismatch',
    )
    require(
        set(manifest['files']) == set(expected) | set(FIGURES),
        'Incomplete artifact inventory',
    )
    for name, sha in manifest['files'].items():
        require(checksum(output / name) == sha, f'Artifact hash mismatch: {name}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, default=DATA)
    parser.add_argument('--output-dir', type=Path, default=OUTPUT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    record = build(load_inputs(args.data_root))
    if args.check:
        verify_outputs(record, args.output_dir)
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        (args.output_dir / 'summary.json').write_text(text_json(record))
        (args.output_dir / 'runs.md').write_text(run_table(record))
        renderer = render_figures(record, args.output_dir)
        manifest = {
            'inputs': record['inputs'],
            'analysis_producer': record['analysis_producer'],
            'renderer': renderer,
            'files': {
                name: checksum(args.output_dir / name)
                for name in ('summary.json', 'runs.md', *FIGURES)
            },
        }
        (args.output_dir / 'artifacts.json').write_text(text_json(manifest))
        verify_outputs(record, args.output_dir)
    print(
        'Verified 48 saved runs in eight separate arms; original archives unchanged; zero molecular/native operations.'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
