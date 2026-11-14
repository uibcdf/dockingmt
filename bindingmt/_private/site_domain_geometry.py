"""Offline C2 geometry recipes; molecular placement is deliberately unassessed."""

import numpy as np
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord

from bindingmt._private.interface_records import _require
from bindingmt._private.serialization import json_copy
from bindingmt._private.site_records import keys
from bindingmt._private.smonitor import ArgumentError, CapabilityMismatchError

FORMAT = 'bindingmt.site_domain_geometry'
FIELDS = {name: f'{FORMAT}.{name}' for name in ('padding', 'center', 'lengths')}
ASSURANCE = {
    'scope': 'geometry_only',
    'placement': 'not_assessed',
    'current_finding': 'not_assessed',
    'molecular_correspondence': 'not_assessed',
    'membership': 'not_requested',
}


def _capability(condition, name):
    if not condition:
        raise CapabilityMismatchError(capability=name, engine=FORMAT)


def _quantity(value, field, shape, *, sign=None):
    quantity = QuantityRecord.from_dict(value).to_quantity(
        field=FIELDS[field], unit='nm', dimensionality={'[L]': 1}, form='pint'
    )
    values = np.asarray(puw.get_value(quantity, to_unit='nm'))
    _require(
        values.shape == shape
        and values.dtype.kind in ('i', 'u', 'f')
        and np.isfinite(values).all()
        and (sign is None or (values > 0 if sign == 'positive' else values >= 0).all()),
        field,
        'Use finite length data with the admitted shape and sign.',
    )
    return values


def _sealed(values, field):
    return QuantityRecord.from_quantity(
        puw.quantity(values, 'nm', form='pint'), field=FIELDS[field]
    ).to_dict()


def _padding(value):
    from bindingmt.core.search_domain import _ensure_length_quantity

    if value is None:
        return None, 0.0
    quantity = _ensure_length_quantity(value, 'padding')
    values = np.asarray(puw.get_value(quantity, to_unit='nm'))
    _require(
        values.shape == () and float(values) >= 0,
        'padding',
        'Use a finite nonnegative scalar length, or None for no enlargement.',
    )
    return _sealed(float(values), 'padding'), float(values)


def _geometry(site, method, view, padding):
    from bindingmt._private.site_geometry import _length_quantity, _read_axes

    _require(
        type(method) is str and type(view) is str,
        'method/view',
        'Name the method and eligible view explicitly.',
    )
    views = site.views
    _capability(
        len(views) == 1 and views[0]['kind'] in ('sphere', 'box'),
        'self-contained sphere or box support',
    )
    _capability(view == views[0]['key'], 'explicit eligible geometry view')
    payload = views[0]['payload']
    center = np.asarray(
        puw.get_value(_length_quantity(payload['center'], 'center', (3,)), to_unit='nm')
    )
    kind = views[0]['kind']
    _capability(
        (kind, method) in (('sphere', 'sphere_enclosure'), ('box', 'axis_aligned_box')),
        'admitted sphere/box derivation method',
    )
    if kind == 'box':
        _capability(
            np.array_equal(_read_axes(payload['axes']), np.eye(3)),
            'axis-aligned geometry without rotation or orientation repair',
        )
    try:
        with np.errstate(over='raise', invalid='raise'):
            if kind == 'sphere':
                radius = float(
                    puw.get_value(
                        _length_quantity(payload['radius'], 'radius', (), True),
                        to_unit='nm',
                    )
                )
                lengths = np.full(3, 2 * (radius + np.float64(padding)))
            else:
                original = np.asarray(
                    puw.get_value(
                        _length_quantity(payload['lengths'], 'lengths', (3,), True),
                        to_unit='nm',
                    )
                )
                lengths = original + 2 * np.float64(padding)
    except FloatingPointError as error:
        raise ArgumentError(
            arg_name='padding', reason='The derived full box lengths must stay finite.'
        ) from error
    _require(
        np.isfinite(lengths).all() and (lengths > 0).all(),
        'lengths',
        'The derived full box lengths must stay finite and positive.',
    )
    relation = 'equal' if kind == 'box' and padding == 0 else 'encloses'
    return (
        center,
        lengths,
        {
            'support_relation': relation,
            'added_support': 'none' if relation == 'equal' else 'unquantified',
        },
    )


