"""Historical controls keep distinct operations, contexts and source-proof scope."""

import copy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from dmt_test_support import synthesize_5x72_controls as synthesis


@pytest.fixture(scope='module')
def record():
    return synthesis.build()


@pytest.fixture(scope='module')
def original():
    return synthesis.read_archive('root_order')[0]


def test_all_seven_producers_and_original_operation_populations_remain_separate(record):
    assert [r['stage'] for r in record['stages']] == list(synthesis.INPUTS)
    assert (
        len({r['original_producer']['consumer_base_commit'] for r in record['stages']})
        == 7
    )
    assert [
        tuple(
            r['operation_counts'][k]
            for k in (
                'original_new_searches',
                'original_returned_poses',
                'original_new_fixed_evaluations',
            )
        )
        for r in record['stages']
    ] == [
        (24, 99, 0),
        (24, 78, 256),
        (24, 78, 254),
        (0, 0, 8),
        (0, 0, 8),
        (0, 0, 0),
        (0, 0, 112),
    ]
    assert 'total_recovery' not in record and 'independent_complexes' not in record
    assert record['score_modes']['docking']['provider_call'] == 'Vina.energies'
    assert record['score_modes']['fixed']['provider_call'] == 'Vina.score'


def test_reused_poses_and_evaluations_are_not_new_searches(record):
    stages = {r['stage']: r for r in record['stages']}
    for name in ('reference', 'rigid'):
        counts = stages[name]['operation_counts']
        assert counts['original_new_searches'] == counts['original_returned_poses'] == 0
        assert counts['previous_saved_poses_reused'] == 156
        assert counts['previous_fixed_evaluations_reused'] == 312
    assert stages['occupancy']['operation_counts']['previous_saved_poses_reused'] == 50
    assert stages['reciprocal']['operation_counts']['previous_saved_poses_reused'] == 49
    assert stages['contact']['recorded_facts']['distance_matrices'] == 8
    assert stages['contact']['recorded_facts']['distance_entries'] == 298700
    assert (
        stages['displacement']['recorded_facts']['fresh_zero_anchor_evaluations'] == 16
    )
    assert stages['displacement']['recorded_facts']['nonzero_fixed_evaluations'] == 96


def test_occupancy_and_reciprocal_keep_both_root_arms_and_adverse_outcomes(record):
    stages = {r['stage']: r for r in record['stages']}
    p59 = stages['occupancy']['recorded_facts']['search_recovery']
    p69 = stages['reciprocal']['recorded_facts']['search_recovery']
    assert [r['evaluated_runs'] for r in p59 + p69] == [6] * 8
    assert [r['first_recovered'] for r in p59] == [0, 0, 5, 5]
    assert [r['any_returned_recovered'] for r in p59] == [3, 4, 5, 5]
    assert [r['recorded_minimum_fixed_recovered']['occupied'] for r in p59] == [
        3,
        4,
        5,
        5,
    ]
    assert [r['first_recovered'] for r in p69] == [0, 0, 0, 0]
    assert [r['any_returned_recovered'] for r in p69] == [0, 0, 4, 3]
    assert [r['recorded_minimum_fixed_recovered']['occupied'] for r in p69] == [0] * 4
    assert all(
        r['recorded_minimum_fixed_recovered'] is None
        for r in stages['root_order']['recorded_facts']['search_recovery']
    )


def test_original_false_proof_flags_are_preserved_without_requalification(record):
    stages = {r['stage']: r for r in record['stages']}
    for name in ('contact', 'displacement'):
        flags = [
            r['original_sources_verified']
            for r in stages[name]['dependencies']
            if 'original_sources_verified' in r
        ]
        assert flags == [False, False]
    assert record['presentation_producer']['scope'].startswith('retrospective')


