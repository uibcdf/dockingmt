"""Scientific display fidelity in the addon; not browser acceptance."""

from copy import deepcopy
from types import SimpleNamespace

import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt import DockingPose, DockingResult
from molsysviewer_dockingmt.adapters.complex import set_active_pose
from molsysviewer_dockingmt.export import build_docking_export_payload
from molsysviewer_dockingmt.panels import DockingExplorerPanel
from molsysviewer_dockingmt.runtime import ensure_runtime
from molsysviewer_dockingmt.workbench import get_docking_summary_section


def _pose(identity, rank=None, scores=None, definitions=None):
    return DockingPose(
        puw.quantity([[0, 0, 0]], 'nm'),
        pose_id=identity,
        rank=rank,
        scores=scores,
        score_definitions=definitions,
    )


@pytest.fixture
def explorer():
    frames = []
    view = SimpleNamespace(player=SimpleNamespace(go_to_structure=frames.append))
    runtime = ensure_runtime(view)
    runtime.result = DockingResult(
        [
            _pose('seventh', 7, {'custom': 12}),
            _pose('unranked', None),
            _pose('first', 1, {'control': -2, 'vina': 0}),
        ]
    )
    panel = DockingExplorerPanel(view=view)
    states = []
    panel.push_state = states.append
    yield view, runtime, panel, frames, states
    panel.close()


def test_pose_selection_uses_collection_position_not_scientific_rank(explorer):
    view, runtime, panel, frames, states = explorer
    original = deepcopy(runtime.result.to_dict())
    panel.on_mount(view)
    assert [row['rank'] for row in states[-1]['poses']] == [7, None, 1]
    assert [row['pose_id'] for row in states[-1]['poses']] == [
        'seventh',
        'unranked',
        'first',
    ]
    for index, identity, rank in [
        (2, 'first', 1),
        (0, 'seventh', 7),
        (1, 'unranked', None),
    ]:
        panel.handle_action(view, 'set_pose', {'index': index})
        state = states[-1]
        assert state['status'] == 'idle'
        assert state['active_index'] == index
        assert frames[-1] == index
        row = state['poses'][index]
        assert (row['position'], row['pose_id'], row['rank']) == (
            index + 1,
            identity,
            rank,
        )
        summary = get_docking_summary_section(view)
        assert summary['selected_pose'] == row
        assert summary['active_pose_index'] == index
        assert summary['item_title'] == f'Pose {index + 1} of 3'
        assert build_docking_export_payload(view)['selected_pose'] == row
    panel.handle_action(view, 'prev_pose', {})
    assert frames[-1] == 0
    panel.handle_action(view, 'next_pose', {})
    assert frames[-1] == 1
    assert runtime.result.to_dict() == original


def test_top_score_zero_is_not_replaced_and_selected_pose_is_distinct(explorer):
    view, runtime, panel, _, _ = explorer
    summary = get_docking_summary_section(view)
    assert summary['selected_pose']['pose_id'] == 'seventh'
    assert summary['top_score'] == 0.0
    assert summary['top_scores'] == [
        {'name': 'control', 'value': -2.0, 'unit': None, 'definition': None},
        {'name': 'vina', 'value': 0.0, 'unit': None, 'definition': None},
    ]
    assert 'vina=0.00 (unit unknown)' in summary['item_subtitle']
    assert 'kcal/mol' not in summary['item_subtitle']
    rows = panel._build_state(runtime, view)['poses']
    assert rows[0]['scores'] == [
        {'name': 'custom', 'value': 12.0, 'unit': None, 'definition': None}
    ]
    assert rows[1]['scores'] == []
    assert rows[2]['scores'] == summary['top_scores']


@pytest.mark.parametrize('scores', [{}, {'custom': 3}, {'other': 5, 'custom': 3}])
def test_summary_never_substitutes_other_scores_for_vina(explorer, scores):
    view, runtime, _, _, _ = explorer
    runtime.result = DockingResult([_pose('custom', scores=scores)])
    summary = get_docking_summary_section(view)
    assert summary['top_score'] is None
    assert {s['name']: s['value'] for s in summary['top_scores']} == scores


