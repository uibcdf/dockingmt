---
summary: Stop recorded batch execution on OS-level memory allocation failure.
issue: uibcdf/dockingmt#106
status: active
opened: 2026-11-10
closed:
severity: medium
verification: measured
area: [execution, resources, diagnostics]
guard: tests/test_batch.py::test_control_and_resource_exceptions_propagate
normative: devguide/validation/installed_execution_boundaries_2026-11-10.md
blocked_by: []
supersedes: []
---

# OS-level allocation failures in recorded batches

## Observed boundary

The genuine installed aeae47d consumer stops its three-item stream for the same
`MemoryError` object, but records `OSError(errno.ENOMEM)` as an item failure and
executes the third item. ENOENT is correctly recordable. The generic Exception
handler after the explicit MemoryError handler causes this distinction. This
additional failure representation is absent from the 98 original batch/backend/
staging tests; their passing scope is preserved.

The controlled diagnostic raises pre-created errors; it allocates no large
objects and runs no molecular/native engine operation. Its outcomes are:

| Error | Outcomes yielded | Backend items visited | Same error propagated |
| --- | --- | --- | --- |
| MemoryError | success | first, bad | yes |
| OSError, errno.ENOMEM | success, failure, success | first, bad, third | no |
| FileNotFoundError, errno.ENOENT | success, failure, success | first, bad, third | no |

Exact private program/registration/outcomes remain under
`.molsyssuite/batch-allocation-error-20261110/diagnostic-01`, owners #106/#50,
review 2026-11-14. Actual elapsed 0.922 seconds, peak 78745600 B, no interruption,
all owned groups terminal. Receipt SHA256: `403a953657797a106c839bfefc4c58f49e75af2e0bb71c65e16f80fe9f981125`.
This is exception-routing evidence, not an observed native allocator failure.

## Correction and acceptance

Propagate the original OS error only for errno.ENOMEM, under both error policies,
without consuming another item. Preserve earlier successful outcomes, original
error identity, source ownership and traceback/result release. Do not parse error
messages or classify every OSError as an allocation failure. ENOENT and ENOSPC
remain ordinary item failures when recording is explicitly requested.

Add regression coverage and a red/green source receiving, followed by the whole
original native batch selection under both caller unit policies with the same
tiny inputs/seed/CPU 1. Keep source and old installed-wheel evidence separate.
No shared environment, provider, scientific fixture or runtime schema change is
needed. Public delivery/full-platform/scientific gates remain separately owned.
