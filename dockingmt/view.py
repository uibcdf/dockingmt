"""Interactive visualization of docking results, problems, and search domains in MolSysViewer."""

from __future__ import annotations

from typing import Any

import smonitor
from depdigest import dep_digest

from dockingmt.core.problem import DockingProblem
from dockingmt.core.results import DockingResult
from dockingmt.core.search_domain import SearchDomain


@dep_digest('molsysviewer')
@smonitor.signal(tags=['api', 'view'])
def view(
    item: Any = None,
    *,
    result: DockingResult | None = None,
    problem: DockingProblem | None = None,
    search_domain: SearchDomain | None = None,
    reference: Any = None,
    receptor: Any = None,
    partner: Any = None,
    pose_rank: int = 1,
    view: Any = None,
    **kwargs: Any,
) -> Any:
    """Display a docking result, problem, or search domain in MolSysViewer.

    Parameters
    ----------
    item : Any, optional
        A DockingResult, DockingProblem, or SearchDomain passed positionally.
    result : DockingResult | None, optional
        The docking result containing candidate poses and scores.
    problem : DockingProblem | None, optional
        The docking problem specification.
    search_domain : SearchDomain | None, optional
        Explicit search domain or box region to render.
    reference : Any, optional
        A crystallographic reference ligand to display alongside docking poses.
    receptor : Any, optional
        Explicit receptor system if not attached to result or problem.
    partner : Any, optional
        Explicit partner system if not attached to result or problem.
    pose_rank : int, default 1
        Initial candidate pose rank to focus in the viewer (1-indexed).
    view : MolSysView | None, optional
        An existing MolSysView instance to reuse. If None, a new view is created.

    Returns
    -------
    MolSysView
        Interactive MolSysViewer widget with loaded docking components and addon.
    """
    import molsysviewer as msv

    from molsysviewer_dockingmt.adapters.complex import (
        render_docking_result,
        set_active_pose,
    )
    from molsysviewer_dockingmt.adapters.shapes import render_search_domain
    from molsysviewer_dockingmt.addon import on_enable

    # Resolve positional item
    if item is not None:
        if isinstance(item, DockingResult):
            result = item
        elif isinstance(item, DockingProblem):
            problem = item
        elif isinstance(item, SearchDomain):
            search_domain = item
        elif hasattr(item, 'poses'):
            result = item
        elif hasattr(item, 'search_domain'):
            problem = item
        elif hasattr(item, 'bounds'):
            search_domain = item

    # If problem is provided and result is None, extract domain, receptor, partner
    if problem is not None:
        if receptor is None:
            receptor = problem.receptor_molsys or problem.receptor
        if partner is None:
            partner = problem.partner_molsys or problem.partner
        if search_domain is None:
            search_domain = problem.search_domain

    # Create viewer if not supplied
    if view is None:
        view = msv.new_view(**kwargs)

    # Enable DockingMT addon
    on_enable(view)

    # Case 1: Render docking result
    if result is not None:
        render_docking_result(
            view=view,
            result=result,
            receptor=receptor,
            partner=partner,
            reference=reference,
            search_domain=search_domain,
        )
        if pose_rank > 1:
            set_active_pose(view, pose_rank)

    # Case 2: Render problem without poses (receptor + search domain)
    elif receptor is not None:
        import molsysmt as msm

        rec_sys = (
            receptor.to_molecular_system()
            if hasattr(receptor, 'to_molecular_system')
            else msm.convert(receptor, to_form='molsysmt.MolSys')
        )
        view.load(rec_sys, label='receptor')
        if partner is not None:
            part_sys = (
                partner.to_molecular_system()
                if hasattr(partner, 'to_molecular_system')
                else msm.convert(partner, to_form='molsysmt.MolSys')
            )
            view.load(part_sys, label='partner', mode='add')
        if search_domain is not None:
            render_search_domain(view, search_domain)

    # Case 3: Only search domain
    elif search_domain is not None:
        render_search_domain(view, search_domain)

    return view


show = view
