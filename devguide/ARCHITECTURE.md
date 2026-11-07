# Architecture

This document distinguishes the existing implementation from the richer
scientific design. Use [development setup](DEVELOPMENT.md) to work in the code
and [the full requirement/evidence plan](PRE_STABILIZATION_PLAN.md) to assess
acceptance. A source module or conceptual diagram does not establish a completed
Core/Extended gate.

## Current source map

The following paths are implemented entry points, reviewed for the
[2026-11-06 handoff](MACHINE_HANDOFF.md). Public exports in
[`dockingmt/__init__.py`](../dockingmt/__init__.py) and the actual source remain
authoritative when this navigation map changes.

| Area | Current source | Responsibility |
| --- | --- | --- |
| Scientific declarations and records | [`core/problem.py`](../dockingmt/core/problem.py), [`protocol.py`](../dockingmt/core/protocol.py), [`search_domain.py`](../dockingmt/core/search_domain.py), [`results.py`](../dockingmt/core/results.py), [`outcome.py`](../dockingmt/core/outcome.py) | Problems, resolved Vina protocol, physical search domains, poses/results and per-item batch outcomes. |
| Record admission and provenance | [`core/audit.py`](../dockingmt/core/audit.py), [`pose_audit.py`](../dockingmt/core/pose_audit.py), [`_scores.py`](../dockingmt/core/_scores.py), [`_private/artifacts.py`](../dockingmt/_private/artifacts.py) | Internal consistency, named score/ranking evidence and captured backend-input identity. These do not certify chemistry or reconstruct missing molecular sources. |
| Public orchestration | [`dock.py`](../dockingmt/dock.py), [`score.py`](../dockingmt/score.py), [`batch.py`](../dockingmt/batch.py), [`evaluation.py`](../dockingmt/evaluation.py), [`aggregation.py`](../dockingmt/aggregation.py) | Docking/fixed scoring, serial prepared-problem execution and explicitly delimited reference-recovery evaluation/aggregation. |
| Existing interaction association | [`interactions.py`](../dockingmt/interactions.py) | `bind_interactions`/`PoseInteractions` bind one explicitly selected pose to an admitted one-frame carrier. Source controls and [bounded installed normal/pm-fs receiving](validation/e4_pose_binding_installed_2026-11-07.md) pass, preserving full original results/provider analyses and full-carrier persistence. [Empty-source native unevaluated coverage](validation/e4_native_unevaluated_2026-11-07.md) also passes. Positive-source persistence awaits [client receiving of the published #642 source fix](validation/e4_evidence_catalog_fix_2026-11-07.md); exact native construction is held after an owned-memory stop. The [view route](validation/pose_interaction_view.md) has separate source/DOM controls and [passing exact-candidate receiving](validation/e4_pose_interaction_view_installed_2026-11-07.md): eight real-provider View/native cells normal/pm-fs plus independent record checks. Actual canvas/public delivery remain unproven. |
| Docking preparation | [`preparation/`](../dockingmt/preparation/) | Docking intent, named preparation choices, assessments, provider orchestration and source/prepared/backend maps. General molecular operations belong to MolSysMT; remaining migration boundaries stay in #49. |
| Backend adapter | [`engines/base.py`](../dockingmt/engines/base.py), [`vina.py`](../dockingmt/engines/vina.py), [`_vina_scoring.py`](../dockingmt/engines/_vina_scoring.py) | Capability negotiation, native Vina execution and interpretation of backend outputs. |
| Viewer entry and addon | [`view.py`](../dockingmt/view.py), [`molsysviewer_dockingmt/`](../molsysviewer_dockingmt/), [`viewer/__init__.py`](../dockingmt/viewer/__init__.py) | Public view entry, DockingMT-owned runtime/panels/adapters and compatibility exports. [`adapters/interactions.py`](../molsysviewer_dockingmt/adapters/interactions.py) displays an admitted one-frame binding with full result preservation and explicit pose/frame mapping. MolSysViewer owns generic host/rendering behavior. |
| Shared support integration | [`_argdigest.py`](../dockingmt/_argdigest.py), [`_depdigest.py`](../dockingmt/_depdigest.py), [`_smonitor.py`](../dockingmt/_smonitor.py), [`_pyunitwizard.py`](../dockingmt/_pyunitwizard.py), [`_private/`](../dockingmt/_private/) | Owned argument contracts, dependency declarations, structured diagnostics and quantity policy. Follow the synchronized root tool guides. |
| User-facing example | [`examples/inspect_saved_scoring.py`](../examples/inspect_saved_scoring.py) | Explicit saved-pose/result inspection; it is not a molecular recovery tool or a new scoring study. |
| Tests and qualification tools | [`tests/`](../tests/), [`devtools/`](../devtools/), [`dmt_test_support/`](../dmt_test_support/) | Software guards, administrative controls and unshipped scientific helpers. The exact installed helper/data selection is declared in `devtools/conda-build/resources.toml`. |
| Engineering and scientific evidence | [`.github/workflows/`](../.github/workflows/), [`devguide/`](README.md) | Source/installed/administrative gates, accepted design, owning work records and original scientific receipts. |

There are no standalone public `DockingRun`, `DockingCampaign`, general executor
or stage-plugin implementations implied by this map. Current run information is
recorded through problem/protocol/result provenance and `DockingOutcome`.
`dock_many` is incremental serial execution, not a campaign framework. Existing
score/evaluation APIs and the bounded provider-backed interaction notebook are
pieces of Extended workflows, not whole-E1–E5 acceptance.

## Architectural objective

The original design objective is a backend-independent scientific core surrounded
by adapters. The following diagrams describe that scientific model, including
concepts that remain `DESIGNED FOR` or `HORIZON`; they are not the current class
or import graph.

```text
                    DockingProblem
                         |
        +----------------+----------------+
        |                |                |
  Molecular states   Search domain   Constraints /
                                    Search guidance
        |                |                |
        +----------------+----------------+
                         |
                  DockingProtocol
                         |
       +---------+-------+-------+---------+
       |         |       |       |         |
 Preparation  Sampling Scoring Refinement Ranking
       |         |       |       |         |
       +---------+-------+-------+---------+
                         |
                    Backend(s)
                         |
                    DockingRun
                         |
                   DockingResult
                         |
                       Poses
```

Above individual runs:

```text
DockingCampaign
      |
      +-- Run/Result
      +-- Run/Result
      +-- Run/Result
      |
      +-- aggregate analysis
```

## Original proposed package boundaries

This original conceptual layout is retained to explain separation of concerns.
It differs from the implemented tree above; it does not authorize creating the
absent packages:

```text
dockingmt/
├── core/          # scientific concepts and stable data model
├── protocols/     # canonical/composed workflows
├── preparation/   # docking intent/orchestration over provider tools
├── regions/       # search-domain representations/conversions
├── guidance/      # future search-guidance abstractions
├── constraints/   # future constraint abstractions
├── scoring/       # scoring/rescoring abstractions
├── engines/       # docking-engine/backend adapters
├── analysis/      # docking associations/interpretation of provider analyses
├── campaigns/     # higher-level execution/aggregation when needed
├── integrations/  # optional MolSysSuite bridges
└── io/            # serialization/interchange
```

Do not create empty architecture for speculative completeness. Add modules when responsibilities become real.

## Protocol composition

A protocol must not require one monolithic engine in the scientific model.
The following multi-provider composition is a design direction; the current
Vina protocol/adapter does not implement a generic stage-resolution framework:

```text
Preparation provider
      ↓
Sampling backend A
      ↓
Refinement backend B
      ↓
Scoring backend C
      ↓
Ranking policy
```

The MVP may use Vina for several stages, but the public model must not encode this as a permanent 1:1 relationship.

## Capability-driven backends

The current `DockingBackend`/`VinaBackend` contracts advertise and validate actual
adapter capabilities. Inspect their `capabilities` and the protocol's
`required_capabilities` rather than assuming every upstream Vina feature is
exposed. The following vocabulary is illustrative design space, not the
current adapter's capability set:

```text
small_molecule
macrocycle
peptide
rigid_receptor
flexible_sidechains
global_search
multiple_ligands
custom_scoring
rescoring
gpu
constraints
water_aware
metal_aware
covalent
```

Protocols should validate requested capabilities before execution.

## Adapters

```text
DockingMT scientific model
          ↓
backend-specific model/files/parameters
          ↓
execution
          ↓
backend output
          ↓
DockingMT result model
```

Lossy conversions must be explicit. Example:

```text
TopoMT-rich pocket
      ↓
BoxRegion approximation
      ↓
Vina search box
```

The original rich pocket information should remain attached to provenance/context rather than being discarded.

## Preparation boundary

Backend file generation is not equivalent to scientific preparation.

Keep separable:

```text
molecular preparation
        ↓
prepared molecular state
        ↓
backend conversion
        ↓
backend input
```

This permits future alternative preparation methods without redefining docking.

General molecular inspection, chemical-state/identity work, repair, hydrogen
handling, coordinate transformations and molecular format serialization must
use MolSysMT's supported operations. Missing reusable capabilities are requested
in MolSysMT, not filled by a DockingMT molecular helper. Other specialized
capabilities retain TopoMT, PharmacophoreMT and ElastNetMT ownership. DockingMT
owns the docking-specific policy, association and interpretation around them.

## Provenance

The conceptual `DockingRun` should eventually capture at least the fields below.
Today inspect the actual problem/protocol/result declarations and provenance;
do not infer that a standalone run object or every listed field is implemented:

- DockingMT version;
- backend(s) and versions;
- protocol and resolved parameters;
- preparation methods and versions;
- molecular-state identities;
- random seed(s);
- receptor/partner identity;
- search-domain definition and conversions;
- constraints/guidance and approximations;
- unit conversions;
- execution metadata relevant to reproducibility.

## Identity preservation

Backend conversion must preserve a mapping between source atoms/entities and backend atoms/entities wherever possible. If an engine changes ordering, typing or representation, DockingMT should retain the mapping required to reconstruct scientifically meaningful results.

## Physical-quantity infrastructure

The core follows the current MolSysSuite PyUnitWizard contract. DockingMT does not own a
separate unit subsystem.

Adapters own conversion to/from backend-native numerical conventions.

Scores must carry semantic metadata sufficient to distinguish:

- physical quantities with units;
- empirical scores expressed conventionally in energy-like units;
- dimensionless model scores;
- ranks/probabilities/confidences.

## Shared MolSysSuite infrastructure

DockingMT should inherit the suite infrastructure contracts:

```text
physical quantities       -> PyUnitWizard
public argument boundary  -> ArgDigest
optional dependencies     -> DepDigest
structured diagnostics    -> SMonitor
molecular-system model    -> MolSysMT
visualization host        -> MolSysViewer
```

These are architectural responsibilities, not convenience libraries.

## Optional dependencies

The core should remain importable without every docking engine or optional chemistry
provider installed. Optional provider availability and lazy loading should use DepDigest
rather than ad hoc import guards.

Missing providers and capability failures should surface through actionable,
catalog-driven SMonitor diagnostics.

## Native high-performance code

No implementation language is prescribed. Rust, C++, CUDA or other approaches should be selected only when a concrete algorithmic or performance requirement exists.

A native engine must implement DockingMT contracts rather than redefine them.

## Scientific defaults

Defaults with scientific consequences belong to the resolved protocol/run, not hidden
implementation constants.

Examples include search padding, exhaustiveness, pose count, seed policy and preparation
choices. They must be inspectable and version-aware.


## Execution model

Backend and execution environment are orthogonal:

```text
DockingProtocol
      |
      v
Backend / Engine
      |
      v
Execution request
      |
      v
Executor
      |
      v
DockingRun
```

The backend answers **what scientific implementation performs the operation**.
The executor answers **where and how the resolved operation is executed**.

Possible future executors include local serial execution, local multiprocessing,
Slurm/HPC submission, GPU-node execution and distributed campaign execution.

The Core MVP does not need a generalized executor framework. A local execution path
may remain implicit until a second real execution environment creates a concrete need
for the abstraction.


## Serialization boundary

Serialization belongs to the scientific-object boundary, not to backend artifacts.
Backend files such as PDBQT may be retained for provenance/debugging, but they are not
the canonical persistent representation of a `DockingResult`.

Stable scientific objects should use versioned schemas so saved results can be read,
inspected and migrated independently of the backend process that produced them.

DockingMT's own record admission and backend-artifact hashes remain separate from
molecular persistence and authentication. MolSysMT owns molecular codecs and
typed interaction persistence. A detached `DockingResult` or captured PDBQT file
does not by itself restore a complete molecular state. Preserve source/index
maps and explicit missing evidence rather than inventing a local codec or
reconstruction route.