@pytest.mark.parametrize(
    'kind,unit,value',
    [('empirical', 'kJ/mol', -25.104), ('dimensionless', 'dimensionless', 0)],
)
def test_declared_score_meaning_survives_nondefault_application_policy(
    explorer, kind, unit, value
):
    view, runtime, panel, _, _ = explorer
    definition = {
        'schema_version': '1.0',
        'method': 'explicit-method',
        'method_version': '1',
        'component': 'reported-score',
        'kind': kind,
        'unit': unit,
        'preferred_direction': 'lower',
        'context': {'input': 'declared-state'},
    }
    with puw.context(standard_units=['pm', 'fs', 'kJ/mol']):
        pose = _pose(
            'declared', scores={'metric': value}, definitions={'metric': definition}
        )
        runtime.result = DockingResult([pose])
        before = deepcopy(pose.to_dict())
        row = panel._build_state(runtime, view)['poses'][0]
        score = row['scores'][0]
        assert score['value'] == value
        assert score['unit'] == pose.score_definitions['metric']['unit']
        assert score['definition'] == pose.score_definitions['metric']
        assert get_docking_summary_section(view)['top_scores'] == row['scores']
        score['definition']['context']['input'] = 'display-only-change'
        assert pose.to_dict() == before
        assert puw.configure.report()['standard_units'] == ['pm', 'fs', 'kJ/mol']


def test_display_refresh_and_navigation_never_compute_rmsd(explorer, monkeypatch):
    view, runtime, panel, frames, states = explorer
    calls = []

    def forbidden(*args, **kwargs):
        calls.append('rmsd')
        raise AssertionError('Display must not launch a molecular calculation.')

    runtime.reference = object()
    monkeypatch.setattr(runtime.result, 'get_rmsds', forbidden)
    panel.on_mount(view)
    panel.handle_action(view, 'next_pose', {})
    panel.on_mount(view)
    panel._build_state(runtime, view)
    assert calls == []
    assert frames == [1]
    assert states[-1]['has_reference'] is True
    assert 'RMSD unavailable' in states[-1]['comparison_note']


@pytest.mark.parametrize('position', [True, False, 1.5, '2', None, -1, 0, 4])
def test_invalid_legacy_position_does_not_move_player_or_publish_state(
    explorer, position
):
    view, runtime, _, frames, _ = explorer
    before = list(runtime.event_log)
    with pytest.raises(ValueError, match='pose position'):
        set_active_pose(view, position)
    assert frames == []
    assert runtime.active_pose_index == 0
    assert runtime.event_log == before


@pytest.mark.parametrize('position', [2, np.int64(2)])
def test_legacy_position_remains_one_based(explorer, position):
    view, runtime, panel, frames, states = explorer
    panel.handle_action(view, 'set_pose', {'rank': position})
    assert frames == [1]
    assert runtime.active_pose_rank == 2
    assert states[-1]['poses'][1]['rank'] is None


@pytest.mark.parametrize(
    'payload',
    [
        {'index': True},
        {'index': 0.5},
        {'index': -1},
        {'index': 3},
        {},
        {'index': 0, 'rank': 1},
    ],
)
def test_invalid_panel_selection_reports_error_without_changing_selection(
    explorer, payload
):
    view, runtime, panel, frames, states = explorer
    panel.handle_action(view, 'set_pose', payload)
    assert states[-1]['status'] == 'error'
    assert states[-1]['error']
    assert states[-1]['active_index'] == 0
    assert frames == []
    assert runtime.active_pose_index == 0


def test_player_failure_preserves_selection_and_reports_error(explorer):
    view, runtime, panel, _, states = explorer

    def fail(index):
        raise RuntimeError('player transport failed')

    view.player.go_to_structure = fail
    panel.handle_action(view, 'set_pose', {'index': 2})
    assert states[-1]['status'] == 'error'
    assert states[-1]['error'] == 'player transport failed'
    assert states[-1]['active_index'] == 0
    assert runtime.active_pose_index == 0
    assert runtime.event_log == []


@pytest.mark.parametrize('result', [None, DockingResult([])])
def test_empty_workspace_has_no_selected_pose(explorer, result):
    view, runtime, panel, _, _ = explorer
    runtime.result = result
    state = panel._build_state(runtime, view)
    assert state['active_index'] is None
    assert state['poses'] == []
    assert state['has_reference'] is False
    assert state['has_domain'] is False
    assert get_docking_summary_section(view)['selected_pose'] is None
    assert build_docking_export_payload(view)['selected_pose'] is None


def test_selection_and_remount_are_isolated_per_view(explorer):
    view, runtime, panel, _, states = explorer
    other = SimpleNamespace()
    other_runtime = ensure_runtime(other)
    other_runtime.result = runtime.result
    panel.handle_action(view, 'set_pose', {'index': 2})
    panel.on_mount(view)
    assert states[-1]['active_index'] == 2
    assert get_docking_summary_section(other)['active_pose_index'] == 0
    assert other_runtime.event_log == []
