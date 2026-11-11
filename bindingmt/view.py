"""Interactive visualization of docking results, problems, and search domains in MolSysViewer."""

from __future__ import annotations

from typing import Any

import smonitor
from argdigest import arg_digest
from depdigest import dep_digest

from bindingmt._private.smonitor import ArgumentError, ViewerPosePositionError
from bindingmt.core.problem import DockingProblem
from bindingmt.core.results import DockingResult
from bindingmt.core.search_domain import SearchDomain
from bindingmt.interactions import PoseInteractions


@arg_digest(config='bindingmt._argdigest', native_view='bindingmt.view.view')
def _resolve_view_inputs(item, result, problem, search_domain, pose_rank):
    """Digest owned options in a closed boundary, apart from provider kwargs.

    In particular, MolSysViewer's forwarded skip_digestion cannot bypass this
    boundary. Molecular inputs and widget options retain provider ownership.
    """
    if isinstance(item, PoseInteractions):
        for argument, value in (('result', result), ('problem', problem)):
            if value is not None:
                raise ArgumentError(
                    arg_name=argument,
                    reason='The interaction binding already retains its complete result.',
                )
        if pose_rank != 1:
            raise ArgumentError(
                arg_name='pose_rank',
                reason='The interaction binding already selects its pose.',
            )
        return None, None, search_domain, pose_rank
    if item is not None:
        if isinstance(item, DockingResult) or hasattr(item, 'poses'):
            if result is not None and result is not item:
                raise ArgumentError(
                    arg_name='result',
                    caller='bindingmt.view.view',
                    reason='Supply the result once, positionally or by keyword.',
                )
            result = item
        elif isinstance(item, DockingProblem) or hasattr(item, 'search_domain'):
            if problem is not None and problem is not item:
                raise ArgumentError(
                    arg_name='problem',
                    caller='bindingmt.view.view',
                    reason='Supply the problem once, positionally or by keyword.',
                )
            problem = item
        else:
            if search_domain is not None and search_domain is not item:
                raise ArgumentError(
                    arg_name='search_domain',
                    caller='bindingmt.view.view',
                    reason='Supply the search domain once, positionally or by keyword.',
                )
            search_domain = item
    if result is not None and pose_rank > 1 and pose_rank > len(result.poses):
        raise ViewerPosePositionError(
            position=pose_rank,
            n_poses=len(result.poses),
            operation='view',
        )
    return result, problem, search_domain, pose_rank


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
        A DockingResult, PoseInteractions, DockingProblem, or SearchDomain.
        An interaction binding displays its admitted one-frame carrier and all
        original result records. Only its selected pose has loaded geometry;
        no analysis is projected onto other poses. Use the binding's original
        pose selection; additional receptor/partner/reference inputs and a
        nondefault pose_rank are refused.
    result : DockingResult | None, optional
        The docking result containing candidate poses and scores.
    problem : DockingProblem | None, optional
        The docking problem specification.
    search_domain : SearchDomain | None, optional
        Explicit search domain or box region to render.
    reference : Any, optional
        Reference ligand with one static structure or one structure per pose.
        Static references are explicitly repeated; trajectories are paired by
        index without alignment. Other structure counts raise ValueError.
    receptor : Any, optional
        Explicit receptor system if not attached to result or problem.
    partner : Any, optional
        Explicit partner system if not attached to result or problem.
    pose_rank : int, default 1
        Initial one-based collection position, independent of scientific pose rank.
    view : MolSysView | None, optional
        An existing MolSysView instance to reuse. If None, a new view is created.
        Displaying a result replaces its molecular scene. Provider loading and
        player failures propagate; several loading calls are not transactional.

    Returns
    -------
    MolSysView
        Interactive MolSysViewer widget with loaded docking components and addon.
    """
    result, problem, search_domain, pose_rank = _resolve_view_inputs(
        item, result, problem, search_domain, pose_rank
    )
    if isinstance(item, PoseInteractions):
        for argument, value in (
            ('receptor', receptor),
            ('partner', partner),
            ('reference', reference),
        ):
            if value is not None:
                raise ArgumentError(
                    arg_name=argument,
                    reason='The interaction binding supplies its complete carrier.',
                )

    import molsysviewer as msv

    from molsysviewer_bindingmt.adapters.complex import (
        render_docking_result,
        set_active_pose,
    )
    from molsysviewer_bindingmt.adapters.shapes import render_search_domain
    from molsysviewer_bindingmt.addon import on_enable

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

    # Enable BindingMT addon
    on_enable(view)

    if isinstance(item, PoseInteractions):
        from molsysviewer_bindingmt.adapters.interactions import (
            _render_pose_interactions,
        )

        return _render_pose_interactions(view, item, search_domain=search_domain)

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
