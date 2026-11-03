"""Read public scene state and enforce ownership of docking controls."""

from numbers import Integral
from typing import Any

from .runtime import ensure_runtime


class ScenePrerequisiteError(RuntimeError):
    """A docking-owned visual is absent; provider failures remain distinct."""


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
            'Render the search domain before changing its visibility.'
        )
    return layer


def reference_region(view: Any) -> Any:
    runtime = ensure_runtime(view)
    region = runtime.reference_region
    regions = getattr(view, 'regions', None)
    if region is None or regions is None or regions.get(region.tag) is not region:
        raise ScenePrerequisiteError(
            'Load an explicit reference before changing its visibility.'
        )
    return region


def sync_scene_state(view: Any) -> Any:
    """Read current public handles; do not compute or change the molecular scene."""
    runtime = ensure_runtime(view)
    index = getattr(getattr(view, 'player', None), 'index', None)
    if (
        runtime.result is not None
        and isinstance(index, Integral)
        and not isinstance(index, bool)
    ):
        runtime.active_pose_rank = int(index) + 1
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
    return controls
