"""MolSysViewer integration for DockingMT."""

from __future__ import annotations

from .adapters import (
    build_docking_complex_system,
    clear_docking,
    compute_box_wireframe_coordinate_pairs,
    render_docking_result,
    render_search_domain,
    set_active_pose,
    set_reference_visibility,
    set_search_domain_visibility,
)
from .addon import (
    get_addon,
    get_lifecycle,
    on_context_action,
    on_disable,
    on_enable,
)
from .runtime import (
    DockingMTAddonRuntime,
    create_dockingmt_state,
    ensure_runtime,
    record_event,
)

__all__ = [
    'DockingMTAddonRuntime',
    'addon',
    'build_docking_complex_system',
    'clear_docking',
    'compute_box_wireframe_coordinate_pairs',
    'create_dockingmt_state',
    'ensure_runtime',
    'get_addon',
    'get_lifecycle',
    'lifecycle',
    'on_context_action',
    'on_disable',
    'on_enable',
    'record_event',
    'render_docking_result',
    'render_search_domain',
    'set_active_pose',
    'set_reference_visibility',
    'set_search_domain_visibility',
]


addon = get_addon()
lifecycle = get_lifecycle()
