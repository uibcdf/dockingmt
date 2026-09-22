import pytest
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import VinaProtocol
from dockingmt.core.search_domain import BoxRegion


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

    invalid_problem = DockingProblem.__new__(DockingProblem)
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
    )
    d = proto.to_dict()
    assert d['protocol_type'] == 'VinaProtocol'
    assert d['parameters']['exhaustiveness'] == 12
    assert d['parameters']['seed'] == 99
    assert d['parameters']['scoring'] == 'ad4'
    assert d['parameters']['allow_provisional_preparation'] is True

    reconstructed = VinaProtocol.from_dict(d)
    assert reconstructed.exhaustiveness == 12
    assert reconstructed.n_poses == 7
    assert reconstructed.seed == 99
    assert reconstructed.scoring == 'ad4'
    assert reconstructed.allow_provisional_preparation is True
