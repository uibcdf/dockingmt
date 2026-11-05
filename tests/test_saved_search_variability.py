"""Frozen numerical observations retain axes, provenance and denominators."""

import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from dmt_test_support import saved_search_variability as analysis


@pytest.fixture(scope='module')
def documents():
    return analysis.load_inputs()


@pytest.fixture(scope='module')
def record(documents):
    return analysis.build(documents)


def test_frozen_populations_and_original_reporting_are_kept_separate(record):
    assert len(record['runs']) == 48
    assert len(record['arm_effort_groups']) == 16
    assert len(record['within_seed_effort_comparisons']) == 24
    assert record['original_3ptb_reporting'] == {
        'searches': 24,
        'original_evaluation_failures': 24,
        'later_saved_evaluations': 24,
        'new_searches_in_receiving': 0,
    }
    for population, poses, atoms, cutoff in (
        ('registered_3ptb', 167, 9, 2.0),
        ('root_order_5x72', 99, 24, 2.5),
    ):
        rows = [r for r in record['runs'] if r['population'] == population]
        assert len(rows) == 24
        assert sum(r['n_returned'] for r in rows) == poses
        assert {r['criterion']['n_heavy_atoms'] for r in rows} == {atoms}
        assert {r['criterion']['cutoff'] for r in rows} == {cutoff}
    assert record['original_producers']['search']['consumer_base_commit'].startswith(
        '105dfc15'
    )
    assert record['original_producers']['root_order'][
        'consumer_base_commit'
    ].startswith('357cd87f')


def test_top_n_retains_finite_run_denominators_and_returned_set_gap(record):
    groups = record['arm_effort_groups']
    for group in groups:
        assert group['n_evaluated_runs'] == 3
        points = group['top_n']
        assert [p['n_recovered'] for p in points] == sorted(
            p['n_recovered'] for p in points
        )
        assert all(p['n_evaluated_runs'] == 3 for p in points)
        assert all(len(p['considered_pose_counts']) == 3 for p in points)
    for arm, recovered in (('p59/native', 3), ('p59/first_fixed', 4)):
        selected = [
            g
            for g in groups
            if g['population'] == 'root_order_5x72' and g['arm'] == arm
        ]
        assert sum(g['top_n'][0]['n_recovered'] for g in selected) == 0
        assert sum(g['top_n'][-1]['n_recovered'] for g in selected) == recovered
    assert any(
        any(
            n < g['top_n'][-1]['requested']
            for n in g['top_n'][-1]['considered_pose_counts']
        )
        for g in groups
    )


def test_receiver_is_joined_by_recorded_index_not_archive_position(documents, record):
    changed = dict(documents)
    changed['receiving'] = dict(documents['receiving'])
    changed['receiving']['runs'] = list(reversed(documents['receiving']['runs']))
    received = analysis.build(changed)
    for expected, actual in zip(record['runs'], received['runs'], strict=True):
        assert {k: v for k, v in expected.items() if k != 'source_pointers'} == {
            k: v for k, v in actual.items() if k != 'source_pointers'
        }


@pytest.mark.parametrize('damage', ['duplicate', 'missing', 'changed_context'])
def test_matrix_does_not_silently_change_or_pool_cells(damage, record):
    rows = copy.deepcopy(record['runs'])
    if damage == 'duplicate':
        rows.append(rows[0])
    elif damage == 'missing':
        rows.pop()
    else:
        rows[0]['protocol']['parameters']['capture_backend_inputs'] = False
    with pytest.raises(ValueError):
        analysis.summarize(rows)


@pytest.mark.parametrize(
    'damage', ['unit', 'source_binding', 'status', 'new_searches', 'position']
)
def test_source_receiver_and_measurement_policy_are_validated(damage, documents):
    changed = copy.deepcopy(documents)
    received = changed['receiving']
    report = received['runs'][0]['evaluation']['report']
    if damage == 'unit':
        report['criterion']['unit'] = 'nanometer'
    elif damage == 'source_binding':
        received['search_archive_sha256'] = '0' * 64
    elif damage == 'status':
        received['runs'][0]['original_status'] = 'evaluated'
    elif damage == 'new_searches':
        received['new_searches_executed'] = 1
    else:
        report['poses'][0]['position'] = 2
    with pytest.raises(ValueError):
        analysis.build(changed)


@pytest.mark.parametrize('invalid', [True, -1.0, float('nan'), float('inf')])
def test_saved_rmsd_requires_finite_nonnegative_real_values(invalid, documents):
    changed = copy.deepcopy(documents)
    changed['root_order']['new_runs'][0]['heavy_atom_metrics'][0][
        'heavy_atom_positional_rmsd_angstrom'
    ] = invalid
    with pytest.raises(ValueError, match='RMSD'):
        analysis.build(changed)


@pytest.mark.parametrize('ranks', [(7, 1), (None, None)])
def test_collection_positions_are_not_inferred_from_scientific_ranks(ranks, documents):
    result = copy.deepcopy(documents['root_order']['new_runs'][0]['result'])
    result['poses'] = result['poses'][:2]
    for pose, rank in zip(result['poses'], ranks, strict=True):
        pose['rank'] = rank
    metrics = [
        {'rank': ranks[0], 'rmsd': 1.0, 'recovered': True},
        {'rank': ranks[1], 'rmsd': 0.5, 'recovered': True},
    ]
    run = analysis.run_record(
        'root_order_5x72', 'p59/native', result, metrics, 2.5, 24, 5, 'reference', {}
    )
    assert run['first_recovered_position'] == 1
    assert run['first_recovered_rank'] == ranks[0]
    assert run['closest_position'] == 2
    assert run['closest_rank'] == ranks[1]


def test_changed_archive_is_refused_before_parsing(tmp_path):
    name, _ = analysis.INPUTS['search']
    target = tmp_path / name
    target.parent.mkdir(parents=True)
    target.write_bytes((analysis.DATA / name).read_bytes() + b'changed')
    with pytest.raises(ValueError, match='hash mismatch'):
        analysis.load_inputs(tmp_path)


def test_derived_output_tampering_is_detected(tmp_path, record):
    shutil.copytree(analysis.OUTPUT, tmp_path, dirs_exist_ok=True)
    manifest = json.loads((tmp_path / 'artifacts.json').read_text())
    assert len(manifest['files']) == 6
    (tmp_path / 'runs.md').write_text('changed')
    with pytest.raises(ValueError, match='Stale derived output'):
        analysis.verify_outputs(record, tmp_path)


def test_reproducer_checks_records_without_scientific_or_plotting_imports(tmp_path):
    script = """
import importlib.abc, runpy, sys
blocked = {'dockingmt','molsysmt','vina','rdkit','openmm','pyunitwizard','numpy','matplotlib'}
class BlockScientific(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            raise AssertionError('Unexpected scientific/plotting import: ' + fullname)
sys.meta_path.insert(0, BlockScientific())
sys.argv = [sys.argv[1], '--check']
runpy.run_path(sys.argv[0], run_name='__main__')
"""
    result = subprocess.run(
        [sys.executable, '-c', script, str(Path(analysis.__file__).resolve())],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert '48 saved runs' in result.stdout
