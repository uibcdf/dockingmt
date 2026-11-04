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

## 8. Named charge consumption controls

The [named-charge contract](validation/named_partial_charges.md) and executed
notebook distinguish original MolSysMT calculation coverage, selected projection,
existing nonpolar-H transfers and three-decimal export. Methanol, flexible 5X72
and explicit-H 1VII protect fixed units, provenance and conservation. Native Vina
admission is an interoperability control; preparation typing and charge-model
suitability for a scoring function remain separately unqualified.

## 9. Explicit hydrogen-stage controls

The [ligand-stage contract](validation/ligand_preparation_stages.md) and executed
notebook retain the provider's generated-H geometry evidence separately from
unchanged original coordinates, atom correspondence and charge conservation.
A supported polar control is positive; original 181L BNZ remains explicitly
provider-blocked on bond aromaticity (MolSysMT #314). Neither successful local
H placement nor Vina admission establishes biological or preparation validity.

The BNZ blocker above describes the original stage qualification: MolSysMT #314
was subsequently delivered and consumed by the explicit 181L preparation workflow.
For the 2026-10-20 continuation, see the
[optional declared-state symmetry qualification](validation/symmetry_redocking.md)
and executed [human notebook](validation/human_3ptb_workflow_2026-10-20.ipynb).
Its new measurements retain positional baselines, explicit chemical hypotheses,
initial admission diagnostics and negative controls. This does not promote the
preparation model or all Core-MVP gates to scientific acceptance; visualization
is deliberately pending maintainer discussion.

## 10. Proposed additional-case pilot and plausibility boundary

The [2026-11-04 design](validation/scientific_panel_design_2026-11-04.md)
proposes 1HSG/MK1 and 1STP/BTN as additional local-redocking candidates, with
rigid/explicit-cut arms, three seeds and two effort levels (at most 24 searches).
Their source files, assemblies, chemical states, maps and resource/producer
identities are not yet admitted. This is a design, not an execution registration
or new scientific result. Existing cases remain development/regression evidence
with separate populations. The next step is source/admission review under #33.

The [provider inventory](validation/molecular_plausibility_inventory_2026-11-04.md)
records public MolSysMT coverage/CIP/geometry primitives and the distinction
between a measurement and a chemically justified assessment. Missing reusable
geometry/steric rules are proposed in [MolSysMT #555](https://github.com/uibcdf/molsysmt/issues/555).
RMSD and plausibility must remain separate outcomes. Unknown chemistry or missing
H-dependent geometry is unassessed, not silently passing or repaired downstream.

The [first source inspection](validation/scientific_panel_admission_2026-11-04.md)
preserves both PDB/CIF representations, actual provider assembly observations,
missing-residue reports and incomplete ligand chemistry. It does not admit a
case for search. MolSysMT #556 owns the observed native CIF occupancy loss;
no local molecular parser or metadata patch is introduced.

The [environment/template continuation](validation/scientific_panel_environment_2026-11-04.md)
adds nonperiodic provider measurements and before/after coordinate/readiness
digests. Water shells are descriptive, not hydrogen-bond or retention decisions;
boundary distances do not prove safe truncation. Provider CCD/template #557 and
existing provider terminal-completion tools retain their separate admission work.

The [terminal-control receiving](validation/scientific_panel_terminal_probe_2026-11-04.md)
executes one native OXT reconstruction on a detached 1HSG protein copy. Two OXT
atoms are generated, with source/input immutability and an attribute-drop warning;
the public map/new generation-history boundary is requested in MolSysMT #558.
Output old-atom geometry stays unassessed without that map. This is a software
control, not an admitted receptor or new docking outcome.
