---
summary: Audit saved pose scores and evaluation history without a live backend.
issue: uibcdf/dockingmt#35
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [results, scoring, validation]
guard: tests/test_pose_audit.py
normative:
blocked_by: []
supersedes: []
---

# Offline scoring-pose audit

## What

Provide public `audit_pose(record)` for the saved standalone poses produced by
issue #34. Reuse the compact consistency report of issue #32 with explicit
scope `saved_pose_internal_consistency`.

## How

Share pose payload validation, byte integrity, score descriptors and native
component crosschecks. Check evaluation records against current pose values,
definitions and known states, distinguishing contradictions from absent evidence.
New scoring records retain independent `score_name` and `backend_box` evidence;
legacy missing fields remain incomplete. Keep molecular operations with MolSysMT.

## Why

The executed scoring workflow now saves successive evaluations. Its records
need independent verification before downstream analysis; a docking result's
provenance does not describe a standalone rescored pose.

## What was refuted

Running Vina to audit a record, parsing captured molecular bytes locally,
inventing legacy provenance, assuming a score name establishes meaning,
or interpreting internal agreement as chemical or scientific qualification.

## Scope and exclusions

Already loaded pose mappings only. The caller owns IO. No engine, optional
viewer, molecular conversion, geometry replay, generic stage executor,
result comparison, new ranking policy or scientific validation is introduced.

## Acceptance criteria

Durable behavior tests cover native controls, independence, malformed and
missing evidence, byte/semantic/current-score/state contradictions, multiple
evaluations, explicit unit policy and blocked external operations. Preserve
existing result-audit behavior and retain an executed notebook and contract.

## Measured outcome — 2026-10-03

Public `dockingmt.audit_pose(record)` is exported from both root and core APIs.
The implementation shares pose payload/native descriptor checks with
`audit_result`, byte checks with replay, and preparation declarations with
`assess_preparation`. Molecular data is not interpreted here; optional-engine
execution boundaries are unchanged. Fresh-process tests prove the saved-record
route works with Vina, MolSysViewer and RDKit imports blocked.

The guard contains 48 passing cases, including one fresh Vina/Vinardo integration
and a retained two-evaluation control. Contradictions include deleted historical
scores, strict boolean/numeric descriptor differences, tampered input bytes,
known-state mismatch and inconsistent execution/preparation declarations.
Missing fields, unknown states and absent capture stay incomplete. Legacy
scoring records roundtrip unchanged. Finite coordinate edits remain outside
the input-match scope and are explicitly tested and documented.

All 643 tests pass without skips in 126.39 s on Python 3.14.7 in
`molsyssuite@uibcdf_3.14`, with Vina 1.2.7 and the unchanged CI provider source
pins. The 27 existing provider warnings remain visible. Ruff lint/format,
report indexes, diff checks and `pip check` pass. The three code cells of
`devguide/validation/pose_audit.ipynb` execute successfully in that interpreter.
See `devguide/validation/pose_audit.md` for the bounded public contract.
