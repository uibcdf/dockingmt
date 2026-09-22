---
summary: Select active ligand torsions for Vina preparation
issue: uibcdf/dockingmt#6
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [preparation, vina]
guard:
normative:
blocked_by: []
supersedes: []
---

# Select active ligand torsions for Vina preparation

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; DockingMT Core MVP work.

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

Docking protocol choice and provenance; general torsion perception and PDBQT ROOT/BRANCH writing stay in MolSysMT.

## Acceptance criteria

- The selected active bonds and resulting torsion degree of freedom are inspectable for each ligand state.
- A flexible ligand reaches Vina with a valid tree, and invalid or unavailable torsion choices fail explicitly.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#214, uibcdf/molsysmt#224.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
