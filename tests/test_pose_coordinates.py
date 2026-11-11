"""Pose records require finite real coordinates without lossy admission."""

import warnings
from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError


@pytest.fixture(autouse=True)
def no_molecular_operations(monkeypatch):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Coordinate-record admission attempted a molecular operation.')

    for name in ('get', 'set', 'convert', 'select', 'extract', 'copy'):
        monkeypatch.setattr(msm, name, forbidden)


@pytest.mark.parametrize(
    'values',
    [
        [[np.nan, 0, 0]],
        [[np.inf, 0, 0]],
        [[-np.inf, 0, 0]],
        [[1 + 2j, 0, 0]],
        np.asarray([[1, 0, 0]], dtype=complex),
        np.asarray([[True, False, True]]),
        np.asarray([['1', '0', '0']]),
    ],
)
def test_constructor_rejects_invalid_values_before_float_coercion(values):
    quantity = puw.quantity(values, 'angstrom')
    with warnings.catch_warnings():
        warnings.simplefilter('error', np.exceptions.ComplexWarning)
        with pytest.raises(ArgumentError) as caught:
            bmt.DockingPose(quantity)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == 'coordinates'


@pytest.mark.parametrize(
    'values',
    [
        [[np.nan, 0, 0]],
        [[np.inf, 0, 0]],
        [[1 + 2j, 0, 0]],
        [[True, 0, 0]],
        [['1', 0, 0]],
        [[None, 0, 0]],
        [[0, 0, 0], [1, 2]],
    ],
)
def test_saved_pose_rejects_invalid_values_before_quantity_construction(values):
    record = {
        'schema_version': '1.0',
        'coordinates': {'value': values, 'unit': 'angstrom'},
    }
    before = deepcopy(record)
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingPose.from_dict(record)
    assert caught.value.extra['arg_name'] == 'coordinates'
    # NaN does not compare equal; compare preserved representations instead.
    assert repr(record) == repr(before)


def test_normalization_overflow_is_an_argument_error():
    quantity = puw.quantity([[1e308, 0, 0]], 'km')
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingPose(quantity)
    assert caught.value.extra['arg_name'] == 'coordinates'


@pytest.mark.parametrize('value', [np.nan, np.inf, -np.inf])
def test_mutated_live_pose_cannot_export_invalid_coordinates(value):
    pose = bmt.DockingPose(puw.quantity([[0.0, 1.0, 2.0]], 'angstrom'))
    pose.coordinates[0, 0] = puw.quantity(value, 'nm')
    with pytest.raises(ArgumentError) as caught:
        bmt.DockingResult([pose]).to_dict()
    assert caught.value.extra['arg_name'] == 'coordinates'


@pytest.mark.parametrize('dtype', [np.int64, np.float32, np.float64])
def test_valid_coordinates_convert_roundtrip_and_detach_under_caller_policy(dtype):
    values = np.asarray([[1, 2, 3], [4, 5, 6]], dtype=dtype)
    with puw.context(standard_units=['pm', 'fs', 'kJ/mol']):
        policy = puw.configure.get_standard_units()
        incoming = puw.quantity(values, 'angstrom')
        input_unit = str(puw.get_unit(incoming))
        pose = bmt.DockingPose(incoming, pose_id='valid')
        assert str(puw.get_unit(incoming)) == input_unit
        np.testing.assert_array_equal(puw.get_value(incoming), values)
        record = pose.to_dict()
        restored = bmt.DockingPose.from_dict(record)
        np.testing.assert_allclose(
            puw.get_value(restored.coordinates, to_unit='angstrom'), values
        )
        assert restored.n_atoms == 2 and restored.pose_id == 'valid'
        assert puw.configure.get_standard_units() == policy
        record['coordinates']['value'][0][0] = 999
        assert puw.get_value(restored.coordinates, to_unit='angstrom')[
            0, 0
        ] == pytest.approx(1)
        assert pose.to_dict()['coordinates']['value'][0][0] != 999


def test_explicit_shaped_empty_pose_remains_supported():
    pose = bmt.DockingPose(puw.quantity(np.empty((0, 3)), 'angstrom'))
    assert pose.n_atoms == 0
    assert pose.to_dict()['coordinates']['value'] == []
