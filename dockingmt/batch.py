"""Incremental local execution of already prepared docking problems."""

from copy import deepcopy

import smonitor
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.outcome import DockingOutcome
from dockingmt.core.problem import DockingProblem, _is_pdbqt_input
from dockingmt.core.protocol import VinaProtocol
from dockingmt.dock import _resolve_backend, dock
from dockingmt.preparation import PreparedLigand, PreparedReceptor


@smonitor.signal(tags=['api', 'docking', 'batch'])
@arg_digest(config='dockingmt._argdigest')
def _dock_prepared(problem, protocol, backend):
    for role, prepared_type in (
        ('receptor', PreparedReceptor),
        ('partner', PreparedLigand),
    ):
        value = getattr(problem, role)
        if not isinstance(value, prepared_type) and not _is_pdbqt_input(value):
            raise ArgumentError(
                arg_name=f'problem.{role}',
                reason='Batch execution requires already prepared inputs or PDBQT.',
            )
    return dock(problem=problem, protocol=protocol, backend=backend)


@smonitor.signal(tags=['api', 'docking', 'batch'])
@arg_digest(config='dockingmt._argdigest')
def dock_many(problems, protocol=None, backend=None, on_error='raise'):
    """Return an iterator of DockingOutcome records for prepared problems.

    API options are admitted now; items execute serially as the caller advances
    the iterator. Default item errors propagate. Explicit ``on_error='record'``
    yields failure summaries and continues. Source, process-control and memory
    failures always propagate. No future item is consumed before the current
    outcome is yielded, and completed outcomes are not retained.

    Inputs, protocol/backend and source iterator are borrowed. Keep them stable
    while an item executes. Each item uses the same seed rules as ``dock``;
    no seed derivation, global ranking, preparation or affinity-map reuse occurs.
    The caller owns retained outcomes and file access.
    """
    if protocol is None:
        protocol = VinaProtocol()
    resolved = _resolve_backend(protocol, backend)

    def iterate():
        for index, problem in enumerate(problems):
            problem_info = {}
            protocol_info = deepcopy(protocol.to_dict())
            result = None
            error = None
            try:
                if isinstance(problem, DockingProblem):
                    problem_info = deepcopy(problem.to_dict())
                result = _dock_prepared(problem, protocol, resolved)
            except MemoryError:
                raise
            except Exception as exc:
                if on_error == 'raise':
                    raise
                code = getattr(exc, 'code', None)
                error = {
                    'type': f'{type(exc).__module__}.{type(exc).__qualname__}',
                    'message': str(exc),
                    'code': code if isinstance(code, str) and code.strip() else None,
                }
            # Yield outside the exception handler so it retains no traceback.
            yield DockingOutcome(
                index,
                backend=resolved.name,
                problem_info=problem_info,
                protocol_info=protocol_info,
                result=result,
                error=error,
            )

    return iterate()