def derive_geometry_box(site, *, method, view=None, padding=None):
    """Internal implemented substep, not a public placed-domain application."""
    from bindingmt.core.search_domain import BoxRegion
    from bindingmt.core.site import BindingSite

    _require(isinstance(site, BindingSite), 'site', 'Supply a BindingSite declaration.')
    view = 'geometry' if view is None else view
    padding_record, padding_nm = _padding(padding)
    center, lengths, losses = _geometry(site, method, view, padding_nm)
    box = BoxRegion(
        center=puw.quantity(center, 'nm'),
        lengths=puw.quantity(lengths, 'nm'),
        name=site.to_dict()['name'],
    )
    recipe = {
        'format': FORMAT,
        'format_version': '0.1',
        'experimental': True,
        'site': site.to_dict(),
        'site_ref': {**site.definition_ref, 'view_key': view},
        'request': {'method': method, 'view': view, 'padding': padding_record},
        'box': {
            'center': _sealed(center, 'center'),
            'lengths': _sealed(lengths, 'lengths'),
        },
        'losses': losses,
        'assurance': dict(ASSURANCE),
    }
    box._set_derivation(recipe)
    return box


def validate_derivation(record, center, lengths):
    """Recompute retained inputs and bind them to the actual current box."""
    from bindingmt.core.site import BindingSite

    keys(
        record,
        {
            'format',
            'format_version',
            'experimental',
            'site',
            'site_ref',
            'request',
            'box',
            'losses',
            'assurance',
        },
        'derivation',
    )
    _require(
        record['format'] == FORMAT
        and record['format_version'] == '0.1'
        and record['experimental'] is True,
        'derivation',
        'Use the admitted experimental offline recipe version 0.1.',
    )
    site = BindingSite.from_dict(record['site'], experimental=True)
    keys(record['request'], {'method', 'view', 'padding'}, 'request')
    request = record['request']
    _require(
        record['site_ref'] == {**site.definition_ref, 'view_key': request['view']},
        'site_ref',
        'Retain the exact original site, definition and view reference.',
    )
    _require(
        record['assurance'] == ASSURANCE,
        'assurance',
        'Offline geometry has no molecular placement or finding assurance.',
    )
    padding = (
        0.0
        if request['padding'] is None
        else float(_quantity(request['padding'], 'padding', (), sign='nonnegative'))
    )
    expected_center, expected_lengths, losses = _geometry(
        site, request['method'], request['view'], padding
    )
    keys(record['box'], {'center', 'lengths'}, 'box')
    saved_center = _quantity(record['box']['center'], 'center', (3,))
    saved_lengths = _quantity(
        record['box']['lengths'], 'lengths', (3,), sign='positive'
    )
    for field, expected, saved, current in (
        ('center', expected_center, saved_center, center),
        ('lengths', expected_lengths, saved_lengths, lengths),
    ):
        current = np.asarray(puw.get_value(current, to_unit='nm'))
        _require(
            np.array_equal(expected, saved)
            and current.shape == saved.shape
            and current.dtype.kind in ('i', 'u', 'f')
            and np.isfinite(current).all()
            and np.allclose(
                saved,
                current,
                rtol=8 * np.finfo(float).eps,
                atol=0,
            ),
            field,
            'The current box and saved output must match the retained offline recipe.',
        )
    _require(
        record['losses'] == losses,
        'losses',
        'Preserve the admitted geometric relation and unknown added support.',
    )
    return json_copy(record, 'derivation')


def refuse_unplaced_export(record):
    """Fail closed at the numerical backend boundary for this offline profile."""
    if record is not None and record.get('format') == FORMAT:
        raise CapabilityMismatchError(
            capability='molecular placement of offline site geometry is not assessed',
            engine=FORMAT,
        )
