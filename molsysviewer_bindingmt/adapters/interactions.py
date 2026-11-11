"""Display one admitted interaction carrier without projecting it over poses."""

from typing import Any

from bindingmt._private.smonitor import (
    ViewerCapabilityError,
    ViewerStateError,
    signal,
)

from ..runtime import ensure_runtime, record_event
from .shapes import _clear_domain_layers, render_search_domain


def _clear_interaction_layers(view: Any) -> None:
    """Release owned visuals, preserving scientific analyses and foreign handles."""
    runtime = ensure_runtime(view)
    manager = getattr(view, 'interactions', None)
    if runtime.interaction_layers and not callable(getattr(manager, 'get', None)):
        raise ViewerCapabilityError(
            capability='interaction visual registry', operation='clear_interactions'
        )
    for layer in runtime.interaction_layers.copy():
        if manager is not None and manager.get(layer.tag) is layer:
            layer.delete()
        runtime.interaction_layers.remove(layer)


@signal(tags=['addon', 'viewer', 'interactions'])
def _render_pose_interactions(
    view: Any, binding: Any, *, search_domain: Any = None
) -> Any:
    """Load the complete admitted carrier and retain the whole original result.

    Provider calls are not transactional. Native failures propagate, and handles
    of partially created visuals remain owned for explicit cleanup.
    """
    manager = getattr(view, 'interactions', None)
    if manager is None or any(
        not callable(getattr(manager, name, None))
        for name in ('add', 'get', 'analyses')
    ):
        raise ViewerCapabilityError(
            capability='scientific interactions', operation='view_interactions'
        )
    player = getattr(view, 'player', None)
    if not callable(getattr(player, 'go_to_structure', None)):
        raise ViewerCapabilityError(capability='player', operation='view_interactions')

    result = binding.result
    association = binding.association
    carrier = binding.to_molecular_system()
    _clear_interaction_layers(view)
    _clear_domain_layers(view)
    view.load(carrier, label='docking_interactions', mode='replace')
    loaded = getattr(view, 'molsys', None)
    if loaded is None:
        raise ViewerCapabilityError(
            capability='public loaded molecular system', operation='view_interactions'
        )
    metadata = {row['name']: row for row in manager.analyses()}
    if set(metadata) != set(binding.analysis_names) or any(
        row['n_atoms'] != association['carrier_n_atoms'] or row['n_structures'] != 1
        for row in metadata.values()
    ):
        raise ViewerStateError(
            resource='complete interaction carrier axes', operation='view_interactions'
        )
    runtime = ensure_runtime(view)
    for index, name in enumerate(binding.analysis_names):
        layer = manager.add(
            name,
            tag=f'{runtime.tag_prefix}:interactions:{index}',
            structure_indices=[0],
        )
        runtime.interaction_layers.append(layer)
    if search_domain is not None:
        render_search_domain(view, search_domain)
    player.go_to_structure(0)

    runtime.result = result
    runtime.interaction_binding = binding
    runtime.interaction_carrier = loaded
    runtime.active_pose_rank = binding.pose_index + 1
    runtime.search_domain = search_domain
    runtime.domain_visible = search_domain is not None
    runtime.reference = None
    runtime.reference_region = None
    runtime.reference_visible = False
    record_event(
        view,
        'render_pose_interactions',
        index=binding.pose_index,
        frame=0,
        n_poses=len(result.poses),
        analysis_names=list(binding.analysis_names),
    )
    return view
