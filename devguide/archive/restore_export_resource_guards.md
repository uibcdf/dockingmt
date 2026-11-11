---
summary: Restore isolated tracing guards against the migrated export benchmark implementation.
issue: uibcdf/bindingmt#72
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: low
verification: reproduced
area: [tooling, ci]
guard: devtools/tests/test_result_export_resources.py
normative:
blocked_by: []
supersedes: []
---

# Restore the migrated export resource guards

## What

All five `devtools/tests/test_result_export_resources.py` cases fail at
`4873a738bb5a4a40a079efd4cfe6ff38e14dc88a`. Their isolated `python -S` children
load the legacy `devtools/benchmark_result_export.py` shim, whose new helper
import is deliberately unavailable outside the checkout. The original ownership
assertions are never reached.

## How

Load the actual standard-library-only implementation directly from
`bmt_test_support/benchmark_result_export.py`. Add these five existing guards to
the current administrative CI job; do not create another job or dependency route.
The installed-support tests retain source shim coverage.

## Why

The #48 mechanism otherwise loses its executed isolated regression protection
after #47. This finding belongs to the local #50 operational review.

## What was refuted

The reproduction demonstrates a test entry-point failure, not a regression in
the benchmark's tracing ownership. Its implementation and measurements do not
need changing. Adding the checkout to the child import path would unnecessarily
weaken the isolated, standard-library-only guard.

## Scope and exclusions

The test entry point and existing administrative selection only. No helper/data
bytes, molecular operations, scientific benchmark, runtime payload, provider,
release or public-package qualification is changed.

## Acceptance criteria

The five child cases reach and pass their existing success/failure, caller/owned
tracing and no-molecular-import assertions. Run the updated administrative
selection and final committed-source publication/resource validators; retire
owned child scratch. Preserve #48's historical evidence with an addendum.

## Verification — 2026-11-05

The first execution fails all five cases with `ModuleNotFoundError` while loading
the legacy shim in the isolated child. After the path correction, all five pass
as part of the updated **38-test administrative selection** with published Pytest
Receptor 1.2.1. Every child still uses `-S`, a managed directory outside the clone,
the inert result, and its original no-molecular-import and tracing-ownership
assertions. The original #48 report receives a dated addendum.

The workflow change adds only the existing test module to the current job's
selection. The first combined administrative run also refuses the changed
workflow digest and stale report index (four failures, 34 passes); neither guard
is bypassed. After reviewing the exact test-selection-only diff, the dependency
route inventory records the new SHA-256 with unchanged acquisition routes, and
indexes are regenerated. The repeated selection passes all 38 tests.

No registered helper/data bytes change, so the support declarations and historical
producers retain their hashes. Ruff and index checks pass; final workspace and
fresh committed-export publication/resource receipts belong in #72. Exact-head
remote evidence remains #28 and is not inferred from a local passing run. #50's
broader review, including its deferred central handoff, remains open.
