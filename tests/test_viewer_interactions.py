"""One-frame interaction views using protocol doubles, never molecular loading."""

from copy import deepcopy
from types import SimpleNamespace

import pytest
import pyunitwizard as puw

import dockingmt as dmt
from dockingmt._private.smonitor import (
    ArgumentError,
    ViewerCapabilityError,
    ViewerStateError,
)
from molsysviewer_dockingmt import (
    clear_docking,
    on_context_action,
    on_disable,
    set_active_pose,
)
from molsysviewer_dockingmt.adapters.interactions import _render_pose_interactions
from molsysviewer_dockingmt.export import build_docking_export_payload
from molsysviewer_dockingmt.panels import DockingExplorerPanel, SearchDomainPanel
from molsysviewer_dockingmt.runtime import ensure_runtime
from molsysviewer_dockingmt.workbench import get_docking_summary_section


class _Visual:
    def __init__(self, manager, tag):
        self.manager = manager
        self.tag = tag
        self.fail_delete = False
        self.deleted = False

    def delete(self):
        if self.fail_delete:
            raise RuntimeError('provider visual deletion failed')
        self.deleted = True
        del self.manager.items[self.tag]


class _Interactions:
    def __init__(self, view):
        self.view = view
        self.items = {}
        self.calls = []
        self.fail_add = None
        self.fail_read = False

    def analyses(self):
        if self.fail_read:
            raise RuntimeError('provider analysis inspection failed')
        return deepcopy(self.view.molsys['analyses'])

    def add(self, name, *, tag, structure_indices):
        self.calls.append((name, tag, structure_indices))
        if name == self.fail_add:
            raise RuntimeError('provider visual creation failed')
        visual = _Visual(self, tag)
        self.items[tag] = visual
        return visual

    def get(self, tag):
        return self.items.get(tag)


class _View:
    def __init__(self):
        self.molsys = None
        self.moves = []
        self.loads = []
        self.callbacks = []
        self.fail_load = False
        self.fail_move = False
        self.interactions = _Interactions(self)
        self.player = SimpleNamespace(index=0, go_to_structure=self.move)
        self.regions = SimpleNamespace(get=lambda tag: None)
        self.shapes = SimpleNamespace(get=lambda tag: None)

    def move(self, index):
        if self.fail_move:
            raise RuntimeError('provider player failed')
        self.moves.append(index)
        self.emit_frame(index)

    def emit_frame(self, index):
        self.player.index = index
        for callback in self.callbacks.copy():
            callback({'event': 'frame_changed', 'frame': index})

    def on_frame_change(self, callback):
        self.callbacks.append(callback)

    def off_frame_change(self, callback):
        self.callbacks.remove(callback)

    def load(self, carrier, *, label, mode):
        self.loads.append((label, mode))
        if self.fail_load:
            raise RuntimeError('provider load failed')
        self.molsys = deepcopy(carrier)
        self.interactions.items.clear()


@pytest.fixture
def binding(monkeypatch):
    """Already admitted binding protocol; constructor/native evidence is separate."""
    import molsysmt as msm

    def copy(carrier):
        assert isinstance(carrier, dict) and carrier['test_protocol_carrier'] is True
        return deepcopy(carrier)

    monkeypatch.setattr(msm, 'copy', copy)
    poses = [
        dmt.DockingPose(
            puw.quantity([[float(index), 0, 0]], 'angstrom'),
            pose_id=f'original-{index}',
            rank=[7, None, 1, 2, 9][index],
            scores={'vina': -index - 1.0},
        )
        for index in range(5)
    ]
    original = dmt.DockingResult(poses, provenance={'original': 'preserve-me'})
    result = object.__new__(dmt.PoseInteractions)
    result._result_record = original.to_dict()
    result._pose_index = 3
    result._analysis_names = ('hbonds', 'hydrophobic')
    result._association = {
        'pose_index': 3,
        'pose_id': 'original-3',
        'original_pose_count': 5,
        'carrier_n_atoms': 12,
        'carrier_n_structures': 1,
        'analysis_evaluated': {'hbonds': False, 'hydrophobic': True},
    }
    result._carrier = {
        'test_protocol_carrier': True,
        'analyses': [
            {
                'name': name,
                'method': 'declared-method',
                'n_atoms': 12,
                'n_structures': 1,
                'n_evaluated_structures': evaluated,
                'n_occurrences': 0,
            }
            for name, evaluated in [('hbonds', 0), ('hydrophobic', 1)]
        ],
    }
    return result


