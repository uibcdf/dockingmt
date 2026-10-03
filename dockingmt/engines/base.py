from __future__ import annotations

from abc import ABC, abstractmethod

from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError, CapabilityMismatchError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol
from dockingmt.core.results import DockingPose, DockingResult


class DockingBackend(ABC):
    """Abstract base class for docking calculation backends and engine adapters.

    Each backend advertises its capabilities, validates compatibility with requested
    protocols, and transforms backend-agnostic problems into backend executions and
    normalized DockingResult instances.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the engine/backend."""
        pass

    @property
    @abstractmethod
    def capabilities(self) -> set[str]:
        """Set of capabilities advertised by this backend."""
        pass

    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Whether the backend is available in the current environment."""
        pass

    @arg_digest(config='dockingmt._argdigest')
    def validate_capabilities(self, protocol: DockingProtocol) -> None:
        """Validate that all capabilities required by the protocol are supported.

        Raises
        ------
        CapabilityMismatchError
            If one or more required capabilities are not supported by this backend.
        """
        if protocol is None:
            raise ArgumentError(
                arg_name='protocol', reason='Use a DockingProtocol instance.'
            )
        required = protocol.required_capabilities
        supported = self.capabilities
        missing = required - supported
        if missing:
            unsupported = sorted(list(missing))[0]
            raise CapabilityMismatchError(
                capability=unsupported,
                engine=self.name,
                protocol=protocol.name,
                requested_capabilities=sorted(required),
                supported_capabilities=sorted(supported),
                missing_capabilities=sorted(missing),
            )

    @abstractmethod
    def dock(
        self,
        problem: DockingProblem,
        protocol: DockingProtocol | None = None,
    ) -> DockingResult:
        """Execute docking for the given problem and protocol."""
        pass

    @arg_digest(config='dockingmt._argdigest')
    def score(
        self,
        problem: DockingProblem,
        protocol: DockingProtocol | None = None,
        pose: DockingPose | None = None,
        score_name: str = 'score',
    ) -> DockingPose:
        """Score a prepared fixed conformation when supported by the backend.

        This optional operation keeps existing docking-only adapters compatible.
        """
        raise CapabilityMismatchError(capability='pose_scoring', engine=self.name)
