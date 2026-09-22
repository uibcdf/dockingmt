"""Runtime state management for the DockingMT MolSysViewer integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DockingMTAddonRuntime:
    """Public per-view state namespace for the DockingMT add-on.

    Accessible as ``view.addons.dockingmt`` (one instance per view). Holds
    the active docking results, loaded search domain, reference ligand,
    active pose index, and visibility toggles.
    """

    enabled: bool = False
    workspace: str = 'dockingmt'
    result: Any = None
    search_domain: Any = None
    reference: Any = None
    active_pose_rank: int = 1
    domain_visible: bool = True
    reference_visible: bool = True
    tag_prefix: str = 'dockingmt'
    last_context_action: dict[str, Any] | None = None
    event_log: list[dict[str, Any]] = field(default_factory=list)


def create_dockingmt_state(view: Any) -> DockingMTAddonRuntime:
    """Factory consumed by AddonSpec.state_factory."""
    state = DockingMTAddonRuntime()
    try:
        view._dockingmt_addon_runtime = state
    except Exception:
        pass
    return state


def ensure_runtime(view: Any) -> DockingMTAddonRuntime:
    """Return the DockingMT runtime state namespace for ``view``.

    Prefers the public ``view.addons.dockingmt`` namespace; falls back to
    the legacy/test-double attribute ``view._dockingmt_addon_runtime``.
    """
    addons = getattr(view, 'addons', None)
    if addons is not None:
        try:
            namespace = getattr(addons, 'dockingmt', None)
        except Exception:
            namespace = None
        if isinstance(namespace, DockingMTAddonRuntime):
            try:
                view._dockingmt_addon_runtime = namespace
            except Exception:
                pass
            return namespace

    runtime = getattr(view, '_dockingmt_addon_runtime', None)
    if not isinstance(runtime, DockingMTAddonRuntime):
        runtime = DockingMTAddonRuntime()
        try:
            view._dockingmt_addon_runtime = runtime
        except Exception:
            pass
    return runtime


def record_event(view: Any, event_name: str, **kwargs: Any) -> None:
    """Append a structured lifecycle/interaction event to the runtime event log."""
    runtime = ensure_runtime(view)
    runtime.event_log.append({'event': event_name, **kwargs})
