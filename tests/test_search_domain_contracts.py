import numpy as np
import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

from dockingmt import BoxRegion
from dockingmt._private.smonitor import ArgumentError


@pytest.mark.parametrize('argument', ['center', 'lengths', 'size'])
@pytest.mark.parametrize('invalid', [float('nan'), float('inf'), -float('inf')])
def test_box_rejects_nonfinite_geometry(argument, invalid):
    kwargs = {
        'center': puw.quantity([0, 0, 0], 'nm'),
        'size' if argument == 'size' else 'lengths': puw.quantity([1, 1, 1], 'nm'),
    }
    kwargs[argument] = puw.quantity([1, invalid, 1], 'nm')
    with pytest.raises(ArgumentError) as caught:
        BoxRegion(**kwargs)
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == argument


def test_box_rejects_ambiguous_dimensions():
    with pytest.raises(ArgumentError, match='only one'):
        BoxRegion(
            center=puw.quantity([0, 0, 0], 'nm'),
            lengths=puw.quantity([1, 1, 1], 'nm'),
            size=puw.quantity([2, 2, 2], 'nm'),
        )


def test_size_alias_with_explicit_absent_lengths_and_round_trip():
    box = BoxRegion(
        center=puw.quantity([10, 20, 30], 'angstrom'),
        lengths=None,
        size=puw.quantity([20, 40, 60], 'angstrom'),
        name='site',
    )
    recovered = BoxRegion.from_dict(box.to_dict())
    assert recovered.to_dict() == box.to_dict()
    assert recovered.to_backend_box()['size'] == pytest.approx((20, 40, 60))


@pytest.mark.parametrize(
    'call',
    [
        lambda: BoxRegion(centre=puw.quantity([0, 0, 0], 'nm')),
        lambda: BoxRegion(
            center=puw.quantity([0, 0, 0], 'nm'), siz=puw.quantity([1, 1, 1], 'nm')
        ),
    ],
)
def test_box_unknown_keywords_use_argdigest(call):
    with pytest.raises(UnknownArgumentError):
        call()


@pytest.mark.parametrize(
    'points',
    [
        [[2, 3, 4]],
        [[2, 3, 4], [6, 3, 4]],
        [[2, 3, 4], [6, 7, 4]],
    ],
)
def test_flat_point_sets_form_positive_boxes_with_padding(points):
    values = np.asarray(points)
    box = BoxRegion.from_points(puw.quantity(values, 'nm'), padding='2 angstrom')
    np.testing.assert_allclose(
        puw.get_value(box.center), (values.min(0) + values.max(0)) / 2
    )
    np.testing.assert_allclose(puw.get_value(box.lengths), np.ptp(values, axis=0) + 0.4)
    assert all(box.contains(puw.quantity(point, 'nm')) for point in points)


@pytest.mark.parametrize('padding', [None, puw.quantity(0, 'nm')])
def test_flat_points_still_require_positive_padding(padding):
    with pytest.raises(ArgumentError):
        BoxRegion.from_points(puw.quantity([[0, 0, 0]], 'nm'), padding=padding)


@pytest.mark.parametrize(
    'padding',
    [
        puw.quantity(float('nan'), 'nm'),
        puw.quantity(float('inf'), 'nm'),
        puw.quantity(-1, 'nm'),
        puw.quantity([1], 'nm'),
        puw.quantity(1, 'ps'),
        1,
    ],
)
def test_padding_requires_finite_nonnegative_scalar_length(padding):
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_bounds(
            puw.quantity([0, 0, 0], 'nm'),
            puw.quantity([1, 1, 1], 'nm'),
            padding=padding,
        )
    assert caught.value.extra['arg_name'] == 'padding'


@pytest.mark.parametrize('argument', ['min_coords', 'max_coords'])
def test_bounds_reject_nonfinite_corners(argument):
    kwargs = {
        'min_coords': puw.quantity([0, 0, 0], 'nm'),
        'max_coords': puw.quantity([1, 1, 1], 'nm'),
    }
    kwargs[argument] = puw.quantity([0, float('nan'), 0], 'nm')
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_bounds(**kwargs)
    assert caught.value.extra['arg_name'] == argument


def test_padding_never_repairs_inverted_bounds():
    with pytest.raises(ArgumentError):
        BoxRegion.from_bounds(
            puw.quantity([2, 0, 0], 'nm'),
            puw.quantity([1, 1, 1], 'nm'),
            padding=puw.quantity(10, 'nm'),
        )


@pytest.mark.parametrize(
    'values', [[], [[1, 2]], [[0, float('nan'), 0]], [[0, float('inf'), 0]]]
)
def test_points_require_finite_nonempty_xyz_array(values):
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_points(puw.quantity(values, 'nm'), padding=puw.quantity(1, 'nm'))
    assert caught.value.extra['arg_name'] == 'points'


def test_contains_rejects_invalid_point_instead_of_returning_false():
    box = BoxRegion(
        center=puw.quantity([0, 0, 0], 'nm'), size=puw.quantity([2, 2, 2], 'nm')
    )
    with pytest.raises(ArgumentError) as caught:
        box.contains(puw.quantity([float('nan'), 0, 0], 'nm'))
    assert caught.value.extra['arg_name'] == 'point'
    assert box.contains(puw.quantity([1, -1, 1], 'nm'))
    with pytest.raises(UnknownArgumentError):
        box.contains(poit=puw.quantity([0, 0, 0], 'nm'))


def test_box_name_requires_string_or_none():
    with pytest.raises(ArgumentError) as caught:
        BoxRegion(
            center=puw.quantity([0, 0, 0], 'nm'),
            size=puw.quantity([1, 1, 1], 'nm'),
            name=3,
        )
    assert caught.value.extra['arg_name'] == 'name'


def test_explicit_geometry_needs_no_molecular_operations(monkeypatch):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Explicit search-domain geometry requested a molecular operation')

    for operation in ('get', 'select', 'convert'):
        monkeypatch.setattr(msm, operation, forbidden)
    box = BoxRegion.from_points(
        puw.quantity([[0, 0, 0], [2, 0, 0]], 'nm'),
        padding='1 nm',
    )
    recovered = BoxRegion.from_dict(box.to_dict())
    assert recovered.contains(puw.quantity([1, 0, 0], 'nm'))
    assert recovered.to_backend_box()['size'] == pytest.approx((40, 20, 20))
