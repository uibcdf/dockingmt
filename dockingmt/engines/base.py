from __future__ import annotations

from abc import ABC, abstractmethod

from dockingmt._private.smonitor import CapabilityMismatchError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol
from dockingmt.core.results import DockingResult


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

    def validate_capabilities(self, protocol: DockingProtocol) -> None:
        """Validate that all capabilities required by the protocol are supported.

        Raises
        ------
        CapabilityMismatchError
            If one or more required capabilities are not supported by this backend.
        """
        missing = protocol.required_capabilities - self.capabilities
        if missing:
            unsupported = sorted(list(missing))[0]
            raise CapabilityMismatchError(capability=unsupported, engine=self.name)

    @abstractmethod
    def dock(
        self,
        problem: DockingProblem,
        protocol: DockingProtocol | None = None,
    ) -> DockingResult:
        """Execute docking for the given problem and protocol."""
        pass
