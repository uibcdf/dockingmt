---
summary: Stop recorded batch execution on OS-level memory allocation failure.
issue: uibcdf/bindingmt#106
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: medium
verification: measured
area: [execution, resources, diagnostics]
guard: tests/test_batch.py::test_os_allocation_failure_stops_without_consuming_next_item
normative: devguide/validation/batch_os_allocation_fix_2026-11-10.md
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


## Resolution — 2026-11-10

The recording policy now propagates the same OS allocation exception only when
its errno is ENOMEM. Four new cases verify both policies, first-outcome identity,
source borrowing/consumption and ordinary ENOENT/ENOSPC recording. The new
record-policy guard fails on original code, then both complete 45-case source
profiles pass with ten original tiny native searches each. All 41 original test
declarations/assertions remain unchanged; independent AST checks and retained
red/green records confirm that scope.

The normative source record retains 257 primary and 20 reader members, including
the original installed diagnostic, initial selector failure and missing serialized
post-origin metadata. Initial source import is checked by the executed driver;
missing later metadata is explicit. Original generated version labels and the
old aeae47d artifact keep their identities; new installed receiving remains #47.
No scientific fixture/dependency/environment or runtime schema change is made.

## Installed receiving addendum — 2026-11-10

[Genuine private wheel receiving](../validation/installed_allocation_fixes_2026-11-10.md)
now receives this correction from exact producer `37a61e6`, actual version
`0.0.0+359.g37a61e6`. All 45 batch cases pass under each caller unit policy,
including all four allocation/ordinary-I/O controls and the original ten tiny
native searches per policy. The additional overlapping four-case pilot passes
without actual native/molecular calls. All 305 main installed cases per policy
pass; independent 419/14-member records bind actual wheel/installed bytes,
version/RECORD/PEP 610, native outputs and 606 shared support declarations.

The old aeae47d diagnostic, source red/green population and missing historical
post-origin field remain unchanged. No source/fixture/provider change, native
rebuild, shared install, publication or remote CI occurs. This issue remains
resolved; broader public/full/platform delivery stays #47/#30/#73 and retained
private resources stay #47/#50, review 2026-11-14.
