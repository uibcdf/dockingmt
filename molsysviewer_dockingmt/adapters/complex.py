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


def _fallback_partner_system(n_atoms: int, group_name: str = 'LIG') -> Any:
    """Construct a minimal MolSysMT system with n_atoms as a fallback."""
    from dockingmt._private.conversion import pdb_text_to_molsys

    lines = [
        f'ATOM  {i + 1:5d}  C{i + 1:<3d}{group_name[:3]:3s} A{1:4d}    '
        f'{0.0:8.3f}{0.0:8.3f}{0.0:8.3f}  1.00  0.00           C'
        for i in range(n_atoms)
    ]
    pdb_text = '\n'.join(lines) + '\nEND\n'
    return pdb_text_to_molsys(pdb_text)


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
    partner : Any, optional
        Partner molecular system or PreparedLigand providing ligand topology.

    Returns
    -------
    Any
        A multi-structure MolSysMT MolSys system.
    """
    import molsysmt as msm

    if not poses:
        raise ValueError('Cannot build docking complex without candidate poses.')

    rec_sys = _ensure_molsys(receptor)

    # Resolve ligand base system
    n_lig_atoms = poses[0].n_atoms
    lig_base: Any
    if partner is not None:
        lig_base = _ensure_molsys(partner)
        partner_n_atoms = msm.get(lig_base, element='system', n_atoms=True)
        if partner_n_atoms != n_lig_atoms:
            selected = poses[0].metadata.get('selected_atom_indices')
            mapped = (
                poses[0].metadata.get('pose_atom_order') == 'verified_pdbqt_order'
                and poses[0].metadata.get('selected_partner_n_atoms') == partner_n_atoms
                and isinstance(selected, list)
                and len(selected) == n_lig_atoms
                and len(set(selected)) == len(selected)
                and all(
                    isinstance(i, int) and 0 <= i < partner_n_atoms for i in selected
                )
                and all(
                    pose.metadata.get('selected_atom_indices') == selected
                    for pose in poses
                )
            )
            if not mapped:
                raise ValueError(
                    f'Pose has {n_lig_atoms} atoms but partner has {partner_n_atoms}; '
                    'a verified pose-to-partner atom map is required.'
                )
            lig_base = msm.extract(lig_base, selection=selected)
    else:
        lig_base = _fallback_partner_system(n_lig_atoms)

    # Frame 0
    pose0_coords = puw.quantity(
        np.expand_dims(puw.get_value(poses[0].coordinates), axis=0),
        puw.get_unit(poses[0].coordinates),
    )
    lig_frame0 = msm.copy(lig_base)
    msm.set(lig_frame0, element='atom', coordinates=pose0_coords)
    complex_sys = msm.merge([rec_sys, lig_frame0])

    # If there are additional poses, append their structures
    rec_coords = msm.get(rec_sys, element='atom', coordinates=True)
    rec_vals = puw.get_value(rec_coords)[0]
    rec_unit = puw.get_unit(rec_coords)

    # Base single-structure complex used as a template for additional frames
    base_frame = msm.copy(complex_sys)

    for pose in poses[1:]:
        pose_vals = puw.get_value(puw.convert(pose.coordinates, to_unit=rec_unit))
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
