"""Saved box records retain their scalar meaning before numerical conversion."""

from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw

from bindingmt import BoxRegion
from bindingmt._private.smonitor import ArgumentError


def _record():
    return BoxRegion(
        center=puw.quantity([0, 0, 0], 'nm'),
        lengths=puw.quantity([2, 2, 2], 'nm'),
        name='saved-domain',
    ).to_dict()


@pytest.mark.parametrize('field', ['center', 'lengths'])
@pytest.mark.parametrize(
    'value',
    [
        [True, 1, 1],
        [np.bool_(True), 1, 1],
        np.array([True, True, True]),
        ['3', 1, 1],
        np.array(['3', '2', '1']),
        [3 + 2j, 1, 1],
        np.array([3 + 2j, 1, 1]),
        [],
        [1, 2],
        [[1, 1, 1]],
        [None, 1, 1],
        [np.nan, 1, 1],
        [np.inf, 1, 1],
        [10**400, 1, 1],
    ],
)
def test_box_reader_rejects_invalid_vectors_before_coercion(field, value):
    record = _record()
    record[field]['value'] = value
    before = repr(record)
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_dict(record)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == field
    assert record[field]['value'] is value
    assert repr(record) == before


@pytest.mark.parametrize('field', ['center', 'lengths'])
def test_box_reader_does_not_invoke_arbitrary_float_conversion(field):
    calls = []

    class NumericObject:
        def __float__(self):
            calls.append('float')
            return 3.0

    record = _record()
    record[field]['value'] = [NumericObject(), 1, 1]
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_dict(record)
    assert caught.value.extra['arg_name'] == field
    assert calls == []


@pytest.mark.parametrize('field', ['center', 'lengths'])
@pytest.mark.parametrize(
    'payload', [None, [], 1, {}, {'value': [1, 1, 1]}, {'unit': 'nm'}]
)
def test_box_reader_requires_complete_vector_record(field, payload):
    record = _record()
    record[field] = payload
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_dict(record)
    assert caught.value.extra['arg_name'] == field


@pytest.mark.parametrize('field', ['center', 'lengths'])
def test_box_reader_requires_both_vector_fields(field):
    record = _record()
    del record[field]
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_dict(record)
    assert caught.value.extra['arg_name'] == field


@pytest.mark.parametrize('field', ['center', 'lengths'])
@pytest.mark.parametrize('unit', ['not-a-unit', None, [], 'ps'])
def test_box_reader_preserves_local_unit_diagnostic_and_cause(field, unit):
    record = _record()
    record[field]['unit'] = unit
    before = deepcopy(record)
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_dict(record)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == field
    assert caught.value.__cause__ is not None
    assert record == before


@pytest.mark.parametrize('unit', ['nm', 'angstrom', 'pm'])
@pytest.mark.parametrize('legacy', [False, True])
@pytest.mark.parametrize(
    'values',
    [
        [3, 2, 1],
        (3.5, 2.5, 1.5),
        np.array([3, 2, 1], dtype=np.int64),
        np.array([3.5, 2.5, 1.5]),
    ],
)
def test_box_reader_preserves_valid_vectors_units_and_legacy_records(
    unit, legacy, values
):
    record = _record()
    for field in ['center', 'lengths']:
        record[field] = {'value': values, 'unit': unit}
    if legacy:
        del record['schema_version']
    before = repr(record)
    restored = BoxRegion.from_dict(record)
    assert restored.name == 'saved-domain'
    for field in ['center', 'lengths']:
        np.testing.assert_allclose(
            puw.get_value(getattr(restored, field), to_unit=unit), values
        )
    assert repr(record) == before
    assert BoxRegion.from_dict(restored.to_dict()).to_dict() == restored.to_dict()
    if isinstance(values, np.ndarray):
        previous = values[0].copy()
        try:
            values[0] = 99
            assert puw.get_value(restored.center, to_unit=unit)[0] == pytest.approx(
                previous
            )
            assert puw.get_value(restored.lengths, to_unit=unit)[0] == pytest.approx(
                previous
            )
        finally:
            values[0] = previous


def test_box_reader_still_validates_derivation():
    record = _record()
    record['derivation'] = {'schema': 'unsupported'}
    with pytest.raises(ArgumentError) as caught:
        BoxRegion.from_dict(record)
    assert caught.value.extra['arg_name'] == 'derivation'


def test_box_reader_preserves_quantity_construction_memory_failure(monkeypatch):
    record = _record()
    error = MemoryError('interrupted quantity construction')

    def interrupted(*args, **kwargs):
        raise error

    monkeypatch.setattr(puw, 'quantity', interrupted)
    with pytest.raises(MemoryError) as caught:
        BoxRegion.from_dict(record)
    assert caught.value is error
