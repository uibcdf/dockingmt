"""Read public scene state and enforce ownership of docking controls."""

from numbers import Integral
from typing import Any

from bindingmt._private.smonitor import ViewerStateError

from .runtime import ensure_runtime


class ScenePrerequisiteError(ViewerStateError):
    """A docking-owned visual is absent; provider failures remain distinct."""


def _interaction_carrier_available(view: Any) -> bool:
    runtime = ensure_runtime(view)
    return (
        runtime.interaction_binding is not None
        and runtime.interaction_carrier is not None
        and getattr(view, 'molsys', None) is runtime.interaction_carrier
    )


def domain_layer(view: Any, tag: str | None = None) -> Any:
    runtime = ensure_runtime(view)
    shapes = getattr(view, 'shapes', None)
    layer = (
        runtime.domain_layer
        if tag is None
        else next((item for item in runtime.domain_layers if item.tag == tag), None)
    )
    if layer is None or shapes is None or shapes.get(layer.tag) is not layer:
        raise ScenePrerequisiteError(
            resource='search domain', operation='set_search_domain_visibility'
        )
    return layer


def reference_region(view: Any) -> Any:
    runtime = ensure_runtime(view)
    region = runtime.reference_region
    regions = getattr(view, 'regions', None)
    if region is None or regions is None or regions.get(region.tag) is not region:
        raise ScenePrerequisiteError(
            resource='explicit reference', operation='set_reference_visibility'
        )
    return region


def sync_scene_state(view: Any, *, include_interactions: bool = True) -> Any:
    """Read current public handles; do not compute or change the molecular scene."""
    runtime = ensure_runtime(view)
    index = getattr(getattr(view, 'player', None), 'index', None)
    if (
        runtime.result is not None
        and isinstance(index, Integral)
        and not isinstance(index, bool)
    ):
        if runtime.interaction_binding is None:
            runtime.active_pose_rank = int(index) + 1
        elif _interaction_carrier_available(view) and index == 0:
            runtime.active_pose_rank = runtime.interaction_binding.pose_index + 1
    controls = {}
    try:
        layer = domain_layer(view)
    except ScenePrerequisiteError as exc:
        runtime.domain_visible = False
        controls.update(domain_available=False, domain_reason=str(exc))
    else:
        runtime.domain_visible = layer.info()['visible']
        controls.update(domain_available=True, domain_reason=None)
    try:
        region = reference_region(view)
    except ScenePrerequisiteError as exc:
        runtime.reference_visible = False
        controls.update(reference_available=False, reference_reason=str(exc))
    else:
        runtime.reference_visible = region.visible
        controls.update(reference_available=True, reference_reason=None)
    if runtime.interaction_binding is not None:
        available = (
            _interaction_carrier_available(view)
            and isinstance(index, Integral)
            and not isinstance(index, bool)
            and index == 0
        )
        controls.update(
            interaction_geometry_available=available,
            interaction_geometry_reason=None
            if available
            else 'The loaded system no longer matches this pose interaction view.',
            interaction_analyses=[],
        )
        if available and include_interactions:
            rows = {row['name']: row for row in view.interactions.analyses()}
            controls['interaction_analyses'] = [
                {
                    'name': name,
                    'method': rows[name]['method'],
                    'n_occurrences': rows[name]['n_occurrences'],
                    'available': True,
                    'evaluated': rows[name]['n_evaluated_structures'] == 1,
                }
                if name in rows
                else {'name': name, 'available': False, 'evaluated': None}
                for name in runtime.interaction_binding.analysis_names
            ]
    return controls
