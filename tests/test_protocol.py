from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw

from bindingmt._private.smonitor import ArgumentError
from bindingmt.core.problem import DockingProblem
from bindingmt.core.protocol import VinaProtocol
from bindingmt.core.search_domain import BoxRegion


def test_vina_protocol_defaults():
    proto = VinaProtocol()
    assert proto.exhaustiveness == 8
    assert proto.n_poses == 9
    assert puw.are_compatible(proto.energy_range, 'kcal/mol')
    assert float(puw.get_value(proto.energy_range)) == 3.0
    assert proto.scoring == 'vina'
    assert proto.seed is None
    assert proto.cpu == 0
    assert proto.allow_provisional_preparation is False
    assert proto.capture_backend_inputs is False
    assert proto.collect_timings is False
    assert 'rigid_receptor' in proto.required_capabilities
    assert 'box_search' in proto.required_capabilities
    assert 'scoring_vina' in proto.required_capabilities
    assert 'VinaProtocol' in repr(proto)


def test_vina_protocol_custom_parameters():
    proto = VinaProtocol(
        exhaustiveness=16,
        n_poses=5,
        energy_range=puw.quantity(12.552, 'kJ/mol'),  # ~3 kcal/mol
        seed=42,
        scoring='vinardo',
        cpu=4,
    )
    assert proto.exhaustiveness == 16
    assert proto.n_poses == 5
    assert float(puw.get_value(proto.energy_range)) == pytest.approx(3.0, rel=1e-2)
    assert proto.seed == 42
    assert proto.scoring == 'vinardo'
    assert proto.cpu == 4
    assert 'scoring_vinardo' in proto.required_capabilities


def test_vina_protocol_validation_errors():
    with pytest.raises(ArgumentError):
        VinaProtocol(exhaustiveness=0)

    with pytest.raises(ArgumentError):
        VinaProtocol(n_poses=-1)

    with pytest.raises(ArgumentError):
        VinaProtocol(energy_range=-2.0)

    with pytest.raises(ArgumentError):
        VinaProtocol(energy_range=puw.quantity(5.0, 'nm'))  # incompatible unit

    with pytest.raises(ArgumentError):
        VinaProtocol(scoring='nonexistent_scoring_fx')

    with pytest.raises(ArgumentError):
        VinaProtocol(cpu=-1)

    with pytest.raises(ArgumentError):
        VinaProtocol(allow_provisional_preparation='yes')

    with pytest.raises(ArgumentError):
        VinaProtocol(capture_backend_inputs='yes')

    with pytest.raises(ArgumentError):
        VinaProtocol(collect_timings='yes')


def test_vina_protocol_problem_validation():
    proto = VinaProtocol()
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([1.0, 1.0, 1.0], 'nm'),
    )
    problem = DockingProblem(
        receptor='rec.pdbqt',
        partner='lig.pdbqt',
        search_domain=box,
    )
    # Should not raise
    proto.validate_problem(problem)

    class IncompatibleDomain:
        pass

    invalid_problem = problem
    invalid_problem._search_domain = IncompatibleDomain()

    with pytest.raises(ArgumentError) as exc:
        proto.validate_problem(invalid_problem)
    assert 'box-compatible SearchDomain' in str(exc.value)


def test_vina_protocol_serialization():
    proto = VinaProtocol(
        exhaustiveness=12,
        n_poses=7,
        seed=99,
        scoring='ad4',
        allow_provisional_preparation=True,
        capture_backend_inputs=True,
        collect_timings=True,
    )
    d = proto.to_dict()
    assert d['protocol_type'] == 'VinaProtocol'
    assert d['parameters']['exhaustiveness'] == 12
    assert d['parameters']['seed'] == 99
    assert d['parameters']['scoring'] == 'ad4'
    assert d['parameters']['allow_provisional_preparation'] is True
    assert d['parameters']['capture_backend_inputs'] is True
    assert d['parameters']['collect_timings'] is True

    reconstructed = VinaProtocol.from_dict(d)
    assert reconstructed.exhaustiveness == 12
    assert reconstructed.n_poses == 7
    assert reconstructed.seed == 99
    assert reconstructed.scoring == 'ad4'
    assert reconstructed.allow_provisional_preparation is True
    assert reconstructed.capture_backend_inputs is True
    assert reconstructed.collect_timings is True

    del d['parameters']['collect_timings']
    assert VinaProtocol.from_dict(d).collect_timings is False


