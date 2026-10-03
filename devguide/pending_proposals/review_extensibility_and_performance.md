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

## 2026-10-03 chemical-coverage summary cost

The [chemical readiness consumer record](../validation/chemical_readiness_consumption.md)
and its raw preparation profile compare prior evidence collection at `559f7c3`
with the compact MolSysMT coverage summary. Five paired warm-cache samples per
profile and role alternate execution order. The source/selection and remaining
preparation code are shared. Metadata adds roughly 3.6–3.7 kB for the selected 181L
ligand/protein, avoiding duplicated per-atom/bond value arrays. Small uncontrolled
samples do not establish a universal timing bound; retain their variability and
do not infer speed from footprint. No new benchmark framework or campaign cache
is introduced for this slice.

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

## Admission-block progress (2026-10-02)

The first proposed implementation block is complete locally: unsupported Vina
intent and scientific-schema admission now have focused guards. Resolved records
are archived in
[`vina_ignores_constraints_and_search_guidance.md`](../archive/vina_ignores_constraints_and_search_guidance.md)
and
[`scientific_record_readers_ignore_schema_versions.md`](../archive/scientific_record_readers_ignore_schema_versions.md).
The five existing readers share the explicit/legacy version policy recorded in
DMT-030; no generic framework or sibling changes were introduced.

Full local validation passed all 344 tests in 48.96 seconds with unchanged provider
warnings and passing quality gates. This review remains partial: phase profiling,
representative performance workloads, and the next accepted extension contract
still require their bounded follow-up. The initial measurements and current-state
table above describe the inspected baseline, not a claim that all future boundaries
are now implemented.

## Phase-profiling progress (2026-10-02)

The second proposed implementation block now has a bounded implementation:
`VinaProtocol(collect_timings=True)` retains ten consecutive adapter phases,
their total, a monotonic clock and an explicit second unit in successful result
provenance. The default path allocates no recorder and makes no additional clock
reads. Native `elapsed_seconds` keeps its scope and now uses the monotonic clock.
Cleanup and native exception behavior are protected; no sibling code is changed.

`devtools/profile_workflow.py` measures fresh-process import, input normalization,
public docking, dictionary export, encoding and writing separately. It compares
paired enabled/disabled outputs, input identities and execution contexts. The
[measurement record](../validation/workflow_profiling.md) retains phase definitions,
environment/source identity, methods, medians, raw docking times and limits.

Three enabled/disabled pairs per route preserve identical scientific snapshots
within each route. Molecular 181L input normalization has a 5.498 s enabled
median; the captured-PDBQT route has 0.0109 s. Adapter maps take about 0.65 s,
native docking 0.32 s and automatic preparation 0.274 s. Small-result export
takes 0.00145 s / 0.000366 s respectively. Negative enabled-minus-disabled median
differences are noisy observations, not a demonstrated speedup or overhead bound.
The environment's PyUnitWizard and SMonitor generations changed since the initial
baseline; these data do not establish a cross-version performance comparison.

Remaining work includes larger representative result export and measured local
optimization, followed by the next accepted extension's concrete contract. The
existing large synthetic export evidence remains relevant; current small-result
measurements do not refute it. No global cache, generalized executor, scientific
qualification claim or portable timing gate has been introduced.

Final local validation passes all 354 tests in 51.06 seconds with the same 12
provider warnings, Ruff lint/format, current report indexes and a clean diff check.
`tests/test_workflow_profiling.py` guards deterministic attribution, the disabled
path, cleanup, captured input integrity and preserved unsupported intent.
`tests/test_engines.py::test_vina_backend_docking_execution` compares actual Vina
and Vinardo outputs in both modes and round-trips the timing provenance. The final
paired captured-input CLI smoke also passes all three equality checks. This issue
remains partial for the remaining optimization and extension-contract work above.

## Retained notebook and raw evidence (2026-10-02)

The phase-profiling baseline now also has an executed
[Jupyter notebook](../validation/workflow_profiling.ipynb) and two unchanged
[raw reports in Git](../validation/data/workflow_profiling/), preserving the twelve
samples previously kept only in `/tmp`. The notebook reuses the existing report
summarizer, checks output/input/context equality and renders separate workflow and
adapter tables/plots. Native measurements are explicitly opt-in through the
existing command; default execution reads retained evidence without importing
DockingMT or Vina. Notebook tools do not become package runtime dependencies.
All seven code cells execute successfully, the notebook schema validates, and
the retained report bytes match the original files. Local gates pass with 354
tests in 54.70 seconds and the same 12 provider warnings.

## Result-export optimization progress (2026-10-02)

The third follow-up block confirms redundant deep-copy traversals as a local
serialization cost and removes them. A pose's freshly allocated coordinate lists
no longer need another copy; independently owned pose snapshots no longer need
another complete result traversal. Custom serializers retain the existing
defensive copy. Structured pose metadata and result context still receive independent
copies. Schema, scientific content, score validation,
units, serializer dispatch and reconstruction are preserved.

The new `devtools/benchmark_result_export.py` measures five deterministic cases
and optional existing result manifests, with separate timing, allocation and
profile calls. The [measurement record](../validation/result_export.md),
[executed notebook](../validation/result_export.ipynb) and
[raw before/after reports](../validation/data/result_export/) retain this evidence.
All six case JSON digests match before/after. On the measured environment, 256
poses × 1024 atoms export in 0.0860 s versus 1.4536 s; with full maps, 1.1833 s
versus 4.4220 s. Peak traced Python allocations fall from 87.19 to 40.32 MiB and
208.16 to 90.66 MiB respectively. These are export-only measurements, not docking
speedups, total RSS, campaign capacity or portable thresholds.

