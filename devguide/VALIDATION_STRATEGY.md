# Validation Strategy

## Principle

> **Software correctness is not scientific validation.**

DockingMT requires both.

## 1. Software validation

Software tests should establish that the implementation behaves as specified.

### Core concerns

- molecular identity preservation;
- atom/entity mapping across backend conversion;
- unit conversion;
- deterministic region construction;
- configuration resolution;
- provenance recording;
- backend capability validation;
- parser/result normalization;
- error handling;
- serialization where implemented.

### Reproducibility tests

Where a backend supports deterministic seeded behavior, test repeatability under controlled conditions.

Where bitwise reproducibility is not realistic, define the appropriate reproducibility expectation rather than pretending it exists.

## 2. Scientific validation

Scientific validation asks whether the workflow produces scientifically meaningful behavior.

### Primary MVP benchmark: redocking

For a small transparent set of protein–ligand complexes:

```text
native complex
    ↓
remove/extract ligand
    ↓
prepare receptor/ligand
    ↓
redock
    ↓
compare predicted/native pose
```

Measure at minimum:

- pose RMSD to native/reference pose;
- whether a near-native pose is generated;
- rank of near-native pose;
- backend score distribution;
- failure mode.

Do not reduce validation to one average number.

### Preparation sensitivity

Preparation choices can dominate docking outcomes. Representative validation should eventually probe sensitivity to:

- protonation;
- tautomer choice;
- receptor hydrogens;
- retained waters;
- cofactors/metals where relevant.

The MVP need not solve all these cases, but failures should inform scope rather than be hidden.

### Search sensitivity

Evaluate representative sensitivity to:

- search-domain size/placement;
- sampling/exhaustiveness parameters;
- random seed where applicable.

### Failure cases

Maintain explicit cases where docking fails or is unreliable. A scientific library should document boundaries rather than benchmark only successes.

## 3. Later validation levels

### Cross-docking
Dock ligands into non-cognate receptor conformations to stress receptor-state dependence.

### Virtual-screening enrichment
When screening becomes mature, use appropriate benchmark sets and metrics rather than inferring screening quality from redocking alone.

### Engine comparison
When multiple engines exist, compare normalized outcomes without assuming score equivalence.

### Ensemble/dynamic-pocket validation
When these workflows exist, validate whether additional receptor states improve meaningful recovery rather than merely increasing computation.

## 4. Regression benchmark

The initial redocking set should become a stable regression benchmark.

The first measured, exploratory case is the
[181L redocking regression baseline](validation/181l_redocking_exploratory.md).
The [1IEP external PDBQT adapter check](validation/1iep_external_pdbqt.md)
separately probes a flexible ligand and the Vina boundary with upstream
prepared inputs. It does not validate DockingMT's preparation chemistry.

Changes to:

- preparation;
- backend adapter;
- default parameters;
- region construction;
- result normalization

should be checked against it.

## 5. Validation metadata

Every reported benchmark should record enough provenance to reproduce:

- source structures;
- selections;
- molecular states/preparation;
- search domain;
- engine/version;
- parameters/seeds;
- DockingMT version;
- metric definitions.

## 6. Avoid benchmark overfitting

The initial validation set is for correctness and regression, not for tuning DockingMT into apparent superiority.

Broader scientific claims require independent, appropriately designed benchmarks.

## 7. MolSysSuite contract validation

DockingMT should test not only docking algorithms/adapters but its citizenship in
MolSysSuite:

- PyUnitWizard dimension/quantity behavior at public boundaries;
- ArgDigest contract behavior for public APIs;
- DepDigest lazy-loading and missing-provider behavior;
- SMonitor diagnostic codes/signals for representative scientific failures;
- MolSysMT identity preservation across preparation/backend round trips;
- DockingMT-owned MolSysViewer addon integration when present.
