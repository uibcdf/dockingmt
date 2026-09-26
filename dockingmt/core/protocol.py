from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Integral
from typing import Any

import pyunitwizard as puw

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
        Maximum energy difference relative to the top pose (in energy or energy/mol units,
        or as float in kcal/mol). Poses with energies exceeding this threshold are discarded.
    seed : int | None, default None
        Random seed for reproducibility. If None, the engine selects an arbitrary seed.
    scoring : str, default 'vina'
        Scoring function to use ('vina', 'vinardo', or 'ad4').
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

    def __init__(
        self,
        exhaustiveness: int = 8,
        n_poses: int = 9,
        energy_range: Any = 3.0,
        seed: int | None = None,
        scoring: str = 'vina',
        cpu: int = 0,
        allow_provisional_preparation: bool = False,
        capture_backend_inputs: bool = False,
        active_torsion_bonds: list[tuple[int, int]] | None = None,
    ):
        if not isinstance(exhaustiveness, (int, float)) or int(exhaustiveness) < 1:
            raise ArgumentError(
                arg_name='exhaustiveness',
                reason=f"'exhaustiveness' must be an integer >= 1, got {exhaustiveness}.",
            )
        self._exhaustiveness = int(exhaustiveness)

        if not isinstance(n_poses, (int, float)) or int(n_poses) < 1:
            raise ArgumentError(
                arg_name='n_poses',
                reason=f"'n_poses' must be an integer >= 1, got {n_poses}.",
            )
        self._n_poses = int(n_poses)

        # Validate energy_range
        if puw.is_quantity(energy_range):
            if not puw.are_compatible(energy_range, 'kcal/mol'):
                raise ArgumentError(
                    arg_name='energy_range',
                    reason=f"'energy_range' unit '{puw.get_unit(energy_range)}' is not compatible with kcal/mol.",
                )
            e_val = float(puw.get_value(puw.convert(energy_range, to_unit='kcal/mol')))
        else:
            try:
                e_val = float(energy_range)
            except (TypeError, ValueError) as exc:
                raise ArgumentError(
                    arg_name='energy_range',
                    reason=f"'energy_range' must be a numeric value or energy quantity, got {energy_range}.",
                ) from exc

        if e_val < 0.0:
            raise ArgumentError(
                arg_name='energy_range',
                reason=f"'energy_range' must be non-negative, got {e_val}.",
            )
        self._energy_range = puw.quantity(e_val, 'kcal/mol')

        if seed is not None and not isinstance(seed, int):
            raise ArgumentError(
                arg_name='seed',
                reason=f"'seed' must be an integer or None, got {type(seed)}.",
            )
        self._seed = seed

        if scoring not in self.SUPPORTED_SCORING:
            raise ArgumentError(
                arg_name='scoring',
                reason=f"Unsupported scoring function '{scoring}'. Must be one of {self.SUPPORTED_SCORING}.",
            )
        self._scoring = scoring

        if not isinstance(cpu, int) or cpu < 0:
            raise ArgumentError(
                arg_name='cpu',
                reason=f"'cpu' must be an integer >= 0, got {cpu}.",
            )
        self._cpu = cpu

        if not isinstance(allow_provisional_preparation, bool):
            raise ArgumentError(
                arg_name='allow_provisional_preparation',
                reason='allow_provisional_preparation must be a bool.',
            )
        self._allow_provisional_preparation = allow_provisional_preparation

        if not isinstance(capture_backend_inputs, bool):
            raise ArgumentError(
                arg_name='capture_backend_inputs',
                reason='capture_backend_inputs must be a bool.',
            )
        self._capture_backend_inputs = capture_backend_inputs

        if active_torsion_bonds is not None and (
            not isinstance(active_torsion_bonds, (list, tuple))
            or any(
                not isinstance(pair, (list, tuple))
                or len(pair) != 2
                or any(isinstance(i, bool) or not isinstance(i, Integral) for i in pair)
                for pair in active_torsion_bonds
            )
        ):
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason='Use pairs of selected-ligand integer atom indices.',
            )
        self._active_torsion_bonds = (
            [tuple(int(i) for i in pair) for pair in active_torsion_bonds]
            if active_torsion_bonds is not None
            else []
        )

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
        e_info = params.get('energy_range', {})
        if isinstance(e_info, dict) and 'value' in e_info and 'unit' in e_info:
            energy_range = puw.quantity(float(e_info['value']), e_info['unit'])
        else:
            energy_range = e_info

        return cls(
            exhaustiveness=params.get('exhaustiveness', 8),
            n_poses=params.get('n_poses', 9),
            energy_range=energy_range if energy_range is not None else 3.0,
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
