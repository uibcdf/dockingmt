"""Export helpers for the DockingMT MolSysViewer integration."""

from __future__ import annotations

from typing import Any

from ._presentation import selected_pose_record
from ._scene import sync_scene_state
from .runtime import ensure_runtime


def build_docking_export_payload(view: Any) -> dict[str, Any]:
    """Build a serialized dictionary payload of the active docking session for export."""
    runtime = ensure_runtime(view)
    controls = sync_scene_state(view)
    result = runtime.result

    payload = {
        'title': 'DockingMT Result Export',
        'active_pose_rank': runtime.active_pose_rank,
        'selected_pose': selected_pose_record(runtime),
        'domain_visible': runtime.domain_visible,
        'reference_visible': runtime.reference_visible,
        'result': result.to_dict() if result is not None else None,
        'search_domain': runtime.search_domain.to_dict()
        if runtime.search_domain is not None
        else None,
    }
    if runtime.interaction_binding is not None:
        payload.update(
            interaction_association=runtime.interaction_binding.association,
            interaction_geometry_available=controls['interaction_geometry_available'],
            interaction_analyses=controls['interaction_analyses'],
        )
    return payload
