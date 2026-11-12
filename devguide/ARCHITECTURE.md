# Architecture

This document distinguishes the existing implementation from the richer
scientific design. Use [development setup](DEVELOPMENT.md) to work in the code
and [the full requirement/evidence plan](PRE_STABILIZATION_PLAN.md) to assess
acceptance. A source module or conceptual diagram does not establish a completed
Core/Extended gate.

## Domain operations and compatibility

BindingMT owns molecular docking, fixed-identity complex prediction, complex
refinement, binding free-energy calculation and prediction, and binding-interface
characterization. [Scientific scope](SCIENTIFIC_SCOPE.md) distinguishes these
promises and their current implementation states. The class names below remain
docking-specific; this transition creates no universal request/result classes
or implementations of future operations.

Operation-specific inputs/results share molecular identities/maps, quantities,
resolved protocol/provider choices, actual artifacts and explicit failures.
Predictions may accept coordinate-free identities and move all partners.
Free-energy methods need defined states, thermodynamic conventions, conditions
and uncertainty/convergence evidence. Predictions and interface descriptors keep
their own endpoints/applicability. A technical receipt does not erase these
scientific differences.

Canonical source is `bindingmt` and `molsysviewer_bindingmt`; the addon/workspace
identity and development namespace follow the same early-development clean cut.
See [the identity/scope decision](archive/rename_bindingmt.md). New
integrations remain reviewed independently under #109/#110. Generic chemistry,
numerical methods, recording and scheduling keep their suite/platform owners.

## Binding-site contract study (draft)

