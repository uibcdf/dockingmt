"""Bounded DockingMT receiving with externally selected support providers."""

import importlib
import json
import sys
from contextlib import nullcontext
from copy import deepcopy
from pathlib import Path

import dockingmt as dmt
import smonitor
from smonitor.handlers.memory import MemoryHandler
from smonitor.integrations import CatalogException


class ProviderFailure(CatalogException):
    pass


class OpaqueFailure(ValueError):
    calls = 0

    def __str__(self):
        self.calls += 1
        raise AssertionError('Native exception text was evaluated')


class OpaqueInput:
    calls = 0

    def __repr__(self):
        self.calls += 1
        raise AssertionError('Molecular input repr was evaluated')


def observe(role, threshold, kind):
    handler = MemoryHandler()
    smonitor.configure(
        profile='user',
        level=threshold,
        enabled=True,
        handlers=[handler],
        capture_warnings=False,
        capture_logging=False,
        capture_exceptions=False,
        trace_depth=8,
        duplicate_policy='off',
        event_buffer_size=50,
    )
    if kind == 'catalog':
        failure = ProviderFailure(
            'controlled provider refusal',
            code='RECEIVING-PROVIDER-E001',
            extra={'provider_marker': 'preserved'},
        )
    elif kind == 'metadata':
        failure = OpaqueFailure('PRIVATE_NATIVE_MARKER')
    else:
        failure = ValueError('controlled native failure', 17)
    cause = RuntimeError('original cause')
    original_args = failure.args
    value = OpaqueInput() if kind == 'metadata' else object()
    module = importlib.import_module(f'dockingmt.preparation.{role}')
    original_select = module.select_one_structure

    def reject(*args, **kwargs):
        raise failure from cause

    module.select_one_structure = reject
    before = deepcopy(smonitor.get_manager().config)
    scope = smonitor.diagnostic_scope() if kind == 'metadata' else nullcontext()
    caught = None
    try:
        with scope:
            try:
                getattr(dmt, f'prepare_{role}')(value, selection='all')
            except Exception as error:
                caught = error
    finally:
        module.select_one_structure = original_select
    events = [event for event in handler.events if event['level'] == 'ERROR']
    expected_code = (
        'SMONITOR-NATIVE-FAILURE'
        if kind == 'metadata'
        else getattr(failure, 'code', None)
    )
    valid = (
        caught is failure
        and failure.args == original_args
        and failure.__cause__ is cause
        and before == smonitor.get_manager().config
        and len(events) == 1
        and events[0]['code'] == expected_code
        and events[0]['source'] == f'dockingmt.preparation.{role}.prepare_{role}'
    )
    if kind == 'metadata':
        valid = valid and failure.calls == 0 and value.calls == 0
        valid = valid and 'PRIVATE_NATIVE_MARKER' not in json.dumps(handler.events)
    if kind == 'catalog' and events:
        valid = valid and events[0]['extra'].get('provider_marker') == 'preserved'
    return {
        'role': role,
        'threshold': threshold,
        'failure': kind,
        'passed': bool(valid),
        'error_events': len(events),
        'identity_args_cause_preserved': caught is failure
        and failure.args == original_args
        and failure.__cause__ is cause,
        'application_policy_preserved': before == smonitor.get_manager().config,
    }


rows = [
    observe(role, threshold, kind)
    for role in ('ligand', 'receptor')
    for threshold in ('WARNING', 'ERROR')
    for kind in ('native', 'catalog')
]
rows.extend(observe(role, 'WARNING', 'metadata') for role in ('ligand', 'receptor'))
receipt = {
    'passed': sum(row['passed'] for row in rows),
    'total': len(rows),
    'cases': rows,
}
Path(sys.argv[1]).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({key: receipt[key] for key in ('passed', 'total')}))
raise SystemExit(0 if all(row['passed'] for row in rows) else 1)
