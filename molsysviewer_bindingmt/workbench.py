"""Workbench section helpers for the BindingMT MolSysViewer integration."""

from __future__ import annotations

from typing import Any

from ._presentation import pose_record, score_text, selected_pose_record
from ._scene import sync_scene_state
from .runtime import ensure_runtime


def get_docking_summary_section(view: Any) -> dict[str, Any]:
    """Build a workbench section dictionary summarizing the active docking state."""
    runtime = ensure_runtime(view)
    controls = sync_scene_state(view)
    result = runtime.result

    n_poses = len(result.poses) if result is not None else 0
    selected = selected_pose_record(runtime)
    top_scores = []
    if result is not None and result.top_pose is not None:
        top_scores = pose_record(result.top_pose, result.poses.index(result.top_pose))[
            'scores'
        ]
    # Retain the old scalar Vina summary without arbitrary-score substitution.
    top_score = next((s['value'] for s in top_scores if s['name'] == 'vina'), None)

    subtitle_parts = [f'{n_poses} poses']
    if top_scores:
        subtitle_parts.append('top pose: ' + '; '.join(map(score_text, top_scores)))
    if runtime.search_domain is not None:
        subtitle_parts.append('domain active')

    section = {
        'id': 'docking-summary',
        'title': 'Docking Summary',
        'item_title': f'Pose {selected["position"]} of {n_poses}'
        if selected is not None
        else 'No Docking Result',
        'item_subtitle': ', '.join(subtitle_parts),
        'n_poses': n_poses,
        'active_rank': runtime.active_pose_rank,
        'top_score': top_score,
        'top_scores': top_scores,
        'active_pose_index': runtime.active_pose_index
        if selected is not None
        else None,
        'selected_pose': selected,
    }
    if runtime.interaction_binding is not None:
        section.update(
            interaction_association=runtime.interaction_binding.association,
            interaction_geometry_available=controls['interaction_geometry_available'],
            interaction_analyses=controls['interaction_analyses'],
        )
    return section
