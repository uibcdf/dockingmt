"""Shape adapters for rendering docking search domains in MolSysViewer."""

from __future__ import annotations

from typing import Any

import numpy as np
import pyunitwizard as puw

from .._scene import domain_layer
from ..runtime import ensure_runtime, record_event


def _clear_domain_layers(view: Any) -> None:
    """Retain failed handles for retry and leave reused tags to their current owner."""
    runtime = ensure_runtime(view)
    shapes = getattr(view, 'shapes', None)
    if runtime.domain_layers and shapes is None:
        raise RuntimeError(
            'Owned search-domain cleanup requires Viewer shapes support.'
        )
    for layer in runtime.domain_layers.copy():
        if shapes.get(layer.tag) is layer:
            layer.delete()
        runtime.domain_layers.remove(layer)
        if runtime.domain_layer is layer:
            runtime.domain_layer = None


def compute_box_wireframe_coordinate_pairs(box_or_domain: Any) -> Any:
    """Compute the 12 edge coordinate pairs defining a 3D box wireframe.

    Parameters
    ----------
    box_or_domain : Any
        A SearchDomain or BoxRegion instance exposing ``bounds`` or
        ``as_box_approximation()``.

    Returns
    -------
    Any
        A PyUnitWizard quantity of shape (12, 2, 3) containing the start and end
        3D coordinates for all 12 box edges in Angstroms.
    """
    if hasattr(box_or_domain, 'as_box_approximation'):
        box = box_or_domain.as_box_approximation()
    else:
        box = box_or_domain

    min_c, max_c = box.bounds

    # Convert bounds to angstroms for MolSysViewer wire format
    min_vals = np.asarray(
        puw.get_value(puw.convert(min_c, to_unit='angstrom')), dtype=float
    )
    max_vals = np.asarray(
        puw.get_value(puw.convert(max_c, to_unit='angstrom')), dtype=float
    )

    x0, y0, z0 = min_vals
    x1, y1, z1 = max_vals

    # 8 box corners
    corners = [
        [x0, y0, z0],  # 0
        [x0, y0, z1],  # 1
        [x0, y1, z0],  # 2
        [x0, y1, z1],  # 3
        [x1, y0, z0],  # 4
        [x1, y0, z1],  # 5
        [x1, y1, z0],  # 6
        [x1, y1, z1],  # 7
    ]

    # 12 edges connecting pairs of corners
    edge_indices = [
        # Parallel to X
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
        # Parallel to Y
        (0, 2),
        (1, 3),
        (4, 6),
        (5, 7),
        # Parallel to Z
        (0, 1),
        (2, 3),
        (4, 5),
        (6, 7),
    ]

    coord_pairs = [[corners[i], corners[j]] for i, j in edge_indices]
    return puw.quantity(np.asarray(coord_pairs, dtype=float), 'angstrom')


def render_search_domain(
    view: Any,
    search_domain: Any,
    radius: str = '0.1 angstrom',
    color: int = 0x2288EE,
    tag: str = 'dockingmt:search_domain',
) -> Any:
    """Render a search domain as a wireframe box shape in MolSysViewer.

    Parameters
    ----------
    view : Any
        The target MolSysView instance.
    search_domain : Any
        The SearchDomain or BoxRegion to render.
    radius : str, default '0.1 angstrom'
        Cylinder radius of the wireframe edges.
    color : int, default 0x2288EE
        Hexadecimal RGB color code.
    tag : str, default 'dockingmt:search_domain'
        Unique identifier for the shape layer.

    Returns
    -------
    Any
        The created or updated ShapeLayer.
    """
    runtime = ensure_runtime(view)

    # Validate docking geometry before touching any existing scene element.
    coord_pairs = compute_box_wireframe_coordinate_pairs(search_domain)
    shapes = getattr(view, 'shapes', None)
    if shapes is None or not callable(
        getattr(getattr(shapes, 'links', None), 'add_links', None)
    ):
        raise RuntimeError(
            'Search-domain rendering requires public Viewer shapes support.'
        )
    previous = shapes.get(tag)
    if previous is not None:
        if not any(item is previous for item in runtime.domain_layers):
            raise ValueError(
                f'Shape tag {tag!r} is already owned by another scene element.'
            )
        previous.delete()
        runtime.domain_layers.remove(previous)
        if runtime.domain_layer is previous:
            runtime.domain_layer = None
    layer = shapes.links.add_links(
        coordinate_pairs=coord_pairs,
        radius=radius,
        color=color,
        tag=tag,
    )
    if layer is None:
        raise RuntimeError('The Viewer did not return a rendered search-domain handle.')

    runtime.domain_layers.append(layer)
    runtime.domain_layer = layer
    runtime.search_domain = search_domain
    runtime.domain_visible = True
    record_event(view, 'render_search_domain', tag=tag)
    return layer


def set_search_domain_visibility(
    view: Any,
    visible: bool,
    tag: str | None = None,
) -> None:
    """Toggle the visibility of the search domain wireframe box."""
    layer = domain_layer(view, tag)
    if visible:
        layer.show()
    else:
        layer.hide()
    runtime = ensure_runtime(view)
    runtime.domain_visible = visible
    record_event(view, 'set_search_domain_visibility', visible=visible)
