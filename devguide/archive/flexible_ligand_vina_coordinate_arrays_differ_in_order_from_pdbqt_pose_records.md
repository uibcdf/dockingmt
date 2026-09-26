---
summary: Flexible-ligand Vina coordinate arrays differ in order from PDBQT pose records
issue: uibcdf/dockingmt#12
status: resolved
opened: 2026-09-26
closed: 2026-09-26
severity: high
verification: measured
area: [vina, pose_identity]
guard: tests/test_engines.py::test_vina_pose_coordinate_array_permutation_uses_pdbqt_order
normative:
blocked_by: []
supersedes: []
---

# Flexible-ligand Vina coordinate arrays differ in order from PDBQT pose records

## What

The Vina adapter rejects an externally prepared flexible ligand when Vina's
coordinate array uses a different atom order from its PDBQT pose records.

## How

In the official 1IEP example, input and output PDBQT atom keys match in order.
Vina 1.2.7 returns one pose with 40 coordinate rows and 40 PDBQT records. The
two coordinate multisets match exactly at 0.001 Å precision, but corresponding
rows differ by up to 9.108 Å. The adapter currently compares rows and rejects
the result.

Use the verified PDBQT record order for DockingMT poses, and verify that each
Vina coordinate array represents the same coordinate multiset as the records.
Retain the existing atom-key and atom-count checks.

## Why

This blocks an ordinary flexible-ligand input and obscures the difference
between Vina's internal coordinate order and the input PDBQT atom identity.

## What was refuted

The rejection is not evidence of atom loss or changed PDBQT identity: counts,
keys and coordinate multisets agree. Accepting output records without checking
their relationship to Vina's coordinate array would discard an existing guard.

## Scope and exclusions

Output pose interpretation in DockingMT's Vina adapter. DockingMT's own rigid
ligand writer remains tracked by #6; generic PDBQT interpretation belongs to
MolSysMT issues #223 and #226. This is distinct from archived DockingMT #8.

## Acceptance criteria

- A permuted Vina coordinate array with matching PDBQT records yields poses in
  verified source PDBQT order.
- Changed atom keys, missing/extra atoms or changed coordinates still fail.
- The official externally prepared 1IEP pair reaches a result and its measured
  outcome is documented without claiming that DockingMT prepared its chemistry.

## Resolution

The adapter now checks ordered PDBQT atom keys against the input ligand and
compares the PDBQT and Vina numeric coordinates as multisets at Vina's 0.001 Å
output precision. DockingMT poses use the PDBQT record order, which carries
the verified atom keys. The guard named above proves that a permuted numeric
array produces the correct ordered pose and that a changed coordinate fails;
`test_vina_atom_order_verifier_rejects_permuted_pose` continues to reject
changed atom-key order.

The pinned external 1IEP case reaches a result with 40 mapped PDBQT atoms and
is documented in `devguide/validation/1iep_external_pdbqt.md`. Box-number
normalization is separately resolved under #13. The chemical assessment of
the external PDBQT remains `unassessed`.
