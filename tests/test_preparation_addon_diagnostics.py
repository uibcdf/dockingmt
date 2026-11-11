"""Owned diagnostic codes and provider failure identity across orchestration."""

import importlib
from dataclasses import replace
from types import SimpleNamespace

import pytest
import pyunitwizard as puw
import smonitor

import bindingmt as bmt
from molsysviewer_bindingmt import (
    build_docking_complex_system,
    build_docking_reference_system,
    render_search_domain,
    set_active_pose,
    set_reference_visibility,
    set_search_domain_visibility,
)
from molsysviewer_bindingmt._scene import sync_scene_state
from molsysviewer_bindingmt.panels import DockingExplorerPanel, SearchDomainPanel
from molsysviewer_bindingmt.runtime import ensure_runtime


@pytest.fixture
def events(monkeypatch):
    observed = []

    class Collector:
        def handle(self, event, **kwargs):
            observed.append(event)

    manager = smonitor.get_manager()
    monkeypatch.setattr(
        manager, '_config', replace(manager._config, trace_depth=16, level='DEBUG')
    )
    collector = Collector()
    manager.add_handler(collector)
    try:
        yield observed
    finally:
        manager.remove_handler(collector)


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
def test_preparation_traces_provider_failure_without_translation(
    role, monkeypatch, events
):
    module = importlib.import_module(f'bindingmt.preparation.{role}')
    failure = ValueError('provider selection failed')

    def reject(*args, **kwargs):
        raise failure

    monkeypatch.setattr(module, 'select_one_structure', reject)
    with pytest.raises(ValueError) as caught:
        getattr(bmt, f'prepare_{role}')(object(), selection='all')
    assert caught.value is failure
    frames = [
        frame
        for event in events
        for frame in event.get('context', {}).get('frames', [])
    ]
    matching = [frame for frame in frames if frame['function'] == f'prepare_{role}']
    assert matching
    assert matching[-1]['extra']['operation'] == f'prepare_{role}'
    assert matching[-1]['extra']['provider'] == 'molsysmt'


@pytest.mark.parametrize(
    'call, family, code, field, expected',
    [
        (
            lambda: build_docking_reference_system(object(), True),
            ValueError,
            'BMT-E004',
            'n_poses',
            True,
        ),
        (
            lambda: build_docking_complex_system(object(), []),
            ValueError,
            'BMT-E006',
            'resource',
            'nonempty pose collection',
        ),
        (
            lambda: set_active_pose(SimpleNamespace(), 1),
            RuntimeError,
            'BMT-E009',
            'resource',
            'docking result',
        ),
        (
            lambda: set_reference_visibility(SimpleNamespace(), True),
            RuntimeError,
            'BMT-E009',
            'resource',
            'explicit reference',
        ),
        (
            lambda: set_search_domain_visibility(SimpleNamespace(), True),
            RuntimeError,
            'BMT-E009',
            'resource',
            'search domain',
        ),
        (
            lambda: render_search_domain(
                SimpleNamespace(), bmt.BoxRegion('[0, 0, 0] nm', '[1, 1, 1] nm')
            ),
            RuntimeError,
            'BMT-E010',
            'capability',
            'shapes',
        ),
    ],
)
def test_addon_errors_keep_python_family_and_emit_owned_code(
    call, family, code, field, expected, events
):
    with pytest.raises(family) as caught:
        call()
    assert caught.value.code == code
    assert caught.value.extra[field] == expected
    assert caught.value.extra['provider'] == 'molsysviewer'
    emitted = [event for event in events if event.get('code') == code]
    assert len(emitted) == 1
    assert emitted[0]['extra'][field] == expected
    assert emitted[0]['extra']['operation']


@pytest.mark.parametrize('panel_type', [DockingExplorerPanel, SearchDomainPanel])
def test_panel_handles_owned_error_with_code_and_trace(panel_type, events):
    view = SimpleNamespace()
    panel = panel_type(view=view)
    states = []
    panel.push_state = states.append
    try:
        panel.handle_action(view, 'unknown-control', {})
        assert states[-1]['status'] == 'error'
        assert states[-1]['error_code'] == 'BMT-E011'
        emitted = [event for event in events if event.get('code') == 'BMT-E011']
        assert len(emitted) == 1
        assert emitted[0]['extra']['action_id'] == 'unknown-control'
        panel.handle_action(view, 'refresh', {})
        assert states[-1]['status'] == 'idle'
        assert states[-1]['error_code'] is None
    finally:
        panel.close()


def test_panel_provider_failure_is_reported_without_local_reclassification(events):
    failure = RuntimeError('player transport failed')

    def reject(index):
        raise failure

    view = SimpleNamespace(player=SimpleNamespace(go_to_structure=reject))
    runtime = ensure_runtime(view)
    runtime.result = bmt.DockingResult(
        [bmt.DockingPose(puw.quantity([[0, 0, 0]], 'nm'))]
    )
    panel = DockingExplorerPanel(view=view)
    states = []
    panel.push_state = states.append
    try:
        panel.handle_action(view, 'set_pose', {'index': 0})
        assert states[-1]['error'] == str(failure)
        assert states[-1]['error_code'] is None
        assert runtime.active_pose_rank == 1
        emitted = [
            event for event in events if event.get('exception_type') == 'RuntimeError'
        ]
        assert len(emitted) == 1
        assert emitted[0].get('code') is None
    finally:
        panel.close()


def test_idle_scene_absence_does_not_emit_errors(events):
    for _ in range(3):
        controls = sync_scene_state(SimpleNamespace())
        assert controls['domain_available'] is False
        assert controls['reference_available'] is False
    assert not events


def test_owned_error_is_emitted_at_normal_application_threshold(events, monkeypatch):
    manager = smonitor.get_manager()
    monkeypatch.setattr(manager, '_config', replace(manager._config, level='WARNING'))
    with pytest.raises(RuntimeError) as caught:
        set_active_pose(SimpleNamespace(), 1)
    assert caught.value.code == 'BMT-E009'
    assert [event['level'] for event in events] == ['ERROR']


def test_panel_refresh_reports_provider_read_failure(events):
    failure = RuntimeError('shape query failed')

    def reject():
        raise failure

    layer = SimpleNamespace(tag='domain', info=reject)
    view = SimpleNamespace(shapes=SimpleNamespace(get=lambda tag: layer))
    runtime = ensure_runtime(view)
    runtime.domain_layer = layer
    panel = SearchDomainPanel(view=view)
    states = []
    panel.push_state = states.append
    try:
        panel.on_mount(view)
        assert states[-1]['status'] == 'error'
        assert states[-1]['error'] == 'shape query failed'
        assert states[-1]['error_code'] is None
        assert states[-1]['domain_available'] is False
        emitted = [
            event for event in events if event.get('exception_type') == 'RuntimeError'
        ]
        assert len(emitted) == 1
        assert emitted[0]['extra']['operation'] == 'read_panel_state'
    finally:
        panel.close()
