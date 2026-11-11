"""BindingMT MolSysViewer integration module."""

from __future__ import annotations

from bindingmt.view import show, view
from molsysviewer_bindingmt import (
    BindingMTAddonRuntime,
    addon,
    build_docking_complex_system,
    clear_docking,
    compute_box_wireframe_coordinate_pairs,
    ensure_runtime,
    get_addon,
    get_lifecycle,
    lifecycle,
    on_context_action,
    on_disable,
    on_enable,
    render_docking_result,
    render_search_domain,
    set_active_pose,
    set_reference_visibility,
    set_search_domain_visibility,
)

__all__ = [
    'BindingMTAddonRuntime',
    'addon',
    'build_docking_complex_system',
    'clear_docking',
    'compute_box_wireframe_coordinate_pairs',
    'ensure_runtime',
    'get_addon',
    'get_lifecycle',
    'lifecycle',
    'on_context_action',
    'on_disable',
    'on_enable',
    'render_docking_result',
    'render_search_domain',
    'set_active_pose',
    'set_reference_visibility',
    'set_search_domain_visibility',
    'show',
    'view',
]
