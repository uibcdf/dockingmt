---
summary: Consume named MolSysMT charges with explicit conserved projection evidence.
issue: uibcdf/dockingmt#40
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [preparation, validation]
guard: tests/test_named_partial_charges.py
normative:
blocked_by: []
supersedes: []
---

# Consume named partial charges

## What

Preserve the public MolSysMT assignment report in prepared ligand/receptor
metadata. Record the existing nonpolar-H charge transfers and PDBQT rounding.

## How

Explicit callers assign a named model through MolSysMT. Public MolSysMT indexed
extraction validates its molecular binding and marks stale reports. DockingMT
rejects stale attribution and records original software, coverage, units and
atom correspondence without recalculating a model. Public
`audit_preparation_charges` observes current prepared numeric values and export
rounding; writers reject changed named consumer values.

## Why

MolSysMT #221 delivered named Gasteiger–Marsili and forcefield assignment in
`d43648337`. Existing DockingMT preparation consumes charges but drops model
provenance. Original calculation coverage, a selected projection, nonpolar-H
transfers and decimal rounding must remain distinguishable.

## What was refuted

No automatic default charge method, charge renormalization, new molecular
algorithm, private provider import, or Meeko runtime dependency.

## Scope and exclusions

Consumer qualification of committed provider source `7894435e748bc55254b6c3d2b63ae82c101e5774`,
using an isolated archive because the sibling checkout has human work in progress.
AutoDock typing remains heuristic and provisional (#5, MolSysMT #222).
The existing hydrogen/export operation remains temporary pending MolSysMT #223;
this records its behavior, without extending that molecular implementation.
`source_molsys` contains retained original individual charges, not the consumer's
merged values. H5MSM 0.5 does not preserve molecular mechanics attribution.

## Acceptance criteria

Independent explicit-H ligand and positive-total receptor controls; source
immutability, original versions, correspondence, stale rejection, finite JSON,
nondefault charge units, default provisional rejection, native engine acceptance,
saved result provenance, executed notebook and all required local gates.

## Measured outcome — 2026-10-04

All 24 new consumer controls pass. Original model/reference/software records,
explicit atom transfer maps, full versus selected calculation scopes, source
immutability, nondefault coulomb/pm units, stale provider binding and changed
consumer arrays are protected. A same-total atomic charge exchange cannot be
exported with unchanged named attribution. Flexible 5X72 preserves the known
source/prepared/PDBQT permutation. Real receptor and ligand Vina parsing and
exploratory docking/save/reload pass; the default heuristic-typing gate remains.

The complete final local gate passes **861 tests, no skips, 200.83 s**, with the
same 96 known warnings. Ruff lint/format (112 Python files), `pip check`, report
indexes and diff checks pass in `molsyssuite@uibcdf_3.14`, Python 3.14.7, Vina
1.2.7. DockingMT's editable distribution points at this checkout; no provider or
viewer worktree is changed. MolSysMT source `7894435e748bc55254b6c3d2b63ae82c101e5774`
is qualified through a committed archive; viewer pin `ec4c71e574d798b7c8675b7e7e983da878ce9889`
remains unchanged. CI pins advance only the MolSysMT source.

All three notebook cells execute in the requested interpreter; receipts bind
loaded source to the provider commit and retain actual producer distribution
metadata separately. Four controls are admitted by native Vina. 1VII preserves
+2 e before export and writes +1.988 e after rounding. The selected OH control
retains -0.190000579171 e rather than being renormalized to the original graph's
zero total. The 5X72 output has -0.001 e at decimal precision. These observations
are not model/scoring suitability, chemical typing or predictive qualification.

Provider delivery consumption is reported in
[MolSysMT #221](https://github.com/uibcdf/molsysmt/issues/221#issuecomment-5978093987);
derived transform/binding and retirement evidence is handed off in
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223#issuecomment-5978094139).
DockingMT #5/#33 remain partial. The remote instruction/guide-only checkpoint
adoption `a5db15c` was integrated without changing scientific source; completed
scientific gates remain applicable under the scoped checkpoint policy. Hosted
Python-lane results remain separate from this local source-qualified receipt.
