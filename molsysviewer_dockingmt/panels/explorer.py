"""Docking Explorer panel widget for MolSysViewer."""

from __future__ import annotations

from typing import Any

import pyunitwizard as puw
from molsysviewer.addons import AddonPanelWidget

from ..adapters.complex import set_active_pose, set_reference_visibility
from ..adapters.shapes import set_search_domain_visibility
from ..runtime import ensure_runtime, record_event

_ESM = """
export function render({ model, el }) {
  let state = {
    n_poses: 0,
    active_rank: 1,
    poses: [],
    domain_visible: true,
    reference_visible: true,
    has_reference: false,
    status: "idle",
    error: null,
  };

  el.innerHTML = `
    <div class="dmt-explorer-panel">
      <div class="dmt-header">
        <span class="dmt-title">Docking Poses</span>
        <span class="dmt-count" id="dmt-pose-count">0 poses</span>
      </div>

      <div class="dmt-nav-row">
        <button class="dmt-btn dmt-btn--nav" id="dmt-prev" title="Previous pose">&#8592; Prev</button>
        <div class="dmt-pose-display">
          <span class="dmt-label">Pose</span>
          <input class="dmt-input" type="number" id="dmt-pose-input" min="1" step="1" value="1" />
        </div>
        <button class="dmt-btn dmt-btn--nav" id="dmt-next" title="Next pose">Next &#8594;</button>
      </div>

      <div class="dmt-table-container">
        <table class="dmt-table" id="dmt-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Score (kcal/mol)</th>
              <th>RMSD (Å)</th>
            </tr>
          </thead>
          <tbody id="dmt-tbody">
            <tr><td colspan="3" class="dmt-empty">No docking poses loaded.</td></tr>
          </tbody>
        </table>
      </div>

      <div class="dmt-controls">
        <button class="dmt-btn dmt-btn--toggle" id="dmt-toggle-box">Toggle Search Box</button>
        <button class="dmt-btn dmt-btn--toggle" id="dmt-toggle-ref">Toggle Reference</button>
      </div>

      <div class="dmt-status" id="dmt-status"></div>
    </div>
  `;

  const countEl = el.querySelector("#dmt-pose-count");
  const prevBtn = el.querySelector("#dmt-prev");
  const nextBtn = el.querySelector("#dmt-next");
  const poseInput = el.querySelector("#dmt-pose-input");
  const tbodyEl = el.querySelector("#dmt-tbody");
  const toggleBoxBtn = el.querySelector("#dmt-toggle-box");
  const toggleRefBtn = el.querySelector("#dmt-toggle-ref");
  const statusEl = el.querySelector("#dmt-status");

  function applyState(s) {
    state = { ...state, ...s };

    countEl.textContent = `${state.n_poses} pose${state.n_poses === 1 ? '' : 's'}`;
    poseInput.value = state.active_rank;
    poseInput.max = state.n_poses || 1;

    prevBtn.disabled = state.active_rank <= 1 || state.n_poses <= 1;
    nextBtn.disabled = state.active_rank >= state.n_poses || state.n_poses <= 1;
    toggleRefBtn.disabled = !state.has_reference;

    toggleBoxBtn.textContent = state.domain_visible ? "Hide Search Box" : "Show Search Box";
    toggleRefBtn.textContent = state.reference_visible ? "Hide Reference" : "Show Reference";

    if (!state.poses || state.poses.length === 0) {
      tbodyEl.innerHTML = '<tr><td colspan="3" class="dmt-empty">No docking poses loaded.</td></tr>';
    } else {
      tbodyEl.innerHTML = state.poses.map(p => {
        const isSelected = p.rank === state.active_rank;
        const rowClass = isSelected ? 'dmt-row dmt-row--active' : 'dmt-row';
        const rmsdText = p.rmsd !== null && p.rmsd !== undefined ? p.rmsd.toFixed(2) : '-';
        const scoreText = p.score !== null && p.score !== undefined ? p.score.toFixed(2) : '-';
        return `
          <tr class="${rowClass}" data-rank="${p.rank}">
            <td><strong>#${p.rank}</strong></td>
            <td>${scoreText}</td>
            <td>${rmsdText}</td>
          </tr>
        `;
      }).join('');

      tbodyEl.querySelectorAll('.dmt-row').forEach(row => {
        row.addEventListener('click', () => {
          const rank = parseInt(row.getAttribute('data-rank'), 10);
          model.send({ type: "action", id: "set_pose", payload: { rank: rank } });
        });
      });
    }

    if (state.status === "error" && state.error) {
      statusEl.textContent = `Error: ${state.error}`;
      statusEl.className = "dmt-status dmt-status--error";
    } else {
      statusEl.textContent = "";
      statusEl.className = "dmt-status";
    }
  }

  prevBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "prev_pose", payload: {} });
  });

  nextBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "next_pose", payload: {} });
  });

  poseInput.addEventListener("change", () => {
    const val = parseInt(poseInput.value, 10);
    if (!isNaN(val) && val >= 1 && val <= (state.n_poses || 1)) {
      model.send({ type: "action", id: "set_pose", payload: { rank: val } });
    }
  });

  toggleBoxBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "toggle_search_domain", payload: {} });
  });

  toggleRefBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "toggle_reference", payload: {} });
  });

  model.on("msg:custom", (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  });

  model.send({ type: "query", id: "viewer.context" });
  applyState(state);
}
"""

