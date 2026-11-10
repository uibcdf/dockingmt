---
summary: Remaining sibling-test imports prevent isolated installed collection.
issue: uibcdf/dockingmt#102
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [tests, packaging, provenance]
guard: devtools/tests/test_test_support_boundaries.py
normative: devguide/validation/installed_collection_2026-11-09.md
blocked_by: []
supersedes: []
---

# Installed collection helper ownership

## What

The full isolated collection diagnostic at source 9375f3a8 fails with unresolved
`molecular_fixtures` and imports from sibling `test_*` modules. Zero tests or
fixtures execute. Missing optional Vina is an independent environment limitation.

## How

Move shared factories and finite declarations to declared, unshipped support.
Keep their function bodies, source aliases, original data targets and producer
identities. Adjust helper-relative data paths explicitly; retain all existing
595 support records. Guard against new sibling-test dependencies.

## Why

The installed runner deliberately excludes the source runtime and top-level test
path. Its supported staging mechanism owns helper imports and their custody.

## What was refuted

This is not a production-runtime or shared-runner defect. Collection does not
execute scientific tests and is not an installed scientific gate pass. No source
path injection, engine stub or provider code change can certify missing tools.

## Scope and acceptance

Receive direct helper imports, preserved test/function ASTs and input bytes,
exact support declarations, meaningful administrative controls and an isolated
collection diagnostic retaining any real optional dependency limitations.
Keep #47 public/full scientific and #100 actual source-context receiving separate.

## Received resolution — 2026-11-09

Eleven declared helper modules own the original shared factories/declarations;
31 test-module ASTs preserve every non-import/non-relocated node, and the source
fixture shim retains all three aliases. Exact helper bindings are preserved
apart from three explicit data-path rebases onto unchanged staged targets.
All original 595 support rows and scientific data remain exact;606 inputs now
stage/check/retire (42 code, 564 data). Both runtime packages and metadata stay
unchanged, 67 required paths.

The real installed wheel collects all 2,593 cases in importlib isolation with
zero tests/fixtures or molecular operations executed. Retained original Vina
bytes supply only collection imports; no installation/build occurs. Both complete
offline profiles pass 1,267 cases, four explicit native deselections and zero
warnings/errors/skips each. Administrative checks pass 104 tests/26 subtests,
including source-free fixture-path routing. Full scientific/native/public/platform
and hosted gates remain separately pending. Initial failures and the existing
Pytest Receptor#46 count discrepancy are retained rather than reclassified.


The first committed export also exposes five ignored compressed evidence members.
Their exact original bytes are explicitly versioned without rewriting either
manifest or result. The 13-member failure appendix preserves this failed admission;
final local/fresh committed checks authenticate all 235 members before push.
