# Scientific MVP

## Definition of success

The MVP is judged by complete scientific workflows, not by number of functions.

Redocking is the primary end-to-end scientific validation workflow.

# Part I — Core MVP

## Gate C0 — Foundations

**PASS when:**

- core concepts have implementable representations;
- Vina is isolated behind an adapter;
- backend files are not the public scientific model;
- molecular identity can survive backend conversion;
- runs can record provenance;
- capability validation exists;
- physical quantities follow the MolSysSuite PyUnitWizard contract;
- public boundary validation follows the suite ArgDigest pattern;
- optional providers are isolated through DepDigest;
- diagnostics use SMonitor contracts;
- scientifically meaningful defaults are inspectable.

## Gate C1 — Preparation

Reproducibly prepare a conventional protein receptor and small-molecule ligand.

**PASS when:**

- inputs and transformations are inspectable;
- prepared molecular states are identifiable;
- backend representations can be traced to source systems/states;
- preparation errors are surfaced clearly.

The first preparation path need not solve all chemistry.

## Gate C2 — Redocking

```text
experimental complex
      ↓
identify/extract ligand
      ↓
prepare receptor + ligand state
      ↓
search domain from native ligand
      ↓
dock
      ↓
compare predicted/native poses
```

**PASS when:**

- multiple poses are normalized as DockingMT poses;
- scores and ranks are preserved;
- RMSD against the native ligand can be calculated;
- molecular/receptor state identity is retained;
- the run can be reconstructed from recorded configuration.

## Gate C3 — Explicit local docking

Dock one small molecule into an explicit local search domain.

**PASS when:**

- a box can be specified without making VinaBox the scientific API;
- results use the same result model as redocking;
- engine limitations/conversions are inspectable.

## Gate C4 — Selection-derived search domain

Construct a domain from a MolSysMT-compatible molecular selection.

**PASS when:**

- construction is deterministic and inspectable;
- the domain can be visualized;
- it can be converted for Vina without losing its source/provenance.

## Gate C5 — Result/provenance model

**PASS when** each pose/result can answer:

- which source molecules/states produced it?
- which receptor state was used?
- what preparation occurred?
- what domain was searched?
- which backend/version/parameters/seed were used?
- what produced each score?

## Gate C6 — Basic MolSysViewer integration

**PASS when:**

- receptor, search domain and selected pose(s) can be displayed together;
- a native/reference ligand can optionally be compared;
- no manual ad hoc file conversion is required.

**Core MVP complete:** gates C0–C6 pass and redocking validation is scientifically credible.

# Part II — Extended MVP

## Gate E1 — Explicit scoring/rescoring

**PASS when:**

- an existing pose can receive a named score;
- multiple named scores can coexist;
- ranking does not assume one universal score.

## Gate E2 — Small virtual screening

Dock a modest collection of ligands.

**PASS when:**

- individual failures do not corrupt the campaign;
- ligand/molecular-state identity is retained;
- results can be aggregated/ranked;
- campaign/run/result boundaries remain clear.

## Gate E3 — Pose comparison and clustering

Support basic:

- RMSD/reference comparison;
- pose-to-pose comparison;
- simple clustering where meaningful.

## Gate E4 — Basic interaction analysis

Provide a minimal structured interaction representation useful for filtering and visualization without making MolSysViewer the owner of the scientific information.

## Gate E5 — Reproducibility audit

A stored representative workflow should be independently reconstructable to the degree permitted by the backend and environment.

# Validation dataset

Before broad benchmarking, select a small transparent set of ordinary Vina-compatible protein–ligand complexes. Redocking should become the first end-to-end regression benchmark.

See `VALIDATION_STRATEGY.md`.
