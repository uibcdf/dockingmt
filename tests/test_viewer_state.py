"""Addon-owned state propagation, prerequisites and visual ownership."""

from types import SimpleNamespace

import pytest
import pyunitwizard as puw

from dockingmt import BoxRegion, DockingPose, DockingResult
from molsysviewer_dockingmt import (
    clear_docking,
    on_context_action,
    on_disable,
    render_docking_result,
    render_search_domain,
    set_active_pose,
    set_reference_visibility,
    set_search_domain_visibility,
)
from molsysviewer_dockingmt.export import build_docking_export_payload
from molsysviewer_dockingmt.panels import DockingExplorerPanel, SearchDomainPanel
from molsysviewer_dockingmt.runtime import ensure_runtime
from molsysviewer_dockingmt.workbench import get_docking_summary_section


class _Shape:
    def __init__(self, shapes, tag):
        self.shapes = shapes
        self.tag = tag
        self.visible = True
        self.fail_delete = False
        self.fail_info = False

    def info(self):
        if self.fail_info:
            raise RuntimeError('shape query failed')
        return {'visible': self.visible}

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def delete(self):
        if self.fail_delete:
            raise RuntimeError('shape deletion failed')
        self.shapes.deleted.append(self.tag)
        del self.shapes.items[self.tag]

    def set_tag(self, new_tag):
        del self.shapes.items[self.tag]
        self.tag = new_tag
        self.shapes.items[new_tag] = self


class _Shapes:
    def __init__(self):
        self.items = {}
        self.deleted = []
        self.fail_add = False
        self.links = SimpleNamespace(add_links=self.add)

    def get(self, tag):
        return self.items.get(tag)

    def add(self, *, tag, **kwargs):
        if self.fail_add:
            raise RuntimeError('shape creation failed')
        if tag in self.items:
            raise ValueError('duplicate shape tag')
        layer = _Shape(self, tag)
        self.items[tag] = layer
        return layer


class _View:
    def __init__(self):
        self.shapes = _Shapes()
        self.region_items = {}
        self.regions = SimpleNamespace(get=self.region_items.get)
        self.callbacks = []
        self.moves = []
        self.player = SimpleNamespace(index=0, go_to_structure=self.move)

    def move(self, index):
        self.moves.append(index)
        self.player.index = index

    def on_frame_change(self, callback):
        self.callbacks.append(callback)

    def off_frame_change(self, callback):
        self.callbacks.remove(callback)

    def emit_frame(self, index):
        self.player.index = index
        for callback in self.callbacks.copy():
            callback({'event': 'frame_changed', 'frame': index})


@pytest.fixture
def state():
    view = _View()
    runtime = ensure_runtime(view)
    runtime.result = DockingResult(
        [
            DockingPose(puw.quantity([[0, 0, 0]], 'nm'), pose_id='a', rank=8),
            DockingPose(puw.quantity([[1, 1, 1]], 'nm'), pose_id='b'),
        ]
    )
    panels = [DockingExplorerPanel(view=view), SearchDomainPanel(view=view)]
    states = [[], []]
    for panel, received in zip(panels, states):
        panel.push_state = received.append
        panel.on_mount(view)
    yield view, runtime, panels, states
    for panel in panels:
        panel.close()


@pytest.fixture
def box():
    return BoxRegion(
        center=puw.quantity([1, 2, 3], 'nm'),
        lengths=puw.quantity([2, 2, 2], 'nm'),
    )


def test_python_and_context_actions_refresh_both_mounted_panels(state, box):
    view, runtime, panels, states = state
    render_search_domain(view, box)
    assert states[0][-1]['domain_available'] is True
    assert states[1][-1]['has_domain'] is True
    set_active_pose(view, 2)
    assert states[0][-1]['active_index'] == 1
    assert states[0][-1]['poses'][1]['rank'] is None
    on_context_action(view, 'toggle-search-domain', {})
    assert states[0][-1]['domain_visible'] is False
    assert states[1][-1]['visible'] is False
    panels[1].handle_action(view, 'toggle_domain', {})
    assert states[0][-1]['domain_visible'] is True
    assert states[1][-1]['visible'] is True
    assert runtime.domain_layer.info()['visible'] is True


