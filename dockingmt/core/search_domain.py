from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError


def _ensure_length_quantity_1d(val: Any, name: str, expected_len: int = 3) -> Any:
    """Validate that val is a 1D physical quantity with length dimensions."""
    if not puw.is_quantity(val):
        raise ArgumentError(
            arg_name=name,
            reason=f"'{name}' must be a physical quantity with length units (e.g. using PyUnitWizard).",
        )
    if not puw.are_compatible(val, 'nm'):
        unit_str = str(puw.get_unit(val))
        raise ArgumentError(
            arg_name=name,
            reason=f"'{name}' has unit '{unit_str}', which is not compatible with length.",
        )
    raw_val = np.asarray(puw.get_value(val), dtype=float)
    if raw_val.ndim != 1 or raw_val.shape[0] != expected_len:
        raise ArgumentError(
            arg_name=name,
            reason=f"'{name}' must be a 1D vector of length {expected_len}, got shape {raw_val.shape}.",
        )
    unit = puw.get_unit(val)
    return puw.quantity(raw_val, unit)


def _ensure_scalar_length_quantity(val: Any, name: str) -> Any:
    """Validate that val is a scalar physical quantity with length dimensions."""
    if not puw.is_quantity(val):
        raise ArgumentError(
            arg_name=name,
            reason=f"'{name}' must be a physical quantity with length units.",
        )
    if not puw.are_compatible(val, 'nm'):
        unit_str = str(puw.get_unit(val))
        raise ArgumentError(
            arg_name=name,
            reason=f"'{name}' has unit '{unit_str}', which is not compatible with length.",
        )
    raw_val = np.asarray(puw.get_value(val), dtype=float)
    if raw_val.ndim != 0 and raw_val.size != 1:
        raise ArgumentError(
            arg_name=name,
            reason=f"'{name}' must be a scalar quantity, got shape {raw_val.shape}.",
        )
    return puw.quantity(float(raw_val), puw.get_unit(val))


class SearchDomain(ABC):
    """Abstract base class representing a spatial domain where docking search may occur."""

    @property
    @abstractmethod
    def center(self) -> Any:
        """Centroid of the search domain as a 3D physical quantity."""
        pass

    @property
    @abstractmethod
    def volume(self) -> Any:
        """Volume enclosed by the search domain as a physical quantity with [length]^3 dimensions."""
        pass

    @abstractmethod
    def as_box_approximation(self) -> BoxRegion:
        """Return an explicit BoxRegion approximating or bounding this search domain.

        Backend adapters that only accept rectangular boxes (e.g. AutoDock Vina)
        invoke this method to obtain an explicit, inspectable approximation without
        polluting the richer source domain.
        """
        pass


