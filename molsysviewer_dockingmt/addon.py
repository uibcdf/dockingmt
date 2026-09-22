"""Addon specification and lifecycle for the DockingMT MolSysViewer integration."""

from __future__ import annotations

import inspect
from typing import Any

from .runtime import create_dockingmt_state, ensure_runtime, record_event


def on_enable(view: Any) -> None:
    """Invoked when the DockingMT addon or workspace is enabled."""
    runtime = ensure_runtime(view)
    runtime.enabled = True
    record_event(view, 'enable', workspace=runtime.workspace)


def on_disable(view: Any) -> None:
    """Invoked when the DockingMT addon is disabled."""
    runtime = ensure_runtime(view)
    runtime.enabled = False
    record_event(view, 'disable', workspace=runtime.workspace)


def on_context_action(view: Any, action_id: str, payload: dict[str, Any]) -> None:
    """Handle context menu action triggers dispatched by MolSysViewer."""
    from .adapters.complex import set_active_pose, set_reference_visibility
    from .adapters.shapes import set_search_domain_visibility

    runtime = ensure_runtime(view)
    runtime.last_context_action = {'action_id': action_id, 'payload': dict(payload)}
    record_event(view, 'context_action', action_id=action_id)

    if action_id == 'toggle-search-domain':
        new_vis = not runtime.domain_visible
        set_search_domain_visibility(view, new_vis)

    elif action_id == 'toggle-reference':
        new_vis = not runtime.reference_visible
        set_reference_visibility(view, new_vis)

    elif action_id == 'set-pose':
        rank = payload.get('rank', 1)
        set_active_pose(view, rank)


_addon_instance = None
_lifecycle_instance = None


def _accepts_keyword(callable_obj: Any, keyword: str) -> bool:
    try:
        return keyword in inspect.signature(callable_obj).parameters
    except (TypeError, ValueError):
        return False


def get_lifecycle():
    """Build or retrieve the singleton AddonLifecycleSpec."""
    global _lifecycle_instance
    if _lifecycle_instance is not None:
        return _lifecycle_instance

    from molsysviewer.addons import AddonLifecycleSpec

    _lifecycle_instance = AddonLifecycleSpec(
        on_enable=on_enable,
        on_disable=on_disable,
        on_context_action=on_context_action,
    )
    return _lifecycle_instance


def get_addon():
    """Build or retrieve the singleton AddonSpec."""
    global _addon_instance
    if _addon_instance is not None:
        return _addon_instance

    from molsysviewer.addons import (
        AddonContextActionSpec,
        AddonExportHelperSpec,
        AddonPanelSpec,
        AddonSectionSpec,
        AddonShapeProviderSpec,
        AddonSpec,
        AddonWorkspaceSpec,
    )

    addon_kwargs: dict[str, Any] = {
        'name': 'dockingmt',
        'package': 'dockingmt',
        'version': '0.1.0',
        'description': 'Molecular docking workspace for poses, search domains, and scores in MolSysViewer.',
    }
    if _accepts_keyword(AddonSpec, 'state_factory'):
        addon_kwargs['state_factory'] = create_dockingmt_state

    _addon_instance = AddonSpec(
        **addon_kwargs,
        workspaces=(
            AddonWorkspaceSpec(
                id='dockingmt',
                title='Docking',
                entry_panel='explorer',
                description='Docking results, candidate pose navigation, and search domain inspection.',
                order=30,
            ),
        ),
        panels=(
            AddonPanelSpec(
                id='explorer',
                title='Docking Explorer',
                entry='molsysviewer_dockingmt.panels.explorer',
                description='Browse candidate docking poses, scores, ranks, and RMSD comparison.',
                order=10,
                widget_class='molsysviewer_dockingmt.panels.explorer.DockingExplorerPanel',
            ),
            AddonPanelSpec(
                id='domain',
                title='Search Domain',
                entry='molsysviewer_dockingmt.panels.domain',
                description='Search domain bounding box and geometry.',
                order=20,
                widget_class='molsysviewer_dockingmt.panels.domain.SearchDomainPanel',
            ),
        ),
        context_actions=(
            AddonContextActionSpec(
                id='toggle-search-domain',
                title='Toggle Search Domain',
                entry='molsysviewer_dockingmt.context.toggle_search_domain',
                target_kinds=('structure', 'shape'),
                group='dockingmt',
                order=10,
            ),
            AddonContextActionSpec(
                id='toggle-reference',
                title='Toggle Reference Ligand',
                entry='molsysviewer_dockingmt.context.toggle_reference',
                target_kinds=('structure',),
                group='dockingmt',
                order=20,
            ),
        ),
        addon_sections=(
            AddonSectionSpec(
                id='docking-summary',
                title='Docking Summary',
                entry='molsysviewer_dockingmt.workbench.docking_summary',
                target_panel='addons',
                order=10,
            ),
        ),
        shape_providers=(
            AddonShapeProviderSpec(
                id='search-domain-box',
                title='Search Domain Box',
                entry='molsysviewer_dockingmt.shapes.search_domain_provider',
                kinds=('box', 'search_domain'),
                order=10,
            ),
        ),
        export_helpers=(
            AddonExportHelperSpec(
                id='docking-summary-export',
                title='Docking Summary Export',
                entry='molsysviewer_dockingmt.export.docking_summary_export',
                formats=('json',),
                order=10,
            ),
        ),
        meta={
            'domain': 'docking',
            'repo': 'dockingmt',
        },
    )
    return _addon_instance


addon = get_addon()
lifecycle = get_lifecycle()
