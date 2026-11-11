"""Docking Explorer panel widget for MolSysViewer."""

from __future__ import annotations

from numbers import Integral
from typing import Any

from bindingmt._private.smonitor import ViewerActionError, ViewerPosePositionError

from .._presentation import pose_record
from .._scene import sync_scene_state
from ..adapters.complex import set_active_pose, set_reference_visibility
from ..adapters.shapes import set_search_domain_visibility
from ..runtime import ensure_runtime, record_event
from ._base import _DockingPanel

_ESM = """
export function render({ model, el }) {
  let state = {
    n_poses: 0,
    active_index: null,
    poses: [],
    domain_visible: true,
    reference_visible: true,
    has_reference: false,
    has_domain: false,
    comparison_note: "RMSD unavailable: no recorded comparison is bound.",
    status: "idle",
    error: null,
  };

  el.innerHTML = `
    <div class="bmt-explorer-panel">
      <div class="bmt-header">
        <span class="bmt-title">Docking Poses</span>
        <span class="bmt-count" id="bmt-pose-count">0 poses</span>
      </div>

      <div class="bmt-nav-row">
        <button class="bmt-btn bmt-btn--nav" id="bmt-prev" title="Previous pose">&#8592; Prev</button>
        <div class="bmt-pose-display">
          <span class="bmt-label">Position</span>
          <input class="bmt-input" type="number" id="bmt-pose-input" min="1" step="1" value="1" />
        </div>
        <button class="bmt-btn bmt-btn--nav" id="bmt-next" title="Next pose">Next &#8594;</button>
      </div>

      <div class="bmt-table-container">
        <table class="bmt-table" id="bmt-table">
          <thead>
            <tr>
              <th>Position</th>
              <th>Pose ID</th>
              <th>Rank</th>
              <th>Named scores</th>
            </tr>
          </thead>
          <tbody id="bmt-tbody">
            <tr><td colspan="4" class="bmt-empty">No docking poses loaded.</td></tr>
          </tbody>
        </table>
      </div>

      <div class="bmt-controls">
        <button class="bmt-btn bmt-btn--toggle" id="bmt-toggle-box">Toggle Search Box</button>
        <button class="bmt-btn bmt-btn--toggle" id="bmt-toggle-ref">Toggle Reference</button>
        <button class="bmt-btn" id="bmt-refresh">Refresh</button>
      </div>

      <div id="bmt-comparison-note"></div>
      <div id="bmt-interaction-note"></div>
      <div id="bmt-interaction-analyses"></div>
      <div class="bmt-status" id="bmt-status"></div>
    </div>
  `;

  const countEl = el.querySelector("#bmt-pose-count");
  const prevBtn = el.querySelector("#bmt-prev");
  const nextBtn = el.querySelector("#bmt-next");
  const poseInput = el.querySelector("#bmt-pose-input");
  const tbodyEl = el.querySelector("#bmt-tbody");
  const toggleBoxBtn = el.querySelector("#bmt-toggle-box");
  const toggleRefBtn = el.querySelector("#bmt-toggle-ref");
  const statusEl = el.querySelector("#bmt-status");
  const refreshBtn = el.querySelector("#bmt-refresh");
  const comparisonEl = el.querySelector("#bmt-comparison-note");
  const interactionNote = el.querySelector("#bmt-interaction-note");
  const interactionAnalyses = el.querySelector("#bmt-interaction-analyses");

  function applyState(s) {
    state = { ...state, ...s };

    countEl.textContent = `${state.n_poses} pose${state.n_poses === 1 ? '' : 's'}`;
    poseInput.value = state.active_index === null ? '' : state.active_index + 1;
    poseInput.max = state.n_poses || 1;
    const poses = state.poses ?? [];
    const limitedGeometry = poses.some(p => p.geometry_available !== undefined);
    const availablePoses = poses.filter(p => p.geometry_available !== false);
    poseInput.disabled = !state.n_poses || (limitedGeometry && availablePoses.length <= 1);

    prevBtn.disabled = state.active_index === null || !availablePoses.some(p => p.index < state.active_index);
    nextBtn.disabled = state.active_index === null || !availablePoses.some(p => p.index > state.active_index);
    toggleRefBtn.disabled = !state.reference_available;
    toggleRefBtn.title = state.reference_reason ?? '';
    toggleBoxBtn.disabled = !state.domain_available;
    toggleBoxBtn.title = state.domain_reason ?? '';
    comparisonEl.textContent = state.comparison_note;
    interactionNote.textContent = limitedGeometry
      ? (state.interaction_geometry_available
        ? `Geometry is loaded for position ${state.active_index + 1}. Other poses remain listed.`
        : state.interaction_geometry_reason)
      : '';
    interactionAnalyses.replaceChildren();
    if (limitedGeometry) {
      (state.interaction_analyses ?? []).forEach(analysis => {
        const line = document.createElement('div');
        const coverage = !analysis.available ? 'unavailable'
          : (!analysis.evaluated ? 'not evaluated'
          : `evaluated, ${analysis.n_occurrences} observations`);
        line.textContent = `${analysis.name}: ${coverage}`;
        interactionAnalyses.appendChild(line);
      });
    }

    toggleBoxBtn.textContent = state.domain_visible ? "Hide Search Box" : "Show Search Box";
    toggleRefBtn.textContent = state.reference_visible ? "Hide Reference" : "Show Reference";

    if (!state.poses || state.poses.length === 0) {
      tbodyEl.innerHTML = '<tr><td colspan="4" class="bmt-empty">No docking poses loaded.</td></tr>';
    } else {
      tbodyEl.replaceChildren();
      state.poses.forEach(p => {
        const row = document.createElement('tr');
        row.className = p.index === state.active_index ? 'bmt-row bmt-row--active' : 'bmt-row';
        row.dataset.index = p.index;
        const geometryAvailable = p.geometry_available !== false;
        row.setAttribute('aria-disabled', String(!geometryAvailable));
        if (!geometryAvailable) {
          row.classList.add('bmt-row--unavailable');
          row.title = p.geometry_reason;
        }
        [p.position, p.pose_id ?? 'Unavailable', p.rank ?? 'Unassigned'].forEach(value => {
          const cell = document.createElement('td');
          cell.textContent = String(value);
          row.appendChild(cell);
        });
        const scores = document.createElement('td');
        if (!p.scores.length) scores.textContent = 'Unavailable';
        p.scores.forEach(score => {
          const line = document.createElement('div');
          const unit = score.unit ?? 'unit unknown';
          line.textContent = `${score.name}=${score.value.toFixed(2)} (${unit})`;
          line.title = score.definition ? JSON.stringify(score.definition) : 'Score meaning undeclared';
          scores.appendChild(line);
        });
        row.appendChild(scores);
        if (geometryAvailable) {
          row.addEventListener('click', () => {
            model.send({ type: "action", id: "set_pose", payload: { index: p.index } });
          });
        }
        tbodyEl.appendChild(row);
      });
    }

    if (state.status === "error" && state.error) {
      statusEl.textContent = `Error: ${state.error}`;
      statusEl.className = "bmt-status bmt-status--error";
    } else {
      statusEl.textContent = "";
      statusEl.className = "bmt-status";
    }
  }

  prevBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "prev_pose", payload: {} });
  });

  nextBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "next_pose", payload: {} });
  });

  poseInput.addEventListener("change", () => {
    const val = Number(poseInput.value);
    if (Number.isInteger(val) && val >= 1 && val <= state.n_poses) {
      if (state.poses?.[val - 1]?.geometry_available === false) return;
      model.send({ type: "action", id: "set_pose", payload: { index: val - 1 } });
    }
  });

  toggleBoxBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "toggle_search_domain", payload: {} });
  });

  toggleRefBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "toggle_reference", payload: {} });
  });
  refreshBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "refresh", payload: {} });
  });

  const onMessage = (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  };
  model.on("msg:custom", onMessage);
  const onState = () => applyState(model.get("explorer") ?? {});
  model.on("change:explorer", onState);

  model.send({ type: "query", id: "viewer.context" });
  applyState(model.get("explorer") ?? state);
  return () => {
    model.off("msg:custom", onMessage);
    model.off("change:explorer", onState);
  };
}
"""