_CSS = """
.dmt-explorer-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 8px;
  font-family: sans-serif;
  font-size: 13px;
}
.dmt-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(128, 128, 128, 0.2);
  padding-bottom: 4px;
}
.dmt-title {
  font-weight: 600;
  font-size: 14px;
}
.dmt-count {
  font-size: 11px;
  opacity: 0.6;
}
.dmt-nav-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
.dmt-pose-display {
  display: flex;
  align-items: center;
  gap: 4px;
}
.dmt-input {
  width: 48px;
  padding: 3px 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  text-align: center;
}
.dmt-btn {
  padding: 5px 10px;
  border: 1px solid rgba(128, 128, 128, 0.3);
  border-radius: 4px;
  background: #f5f5f5;
  cursor: pointer;
  font-size: 12px;
}
.dmt-btn:hover:not(:disabled) {
  background: #e5e5e5;
}
.dmt-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
.dmt-table-container {
  max-height: 220px;
  overflow-y: auto;
  border: 1px solid rgba(128, 128, 128, 0.2);
  border-radius: 4px;
}
.dmt-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}
.dmt-table th {
  background: rgba(128, 128, 128, 0.1);
  padding: 6px;
  text-align: left;
  font-size: 11px;
}
.dmt-table td {
  padding: 5px 6px;
  border-top: 1px solid rgba(128, 128, 128, 0.1);
}
.dmt-row {
  cursor: pointer;
}
.dmt-row:hover {
  background: rgba(51, 136, 255, 0.1);
}
.dmt-row--active {
  background: rgba(51, 136, 255, 0.25) !important;
}
.dmt-empty {
  text-align: center;
  color: #888;
  font-style: italic;
  padding: 12px;
}
.dmt-controls {
  display: flex;
  gap: 8px;
}
.dmt-btn--toggle {
  flex: 1;
}
.dmt-status {
  font-size: 11px;
  min-height: 14px;
}
.dmt-status--error {
  color: #f44336;
}
"""


class DockingExplorerPanel(AddonPanelWidget):
    """Panel widget for browsing candidate poses, scores, and reference comparison."""

    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        runtime = ensure_runtime(view)
        self.push_state(self._build_state(runtime, view))

    def handle_action(self, view: Any, action_id: str, payload: dict[str, Any]) -> None:
        runtime = ensure_runtime(view)

        try:
            if action_id == 'set_pose':
                rank = payload.get('rank')
                if isinstance(rank, int):
                    set_active_pose(view, rank)
                    record_event(view, 'panel_set_pose', rank=rank)

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

            self.push_state(self._build_state(runtime, view))

        except Exception as exc:
            state = self._build_state(runtime, view)
            state['status'] = 'error'
            state['error'] = str(exc)
            self.push_state(state)

    def _build_state(self, runtime: Any, view: Any) -> dict[str, Any]:
        result = runtime.result
        if result is None or not result.poses:
            return {
                'n_poses': 0,
                'active_rank': 1,
                'poses': [],
                'domain_visible': runtime.domain_visible,
                'reference_visible': runtime.reference_visible,
                'has_reference': runtime.reference is not None,
                'status': 'idle',
                'error': None,
            }

        poses_data = []
        reference = runtime.reference

        # Compute RMSDs if reference is present
        rmsds = None
        if reference is not None:
            try:
                raw_rmsds = result.get_rmsds(reference)
                rmsds = [
                    float(puw.get_value(puw.convert(r, to_unit='angstrom')))
                    for r in raw_rmsds
                ]
            except Exception:
                rmsds = None

        for idx, pose in enumerate(result.poses):
            # Prefer 'vina' score or first score
            primary_score = None
            if 'vina' in pose.scores:
                primary_score = pose.scores['vina']
            elif pose.scores:
                primary_score = next(iter(pose.scores.values()))

            pose_rmsd = rmsds[idx] if rmsds is not None and idx < len(rmsds) else None

            poses_data.append(
                {
                    'rank': pose.rank if pose.rank is not None else idx + 1,
                    'score': primary_score,
                    'rmsd': pose_rmsd,
                }
            )

        return {
            'n_poses': len(result.poses),
            'active_rank': runtime.active_pose_rank,
            'poses': poses_data,
            'domain_visible': runtime.domain_visible,
            'reference_visible': runtime.reference_visible,
            'has_reference': reference is not None,
            'status': 'idle',
            'error': None,
        }
