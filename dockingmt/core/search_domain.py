from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from copy import deepcopy
from numbers import Real
from typing import Any

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest

from dockingmt._private.serialization import SCHEMA_VERSION, validate_schema_version
from dockingmt._private.smonitor import ArgumentError


def _descriptor(value):
    """Detach the declared docking recipe, never a native molecular object."""

    def numeric(item):
        if isinstance(item, np.ndarray):
            return item.tolist()
        if isinstance(item, np.generic):
            return item.item()
        raise TypeError('Use JSON data in a domain derivation.')

    try:
        return json.loads(json.dumps(value, default=numeric, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ArgumentError(
            arg_name='derivation', reason='Use finite JSON data for domain derivation.'
        ) from exc


def _validate_derivation(record, center, lengths):
    """Validate a declared recipe and its binding to the current box geometry."""

    def require(condition, reason):
        if not condition:
            raise ArgumentError(arg_name='derivation', reason=reason)

    def axis(value):
        return (
            isinstance(value, list)
            and bool(value)
            and all(type(i) is int and i >= 0 for i in value)
        )

    require(
        isinstance(record, dict)
        and set(record)
        == {
            'schema',
            'method',
            'source',
            'selection',
            'atom_indices',
            'structure_indices',
            'structure_position',
            'selection_chemical_state',
            'structure_chemical_state',
            'padding',
            'box',
        },
        'Use a complete selection-domain derivation record.',
    )
    require(
        record['schema'] == 'dockingmt.box_derivation@1'
        and record['method'] in ('selection_bounds', 'redocking_partner_bounds'),
        'Unsupported domain derivation schema or method.',
    )
    source = record['source']
    require(
        isinstance(source, dict) and set(source) == {'form', 'n_atoms', 'fingerprint'},
        'Invalid domain source descriptor.',
    )
    forms = source['form'] if isinstance(source['form'], list) else [source['form']]
    require(
        bool(forms) and all(isinstance(f, str) and bool(f) for f in forms),
        'Invalid source form.',
    )
    require(
        type(source['n_atoms']) is int and source['n_atoms'] > 0,
        'Invalid source atom count.',
    )
    fingerprint = source['fingerprint']
    require(
        fingerprint is None
        or (
            isinstance(fingerprint, dict)
            and set(fingerprint) == {'kind', 'sha256'}
            and fingerprint['kind'] in ('file', 'literal')
            and isinstance(fingerprint['sha256'], str)
            and re.fullmatch('[0-9a-f]{64}', fingerprint['sha256']) is not None
        ),
        'Invalid input-byte fingerprint.',
    )
    require(
        axis(record['atom_indices'])
        and all(i < source['n_atoms'] for i in record['atom_indices']),
        'Resolved domain atoms must lie on the declared source axis.',
    )
    selection = record['selection']
    require(
        selection is None
        or isinstance(selection, str)
        and bool(selection)
        or axis(selection),
        'Invalid requested selection record.',
    )
    frames = record['structure_indices']
    require(
        frames is None
        or frames == 'all'
        or type(frames) is int
        and frames >= 0
        or axis(frames),
        'Invalid requested structure axis.',
    )
    require(
        type(record['structure_position']) is int and record['structure_position'] == 0,
        'The selection-box policy uses the first returned structure.',
    )
    state = record['selection_chemical_state']
    require(
        state is None
        or state in ('reference', 'structure')
        or type(state) is int
        and state >= 0,
        'Invalid chemical-state selection policy.',
    )
    state = record['structure_chemical_state']
    require(
        state is None
        or (
            isinstance(state, dict)
            and set(state) == {'index', 'id'}
            and type(state['index']) is int
            and state['index'] >= 0
            and (
                state['id'] is None
                or isinstance(state['id'], str)
                and bool(state['id'])
            )
        ),
        'Invalid structure chemical-state association.',
    )
    padding = record['padding']
    require(
        padding is None
        or (
            isinstance(padding, dict)
            and set(padding) == {'value', 'unit'}
            and padding['unit'] == 'nm'
            and isinstance(padding['value'], Real)
            and not isinstance(padding['value'], bool)
            and padding['value'] >= 0
        ),
        'Padding must be a non-negative scalar length record in nm.',
    )
    box = record['box']
    require(
        isinstance(box, dict)
        and set(box) == {'center', 'lengths', 'unit'}
        and box['unit'] == 'nm',
        'Invalid derived box binding.',
    )
    for name, current in [('center', center), ('lengths', lengths)]:
        values = box[name]
        require(
            isinstance(values, list)
            and len(values) == 3
            and all(isinstance(v, Real) and not isinstance(v, bool) for v in values),
            'Derived box binding needs three finite real values per axis.',
        )
        require(
            np.array_equal(values, puw.get_value(current, to_unit='nm')),
            'The box geometry no longer matches its derivation; construct a new domain.',
        )


def _ensure_length_quantity(val: Any, name: str, caller: str | None = None) -> Any:
    """Validate finite real length data and normalize units through PyUnitWizard."""
    try:
        quantity = puw.ensure_quantity(
            val,
            dimensionality={'[L]': 1},
            to_unit='nm',
            standardized=False,
            caller=caller,
        )
    except Exception as exc:
        raise ArgumentError(
            arg_name=name,
            caller=caller,
            reason=(
                f"'{name}' must be a physical quantity with length units; "
                'bare values and units not compatible with length are rejected.'
            ),
        ) from exc
    values = np.asarray(puw.get_value(quantity))
    if (
        not np.issubdtype(values.dtype, np.number)
        or not np.isrealobj(values)
        or not np.isfinite(values).all()
    ):
        raise ArgumentError(
            arg_name=name,
            caller=caller,
            reason=f"'{name}' must contain finite real length values.",
        )
    return puw.quantity(values.astype(float), 'nm')


def _ensure_length_quantity_1d(
    val: Any,
    name: str,
    expected_len: int = 3,
    caller: str | None = None,
) -> Any:
    """Validate that val is a finite 1D length quantity."""
    quantity = _ensure_length_quantity(val, name, caller)
    raw_val = puw.get_value(quantity)
    if raw_val.ndim != 1 or raw_val.shape[0] != expected_len:
        raise ArgumentError(
            arg_name=name,
            caller=caller,
            reason=f"'{name}' must be a 1D vector of length {expected_len}, got shape {raw_val.shape}.",
        )
    return quantity


def _ensure_scalar_length_quantity(val: Any, name: str) -> Any:
    """Validate that val is a finite scalar length quantity."""
    quantity = _ensure_length_quantity(val, name)
    raw_val = puw.get_value(quantity)
    if raw_val.ndim != 0:
        raise ArgumentError(
            arg_name=name,
            reason=f"'{name}' must be a scalar quantity, got shape {raw_val.shape}.",
        )
    return puw.quantity(float(raw_val), 'nm')


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
    lengths : Any, optional
        3D vector with length units defining the edge lengths (size) of the box [Lx, Ly, Lz].
    size : Any, optional
        Alias for lengths. Supply exactly one of lengths and size, with finite,
        strictly positive dimensions.
    name : str, optional
        An optional label or identifier for the search domain.
    """

    @arg_digest(config='dockingmt._argdigest')
    def __init__(
        self,
        center: Any,
        lengths: Any | None = None,
        size: Any | None = None,
        name: str | None = None,
    ):
        if lengths is None and size is None:
            raise ArgumentError(
                arg_name='lengths',
                reason="Either 'lengths' or 'size' must be provided.",
            )
        if lengths is not None and size is not None:
            raise ArgumentError(
                arg_name='lengths',
                reason="Provide only one of 'lengths' and 'size'.",
            )
        self._center = center
        self._lengths = lengths if lengths is not None else size
        self.name = name
        self._derivation = None

    @property
    def derivation(self) -> dict[str, Any] | None:
        """Detached selection recipe, or None for explicit/legacy geometry."""
        if self._derivation is not None:
            _validate_derivation(self._derivation, self._center, self._lengths)
        return deepcopy(self._derivation)

    def _set_derivation(self, value):
        record = _descriptor(value)
        if record is not None:
            _validate_derivation(record, self._center, self._lengths)
        self._derivation = record

    @property
    def center(self) -> Any:
        """3D center of the box as a PyUnitWizard quantity in nanometers."""
        return self._center

    @property
    def lengths(self) -> Any:
        """3D edge lengths [Lx, Ly, Lz] of the box as a PyUnitWizard quantity in nanometers."""
        return self._lengths

    @property
    def size(self) -> Any:
        """3D edge lengths [Lx, Ly, Lz] of the box as a PyUnitWizard quantity in nanometers (alias for lengths)."""
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
        # Reject stale attribution before submitting a derived box to an engine.
        self.derivation
        center_conv = puw.convert(self._center, to_unit=unit)
        lengths_conv = puw.convert(self._lengths, to_unit=unit)
        c_vals = tuple(float(x) for x in puw.get_value(center_conv))
        l_vals = tuple(float(x) for x in puw.get_value(lengths_conv))
        return {
            'center': c_vals,
            'lengths': l_vals,
            'size': l_vals,
            'unit': unit,
        }

    @arg_digest(config='dockingmt._argdigest')
    def contains(self, point: Any) -> bool:
        """Check whether a 3D point is inside the box region."""
        p_val = puw.get_value(point)
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
        """Construct a BoxRegion from ordered corners and optional isotropic padding.

        Corners may coincide along an axis if positive padding yields a box
        with strictly positive dimensions. Inverted corners are rejected.

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
        min_q = _ensure_length_quantity_1d(min_coords, 'min_coords')
        max_q = _ensure_length_quantity_1d(max_coords, 'max_coords')
        min_val = puw.get_value(min_q)
        max_val = puw.get_value(max_q)
        if np.any(min_val > max_val):
            raise ArgumentError(
                arg_name='min_coords',
                reason='min_coords must not exceed max_coords along any axis.',
            )
        center_val = (min_val + max_val) / 2.0
        lengths_val = max_val - min_val

        if padding is not None:
            pad_q = _ensure_scalar_length_quantity(padding, 'padding')
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
        pts_conv = _ensure_length_quantity(points, 'points')
        raw_pts = puw.get_value(pts_conv)
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
        chemical_state: Any = 'reference',
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
        chemical_state : Any, default 'reference'
            Selection context forwarded unchanged to MolSysMT. If several frames
            are requested, the existing policy uses the first returned frame;
            the request and that position are retained in ``derivation``.
        """
        import molsysmt as msm

        from dockingmt.core.problem import _source_fingerprint

        fingerprint = _source_fingerprint(molecular_system)
        indices = msm.select(
            molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            chemical_state=chemical_state,
        )
        coords = msm.get(
            molecular_system,
            element='atom',
            selection=indices,
            structure_indices=structure_indices,
            chemical_state=chemical_state,
            coordinates=True,
        )
        raw_coords = puw.get_value(coords)
        if raw_coords.ndim == 3:
            raw_coords = raw_coords[0]
        pts = puw.quantity(raw_coords, puw.get_unit(coords))
        box = cls.from_points(pts, padding=padding, name=name)
        association = None
        if msm.has_attribute(molecular_system, 'structure_chemical_state_index'):
            state_indices = msm.get(
                molecular_system,
                structure_indices=structure_indices,
                structure_chemical_state_index=True,
            )
            if (
                state_indices is not None
                and len(state_indices)
                and state_indices[0] is not None
            ):
                index = int(state_indices[0])
                state_ids = msm.get(molecular_system, chemical_state_id=True)
                state_id = None if state_ids is None else state_ids[index]
                association = {
                    'index': index,
                    'id': None if state_id in (None, '', 'None') else str(state_id),
                }
        box._record_selection(
            source={
                'form': msm.get_form(molecular_system),
                'n_atoms': int(msm.get(molecular_system, n_atoms=True)),
                'fingerprint': fingerprint,
            },
            selection=selection,
            atom_indices=list(indices),
            structure_indices=structure_indices,
            chemical_state=chemical_state,
            association=association,
            padding=padding,
        )
        if fingerprint != _source_fingerprint(molecular_system):
            raise ArgumentError(
                arg_name='molecular_system',
                reason='Source bytes changed while constructing the domain.',
            )
        return box

    def _record_selection(
        self,
        *,
        source,
        selection,
        atom_indices,
        structure_indices,
        chemical_state,
        association,
        padding,
        method='selection_bounds',
    ):
        """Record an already executed docking-domain construction decision."""
        pad = (
            None
            if padding is None
            else {
                'value': float(
                    puw.get_value(_ensure_scalar_length_quantity(padding, 'padding'))
                ),
                'unit': 'nm',
            }
        )
        self._set_derivation(
            {
                'schema': 'dockingmt.box_derivation@1',
                'method': method,
                'source': source,
                'selection': selection,
                'atom_indices': atom_indices,
                'structure_indices': structure_indices,
                'structure_position': 0,
                'selection_chemical_state': chemical_state,
                'structure_chemical_state': association,
                'padding': pad,
                'box': {
                    'center': puw.get_value(self.center, to_unit='nm').tolist(),
                    'lengths': puw.get_value(self.lengths, to_unit='nm').tolist(),
                    'unit': 'nm',
                },
            }
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize BoxRegion into a versioned dictionary."""
        record = {
            'schema_version': SCHEMA_VERSION,
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
        derivation = self.derivation
        if derivation is not None:
            record['derivation'] = derivation
        return record

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BoxRegion:
        """Reconstruct BoxRegion from a serialized dictionary."""
        validate_schema_version(data, cls.__name__)
        c_data = data['center']
        l_data = data['lengths']
        center = puw.quantity(np.asarray(c_data['value'], dtype=float), c_data['unit'])
        lengths = puw.quantity(np.asarray(l_data['value'], dtype=float), l_data['unit'])
        box = cls(center=center, lengths=lengths, name=data.get('name'))
        box._set_derivation(data.get('derivation'))
        return box

    def __repr__(self) -> str:
        if not hasattr(self, '_lengths'):
            return object.__repr__(self)
        c_val = np.round(puw.get_value(self._center), 3)
        l_val = np.round(puw.get_value(self._lengths), 3)
        name_part = f", name='{self.name}'" if self.name else ''
        return f'BoxRegion(center={c_val} nm, lengths={l_val} nm{name_part})'
