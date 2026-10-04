# Architectural and Scientific Decisions

This is a lightweight decision log. It records decisions that should not be silently reversed during implementation.

Each decision may be revisited when evidence justifies it.

---

## DMT-001 — AutoDock Vina is the initial reference engine

**Status:** Accepted

**Decision:** Begin canonical docking implementation with AutoDock Vina.

**Reason:** It provides an established reference point for protein–small-molecule docking and lets us validate DockingMT's scientific architecture without first inventing a new engine.

**Does not imply:** DockingMT is a Vina wrapper or that Vina defines its concepts.

**Revisit when:** A different backend is required for a validated scientific workflow or Vina blocks the Core MVP.

---

## DMT-002 — DockingMT will not model a search domain as a Vina box

**Status:** Accepted

**Decision:** A rectangular box is one search-domain representation/backend approximation.

**Reason:** Future TopoMT, blind-docking and native-engine workflows require richer spatial concepts.

---

## DMT-003 — Sampling, scoring, refinement and ranking remain distinct

**Status:** Accepted

**Reason:** Future protocols may combine different methods/backends for each stage.

---

## DMT-004 — Do not rewrite Vina in Rust for the MVP

**Status:** Accepted

**Reason:** A language rewrite does not advance the initial scientific objective. Native high-performance code should follow a concrete algorithmic/performance need.

**Revisit when:** DockingMT develops native algorithms or profiling identifies a justified kernel.

---

## DMT-005 — Preparation is part of the scientific protocol

**Status:** Accepted

**Decision:** Do not treat receptor/ligand preparation as mere backend file conversion.

**Reason:** Protonation, tautomerism, stereochemistry, waters, charges and related choices change the scientific problem.

---

## DMT-006 — Molecular states must remain identifiable

**Status:** Accepted

**Decision:** Prepared receptor/partner states must remain traceable to source entities and downstream poses/results.

---

## DMT-007 — Search domain, constraints and search guidance are distinct concepts

**Status:** Accepted

**Reason:** “Where to search,” “what is required,” and “what information should guide search” are scientifically different.

---

## DMT-008 — One protocol may use multiple backends

**Status:** Accepted

**Reason:** Multi-stage workflows may combine classical docking, physical refinement and ML rescoring.

---

## DMT-009 — DockingResult is not a file

**Status:** Accepted

**Decision:** Backend files are interchange/serialization details. The scientific result is structured DockingMT data.

---

## DMT-010 — Scores are plural and semantically named

**Status:** Accepted

**Decision:** A pose may carry multiple named scores. Ranking policy must be explicit.

---

## DMT-011 — Run and campaign are different conceptual levels

**Status:** Accepted

**Reason:** Screening, ensembles and consensus docking require aggregation above individual executions.

---

## DMT-012 — MolSysSuite integration uses scientific contracts

**Status:** Accepted

**Decision:** Avoid hard coupling to evolving internal APIs of TopoMT, PharmacophoreMT and ElastNetMT.

---

## DMT-013 — Redocking is the primary Core MVP scientific gate

**Status:** Accepted

**Reason:** It provides a transparent end-to-end validation of preparation, search, execution, normalization and analysis.

---

## DMT-014 — Core MVP and Extended MVP are separate

**Status:** Accepted

**Decision:** Screening, clustering and richer analysis should not prevent declaring the canonical core scientifically viable.

---

## DMT-015 — Difficult future chemistry is an architectural stress test

**Status:** Accepted

**Decision:** Peptides, macrocycles, waters, metals, blind docking and covalent docking should influence abstraction review without becoming premature MVP implementation requirements.

---

## DMT-016 — Long-term direction: molecular-landscape-aware docking

**Status:** Directional, not implementation commitment

**Decision:** Preserve the possibility of combining topographic, pharmacophoric, flexibility and conformational landscapes to guide docking and describe pose landscapes.

**Does not imply:** speculative abstractions should be implemented before a concrete workflow needs them.

---

## DMT-017 — DockingMT is a native MolSysSuite component

**Status:** Accepted

**Decision:** DockingMT inherits suite governance, shared infrastructure and scientific
integration philosophy from its first implementation.

---

## DMT-018 — Third-party tools are providers, not the scientific model

**Status:** Accepted

**Decision:** RDKit, PDBFixer, Meeko, Vina and future external libraries may implement
capabilities behind MolSysSuite/DockingMT contracts. Their concepts do not define the
public DockingMT ontology.

