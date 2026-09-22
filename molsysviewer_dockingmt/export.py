"""Export helpers for the DockingMT MolSysViewer integration."""

from __future__ import annotations

from typing import Any

from .runtime import ensure_runtime


def build_docking_export_payload(view: Any) -> dict[str, Any]:
    """Build a serialized dictionary payload of the active docking session for export."""
    runtime = ensure_runtime(view)
    result = runtime.result

    return {
        'title': 'DockingMT Result Export',
        'active_pose_rank': runtime.active_pose_rank,
        'domain_visible': runtime.domain_visible,
        'reference_visible': runtime.reference_visible,
        'result': result.to_dict() if result is not None else None,
        'search_domain': runtime.search_domain.to_dict()
        if runtime.search_domain is not None
        else None,
    }
