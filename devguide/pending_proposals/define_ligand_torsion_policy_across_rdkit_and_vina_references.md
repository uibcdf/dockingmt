---
summary: Define ligand torsion policy across RDKit and Vina reference differences
issue: uibcdf/dockingmt#17
status: partial
opened: 2026-09-26
closed:
verification: measured
area: [preparation, vina]
guard: tests/test_vina_torsion_matrix.py
normative:
blocked_by: []
supersedes: []
---

# Define ligand torsion policy across RDKit and Vina reference differences

## What

Decide the DockingMT protocol policy for ligand torsions when RDKit descriptors,
published Vina PDBQT branches, and explicitly selected bonds differ. The current
API accepts explicit bonds after bounded structural checks; it has no automatic
chemical classifier.

## How

Keep a small pinned [comparison matrix](../validation/vina_torsion_matrix.md)
with source atom IDs, selected branch bonds, rigid fragments, explicit hydrogen
differences, RDKit descriptor mode, and Vina parser acceptance. Define which
explicit requests remain valid, which fail or warn, and whether any automatic
policy can be justified. Preserve the chosen policy and source bond IDs in
preparation provenance.

## Why

For 1IEP, the published PDBQT has seven branches and RDKit `Strict` counts
seven, but the published bonds were supplied explicitly to DockingMT. In 1S63,
the published PDBQT has six branches while RDKit `Strict` counts five; the extra
branch is aryl–C≡N (source atoms 26–27). For ethyl acetate, DockingMT permits
an explicit ester acyl C–O torsion while RDKit `Strict` excludes it. Matching
one descriptor count cannot establish a general docking torsion policy.

## What was refuted

Treating RDKit `Strict` as the Vina branch oracle was refuted by 1S63. Treating
published Vina branches as chemically necessary was refuted as an unsupported
inference; they are comparison inputs. Comparing only `TORSDOF` counts was
refuted by tests where an incorrect cut has the same branch count.

## Scope and exclusions

DockingMT owns protocol-level selection and user-facing policy. MolSysMT
[#224](https://github.com/uibcdf/molsysmt/issues/224) owns reusable bond
classification and fragment contracts; MolSysMT
[#214](https://github.com/uibcdf/molsysmt/issues/214) owns eventual PDBQT
serialization. No Meeko runtime dependency or affinity-score claim is part of
this proposal. The temporary four-character atom-name defect is tracked
separately in [DockingMT #18](https://github.com/uibcdf/dockingmt/issues/18).

## Acceptance criteria

- Document the exact torsion-selection policy and whether explicit overrides
  can include ester and aryl–nitrile bonds.
- Preserve source bond identity, hydrogen projection, and selected policy in
  preparation and docking provenance.
- Keep representative conformational and reference-tree tests; explain every
  RDKit–Vina discrepancy instead of enforcing numerical equality.
- Replace temporary graph classification only after MolSysMT #224 passes the
  same bounded cases and preserves atom identity.

## Progress, 2026-09-26

Pinned 1IEP, 1S63, and both 5X72 stereoisomers are covered by
`tests/test_vina_torsion_matrix.py`. The test compares branch bond IDs and rigid
fragments with the published PDBQT and MolSysMT's independent covalent blocks.
RDKit `Strict` and `NonStrict` counts are recorded separately after removing
explicit hydrogens. `tests/test_flexible_ligand.py` captures the ethyl-acetate
difference. Chemical-policy acceptance criteria remain open.
