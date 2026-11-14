---
summary: Molecular input normalization wraps an original OS ENOMEM failure as invalid input.
issue: uibcdf/bindingmt#116
status: resolved
opened: 2026-11-13
closed: 2026-11-14
severity: medium
verification: reproduced
area: [core, diagnostics, resources]
guard: tests/test_input_resource_errors.py::test_molecular_admission_preserves_enomem_and_ordinary_os_diagnostics
normative:
blocked_by: []
supersedes: []
---

# Molecular input OS resource exception identity

## What

On source `08356484a6e30ab173fb0b123ae9c6b8b652f30b`, an authored
OSError(errno.ENOMEM) at the public constructor's extraction step becomes
ArgumentError with the original exception only as cause. The input-normalization
handler preserves MemoryError but wraps the measured OS resource condition.
#92's resolved MemoryError and #115's resolved quantity boundaries retain their
separate scopes; neither is reopened or credited with fixing this path.

## How

Reuse the existing software provider double in `tests/test_input_resource_errors.py`,
inject the exact OSError(12) in extraction and call its ordinary receptor route.
Visits stop at form, conversion, sizes, state count/index/id, selection and
extraction. No real MolSys operation or allocation pressure occurs.
The unchanged `core/problem.py` source SHA-256 is
`1544f665d3c472edf5151b11b406e6762a6a01c8d76140b4fd2e6f12be906061`.
Source copy, receipt and terminal bounded outcome remain under
`.molsyssuite/site-domain-geometry-111-20261113/input-os-probe-01/`.

## Why

Callers must be able to distinguish resource interruption from invalid molecular
input. The independent C2 offline recipe does not exercise this route, so it can
advance while this explicit owning follow-up precedes molecular placement work.

## What was refuted

This is a local exception-boundary defect, not a demonstrated MolSysMT or
support-library failure. It needs no new molecular algorithm, source matcher,
exception framework, retry system, native build or real resource exhaustion.
The measured condition is ENOMEM; ordinary file/IO errors must not automatically
be called allocation failures.

## Scope and exclusions

Preserve source/structure/state/selection semantics, ordinary malformed-input
diagnostics and original scientific producers. The C2 increment records this
separate finding without changing the normalization implementation or claiming
its correction. Shared prefixes, native binaries and the previous #30 evaluator
hold are unchanged. #50 custody review: 2026-11-14.

## Acceptance criteria

Propagate the original admitted OS resource exception unchanged through public
constructor roles/redocking and relevant normalization steps. Cover expected
ordinary-provider errors separately and review the related branches' intended
IO/error contracts. Register a durable guard and run complete affected selections
under normal and pm/fs policies before closure; this report's probe is not that
final receiving evidence.

## Resolution — 2026-11-14

The existing `_normalize_input` translation now re-raises the original
OSError only when `errno == errno.ENOMEM`. Other OS/provider failures retain
the original field-local BMT-E002 and cause. This follows the already admitted
fixed-pose scoring pattern; it adds no generic exception framework or retry.
An AST check proves that the executable delta is exactly one `errno` import
and this conditional bare raise. All scientific choices, values, axes, states,
source metadata and existing input/record behavior remain unchanged.

The new guard supplies **135 controls**: three public routes, nine provider
stages and ENOMEM/ENOSPC/ENOENT/EACCES/unknown-errno failures. ENOMEM preserves
the exact object; ordinary OS failures preserve their owning diagnostic and
cause, and every path stops at the injected stage. Against the original runtime,
the complete 290-case resource module has **27 failures and 263 passes**. The
original 155 assertions are unchanged; no native allocation failure is induced.

Final smaller complete-module receiving passes **500 cases per policy**, normal
and pm/fs: 463 resource/helper/serialization/offline-domain cases plus 37
argument/bootstrap cases. Its final cells are `final-software-normal-01`,
`final-software-pm-fs-01` and the two `final-arguments-*-01` cells. The original
core-native population `final-core-normal-01` was interrupted at the owned group
RSS limit: sampled peak 564,477,952 bytes with a 512 MiB stop threshold, host
available memory still above 49 GiB, all owned processes terminal. Its 498/498
progress is not a successful result. The original broader selection is retained
under #30 and is not automatically restarted or replaced by the smaller result.
Neither is the prior evaluator hold restarted.

The selected lower-resource cells stay below 270 MiB group RSS. Execution is
serial, CPU 0/nice 10/one native worker, monitored 13 GiB reserve, 512 MiB RSS
threshold, 2 GiB AS and 45 CPU/120 wall seconds. Exact registration/source/test/
resource hashes, original/interrupted/final attempts, AST delta and final
workspace/committed-export/publication receipts retain #50 custody in
`.molsyssuite/molecular-input-enomem-116-20261114/`, review 2026-11-21.
Do not delete the earlier receipts whose 2026-11-14 review is due.

Audit: prepared/backend fast paths are unchanged; prepared source state getters
already propagate directly. Native state getters and redocking feed the same
normalization boundary now corrected. File/literal classification and direct
file open/read behavior are unchanged; this is not a new general file-IO policy.
Missing-file/permission/no-space controls keep their original diagnostic contract.

Source qualification uses MolSysMT `ff25f120243319ca9515009b4971e24a2eb0dc22`,
PyUnitWizard `cc51c8e600f78f108bc563edd3221bd8788ead86`, ArgDigest
`7be790b7334e16715fceebbfa8a2b400edf768bb`, SMonitor
`4a4cd1e415ea57e50c22925c36c2e727772fb3ab` and DepDigest
`5e93eaff314fe7cddf4eee89842977023b3a8b00`. The historical on-disk native SHA-256
is `2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`;
build/source authenticity is not inferred. These are the qualified original
development inputs, before any separate MolSysMT #746 source receiving.

No scientific fixture/helper/resource producer, dependency floor, shared prefix,
native build, public tag/package or remote CI is changed by this correction.
The six local and fresh committed-export gates cover Ruff, format, indexes,
documentation references/sketches, shared resources and the Conda contract.
Hosted/full-suite/installed/public/platform receiving and the actual BindingSite
C1 application retain their separate scope. Public closure follows successful
push and exact readback of the archived fix/evidence.
