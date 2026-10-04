---
summary: Summarize compatible redocking evaluations with explicit failure denominators.
issue: uibcdf/dockingmt#39
status: resolved
opened: 2026-10-04
closed: 2026-10-04
verification: measured
area: [analysis, validation, aggregation]
guard: tests/test_redocking_summary.py
normative:
blocked_by: []
supersedes: []
---

# Summarize redocking evaluations

## What

Public `summarize_redocking(evaluations, *, failures=None)` summarizes explicitly
selected case-ID mappings of saved evaluation reports and separately declared
failures. Preserve each case and its interpretation while exposing denominators.

## How

Validate finite schema 1.0 records, fixed-unit observations and their numerical
summaries. Admit only identical recorded criteria, ordered top-N requests,
evaluator identity, backend/version, protocol and complete preparation declarations.
Keep different references, inputs and domains case-specific. Preserve compact
per-case identity/context/reference evidence and a digest of the complete report.
Reuse DockingOutcome's public typed-error contract. Unknown recovery is separate
from evaluated nonrecovery; empty results are evaluated, with no recovered pose.

## Why

The accepted next workflow combines existing incremental docking and per-case
evaluation without introducing campaign classes, caches or another executor.
Silently pooling policies or excluding failures obscures what was measured.

## What was refuted

No implicit grouping, chemistry qualification, molecule matching, engine reruns,
score aggregation, scientific dataset certification or universal cutoff.

## Scope and exclusions

Small offline caller-selected collections. Full preparation/protocol equality is
deliberately conservative. Equality of unknown declarations is not validation;
reference populations and biological comparability remain caller responsibilities.
No provider changes or symmetry correction. Retain original reports separately.

## Acceptance criteria

Independent positive/negative/empty and failure controls, policy mismatches,
malformed report admission, denominators, finite JSON detachment, non-default
units and an offline fresh-reader gate. Execute a notebook over the existing
native reports and retain input hashes and reproducibility/interpretation limits.

## Measured outcome — 2026-10-04

Public `summarize_redocking` returns the detached finite schema 1.0 collection
record described in [the contract](../validation/redocking_summary.md).
All 87 focused cases pass (6.54 s before compact context storage, 7.70 s after).
Independent analytical translations distinguish first/closest and top-N recovery;
denominators cover positive, negative, empty and failed cases. Guards cover
known/unknown policy differences, typed JSON and summary inconsistencies, fixed
units under a non-default policy, detached ownership and a fresh offline reader
with Vina/MolSysViewer/Meeko blocked. The native saved-report control rejects
181L/1IEP mixing and preserves the positive/displaced-domain observations.

The complete final gate passes **837 tests, no skips, 210.09 s**, with the same
96 existing/provider warnings. Ruff lint/format (109 Python files), report
indexes, reporting guard and diff checks pass. `pip check` exits 0. Qualification
uses editable `molsyssuite@uibcdf_3.14`, Python 3.14.7 and unchanged source pins
MolSysMT `c19a47ada0c2279029abfa296cf915560610ad9a` and MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889`; source qualification is separate
from public dependency delivery.

All three notebook code cells execute in the requested interpreter. The input
report file remains 174,825 bytes with SHA-256
`383a3b1c75d66881d59862b0ff3e0676e1116b71530b72fe1af7d4c326870e1a`.
Raw receipts retain implementation/helper hashes and actual interpreter identity.
Five demonstration summaries occupy 133,190 pretty-printed JSON bytes after
storing common declarations once. No full reference coordinates or pose
populations are duplicated in collection records. This storage observation is
not a universal runtime/memory bound.

No native engine is rerun by this qualification helper or notebook; full existing
regression still includes the native engine controls. The declared failures are
explicit fixtures, not reported provider/runtime failures. Historical evaluator
versions, chemistry limits and metric populations remain untouched. The remote
canonical guide-only update `d4d4a89` was integrated without changing scientific
code or provider worktrees. No new cross-component limitation was found.