@pytest.mark.parametrize(
    'value',
    [True, False, '3', 'not-energy', [], [3], 3 + 0j, None, {}, np.nan, np.inf, -1],
)
def test_protocol_reader_rejects_invalid_saved_energy_without_coercion(value):
    record = {'parameters': {'energy_range': {'value': value, 'unit': 'kcal/mol'}}}
    with pytest.raises(ArgumentError) as caught:
        VinaProtocol.from_dict(record)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == 'energy_range'
    assert record['parameters']['energy_range']['value'] is value


def test_protocol_reader_does_not_invoke_arbitrary_numeric_coercion():
    calls = []

    class NumericText:
        def __float__(self):
            calls.append('float')
            return 3.0

    with pytest.raises(ArgumentError):
        VinaProtocol.from_dict(
            {
                'parameters': {
                    'energy_range': {'value': NumericText(), 'unit': 'kcal/mol'}
                }
            }
        )
    assert calls == []


@pytest.mark.parametrize('parameters', [None, [], 'parameters', 1, True])
def test_protocol_reader_requires_parameter_mapping(parameters):
    with pytest.raises(ArgumentError) as caught:
        VinaProtocol.from_dict({'parameters': parameters})
    assert caught.value.extra['arg_name'] == 'parameters'


@pytest.mark.parametrize('unit', ['not-a-unit', None, [], 'nm'])
def test_protocol_reader_wraps_invalid_energy_units(unit):
    record = {'parameters': {'energy_range': {'value': 3, 'unit': unit}}}
    before = deepcopy(record)
    with pytest.raises(ArgumentError) as caught:
        VinaProtocol.from_dict(record)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == 'energy_range'
    assert caught.value.__cause__ is not None
    assert record == before


@pytest.mark.parametrize('value', [0, 3, 3.5, np.int64(3), np.float64(3.5)])
@pytest.mark.parametrize('unit', ['kcal/mol', 'kJ/mol'])
def test_protocol_reader_preserves_valid_energy_and_caller_record(value, unit):
    record = {'parameters': {'energy_range': {'value': value, 'unit': unit}}}
    before = deepcopy(record)
    restored = VinaProtocol.from_dict(record)
    assert puw.get_value(restored.energy_range, to_unit=unit) == pytest.approx(value)
    assert record == before
    assert VinaProtocol.from_dict(restored.to_dict()).to_dict() == restored.to_dict()


def test_protocol_reader_retains_legacy_default_and_unit_bearing_string():
    assert VinaProtocol.from_dict({}).to_dict() == VinaProtocol().to_dict()
    assert (
        VinaProtocol.from_dict({'parameters': {}}).to_dict() == VinaProtocol().to_dict()
    )
    restored = VinaProtocol.from_dict({'parameters': {'energy_range': '12.552 kJ/mol'}})
    assert puw.get_value(restored.energy_range, to_unit='kcal/mol') == pytest.approx(3)


@pytest.mark.parametrize('energy_record', [{}, {'value': 3}, {'unit': 'kcal/mol'}])
def test_protocol_reader_requires_complete_saved_energy_record(energy_record):
    before = deepcopy(energy_record)
    with pytest.raises(ArgumentError) as caught:
        VinaProtocol.from_dict({'parameters': {'energy_range': energy_record}})
    assert caught.value.extra['arg_name'] == 'energy_range'
    assert energy_record == before


def test_protocol_reader_preserves_quantity_construction_resource_failure(monkeypatch):
    error = MemoryError('quantity construction interrupted')

    def interrupted(*args, **kwargs):
        raise error

    monkeypatch.setattr(puw, 'quantity', interrupted)
    with pytest.raises(MemoryError) as caught:
        VinaProtocol.from_dict(
            {'parameters': {'energy_range': {'value': 3, 'unit': 'kcal/mol'}}}
        )
    assert caught.value is error
