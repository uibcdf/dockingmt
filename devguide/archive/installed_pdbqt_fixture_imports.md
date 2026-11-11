---
summary: Isolated installed tests import shared PDBQT fixtures from a sibling test module.
issue: uibcdf/bindingmt#101
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [tests, packaging, provenance]
guard: devtools/tests/test_installed_support.py
normative: devguide/validation/record_wheel_inputs_2026-11-09.md
blocked_by: []
supersedes: []
---

# Installed PDBQT fixture ownership

## What

The expanded installed selection fails collection because importlib mode cannot
resolve `test_engines` as a sibling top-level module. The actual wheel,67-path
payload, ordinary installation and four import-origin controls already pass;
no molecular test executes in the failed selection. This is test support.

## How

Move the two original literal constants into unshipped `bmt_test_support`,
retain their byte identities/producer and test-engine aliases, update direct
consumer imports and add one exact support SHA-256 entry. Preserve all previous
594 source/target/digest records and every scientific assertion. Transport only
explicit qualification-test/helper/descriptor overrides into the source-free
harness, with exact frozen input hashes, retaining the same original wheel.

## Why

Installed scientific tests must use declared helper ownership, without depending
on source-path injection or importing unrelated optional-engine test modules.
The shared runner's importlib isolation is intentional and remains unchanged.

## What was refuted

No production import, shared-runner defect or new molecular fixture is shown.
No provider workaround, source-path bypass, rebuilt wheel or scientific replay.
The initial two assertion-rewrite warnings come from harness plugin pre-import;
let pytest load its plugin before reading its artifact, without suppressing them.

## Scope and acceptance

Receive exact original fixture/import/AST preservation, complete administrative
support controls and both whole installed normal/pm-fs selections. Verify all 595
support inputs/retirement, original wheel identity/imports and independent records.
Keep full native/public/platform/hosted qualification separate and preserve every
old failed outcome, original helper input and producer.

## Bounded installed resolution — 2026-11-09

The exact same original wheel passes complete1,267-case normal/pm-fs receiving,
zero errors/skips/warnings and four explicit unchanged native deselections each.
The one new declared helper makes595 staged inputs; all old594 records and
original two literal hashes remain exact. All20 affected scientific test-module
ASTs match outside fixture-only import/assignment placement. Full administrative
support/source controls pass 101 tests/26 subtests; independent415/25-member
receiving authenticates original failed collection, both intermediate and final
profiles, wheel identity, payload/imports and complete support retirement without
replay. No runtime code/provider/native algorithm or original scientific input
changes. Actual public/full native/platform/hosted evidence remains separate.