@pytest.mark.parametrize(
    'damage',
    ['missing_link', 'wrong_link', 'missing_historical', 'wrong_json', 'invalid_proof'],
)
def test_dependency_loss_and_identity_changes_are_rejected(damage, record):
    previous = record['inputs']
    document = {'baseline_sha256': previous['root_order']['sha256']}
    stage = 'occupancy'
    if damage == 'missing_link':
        document.clear()
    elif damage == 'wrong_link':
        document['baseline_sha256'] = '0' * 64
    else:
        stage = 'reference'
        document = {
            'historical_archives': {
                ligand: {
                    'gzip_sha256': previous[target]['sha256'],
                    'json_sha256': previous[target]['json_sha256'],
                    'producer_commit': '1' * 40,
                    'original_sources_verified': False,
                }
                for ligand, target in (('p59', 'occupancy'), ('p69', 'reciprocal'))
            }
        }
        if damage == 'missing_historical':
            document['historical_archives'].pop('p69')
        elif damage == 'wrong_json':
            document['historical_archives']['p59']['json_sha256'] = '0' * 64
        else:
            document['historical_archives']['p59']['original_sources_verified'] = (
                'unknown'
            )
    with pytest.raises(ValueError):
        synthesis.source_links(stage, document, previous)


@pytest.mark.parametrize(
    'damage',
    [
        'missing',
        'duplicate',
        'wrong_count',
        'flag_type',
        'recovery',
        'criterion',
        'missing_result',
        'fixed_rmsd',
    ],
)
def test_search_cells_and_recovery_denominators_cannot_silently_change(
    damage, original
):
    changed = dict(original)
    changed['comparison_rows'] = copy.deepcopy(original['comparison_rows'])
    if damage == 'missing':
        changed['comparison_rows'].pop()
    elif damage == 'duplicate':
        changed['comparison_rows'][0] = copy.deepcopy(changed['comparison_rows'][1])
    elif damage == 'wrong_count':
        changed['comparison_rows'][0]['poses'] += 1
    elif damage == 'flag_type':
        changed['comparison_rows'][0]['first_recovered'] = 0
    elif damage == 'recovery':
        changed['comparison_rows'][0]['first_recovered'] = not changed[
            'comparison_rows'
        ][0]['first_recovered']
    elif damage == 'criterion':
        changed['criterion'] = {**original['criterion'], 'cutoff_angstrom': 3.0}
    elif damage == 'fixed_rmsd':
        changed['comparison_rows'][0]['fixed_score_lowest'] = {
            'sham': {'heavy_rmsd_angstrom': float('nan'), 'recovered': False}
        }
    else:
        changed['new_runs'] = original['new_runs'][:-1]
    with pytest.raises(ValueError):
        synthesis.recovery_groups('root_order', changed)


def test_comparison_order_is_not_a_pose_or_run_identity(original):
    changed = {
        **original,
        'comparison_rows': list(reversed(original['comparison_rows'])),
        'new_runs': list(reversed(original['new_runs'])),
    }
    assert synthesis.recovery_groups(
        'root_order', changed
    ) == synthesis.recovery_groups('root_order', original)


def test_corrupt_compressed_input_is_rejected_before_parsing(tmp_path):
    path = tmp_path / '5x72_root_order/audit_2026-10-09.json.gz'
    path.parent.mkdir()
    path.write_bytes(b'not the frozen archive')
    with pytest.raises(ValueError, match='hash mismatch'):
        synthesis.read_archive('root_order', tmp_path)


def test_stale_ledger_is_rejected(tmp_path, record):
    shutil.copytree(synthesis.OUTPUT, tmp_path, dirs_exist_ok=True)
    (tmp_path / 'tables.md').write_text('changed')
    with pytest.raises(ValueError, match='Stale synthesis output'):
        synthesis.verify_outputs(record, tmp_path)


def test_check_mode_has_no_scientific_imports(tmp_path):
    script = """
import importlib.abc, runpy, sys
class BlockScientific(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'dockingmt','molsysmt','vina','rdkit','openmm','pyunitwizard','numpy','matplotlib'}:
            raise AssertionError('Unexpected scientific import: ' + fullname)
sys.meta_path.insert(0, BlockScientific())
sys.argv = [sys.argv[1], '--check']
runpy.run_path(sys.argv[0], run_name='__main__')
"""
    r = subprocess.run(
        [sys.executable, '-c', script, str(Path(synthesis.__file__).resolve())],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'seven historical 5X72 stages' in r.stdout