Independence guards include repeated snapshots/pose entries, NumPy/tuple/set
metadata, custom serializer extensions and non-default quantity policy. The
benchmark comparison rejects mismatched units/clock/method, environment, repeats,
case selection and payload hashes. No molecular operation, cache, native engine
change or sibling coordination is involved. The review remains partial for the
next accepted extension's concrete contract and scientifically qualified workloads.

Final local gates pass with 368 tests in 45.74 seconds and the same 12 provider
warnings. Ruff lint/format, report-index and diff checks pass. The five-cell
comparison notebook executes successfully and reads reports without scientific
imports. Its retained raw reports match the sampled originals byte for byte.

## Score/ranking contract progress (2026-10-03)

The next accepted local extension boundary is complete in
[#31](https://github.com/uibcdf/dockingmt/issues/31): validated optional score
descriptors, actual Vina/Vinardo empirical meaning and comparison context, and
independent scalar evidence for successive rankings. Legacy records remain
readable and explicitly rankable; mixed/incompatible declared meanings are
rejected. Explicit direction, stable ties, original values and state/pose identity
are retained. The adapter also records its initial native order.

The [contract](../validation/score_semantics.md) and
[executed offline notebook](../validation/ranking_history.ipynb) document the
behavior without molecular operations or optional engine/viewer imports. Their
saved fixture is synthetic software evidence. No scoring engine, physical-energy
API, generic protocol-stage infrastructure, campaign, cache or sibling change is
introduced. This review remains partial for scientifically qualified workloads
and the concrete comparison/identity policies of later accepted extensions.

## Fixed-pose scoring progress (2026-10-03)

[Issue #34](https://github.com/uibcdf/dockingmt/issues/34) adds the first concrete
independent scoring operation. `score` evaluates already prepared Vina/Vinardo
conformations, and `DockingPose.with_scores` preserves separate named outputs.
The optional backend method leaves docking-only adapters compatible. Prior pose
geometry and known state identifiers are checked; submitted bytes, eight native
components, empirical meaning and detached evaluation history are retained.
The [contract](../validation/fixed_pose_scoring.md) and executed notebook bound
this software evidence. No provider code, Meeko dependency, stage executor,
campaign or scientific parameterization claim is introduced. This architecture
review remains partial for representative scientific workloads and subsequent
accepted extension/comparison contracts.

## Offline pose audit and incremental execution progress (2026-10-03)

[Issue #35](https://github.com/uibcdf/dockingmt/issues/35) adds bounded public
`audit_pose(record)` for standalone fixed-pose evaluation history, sharing
existing result/descriptor/unit/input checks. Its
[contract](../validation/pose_audit.md) explicitly excludes molecular geometry
replay and scientific qualification.

[Issue #36](https://github.com/uibcdf/dockingmt/issues/36) adds lazy serial
`dock_many(...)` for already prepared problems, reusing public `dock`.
Independent `DockingOutcome` records preserve declarations, resolved adapter,
input position and success/failure evidence. The
[contract](../validation/incremental_docking.md) and executed notebook retain
native equivalence, explicit failure handling and bounded orchestration ownership.
All 684 tests pass in 128.69 s with the existing 27 provider warnings; required
local gates pass. No sibling implementation or new performance claim is involved.
This review remains partial for aggregation/comparison contracts, representative
scientific workloads and future accepted integration boundaries.

## Explicit redocking evaluation progress (2026-10-03)

[Issue #38](https://github.com/uibcdf/dockingmt/issues/38) adds public
`evaluate_redocking`, reusing the existing RMSD/MolSysMT boundary and preserving
explicit cutoff, correspondence, result-order top-N interpretation and detached
comparison evidence. The [contract](../validation/redocking_evaluation.md) and
executed notebook retain provisional 181L and unassessed external 1IEP controls,
with a displaced-domain negative methodological control. MolSysMT #310 owns
future chemical symmetry correspondence. All 750 tests pass without skips;
the independent full host closure limitation is retained and reported to
MolSysSuite #82. No dataset success rate, chemistry qualification, new molecular
algorithm, campaign or performance guarantee follows. This review stays partial.

## What was refuted

More abstract classes, plugins, schedulers, or dependencies do not establish
extensibility. No coordinate-copy bottleneck or heavy optional-provider import
was demonstrated. A native-language rewrite is not justified by these data.
Silently dropping constraints or weakening snapshot independence is not a
performance optimization. More computation alone does not establish better
scientific recovery.

## Scope and exclusions

The initial review changed documentation and issue tracking. Its accepted follow-up
now adds optional Vina timing provenance and a bounded developer measurement tool;
scientific execution choices and results are preserved. It requires no sibling
modifications or coordination.
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

## 2026-10-03 exact residue-comparison cost

The [receptor coverage record](../validation/receptor_coverage_consumption.md)
and its executed notebook retain five paired warm-template rounds with alternating
profile order. Complete 181L preparation measures 168.15 ms for stored fields
versus 365.58 ms including residue comparison, with 4,006 additional JSON bytes.
Original 1IEP source assessment alone measures 33.73 versus 390.98 ms, adding
4,183 bytes; unmodified preparation remains unsupported. Those different operations
must not be directly compared. 181L PDBQT bytes and stored-field evidence are
identical between profiles. The cost remains visible as a provider measurement
point; no local molecular audit or campaign cache is added. These small local
samples do not establish universal time or peak-memory guarantees. Provider #218
receives the consumer evidence, and this performance issue remains partial.
