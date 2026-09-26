---
summary: Select active ligand torsions for Vina preparation
issue: uibcdf/dockingmt#6
status: partial
opened: 2026-09-22
closed:
verification: asserted
area: [preparation, vina]
guard: tests/test_preparation.py::test_ligand_writer_rejects_torsion_count_without_branch_tree
normative:
blocked_by: []
supersedes: []
---

# Select active ligand torsions for Vina preparation

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial; DockingMT Core MVP work.

## What

Allow the docking protocol to choose which candidate ligand bonds are active torsions.

## How

Consume MolSysMT rotatable-bond and rigid-fragment information, expose explicit selection or a documented default, and pass the selected torsions to the PDBQT writer.

## Why

The present ligand preparator defaults to zero torsional degrees of freedom, while flexible-ligand Vina input requires a valid torsion tree.

## What is measured and what is assumed

**Inspected:** Inspected dockingmt/preparation/ligand.py; no flexible-ligand validation fixture was measured.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

An unrecorded hard-coded torsion count was rejected because it cannot identify which bonds were flexible.

## Scope and exclusions

Docking protocol choice and provenance remain in DockingMT. General
rotatable-bond classification and rigid-fragment derivation belong in MolSysMT
under molsysmt#224. The current local graph bridge is temporary. PDBQT
ROOT/BRANCH serialization is also a temporary local implementation pending
MolSysMT's general PDBQT form in molsysmt#214.

## Acceptance criteria

- The selected active bonds and resulting torsion degree of freedom are inspectable for each ligand state.
- A flexible ligand reaches Vina with a valid tree, and invalid or unavailable torsion choices fail explicitly.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#214, uibcdf/molsysmt#224.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## 2026-09-22 progress

DockingMT's current PDBQT writer emits a rigid ROOT block and no BRANCH records.
It now rejects nonzero `torsion_dof` at preparation and export, rather than
writing a misleading TORSDOF count. The rigid policy is recorded in prepared
ligand metadata and therefore in Vina run provenance. This does not implement
active torsion selection or flexible-ligand PDBQT writing; the proposal stays
open pending the provider capabilities in molsysmt#214 and molsysmt#224.

## 2026-09-26 explicit torsion bridge

`VinaProtocol(active_torsion_bonds=[...])` now passes explicit selected-ligand
bond pairs into automatic MolSysMT ligand preparation. `prepare_ligand` accepts
the same selection directly. The temporary graph bridge in
`dockingmt/preparation/_temporary_torsions.py` consumes MolSysMT's public bond
pairs and orders, rejects non-single, ring, amide C–N, hydrogen, and terminal
heavy-atom bonds, and derives a deterministic rigid-fragment tree. The PDBQT
writer emits matching `ROOT`/`BRANCH` records and `TORSDOF`; it records the exact
PDBQT atom permutation so Vina poses reconstruct against source MolSysMT atom
identity. This bridge must be removed in favor of MolSysMT's implementation of
[#224](https://github.com/uibcdf/molsysmt/issues/224) once that API passes the
same cases and preserves the source map. The default remains rigid; there is no
unqualified automatic torsion-perception policy.

The [pinned 1IEP audit](../validation/1iep_preparation_audit.md) maps the seven
published BRANCH bonds to the molecular source and selects those bonds explicitly.
The native flexible writer retains all 40 matched atoms and emits seven branches
and `TORSDOF 7`. A separate conventional hexane case is accepted by Vina and
reconstructs its returned pose against MolSysMT after the PDBQT atom-order
permutation. These are software and reference-conformance results; they do not
validate ligand charges or atom types. The proposal remains partial until the
MolSysMT provider operation replaces the temporary graph bridge.

The expanded audit compares undirected branch bonds and rigid-fragment atom sets,
independently of root orientation and PDBQT serials. The native 1IEP projection
matches all seven published branch bonds and eight fragment sets. This confirms
tree serialization for explicitly supplied reference bonds, not automatic
torsion perception. RDKit 2025.09.5 counts seven `Strict` rotatable bonds on the
hydrogen-suppressed source and eight with `NonStrict`. A separate ethyl-acetate
probe (`CC(=O)OCC`) shows that the current bridge permits selecting the ester
acyl C–O bond while RDKit `Strict` excludes it. Chemical eligibility rules
therefore need an explicit provider policy; this discrepancy was reported in
[MolSysMT #224](https://github.com/uibcdf/molsysmt/issues/224#issuecomment-5844981980).
MolSysMT's existing `get_covalent_blocks(remove_bonds=...)` already supplies
basic bond-cut connectivity; the provider gap includes chemical classification
and a stable atom-identity-preserving fragment contract.