def panel_state(view):
    panel = DockingExplorerPanel(view=view)
    try:
        return panel._read_state(view)
    finally:
        panel.close()


def test_view_binding_retains_all_results_and_maps_nonfirst_pose_to_frame_zero(binding):
    before = binding.result.to_dict()
    view = _View()
    assert dmt.view(binding, view=view) is view
    runtime = ensure_runtime(view)
    assert runtime.result.to_dict() == before
    assert len(runtime.result.poses) == 5
    assert runtime.active_pose_index == 3
    assert runtime.result.poses[3].rank == 2
    assert runtime.domain_visible is False
    assert view.moves == [0]
    assert view.loads == [('docking_interactions', 'replace')]
    assert [call[0] for call in view.interactions.calls] == ['hbonds', 'hydrophobic']
    assert all(call[2] == [0] for call in view.interactions.calls)
    view.molsys['analyses'][0]['n_occurrences'] = 11
    runtime.result.poses[0].scores['changed'] = 99
    assert binding.result.to_dict() == before
    assert binding._carrier['analyses'][0]['n_occurrences'] == 0


def test_explorer_coverage_is_live_and_missing_is_not_empty(binding):
    view = _View()
    dmt.view(binding, view=view)
    state = panel_state(view)
    assert state['active_index'] == 3
    assert len(state['poses']) == 5
    assert [p['geometry_available'] for p in state['poses']] == [
        False,
        False,
        False,
        True,
        False,
    ]
    assert [row['evaluated'] for row in state['interaction_analyses']] == [False, True]
    assert all(row['n_occurrences'] == 0 for row in state['interaction_analyses'])
    view.molsys['analyses'][0]['n_evaluated_structures'] = 1
    assert panel_state(view)['interaction_analyses'][0]['evaluated'] is True
    view.molsys['analyses'].pop(0)
    assert panel_state(view)['interaction_analyses'][0] == {
        'name': 'hbonds',
        'available': False,
        'evaluated': None,
    }


def test_callbacks_summary_and_export_keep_original_position_and_result(binding):
    view = _View()
    dmt.view(binding, view=view)
    panel = DockingExplorerPanel(view=view)
    try:
        panel.on_mount(view)
        count = len(view.moves)
        view.emit_frame(0)
        assert panel._last_state['active_index'] == 3
        assert len(view.moves) == count
        for record in [
            get_docking_summary_section(view),
            build_docking_export_payload(view),
        ]:
            assert record['selected_pose']['pose_id'] == 'original-3'
            assert record['selected_pose']['rank'] == 2
            assert record['interaction_association'] == binding.association
            assert record['interaction_geometry_available'] is True
        assert build_docking_export_payload(view)['result'] == binding.result.to_dict()
        view.emit_frame(4)
        assert panel._last_state['active_index'] == 3
        assert panel._last_state['interaction_geometry_available'] is False
        assert not any(row['geometry_available'] for row in panel._last_state['poses'])
    finally:
        panel.close()


@pytest.mark.parametrize('rank', [1, 2, 3, 5])
def test_unloaded_pose_navigation_is_refused_before_player(binding, rank):
    view = _View()
    dmt.view(binding, view=view)
    moves = view.moves.copy()
    with pytest.raises(ViewerStateError):
        set_active_pose(view, rank)
    assert view.moves == moves
    assert ensure_runtime(view).active_pose_index == 3
    set_active_pose(view, 4)
    assert view.moves == [*moves, 0]