_CSS = """
.bmt-explorer-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 8px;
  font-family: sans-serif;
  font-size: 13px;
}
.bmt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(128, 128, 128, 0.2);
  padding-bottom: 4px;
}
.bmt-title {
  font-weight: 600;
  font-size: 14px;
}
.bmt-count {
  font-size: 11px;
  opacity: 0.6;
}
.bmt-nav-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
.bmt-pose-display {
  display: flex;
  align-items: center;
  gap: 4px;
}
.bmt-input {
  width: 48px;
  padding: 3px 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  text-align: center;
}
.bmt-btn {
  padding: 5px 10px;
  border: 1px solid rgba(128, 128, 128, 0.3);
  border-radius: 4px;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 12px;
}
.bmt-btn:hover:not(:disabled) {
  background: #e5e5e5;
}
.bmt-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.bmt-table-container {
  max-height: 220px;
  overflow-y: auto;
  border: 1px solid rgba(128, 128, 128, 0.2);
  border-radius: 4px;
}
.bmt-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}
.bmt-table th {
  background: rgba(128, 128, 128, 0.1);
  padding: 6px;
  text-align: left;
  font-size: 11px;
}
.bmt-table td {
  padding: 5px 6px;
  border-top: 1px solid rgba(128, 128, 128, 0.1);
}
.bmt-row {
  cursor: pointer;
}
.bmt-row--unavailable {
  opacity: 0.6;
  cursor: default;
}
.bmt-row:hover {
  background: rgba(51, 136, 255, 0.1);
}
.bmt-row--active {
  background: rgba(51, 136, 255, 0.25) !important;
}
.bmt-empty {
  text-align: center;
  color: #888;
  font-style: italic;
  padding: 12px;
}
.bmt-controls {
  display: flex;
  gap: 8px;
}
.bmt-btn--toggle {
  flex: 1;
}
.bmt-status {
  font-size: 11px;
  min-height: 14px;
}
.bmt-status--error {
  color: #f44336;
}
"""


