"""Detached display records for docking results; no scientific computation."""

from __future__ import annotations

from typing import Any


def pose_record(pose: Any, index: int) -> dict[str, Any]:
    """Keep collection position, scientific identity and declared scores distinct."""
    definitions = pose.score_definitions
    scores = []
    for name, value in pose.scores.items():
        definition = definitions.get(name)
        scores.append(
            {
                'name': name,
                'value': value,
                'unit': definition['unit'] if definition is not None else None,
                'definition': definition,
            }
        )
    return {
        'index': index,
        'position': index + 1,
        'pose_id': pose.pose_id,
        'rank': pose.rank,
        'scores': scores,
    }


def selected_pose_record(runtime: Any) -> dict[str, Any] | None:
    """Return the selected collection member without assigning a scientific rank."""
    poses = runtime.result.poses if runtime.result is not None else []
    index = runtime.active_pose_index
    if not 0 <= index < len(poses):
        return None
    return pose_record(poses[index], index)


def score_text(score: dict[str, Any]) -> str:
    """Format a named value with only its declared unit."""
    unit = score['unit'] if score['unit'] is not None else 'unit unknown'
    return f'{score["name"]}={score["value"]:.2f} ({unit})'
