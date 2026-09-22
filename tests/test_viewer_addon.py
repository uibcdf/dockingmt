"""Tests for the MolSysViewer integration and DockingMT addon (Gate C6)."""

from __future__ import annotations

import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt
from dockingmt.core import BoxRegion, DockingPose, DockingProblem, DockingResult
from dockingmt.view import show, view


def test_addon_spec_matches_molsysviewer_contract():
    """Verify that the DockingMT addon spec adheres to MolSysViewer standards."""
    molsysviewer = pytest.importorskip('molsysviewer')
    import molsysviewer_dockingmt as dmt_viewer

    addon = dmt_viewer.addon
    assert isinstance(addon, molsysviewer.AddonSpec)
    assert addon.name == 'dockingmt'
    assert addon.package == 'dockingmt'

    assert len(addon.workspaces) == 1
    assert addon.workspaces[0].id == 'dockingmt'
    assert addon.workspaces[0].entry_panel == 'explorer'

    panel_ids = [p.id for p in addon.panels]
    assert panel_ids == ['explorer', 'domain']

    action_ids = [a.id for a in addon.context_actions]
    assert 'toggle-search-domain' in action_ids
    assert 'toggle-reference' in action_ids

    section_ids = [s.id for s in addon.addon_sections]
    assert 'docking-summary' in section_ids

    shape_ids = [s.id for s in addon.shape_providers]
    assert 'search-domain-box' in shape_ids

    export_ids = [e.id for e in addon.export_helpers]
    assert 'docking-summary-export' in export_ids


def test_lifecycle_hooks_and_runtime_events():
    """Verify on_enable, on_disable, and on_context_action lifecycle hooks."""
    molsysviewer = pytest.importorskip('molsysviewer')
    import molsysviewer_dockingmt as dmt_viewer

    v = molsysviewer.MolSysView(debug_js=True)
    dmt_viewer.on_enable(v)
    runtime = dmt_viewer.ensure_runtime(v)

    assert runtime.enabled is True
    assert runtime.workspace == 'dockingmt'
    assert runtime.event_log[-1]['event'] == 'enable'

    dmt_viewer.on_context_action(v, 'toggle-search-domain', {})
    assert runtime.domain_visible is False
    assert any(e['event'] == 'context_action' for e in runtime.event_log)

    dmt_viewer.on_context_action(v, 'toggle-search-domain', {})
    assert runtime.domain_visible is True

    dmt_viewer.on_disable(v)
    assert runtime.enabled is False
    assert runtime.event_log[-1]['event'] == 'disable'


