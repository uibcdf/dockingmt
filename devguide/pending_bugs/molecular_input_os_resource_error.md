---
summary: Molecular input normalization wraps an original OS ENOMEM failure as invalid input.
issue: uibcdf/bindingmt#116
status: open
opened: 2026-11-13
closed:
severity: medium
verification: reproduced
area: [core, diagnostics, resources]
guard:
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