class BoxRegion(SearchDomain):
    """An orthorhombic (axis-aligned) rectangular box search domain.

    Parameters
    ----------
    center : Any
        3D coordinate vector with length units defining the center of the box.
    lengths : Any
        3D vector with length units defining the edge lengths (size) of the box [Lx, Ly, Lz].
    name : str, optional
        An optional label or identifier for the search domain.
    """

    def __init__(self, center: Any, lengths: Any, name: str | None = None):
        self._center = puw.convert(
            _ensure_length_quantity_1d(center, 'center'), to_unit='nm'
        )
        lengths_q = puw.convert(
            _ensure_length_quantity_1d(lengths, 'lengths'), to_unit='nm'
        )
        lengths_val = puw.get_value(lengths_q)
        if np.any(lengths_val <= 0.0):
            raise ArgumentError(
                arg_name='lengths',
                reason='All box dimensions must be strictly positive (> 0).',
            )
        self._lengths = lengths_q
        self.name = name

    @property
    def center(self) -> Any:
        """3D center of the box as a PyUnitWizard quantity in nanometers."""
        return self._center

    @property
    def lengths(self) -> Any:
        """3D edge lengths [Lx, Ly, Lz] of the box as a PyUnitWizard quantity in nanometers."""
        return self._lengths

    @property
    def bounds(self) -> tuple[Any, Any]:
        """Minimum and maximum corner coordinates as a tuple (min_coords, max_coords)."""
        half = self._lengths / 2.0
        min_c = self._center - half
        max_c = self._center + half
        return (min_c, max_c)

    @property
    def volume(self) -> Any:
        """Enclosed volume as a PyUnitWizard quantity with nm^3 units."""
        vals = puw.get_value(self._lengths)
        v = float(np.prod(vals))
        return puw.quantity(v, 'nm**3')

    def as_box_approximation(self) -> BoxRegion:
        """For a BoxRegion, the approximation is identically self."""
        return self

    def to_backend_box(self, unit: str = 'angstrom') -> dict[str, Any]:
        """Convert the box geometry to raw numerical tuples in the requested unit.

        This boundary conversion facilitates interfacing with external engines (such as
        AutoDock Vina, which operates in Angstroms) while keeping backend-specific
        assumptions out of the core data model.
        """
        center_conv = puw.convert(self._center, to_unit=unit)
        lengths_conv = puw.convert(self._lengths, to_unit=unit)
        c_vals = tuple(float(x) for x in puw.get_value(center_conv))
        l_vals = tuple(float(x) for x in puw.get_value(lengths_conv))
        return {
            'center': c_vals,
            'lengths': l_vals,
            'unit': unit,
        }

    def contains(self, point: Any) -> bool:
        """Check whether a 3D point is inside the box region."""
        p_q = puw.convert(_ensure_length_quantity_1d(point, 'point'), to_unit='nm')
        p_val = puw.get_value(p_q)
        min_val = puw.get_value(self.bounds[0])
        max_val = puw.get_value(self.bounds[1])
        return bool(np.all(p_val >= min_val) and np.all(p_val <= max_val))

    @classmethod
    def from_bounds(
        cls,
        min_coords: Any,
        max_coords: Any,
        padding: Any | None = None,
        name: str | None = None,
    ) -> BoxRegion:
        """Construct a BoxRegion from corner coordinates and optional isotropic padding.

        Parameters
        ----------
        min_coords : Any
            Minimum (x, y, z) corner coordinate with length units.
        max_coords : Any
            Maximum (x, y, z) corner coordinate with length units.
        padding : Any, optional
            Isotropic padding added to all sides (expands lengths by 2 * padding).
        name : str, optional
            Identifier for the box region.
        """
        min_q = puw.convert(
            _ensure_length_quantity_1d(min_coords, 'min_coords'), to_unit='nm'
        )
        max_q = puw.convert(
            _ensure_length_quantity_1d(max_coords, 'max_coords'), to_unit='nm'
        )
        min_val = puw.get_value(min_q)
        max_val = puw.get_value(max_q)
        if np.any(min_val >= max_val):
            raise ArgumentError(
                arg_name='min_coords',
                reason='min_coords must be strictly less than max_coords along all axes.',
            )
        center_val = (min_val + max_val) / 2.0
        lengths_val = max_val - min_val

        if padding is not None:
            pad_q = puw.convert(
                _ensure_scalar_length_quantity(padding, 'padding'), to_unit='nm'
            )
            pad_val = puw.get_value(pad_q)
            if pad_val < 0.0:
                raise ArgumentError(
                    arg_name='padding', reason='padding must be non-negative (>= 0).'
                )
            lengths_val += 2.0 * pad_val

        center = puw.quantity(center_val, 'nm')
        lengths = puw.quantity(lengths_val, 'nm')
        return cls(center=center, lengths=lengths, name=name)

    @classmethod
    def from_points(
        cls,
        points: Any,
        padding: Any | None = None,
        name: str | None = None,
    ) -> BoxRegion:
        """Construct a bounding BoxRegion enclosing a collection of 3D points.

        Parameters
        ----------
        points : Any
            Coordinate array of shape (N, 3) with length units.
        padding : Any, optional
            Isotropic padding added to the bounding box.
        name : str, optional
            Identifier for the box region.
        """
        if not puw.is_quantity(points):
            raise ArgumentError(
                arg_name='points',
                reason="'points' must be a physical quantity with length units.",
            )
        if not puw.are_compatible(points, 'nm'):
            raise ArgumentError(
                arg_name='points',
                reason="'points' units are not compatible with length.",
            )
        pts_conv = puw.convert(points, to_unit='nm')
        raw_pts = np.asarray(puw.get_value(pts_conv), dtype=float)
        if raw_pts.ndim != 2 or raw_pts.shape[1] != 3 or raw_pts.shape[0] == 0:
            raise ArgumentError(
                arg_name='points',
                reason=f"'points' must be a non-empty array of shape (N, 3), got shape {raw_pts.shape}.",
            )
        min_vals = np.min(raw_pts, axis=0)
        max_vals = np.max(raw_pts, axis=0)

        # Handle flat/single point case
        if np.any(min_vals == max_vals) and padding is None:
            raise ArgumentError(
                arg_name='points',
                reason='Points have zero span along at least one axis; provide non-zero padding.',
            )

        min_q = puw.quantity(min_vals, 'nm')
        max_q = puw.quantity(max_vals, 'nm')
        return cls.from_bounds(min_q, max_q, padding=padding, name=name)

    @classmethod
    def from_selection(
        cls,
        molecular_system: Any,
        selection: str = 'all',
        structure_indices: int | list[int] = 0,
        padding: Any | None = None,
        name: str | None = None,
    ) -> BoxRegion:
        """Construct a bounding BoxRegion from a MolSysMT molecular selection.

        Parameters
        ----------
        molecular_system : Any
            Any molecular system recognized by MolSysMT (e.g. MolSys, PDB file,
            path, etc.).
        selection : str, default 'all'
            MolSysMT selection string identifying the atoms to enclose (e.g.
            "molecule_type == 'small molecule'").
        structure_indices : int or list of int, default 0
            Structure/conformation index to extract coordinates from.
        padding : Any, optional
            Isotropic padding with length units added around the bounding box.
        name : str, optional
            Identifier for the box region.
        """
        import molsysmt as msm

        coords = msm.get(
            molecular_system,
            element='atom',
            selection=selection,
            structure_indices=structure_indices,
            coordinates=True,
        )
        raw_coords = puw.get_value(coords)
        if raw_coords.ndim == 3:
            raw_coords = raw_coords[0]
        pts = puw.quantity(raw_coords, puw.get_unit(coords))
        return cls.from_points(pts, padding=padding, name=name)

    def to_dict(self) -> dict[str, Any]:
        """Serialize BoxRegion into a versioned dictionary."""
        return {
            'schema_version': '1.0',
            'type': 'BoxRegion',
            'name': self.name,
            'center': {
                'value': puw.get_value(self._center).tolist(),
                'unit': str(puw.get_unit(self._center)),
            },
            'lengths': {
                'value': puw.get_value(self._lengths).tolist(),
                'unit': str(puw.get_unit(self._lengths)),
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BoxRegion:
        """Reconstruct BoxRegion from a serialized dictionary."""
        c_data = data['center']
        l_data = data['lengths']
        center = puw.quantity(np.asarray(c_data['value'], dtype=float), c_data['unit'])
        lengths = puw.quantity(np.asarray(l_data['value'], dtype=float), l_data['unit'])
        return cls(center=center, lengths=lengths, name=data.get('name'))

    def __repr__(self) -> str:
        c_val = np.round(puw.get_value(self._center), 3)
        l_val = np.round(puw.get_value(self._lengths), 3)
        name_part = f", name='{self.name}'" if self.name else ''
        return f'BoxRegion(center={c_val} nm, lengths={l_val} nm{name_part})'
