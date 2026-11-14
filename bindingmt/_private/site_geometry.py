"""Sealed elementary site geometry; validation only, without molecular work."""

import numpy as np
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

from bindingmt._private.interface_records import _require
from bindingmt._private.serialization import json_copy
from bindingmt._private.site_records import capability, keys, text
from bindingmt._private.smonitor import ArgumentError
from bindingmt.core.search_domain import _ensure_length_quantity

FIELDS = {
    k: f'bindingmt.site.geometry.{k}'
    for k in ('center', 'radius', 'lengths', 'box_axes')
}
AXES_KIND = 'urn:bindingmt:site:box-axes'
AXES_CONVENTION = 'rows_are_right_handed_local_axes_in_declared_frame'
AXES_ATOL = 1e-6


def frame_record(frame):
    keys(frame, {'id', 'coordinate_policy', 'pbc'}, 'frame')
    _require(
        text(frame['id'])
        and isinstance(frame['coordinate_policy'], str)
        and type(frame['pbc']) is bool,
        'frame',
        'Declare an explicit frame id, policy and bool PBC flag.',
    )
    capability(
        frame['coordinate_policy'] == 'cartesian' and frame['pbc'] is False,
        'single-image Cartesian site geometry',
    )
    return json_copy(frame, 'frame')


def _check_length(values, field, shape, positive):
    values = np.asarray(values)
    _require(
        values.shape == shape
        and values.dtype.kind in ('i', 'u', 'f')
        and np.isfinite(values).all()
        and (not positive or (values > 0).all()),
        field,
        f'Use finite real length data with shape {shape}'
        + (' and strictly positive extent.' if positive else '.'),
    )
    return values


def _length_record(value, field, shape, positive=False):
    quantity = _ensure_length_quantity(value, field)
    _check_length(puw.get_value(quantity, to_unit='nm'), field, shape, positive)
    return QuantityRecord.from_quantity(quantity, field=FIELDS[field]).to_dict()


def _length_quantity(record, field, shape, positive=False, *, form='pint'):
    quantity = QuantityRecord.from_dict(record).to_quantity(
        field=FIELDS[field], unit='nm', dimensionality={'[L]': 1}, form=form
    )
    _check_length(puw.get_value(quantity, to_unit='nm'), field, shape, positive)
    return quantity


def axes_values(axes):
    if type(axes) is np.ndarray:
        _require(
            axes.dtype.kind in ('i', 'u', 'f'),
            'axes',
            'Use a fully known real numeric matrix.',
        )
        values = axes.copy()
    else:
        _require(
            type(axes) in (list, tuple) and len(axes) == 3,
            'axes',
            'Declare three ordered local axes.',
        )
        for row in axes:
            _require(
                type(row) in (list, tuple)
                and len(row) == 3
                and all(
                    (
                        type(v) in (int, float)
                        or isinstance(v, (np.integer, np.floating))
                    )
                    and not isinstance(v, (bool, np.bool_))
                    for v in row
                ),
                'axes',
                'Use numeric axis entries without units or object coercion.',
            )
        try:
            values = np.asarray(axes, dtype=float)
        except (OverflowError, ValueError) as error:
            raise ArgumentError(
                arg_name='axes', reason='Axis values are not finite float data.'
            ) from error
    values = values.astype(float, copy=True)
    _require(
        values.shape == (3, 3) and np.isfinite(values).all(),
        'axes',
        'Use a finite 3x3 orientation matrix.',
    )
    _require(
        np.allclose(values @ values.T, np.eye(3), rtol=0, atol=AXES_ATOL)
        and np.isclose(np.linalg.det(values), 1, rtol=0, atol=AXES_ATOL),
        'axes',
        'Preserve right-handed orthonormal axes; no orientation repair is performed.',
    )
    return values


def _axes_record(axes):
    values = axes_values(np.eye(3) if axes is None else axes)
    return QuantityRecord.from_quantity(
        puw.quantity(values, 'dimensionless'), field=FIELDS['box_axes'], kind=AXES_KIND
    ).to_dict()


def _read_axes(record):
    quantity = QuantityRecord.from_dict(record).to_quantity(
        field=FIELDS['box_axes'],
        unit='dimensionless',
        dimensionality={},
        kind=AXES_KIND,
        form='pint',
    )
    return axes_values(np.asarray(puw.get_value(quantity, to_unit='dimensionless')))


def geometry_payload(kind, center, frame, *, radius=None, lengths=None, axes=None):
    payload = {
        'frame': frame_record(frame),
        'center': _length_record(center, 'center', (3,)),
    }
    if kind == 'sphere':
        payload['radius'] = _length_record(radius, 'radius', (), True)
    else:
        payload.update(
            lengths=_length_record(lengths, 'lengths', (3,), True),
            axes=_axes_record(axes),
            axes_convention=AXES_CONVENTION,
        )
    return payload


def validate_geometry(kind, payload, scope):
    keys(
        payload,
        {'frame', 'center', 'radius'}
        if kind == 'sphere'
        else {'frame', 'center', 'lengths', 'axes', 'axes_convention'},
        'geometry',
    )
    frame_record(payload['frame'])
    _require(
        scope['kind'] == 'independent' or len(scope['source_structure_indices']) == 1,
        'scope',
        'One saved geometry admits at most one source-structure occurrence.',
    )
    _length_quantity(payload['center'], 'center', (3,))
    if kind == 'sphere':
        _length_quantity(payload['radius'], 'radius', (), True)
    else:
        _length_quantity(payload['lengths'], 'lengths', (3,), True)
        _require(
            payload['axes_convention'] == AXES_CONVENTION,
            'axes',
            'Preserve the declared orientation convention.',
        )
        _read_axes(payload['axes'])


def public_geometry(kind, payload):
    result = {
        'kind': kind,
        'frame': json_copy(payload['frame'], 'frame'),
        'center': _length_quantity(payload['center'], 'center', (3,), form=None),
    }
    if kind == 'sphere':
        result['radius'] = _length_quantity(
            payload['radius'], 'radius', (), True, form=None
        )
    else:
        result.update(
            lengths=_length_quantity(
                payload['lengths'], 'lengths', (3,), True, form=None
            ),
            axes=_read_axes(payload['axes']),
            axes_convention=AXES_CONVENTION,
        )
    return result