def test_public_frame_callback_and_manual_readback_do_not_reissue_navigation(state):
    view, runtime, panels, states = state
    view.emit_frame(1)
    assert states[0][-1]['active_index'] == 1
    assert runtime.active_pose_index == 1
    assert view.moves == []
    # The qualified host does not notify callbacks for direct Python player calls.
    view.player.go_to_structure(0)
    assert states[0][-1]['active_index'] == 1
    panels[0].handle_action(view, 'refresh', {})
    assert states[0][-1]['active_index'] == 0
    assert view.moves == [0]
    view.player.go_to_structure(1)
    assert get_docking_summary_section(view)['selected_pose']['pose_id'] == 'b'
    assert build_docking_export_payload(view)['selected_pose']['pose_id'] == 'b'


def test_mount_is_idempotent_and_unmount_is_local_to_one_widget(state):
    view, runtime, panels, states = state
    assert len(view.callbacks) == 2
    panels[0].on_mount(view)
    assert len(view.callbacks) == 2
    old_callbacks = view.callbacks.copy()
    panels[0].on_unmount(view)
    before = len(states[0])
    set_active_pose(view, 2)
    assert len(states[0]) == before
    assert len(view.callbacks) == 1
    assert len(runtime._panels) == 1
    panels[0].on_mount(view)
    assert states[0][-1]['active_index'] == 1
    panels[0].close()
    for callback in old_callbacks:
        callback({'event': 'frame_changed', 'frame': 0})
    assert len(view.callbacks) == 1
    assert len(states[0]) == before + 1
    panels[1].close()
    assert view.callbacks == []
    assert not runtime._panels


def test_two_views_keep_panels_independent(state):
    view, _, _, states = state
    other = _View()
    ensure_runtime(other).result = ensure_runtime(view).result
    panel = DockingExplorerPanel(view=other)
    received = []
    panel.push_state = received.append
    try:
        panel.on_mount(other)
        set_active_pose(view, 2)
        assert states[0][-1]['active_index'] == 1
        assert received[-1]['active_index'] == 0
    finally:
        panel.close()


@pytest.mark.parametrize('which', ['domain', 'reference'])
def test_absent_visual_rejects_visibility_change(state, which):
    view, runtime, panels, states = state
    operation = (
        set_search_domain_visibility if which == 'domain' else set_reference_visibility
    )
    event_count = len(runtime.event_log)
    with pytest.raises(RuntimeError, match='before changing its visibility'):
        operation(view, True)
    assert len(runtime.event_log) == event_count
    action = 'toggle_search_domain' if which == 'domain' else 'toggle_reference'
    panels[0].handle_action(view, action, {})
    assert states[0][-1]['status'] == 'error'
    assert states[0][-1][f'{which}_available'] is False


def test_caller_visibility_is_read_on_refresh(state, box):
    view, runtime, panels, states = state
    layer = render_search_domain(view, box)
    layer.hide()
    panels[1].handle_action(view, 'refresh', {})
    assert states[1][-1]['visible'] is False
    assert runtime.domain_visible is False
    on_context_action(view, 'toggle-search-domain', {})
    assert layer.visible is True
    reference = _Shape(view.shapes, 'reference_ligand')
    view.region_items[reference.tag] = reference
    runtime.reference_region = reference
    runtime.reference = object()
    panels[0].handle_action(view, 'refresh', {})
    assert states[0][-1]['reference_available'] is True
    reference.hide()
    panels[0].handle_action(view, 'refresh', {})
    assert states[0][-1]['reference_visible'] is False
    replacement = _Shape(view.shapes, 'reference_ligand')
    view.region_items[reference.tag] = replacement
    with pytest.raises(RuntimeError, match='explicit reference'):
        set_reference_visibility(view, False)
    assert replacement.visible is True


