---
summary: Qualify exact-input adapter/direct Vina fidelity with a bounded control.
issue: uibcdf/bindingmt#62
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: measured
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

## Resolution — 2026-11-04

Published/registered producer `32599a8ea59dbe9615cef005b7f1c4685dae39b2` attempts
both routes once. Each returns five poses with identical native energies, arrays
and raw PDBQT bytes, matching prescribed input/options and score projection.
The original gate fails 14/16 because its new oracle compares a unit abbreviation
literally and excludes the wrong engine-info path keys. Preserve that failure,
producer and all original output hashes. No BindingMT runtime defect is demonstrated.

The separately registered offline amendment corrects those two observer rules
on saved data through PyUnitWizard and exact nonpath metadata equality. It first
reproduces the failed original gate, then passes 16 corrected checks and rejects
12 adverse mutations, with zero additional searches or molecular/optional-engine
imports. Numeric tolerances remain exact. The original two-search denominator
and unassessed molecular/physical/public/visual scope remain unchanged.

The saved ligand declaration is rigid-only and native internal/torsional terms
are zero; flexible/nonzero-term behavior is outside this control's claim.

[Report and reproduction](../validation/vina_adapter_fidelity_2026-11-04.md),
[original identities/disclosure](../validation/data/adapter_fidelity_2026-11-04/manifest.json)
and [separate offline assessment](../validation/data/adapter_fidelity_2026-11-04/offline_assessment.json)
complete this bounded control under the existing validation/evidence policies.
The source gate/checkpoint and hosted recovery are recorded in #62/#28; broader
scientific/provider questions remain #33/#49. Original evidence remains retained
under the declared custody; managed inputs/caches and workers are retired.
