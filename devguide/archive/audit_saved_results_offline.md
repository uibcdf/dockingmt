---
summary: Audit internal consistency of saved docking results offline
issue: uibcdf/dockingmt#32
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [results, provenance, validation]
guard: tests/test_result_audit.py::test_saved_native_control_is_consistent_without_live_dependencies
normative: devguide/validation/result_audit.md
blocked_by: []
supersedes: []
---

# Audit saved results offline

## What

Provide an offline consistency report for existing saved DockingResult records,
following Core C5 and the bounded extension work in #28.

## How

Reuse record, score and ranking validators and promote the replay tools' captured
PDBQT integrity check. Report consistent, incomplete and inconsistent evidence
independently, without a live backend or molecular system.

## Why

Saved records need reviewable interpretation and evidence checks before replay
or later analysis. Missing evidence must remain distinguishable from contradictions.

## What was refuted

A successful parse or matching digest does not establish chemical validity,
authentication or full scientific reproducibility. Inferring legacy units would
hide missing evidence.

## Scope and exclusions

Existing result schema, score meaning, explicit units, retained input bytes,
Vina context and ranking evidence only. No molecular operations, provider or viewer
changes, new scoring framework, campaign model or publication platform.

## Acceptance criteria

- Expose a supported offline operation with deterministic independent reports.
- Reuse captured-input integrity rules in audit and replay.
- Distinguish missing evidence from malformed or contradictory claims.
- Guard behavior with tests and retain an executed illustrative notebook.
- Pass local gates and synchronize issue-backed evidence.

## Implemented evidence (2026-10-03)

`audit_result(record)` returns a deterministic detached JSON report;
`verify_captured_inputs(artifacts)` promotes the existing replay integrity rule.
Both reuse the same private byte checker. Schema, named scores, descriptors and
ranking records reuse existing validators; native retained component meanings
are shared with the Vina adapter. No new dependency or sibling change is needed.

The retained minimal native Vina 1.2.7 result includes captured raw PDBQT inputs
and explicitly unassessed preparation. Its complete claims agree. Sixty-four
audit tests cover tampering, absent evidence, malformed scores/units/history,
context contradictions, stable ties, policy snapshots and successive rankings.
Guards forbid file access, live engine/viewer imports and molecular operations.
The executed notebook contains four code cells demonstrating all three statuses.

Focused audit/replay/profiling checks passed 82 cases before the final two missing
artifact cases; the final audit-only run passed all 64 cases in 1.53 s. Full
`pytest --receptor=llm` passed 478 tests without skips in 48.23 s on Python 3.13,
with the same twelve existing provider warnings. Ruff, formatting (84 Python
files), report indexes and whitespace checks pass. Hosted qualification for this
new operation is not inferred from the preceding commit's 414-test matrix.

The audit checks internal agreement only. Actual grid/weight settings have no
independent provenance copy; chemistry, authentication, full scientific replay
and public dependency admission are outside its report. The contract and notebook
retain these limits. Further publication decisions remain in #29.
