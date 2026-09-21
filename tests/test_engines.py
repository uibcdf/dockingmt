import pytest
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError, CapabilityMismatchError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol, VinaProtocol
from dockingmt.core.results import DockingResult
from dockingmt.core.search_domain import BoxRegion
from dockingmt.dock import dock
from dockingmt.engines.vina import VinaBackend


class DummyCustomProtocol(DockingProtocol):
    @property
    def name(self):
        return 'DummyCustomProtocol'

    @property
    def required_capabilities(self):
        return {'flexible_receptor', 'quantum_scoring'}

    @property
    def parameters(self):
        return {}

    def validate_problem(self, problem):
        pass

    def to_dict(self):
        return {}


def test_capability_validation():
    backend = VinaBackend()
    # Vina backend does not support flexible_receptor or quantum_scoring
    custom_proto = DummyCustomProtocol()
    with pytest.raises(CapabilityMismatchError) as exc:
        backend.validate_capabilities(custom_proto)
    assert 'not supported by engine' in str(exc.value)


MINIMAL_REC_PDBQT = """ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00     0.000 N
ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00  0.00     0.000 C
ATOM      3  C   ALA A   1       2.009   1.428   0.000  1.00  0.00     0.000 C
ATOM      4  O   ALA A   1       1.246   2.392   0.000  1.00  0.00     0.000 OA
"""

MINIMAL_LIG_PDBQT = """ROOT
ATOM      1  C1  LIG A   1       0.000   0.000   0.000  1.00  0.00     0.000 C
ATOM      2  C2  LIG A   1       1.500   0.000   0.000  1.00  0.00     0.000 C
ENDROOT
TORSDOF 0
"""


def test_vina_backend_docking_execution():
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'angstrom'),
        size=puw.quantity([10.0, 10.0, 10.0], 'angstrom'),
    )

    problem = DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=MINIMAL_LIG_PDBQT,
        search_domain=box,
        metadata={
            'partner_state_id': 'lig_state_1',
            'receptor_state_id': 'rec_state_1',
        },
    )

    protocol = VinaProtocol(exhaustiveness=1, n_poses=2, seed=123)

    result = backend.dock(problem, protocol)

    assert isinstance(result, DockingResult)
    assert len(result) > 0
    top_pose = result.top_pose
    assert top_pose is not None
    assert top_pose.rank == 1
    assert top_pose.partner_state_id == 'lig_state_1'
    assert top_pose.receptor_state_id == 'rec_state_1'
    assert 'vina' in top_pose.scores
    assert puw.are_compatible(top_pose.coordinates, 'nm')

    # Provenance checks
    assert result.provenance['backend'] == 'vina'
    assert 'elapsed_seconds' in result.provenance
    assert result.provenance['seed'] == 123


def test_dock_top_level_api():
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'angstrom'),
        size=puw.quantity([10.0, 10.0, 10.0], 'angstrom'),
    )

    problem = DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=MINIMAL_LIG_PDBQT,
        search_domain=box,
    )

    protocol = VinaProtocol(exhaustiveness=1, n_poses=1, seed=42)

    # Calling top-level dockingmt.dock
    result = dock(problem, protocol=protocol, backend='vina')
    assert isinstance(result, DockingResult)
    assert len(result) >= 1
    assert result.provenance['backend'] == 'vina'


def test_dock_invalid_backend():
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([1.0, 1.0, 1.0], 'nm'),
    )
    problem = DockingProblem(
        receptor='rec.pdbqt', partner='lig.pdbqt', search_domain=box
    )

    with pytest.raises(ArgumentError):
        dock(problem, backend='nonexistent_engine')

    with pytest.raises(ArgumentError):
        dock(problem, backend=12345)  # type: ignore
