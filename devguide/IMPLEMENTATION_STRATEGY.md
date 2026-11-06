# Implementation Strategy

## Purpose

This document explains how to extend the existing library without prematurely
implementing its full ontology or scientific horizons. Start with
[development setup and workflow](DEVELOPMENT.md) and the
[machine handoff](MACHINE_HANDOFF.md), then select work from the
[complete requirement/evidence plan](PRE_STABILIZATION_PLAN.md).

The accepted target is Core C0–C6 plus Extended E1–E5 in the prospective 0.5.0
functional milestone, followed by stabilization and the later 1.0.0 decision.
[DMT-045](DECISIONS.md#dmt-045--require-core-and-extended-mvp-for-100),
[DMT-046](DECISIONS.md#dmt-046--deliver-the-complete-functional-objective-before-stabilization)
and the [release ladder](RELEASE_MILESTONES.md) own that scope. It remains
incomplete; an implemented API, a passing helper or one qualified workflow does
not accept the complete objective. Moving development to another machine does
not authorize a new calculation or release.

## Prime directive

> **Advance the complete accepted Core-plus-Extended objective through concrete,
> scientifically justified workflows.**

Concepts marked `DESIGNED FOR` or `HORIZON` exist to protect architecture. They do not,
by themselves, authorize code, empty modules, abstract base classes or dependencies.

## Before writing code

1. Read the root [contributor instructions](../AGENTS.md), synchronized
   [MolSysSuite guide](../MOLSYSSUITE_GUIDE.md) and applicable directory instructions.
2. Read the current [handoff](MACHINE_HANDOFF.md), [development workflow](DEVELOPMENT.md)
   and [operational roadmap](ROADMAP.md#current-operational-plan). Use the
   [document map](DOCUMENT_MAP.md) for the relevant design and evidence, rather
   than treating every archived checkpoint as a current work queue.
3. Identify the accepted workflow, its owning issue and its requirement in
   [the full plan](PRE_STABILIZATION_PLAN.md). Preserve the other requirements
   while making a bounded change.
4. Check [component responsibilities](MOLSYSSUITE_CONTRACT.md) and existing public
   provider tools. General molecular inspection, characterization, identity,
   geometry, manipulation and serialization belong to MolSysMT. Report an
   uncovered capability there; do not implement a molecular fallback here.
5. State the relevant scientific/API acceptance criteria, compatibility and
   informative controls before expanding scope. Distinguish software, source,
   installed, scientific, public-package and visible evidence.
6. Select checks appropriate to the change. Register scientific populations,
   resources and failure rules before computation; the handoff's local resource
   hold and deferred visual review remain in force.

## Original bootstrap sequence — historical foundation

The following sequence records the original approach to establishing the first
Core path. Those seams now exist; it is not an instruction to recreate the
repository skeleton, add speculative packages or repeat completed experiments.
The [actual source map](ARCHITECTURE.md#current-source-map) and current owning
issues determine where new work belongs.

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

Delegate general molecular operations to MolSysMT. If a required operation is
missing, request or propose it in MolSysMT and receive the supported contract.

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

Core MVP completion is a scientific milestone, not the presence of individual
features. The later accepted Core-plus-Extended objective permits concrete
E1–E5 workflows to advance alongside remaining Core work. Reuse delivered APIs
and follow [the full plan](PRE_STABILIZATION_PLAN.md); neither Extended features
nor partial Core evidence waive the other gates.

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

Follow the owning component's supported contract, preserving the scientific
abstraction. Selecting an external backend does not move a reusable molecular,
pharmacophore, topographic or flexibility operation into DockingMT.

## Cross-component discovery rule

If implementation reveals that DockingMT needs a missing MolSysMT/PyUnitWizard/
ArgDigest/DepDigest/SMonitor/MolSysViewer capability, do not quietly solve the provider's
problem inside DockingMT.

Use the MolSysSuite cross-component feedback workflow: open or update the
provider issue with concrete consumer evidence, cross-link the DockingMT owner,
and receive the delivered public operation. Existing relevant issues should be
extended instead of duplicated. Provider source availability is not proof of
compatibility with a particular installed artifact.

## Definition of a useful implementation commit

A useful DockingMT commit should make an accepted scientific workflow more correct,
inspectable or testable.

It should not make the repository merely look architecturally complete.


## Execution restraint

Do not build generalized execution infrastructure solely because future campaigns
may use Slurm, GPUs or distributed workers. The accepted small-collection E2
workflow reuses serial `dock_many`; it does not require a campaign scheduler.

Preserve the conceptual distinction `Backend != Executor`, but keep local execution
simple until a second real execution mode requires a reusable executor contract.
