---
summary: Returned Vina poses lack a verified map to source ligand atoms
issue: uibcdf/dockingmt#8
status: open
opened: 2026-09-22
closed:
severity: high
verification: inspected
area: [results, identity]
guard:
normative:
blocked_by: []
supersedes: []
---

# Returned Vina poses lack a verified map to source ligand atoms

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; DockingMT Core MVP work.

## What

Vina coordinates are collected without a verified source-atom map; prepared-ligand reconstruction writes every element as carbon and RMSD can rely on positional alignment.

## How

Carry the PDBQT export map into each pose, reconstruct on the original ligand topology, and validate atom identity before RMSD or molecular export.

## Why

Pose geometry, molecular identity, and redocking RMSD cannot be trusted when source and returned atom order or membership differ.

## What is measured and what is assumed

**Inspected:** Source inspected at dockingmt/engines/vina.py, preparation/ligand.py, and core/results.py; no mismatched-order result was executed.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Comparing equal-length coordinate arrays by position was rejected as evidence of identity because omitted or reordered atoms can still have matching shapes.

## Scope and exclusions

Result identity and reconstruction for the initial Vina ligand workflow; multi-model PDBQT parsing and generic mapping belong to MolSysMT.

## Acceptance criteria

- Every pose either carries a verified source-atom correspondence or rejects topology reconstruction and molecular RMSD.
- Tests cover reordered atoms, omitted hydrogens, preserved non-carbon elements, and a mapped redocking RMSD.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#223, uibcdf/molsysmt#226.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
