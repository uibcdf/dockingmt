---
summary: Reject unlabelled numerical backend-box exports
issue: uibcdf/dockingmt#65
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: measured
area: [core, units, arguments]
guard: tests/test_core_helper_contracts.py::test_backend_box_requires_an_explicit_length_unit
normative:
blocked_by: []
supersedes: []
---

# Backend-box export requires an explicit length unit

## What

At source `5071731168bab30cab514fcf32142b76d732cae4`,
`BoxRegion.to_backend_box(unit=None)` strips its nanometer geometry into raw
tuples and returns `unit=None`. The record cannot identify the physical unit.

## How

Construct a box with center `[1, 2, 3] nm` and lengths `[2, 4, 6] nm`, then
export with `unit=None` in a pm/fs/kJ/mol application context. The returned
numbers are `(1, 2, 3)` and `(2, 4, 6)`, with no unit. Inspected PyUnitWizard
source is `9d74f0e1e911d78c1906948e74ce8da93935557d`; no provider is edited.

## Why

The consumer promises a declared numerical length boundary. Calling the
provider's `convert(..., to_unit=None)` requests no explicit destination;
that supported provider behavior does not supply the consumer's missing label.
Require explicit recognized length units using ArgDigest and public PyUnitWizard
predicates. Preserve strings/unit objects, caller policy, input geometry and
provider failures. General conversion and parsing remain provider-owned.

## What was refuted

The Vina adapter already requests angstrom explicitly. This reproduction does
not demonstrate incorrect existing docking results. #13's decimal precision
normalization is a separate delivered correction and is not reopened.

## Scope and exclusions

No new molecular routine, unit parser, normalization precision, scientific
population, public dependency floor or release. Broader helper review is #19.

## Acceptance criteria

Reject missing/wrong-dimensional unit requests with the owned `unit` argument
diagnostic; retain correct explicit strings/objects and values under non-default
application policy, without changing the source box or caller configuration.

## Resolution and evidence

ArgDigest now validates the export's unit through public PyUnitWizard
`is_unit` and `check(..., dimensionality={'[L]': 1})`. Missing, non-unit or
wrong-dimensional values fail with the owned `unit` argument diagnostic before
numerical export. Valid strings and unit objects retain their original
representation; existing conversion and Vina decimal normalization stay intact.
An unexpected provider validation failure retains its original exception cause.

The containing helper module initially gives twenty failures/eleven passes
across 31 controls on the starting source. All 31 then pass; relevant domain,
protocol, reconstruction, RMSD, replay, argument and bootstrap selections pass
353 cases with each of routine development ArgDigest `7e09e974` and exact CI
source `3d1ec53c`. Explicit strings/objects in Pint and unyt sessions retain
correct angstrom/pm values, original geometry and pm/fs/kJ/mol caller policy.
Those are software/unit-contract checks, not new molecular or docking evidence.
The six-case guard directly refuses the previously unlabelled None export and
invalid unit categories. Existing public/release/visual gates stay independent.
