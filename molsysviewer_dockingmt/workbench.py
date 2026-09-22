"""Workbench section helpers for the DockingMT MolSysViewer integration."""

from __future__ import annotations

from typing import Any

from .runtime import ensure_runtime


def get_docking_summary_section(view: Any) -> dict[str, Any]:
    """Build a workbench section dictionary summarizing the active docking state."""
    runtime = ensure_runtime(view)
    result = runtime.result

    n_poses = len(result.poses) if result is not None else 0
    top_score = None
    if result is not None and result.top_pose and result.top_pose.scores:
        top_score = result.top_pose.scores.get('vina') or next(
            iter(result.top_pose.scores.values())
        )

    subtitle_parts = [f'{n_poses} poses']
    if top_score is not None:
        subtitle_parts.append(f'top score={top_score:.2f} kcal/mol')
    if runtime.search_domain is not None:
        subtitle_parts.append('domain active')

    return {
        'id': 'docking-summary',
        'title': 'Docking Summary',
        'item_title': f'Pose {runtime.active_pose_rank} of {n_poses}'
        if n_poses > 0
        else 'No Docking Result',
        'item_subtitle': ', '.join(subtitle_parts),
        'n_poses': n_poses,
        'active_rank': runtime.active_pose_rank,
        'top_score': top_score,
    }