class DockingExplorerPanel(_DockingPanel):
    """Panel widget for browsing candidate poses, scores, and reference comparison."""

    _esm: str = _ESM
    _css: str = _CSS
    _state_key = 'explorer'

    def _handle_action(
        self, view: Any, action_id: str, payload: dict[str, Any]
    ) -> None:
        runtime = ensure_runtime(view)

        sync_scene_state(view)
        if action_id == 'set_pose':
            if 'index' in payload and 'rank' not in payload:
                index = payload['index']
                if isinstance(index, bool) or not isinstance(index, Integral):
                    raise ViewerPosePositionError(
                        arg_name='index', position=index, operation='panel_action'
                    )
                position = int(index) + 1
            elif 'rank' in payload and 'index' not in payload:
                # Retain the old one-based position message for callers.
                position = payload['rank']
            else:
                raise ViewerPosePositionError(
                    arg_name='index/rank', operation='panel_action'
                )
            set_active_pose(view, position)
            record_event(view, 'panel_set_pose', index=runtime.active_pose_index)

        elif action_id == 'prev_pose':
            new_rank = max(1, runtime.active_pose_rank - 1)
            set_active_pose(view, new_rank)
            record_event(view, 'panel_prev_pose', rank=new_rank)

        elif action_id == 'next_pose':
            max_rank = len(runtime.result.poses) if runtime.result else 1
            new_rank = min(max_rank, runtime.active_pose_rank + 1)
            set_active_pose(view, new_rank)
            record_event(view, 'panel_next_pose', rank=new_rank)

        elif action_id == 'toggle_search_domain':
            new_vis = not runtime.domain_visible
            set_search_domain_visibility(view, new_vis)
            record_event(view, 'panel_toggle_search_domain', visible=new_vis)

        elif action_id == 'toggle_reference':
            new_vis = not runtime.reference_visible
            set_reference_visibility(view, new_vis)
            record_event(view, 'panel_toggle_reference', visible=new_vis)

        elif action_id != 'refresh':
            raise ViewerActionError(
                panel='docking explorer', action_id=action_id, operation='panel_action'
            )

    def _build_state(self, runtime: Any, view: Any) -> dict[str, Any]:
        controls = sync_scene_state(view)
        result = runtime.result
        poses = result.poses if result is not None else []
        index = runtime.active_pose_index

        records = [pose_record(pose, idx) for idx, pose in enumerate(poses)]
        if runtime.interaction_binding is not None:
            for record in records:
                available = (
                    controls['interaction_geometry_available']
                    and record['index'] == runtime.interaction_binding.pose_index
                )
                record.update(
                    geometry_available=available,
                    geometry_reason=None
                    if available
                    else 'This view has no loaded geometry for this pose.',
                )
        return {
            'n_poses': len(poses),
            'active_rank': runtime.active_pose_rank,
            'active_index': index if 0 <= index < len(poses) else None,
            'poses': records,
            'domain_visible': runtime.domain_visible,
            'reference_visible': runtime.reference_visible,
            'has_reference': runtime.reference is not None,
            'has_domain': runtime.search_domain is not None,
            'comparison_note': 'RMSD unavailable: no recorded comparison is bound.',
            'status': 'idle',
            'error': None,
            **controls,
        }
