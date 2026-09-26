---
summary: Normalize Vina box numbers after unit conversion
issue: uibcdf/dockingmt#13
status: resolved
opened: 2026-09-26
closed: 2026-09-26
severity: high
verification: measured
area: [vina, search_domain, units]
guard: tests/test_engines.py::test_vina_box_rounds_unit_conversion_noise
normative:
blocked_by: []
supersedes: []
---

# Normalize Vina box numbers after unit conversion

## What

BoxRegion's Å-to-nm-to-Å conversion can pass sub-precision floating-point
artifacts to Vina. For the official 1IEP box, 20 Å becomes
19.999999999999996 Å and 53.903 Å becomes 53.90299999999999 Å.

## How

Using the official 1IEP PDBQT pair with Vina 1.2.7, seed 42, one CPU,
exhaustiveness 1 and five requested poses, exact documented box values gave
one pose with best score -13.286 kcal/mol. Passing the converted floating-point
values to the same direct Vina code gave two poses with best score -7.531
kcal/mol. DockingMT gave the latter result. The numeric box values are the
observed input difference; the internal Vina mechanism remains unconfirmed.

Round Vina center and size values to an explicit fine decimal precision after
unit conversion, and record the actual backend box in provenance. Verify
equivalent quantities under different units.

## Why

Scientifically identical user boxes should reach Vina as the same explicit
numbers. Otherwise seeded replay and benchmark comparisons can depend on
unit round-trip noise.

## What was refuted

The score difference was reproduced in direct Vina by changing only the box
numbers, so it is not caused by DockingMT's PDBQT staging or atom-order repair.

## Scope and exclusions

The Vina adapter's box projection; no change to SearchDomain's general
physical-quantity model or Vina's internal grid implementation. Related to
#12 and #4.

## Acceptance criteria

- Equivalent box quantities expressed in Å or nm produce the same backend
  center and size to an explicit documented precision.
- Result provenance records the numbers supplied to Vina.
- The official 1IEP case uses the documented 20 Å box and reaches Vina.

## Resolution

The Vina adapter rounds projected center and size values to six decimal
places in Å and records the exact submitted numbers, unit and rounding
precision under `provenance.backend_box`. The guard named above constructs
equivalent boxes in Å and nm under a non-default PyUnitWizard session policy
and asserts that both yield the same documented 1IEP box. The 181L replay
guard also compares recorded and repeated backend boxes.

The pinned 1IEP check now sends the documented 20 Å box and returned one pose
at -13.286 kcal/mol, with 0.897 Å identity-ordered heavy-atom positional RMSD
to the prepared bound ligand. See
`devguide/validation/1iep_external_pdbqt.md`. The internal Vina sensitivity
mechanism was not investigated further; the DockingMT boundary now supplies
stable, inspectable numbers.
