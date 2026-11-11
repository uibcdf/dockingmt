---
summary: Offline batch-test collection imports an optional native engine through a fixture helper.
issue: uibcdf/bindingmt#99
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: low
verification: reproduced
area: [tests, optional-dependencies]
guard: tests/test_batch.py::test_batch_is_lazy_ordered_and_uses_public_dock
normative: devguide/validation/declaration_and_io_receiving_2026-11-09.md
blocked_by: []
supersedes: []
---

# Offline batch-test collection

## What

The first #97/#98 affected selection fails collection because importing two
fixed text constants from `test_engines` imports the Vina-owning typing helper.
No test/scientific assertion executes; exit2/one collection error is preserved.

## How

Move that import into the two scientific tests that actually use its names.
Keep every native assertion, fixture byte and helper unchanged. Offline receiving
explicitly excludes the three existing native execution cases; full native/
hosted scopes still require them. Do not install or synthesize an engine.

## Why

Offline contracts must be independently collectable without optional engines.
A declared deselection cannot take effect if collection has already imported
an unavailable engine through an unrelated fixture module.

## What was refuted

This is local test-import coupling, not missing production dependency or a
provider defect. No shared helper, fixture producer or runtime API changes.

## Scope and acceptance

Receive the complete declared offline selection normal/pm-fs with guarded engine
imports, exact AST/import/fixture inspection, independent records and final local/
fresh committed-source checks. Native execution and hosted debt remain separate.

## Bounded source resolution — 2026-11-09

The final complete [registered receiving](../validation/declaration_and_io_receiving_2026-11-09.md)
passes 521 cases normal/pm-fs, zero failures/errors/skips/warnings and three
explicit unchanged native deselections per profile. Final200-member/16-member
independent reading receives all original failures, intermediate corrections,
final source/AST/JUnit/Receptor/registry/resource facts without test replay.
Five runtime functions and two local test import placements are the complete
executable scope; original helper/data/scientific inputs and producers remain.
Ignored/explicitly replaced problem payloads are not copied. Existing private
wheels retain their original behavior; full installed/public/scientific/platform/
canvas/hosted requirements and broader #19/#28/#73 remain separate.
