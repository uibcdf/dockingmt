from __future__ import annotations

import smonitor

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol, VinaProtocol
from dockingmt.core.results import DockingResult
from dockingmt.engines.base import DockingBackend
from dockingmt.engines.vina import VinaBackend


@smonitor.signal(tags=['api', 'docking'])
def dock(
    problem: DockingProblem,
    protocol: DockingProtocol | None = None,
    backend: DockingBackend | str | None = None,
) -> DockingResult:
    """Execute molecular docking calculation.

    Parameters
    ----------
    problem : DockingProblem
        The scientific docking problem specification.
    protocol : DockingProtocol | None, optional
        Protocol governing the docking calculation. If None, defaults to VinaProtocol().
    backend : DockingBackend | str | None, optional
        Docking calculation backend or backend name (e.g. 'vina'). If None, an
        appropriate backend is resolved based on the protocol.

    Returns
    -------
    DockingResult
        Normalized docking result containing candidate poses, scores, and provenance.
    """
    if protocol is None:
        protocol = VinaProtocol()

    resolved_backend: DockingBackend
    if backend is None:
        if isinstance(protocol, VinaProtocol):
            resolved_backend = VinaBackend()
        else:
            raise ArgumentError(
                arg_name='backend',
                reason=f"No default backend available for protocol '{type(protocol).__name__}'.",
            )
    elif isinstance(backend, str):
        if backend.lower() == 'vina':
            resolved_backend = VinaBackend()
        else:
            raise ArgumentError(
                arg_name='backend',
                reason=f"Unsupported backend name '{backend}'. Supported: ['vina'].",
            )
    elif isinstance(backend, DockingBackend):
        resolved_backend = backend
    else:
        raise ArgumentError(
            arg_name='backend',
            reason=f"'backend' must be a DockingBackend instance or string, got {type(backend).__name__}.",
        )

    result = resolved_backend.dock(problem=problem, protocol=protocol)
    result.problem = problem
    return result
