"""Protect payload equivalence and comparable measurements in the developer tool."""

import builtins
import json
import sys
from copy import deepcopy

import molsysmt as msm
import pytest

from devtools import benchmark_result_export as benchmark


def test_benchmark_cli_reads_no_molecular_or_optional_engine_operations(
    tmp_path, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail('Result export benchmark requested a scientific provider operation')

    for operation in ('get', 'select', 'extract', 'convert', 'copy', 'set'):
        monkeypatch.setattr(msm, operation, forbidden)
    actual_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split('.')[0] in ('vina', 'molsysviewer', 'rdkit'):
            pytest.fail(
                'Result export benchmark imported an optional scientific provider'
            )
        return actual_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded_import)
    report_path = tmp_path / 'report.json'
    monkeypatch.setattr(
        sys,
        'argv',
        [
            'benchmark_result_export',
            '--report',
            str(report_path),
            '--case',
            'small_mapped',
            '--repeats',
            '1',
        ],
    )
    benchmark.main()
    report = json.loads(report_path.read_text())
    assert report['unit'] == 'second' and report['clock'] == 'perf_counter'
    assert set(report['cases']) == {'small_mapped'}
    case = report['cases']['small_mapped']
    assert case['n_poses'] == 9 and case['atoms_per_pose'] == [64] * 9
    assert len(case['seconds']) == 1
    assert len(case['record_sha256']) == 64
    assert benchmark._compare(report, report)['small_mapped']['records_match']


@pytest.fixture
def reference_report():
    return {
        'schema_version': '1.0',
        'unit': 'second',
        'clock': 'perf_counter',
        'memory_unit': 'byte',
        'method': 'same',
        'repeats': 3,
        'environment': {'python': 'same'},
        'cases': {'example': {'record_sha256': 'same', 'median_seconds': 1}},
    }


@pytest.mark.parametrize(
    'field,value',
    [
        ('schema_version', '999.0'),
        ('unit', 'millisecond'),
        ('clock', 'process_time'),
        ('method', 'different'),
        ('memory_unit', 'kilobyte'),
        ('environment', {'python': 'different'}),
        ('repeats', 2),
        ('cases', {}),
    ],
)
def test_benchmark_comparison_rejects_incomparable_references(
    reference_report, field, value
):
    changed = deepcopy(reference_report)
    changed[field] = value
    with pytest.raises(ValueError):
        benchmark._compare(reference_report, changed)


def test_benchmark_comparison_rejects_changed_serialized_content(reference_report):
    changed = deepcopy(reference_report)
    changed['cases']['example']['record_sha256'] = 'changed'
    with pytest.raises(ValueError, match='serialized content differs'):
        benchmark._compare(reference_report, changed)
