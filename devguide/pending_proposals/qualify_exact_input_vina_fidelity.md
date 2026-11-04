---
summary: Qualify exact-input adapter/direct Vina fidelity with a bounded control.
issue: uibcdf/dockingmt#62
status: partial
opened: 2026-11-04
closed:
verification: inspected
area: [validation, backend]
guard:
normative: devguide/VALIDATION_STRATEGY.md
blocked_by: []
supersedes: []
---

# Exact-input Vina adapter differential control

## What

Audit Q1/E3 needs a current bounded adapter/direct observation, separate from
historical 1IEP evidence and in-call matrix retention tests. The new panel's
provider admission is unrelated to this existing-input software control.

## How

Register the dated producer and exact preflight before native execution. Reuse
the original 3PTB human record's authenticated captured PDBQT bytes. Attempt one
adapter and one direct Vina search under the same prescribed seed, CPU, box and
options. Compare native outputs exactly and check score projection/units.

## Why

An interface discrepancy must be separated from backend/model behavior before
interpreting outcomes. Strict same-host differential equality is an informative
software check, not a scientific success rate or a portable reproducibility rule.

## What was refuted

Capturing a matrix within one adapter call does not independently compare its
inputs with a separately prescribed native invocation. Nor does agreement of
native output alone qualify molecular interpretation or physical validity.

## Scope and exclusions

The producer adds no molecular parser, matcher, geometry/repair or preparation.
Existing source-free PDBQT reading retains its bounded #49/#521 ownership; this
control does not qualify complete-source correspondence. No new panel case,
RMSD, affinity, public file or visual criterion is assessed. Original records,
scientific inputs, provider pins and environments remain unchanged.

## Acceptance criteria

Preserve source/producer/native/input identities, actual calls, every attempted
route, raw output observations and pass/fail/unevaluated dispositions. Publish
the registration before execution. Stop on failure/mismatch without retry or
tolerance adjustment. Retain warnings and known shared-environment closure
findings under MolSysSuite #82; local source evidence is not public qualification.

## Initial state

The dated producer is prepared for pre-execution review. No new native search
has been attempted. A maximum of two searches, serial CPU 1, timeout 300 s per
worker and no retries is proposed. Observing one wrapper does not alter its
arguments or return values; the direct route uses independently frozen options.