def test_clear_and_disable_preserve_unrelated_shapes(state, box):
    view, runtime, _, states = state
    unrelated = view.shapes.add(tag='caller-owned')
    first = render_search_domain(view, box, tag='first-domain')
    second = render_search_domain(view, box, tag='second-domain')
    second.set_tag('renamed-domain')
    set_search_domain_visibility(view, False)
    assert second.visible is False
    assert first.visible is True
    on_disable(view)
    assert view.shapes.get('caller-owned') is unrelated
    assert view.shapes.deleted == ['first-domain', 'renamed-domain']
    assert runtime.domain_layers == []
    assert runtime.result is None
    assert runtime.reference is None
    assert states[0][-1]['poses'] == []
    assert states[1][-1]['has_domain'] is False


def test_reused_tag_is_not_mistaken_for_owned_shape(state, box):
    view, runtime, _, _ = state
    old = render_search_domain(view, box)
    old.delete()
    replacement = view.shapes.add(tag=old.tag)
    with pytest.raises(RuntimeError, match='Render the search domain'):
        set_search_domain_visibility(view, False)
    clear_docking(view)
    assert view.shapes.get(old.tag) is replacement
    assert runtime.domain_layers == []


def test_render_refuses_unrelated_existing_tag_without_deletion(state, box):
    view, runtime, _, _ = state
    unrelated = view.shapes.add(tag='dockingmt:search_domain')
    with pytest.raises(ValueError, match='already owned'):
        render_search_domain(view, box)
    assert view.shapes.get(unrelated.tag) is unrelated
    assert view.shapes.deleted == []
    assert runtime.search_domain is None


def test_cleanup_failure_retains_remaining_handles_for_retry(state, box):
    view, runtime, _, _ = state
    first = render_search_domain(view, box, tag='first')
    second = render_search_domain(view, box, tag='second')
    second.fail_delete = True
    with pytest.raises(RuntimeError, match='deletion failed'):
        clear_docking(view)
    assert runtime.domain_layers == [second]
    assert runtime.result is not None
    assert view.shapes.get(first.tag) is None
    assert view.shapes.get(second.tag) is second
    second.fail_delete = False
    clear_docking(view)
    assert runtime.domain_layers == []
    assert runtime.result is None


def test_failed_render_does_not_claim_a_new_domain(state, box):
    view, runtime, _, _ = state
    view.shapes.fail_add = True
    with pytest.raises(RuntimeError, match='creation failed'):
        render_search_domain(view, box)
    assert runtime.domain_layers == []
    assert runtime.domain_layer is None
    assert runtime.search_domain is None


def test_geometry_failure_preserves_previous_owned_visual(state, box):
    view, runtime, _, _ = state
    layer = render_search_domain(view, box)

    class UnsupportedDomain:
        @property
        def bounds(self):
            raise ValueError('unsupported domain geometry')

    with pytest.raises(ValueError, match='unsupported domain geometry'):
        render_search_domain(view, UnsupportedDomain())
    assert view.shapes.get(layer.tag) is layer
    assert view.shapes.deleted == []
    assert runtime.search_domain is box


def test_render_deletion_failure_is_not_swallowed(state, box):
    view, runtime, _, _ = state
    layer = render_search_domain(view, box)
    layer.fail_delete = True
    with pytest.raises(RuntimeError, match='deletion failed'):
        render_search_domain(view, box)
    assert view.shapes.get(layer.tag) is layer
    assert runtime.domain_layer is layer
    assert runtime.domain_layers == [layer]
    layer.fail_delete = False


