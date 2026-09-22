---
summary: Support selected flexible receptor residues in the Vina adapter
issue: uibcdf/dockingmt#7
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [vina, preparation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Support selected flexible receptor residues in the Vina adapter

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; extended DockingMT capability.

## What

Run a Vina protocol with explicitly selected flexible receptor residues.

## How

Request paired rigid/flexible PDBQT projections from MolSysMT, pass both to Vina, and retain residue-to-pose mapping and protocol provenance.

## Why

Vina supports a separate flexible receptor file, while the current adapter advertises rigid receptor only.

## What is measured and what is assumed

**Inspected:** Inspected dockingmt/engines/vina.py and Vina Python documentation; flexible receptor validation has not been performed.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Inserting flexible atoms into the rigid PDBQT was rejected because the rigid and flexible parts must form a partition.

## Scope and exclusions

Extended capability after the rigid Core MVP; no generic induced-fit algorithm or receptor-sidechain prediction.

## Acceptance criteria

- A documented example docks with selected flexible residues using both Vina inputs.
- Returned flexible-residue coordinates map to the original receptor, with no duplicate or lost receptor atoms.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#225.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
