"""Saved total scores stay attached to their original pose/RMSD and definitions."""

import copy
import csv
import io
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from bmt_test_support import p59_score_diagnostic as analysis


@pytest.fixture(scope='module')
def documents():
    return analysis.load_inputs()


@pytest.fixture(scope='module')
def record(documents):
    return analysis.build(*documents)


@pytest.fixture
def pair(documents):
    archive, projection = documents
    run = next(
        r for r in archive['new_runs'] if analysis.run_key(r) == ('p59/native', 7, 1)
    )
    row = next(
        r
        for r in projection['runs']
        if r['population'] == 'root_order_5x72'
        and (r['arm'], r['seed'], r['exhaustiveness']) == ('p59/native', 7, 1)
    )
    return copy.deepcopy(run), copy.deepcopy(row)


def reseal(run, row):
    """Bind intentionally synthetic observations without weakening frozen-input tests."""
    result = run['result']
    event = result['provenance']['ranking_history'][0]
    event['input_order'] = [
        {k: p[k] for k in ('pose_id', 'rank', 'partner_state_id', 'receptor_state_id')}
        | {'value': p['scores'].get('vina')}
        for p in result['poses']
    ]
    event['output_order'] = list(range(len(result['poses'])))
    row['n_returned'] = len(result['poses'])
    row['result_record_sha256'] = analysis.record_digest(result)


def synthetic(pair, scores, rmsds, ranks):
    run, row = pair
    result = run['result']
    result['poses'] = result['poses'][:2]
    run['heavy_atom_metrics'] = run['heavy_atom_metrics'][:2]
    row['poses'] = row['poses'][:2]
    for i, (score, rmsd, rank) in enumerate(zip(scores, rmsds, ranks, strict=True)):
        result['poses'][i]['scores']['vina'] = score
        result['poses'][i]['rank'] = rank
        run['heavy_atom_metrics'][i].update(
            rank=rank, heavy_atom_positional_rmsd_angstrom=rmsd, recovered=rmsd <= 2.5
        )
        row['poses'][i].update(rank=rank, rmsd_angstrom=rmsd, recovered=rmsd <= 2.5)
    reseal(run, row)
    return analysis.describe_run(run, row, 0, 0)


def test_frozen_selection_and_original_producers_remain_explicit(record):
    assert record['population'] == {
        'archive_runs': 24,
        'selected_runs': 12,
        'selected_poses': 50,
        'nonselected_p69_runs': 12,
    }
    assert {r['arm'] for r in record['runs']} == {'p59/native', 'p59/first_fixed'}
    assert all(
        r['n_requested'] == 5 and r['criterion'] == analysis.CRITERION
        for r in record['runs']
    )
    assert record['original_producer']['consumer_base_commit'].startswith('357cd87f')
    assert record['prior_analysis_producer']['sha256'] == analysis.PRIOR_MODULE_SHA
    rows = list(csv.DictReader(io.StringIO(analysis.pose_csv(record))))
    assert len(rows) == 50
    assert {r['score_unit'] for r in rows} == {'kilocalorie / mole'}
    assert {r['rmsd_unit'] for r in rows} == {'angstrom'}
    assert {r['score_name'] for r in rows} == {'vina'}


def test_observed_score_preferences_and_known_within_run_gaps(record):
    assert all(
        r['scores_nondecreasing'] and r['first_is_score_minimum']
        for r in record['runs']
    )
    native = [
        r
        for r in record['runs']
        if r['arm'] == 'p59/native' and r['exhaustiveness'] == 8
    ]
    assert [
        r['recovered_score_difference_from_first'] for r in native
    ] == pytest.approx([0.472, 0.523, 0.480])
    fixed = next(
        r
        for r in record['runs']
        if (r['arm'], r['seed'], r['exhaustiveness']) == ('p59/first_fixed', 42, 1)
    )
    assert fixed['recovered_score_difference_from_first'] == pytest.approx(0.535)
    assert fixed['earliest_recovered']['position'] == 3
    assert all(
        r['recovered_score_difference_from_first'] is None
        for r in record['runs']
        if r['earliest_recovered'] is None
    )


def test_join_uses_run_keys_when_archive_and_projection_order_change(documents, record):
    archive, projection = copy.deepcopy(documents)
    archive['new_runs'].reverse()
    projection['runs'].reverse()
    received = analysis.build(archive, projection)
    for expected, actual in zip(record['runs'], received['runs'], strict=True):
        assert {k: v for k, v in expected.items() if k != 'source_pointers'} == {
            k: v for k, v in actual.items() if k != 'source_pointers'
        }


@pytest.mark.parametrize(
    'damage',
    ['missing', 'duplicate', 'result_digest', 'archive_binding', 'schema', 'producer'],
)
def test_incomplete_or_unbound_records_are_not_silently_selected(damage, documents):
    archive, projection = copy.deepcopy(documents)
    if damage == 'missing':
        archive['new_runs'].pop()
    elif damage == 'duplicate':
        archive['new_runs'][0] = copy.deepcopy(archive['new_runs'][1])
    elif damage == 'result_digest':
        archive['new_runs'][0]['result']['poses'][0]['scores']['vina'] += 1.0
    elif damage == 'schema':
        projection['schema'] = 'unrecognized.saved_search_variability@1'
    elif damage == 'producer':
        projection['analysis_producer']['module'] = 'another_producer.py'
    else:
        projection['inputs']['root_order']['sha256'] = '0' * 64
    with pytest.raises(ValueError):
        analysis.build(archive, projection)