def test_replaced_scene_is_not_accepted_by_equal_dimensions(binding):
    view = _View()
    dmt.view(binding, view=view)
    view.molsys = deepcopy(view.molsys)
    state = panel_state(view)
    assert state['interaction_geometry_available'] is False
    assert state['interaction_analyses'] == []
    assert not any(row['geometry_available'] for row in state['poses'])
    with pytest.raises(ViewerStateError):
        set_active_pose(view, 4)
    assert build_docking_export_payload(view)['interaction_geometry_available'] is False
    assert ensure_runtime(view).result.to_dict() == binding.result.to_dict()


@pytest.mark.parametrize(
    'option', ['result', 'problem', 'receptor', 'partner', 'reference', 'pose_rank']
)
def test_binding_conflicts_fail_before_creating_or_mutating_view(
    binding, option, monkeypatch
):
    import molsysviewer as msv

    def forbidden(**kwargs):
        pytest.fail('Invalid binding options created a view')

    monkeypatch.setattr(msv, 'new_view', forbidden)
    values = {
        'result': binding.result,
        'problem': SimpleNamespace(search_domain=None),
        'receptor': object(),
        'partner': object(),
        'reference': object(),
        'pose_rank': 4,
    }
    with pytest.raises(ArgumentError):
        dmt.view(binding, **{option: values[option]}, skip_digestion=True)


@pytest.mark.parametrize('capability', ['interactions', 'player'])
def test_missing_provider_capability_fails_before_loading(binding, capability):
    view = _View()
    setattr(view, capability, None)
    with pytest.raises(ViewerCapabilityError):
        dmt.view(binding, view=view)
    assert view.loads == []
    assert ensure_runtime(view).result is None


def test_provider_load_error_propagates_without_publishing_result(binding):
    view = _View()
    view.fail_load = True
    with pytest.raises(RuntimeError, match='provider load failed'):
        dmt.view(binding, view=view)
    assert ensure_runtime(view).result is None
    assert ensure_runtime(view).interaction_binding is None


def test_partial_visual_creation_retains_cleanup_ownership(binding):
    view = _View()
    view.interactions.fail_add = 'hydrophobic'
    with pytest.raises(RuntimeError, match='provider visual creation failed'):
        dmt.view(binding, view=view)
    runtime = ensure_runtime(view)
    assert runtime.result is None and runtime.interaction_binding is None
    assert len(runtime.interaction_layers) == 1
    visual = runtime.interaction_layers[0]
    clear_docking(view)
    assert visual.deleted and runtime.interaction_layers == []
    assert len(view.molsys['analyses']) == 2


def test_clear_preserves_foreign_visuals_and_scientific_analyses(binding):
    view = _View()
    dmt.view(binding, view=view)
    runtime = ensure_runtime(view)
    foreign = view.interactions.add('hbonds', tag='foreign', structure_indices=[0])
    original = runtime.interaction_layers[0]
    replacement = _Visual(view.interactions, original.tag)
    view.interactions.items[original.tag] = replacement
    clear_docking(view)
    assert not foreign.deleted and not replacement.deleted and not original.deleted
    assert len(view.molsys['analyses']) == 2
    assert runtime.result is None and runtime.interaction_binding is None
    assert runtime.interaction_layers == []


def test_failed_cleanup_keeps_handles_for_explicit_retry(binding):
    view = _View()
    dmt.view(binding, view=view)
    runtime = ensure_runtime(view)
    first = runtime.interaction_layers[0]
    first.fail_delete = True
    with pytest.raises(RuntimeError, match='provider visual deletion failed'):
        on_disable(view)
    assert (
        runtime.interaction_binding is binding and len(runtime.interaction_layers) == 2
    )
    first.fail_delete = False
    on_disable(view)
    assert runtime.interaction_binding is None and runtime.interaction_layers == []
    assert runtime.enabled is False


def test_provider_read_failure_does_not_leave_geometry_marked_available(binding):
    view = _View()
    dmt.view(binding, view=view)
    panel = DockingExplorerPanel(view=view)
    try:
        panel.on_mount(view)
        view.interactions.fail_read = True
        panel.handle_action(view, 'refresh', {})
        assert panel._last_state['status'] == 'error'
        assert panel._last_state['interaction_geometry_available'] is False
        assert panel._last_state['interaction_analyses'] == []
        assert not any(row['geometry_available'] for row in panel._last_state['poses'])
        domain_panel = SearchDomainPanel(view=view)
        try:
            domain_panel._refresh(view=view)
            assert domain_panel._last_state['status'] == 'idle'
        finally:
            domain_panel.close()
    finally:
        panel.close()


