"""Complex adapter for building and displaying docking poses in MolSysViewer."""

from __future__ import annotations

from typing import Any

import numpy as np
import pyunitwizard as puw

from ..runtime import ensure_runtime, record_event
from .shapes import render_search_domain


def _ensure_molsys(entity: Any) -> Any:
    """Convert any supported entity or prepared state into a molsysmt.MolSys."""
    import molsysmt as msm

    if hasattr(entity, 'to_molecular_system'):
        return entity.to_molecular_system()
    return msm.convert(entity, to_form='molsysmt.MolSys')


def build_docking_complex_system(
    receptor: Any,
    poses: list[Any],
    partner: Any = None,
) -> Any:
    """Build a multi-structure MolSysMT system containing receptor and candidate poses.

    Each structure (frame) corresponds to a docking pose, with frame 0 representing
    the top-ranked pose (rank 1).

    Parameters
    ----------
    receptor : Any
        Receptor molecular system or PreparedReceptor.
    poses : list[DockingPose]
        Candidate docking poses.
    partner : Any
        Source partner molecular system or PreparedLigand providing ligand topology.

    Returns
    -------
    Any
        A multi-structure MolSysMT MolSys system.
    """
    import molsysmt as msm

    if not poses:
        raise ValueError('Cannot build docking complex without candidate poses.')

    rec_sys = _ensure_molsys(receptor)

    if partner is None:
        raise ValueError('A source partner is required to reconstruct molecular poses.')

    ligand_frames = [pose.to_molecular_system(partner) for pose in poses]
    lig_frame0 = ligand_frames[0]
    complex_sys = msm.merge([rec_sys, lig_frame0])

    # If there are additional poses, append their structures
    rec_coords = msm.get(rec_sys, element='atom', coordinates=True)
    rec_vals = puw.get_value(rec_coords)[0]
    rec_unit = puw.get_unit(rec_coords)

    # Base single-structure complex used as a template for additional frames
    base_frame = msm.copy(complex_sys)

    for ligand_frame in ligand_frames[1:]:
        ligand_coords = msm.get(ligand_frame, element='atom', coordinates=True)
        pose_vals = puw.get_value(puw.convert(ligand_coords, to_unit=rec_unit))[0]
        combined_vals = np.concatenate([rec_vals, pose_vals], axis=0)
        frame_coords = puw.quantity(np.expand_dims(combined_vals, axis=0), rec_unit)

        frame_sys = msm.copy(base_frame)
        msm.set(frame_sys, element='atom', coordinates=frame_coords)
        msm.append_structures(complex_sys, frame_sys)

    return complex_sys


def render_docking_result(
    view: Any,
    result: Any,
    receptor: Any = None,
    partner: Any = None,
    reference: Any = None,
    search_domain: Any = None,
) -> Any:
    """Load docking results, receptor, poses, search domain, and reference into MolSysViewer.

    Parameters
    ----------
    view : Any
        Target MolSysView instance.
    result : DockingResult
        The docking result to visualize.
    receptor : Any, optional
        Receptor system. If None, resolved from result.problem.
    partner : Any, optional
        Partner system. If None, resolved from result.problem.
    reference : Any, optional
        Reference crystallographic ligand.
    search_domain : Any, optional
        Search domain. If None, resolved from result.problem or provenance.

    Returns
    -------
    Any
        The MolSysView with loaded components.
    """
    import molsysmt as msm

    runtime = ensure_runtime(view)

    # Resolve receptor
    if receptor is None and getattr(result, 'problem', None) is not None:
        receptor = result.problem.receptor_molsys or result.problem.receptor

    # Resolve partner
    if partner is None and getattr(result, 'problem', None) is not None:
        partner = result.problem.partner_molsys or result.problem.partner

    # Resolve search domain
    if search_domain is None:
        if getattr(result, 'problem', None) is not None:
            search_domain = getattr(result.problem, 'search_domain', None)
        elif 'search_domain' in getattr(result, 'provenance', {}):
            from dockingmt.core.search_domain import BoxRegion

            sd_info = result.provenance['search_domain']
            search_domain = BoxRegion.from_dict(sd_info)

    # Resolve reference
    if reference is None:
        reference = getattr(runtime, 'reference', None)

    # Build and load docking complex
    if receptor is not None and result.poses:
        complex_sys = build_docking_complex_system(
            receptor=receptor,
            poses=result.poses,
            partner=partner,
        )
        view.load(complex_sys, label='docking_complex')

    # Load reference ligand if provided
    if reference is not None and getattr(view, 'load', None) is not None:
        ref_sys = _ensure_molsys(reference)
        n_frames = len(result.poses) if result.poses else 1
        # Replicate frames for reference to match trajectory length
        ref_multi = msm.copy(ref_sys)
        for _ in range(n_frames - 1):
            msm.append_structures(ref_multi, ref_sys)
        try:
            view.load(ref_multi, label='reference_ligand', mode='add')
        except Exception:
            pass

    # Render search domain
    if search_domain is not None:
        render_search_domain(view, search_domain)

    # Update runtime state
    runtime.result = result
    runtime.reference = reference
    runtime.search_domain = search_domain
    runtime.active_pose_rank = 1

    # Ensure player starts at pose 1 (index 0)
    player = getattr(view, 'player', None)
    if player is not None and hasattr(player, 'go_to_structure'):
        try:
            player.go_to_structure(0)
        except Exception:
            pass

    record_event(view, 'render_docking_result', n_poses=len(result.poses))
    return view


def set_active_pose(view: Any, rank: int) -> None:
    """Activate and focus a specific docking pose by 1-based rank."""
    runtime = ensure_runtime(view)
    if runtime.result is None or not runtime.result.poses:
        raise RuntimeError('No docking result loaded in viewer.')

    if rank < 1 or rank > len(runtime.result.poses):
        raise ValueError(
            f'Invalid pose rank {rank}. Must be between 1 and {len(runtime.result.poses)}.'
        )

    player = getattr(view, 'player', None)
    if player is not None and hasattr(player, 'go_to_structure'):
        player.go_to_structure(rank - 1)

    runtime.active_pose_rank = rank
    record_event(view, 'set_active_pose', rank=rank)


def set_reference_visibility(view: Any, visible: bool) -> None:
    """Toggle visibility of the reference ligand."""
    regions = getattr(view, 'regions', None)
    if (
        regions is not None
        and hasattr(regions, 'contains')
        and regions.contains('reference_ligand')
    ):
        region = regions.get('reference_ligand')
        if region is not None:
            if visible:
                region.show()
            else:
                region.hide()
    runtime = ensure_runtime(view)
    runtime.reference_visible = visible
    record_event(view, 'set_reference_visibility', visible=visible)


def clear_docking(view: Any) -> None:
    """Clear docking shapes and reset runtime state."""
    shapes = getattr(view, 'shapes', None)
    if (
        shapes is not None
        and hasattr(shapes, 'contains')
        and shapes.contains('dockingmt:search_domain')
    ):
        try:
            shapes.delete('dockingmt:search_domain')
        except Exception:
            pass

    runtime = ensure_runtime(view)
    runtime.result = None
    runtime.search_domain = None
    runtime.active_pose_rank = 1
    record_event(view, 'clear_docking')