@pytest.mark.parametrize(
    'field,value',
    [
        ('unit', 'kilojoule / mole'),
        ('preferred_direction', 'higher'),
        ('method_version', 'unknown'),
    ],
)
def test_score_definition_is_not_reinterpreted(field, value, pair):
    run, row = pair
    for pose in run['result']['poses']:
        pose['metadata']['score_definitions']['vina'][field] = value
    run['result']['provenance']['ranking_history'][0]['score_definition'][field] = value
    reseal(run, row)
    with pytest.raises(ValueError, match='score definition'):
        analysis.describe_run(run, row, 0, 0)


@pytest.mark.parametrize('value', [True, '-10.0', float('nan'), float('inf')])
def test_scores_require_finite_real_numbers(value, pair):
    run, row = pair
    run['result']['poses'][0]['scores']['vina'] = value
    with pytest.raises(ValueError):
        # Nonfinite values are already refused by the canonical digest encoder.
        reseal(run, row)
        analysis.describe_run(run, row, 0, 0)


@pytest.mark.parametrize(
    'damage', ['position', 'pose_id', 'rank', 'rmsd', 'recovery', 'criterion']
)
def test_score_rmsd_associations_and_criterion_are_verified(damage, pair):
    run, row = pair
    if damage == 'criterion':
        row['criterion']['cutoff'] = 3.0
    elif damage == 'position':
        row['poses'][0]['position'] = 2
    elif damage == 'pose_id':
        row['poses'][0]['pose_id'] = 'other'
    elif damage == 'rank':
        row['poses'][0]['rank'] = 2
    elif damage == 'rmsd':
        row['poses'][0]['rmsd_angstrom'] += 1.0
    else:
        row['poses'][0]['recovered'] = not row['poses'][0]['recovered']
    with pytest.raises(ValueError):
        analysis.describe_run(run, row, 0, 0)


def test_inconsistent_pose_score_context_is_refused(pair):
    run, row = pair
    run['result']['poses'][-1]['metadata']['score_definitions']['vina']['context'][
        'partner_sha256'
    ] = '0' * 64
    reseal(run, row)
    with pytest.raises(ValueError, match='per-pose score context'):
        analysis.describe_run(run, row, 0, 0)


@pytest.mark.parametrize('ranks', [(7, 1), (None, None)])
def test_ties_keep_all_positions_and_earliest_observation_without_inferred_rank(
    ranks, pair
):
    r = synthetic(pair, [-5.0, -5.0], [1.0, 1.0], ranks)
    assert r['minimum_score_positions'] == [1, 2]
    assert r['closest_rmsd_tied_positions'] == [1, 2]
    assert r['lowest_recovered_score_positions'] == [1, 2]
    assert r['closest']['position'] == r['earliest_recovered']['position'] == 1
    assert r['closest']['rank'] == ranks[0]
    assert r['recovered_score_difference_from_first'] == 0.0


def test_ordering_discordance_is_retained_without_reranking(pair):
    r = synthetic(pair, [-5.0, -6.0], [6.0, 1.0], (7, 1))
    assert not r['scores_nondecreasing'] and not r['first_is_score_minimum']
    assert [p['rank'] for p in r['poses']] == [7, 1]
    assert [p['vina_score'] for p in r['poses']] == [-5.0, -6.0]
    assert r['recovered_score_difference_from_first'] == -1.0


def test_absent_recovery_is_not_a_zero_score_contrast(pair):
    r = synthetic(pair, [-5.0, -4.0], [6.0, 7.0], (1, 2))
    assert r['earliest_recovered'] is None
    assert r['lowest_recovered_score'] is None
    assert r['recovered_score_difference_from_first'] is None
    assert r['lowest_recovered_score_positions'] == []


def test_changed_input_is_rejected_before_parsing(tmp_path):
    name, _ = analysis.INPUTS['archive']
    path = tmp_path / name
    path.parent.mkdir(parents=True)
    path.write_bytes(b'not an authorized archive')
    with pytest.raises(ValueError, match='hash mismatch'):
        analysis.load_inputs(tmp_path)


@pytest.mark.parametrize('name', ['poses.csv', 'score_rmsd.png'])
def test_output_tampering_is_detected(name, tmp_path, record):
    shutil.copytree(analysis.OUTPUT, tmp_path, dirs_exist_ok=True)
    (tmp_path / name).write_text('changed')
    with pytest.raises(ValueError):
        analysis.verify_outputs(record, tmp_path)


def test_check_mode_needs_no_molecular_or_plotting_imports(tmp_path):
    script = """
import importlib.abc, runpy, sys
class BlockScientific(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'bindingmt','molsysmt','vina','rdkit','openmm','pyunitwizard','numpy','matplotlib'}:
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
    assert '12 P59 runs / 50 saved poses' in result.stdout
