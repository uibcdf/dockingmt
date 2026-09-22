---
summary: Select molecular states and record preparation decisions for docking
issue: uibcdf/dockingmt#4
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [preparation, provenance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Select molecular states and record preparation decisions for docking

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; DockingMT Core MVP work.

## What

Make the chosen ligand and receptor states and preparation decisions explicit in a docking run.

## How

Record ligand chemical state and conformer, receptor state, pH and residue variants, retained waters/cofactors, and any transformation parameters; associate each result with those inputs.

## Why

The Core MVP requires prepared states and backend representations to be traceable to source systems.

## What is measured and what is assumed

**Inspected:** Inspected devguide/MVP.md and current preparation/result model. No end-to-end provenance audit was run.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Implicit selection from a current coordinate frame was rejected because the same source can have several valid experimental states.

## Scope and exclusions

Selection and provenance for the initial protein–small-molecule workflow; chemical-state enumeration and receptor repair remain MolSysMT capabilities.

## Acceptance criteria

- A run can identify the selected source states, structure indices, preparation choices, and backend artifacts.
- Ambiguous state selection fails or requires an explicit documented policy; redocking tests verify traceability.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#217, uibcdf/molsysmt#218, uibcdf/molsysmt#220.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