[#111](pending_proposals/binding_site_public_contract.md) is a maintainer-requested
[revision-2 design review](binding_site_design.md) before implementation. It proposes
a declaration independent of SearchDomain, with structural scope, per-structure
realizations and ensemble associations. Ordinary coordinates remain MolSys-owned;
direct region/domain applications keep context checks, scientific evidence and
effective inputs explicit. Proposed classes, schema and integration behavior are absent
from the current source map; sibling review/adoption and implementation remain
separate steps.

The [contribution audit and receiving sketches](binding_site_review.md) make
the proposed source/view/claim references, native consumer associations and
effective-input boundaries concrete. Its synthetic JSON specimens are design
material, not runtime schema/adapter qualification or new installed resources.
The [implementation/work plan](binding_site_implementation_plan.md) records the
authorized next increments and their admission/receiving dependencies. It is
planning evidence; the source map below still contains no BindingSite runtime.

## Binding-interface characterization study (draft)

[#112](pending_proposals/binding_interface_public_contract.md) has a
[second detailed design](binding_interface_design.md) for a binding-domain result
composing owner associations/observations, site hypotheses and application
receipts. It distinguishes participants/grouping, exact contexts and immutable
evidence without a second molecular or topographic registry. Revision 2 makes
analysis-level outcomes, public assurance/fact checks, the saved PISA footprint
and effective grouped native projections explicit. Its symbolic records and API
sketches are review proposals. No BindingInterface runtime,
shared schema freeze or consumer receiving is implemented by this document.
The useful #111 core remains independent unless a concrete incompatibility arises.

The [implementation/work plan](binding_interface_implementation_plan.md) evaluates
the favorable second-round responses and records the first data/analysis core,
explicit optional PISA intake, qualified contact footprints and independent
native/consumer receiving. Proposed local contracts, owner facts and real
executed evidence remain separate; the source map still has no runtime
BindingInterface implementation from this planning increment.
Work-plan revision 2 additionally requires the derived footprint's own persistence,
historical versus current-use checks, nonempty-overlap aggregation coverage and
canonical source membership with aligned local maps. These are acceptance
requirements, with runtime qualification still pending.

## Current source map

The following paths are implemented entry points, reviewed for the
[2026-11-06 handoff](MACHINE_HANDOFF.md). Public exports in
[`bindingmt/__init__.py`](../bindingmt/__init__.py) and the actual source remain
authoritative when this navigation map changes.

| Area | Current source | Responsibility |
| --- | --- | --- |
| Scientific declarations and records | [`core/problem.py`](../bindingmt/core/problem.py), [`protocol.py`](../bindingmt/core/protocol.py), [`search_domain.py`](../bindingmt/core/search_domain.py), [`results.py`](../bindingmt/core/results.py), [`outcome.py`](../bindingmt/core/outcome.py) | Problems, resolved Vina protocol, physical search domains, poses/results and per-item batch outcomes. |
| Record admission and provenance | [`core/audit.py`](../bindingmt/core/audit.py), [`pose_audit.py`](../bindingmt/core/pose_audit.py), [`_scores.py`](../bindingmt/core/_scores.py), [`_private/artifacts.py`](../bindingmt/_private/artifacts.py) | Internal consistency, named score/ranking evidence and captured backend-input identity. These do not certify chemistry or reconstruct missing molecular sources. |
| Public orchestration | [`dock.py`](../bindingmt/dock.py), [`score.py`](../bindingmt/score.py), [`batch.py`](../bindingmt/batch.py), [`evaluation.py`](../bindingmt/evaluation.py), [`aggregation.py`](../bindingmt/aggregation.py) | Docking/fixed scoring, serial prepared-problem execution and explicitly delimited reference-recovery evaluation/aggregation. |
| Existing interaction association | [`interactions.py`](../bindingmt/interactions.py) | `bind_interactions`/`PoseInteractions` bind one explicitly selected pose to an admitted one-frame carrier. Source controls and [bounded installed normal/pm-fs receiving](validation/e4_pose_binding_installed_2026-11-07.md) pass, preserving full original results/provider analyses and full-carrier persistence. [Empty-source native unevaluated coverage](validation/e4_native_unevaluated_2026-11-07.md) also passes. Positive-source persistence awaits [client receiving of the published #642 source fix](validation/e4_evidence_catalog_fix_2026-11-07.md); exact native construction is held after an owned-memory stop. The [view route](validation/pose_interaction_view.md) has separate source/DOM controls and [passing exact-candidate receiving](validation/e4_pose_interaction_view_installed_2026-11-07.md): eight real-provider View/native cells normal/pm-fs plus independent record checks. Actual canvas/public delivery remain unproven. |
| Docking preparation | [`preparation/`](../bindingmt/preparation/) | Docking intent, named preparation choices, assessments, provider orchestration and source/prepared/backend maps. General molecular operations belong to MolSysMT; remaining migration boundaries stay in #49. |
| Backend adapter | [`engines/base.py`](../bindingmt/engines/base.py), [`vina.py`](../bindingmt/engines/vina.py), [`_vina_scoring.py`](../bindingmt/engines/_vina_scoring.py) | Capability negotiation, native Vina execution and interpretation of backend outputs. |
| Viewer entry and addon | [`view.py`](../bindingmt/view.py), [`molsysviewer_bindingmt/`](../molsysviewer_bindingmt/), [`viewer/__init__.py`](../bindingmt/viewer/__init__.py) | Public view entry, BindingMT-owned runtime/panels/adapters and compatibility exports. [`adapters/interactions.py`](../molsysviewer_bindingmt/adapters/interactions.py) displays an admitted one-frame binding with full result preservation and explicit pose/frame mapping. MolSysViewer owns generic host/rendering behavior. |
| Shared support integration | [`_argdigest.py`](../bindingmt/_argdigest.py), [`_depdigest.py`](../bindingmt/_depdigest.py), [`_smonitor.py`](../bindingmt/_smonitor.py), [`_pyunitwizard.py`](../bindingmt/_pyunitwizard.py), [`_private/`](../bindingmt/_private/) | Owned argument contracts, dependency declarations, structured diagnostics and quantity policy. Follow the synchronized root tool guides. |
| User-facing example | [`examples/inspect_saved_scoring.py`](../examples/inspect_saved_scoring.py) | Explicit saved-pose/result inspection; it is not a molecular recovery tool or a new scoring study. |
| Tests and qualification tools | [`tests/`](../tests/), [`devtools/`](../devtools/), [`bmt_test_support/`](../bmt_test_support/) | Software guards, administrative controls and unshipped scientific helpers. The exact installed helper/data selection is declared in `devtools/conda-build/resources.toml`. |
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
bindingmt/
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
BindingMT scientific model
          ↓
backend-specific model/files/parameters
          ↓
execution
          ↓
backend output
          ↓
BindingMT result model
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
in MolSysMT, not filled by a BindingMT molecular helper. Other specialized
capabilities retain TopoMT, PharmacophoreMT and ElastNetMT ownership. BindingMT
owns the docking-specific policy, association and interpretation around them.

## Provenance

The conceptual `DockingRun` should eventually capture at least the fields below.
Today inspect the actual problem/protocol/result declarations and provenance;
do not infer that a standalone run object or every listed field is implemented:

- BindingMT version;
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

Backend conversion must preserve a mapping between source atoms/entities and backend atoms/entities wherever possible. If an engine changes ordering, typing or representation, BindingMT should retain the mapping required to reconstruct scientifically meaningful results.

## Physical-quantity infrastructure

The core follows the current MolSysSuite PyUnitWizard contract. BindingMT does not own a
separate unit subsystem.

Adapters own conversion to/from backend-native numerical conventions.

Scores must carry semantic metadata sufficient to distinguish:

- physical quantities with units;
- empirical scores expressed conventionally in energy-like units;
- dimensionless model scores;
- ranks/probabilities/confidences.

## Shared MolSysSuite infrastructure

BindingMT should inherit the suite infrastructure contracts:

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

A native engine must implement BindingMT contracts rather than redefine them.

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

BindingMT's own record admission and backend-artifact hashes remain separate from
molecular persistence and authentication. MolSysMT owns molecular codecs and
typed interaction persistence. A detached `DockingResult` or captured PDBQT file
does not by itself restore a complete molecular state. Preserve source/index
maps and explicit missing evidence rather than inventing a local codec or
reconstruction route.
