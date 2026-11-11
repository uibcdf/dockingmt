---
summary: Unchanged native materialization reassigns coordinates and changes canonical bits.
issue: uibcdf/bindingmt#104
status: resolved
opened: 2026-11-09
closed: 2026-11-09
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

The public copy/setter follow their documented unit contracts. MolSysMT #675's
diagnostic delivery is independent and must not be used to change this baseline
before isolating the consumer correction. No new molecular algorithm is needed.

## Scope and acceptance

Receive both-role unit cross-products, exact unchanged snapshots, setter omission,
explicit edit transport, independent returns, copy/read/set failure identity and
caller-policy preservation. Keep original installed/source failures and qualify
the complete affected source selection plus a genuinely new installed wheel.
Full#47/#30/#73, actual canvas, public/platform/hosted and SSH-source gates retain
their separate scope; the native-build hold remains.


## Resolution and receiving

Producer `aeae47d50c5e90687c2558437cb22cf8f271ce85` keeps native copies independent
and omits a redundant coordinate setter only after an exact public comparison.
The new 24-case guard covers both roles, all nine unit pairs, one-ULP edits,
setter application/omission, original failures, caller policy and unchanged sources.
The original24-case red population has20 failures; original installed pm/fs receiving
has one failure out of18. Keep those outcomes independent from corrected receiving.

Complete source52-case and20-case export selections pass under both caller policies.
The genuinely new normally installed wheel `0.0.0+351.gaeae47d`, SHA256
`0b303ae371466a6736e8d194a89a54048f8bc51de3cd293cdc68c06050ae042b`, passes the
same whole selections on the original efbe67e1 provider cohort before its update.
There are zero errors/skips and one explicit search exclusion per52-case cell.
All 67 runtime paths,606 support declarations, input/native bytes, ordinary private
installation and metadata/RECORD/PEP610/import checks pass; METADATA differs only
in Version. A source cell with changed docstrings and an installed wall interruption
remain unqualified; repeated whole fixed-input cells pass. The owning validation
record preserves resource controls, frozen evidence and later provider receiving.

No scientific tolerance, provider patch, shared reinstall, native rebuild, public
package or hosted validation is claimed. Full distribution and product objectives
remain owned by #47/#30/#73. The durable guard is the complete new regression module.

Independent primary/reader evidence authenticates 1,412/14 members, including 23
stored JUnit/Receptor populations and nine exact qualified source files. The
subsequent source-only MolSysMT 0c6f9c7 cohort also passes52/20/64-case installed
selections under both policies plus six separate owner controls; no warning
filter, native rebuild, input rewrite or scientific acceptance expansion occurs.
