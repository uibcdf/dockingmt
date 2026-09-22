"""Search Domain panel widget for MolSysViewer."""

from __future__ import annotations

from typing import Any

import pyunitwizard as puw
from molsysviewer.addons import AddonPanelWidget

from ..adapters.shapes import render_search_domain, set_search_domain_visibility
from ..runtime import ensure_runtime, record_event

_ESM = """
export function render({ model, el }) {
  let state = {
    has_domain: false,
    center: [0, 0, 0],
    lengths: [0, 0, 0],
    volume: 0,
    visible: true,
    status: "idle",
  };

  el.innerHTML = `
    <div class="dmt-domain-panel">
      <div class="dmt-header">
        <span class="dmt-title">Search Domain</span>
        <span class="dmt-badge" id="dmt-badge">Orthorhombic Box</span>
      </div>

      <div class="dmt-props" id="dmt-props">
        <span class="dmt-empty">No search domain loaded.</span>
      </div>

      <button class="dmt-btn dmt-btn--primary" id="dmt-domain-toggle">Toggle Box</button>
      <div class="dmt-status" id="dmt-status"></div>
    </div>
  `;

  const propsEl = el.querySelector("#dmt-props");
  const toggleBtn = el.querySelector("#dmt-domain-toggle");
  const statusEl = el.querySelector("#dmt-status");

  function applyState(s) {
    state = { ...state, ...s };

    if (!state.has_domain) {
      propsEl.innerHTML = '<span class="dmt-empty">No search domain loaded.</span>';
      toggleBtn.disabled = true;
    } else {
      toggleBtn.disabled = false;
      toggleBtn.textContent = state.visible ? "Hide Search Domain" : "Show Search Domain";
      propsEl.innerHTML = `
        <div class="dmt-prop-row">
          <span class="dmt-label">Center (Å):</span>
          <span class="dmt-value">(${state.center[0].toFixed(2)}, ${state.center[1].toFixed(2)}, ${state.center[2].toFixed(2)})</span>
        </div>
        <div class="dmt-prop-row">
          <span class="dmt-label">Size (Å):</span>
          <span class="dmt-value">${state.lengths[0].toFixed(2)} × ${state.lengths[1].toFixed(2)} × ${state.lengths[2].toFixed(2)}</span>
        </div>
        <div class="dmt-prop-row">
          <span class="dmt-label">Volume (Å³):</span>
          <span class="dmt-value">${state.volume.toFixed(1)}</span>
        </div>
      `;
    }
  }

  toggleBtn.addEventListener("click", () => {
    model.send({ type: "action", id: "toggle_domain", payload: {} });
  });

  model.on("msg:custom", (msg) => {
    if (msg?.type === "state") applyState(msg.state);
  });

  model.send({ type: "query", id: "viewer.context" });
  applyState(state);
}
"""

_CSS = """
.dmt-domain-panel {
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
.dmt-badge {
  font-size: 11px;
  background: rgba(51, 136, 255, 0.15);
  color: #1976d2;
  padding: 2px 6px;
  border-radius: 4px;
}
.dmt-props {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.dmt-prop-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}
.dmt-label {
  color: #666;
}
.dmt-value {
  font-weight: 500;
  font-family: monospace;
}
.dmt-empty {
  font-size: 12px;
  color: #888;
  font-style: italic;
  padding: 8px 0;
}
.dmt-btn--primary {
  padding: 6px 12px;
  border: 1px solid rgba(128, 128, 128, 0.3);
  border-radius: 4px;
  background: #3388ff;
  color: white;
  font-weight: 500;
  cursor: pointer;
}
.dmt-btn--primary:hover:not(:disabled) {
  background: #2575ea;
}
.dmt-btn--primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
"""


class SearchDomainPanel(AddonPanelWidget):
    """Panel widget displaying search domain geometry and bounding box controls."""

    _esm: str = _ESM
    _css: str = _CSS

    def on_mount(self, view: Any) -> None:
        runtime = ensure_runtime(view)
        self.push_state(self._build_state(runtime, view))

    def handle_action(self, view: Any, action_id: str, payload: dict[str, Any]) -> None:
        runtime = ensure_runtime(view)

        if action_id == 'toggle_domain':
            new_vis = not runtime.domain_visible
            set_search_domain_visibility(view, new_vis)
            record_event(view, 'panel_toggle_domain', visible=new_vis)
            self.push_state(self._build_state(runtime, view))

        elif action_id == 'render_domain':
            domain = runtime.search_domain
            if domain is not None:
                render_search_domain(view, domain)
                record_event(view, 'panel_render_domain')
                self.push_state(self._build_state(runtime, view))

    def _build_state(self, runtime: Any, view: Any) -> dict[str, Any]:
        domain = runtime.search_domain
        if domain is None:
            return {
                'has_domain': False,
                'center': [0.0, 0.0, 0.0],
                'lengths': [0.0, 0.0, 0.0],
                'volume': 0.0,
                'visible': runtime.domain_visible,
                'status': 'idle',
            }

        box = (
            domain.as_box_approximation()
            if hasattr(domain, 'as_box_approximation')
            else domain
        )
        c_ang = [
            float(x) for x in puw.get_value(puw.convert(box.center, to_unit='angstrom'))
        ]
        l_ang = [
            float(x)
            for x in puw.get_value(puw.convert(box.lengths, to_unit='angstrom'))
        ]
        v_ang = float(puw.get_value(puw.convert(box.volume, to_unit='angstrom**3')))

        return {
            'has_domain': True,
            'center': c_ang,
            'lengths': l_ang,
            'volume': v_ang,
            'visible': runtime.domain_visible,
            'status': 'idle',
        }
