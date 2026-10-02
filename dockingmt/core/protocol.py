from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import pyunitwizard as puw
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.problem import DockingProblem


class DockingProtocol(ABC):
    """Abstract base class for docking protocols.

    A protocol specifies how a docking problem should be solved:
    resolved parameters, algorithm stages, required capabilities, and inspectable defaults.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the protocol."""
        pass

    @property
    @abstractmethod
    def required_capabilities(self) -> set[str]:
        """Capabilities required by this protocol from an engine or backend."""
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """Resolved protocol parameters."""
        pass

    @abstractmethod
    def validate_problem(self, problem: DockingProblem) -> None:
        """Validate that a problem is compatible with this protocol."""
        pass

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Serialize protocol specification to a versioned machine-readable dictionary."""
        pass


class VinaProtocol(DockingProtocol):
    """Standard docking protocol for AutoDock Vina.

    Provides inspectable, scientifically meaningful defaults for global search optimization.

    Parameters
    ----------
    exhaustiveness : int, default 8
        Number of Monte Carlo search runs. Higher values explore the conformational
        space more thoroughly at the cost of execution time.
    n_poses : int, default 9
        Maximum number of candidate poses to generate and retrieve.
    energy_range : Any, default 3.0 kcal/mol
        Maximum energy difference relative to the top pose as an energy-per-mole
        quantity or unit-bearing string. None resolves to 3 kcal/mol. Bare numbers
        are rejected. Poses exceeding this threshold are discarded.
    seed : int | None, default None
        Random seed for reproducibility. If None, the engine selects an arbitrary seed.
    scoring : str, default 'vina'
        Recognized scoring function ('vina', 'vinardo', or 'ad4'). The current
        VinaBackend executes 'vina' and 'vinardo'. AD4 intent can be serialized,
        but execution requires external affinity-map support absent from the adapter.
    cpu : int, default 0
        Number of CPU threads to utilize. 0 detects and uses all available cores.
    allow_provisional_preparation : bool, default False
        Permit DockingMT's temporary zero-charge or heuristic AutoDock typing path.
        Results from this path are exploratory and their chemistry remains unvalidated.
    capture_backend_inputs : bool, default False
        Include the exact PDBQT input bytes in result provenance for independent audit.
    active_torsion_bonds : list[tuple[int, int]] | None, default None
        Explicit selected-ligand atom-index pairs to rotate during automatic ligand
        preparation. None keeps the ligand rigid. Requires a complete molecular graph.
    """

    SUPPORTED_SCORING = ('vina', 'vinardo', 'ad4')

    @arg_digest(config='dockingmt._argdigest')
    def __init__(
        self,
        exhaustiveness: int = 8,
        n_poses: int = 9,
        energy_range: Any = None,
        seed: int | None = None,
        scoring: str = 'vina',
        cpu: int = 0,
        allow_provisional_preparation: bool = False,
        capture_backend_inputs: bool = False,
        active_torsion_bonds: list[tuple[int, int]] | None = None,
    ):
        self._exhaustiveness = exhaustiveness
        self._n_poses = n_poses
        self._energy_range = energy_range
        self._seed = seed
        self._scoring = scoring
        self._cpu = cpu
        self._allow_provisional_preparation = allow_provisional_preparation
        self._capture_backend_inputs = capture_backend_inputs
        self._active_torsion_bonds = active_torsion_bonds or []

    @property
    def name(self) -> str:
        """Name of the protocol."""
        return 'VinaProtocol'

    @property
    def exhaustiveness(self) -> int:
        """Number of Monte Carlo search runs."""
        return self._exhaustiveness

    @property
    def n_poses(self) -> int:
        """Maximum number of candidate poses to return."""
        return self._n_poses

    @property
    def energy_range(self) -> Any:
        """Energy cutoff threshold relative to the top pose (PyUnitWizard quantity)."""
        return self._energy_range

    @property
    def seed(self) -> int | None:
        """Random seed for execution."""
        return self._seed

    @property
    def scoring(self) -> str:
        """Scoring function name."""
        return self._scoring

    @property
    def cpu(self) -> int:
        """Number of CPU threads requested."""
        return self._cpu

    @property
    def allow_provisional_preparation(self) -> bool:
        """Whether temporary DockingMT chemistry may be sent to Vina."""
        return self._allow_provisional_preparation

    @property
    def capture_backend_inputs(self) -> bool:
        """Whether result provenance retains the submitted PDBQT bytes."""
        return self._capture_backend_inputs

    @property
    def active_torsion_bonds(self) -> list[tuple[int, int]]:
        """Selected source-ligand bonds for automatic preparation."""
        return list(self._active_torsion_bonds)

    @property
    def required_capabilities(self) -> set[str]:
        """Capabilities required by VinaProtocol."""
        capabilities = {
            'rigid_receptor',
            'small_molecule',
            'box_search',
            f'scoring_{self._scoring}',
        }
        if self._active_torsion_bonds:
            capabilities.add('flexible_ligand')
        return capabilities

    @property
    def parameters(self) -> dict[str, Any]:
        """Dictionary of resolved parameters."""
        return {
            'exhaustiveness': self._exhaustiveness,
            'n_poses': self._n_poses,
            'energy_range': {
                'value': float(puw.get_value(self._energy_range)),
                'unit': str(puw.get_unit(self._energy_range)),
            },
            'seed': self._seed,
            'scoring': self._scoring,
            'cpu': self._cpu,
            'allow_provisional_preparation': self._allow_provisional_preparation,
            'capture_backend_inputs': self._capture_backend_inputs,
            'active_torsion_bonds': [list(pair) for pair in self._active_torsion_bonds],
        }

    def validate_problem(self, problem: DockingProblem) -> None:
        """Validate problem compatibility with VinaProtocol.

        Requires problem.search_domain to support box representation (to_backend_box)
        or box approximation (as_box_approximation).
        """
        if not (
            hasattr(problem.search_domain, 'to_backend_box')
            or hasattr(problem.search_domain, 'as_box_approximation')
        ):
            raise ArgumentError(
                arg_name='problem.search_domain',
                reason=(
                    f"VinaProtocol requires a box-compatible SearchDomain supporting 'to_backend_box' "
                    f"or 'as_box_approximation', got {type(problem.search_domain).__name__}."
                ),
            )

    def to_dict(self) -> dict[str, Any]:
        """Serialize protocol specification to a versioned machine-readable dictionary."""
        return {
            'schema_version': '1.0',
            'protocol_type': 'VinaProtocol',
            'parameters': self.parameters,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VinaProtocol:
        """Reconstruct VinaProtocol from a serialized dictionary."""
        params = data.get('parameters', {})
        e_info = params.get('energy_range')
        if isinstance(e_info, dict) and 'value' in e_info and 'unit' in e_info:
            energy_range = puw.quantity(float(e_info['value']), e_info['unit'])
        else:
            energy_range = e_info

        return cls(
            exhaustiveness=params.get('exhaustiveness', 8),
            n_poses=params.get('n_poses', 9),
            energy_range=energy_range,
            seed=params.get('seed'),
            scoring=params.get('scoring', 'vina'),
            cpu=params.get('cpu', 0),
            allow_provisional_preparation=params.get(
                'allow_provisional_preparation', False
            ),
            capture_backend_inputs=params.get('capture_backend_inputs', False),
            active_torsion_bonds=params.get('active_torsion_bonds'),
        )

    def __repr__(self) -> str:
        if not hasattr(self, '_energy_range'):
            # Argument validation can emit a signal before initialization.
            return object.__repr__(self)
        e_val = puw.get_value(self._energy_range)
        e_unit = puw.get_unit(self._energy_range)
        return (
            f'VinaProtocol(exhaustiveness={self._exhaustiveness}, n_poses={self._n_poses}, '
            f'energy_range={e_val} {e_unit}, scoring={self._scoring!r}, '
            f'seed={self._seed}, '
            f'allow_provisional_preparation={self._allow_provisional_preparation}, '
            f'active_torsion_bonds={self._active_torsion_bonds}, '
            f'capture_backend_inputs={self._capture_backend_inputs})'
        )
