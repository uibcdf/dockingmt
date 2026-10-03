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
