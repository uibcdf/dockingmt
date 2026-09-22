---
summary: Returned Vina poses lack a verified map to source ligand atoms
issue: uibcdf/dockingmt#8
status: resolved
opened: 2026-09-22
closed: 2026-09-22
severity: high
verification: asserted
area: [results, identity]
guard: tests/test_results.py::test_molecular_pose_map_preserves_elements_and_rejects_reordered_source
normative:
blocked_by: []
supersedes: []
---

# Returned Vina poses lack a verified map to source ligand atoms

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Resolved for the initial Vina ligand workflow.

## What

Vina coordinates are collected without a verified source-atom map; prepared-ligand reconstruction writes every element as carbon and RMSD can rely on positional alignment.

## How

Carry the PDBQT export map into each pose, reconstruct on the original ligand topology, and validate atom identity before RMSD or molecular export. Preserve the pose score, rank, ligand and receptor state IDs, and run provenance through this reconstruction; do not present omitted hydrogen coordinates as docked coordinates.

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
- Tests cover reordered atoms, omitted hydrogens with an explicit missing-coordinate or named-reconstruction policy, preserved non-carbon elements, mapped redocking RMSD, and unchanged score, rank, state IDs, and provenance.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#223, uibcdf/molsysmt#226.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## Resolution

The Vina adapter verifies output PDBQT atom order and coordinates against the
input PDBQT and records ordered MolSysMT source atom identities in each pose.
It checks prepared names and elements against that source before attaching the
map. Molecular reconstruction checks the identities against the supplied
partner, including same-count systems, and returns only atoms with docked
coordinates. Molecular RMSD aligns the reference by the verified identities;
extra reference hydrogens are omitted from that comparison. Numeric coordinate
arrays remain an explicit positional RMSD input.

Raw PDBQT output without a molecular source map cannot be reconstructed as a
molecular pose or compared to a molecular reference. The MolSysViewer adapter
uses the same reconstruction guard and no longer fabricates carbon atoms when
the partner is missing. Serialization retains each pose's map, score, rank,
state IDs and result provenance. Tests cover reordered identities, retained
oxygen, omitted hydrogens, PDBQT order mismatch and mapped 181L redocking.
Generic PDBQT identity/parsing remains with MolSysMT issues #223 and #226.
