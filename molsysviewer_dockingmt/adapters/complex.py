"""Complex adapter for building and displaying docking poses in MolSysViewer."""

from __future__ import annotations

from inspect import signature
from numbers import Integral
from typing import Any

from ..runtime import ensure_runtime, record_event
from .shapes import render_search_domain


def _ensure_molsys(entity: Any) -> Any:
    """Convert any supported entity or prepared state into a molsysmt.MolSys."""
    import molsysmt as msm

    if hasattr(entity, 'to_molecular_system'):
        return entity.to_molecular_system()
    return msm.convert(entity, to_form='molsysmt.MolSys')


def build_docking_reference_system(reference: Any, n_poses: int) -> Any:
    """Return a detached reference with one structure per docking pose.

    A static reference is explicitly repeated using MolSysMT extraction. An
    existing trajectory must have exactly ``n_poses`` structures and is copied,
    preserving its order. Frame k is compared with pose k, without alignment,
    interpolation or invented atom correspondence. Other counts are rejected.
    Molecular identity, units and declared structure attributes remain owned by
    MolSysMT. The input is never changed.
    """
    import molsysmt as msm

    if isinstance(n_poses, bool) or not isinstance(n_poses, Integral) or n_poses < 1:
        raise ValueError('n_poses must be a positive integer.')
    source = _ensure_molsys(reference)
    n_structures = msm.get(source, n_structures=True)
    if n_structures == n_poses:
        return msm.copy(source)
    if n_structures == 1:
        return msm.extract(source, structure_indices=[0] * n_poses)
    raise ValueError(
        f'The reference must have 1 or {n_poses} structures; got {n_structures}.'
    )


def _load_reference(view: Any, reference: Any) -> None:
    """Adopt the explicit pairing signature, retaining the pinned legacy profile.

    Temporary compatibility boundary: uibcdf/molsysviewer#151 and
    uibcdf/dockingmt#37. Remove after published pairing support is qualified.
    Never retry provider failures or treat arbitrary **kwargs as support.
    """
    options = {}
    parameter = signature(view.load).parameters.get('structure_pairing')
    if parameter is not None and parameter.kind in (
        parameter.POSITIONAL_OR_KEYWORD,
        parameter.KEYWORD_ONLY,
    ):
        options['structure_pairing'] = 'by_index'
    view.load(reference, label='reference_ligand', mode='add', **options)


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
    if msm.get(rec_sys, n_structures=True) != 1:
        raise ValueError('The receptor must have exactly one structure.')

    if partner is None:
        raise ValueError('A source partner is required to reconstruct molecular poses.')

    ligand_frames = [pose.to_molecular_system(partner) for pose in poses]
    if any(msm.get(frame, n_structures=True) != 1 for frame in ligand_frames):
        raise ValueError('Each reconstructed pose must have exactly one structure.')
    lig_frame0 = ligand_frames[0]
    complex_sys = msm.merge([rec_sys, lig_frame0])

    # DockingMT chooses static-receptor pairing; MolSysMT composes each frame.
    for ligand_frame in ligand_frames[1:]:
        frame_sys = msm.merge([rec_sys, ligand_frame])
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
    """Replace the docking scene and pair reference structures with poses by index.

    Reference counts are validated before loading. Loading and player failures
    propagate; completed runtime state is published only after all calls succeed.
    Several provider calls do not form a transaction: a late failure may leave
    a partially changed scene, which the caller can reload explicitly.

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

    ref_multi = (
        build_docking_reference_system(reference, len(result.poses) or 1)
        if reference is not None
        else None
    )

    # Build and load docking complex
    if receptor is not None and result.poses:
        complex_sys = build_docking_complex_system(
            receptor=receptor,
            poses=result.poses,
            partner=partner,
        )
        view.load(complex_sys, label='docking_complex', mode='replace')

    # Load reference ligand if provided
    if ref_multi is not None:
        _load_reference(view, ref_multi)

    # Render search domain
    if search_domain is not None:
        render_search_domain(view, search_domain)

    # Ensure player starts at pose 1 (index 0)
    player = getattr(view, 'player', None)
    if player is not None and hasattr(player, 'go_to_structure'):
        player.go_to_structure(0)

    # Publish completed state only after all required provider calls succeed.
    runtime = ensure_runtime(view)
    runtime.result = result
    runtime.reference = reference
    runtime.search_domain = search_domain
    runtime.active_pose_rank = 1
    runtime.reference_visible = True

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
