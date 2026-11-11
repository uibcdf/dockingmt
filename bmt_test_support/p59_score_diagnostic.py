"""Retrospective P59 scalar-score diagnosis over authenticated saved records.

No molecular runtime is imported. Explicit write runs additionally use Matplotlib.
The previous #67 projection supplies RMSD only after binding it to original bytes.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import itertools
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'devguide/validation/data'
OUTPUT = DATA / 'p59_score_diagnostic_2026-11-05'
INPUTS = {
    'archive': (
        '5x72_root_order/audit_2026-10-09.json.gz',
        '2129d7eed2b73bcf90737b2a6c722e3b8e9269abeba0ca3b1444df51f046634e',
    ),
    'projection': (
        'saved_search_variability_2026-11-05/frozen_20261105_summary.json',
        '0d88030650a768c14e9940b2c58dd21c16465550518cedd5f64c557e3e7369fc',
    ),
}
PRIOR_IDENTITY_SHA = '05df8f441795110375326a50cd0138cf84dac2e119175d51a3d97981ee387b84'
PRIOR_MODULE_SHA = '91ef4d7a591ff0d9904d5d26be93e9b1bad6116bbeba004325ea3974664064a5'
SEEDS = (7, 42, 2026)
EFFORTS = (1, 8)
ORDERS = ('native', 'first_fixed')
SCORE = {
    'schema_version': '1.0',
    'kind': 'empirical',
    'component': 'total docking score',
    'method': 'AutoDock Vina/vina',
    'method_version': '1.2.7',
    'unit': 'kilocalorie / mole',
    'preferred_direction': 'lower',
}
CRITERION = {
    'metric': 'positional_rmsd',
    'unit': 'angstrom',
    'cutoff': 2.5,
    'n_heavy_atoms': 24,
    'alignment': 'none',
    'symmetry_correction': 'none',
    'position_basis': 'saved_result_order',
}
FIGURES = ('score_rmsd.png', 'score_rmsd.svg')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_json(value):
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n'


def record_digest(value):
    # Exact canonical representation used by the frozen #67 numerical projection.
    return hashlib.sha256(text_json(value).encode()).hexdigest()


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def real(value):
    return type(value) in (int, float) and math.isfinite(value)


def load_inputs(data=DATA):
    documents = {}
    for name, (relative, sha) in INPUTS.items():
        payload = (Path(data) / relative).read_bytes()
        require(
            hashlib.sha256(payload).hexdigest() == sha,
            f'Input hash mismatch: {relative}',
        )
        documents[name] = json.loads(
            gzip.decompress(payload) if relative.endswith('.gz') else payload
        )
    return documents['archive'], documents['projection']


def run_key(run):
    parameters = run['result']['protocol_info']['parameters']
    return (
        f'{run["ligand"]}/{run["order"]}',
        parameters['seed'],
        parameters['exhaustiveness'],
    )


def describe_run(run, numerical, archive_index, projection_index):
    result = run['result']
    require(
        record_digest(result) == numerical['result_record_sha256'],
        'Original result/projection digest mismatch',
    )
    require(numerical['criterion'] == CRITERION, 'Changed RMSD criterion/unit')
    require(
        result['protocol_info'] == numerical['protocol'], 'Protocol/projection mismatch'
    )
    require(
        numerical['n_requested']
        == result['protocol_info']['parameters']['n_poses']
        == 5,
        'Changed requested count',
    )
    poses, metrics = result['poses'], run['heavy_atom_metrics']
    require(
        0
        < len(poses)
        == len(metrics)
        == len(numerical['poses'])
        == numerical['n_returned']
        <= 5,
        'Missing or inconsistent pose count',
    )
    provenance = result['provenance']
    require(
        provenance['ranking_policy'] == {'score_name': 'vina', 'ascending': True},
        'Changed ranking policy',
    )
    history = provenance['ranking_history']
    require(len(history) == 1, 'Unsupported ranking history')
    event = history[0]
    require(
        event['origin'] == 'backend'
        and event['evidence'] == 'recorded'
        and event['score_name'] == 'vina'
        and event['ascending'] is True
        and event['output_order'] == list(range(len(poses))),
        'Changed ranking evidence',
    )
    definition = poses[0]['metadata']['score_definitions']['vina']
    require(
        {k: v for k, v in definition.items() if k != 'context'} == SCORE,
        'Changed score definition/unit/direction',
    )
    require(
        event['score_definition'] == definition, 'Ranking score definition mismatch'
    )
    context = definition['context']
    backend_box = numerical['input_context']['backend_box']
    require(
        backend_box['rounding_decimals'] == 6
        and context['backend_box']
        == {key: backend_box[key] for key in ('center', 'size', 'unit')},
        'Changed score box context',
    )
    for role in ('receptor', 'partner'):
        require(
            context[f'{role}_sha256']
            == numerical['input_context']['submitted_input_sha256'][role],
            'Changed score input context',
        )
    require(context['stage'] == 'docking', 'Changed score stage')
    points = []
    for position, (pose, metric, saved) in enumerate(
        zip(poses, metrics, numerical['poses'], strict=True), 1
    ):
        require(
            saved['position'] == position
            and saved['pose_id'] == pose['pose_id']
            and saved['rank'] == pose['rank'] == metric['rank'],
            'Pose position/identity/rank mismatch',
        )
        require(
            pose['rank'] is None or type(pose['rank']) is int and pose['rank'] > 0,
            'Invalid declared rank',
        )
        require(
            pose['metadata']['score_definitions']['vina'] == definition,
            'Inconsistent per-pose score context',
        )
        score = pose['scores'].get('vina')
        rmsd = saved['rmsd_angstrom']
        require(real(score), 'Score must be finite and real')
        require(
            real(rmsd)
            and rmsd >= 0
            and rmsd == metric['heavy_atom_positional_rmsd_angstrom'],
            'Invalid or mismatched saved RMSD',
        )
        require(
            type(saved['recovered']) is bool
            and type(metric['recovered']) is bool
            and saved['recovered'] == metric['recovered'] == (rmsd <= 2.5),
            'Recovery contradicts saved RMSD',
        )
        points.append(
            {
                'position': position,
                'rank': pose['rank'],
                'pose_id': pose['pose_id'],
                'vina_score': score,
                'rmsd_angstrom': rmsd,
                'recovered': saved['recovered'],
            }
        )
    require(
        event['input_order']
        == [
            {
                key: pose[key]
                for key in ('pose_id', 'rank', 'partner_state_id', 'receptor_state_id')
            }
            | {'value': point['vina_score']}
            for pose, point in zip(poses, points, strict=True)
        ],
        'Ranking values/pose association mismatch',
    )
    first = points[0]
    for point in points:
        point['score_difference_from_first'] = point['vina_score'] - first['vina_score']
    closest_rmsd = min(p['rmsd_angstrom'] for p in points)
    closest = next(p for p in points if p['rmsd_angstrom'] == closest_rmsd)
    recovered = [p for p in points if p['recovered']]
    lowest_recovered = min((p['vina_score'] for p in recovered), default=None)
    minimum_score = min(p['vina_score'] for p in points)
    return {
        'arm': numerical['arm'],
        'seed': numerical['seed'],
        'exhaustiveness': numerical['exhaustiveness'],
        'n_requested': 5,
        'n_returned': len(points),
        'criterion': CRITERION,
        'protocol': numerical['protocol'],
        'input_context': numerical['input_context'],
        'score_definition': definition,
        'ranking_policy': provenance['ranking_policy'],
        'ranking_history': history,
        'source_pointers': {
            'archive': f'/new_runs/{archive_index}',
            'projection': f'/runs/{projection_index}',
        },
        'original_result_sha256': numerical['result_record_sha256'],
        'projection_row_sha256': record_digest(numerical),
        'poses': points,
        'first': first,
        'closest': closest,
        'closest_rmsd_tied_positions': [
            p['position'] for p in points if p['rmsd_angstrom'] == closest_rmsd
        ],
        'earliest_recovered': recovered[0] if recovered else None,
        'lowest_recovered_score': lowest_recovered,
        'lowest_recovered_score_positions': [
            p['position'] for p in recovered if p['vina_score'] == lowest_recovered
        ],
        'closest_score_difference_from_first': closest['vina_score']
        - first['vina_score'],
        'recovered_score_difference_from_first': None
        if lowest_recovered is None
        else lowest_recovered - first['vina_score'],
        'minimum_score_positions': [
            p['position'] for p in points if p['vina_score'] == minimum_score
        ],
        'first_is_score_minimum': first['vina_score'] == minimum_score,
        'scores_nondecreasing': all(
            a['vina_score'] <= b['vina_score'] for a, b in zip(points, points[1:])
        ),
    }


def build(archive, projection):
    require(
        record_digest({key: projection[key] for key in ('schema', 'analysis_producer')})
        == PRIOR_IDENTITY_SHA
        and projection['analysis_producer']['sha256'] == PRIOR_MODULE_SHA,
        'Changed prior projection identity',
    )
    require(
        projection['inputs']['root_order']['sha256'] == INPUTS['archive'][1],
        'Projection bound to another archive',
    )
    require(
        archive['criterion']
        == {
            'alignment': False,
            'atom_population': '24_experimental_heavy_atoms',
            'cutoff_angstrom': 2.5,
            'metric': 'positional_rmsd',
            'symmetry_correction': False,
        },
        'Changed original RMSD criterion',
    )
    selected = [
        (i, r)
        for i, r in enumerate(projection['runs'])
        if r['population'] == 'root_order_5x72'
    ]
    projected = {
        (r['arm'], r['seed'], r['exhaustiveness']): (i, r) for i, r in selected
    }
    originals = {run_key(r): (i, r) for i, r in enumerate(archive['new_runs'])}
    expected = {
        (f'{ligand}/{order}', seed, effort)
        for ligand, order, seed, effort in itertools.product(
            ('p59', 'p69'), ORDERS, SEEDS, EFFORTS
        )
    }
    require(
        len(archive['new_runs'])
        == len(originals)
        == len(selected)
        == len(projected)
        == 24
        and set(originals) == set(projected) == expected,
        'Incomplete or duplicate archive/projection cells',
    )
    for key, (_, run) in originals.items():
        require(
            record_digest(run['result']) == projected[key][1]['result_record_sha256'],
            'Original result/projection digest mismatch',
        )
    rows = []
    for order, effort, seed in itertools.product(ORDERS, EFFORTS, SEEDS):
        key = f'p59/{order}', seed, effort
        index, run = originals[key]
        pindex, numerical = projected[key]
        rows.append(describe_run(run, numerical, index, pindex))
    require(
        sum(r['n_returned'] for r in rows) == 50, 'Changed selected P59 pose population'
    )
    for order in ORDERS:
        arm_rows = [r for r in rows if r['arm'] == f'p59/{order}']
        require(
            len(
                {
                    record_digest(
                        {'score': r['score_definition'], 'inputs': r['input_context']}
                    )
                    for r in arm_rows
                }
            )
            == 1,
            'Uncontrolled score/input context variation within a ROOT arm',
        )
    producer = projection['original_producers']['root_order']
    require(
        producer['consumer_base_commit'] == archive['consumer_base_commit']
        and producer['consumer_source_record_sha256']
        == record_digest(archive['consumer_source_sha256']),
        'Original producer association mismatch',
    )
    require(
        producer['qualified_provider_commit'] == archive['qualified_provider_commit'],
        'Original provider association mismatch',
    )
    return {
        'schema': 'bindingmt.p59_score_diagnostic@1',
        'owner': 'uibcdf/bindingmt#69',
        'date': '2026-11-05',
        'analysis_producer': {
            'module': 'bmt_test_support/p59_score_diagnostic.py',
            'sha256': checksum(__file__),
            'prescription_commit': '414ff0e4e0a3932261b7eeb36c10594deb4ba4f9',
        },
        'inputs': {
            k: {'path': path, 'sha256': sha} for k, (path, sha) in INPUTS.items()
        },
        'prior_analysis_producer': projection['analysis_producer'],
        'original_producer': producer,
        'population': {
            'archive_runs': 24,
            'selected_runs': 12,
            'selected_poses': 50,
            'nonselected_p69_runs': 12,
        },
        'runs': rows,
        'limits': [
            'Retrospective within-case description; poses/seeds are not independent complexes.',
            'Only saved total scores and RMSDs; no molecular operation, scoring, search or reranking.',
            'No pooled correlation, significance, affinity, causal or general scoring-accuracy claim.',
        ],
    }


def run_table(record):
    lines = [
        '| ROOT / seed / effort | Requested / returned | First score (kcal/mol) | First RMSD (Å) | Closest position (rank) | Closest RMSD (Å) | Closest score − first (kcal/mol) | Earliest recovered position | Lowest recovered score − first (kcal/mol) |',
        '| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |',
    ]
    for r in record['runs']:
        c, e = r['closest'], r['earliest_recovered']
        gap = r['recovered_score_difference_from_first']
        lines.append(
            f'| {r["arm"]} / {r["seed"]} / {r["exhaustiveness"]} | 5 / {r["n_returned"]} | {r["first"]["vina_score"]:.3f} | {r["first"]["rmsd_angstrom"]:.6f} | {c["position"]} ({c["rank"] if c["rank"] is not None else "unknown"}) | {c["rmsd_angstrom"]:.6f} | {r["closest_score_difference_from_first"]:+.3f} | {e["position"] if e else "—"} | {f"{gap:+.3f}" if gap is not None else "—"} |'
        )
    return '\n'.join(lines) + '\n'


def pose_csv(record):
    stream = io.StringIO(newline='')
    fields = [
        'arm',
        'seed',
        'exhaustiveness',
        'position',
        'rank',
        'pose_id',
        'vina_score',
        'score_difference_from_first',
        'rmsd_angstrom',
        'recovered',
        'score_name',
        'score_unit',
        'rmsd_unit',
    ]
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    for run in record['runs']:
        for pose in run['poses']:
            writer.writerow(
                {k: run[k] for k in ('arm', 'seed', 'exhaustiveness')}
                | pose
                | {
                    'score_name': 'vina',
                    'score_unit': run['score_definition']['unit'],
                    'rmsd_unit': run['criterion']['unit'],
                }
            )
    return stream.getvalue()


def render_figure(record, output):
    import matplotlib

    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    with plt.rc_context(
        {
            'font.family': 'DejaVu Sans',
            'font.size': 9,
            'svg.hashsalt': 'bindingmt-p59-score-69',
        }
    ):
        fig, axes = plt.subplots(3, 4, figsize=(16, 11))
        rows = {(r['arm'], r['seed'], r['exhaustiveness']): r for r in record['runs']}
        for row, seed in enumerate(SEEDS):
            for column, (order, effort) in enumerate(
                itertools.product(ORDERS, EFFORTS)
            ):
                ax = axes[row, column]
                run = rows[f'p59/{order}', seed, effort]
                for point in run['poses']:
                    ax.scatter(
                        point['vina_score'],
                        point['rmsd_angstrom'],
                        color='#007f86' if point['recovered'] else '#be6400',
                        marker='o' if point['recovered'] else 'x',
                        s=38,
                    )
                    offsets = [(5, 6), (5, -11), (5, 7), (-12, 7), (5, -12)]
                    ax.annotate(
                        str(point['position']),
                        (point['vina_score'], point['rmsd_angstrom']),
                        xytext=offsets[point['position'] - 1],
                        textcoords='offset points',
                        fontsize=8,
                    )
                ax.axhline(2.5, color='0.45', linestyle='--', linewidth=1)
                ax.set_title(
                    f'{order.replace("_", "-")} · effort {effort} · seed {seed}\n{run["n_returned"]}/5 returned poses'
                )
                ax.set_xlabel('Saved Vina total score (kcal/mol)')
                ax.set_ylabel('Saved positional RMSD (Å)')
                ax.margins(x=0.15, y=0.15)
                ax.grid(alpha=0.15)
        fig.suptitle(
            'P59: recorded total-score preference and positional recovery', fontsize=16
        )
        fig.legend(
            handles=[
                Line2D(
                    [],
                    [],
                    marker='o',
                    linestyle='none',
                    color='#007f86',
                    label='Recovered (≤ 2.5 Å)',
                ),
                Line2D(
                    [],
                    [],
                    marker='x',
                    linestyle='none',
                    color='#be6400',
                    label='Not recovered',
                ),
            ],
            loc='lower center',
            bbox_to_anchor=(0.5, 0.025),
            ncol=2,
        )
        fig.text(
            0.5,
            0.01,
            'Labels are saved collection positions; panels have independent scales; poses/seeds are not independent complexes.',
            ha='center',
        )
        fig.tight_layout(rect=(0, 0.07, 1, 0.95))
        fig.savefig(
            output / 'score_rmsd.png',
            dpi=160,
            metadata={'Software': 'BindingMT P59 score diagnostic #69'},
        )
        fig.savefig(
            output / 'score_rmsd.svg',
            metadata={'Date': None, 'Creator': 'BindingMT P59 score diagnostic #69'},
        )
        svg = output / 'score_rmsd.svg'
        svg.write_text(
            '\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n'
        )
        plt.close(fig)
    return {'matplotlib': matplotlib.__version__}


def text_outputs(record):
    return {
        'summary.json': text_json(record),
        'runs.md': run_table(record),
        'poses.csv': pose_csv(record),
    }


def verify_outputs(record, output):
    expected = text_outputs(record)
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
    record = build(*load_inputs(args.data_root))
    if not args.check:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, text in text_outputs(record).items():
            (args.output_dir / name).write_text(text)
        renderer = render_figure(record, args.output_dir)
        manifest = {
            'inputs': record['inputs'],
            'analysis_producer': record['analysis_producer'],
            'renderer': renderer,
            'files': {
                name: checksum(args.output_dir / name)
                for name in (*text_outputs(record), *FIGURES)
            },
        }
        (args.output_dir / 'artifacts.json').write_text(text_json(manifest))
    verify_outputs(record, args.output_dir)
    print(
        'Verified 12 P59 runs / 50 saved poses; no molecular operation, scoring, search or reranking.'
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