def test_search_domain_wireframe_coordinate_pairs():
    """Verify calculation of 12 bounding box edge pairs for MolSysViewer wireframe."""
    box = BoxRegion(
        center=puw.quantity([1.0, 2.0, 3.0], 'nm'),
        lengths=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    from molsysviewer_dockingmt.adapters.shapes import (
        compute_box_wireframe_coordinate_pairs,
    )

    coord_pairs = compute_box_wireframe_coordinate_pairs(box)
    assert puw.is_quantity(coord_pairs)
    assert puw.get_unit(coord_pairs) == 'angstrom'

    vals = puw.get_value(coord_pairs)
    assert vals.shape == (12, 2, 3)

    # In angstroms, center is (10, 20, 30) and size is (20, 20, 20) -> bounds [0..20, 10..30, 20..40]
    min_bound = np.min(vals, axis=(0, 1))
    max_bound = np.max(vals, axis=(0, 1))
    assert np.allclose(min_bound, [0.0, 10.0, 20.0])
    assert np.allclose(max_bound, [20.0, 30.0, 40.0])


def test_render_search_domain_and_visibility():
    """Verify that render_search_domain creates a shape layer and can toggle visibility."""
    molsysviewer = pytest.importorskip('molsysviewer')
    from molsysviewer_dockingmt.adapters.shapes import (
        render_search_domain,
        set_search_domain_visibility,
    )
    from molsysviewer_dockingmt.runtime import ensure_runtime

    v = molsysviewer.MolSysView(debug_js=True)
    box = BoxRegion(
        center=puw.quantity([1.0, 1.0, 1.0], 'nm'),
        lengths=puw.quantity([1.0, 1.0, 1.0], 'nm'),
    )

    layer = render_search_domain(v, box)
    assert layer.tag == 'dockingmt:search_domain'
    assert v.shapes.contains('dockingmt:search_domain')

    runtime = ensure_runtime(v)
    assert runtime.domain_visible is True

    set_search_domain_visibility(v, False)
    assert runtime.domain_visible is False

    set_search_domain_visibility(v, True)
    assert runtime.domain_visible is True


def test_build_docking_complex_system_and_set_active_pose():
    """Verify building multi-structure complex and navigating poses."""
    pytest.importorskip('molsysviewer')
    import molsysmt as msm

    from molsysviewer_dockingmt.adapters.complex import (
        build_docking_complex_system,
        render_docking_result,
        set_active_pose,
    )

    rec = msm.build.build_peptide('ALA')

    # 3 mock poses with 3 atoms each
    poses = [
        DockingPose(
            coordinates=puw.quantity(np.ones((3, 3)) * (i + 1), 'angstrom'),
            scores={'vina': -7.0 + i},
            rank=i + 1,
        )
        for i in range(3)
    ]

    complex_sys = build_docking_complex_system(receptor=rec, poses=poses)
    n_rec_atoms = msm.get(rec, element='system', n_atoms=True)
    assert msm.get(complex_sys, element='system', n_atoms=True) == n_rec_atoms + 3
    assert msm.get(complex_sys, element='system', n_structures=True) == 3

    # Render into MolSysView
    import molsysviewer

    v = molsysviewer.MolSysView(debug_js=True)
    res = DockingResult(poses=poses)
    render_docking_result(v, res, receptor=rec)

    assert v.player.n_structures == 3
    assert v.player.index == 0
    assert v.addons.dockingmt.active_pose_rank == 1

    # Switch poses
    set_active_pose(v, 2)
    assert v.player.index == 1
    assert v.addons.dockingmt.active_pose_rank == 2

    set_active_pose(v, 3)
    assert v.player.index == 2
    assert v.addons.dockingmt.active_pose_rank == 3

    with pytest.raises(ValueError):
        set_active_pose(v, 0)

    with pytest.raises(ValueError):
        set_active_pose(v, 4)


def test_dockingmt_view_with_result_problem_and_search_domain():
    """Verify the high-level dockingmt.view() API."""
    pytest.importorskip('molsysviewer')
    import molsysmt as msm

    rec = msm.build.build_peptide('GLY')
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        lengths=puw.quantity([1.0, 1.0, 1.0], 'nm'),
    )
    poses = [
        DockingPose(
            coordinates=puw.quantity(np.zeros((2, 3)), 'angstrom'),
            scores={'vina': -5.0},
            rank=1,
        )
    ]
    problem = DockingProblem(receptor=rec, partner=rec, search_domain=box)
    res = DockingResult(poses=poses, problem=problem)

    # 1. view(result)
    v1 = dockingmt.view(res)
    assert v1.shapes.contains('dockingmt:search_domain')
    assert v1.player.n_structures == 1
    assert v1.addons.dockingmt.active_pose_rank == 1

    # 2. show(result) alias
    v2 = show(res)
    assert v2.shapes.contains('dockingmt:search_domain')

    # 3. view(problem=problem)
    v3 = view(problem=problem)
    assert v3.shapes.contains('dockingmt:search_domain')

    # 4. view(search_domain=box)
    v4 = view(search_domain=box)
    assert v4.shapes.contains('dockingmt:search_domain')


def test_panels_workbench_and_export():
    """Verify panel actions, workbench summary, and export payload."""
    pytest.importorskip('molsysviewer')
    import molsysmt as msm

    from molsysviewer_dockingmt.export import build_docking_export_payload
    from molsysviewer_dockingmt.panels import DockingExplorerPanel, SearchDomainPanel
    from molsysviewer_dockingmt.workbench import get_docking_summary_section

    rec = msm.build.build_peptide('ALA')
    box = BoxRegion(
        center=puw.quantity([1.0, 1.0, 1.0], 'nm'),
        lengths=puw.quantity([1.0, 1.0, 1.0], 'nm'),
    )
    poses = [
        DockingPose(
            coordinates=puw.quantity(np.zeros((3, 3)), 'angstrom'),
            scores={'vina': -6.5},
            rank=1,
        ),
        DockingPose(
            coordinates=puw.quantity(np.ones((3, 3)), 'angstrom'),
            scores={'vina': -5.2},
            rank=2,
        ),
    ]
    res = DockingResult(poses=poses)

    v = dockingmt.view(result=res, receptor=rec, search_domain=box)

    # Explorer panel
    explorer = DockingExplorerPanel(view=v)
    explorer.on_mount(v)
    explorer.handle_action(v, 'set_pose', {'rank': 2})
    assert v.addons.dockingmt.active_pose_rank == 2

    explorer.handle_action(v, 'prev_pose', {})
    assert v.addons.dockingmt.active_pose_rank == 1

    explorer.handle_action(v, 'next_pose', {})
    assert v.addons.dockingmt.active_pose_rank == 2

    # Domain panel
    domain_p = SearchDomainPanel(view=v)
    domain_p.on_mount(v)
    domain_p.handle_action(v, 'toggle_domain', {})
    assert v.addons.dockingmt.domain_visible is False

    # Workbench summary
    summary = get_docking_summary_section(v)
    assert summary['id'] == 'docking-summary'
    assert summary['n_poses'] == 2
    assert summary['active_rank'] == 2
    assert summary['top_score'] == -6.5

    # Export payload
    payload = build_docking_export_payload(v)
    assert payload['title'] == 'DockingMT Result Export'
    assert payload['active_pose_rank'] == 2
    assert payload['result'] is not None
    assert payload['search_domain'] is not None
