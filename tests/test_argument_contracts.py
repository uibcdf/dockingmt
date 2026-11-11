import numpy as np
import pytest
import pyunitwizard as puw
from argdigest.core.errors import UnknownArgumentError

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError


@pytest.mark.parametrize('argument', ['exhaustiveness', 'n_poses', 'cpu', 'seed'])
@pytest.mark.parametrize('value', [True, 1.5, '2'])
def test_integer_arguments_reject_coercion(argument, value):
    with pytest.raises(ArgumentError) as caught:
        bmt.VinaProtocol(**{argument: value})
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == argument
    assert caught.value.extra['caller'] == 'bindingmt.core.protocol.__init__'


def test_numpy_integer_parameters_and_protocol_round_trip():
    protocol = bmt.VinaProtocol(exhaustiveness=np.int64(2), seed=np.int64(42))
    restored = bmt.VinaProtocol.from_dict(protocol.to_dict())
    assert restored.parameters == protocol.parameters
    assert (
        bmt.VinaProtocol.from_dict({'parameters': {}}).parameters
        == bmt.VinaProtocol().parameters
    )


@pytest.mark.parametrize('value', [3.0, float('nan'), '3', 'invalid-unit-text'])
def test_energy_requires_explicit_units(value):
    with pytest.raises(ArgumentError) as caught:
        bmt.VinaProtocol(energy_range=value)
    assert caught.value.extra['arg_name'] == 'energy_range'


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -1, [1, 2]])
def test_energy_requires_finite_nonnegative_scalar(value):
    with pytest.raises(ArgumentError):
        bmt.VinaProtocol(energy_range=puw.quantity(value, 'kcal/mol'))


def test_energy_string_conversion_and_provider_cause():
    protocol = bmt.VinaProtocol(energy_range='12.552 kJ/mol')
    assert puw.get_value(protocol.energy_range) == pytest.approx(3)
    with pytest.raises(ArgumentError) as caught:
        bmt.VinaProtocol(energy_range=puw.quantity(3, 'nm'))
    assert caught.value.__cause__ is not None


@pytest.mark.parametrize(
    'call',
    [
        lambda: bmt.VinaProtocol(exhaustivness=2),
        lambda: bmt.dock(problem=None, protcol=None),
        lambda: bmt.prepare_ligand(None, stateid='ligand'),
        lambda: bmt.prepare_receptor(None, stateid='receptor'),
    ],
)
def test_public_closed_signatures_reject_unknown_arguments(call):
    with pytest.raises(UnknownArgumentError):
        call()


def test_invalid_problem_fails_before_backend_execution(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('Invalid input reached the backend')

    monkeypatch.setattr(bmt.VinaBackend, 'dock', forbidden)
    with pytest.raises(ArgumentError) as caught:
        bmt.dock(problem='not a DockingProblem')
    assert caught.value.extra['arg_name'] == 'problem'


@pytest.mark.parametrize('prepare', [bmt.prepare_ligand, bmt.prepare_receptor])
def test_preparation_rejects_absent_molecular_input(prepare):
    with pytest.raises(ArgumentError) as caught:
        prepare(None)
    assert caught.value.extra['arg_name'] == 'molecular_system'


@pytest.mark.parametrize(
    'argument,value',
    [
        ('state_id', 1),
        ('state_id', ''),
        ('torsion_dof', True),
        ('active_torsion_bonds', [(0, True)]),
        ('active_torsion_bonds', [(-1, 2)]),
    ],
)
def test_invalid_preparation_options_fail_before_molecular_operations(
    argument, value, monkeypatch
):
    import importlib

    ligand = importlib.import_module('bindingmt.preparation.ligand')
    monkeypatch.setattr(
        ligand,
        'select_one_structure',
        lambda *args: pytest.fail('Unexpected molecular operation'),
    )
    with pytest.raises(ArgumentError) as caught:
        bmt.prepare_ligand(object(), **{argument: value})
    assert caught.value.extra['arg_name'] == argument