def test_ordinary_result_render_releases_single_frame_mapping(binding, monkeypatch):
    from molsysviewer_dockingmt.adapters import complex

    view = _View()
    dmt.view(binding, view=view)
    layers = ensure_runtime(view).interaction_layers.copy()
    monkeypatch.setattr(
        complex, 'build_docking_complex_system', lambda **kwargs: {'analyses': []}
    )
    result = binding.result
    complex.render_docking_result(view, result, receptor=object(), partner=object())
    runtime = ensure_runtime(view)
    assert all(layer.deleted for layer in layers)
    assert runtime.interaction_binding is None and runtime.interaction_carrier is None
    set_active_pose(view, 5)
    assert view.moves[-1] == 4
    assert panel_state(view)['active_index'] == 4


def test_loaded_metadata_axes_must_match_before_visual_creation(binding):
    binding._carrier['analyses'][0]['n_structures'] = 5
    view = _View()
    with pytest.raises(ViewerStateError):
        _render_pose_interactions(view, binding)
    assert view.interactions.calls == []
    assert ensure_runtime(view).result is None


def test_missing_cleanup_registry_preserves_ownership_for_retry(binding):
    view = _View()
    dmt.view(binding, view=view)
    manager = view.interactions
    view.interactions = None
    with pytest.raises(ViewerCapabilityError):
        clear_docking(view)
    assert len(ensure_runtime(view).interaction_layers) == 2
    view.interactions = manager
    clear_docking(view)
    assert ensure_runtime(view).interaction_layers == []


def test_context_and_panel_actions_use_the_bound_position(binding):
    view = _View()
    dmt.view(binding, view=view)
    panel = DockingExplorerPanel(view=view)
    try:
        on_context_action(view, 'set-pose', {'rank': 4})
        assert view.moves == [0, 0]
        with pytest.raises(ViewerStateError):
            on_context_action(view, 'set-pose', {'rank': 1})
        panel.handle_action(view, 'set_pose', {'index': 0})
        assert panel._last_state['status'] == 'error'
        assert view.moves == [0, 0]
        panel.handle_action(view, 'set_pose', {'index': 3})
        assert panel._last_state['active_index'] == 3
        assert panel._last_state['status'] == 'idle'
        assert view.moves == [0, 0, 0]
    finally:
        panel.close()


def test_explicit_search_visual_does_not_change_the_bound_carrier(binding, monkeypatch):
    from molsysviewer_dockingmt.adapters import interactions

    domain = dmt.BoxRegion(
        center=puw.quantity([0, 0, 0], 'angstrom'),
        lengths=puw.quantity([1, 1, 1], 'angstrom'),
    )
    calls = []
    monkeypatch.setattr(
        interactions, 'render_search_domain', lambda view, box: calls.append(box)
    )
    view = _View()
    dmt.view(binding, view=view, search_domain=domain)
    assert calls == [domain]
    assert view.molsys == binding._carrier
    assert ensure_runtime(view).active_pose_index == 3


def test_view_keeps_the_callers_nondefault_unit_policy_and_source_record(binding):
    before = binding.result.to_dict()
    with puw.context(standard_units=['pm', 'fs']):
        policy = puw.configure.report()
        dmt.view(binding, view=_View())
        assert puw.configure.report()['standard_units'] == policy['standard_units']
        assert puw.configure.report()['provenance'] == policy['provenance']
        assert binding.result.to_dict() == before


def test_provider_player_failure_does_not_publish_a_completed_binding(binding):
    view = _View()
    view.fail_move = True
    with pytest.raises(RuntimeError, match='provider player failed'):
        dmt.view(binding, view=view)
    runtime = ensure_runtime(view)
    assert runtime.result is None and runtime.interaction_binding is None
    assert len(runtime.interaction_layers) == 2
    clear_docking(view)
    assert runtime.interaction_layers == []
