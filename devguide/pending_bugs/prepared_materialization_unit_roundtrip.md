---
summary: Unchanged native materialization reassigns coordinates and changes canonical bits.
issue: uibcdf/dockingmt#104
status: active
opened: 2026-11-09
closed:
severity: medium
verification: reproduced
area: [preparation, reconstruction, units, ownership]
guard: tests/test_prepared_materialization_units.py
normative: devguide/validation/installed_reconstruction_2026-11-09.md
blocked_by: []
supersedes: []
---

# Native materialization coordinate round trip

## What

The real bba53f6 wheel passes18 selected reconstruction/composition cases normal,
but pm/fs has17 passes and one original failure: the independently returned
source-backed native system differs in canonical coordinate bits. The source
stays unchanged. Both role implementations unconditionally reassign coordinates
after their required public provider copy.

## How

Share #103's exact canonical-native/prepared comparison as private consumer glue.
Keep copying mandatory for materialization and optional for readonly export;
apply real coordinate edits through the public setter. Preserve source-free and
generic-form behavior, identity, available mechanics and original provider errors.
Do not introduce approximate tolerance, private data reads or provider patches.

## Why

Materializing an unchanged preparation should produce an independent equivalent
system without a numerical round trip or unrequested setter. Explicit prepared
edits, including one representable float, still have observable application.

## What was refuted

The public copy/setter follow their documented unit contracts. MolSysMT#675's
diagnostic delivery is independent and must not be used to change this baseline
before isolating the consumer correction. No new molecular algorithm is needed.

## Scope and acceptance

Receive both-role unit cross-products, exact unchanged snapshots, setter omission,
explicit edit transport, independent returns, copy/read/set failure identity and
caller-policy preservation. Keep original installed/source failures and qualify
the complete affected source selection plus a genuinely new installed wheel.
Full#47/#30/#73, actual canvas, public/platform/hosted and SSH-source gates retain
their separate scope; the native-build hold remains.
