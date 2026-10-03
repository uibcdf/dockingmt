from __future__ import annotations

import smonitor
from argdigest import arg_digest

from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol, VinaProtocol
from dockingmt.core.results import DockingPose
from dockingmt.dock import _resolve_backend
from dockingmt.engines.base import DockingBackend


@smonitor.signal(tags=['api', 'scoring'])
@arg_digest(config='dockingmt._argdigest')
def score(
    problem: DockingProblem,
    protocol: DockingProtocol | None = None,
    backend: DockingBackend | str | None = None,
    pose: DockingPose | None = None,
    score_name: str = 'score',
) -> DockingPose:
    """Evaluate one prepared conformation without search or optimization.

    The Vina adapter accepts prepared receptor/ligand objects or PDBQT inputs
    and returns eight named empirical components. An optional existing pose
    must match the submitted ligand geometry and known state identifiers.
    Prior scores, identity and rank are preserved in a detached copy. Use a
    new ``score_name`` for each evaluation to avoid overwriting prior values.

    VinaProtocol's search-only parameters do not apply and are recorded as
    unused. The supplied search box defines the affinity-map domain.
    """
    if protocol is None:
        protocol = VinaProtocol()
    return _resolve_backend(protocol, backend).score(
        problem=problem, protocol=protocol, pose=pose, score_name=score_name
    )