def test_domain_panel_renders_explicitly_and_reports_missing_input(state, box):
    view, runtime, panels, states = state
    panels[1].handle_action(view, 'render_domain', {})
    assert states[1][-1]['status'] == 'error'
    assert 'Supply a search domain' in states[1][-1]['error']
    runtime.search_domain = box
    panels[1].handle_action(view, 'render_domain', {})
    assert states[1][-1]['domain_available'] is True
    assert states[0][-1]['domain_available'] is True


def test_provider_query_failure_is_visible_and_not_treated_as_absent(state, box):
    view, runtime, panels, states = state
    layer = render_search_domain(view, box)
    layer.fail_info = True
    panels[0].handle_action(view, 'refresh', {})
    assert states[0][-1]['status'] == 'error'
    assert states[0][-1]['error'] == 'shape query failed'
    assert states[0][-1]['domain_available'] is False
    assert runtime.domain_layer is layer
    layer.fail_info = False
    panels[0].handle_action(view, 'refresh', {})
    assert states[0][-1]['status'] == 'idle'
    assert states[0][-1]['domain_available'] is True


@pytest.mark.parametrize('missing', ['receptor', 'partner'])
def test_missing_molecular_inputs_reject_before_loading(state, missing):
    view, runtime, _, _ = state
    calls = []
    view.load = lambda *args, **kwargs: calls.append(kwargs)
    inputs = {'receptor': object(), 'partner': object()}
    inputs[missing] = None
    before = runtime.result
    with pytest.raises(ValueError, match='required'):
        render_docking_result(view, before, **inputs)
    assert calls == []
    assert runtime.result is before


def test_domain_display_units_are_explicit_under_nondefault_policy(state, box):
    view, _, panels, states = state
    with puw.context(standard_units=['pm', 'fs']):
        render_search_domain(view, box)
        panels[1].handle_action(view, 'refresh', {})
        assert states[1][-1]['center'] == [10, 20, 30]
        assert states[1][-1]['length_unit'] == 'angstrom'
        assert states[1][-1]['volume_unit'] == 'angstrom**3'
        assert states[1][-1]['lengths'] == [20, 20, 20]
        assert states[1][-1]['volume'] == pytest.approx(8000)
        assert puw.configure.report()['standard_units'] == ['pm', 'fs']


def test_public_resolved_widgets_keep_separate_reactive_state_and_owned_cleanup(box):
    import molsysmt as msm
    import molsysviewer as msv

    source = msm.convert(
        msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
        to_form='molsysmt.MolSys',
    )
    msv.addons.register_module('molsysviewer_dockingmt')
    view = msv.MolSysView()
    widgets = []
    try:
        view.load(msm.extract(source, structure_indices=[0, 0]))
        view.addons.enable('dockingmt')
        runtime = ensure_runtime(view)
        # Only display metadata is bound here; real pose construction is guarded
        # separately in test_viewer_addon and test_viewer_reference.
        runtime.result = DockingResult(
            [
                DockingPose(puw.quantity([[0, 0, 0]], 'nm'), pose_id=name)
                for name in ['a', 'b']
            ]
        )
        for panel_id in ['explorer', 'domain']:
            widget = view.addons.resolve_panel_widget('dockingmt', panel_id)
            widgets.append(widget)
            widget.on_mount(view)
        assert set(view.widget.addon_states['dockingmt']) == {'explorer', 'domain'}
        set_active_pose(view, 2)
        state = view.widget.addon_states['dockingmt']
        assert state['explorer']['active_index'] == 1
        render_search_domain(view, box)
        state = view.widget.addon_states['dockingmt']
        assert state['explorer']['domain_available'] is True
        assert state['domain']['length_unit'] == 'angstrom'
        assert state['domain']['visible'] is True
        set_search_domain_visibility(view, False)
        assert view.widget.addon_states['dockingmt']['domain']['visible'] is False
        clear_docking(view)
        assert view.widget.addon_states['dockingmt']['explorer']['poses'] == []
        assert not view.shapes.contains('dockingmt:search_domain')
    finally:
        for widget in widgets:
            widget.close()
        view.close()
