"""Summarize three frozen evidence populations without molecular operations.

This is a dated, case-specific presentation producer, not a benchmark runner.
Only saved JSON observations are read. Input archives remain unchanged.
"""

import argparse
import gzip
import hashlib
import json
from pathlib import Path

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
    'installed': (
        'installed_3ptb_evaluation/normal_evaluations.json',
        '7949117149a50118e3a3552013338b21598efa460f6b68474ad7ada220d1c675',
    ),
}


def stratum(population, label, samples, cutoff, n_atoms):
    for sample in samples:
        assert sample['first_recovered'] == (sample['first_rmsd'] <= cutoff)
        assert sample['any_recovered'] == (sample['closest_rmsd'] <= cutoff)
        assert sample['closest_rmsd'] <= sample['first_rmsd']
    return {
        'population': population,
        'stratum': label,
        'n_evaluated_results': len(samples),
        'n_returned_poses': sum(s['n_poses'] for s in samples),
        'first_recovered': sum(s['first_recovered'] for s in samples),
        'any_returned_recovered': sum(s['any_recovered'] for s in samples),
        'first_rmsd_range_angstrom': [
            min(s['first_rmsd'] for s in samples),
            max(s['first_rmsd'] for s in samples),
        ],
        'closest_rmsd_range_angstrom': [
            min(s['closest_rmsd'] for s in samples),
            max(s['closest_rmsd'] for s in samples),
        ],
        'criterion': {
            'metric': 'positional_rmsd',
            'cutoff_angstrom': cutoff,
            'n_observed_heavy_atoms': n_atoms,
            'alignment': 'none',
            'symmetry_correction': 'none',
        },
    }


def sample(report):
    assert report['criterion']['unit'] == 'angstrom'
    assert report['n_poses'] == len(report['poses']) and report['n_poses'] > 0
    first = report['poses'][0]
    return {
        'n_poses': report['n_poses'],
        'first_rmsd': first['rmsd'],
        'closest_rmsd': min(p['rmsd'] for p in report['poses']),
        'first_recovered': first['recovered'],
        'any_recovered': any(p['recovered'] for p in report['poses']),
    }


def build(data):
    inputs = {}
    for key, (name, checksum) in INPUTS.items():
        payload = (data / name).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == checksum, name
        inputs[key] = json.loads(
            gzip.decompress(payload) if name.endswith('.gz') else payload
        )
    rows = []
    original, received = inputs['search'], inputs['receiving']
    assert received['search_archive_sha256'] == INPUTS['search'][1]
    assert len(original['runs']) == len(received['runs']) == 24
    assert all(r['status'] == 'evaluation_failed' for r in original['runs'])
    assert all(
        r['status'] == 'evaluated' and r['original_status'] == 'evaluation_failed'
        for r in received['runs']
    )
    for arm in ['rigid', 'flexible']:
        for domain in ['native', 'negative']:
            selected = [
                r for r in received['runs'] if r['arm'] == arm and r['domain'] == domain
            ]
            assert len(selected) == 6
            rows.append(
                stratum(
                    'registered_3ptb',
                    f'{arm}/{domain}',
                    [sample(r['evaluation']['report']) for r in selected],
                    2.0,
                    9,
                )
            )
    root = inputs['root_order']
    assert root['criterion']['cutoff_angstrom'] == 2.5
    assert len(root['new_runs']) == len(root['comparison_rows']) == 24
    for ligand in ['p59', 'p69']:
        for order in ['native', 'first_fixed']:
            selected = [
                r
                for r in root['comparison_rows']
                if r['ligand'] == ligand and r['order'] == order
            ]
            assert len(selected) == 6
            samples = [
                {
                    'n_poses': r['poses'],
                    'first_rmsd': r['first_heavy_rmsd_angstrom'],
                    'closest_rmsd': r['closest_heavy_rmsd_angstrom'],
                    'first_recovered': r['first_recovered'],
                    'any_recovered': r['returned_set_recovered'],
                }
                for r in selected
            ]
            rows.append(
                stratum('root_order_5x72', f'{ligand}/{order}', samples, 2.5, 24)
            )
    assert sum(r['n_returned_poses'] for r in rows[:4]) == 167
    assert sum(r['n_returned_poses'] for r in rows[4:8]) == 99
    for observed, saved in zip(rows[:4], received['summary'], strict=True):
        assert observed['n_evaluated_results'] == saved['evaluated']
        assert observed['n_returned_poses'] == saved['returned_poses']
        assert observed['first_recovered'] == saved['top1_near']
        assert observed['any_returned_recovered'] == saved['any_near']
    for name in ['native', 'displaced']:
        report = inputs['installed'][name]
        assert report['criterion']['cutoff'] == 2.0
        assert report['first_pose']['n_atoms'] == 9
        rows.append(stratum('installed_saved_3ptb', name, [sample(report)], 2.0, 9))
    return {
        'schema': 'dockingmt.scientific_evidence_summary@1',
        'owner': 'uibcdf/dockingmt#29',
        'date': '2026-11-04',
        'inputs': {k: {'path': v[0], 'sha256': v[1]} for k, v in INPUTS.items()},
        'strata': rows,
        'original_3ptb_reporting': {
            'searches_attempted': 24,
            'poses_returned': 167,
            'evaluation_failures': 24,
            'later_saved_evaluations': 24,
            'new_searches_in_receiving': received['new_searches_executed'],
        },
        'limits': [
            'No molecular operations, RMSD recomputation or native execution.',
            'Saved-report consistency is not original scientific validation.',
            'Strata, poses, seeds and repeated 3PTB workflows are not independent complexes.',
            'No pooled recovery rate, affinity or physical-plausibility claim.',
        ],
    }


def table(record):
    lines = [
        '| Population / stratum | Evaluated results | Returned poses | Cutoff / heavy atoms | First recovered | Any returned recovered | First RMSD range (Å) |',
        '| --- | ---: | ---: | --- | ---: | ---: | --- |',
    ]
    for row in record['strata']:
        n = row['n_evaluated_results']
        c = row['criterion']
        lo, hi = row['first_rmsd_range_angstrom']
        lines.append(
            f'| {row["population"]} / {row["stratum"]} | {n} | {row["n_returned_poses"]} | '
            f'{c["cutoff_angstrom"]:g} Å / {c["n_observed_heavy_atoms"]} | '
            f'{row["first_recovered"]}/{n} | {row["any_returned_recovered"]}/{n} | {lo:.4f}–{hi:.4f} |'
        )
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    record = build(directory.parent)
    outputs = {'summary.json': json.dumps(record, indent=2) + '\n'}
    for name, expected in outputs.items():
        path = directory / name
        if args.check:
            assert path.read_text() == expected, f'Stale evidence presentation: {name}'
        else:
            path.write_text(expected)
    overview = directory.parent.parent / 'scientific_evidence_overview_2026-11-04.md'
    start, end = '<!-- BEGIN FROZEN TABLE -->', '<!-- END FROZEN TABLE -->'
    text = overview.read_text()
    prefix, rest = text.split(start)
    existing, suffix = rest.split(end)
    expected = '\n\n' + table(record) + '\n'
    if args.check:
        assert existing == expected, 'Stale scientific overview table'
    else:
        overview.write_text(prefix + start + expected + end + suffix)
    print(
        'Frozen records verified; ten separate strata; zero molecular/native operations.'
    )


if __name__ == '__main__':
    main()
