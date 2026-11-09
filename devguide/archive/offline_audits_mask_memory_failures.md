---
summary: Offline record audits translate native memory failures into inconsistent data.
issue: uibcdf/dockingmt#95
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [core, records, diagnostics, resources]
guard: tests/test_audit_resource_errors.py
normative:
blocked_by: []
supersedes: []
---

# Offline audit memory failures

## What

At source `7271667b35f8d95a5c5097a8ee604a45376b97e7`, three broad handlers
translate native MemoryError into ValueError while checking length quantities,
saved scoring protocols and fixed reference energy. The offline audit then
reports inconsistent input rather than a resource interruption. #92's earlier
seven public input corrections retain their distinct source scope.

## How

Inject native resource/process-control and ordinary value failures through
public `audit_pose`/`audit_result` calls, using existing frozen JSON fixtures.
Cover standalone, docking and scored collections where the boundary applies.
Preserve exact exception identity, ordinary malformed-value reports, clean
report digests, unchanged input and caller units. Never exhaust actual memory.

## Why

A caller must distinguish unavailable resources from invalid saved observations.
An internally consistent record cannot become bad data because a reader runs
out of memory. Resource recovery/termination remains the caller's responsibility.

## What was refuted

This is a local translation defect, not a demonstrated unit-provider defect.
No new exception hierarchy, schema, molecular operation or dependency is needed.

## Scope and exclusions

Add explicit MemoryError passthrough at the three confirmed handlers only.
Keep all ordinary diagnostics and original test assertions. No provider refresh,
native compilation, shared install, engine/viewer work or remote CI. Preserve
#256/#558, scientific/public/platform and actual browser/comm/canvas holds.

## Acceptance criteria

Retain the original failures; pass the complete affected offline selection under
normal and pm/fs policies. The existing native scoring test stays explicitly
outside this source scope, with unchanged assertions. Verify source AST changes
are only three passthrough handlers, preserve fixture/support hashes and receive
final local and fresh committed-source resource/publication checks. Keep #19/
#28/#73 partial; #50 owns private custody, review 2026-11-14.

## Delivered and received — 2026-11-09

[Exact source receiving](../validation/audit_resource_errors_2026-11-09.md)
retains the original 15-failure/45-pass guard and passes complete 464-case
normal/pm-fs selections. All 60 public controls verify exact native identity,
ordinary inconsistency reports, unchanged input and clean-report recovery.
One existing actual-native scoring test remains explicitly deselected per
profile, with its assertions unchanged. Independent primary102/reader9 receiving
verifies native/Receptor/hash agreement and that only three passthrough handlers
change executable AST. All fixture/594 support hashes and 67 runtime paths stay
exact. Final local/fresh committed checks and [skip ci] publication retain missing
hosted/public/installed evidence. No provider defect or molecular work follows.

## Subsequent private installed receiving — 2026-11-09

[Separate installed qualification](../validation/record_wheel_editable_2026-11-09.md)
now receives the later behavior from one genuine wheel at producer `841a34d`,
with 1,062 complete offline cases normal then pm/fs and the original explicit
native-test exclusion. Exact payload/source/metadata/import/support checks and
independent primary 130/reader 9 receiving pass. This later receipt does not change
or relabel the original source failures, old wheel, producer or evidence above.
No public/full scientific/platform/canvas/hosted acceptance is inferred.
