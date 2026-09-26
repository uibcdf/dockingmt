---
summary: Link the 1IEP external PDBQT check to its source ligand
issue: uibcdf/dockingmt#14
status: resolved
opened: 2026-09-26
closed: 2026-09-26
verification: measured
area: [validation, provenance]
guard: tests/test_1iep_reference_map.py
normative:
blocked_by: []
supersedes: []
---

# Link the 1IEP external PDBQT check to its source ligand

## What

The existing public 1IEP check uses the prepared ligand PDBQT as both docking
input and pose reference. It does not tie the metric to the original ligand
molecular graph. The official upstream example also supplies a ligand SDF.

## How

Pin the SDF by source commit and SHA-256, read it with RDKit, then convert its
graph and coordinates to MolSysMT. For this fixed, aligned source pair, verify
each PDBQT atom by element and coordinate against exactly one SDF atom. Record
retained and omitted source indices, and calculate the pose metric against the
mapped molecular source.

Measured locally with the pinned upstream files: the SDF has 69 atoms and 73
bonds, preserved through its RDKit-to-MolSysMT conversion. The
ligand PDBQT has 40 atoms in a different order, and 37 retained atoms are heavy.
All 40 PDBQT coordinates have a unique same-element match within 0.02 Å; 29
source atoms are omitted. The corresponding Vina run returns one pose with a
0.897 Å positional heavy-atom RMSD and -13.286 kcal/mol score. This remains an
externally prepared, chemically unassessed case.

## Why

The source graph and explicit atom correspondence make the validation case
useful for future source-to-pose workflows while detecting reordered, omitted,
ambiguous, or changed atoms. SDF ingestion and the general mapping capabilities
belong to MolSysMT (`uibcdf/molsysmt#215`, `#223`, `#226`); this positional
check applies only to the pinned 1IEP pair and should be replaced when the
provider supplies a validated general mapping route.

## What was refuted

Equal atom order between the SDF and PDBQT is false. An RMSD against the PDBQT
alone does not verify correspondence with the original molecular graph.

## Scope and exclusions

This is a public, bounded validation case. It does not assign charges, validate
the external preparation chemistry, infer atom maps for arbitrary inputs, or
interpret docking scores as affinity or selectivity measurements.

## Acceptance criteria

- The SDF source identity is pinned and checked before docking.
- The case records an unambiguous source-to-PDBQT atom map and omitted atoms.
- The reported pose metric uses source MolSysMT coordinates in mapped order.
- Ambiguous or repeated atom mappings fail a durable test.

## Resolution

The pinned SDF is converted to MolSysMT through RDKit. The validator checks a
unique same-element, coordinate-based map for every retained PDBQT atom, then
measures Vina poses against the mapped source coordinates. The report contains
the source hash, retained map, omitted atom indices, and metric definition.
The full 1IEP case was rerun on 2026-09-26 with one pose at 0.897 Å and
-13.286 kcal/mol. `tests/test_1iep_reference_map.py` guards reordering and
rejects ambiguous or reused source atoms. The case-specific map is documented
as temporary pending MolSysMT #223 and #226; direct SDF ingestion awaits #215.
