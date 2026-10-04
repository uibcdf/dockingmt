"""Reproduce offline collection controls from the retained native evaluations."""

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'devguide/validation/data/redocking_evaluation/cases.json'


def qualify():
    """Return cohort summaries and their source receipts without running Vina.

    Native measurements remain historical software controls. The declared failure
    is a labelled fixture, not a newly observed engine or evaluation failure.
    Equal unassessed preparation does not establish scientific comparability.
    """
    source_bytes = SOURCE.read_bytes()
    reports = json.loads(source_bytes)
    try:
        dmt.summarize_redocking(reports)
    except ArgumentError as exc:
        rejected = {'code': exc.code, 'reason': str(exc)}
    else:
        raise AssertionError('Different comparison/preparation policies were pooled.')
    selected = {
        name: reports[name] for name in ('1iep_external', '1iep_displaced_domain')
    }
    outcome = dmt.DockingOutcome(
        0,
        error={
            'type': 'fixture.DeclaredEvaluationFailure',
            'message': 'Explicit denominator fixture; no runtime failure was observed.',
            'code': None,
        },
    )
    summaries = {
        '181l_provisional': dmt.summarize_redocking(
            {'181l_provisional': reports['181l_provisional']}
        ),
        '1iep_external_controls': dmt.summarize_redocking(selected),
        '1iep_with_declared_failure_fixture': dmt.summarize_redocking(
            selected,
            failures={
                'declared_failure_fixture': {
                    'stage': 'evaluation',
                    'error': outcome.error,
                    'context': {'fixture': True, 'observed_runtime_failure': False},
                }
            },
        ),
        'all_failure_fixture': dmt.summarize_redocking(
            {},
            failures={
                'declared_failure_fixture': {
                    'stage': 'evaluation',
                    'error': outcome.error,
                    'context': {'fixture': True, 'observed_runtime_failure': False},
                }
            },
        ),
        'empty_collection': dmt.summarize_redocking({}),
    }
    for entry in summaries['1iep_with_declared_failure_fixture']['top_n']:
        assert (entry['n_recovered'], entry['n_not_recovered'], entry['n_unknown']) == (
            1,
            1,
            1,
        )
        assert entry['fraction_of_evaluated'] == 0.5
        assert entry['fraction_of_submitted'] == 1 / 3
    assert SOURCE.read_bytes() == source_bytes
    return {
        'schema_version': '1.0',
        'scope': 'offline_saved_native_observations_and_declared_failure_fixtures',
        'source': {
            'path': str(SOURCE.relative_to(ROOT)),
            'sha256': hashlib.sha256(source_bytes).hexdigest(),
            'size_bytes': len(source_bytes),
            'original_qualification': 'dockingmt#38',
            'fresh_engine_execution': False,
        },
        'execution': {
            'python': platform.python_version(),
            'interpreter': sys.executable,
            'dockingmt_version': dmt.__version__,
            'checkout_head': subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True
            ).strip(),
            'implementation_sha256': hashlib.sha256(
                (ROOT / 'dockingmt/aggregation.py').read_bytes()
            ).hexdigest(),
            'helper_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
        'rejected_mixed_policy': rejected,
        'summaries': summaries,
    }
