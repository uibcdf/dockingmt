---
summary: Reject invalid pose-coordinate values before coercion and export.
issue: uibcdf/bindingmt#63
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: measured
area: [results, validation, units]
guard: tests/test_pose_coordinates.py
normative:
blocked_by: []
supersedes: []
---

# Finite real pose-coordinate admission

## What

At `8087603`, DockingPose accepts NaN/infinite length coordinates and boolean
arrays. Complex values are cast to float, discarding their imaginary component
with ComplexWarning. Deserialization casts values before the constructor; a live
pose mutated to NaN can also be exported without a coordinate argument error.

## How

Construct length quantities with those values, pass them to DockingPose, or
inject them into a saved coordinate record. No molecular or native work is
required. Reject invalid numerical schema values before casting/quantity
construction, guard normalized finite values, and validate mutable snapshots.

## Why

Coordinates in normalized docking results must be real finite lengths. A later
evaluator's refusal does not protect independent result readers/exporters from
silently altered complex data or nonfinite snapshots.

## What was refuted

Shape and length units alone do not establish finite real numerical contents.
This is a BindingMT record-admission defect, not an observed molecular-provider
or physical-model defect. No geometric assessment or repair is needed.

## Scope and exclusions

Keep public schemas, valid quantities and explicit shaped-empty behavior.
PyUnitWizard owns units/conversion; MolSysMT owns molecular interpretation,
geometry, identity and manipulation. Add no molecular tool or provider fallback.
Preserve original scientific/artifact receipts and qualification identities.

## Acceptance criteria

Invalid construction, saved values, normalization overflow and mutated snapshot
exports raise BMT-E002 for coordinates. Valid conversion, independent roundtrips
and caller policies remain covered. Existing result/score/evaluation/export and
native-output controls pass with source and installed scopes distinguished.

## Resolution — 2026-11-04

Construction checks real finite values before float conversion, normalizes
through PyUnitWizard and rejects overflow. Saved scalar types are checked before
quantity construction; current mutable values are checked on snapshot export
without another coordinate copy. Schema/arguments and valid quantities/identity/
snapshots remain unchanged. No molecular tool is added.

Before implementation, 18 of 22 new coordinate cases fail; afterward all 22 pass.
The disjoint selections pass 243 and 210 cases (453 total), no failures/skips,
76.62 s and 9.19 s. The first retains 39 LegacyH5MSMWarning and one
StructuralAttributeDropWarning; the second emits none. They cover result/score/
evaluation/audit/export and actual native-output integration. Prior installed/
scientific receipts and #62's native population are unchanged.

The [maintained contract](../validation/pose_coordinate_contract.md) records the
fix, malformed-old-record behavior, units and shaped-empty limits. The separate
four-form probe finds Astropy kcal/mol support missing, owned by PyUnitWizard
#137 under #19/MolSysSuite #127. That question does not block this finite-real
fix or justify a downstream unit alias. Broader #19 adoption and public/visual/
scientific acceptance remain partial. Exact publication/hosted recovery belongs
to #63/#28 closeout.