---

## DMT-019 — General molecular preparation should be composed with MolSysMT

**Status:** Accepted

**Decision:** DockingMT owns docking-specific preparation semantics. General molecular
operations should use MolSysMT where appropriate; backend-specific preparation remains
inside provider/backend adapters.

**Reason:** This preserves one coordinated, traceable MolSysSuite workflow instead of
recreating glue code inside DockingMT.

---

## DMT-020 — PyUnitWizard is the DockingMT physical-quantity layer

**Status:** Accepted

**Decision:** DockingMT does not define an independent unit system. Public physical
quantities follow the current MolSysSuite PyUnitWizard contract.

---

## DMT-021 — Shared infrastructure contracts are inherited

**Status:** Accepted

**Decision:** DockingMT should use ArgDigest for public-boundary contracts, DepDigest for
optional providers/dependencies and SMonitor for structured diagnostics according to
current MolSysSuite policy.

---

## DMT-022 — Scientific defaults must be explicit

**Status:** Accepted

**Decision:** Defaults capable of affecting scientific outcomes are part of the resolved
protocol/run and must be inspectable and version-aware.

---

## DMT-023 — Do not silently fork sibling capabilities

**Status:** Accepted

**Decision:** Missing capabilities owned by another MolSysSuite component are reported to
that provider. Any local workaround is explicit, cross-linked and temporary.

---

## DMT-024 — The MolSysViewer docking addon is owned by DockingMT

**Status:** Accepted

**Decision:** MolSysViewer provides addon infrastructure; the docking-specific addon is
distributed from DockingMT.

---

## DMT-025 — Horizons do not authorize speculative implementation

**Status:** Accepted

**Decision:** `DESIGNED FOR` and `HORIZON` concepts protect architectural possibility but
do not justify code, empty modules, dependencies or generic frameworks until an accepted
workflow requires them.


---

## DMT-026 — Backend/engine and executor are distinct concepts

**Status:** Accepted

**Decision:** A docking backend defines the scientific implementation; an executor
defines the execution environment. Do not create `SlurmVinaEngine`,
`ParallelVinaEngine`, or similar scientific-engine variants solely to represent where
or how Vina runs.

**Implementation note:** The Core MVP may use an implicit local executor and should
not build generic execution infrastructure prematurely.


---

## DMT-027 — Scientific objects require versioned persistent representations

**Status:** Accepted

**Decision:** Core DockingMT scientific objects should be serializable through stable,
versioned, machine-readable representations. No storage technology is frozen at this
stage.

**Reason:** Reproducibility, provenance, campaign analysis, MolSys-AI integration and
long-lived scientific results must not depend on live backend objects.


---

## DMT-028 — Backend support does not imply backend redistribution

**Status:** Accepted

**Decision:** Licensing and packaging constraints are part of every backend/provider
integration decision. A backend may be supported without being bundled or installed
automatically.


---

## DMT-029 — Native MVP preparation uses MolSysMT and DockingMT

**Status:** Accepted

**Decision:** Develop the molecular preparation capabilities needed by the Core MVP
through MolSysMT and DockingMT. Meeko is not an MVP runtime or installation dependency.
DockingMT may use independently published prepared inputs as fixed validation evidence;
their chemistry is recorded as unassessed unless a separate validation establishes it.

