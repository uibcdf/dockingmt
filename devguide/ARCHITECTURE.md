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

## Binding-interface characterization

[#112](pending_proposals/binding_interface_public_contract.md) now has both the
[first data profile](binding_interface_data_core.md) and the
[native Cartesian contact profile](binding_interface_contacts.md). `contacts.py`
uses public MolSysMT tools for all molecular selection/inspection/map validation
and contact/distance computation. BindingMT owns the binding question, selected
profile, contextual result/attribution and atomic-to-group witness aggregation.
No generic molecular representation, parser, matcher or geometry kernel is copied.

`BindingInterface` preserves declared evidence and typed native calculation.
`ContactFootprint` independently preserves source-ordered members/aligned local
maps and all contributors. Both share private offline I/O, immutable copy/read
identity and experimental admission; contacts use 0.2, surfaces use 0.3 while declarations
retain 0.1. Known physical fields use PyUnitWizard sealed records. Saved checks
remain historical and a revised interpretation preserves original calculation scope.

The [second scientific design](binding_interface_design.md),
[work-plan revision 4](binding_interface_implementation_plan.md) and
[collaborator dispositions/readiness](binding_interface_plan_review.md) retain
typed-provider and consumer obligations. The [N2 contract](binding_interface_burial.md)
now binds `burial.py` to public MolSysMT extraction/comparison/radii/SASA. It owns
no molecular kernel; experimental 0.3 retains typed signed contributions and
separate numerical usability. Shared `interface_context` performs only binding
admission/delegated queries and original-axis metadata for contacts and surfaces.
Full chemical correspondence, PISA/H and #111 keep separate gates.
TopoMT #198 regional enrichment remains optional. Source receiving is distinct
from installed/public/native-build qualification and cross-owner adoption.

The [native ionic integration](binding_interface_native_interactions.md) delegates
strict grouped observation views and whole-charge-center checks to MolSysMT, and
observed-participant hypotheses to optional PharmacophoreMT. `chemical_interfaces.py`
composes their scientific outputs and qualified site/contributor references;
`interface_ionic.py` validates only the portable binding view, not a new molecular
codec. Complete observations stay in the full MolSys and H5MSM. Experimental
ionic 0.5 saves explicit analysis order; original 0.4 stays readable. Reading
is independent of native recovery and optional scientific imports. PISA is now
explicitly deferred interoperability, not the next automatic native increment.

The [H-R2 annotation profile](binding_interface_characterization_annotation.md)
composes existing complete core records in an optional BindingMT namespace.
`interface_annotations.py` validates identity axes/criterion/contributor references
offline and delegates current molecular checks through existing public MolSysMT
admission. `with_characterizations` creates a new record and accesses no native
query object/file; observed construction and caller-declared curated references
retain separate authority. Query semantics and original native assets stay with
their owners. No generic molecular matcher or persistence schema is duplicated.

The [#114 persistence correction](archive/interface_json_object_order.md) treats
label mappings as unordered. Contact/surface orientation comes from persisted
public-operation axes, resolved bijectively against participant local axes.
Ionic analysis order is an explicit list in new 0.5 records or actual older
construction evidence; unknown historical order remains unknown. The optional
new-construction choice is attributed to the caller. This is persisted reference
bookkeeping, without molecular correspondence inference or a new numerical kernel.

Offline aggregation admits the original schema-1.0 evaluator's single explicit
historical or current version key, preserves its complete mapping/digest and
keeps exact policy equality. It adds no producer alias to current evaluator
output and performs no molecular operation; [#113](archive/redocking_summary_receiving_controls.md)
records the original frozen evidence and bounded receiving.

The [first BindingSite profile](binding_site_data_core.md) separates undevaluated
criteria, source-addressed annotations and attributed observations without a MolSys
handle or coordinate copy. `site_records.py` validates only the owned declarative
wire profile; `core/site.py` provides immutable public construction/inspection/
revision. Existing local record IO and finite-JSON helpers are reused. New claim
interpretations cite old observations explicitly and preserve their original exact
claim refs; no self-referential digest or new observation credit is introduced.
MolSysMT continues to own all later source resolution/manipulation and geometry.

The [source-index membership profile](binding_site_membership.md) extends the
same site validation/lifecycle with explicit atom/group axis semantics. Local
normalization transports ordered declared integers, without selecting, expanding
groups, matching molecular identity or deriving coordinates. New wire 0.2 is
admitted separately from the actual old 0.1 profile. C1 owner facts are requested
under MolSysMT #746; no successful native projection is fabricated from labels.

The [elementary geometry profile](binding_site_geometry.md) adds explicit sealed
length quantities and an owned dimensionless orientation kind through the same
public site lifecycle. `_private/site_geometry.py` validates only declared
sphere/box data and reuses existing length admission plus PyUnitWizard's public
QuantityRecord codec. It implements no molecular transform, selector, frame
alignment or numerical geometry kernel. Geometry 0.3 and earlier profiles retain
separate admission; molecular resolution and actual placement remain C1/C2 work.

The [internal C2 geometry slice](binding_site_domain_geometry.md) lives in
`_private/site_domain_geometry.py`. It derives only declared sphere/axis-aligned
box data and retains the whole original site in a separate experimental local
recipe. BoxRegion dispatches that exact discriminator to its independent reader,
recomputes retained quantities/output and refuses backend export while placement
is unassessed. Strict old selection recipes are unchanged. This is an implemented
private substep, not a public application stub, new molecular kernel or source
identity/placement framework.

## Current source map

The following paths are implemented entry points, reviewed for the
[2026-11-06 handoff](MACHINE_HANDOFF.md). Public exports in
[`bindingmt/__init__.py`](../bindingmt/__init__.py) and the actual source remain
authoritative when this navigation map changes.

| Area | Current source | Responsibility |
| --- | --- | --- |
| Scientific declarations and records | [`core/problem.py`](../bindingmt/core/problem.py), [`protocol.py`](../bindingmt/core/protocol.py), [`search_domain.py`](../bindingmt/core/search_domain.py), [`results.py`](../bindingmt/core/results.py), [`outcome.py`](../bindingmt/core/outcome.py) | Problems, resolved Vina protocol, physical search domains, poses/results and per-item batch outcomes. |
| Native binding contacts | [`contacts.py`](../bindingmt/contacts.py), [`core/contact_footprint.py`](../bindingmt/core/contact_footprint.py) | Compose actual public MolSysMT contacts/distances and inspect/save/read independent participant footprints. |
| BindingSite declarations | [`core/site.py`](../bindingmt/core/site.py), [`_private/site_records.py`](../bindingmt/_private/site_records.py), [`_private/site_geometry.py`](../bindingmt/_private/site_geometry.py) | Coordinate-free membership/criteria, explicit elementary geometry and immutable offline versioned records; later molecular work remains MolSysMT-owned. |
| Interface data core | [`core/interface.py`](../bindingmt/core/interface.py) | Declared/native analysis records, immutable identity/reinterpretation and offline core JSON persistence; explicit native work is in contacts.py and burial.py. |
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
