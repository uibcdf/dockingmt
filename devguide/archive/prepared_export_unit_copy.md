---
summary: Caller length-unit changes falsely require copying unchanged native preparations.
issue: uibcdf/bindingmt#103
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [preparation, units, ownership]
guard: tests/test_prepared_export_units.py
normative: devguide/validation/installed_small_fixtures_2026-11-09.md
blocked_by: []
supersedes: []
---

# Unchanged native export after a caller unit change

## What

The actual old wheel passes 64 expanded cases under normal units; pm/fs has63
passes and one failure. A native preparation created under pm, exported under
angstrom, falsely appears edited. The resulting unnecessary copy fails on an
unrelated caller resource. Original attempts remain immutable under#47.

## How

The generic public getter follows the caller's unit policy. Comparing its
converted quantity with separately converted prepared coordinates introduces
different floating-point conversion paths. For canonical native sources, use
the provider's documented public `Structures.get_coordinates()` (owned nm
coordinates) and convert once to the prepared representation. Compare exact
arrays there. Preserve the existing generic-form route and explicit-edit copies;
do not access private arrays or alter the active process-wide unit policy.

## Why

Readonly exports should not depend on copying unrelated resources or on the
caller's display-unit choice. Real edits, including one representable float,
still require a detached provider copy and must propagate its original failures.

## What was refuted

This is a BindingMT comparison defect. No provider conversion/read-only contract
violation is demonstrated. Approximate scientific tolerance, hidden coordinate
repair, temporary global unit-policy changes and private native access are not
required. The 12 off-axis warnings are separately retained provider diagnostics.

## Scope and acceptance

Qualify both prepared roles and preparation/export unit cross-products, exact
tiny-edit detection, native read failure identity and caller policy restoration.
Receive the complete affected source selection and a genuinely new installed
wheel; the old wheel retains its original failure. Generic nonnative source
behavior is unchanged and not newly qualified. Full installed/platform/public/
canvas/hosted acceptance and source-context#100 remain separate.


## Actual source and new-wheel resolution

Both the complete 64-case affected selection and the 20-case new regression module
pass separately under normal and pm/fs policies in source and in a genuinely
new private wheel from producerbba53f6. Original source six-failure and old-wheel
one-failure outcomes remain unchanged. The 20 controls cover both roles, all nine
unit pairs, exact one-ULP edits, original MemoryError identity and caller-policy
restoration. All 606 support inputs retire; provider/native/fixture bytes stay
unchanged. Independent 999-member reading and 12 JUnit/Receptor cross-checks verify
the exact programs/inputs/results without molecular replay. MolSysMT#675/#677
retain their separate nonblocking provider feedback. Full#47/#30/#73 and actual
SSH-source/public/platform/canvas/hosted gates remain partial.