**Reason:** General molecular operations belong in MolSysMT, while docking-specific
projection and backend policy belong in DockingMT. If a required MolSysMT capability is
missing, track it in MolSysMT and keep any DockingMT implementation explicitly temporary,
with a removal condition. See [issue #5](https://github.com/uibcdf/dockingmt/issues/5)
and the [1IEP preparation audit](validation/1iep_preparation_audit.md).

---

## DMT-030 — Readers validate scientific schema versions before reconstruction

**Status:** Accepted, 2026-10-02

**Decision:** Existing `BoxRegion`, `DockingPose`, `DockingResult`,
`DockingProblem`, and `VinaProtocol` readers admit the explicit string version
`1.0`. An absent version denotes a legacy 1.0 record. Explicit unsupported or
malformed versions fail before scientific payload interpretation, including
nested pose and domain records. Readers do not modify the supplied version field.

**Reason:** Version fields cannot protect future evolution if readers silently
ignore them and relabel unfamiliar records. This corrects
[issue #27](https://github.com/uibcdf/dockingmt/issues/27) while preserving
the current unversioned input path.

**Implementation note:** The current readers share a small private admission
validator. This establishes no generic migration framework or new storage format.
The rule applies when an owned reader interprets a record; opaque metadata and
context dictionaries are not recursively reinterpreted as scientific objects.

**Revisit when:** An actual new schema or reader requires a documented migration
or a different supported-version set.

---

## DMT-031 — Describe score meaning and retain scalar ranking evidence

**Status:** Accepted, 2026-10-03

**Decision:** Named numeric scores may carry versioned descriptors in the existing
pose metadata extension point. The current Vina/Vinardo adapter declares empirical
meaning, conventional units, method/version and submitted-input/settings context.
Ranking preserves its explicit direction, checks matching declared semantics and
state IDs, and appends independent scalar observations and order indices to result
provenance. Existing latest-policy access and outer schema 1.0 remain compatible.

**Reason:** Saved results need sufficient interpretation and successive decision
evidence without a live engine. Unannotated legacy scores retain unknown meaning;
they may still be ranked explicitly, but cannot silently join a described collection.
Equal descriptors do not establish scientific comparability or physical energies.

**Implementation:** [Issue #31](https://github.com/uibcdf/dockingmt/issues/31) and
the [score/ranking contract](validation/score_semantics.md). Initial backend order,
legacy policy-only evidence and explicit rankings remain distinguishable. This
does not introduce a scoring engine, protocol-stage executor or campaign model.

**Revisit when:** A real rescoring/physical-energy or cross-run aggregation workflow
requires a new comparison policy, quantity boundary or identity contract.

---

## DMT-032 — Audit saved-result evidence without a live molecular system

**Status:** Accepted, 2026-10-03

**Decision:** Expose a bounded offline audit of existing saved result mappings.
Share byte-integrity verification with replay and reuse existing schema, score
and ranking validators. Reports distinguish complete internal agreement, missing
evidence and contradictions; no legacy semantics or scientific validity is inferred.

**Reason:** Core C5 requires reviewable saved evidence before replay or downstream
analysis, without introducing engine execution, molecular preparation, campaign
management or new provider responsibilities.

**Implementation:** [Issue #32](https://github.com/uibcdf/dockingmt/issues/32),
the [audit contract](validation/result_audit.md), a retained native software control
and an executed notebook. Unassessed preparation remains unassessed.

**Revisit when:** An accepted provider or rescoring workflow requires another owned
record crosscheck or stronger evidence than internal agreement.

---

## DMT-033 — Score a prepared fixed conformation independently of search

**Status:** Accepted, 2026-10-03

**Decision:** Expose `score(...) -> DockingPose` for the concrete prepared-input
Vina/Vinardo workflow and `DockingPose.with_scores(...)` for independent additive
evaluations. A nonabstract optional backend operation preserves existing docking
adapters. Reuse backend dispatch, input snapshots, score descriptors, units,
dependency guards and preparation assessment. Molecular geometry reads remain
public MolSysMT operations; submitted PDBQT keeps its exact bytes and torsions.

**Reason:** MVP E1 requires scoring an existing conformation and retaining prior
method outputs without pose optimization, score overwrites or implicit ranking.
This workflow can advance while provider parameterization work remains with
MolSysMT's owners.

**Implementation:** [Issue #34](https://github.com/uibcdf/dockingmt/issues/34),
the [contract](validation/fixed_pose_scoring.md), real-engine guards and an
executed notebook. Optional prior poses must match prepared geometry and known
states. Unknown identity stays unknown. Method components are those returned
by `Vina.score()`, independently of docking's `Vina.energies()` contract.

**Revisit when:** A second concrete scoring method needs broader score kinds,
different molecular identity/comparison policies or a dedicated scoring protocol.
This decision does not introduce a generic stage executor, campaign, refinement,
automatic pose-to-PDBQT reconstruction or scientific preparation qualification.

---

## DMT-034 — Audit standalone scoring evaluations offline

**Status:** Accepted, 2026-10-03

**Decision:** Expose `audit_pose(record)` for saved standalone scoring/rescoring
poses. Share the existing result auditor's payload, unit, descriptor, native
component and artifact checks, and validate evaluation history against current
scores, retained declarations and known states. New scoring records retain an
independent evaluation name and backend box; older records remain readable
with incomplete evidence.

**Reason:** The concrete fixed-pose workflow of DMT-033 saves multiple evaluations
whose evidence belongs to the pose rather than a docking result's provenance.
Core C5 needs a reusable audit before downstream analysis without rerunning a
backend or requiring molecular/provider changes.

**Implementation:** [Issue #35](https://github.com/uibcdf/dockingmt/issues/35),
the [contract](validation/pose_audit.md), retained native control, an executed
notebook and fresh-engine/offline tests. Internal agreement establishes neither
chemical validity nor agreement of stored coordinates with captured inputs.

**Revisit when:** An accepted workflow needs a separate molecular geometry audit,
additional scoring methods or multi-stage result provenance. General molecular
interpretation remains owned by MolSysMT; this decision creates no local parser,
generic stage framework, new ranking policy or provider implementation.

---

## DMT-035 — Execute prepared problems incrementally with explicit outcomes

**Status:** Accepted, 2026-10-03

**Decision:** Expose `dock_many(...)` as a lazy local serial consumer of prepared
`DockingProblem` inputs. Reuse public `dock` and its existing backend resolver.
Deliver one `DockingOutcome` at a time with an input position, detached problem/
protocol declarations and either the existing result or an exception summary.
Default item failures propagate; explicit recording continues ordinary failures.
Source failures, memory exhaustion and process-control exceptions propagate.

**Reason:** The first accepted MVP E2 block needs bounded orchestration storage,
preserved earlier outcomes and explicit failure handling while maintaining the
distinction between a scientific result and a collection of executions.

**Implementation:** [Issue #36](https://github.com/uibcdf/dockingmt/issues/36),
the [contract](validation/incremental_docking.md), native Vina/Vinardo equivalence
and lifecycle tests, and an executed notebook. Inputs/protocol/backend are
borrowed; result ownership remains that of an individual docking call. Index
is positional evidence, not an invented molecular/run/campaign identifier.

**Revisit when:** Accepted aggregation/comparison, a second real execution route
or measured backend reuse requires a new boundary. This block completes neither
scientific screening qualification nor cross-ligand ranking. General molecular
operations remain with MolSysMT and visualization with MolSysViewer.

## DMT-036 — Pair pose/reference frames explicitly and expose viewer failures

**Status:** Accepted, 2026-10-03

**Decision:** Replace the displayed result's molecular scene on reload. Require
one receptor structure and one reconstructed structure per pose. Expose public
`build_docking_reference_system(reference, n_poses)` in the viewer addon: repeat
one static reference or copy exactly N frames, using public MolSysMT operations.
Pair reference frame k with pose frame k through MolSysViewer's advertised
`structure_pairing='by_index'` parameter. Propagate provider/player failures and
publish result state only after successful completion.

**Reason:** A missing reference must not be mistaken for a successful overlay,
and existing reference trajectories must not be multiplied or silently truncated.

**Implementation:** [Issue #37](https://github.com/uibcdf/dockingmt/issues/37),
[contract and source evidence](validation/viewer_reference.md), executed
notebook and `tests/test_viewer_reference.py`. Count rejection precedes scene
replacement; later failures may leave a partially changed scene. No transaction,
alignment, chemistry assignment or browser rendering certification is claimed.

**Revisit when:** [MolSysViewer #151](https://github.com/uibcdf/molsysviewer/issues/151)
delivers published explicit pairing support qualified for every supported
provider profile. Remove the bounded legacy signature branch then; DockingMT
maintainers review it by 2026-11-03. CI source pins remain unchanged.

## DMT-037 — Evaluate redocking with explicit comparison evidence

**Status:** Accepted, 2026-10-03

**Decision:** Expose `evaluate_redocking` as a bounded single-result analysis
operation, reusing `DockingResult.get_rmsds` and public MolSysMT geometry. Require
an explicit length cutoff, retain current result positions separately from ranks,
and report first/closest pose and first-N recovery in a detached finite JSON
record. Molecular references use verified atom keys; explicit coordinates select
declared positional comparison. Preserve known state/population constraints,
reference geometry, actual pose hashes, preparation and execution context.

**Reason:** A numerical RMSD or a successful viewer overlay alone does not retain
the scientific comparison choices required to interpret pose recovery. Thresholds,
atom scope, alignment/symmetry and ordering must remain inspectable after saving.

**Implementation:** [Issue #38](https://github.com/uibcdf/dockingmt/issues/38),
[contract](validation/redocking_evaluation.md), independent geometric controls
and an executed native Vina notebook. 181L is explicitly provisional; external
1IEP remains unassessed. Its prepared-input 40-atom metric differs from the
historical 37-heavy-atom SDF metric.

**Revisit when:** [MolSysMT #310](https://github.com/uibcdf/molsysmt/issues/310)
provides qualified chemically constrained symmetry correspondence, or an accepted
multi-case workflow requires aggregation. No symmetry/graph/RMSD algorithm,
automatic alignment, dataset success rate or preparation validation is claimed.

## DMT-038 — Summarize compatible saved redocking cases with explicit denominators

**Status:** Accepted, 2026-10-04.

**Decision:** Expose public `summarize_redocking` over caller case-ID mappings of
saved evaluations and separately declared failures. Validate finite schema 1.0
observations and their numerical summaries; require exact recorded criteria,
ordered top-N requests, evaluator/backend identity, protocol and preparation.
Keep case input/reference/domain/ranking evidence and original-report hashes in
compact detached records. Reuse the public outcome typed-error contract.

**Rationale:** The accepted small-collection workflow needs visible policy
compatibility, individual cases and failures before a campaign class or executor.
Empty results are evaluated nonrecoveries; failures have unknown recovery.
Fractions explicitly name evaluated and submitted denominators. Empty/all-failure
collections infer no policy. Full preparation/protocol equality is a bounded,
conservative first profile, rather than an inferred common chemical scheme.

**Evidence:** [Owning issue #39](https://github.com/uibcdf/dockingmt/issues/39),
[contract](validation/redocking_summary.md), independent analytical/admission
controls and an executed offline notebook over retained native evaluations.
Positive/displaced-domain software controls are separate from a labelled failure
fixture. Equality of declarations does not certify scientific comparability,
chemical validity or a dataset success rate. No geometry kernel, molecular
matching, engine rerun, global ranking, cache, executor or sibling change occurs.

## DMT-039 — Preserve named charges and audit consumer conservation

**Status:** Accepted, 2026-10-04.

**Decision:** Consume explicit public MolSysMT named assignments through the
existing preparation boundary, preserving original model/software/coverage and
atom correspondence. Let public indexed provider extraction check molecular
binding. Record existing nonpolar-H transfers without renormalization. Expose
`audit_preparation_charges` for current numeric binding, selected-total
conservation and actual PDBQT order/rounding; guard named export after value edits.

**Rationale:** Source values alone lose the model that produced them and obscure
selection, hydrogen transfers and decimal rounding. Charge assignment/chemistry
remain MolSysMT operations, with no implicit model or private validator import.
A named charge model does not validate the remaining heuristic AutoDock types.

**Evidence:** [Issue #40](https://github.com/uibcdf/dockingmt/issues/40),
[contract](validation/named_partial_charges.md), executed notebook and public
provider controls from source `7894435e748bc55254b6c3d2b63ae82c101e5774`.

**Removal condition:** Replace the existing consumer H projection/writer when
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223) supplies a qualified
charge-preserving transform with correspondence and original assignment
provenance. Retain #5's default protection until named typing (#222) and scoring
compatibility satisfy their own scientific criteria. No AD4 or H5MSM mechanics
attribution support is inferred.

## DMT-040 — Delegate explicit H and charge stages at ligand preparation

**Status:** Accepted, 2026-10-04; original BNZ acceptance remains partial.

**Decision:** Extend existing `prepare_ligand` with optional keyword-only
`hydrogen_options` and `charge_options`. Require explicit fixed-state/pH/engine
and charge-model choices; default expansion loss handling is strict. Delegate
all molecular work to public MolSysMT operations and propagate failures without
fallback. Retain original H reports and compose original/expanded/prepared/written
atom indices, with null original indices for generated H. Reuse the named-charge
record and existing projection/audit rather than introducing another model layer.

**Reason:** The accepted preparation workflow needs observable stages and source
identity before engine execution. Existing calls retain their behavior. Metadata
composition is consumer orchestration; molecular construction and validity stay
provider-owned. Template application reports remain separate pending #298.

**Evidence:** [Issue #41](https://github.com/uibcdf/dockingmt/issues/41),
[contract](validation/ligand_preparation_stages.md), polar/idempotence/negative
controls and executed notebook on the existing qualified source pin.

**Limits:** Original 181L BNZ lacks bond-aromaticity evidence after the existing
template route and is rejected by H addition; MolSysMT #314 owns its correction.
No downstream graph repair is admitted. Local H placement is not environmental
refinement; typing/export/scoring qualification remains separately open.
