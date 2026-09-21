# Implementation Strategy

## Purpose

This document tells a human developer or coding agent how to germinate DockingMT from
this `devguide` without prematurely implementing the full ontology or scientific horizons.

## Prime directive

> **Implement the smallest scientifically complete path through the Core MVP.**

Concepts marked `DESIGNED FOR` or `HORIZON` exist to protect architecture. They do not,
by themselves, authorize code, empty modules, abstract base classes or dependencies.

## Before writing code

1. Read `MOLSYSSUITE_CONTRACT.md`.
2. Read the complete DockingMT `devguide`.
3. Read the current canonical `MOLSYSSUITE_GUIDE.md` from the component repository once
   DockingMT is registered/bootstraped.
4. Check the current authoritative suite policies rather than copying an older sibling's
   local conventions.
5. Identify the single Core MVP gate being implemented.
6. State its scientific acceptance criterion and tests before expanding scope.

## Bootstrap sequence

### Step 1 — suite-native repository skeleton

Create only the minimum repository structure required by current MolSysSuite governance
and Python packaging conventions.

Adopt shared infrastructure intentionally:

- PyUnitWizard for physical quantities;
- ArgDigest for public boundaries;
- DepDigest for optional providers/backends;
- SMonitor for diagnostics;
- MolSysMT for molecular-system semantics.

Do not create local substitutes.

### Step 2 — minimal scientific model

Implement only the concepts required for Gate C0 and the first redocking workflow.

Do not instantiate the entire conceptual ontology as code.

For example, if `SearchGuidance` is not required by the first Vina redocking path, its
existence in the scientific model does not require a `guidance/` package yet.

### Step 3 — Vina adapter

Integrate AutoDock Vina behind a backend boundary.

Vina-specific concepts must remain internal to the adapter/provider layer.

Do not expose PDBQT, Vina boxes or command-line flags as DockingMT's universal model.

### Step 4 — preparation path

Construct one explicit, traceable preparation path suitable for a conventional
protein–small-molecule redocking case.

Prefer MolSysMT for general molecular operations.

Use external providers only behind MolSysSuite/DockingMT contracts where needed.

Record what happened.

### Step 5 — first redocking case

Make one scientifically transparent complex work end-to-end:

```text
input complex
    -> molecular state/preparation
    -> search domain
    -> Vina execution
    -> normalized poses
    -> RMSD/reference comparison
    -> provenance
```

This workflow is more important than adding breadth.

### Step 6 — validation and diagnostics

Add:

- deterministic software tests where appropriate;
- scientific redocking metric(s);
- identity/round-trip tests;
- unit-contract tests;
- backend capability tests;
- structured SMonitor diagnostics.

### Step 7 — MolSysViewer basic addon

Once the result model is stable enough, implement the minimal DockingMT-owned viewer
addon needed to inspect receptor, search domain, poses and reference pose.

Visualization must consume scientific objects; it must not become their owner.

### Step 8 — finish Core MVP gate-by-gate

Do not begin Extended MVP merely because individual features are attractive.

Core MVP completion is a scientific milestone.

## Scientific defaults

> **Scientific defaults are part of the protocol and must be explicit, inspectable and
> version-aware.**

Examples include:

- default search padding;
- number of poses;
- Vina exhaustiveness;
- random seed policy;
- water handling policy;
- molecular-state selection policy;
- preparation engine/provider defaults.

Do not hide scientifically meaningful choices inside implementation constants.

A resolved protocol/run should expose the defaults that actually took effect.

## No speculative implementation rule

For `DESIGNED FOR` and `HORIZON` concepts:

**Allowed now:**

- vocabulary;
- conceptual interfaces;
- architecture stress tests;
- documented future contracts;
- tests proving current design does not obviously preclude them, when cheap.

**Not justified solely by documentation:**

- empty packages;
- placeholder base classes;
- generic plugin frameworks;
- speculative database schemas;
- new hard dependencies;
- abstract factories with one implementation;
- premature HPC/campaign infrastructure.

Implement an abstraction when at least one real workflow requires it or two concrete
implementations demonstrate the need for a shared contract.

## Provider selection

Do not hard-code a philosophy of "native" versus "external."

Ask:

1. Does MolSysSuite already provide the capability?
2. Does the capability scientifically belong to a sibling component?
3. Is there an excellent external implementation that can sit behind the contract?
4. Does DockingMT require native control for scientific novelty, traceability or
   performance?

Follow the answer, preserving the scientific abstraction.

## Cross-component discovery rule

If implementation reveals that DockingMT needs a missing MolSysMT/PyUnitWizard/
ArgDigest/DepDigest/SMonitor/MolSysViewer capability, do not quietly solve the provider's
problem inside DockingMT.

Use the MolSysSuite cross-component feedback workflow.

## Definition of a good early commit

A good early DockingMT commit should make one scientific workflow more correct,
inspectable or testable.

It should not make the repository merely look architecturally complete.


## Execution restraint

Do not build generalized execution infrastructure during the Core MVP solely because
future campaigns may use Slurm, GPUs or distributed workers.

Preserve the conceptual distinction `Backend != Executor`, but keep local execution
simple until a second real execution mode requires a reusable executor contract.
