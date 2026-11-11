"""Keep the JavaScript test examples bound to the actual Python panel protocol."""

import json
import runpy
from pathlib import Path
from types import SimpleNamespace

import pytest
import pyunitwizard as puw

import molsysviewer_bindingmt as addon
from bindingmt import BoxRegion, DockingPose, DockingResult
from molsysviewer_bindingmt.panels import DockingExplorerPanel, SearchDomainPanel
from molsysviewer_bindingmt.runtime import ensure_runtime


def example_states():
    """Build the empty and supplied-input examples through production panels."""
    view = SimpleNamespace(player=SimpleNamespace(index=0))
    runtime = ensure_runtime(view)
    explorer = DockingExplorerPanel(view=view)
    domain = SearchDomainPanel(view=view)
    try:
        explorer._refresh(view=view)
        domain._refresh(view=view)
        states = {
            'explorer_empty': explorer._last_state,
            'domain_empty': domain._last_state,
        }
        runtime.result = DockingResult(
            [
                DockingPose(
                    puw.quantity([[0, 0, 0]], 'nm'),
                    pose_id='seventh',
                    rank=7,
                    scores={'custom': 12},
                ),
                DockingPose(puw.quantity([[1, 1, 1]], 'nm')),
                DockingPose(
                    puw.quantity([[2, 2, 2]], 'nm'),
                    pose_id='first',
                    rank=1,
                    scores={'control': -2, 'vina': 0},
                    score_definitions={
                        'control': {
                            'schema_version': '1.0',
                            'method': 'explicit-method',
                            'method_version': '1',
                            'component': 'reported-score',
                            'kind': 'empirical',
                            'unit': 'kJ/mol',
                            'preferred_direction': 'lower',
                            'context': {'input': 'declared-state'},
                        }
                    },
                ),
            ]
        )
        runtime.search_domain = BoxRegion(
            center=puw.quantity([1, 2, 3], 'angstrom'),
            lengths=puw.quantity([2, 4, 6], 'angstrom'),
        )
        explorer._refresh(view=view)
        domain._refresh(view=view)
        states['explorer_poses'] = explorer._last_state
        states['domain_supplied'] = domain._last_state
        runtime.interaction_binding = SimpleNamespace(
            pose_index=2, analysis_names=('hbonds', 'hydrophobic')
        )
        view.molsys = object()
        runtime.interaction_carrier = view.molsys
        view.interactions = SimpleNamespace(
            analyses=lambda: [
                {
                    'name': name,
                    'method': 'declared-method',
                    'n_occurrences': 0,
                    'n_evaluated_structures': coverage,
                }
                for name, coverage in [('hbonds', 0), ('hydrophobic', 1)]
            ]
        )
        explorer._refresh(view=view)
        states['explorer_interactions'] = explorer._last_state
        return states
    finally:
        explorer.close()
        domain.close()


@pytest.mark.parametrize(
    'name',
    [
        'explorer_empty',
        'explorer_poses',
        'domain_empty',
        'domain_supplied',
        'explorer_interactions',
    ],
)
def test_dom_examples_match_python_panel_states(name):
    path = Path(__file__).resolve().parents[1] / 'devtools/frontend/panel_states.json'
    examples = json.loads(path.read_text())
    actual = json.loads(json.dumps(example_states(), allow_nan=False))
    assert actual[name] == examples[name]


@pytest.mark.parametrize(
    'name,kind', [('explorer', DockingExplorerPanel), ('domain', SearchDomainPanel)]
)
def test_extracted_javascript_is_the_actual_widget_module(name, kind):
    root = Path(__file__).resolve().parents[1]
    extractor = runpy.run_path(str(root / 'devtools/frontend/extract_panels.py'))
    sources = extractor['panel_sources'](Path(addon.__file__).resolve().parents[1])
    panel = kind()
    try:
        assert panel._esm == sources[name]
    finally:
        panel.close()
