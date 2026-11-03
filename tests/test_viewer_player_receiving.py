"""Actual public player/widget synchronization; no browser acceptance implied."""

from contextlib import contextmanager
from copy import deepcopy

import pytest
import pyunitwizard as puw

import dockingmt as dmt
from molsysviewer_dockingmt import ensure_runtime, render_search_domain


@contextmanager
def _live_panels(monkeypatch):
    msv = pytest.importorskip('molsysviewer')
    # The provider owns molecular demo construction and explicit frame selection.
    with msv.demo['pentalanine'] as source:
        view = msv.new_view(source.molsys, structure_indices=[8, 3, 11])
    panels = []
    try:
        assert view.player.n_structures == 3
        view.addons.enable('dockingmt')
        runtime = ensure_runtime(view)
        # Controlled presentation records, not a redocking/geometry experiment.
        runtime.result = dmt.DockingResult(
            [
                dmt.DockingPose(
                    puw.quantity([[0, 0, 0]], 'angstrom'), pose_id='seventh', rank=7
                ),
                dmt.DockingPose(puw.quantity([[1, 0, 0]], 'angstrom')),
                dmt.DockingPose(
                    puw.quantity([[2, 0, 0]], 'angstrom'),
                    pose_id='first',
                    rank=1,
                    scores={'vina': 0},
                ),
            ]
        )
        render_search_domain(
            view,
            dmt.BoxRegion(
                center=puw.quantity([0, 0, 0], 'angstrom'),
                lengths=puw.quantity([10, 10, 10], 'angstrom'),
            ),
        )
        published = {'explorer': [], 'domain': []}
        for name in published:
            panel = view.addons.resolve_panel_widget('dockingmt', name)
            panels.append(panel)
            original = panel.push_state

            def observe(state, *, saved=original, history=published[name]):
                history.append(deepcopy(state))
                saved(state)

            # Observe the addon widget's real publication, keeping its transport.
            monkeypatch.setattr(panel, 'push_state', observe)
            panel.on_mount(view)
        yield view, runtime, panels, published
    finally:
        for panel in panels:
            panel.close()
        view.close()


@pytest.fixture
def live_panels(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('Player/panel synchronization must not compute docking or RMSD.')

    monkeypatch.setattr(dmt, 'dock', forbidden)
    monkeypatch.setattr(dmt, 'score', forbidden)
    monkeypatch.setattr(dmt.DockingResult, 'get_rmsds', forbidden)
    with _live_panels(monkeypatch) as state:
        yield state


@pytest.mark.parametrize(
    'method,args,index',
    [
        ('go_to_structure', (2,), 2),
        ('go_to_first', (), 0),
        ('go_to_last', (), 2),
        ('step_forward', (), 2),
        ('step_backward', (), 0),
        ('step_forward', (2,), 0),
        ('step_backward', (2,), 2),
    ],
)
def test_public_player_updates_both_widgets_without_refresh(
    live_panels, method, args, index
):
    view, runtime, panels, published = live_panels
    view.player.go_to_structure(1)
    for history in published.values():
        history.clear()
    events = []
    view.on_frame_change(events.append)
    before = runtime.result.to_dict()
    getattr(view.player, method)(*args)
    assert view.player.index == runtime.active_pose_index == index
    assert events == [{'event': 'frame_changed', 'frame': index, 'is_playing': False}]
    for name, panel in zip(('explorer', 'domain'), panels):
        assert len(published[name]) == 1
        assert panel.state[name] == published[name][-1]
    selected = panels[0].state['explorer']
    assert selected['active_index'] == index
    assert [row['rank'] for row in selected['poses']] == [7, None, 1]
    assert selected['poses'][2]['scores'][0]['value'] == 0
    assert panels[1].state['domain']['domain_available'] is True
    assert runtime.result.to_dict() == before


def test_repeated_public_seek_has_no_duplicate_widget_notifications(live_panels):
    view, runtime, panels, published = live_panels
    events = []
    view.on_frame_change(events.append)
    view.player.go_to_structure(2)
    counts = {name: len(history) for name, history in published.items()}
    view.player.go_to_structure(2)
    assert len(events) == 1
    assert {name: len(history) for name, history in published.items()} == counts
    assert runtime.active_pose_index == panels[0].state['explorer']['active_index'] == 2


def test_playback_state_notifications_retain_the_selected_pose(live_panels):
    view, runtime, panels, published = live_panels
    view.player.go_to_structure(2)
    selected = deepcopy(panels[0].state['explorer']['poses'][2])
    events = []
    view.on_frame_change(events.append)
    counts = {name: len(history) for name, history in published.items()}
    view.player.play()
    view.player.play()
    view.player.pause()
    view.player.pause()
    assert events == [
        {'event': 'frame_changed', 'frame': 2, 'is_playing': True},
        {'event': 'frame_changed', 'frame': 2, 'is_playing': False},
    ]
    assert runtime.active_pose_index == 2
    assert panels[0].state['explorer']['poses'][2] == selected
    for name in counts:
        assert len(published[name]) == counts[name] + 2


def test_real_widget_unmount_and_remount_preserve_other_subscribers(live_panels):
    view, runtime, panels, published = live_panels
    events = []
    view.on_frame_change(events.append)
    panels[0].on_unmount(view)
    before = len(published['explorer'])
    domain_before = len(published['domain'])
    view.player.go_to_structure(2)
    assert len(published['explorer']) == before
    assert len(published['domain']) == domain_before + 1
    assert runtime.active_pose_index == 2
    panels[0].on_mount(view)
    assert panels[0].state['explorer']['active_index'] == 2
    panels[0].close()
    before = len(published['explorer'])
    view.player.go_to_first()
    assert len(published['explorer']) == before
    assert [event['frame'] for event in events] == [2, 0]
    assert panels[1].state['domain']['domain_available'] is True
    view.off_frame_change(events.append)


def test_real_player_invalid_seek_leaves_widget_state_unchanged(live_panels):
    view, runtime, panels, published = live_panels
    before = [deepcopy(panel.state) for panel in panels]
    counts = {name: len(history) for name, history in published.items()}
    with pytest.raises(Exception, match='index'):
        view.player.go_to_structure(3)
    assert view.player.index == runtime.active_pose_index == 0
    assert [panel.state for panel in panels] == before
    assert {name: len(history) for name, history in published.items()} == counts


def test_real_player_isolated_views_keep_their_own_panel_state(
    live_panels, monkeypatch
):
    view, _, panels, _ = live_panels
    with _live_panels(monkeypatch) as (other, _, other_panels, other_published):
        before = [deepcopy(panel.state) for panel in other_panels]
        counts = {name: len(history) for name, history in other_published.items()}
        view.player.go_to_structure(2)
        assert panels[0].state['explorer']['active_index'] == 2
        assert other.player.index == 0
        assert [panel.state for panel in other_panels] == before
        assert {
            name: len(history) for name, history in other_published.items()
        } == counts


def test_closed_real_view_cannot_publish_successful_navigation(live_panels):
    view, _, _, published = live_panels
    view.close()
    counts = {name: len(history) for name, history in published.items()}
    with pytest.raises(RuntimeError, match='closed'):
        view.player.go_to_structure(1)
    assert {name: len(history) for name, history in published.items()} == counts
