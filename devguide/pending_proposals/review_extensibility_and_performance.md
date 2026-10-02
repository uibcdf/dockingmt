---
summary: Review extension boundaries and establish an architecture performance baseline
issue: uibcdf/dockingmt#28
status: partial
opened: 2026-10-02
closed:
verification: measured
area: [architecture, performance, protocols, serialization]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review extensibility and performance

## What

The user reaffirmed that DockingMT must support growth in several scientific
directions while remaining powerful, lightweight, and fast. Review actual
extension boundaries and costs against the existing seed, rather than deriving
the architecture from the first Vina workflow or implementing every horizon.

## How

Read the vision, principles, scientific model/scope/horizons, architecture,
engine strategy, implementation strategy, MVP, roadmap, decisions, validation
strategy, integration contracts, potential evaluation, and open GitHub issues.
Inspect the current problem/protocol/backend/result/preparation boundaries and
measure selected local costs at `181000a4fd63b40d750fd739414fb651f5631fbc`.

This is a review and prioritized proposal, not a replacement of the frozen seed
or acceptance of new public interfaces. Implementation changes remain separate
bounded work, starting with the concrete defects found here.

## Current extension assessment

| Direction | Existing protection | Pressure to resolve at its first real workflow |
| --- | --- | --- |
| Multiple engines and protocol stages | Protocol and backend are separate; callers can supply a backend instance; results have named scores. | `dock` currently dispatches one backend call; the base backend exposes only `dock`. Resolve stages above adapters, with stage-specific capabilities and traceability. |
| Rescoring, refinement, consensus | Poses retain identity and multiple numeric scores; ranking records a score and direction. | Add method/stage, interpretation, unit or dimensionless status, and preferred direction per score. Preserve previous stage outputs and ranking history. Numeric names alone do not establish comparability. |
| TopoMT domains and guided search | Domain, guidance, and constraints are distinct problem fields; Vina has a projection boundary. | Reject unsupported intent now (#26). When a rich domain is supported, distinguish exact projection from approximation, preserve source information, and add its reader. The domain base currently requires box approximation and the problem reader accepts only `BoxRegion`. |
| PharmacophoreMT and ElastNetMT | Scientific contracts are assigned to peers, not copied into DockingMT. | Distinguish annotation, post-filtering, scoring, hard constraints, and sampling guidance. A data field is not proof of supported execution. |
| Ensembles and small screening | Molecular/receptor state identifiers and prepared inputs already exist; run and campaign are conceptually distinct. | Define input ownership, run/pose identity across aggregation, partial failures, bounded memory, and preparation/backend-map reuse before adding campaign behavior. General molecular operations remain in MolSysMT. |
| Local, parallel, Slurm, GPU execution | Accepted backend/executor distinction protects the scientific model. | Keep local execution simple. At a second real mode, resolve CPU/thread resources, work units, cancellation, and failures independently of scientific engine identity. |
| Durable records and independent analysis | Results have schema fields and detached snapshots; optional engines and viewer are not loaded by import. | Enforce schema admission (#27), maintain migration decisions only for actual schema evolution, and retain interpretation without live backend objects. |

Current Vina-specific knobs inside `VinaProtocol` are valid for that concrete
protocol. They must not become required fields of every future protocol. A
second backend should add an adapter and a demonstrated workflow, not force a
rewrite of molecular ownership, scientific result identity, or the viewer.

## Measured baseline (2026-10-02)

Environment: Linux x86_64, Python 3.13.14, NumPy 2.4.6, Vina 1.2.7.
Editable support sources: ArgDigest `0.12.1+7.ga2edfe9`, DepDigest
`0.10.1+15.g78a9106`, PyUnitWizard `0.25.0+7.g00d756c`, SMonitor
`0.13.0+9.g0ec2ef9`, MolSysMT `0.22.4+118.g03b318549.dirty`.
The pre-existing dirty MolSysMT checkout was preserved and not modified.
This is local source evidence, not published-dependency qualification.

### Import measurements

Three fresh Python processes per target, timed around
`importlib.import_module(target)` with `time.perf_counter()`. Linux
`resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024` gives total process
peak RSS in MiB, not incremental memory attributable to that package. OS caches
were not reset. Module counts and loaded-provider flags were inspected through
`sys.modules` after import.

| Import target | Median seconds | Median process peak RSS (MiB) | Loaded modules |
| --- | ---: | ---: | ---: |
| PyUnitWizard | 0.0381 | 20.26 | 167 |
| MolSysMT | 0.4317 | 65.30 | 628 |
| DockingMT | 0.4340 | 65.24 | 656 |

Vina, MolSysViewer, RDKit, and Torch were absent from `sys.modules` after
DockingMT import. MolSysMT is loaded eagerly through the current module graph.
The near-equal import controls do not measure an isolated provider contribution;
in particular, the small RSS difference is noise, not a memory saving claim.

There is no measured need to rewrite the import system immediately. Preserve
optional-provider laziness and measure any proposed deferral of local modules.
Do not remove the MolSysMT ownership/dependency contract to reduce import time.

### Result measurements

Construct poses once using zero-valued `(atoms, 3)` arrays declared in nm,
numeric `metric` scores, and distinct pose IDs. Time `rank_by('metric')` and
`to_dict()` three times each, reporting the median. Import and construction are
excluded; JSON encoding and disk I/O are excluded from export. Metadata is
minimal. No molecular operations or viewer calls are needed.

| Poses | Atoms per pose | Ranking median (s) | Dictionary export median (s) |
| ---: | ---: | ---: | ---: |
| 256 | 32 | 0.0404 | 0.0637 |
| 256 | 1024 | 0.0399 | 1.3793 |
| 1024 | 32 | 0.1307 | 0.2212 |

`numpy.shares_memory` found shared coordinate buffers between source and ranked
poses for all three cases. The suspected ranking coordinate-copy bottleneck was
refuted for this environment. Buffer sharing does require an explicit ownership
decision before concurrent mutable consumers or caches are introduced.

Export traverses pose snapshots and then copies the outer result snapshot;
reconstruction likewise copies the record and individual pose records. This
protects #25's isolation but may add avoidable traversal. The measurements show
export growth, not the fraction attributable to each traversal. Profile before
changing it; preserve independent snapshots and scientific equivalence.

These are synthetic local microbenchmarks, not campaign capacity estimates,
docking speed comparisons, scientific performance claims, or CI time limits.

## Why

The strongest present foundation is separation of scientific responsibilities.
Growth becomes expensive when unsupported intent is accepted, result semantics
are implicit, mutable data is cached without identity/invalidation, or every
optional feature enters the default import and execution path. These are more
immediate architecture risks than the lack of a generic plugin/executor framework.

## Concrete findings

- [#26](https://github.com/uibcdf/dockingmt/issues/26): an actual Vina probe
  accepted nonempty constraints/guidance and returned the unconstrained control's
  coordinates and scores. Source inspection confirms the intent is never consumed.
- [#27](https://github.com/uibcdf/dockingmt/issues/27): an explicit result schema
  `999.0` is accepted and subsequently exported as `1.0`.
- The adapter rebuilds preparation and affinity maps within each execution.
  Prepared objects can already be supplied explicitly. Repeated campaign costs
  have not been measured; do not introduce a global cache from inspection alone.
- The scientific Core MVP remains limited by provisional preparation in
  [#5](https://github.com/uibcdf/dockingmt/issues/5) and unresolved decisions in
  [#4](https://github.com/uibcdf/dockingmt/issues/4) and
  [#17](https://github.com/uibcdf/dockingmt/issues/17). Strong software boundaries
  do not establish scientific qualification or justify skipping the Core gates.

## Proposed next-step order

1. Correct unsupported-intent admission (#26) and scientific-schema admission
   (#27), each with focused guards. Both are DockingMT-only work.
2. Establish repeatable profiling of actual current workflows by phase: import,
   normalization, preparation/projection, affinity maps, native docking, result
   normalization, and export. The current elapsed time covers native docking,
   not the entire workflow. Keep diagnostics optional and overhead measured.
3. Optimize demonstrated local overhead, starting with export if representative
   measurements confirm it, while preserving #25's ownership guarantees.
4. Specify the score/stage, rich-domain, and input-ownership contracts needed by
   the next accepted workflow. Implement only its necessary boundary; record any
   architectural decision explicitly in `DECISIONS.md`.
5. Add explicit rescoring, small collections, and campaign behavior when their
   existing scientific gates are ready. Add generalized executors only when a
   second real execution mode requires them.

Backend-specific reuse would need keys covering submitted input content, search
domain, scoring method, preparation/state choices, relevant provider versions,
and backend settings. Reuse and invalidation must be demonstrated before it is
enabled. A campaign worker must not blindly combine parallel tasks with Vina's
`cpu=0` all-core default and oversubscribe the host.

## What was refuted

More abstract classes, plugins, schedulers, or dependencies do not establish
extensibility. No coordinate-copy bottleneck or heavy optional-provider import
was demonstrated. A native-language rewrite is not justified by these data.
Silently dropping constraints or weakening snapshot independence is not a
performance optimization. More computation alone does not establish better
scientific recovery.

## Scope and exclusions

This review changes documentation and issue tracking, not runtime APIs or
scientific behavior. It requires no sibling modifications or coordination.
The existing roadmap and accepted decisions remain authoritative. Cross-component
integration changes still belong to their scientific owners and shared suite
contracts. No portable runtime/memory budget is claimed until a representative
environment and workload are chosen.

## Acceptance criteria

- Review growth directions against implementation, with concrete pressure points.
- Retain the measurement method, environment, bounds, and refuted performance claims.
- Track reproducible defects separately with their scientific impact and guards.
- Agree the bounded next implementation order and appropriate measurement workloads.
- Preserve molecular ownership, optional dependencies, and all Core scientific gates.
