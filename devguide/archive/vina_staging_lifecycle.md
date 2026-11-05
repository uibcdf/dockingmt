---
summary: Track allocated Vina inputs before writes and report failed cleanup without masking primary errors.
issue: uibcdf/dockingmt#71
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [engines, diagnostics]
guard: tests/test_vina_staging_lifecycle.py
normative:
blocked_by: []
supersedes: []
---

# Vina staging file lifecycle

## What

At `4873a738bb5a4a40a079efd4cfe6ff38e14dc88a`, binary staging and
both receptor text branches register a temporary path after writing and closing.
An earlier I/O error leaves the allocated file outside the cleanup list.
Cleanup also silently discards removal errors.

## How

Inject write, flush, close and removal failures using owned test files. Register
ownership immediately after allocation. Attempt every removal, tolerate an already
absent path, and report other failures through a DockingMT SMonitor catalog entry.
When a primary exception exists, attach its cleanup diagnostic as an exception
note, preserving the same exception even with warnings promoted to errors.

## Why

An operation can otherwise leave temporary backend inputs without giving its
caller a way to discover the failed disposal. This is a concrete finding in the
local operational review #50; its broader inventory and central handoff remain open.

## What was refuted

Molecular export or preparation changes are unnecessary. The defect concerns
custody of the adapter's existing serialized inputs. Caller-owned paths must
never enter the removal list.

## Scope and exclusions

Only Vina staging and its existing dock/score finally blocks are covered. No
native experiment, provider change, release, general resource framework or
cleanup of existing scientific/shared resources is authorized by this fix.

## Acceptance criteria

Controlled failure guards reproduce the defect and pass after correction; exact
staged bytes and caller files are preserved. All owned paths are attempted,
cleanup failures are visible, original exceptions survive, and caller warning
policy is preserved. Run focused runtime/catalog tests, local quality gates and
the shared final-source publication/resource validators.

## Verification — 2026-11-05

The initial 14-case guard run reproduces 12 failures and two passing controls:
nine allocated paths miss registration on injected write/flush/close failure;
two removal-warning guards fail; the primary-error cleanup guard also shows the
old existence precheck bypassing the absent-path removal attempt. Its `finally`
retires controlled leftovers even in the failing reproduction.

After repair, all 19 lifecycle cases pass. Both dock and score finally blocks
retain the same primary exception when cleanup fails under warnings-as-errors.
The primary error is passed explicitly: an unrelated exception already handled
by the caller must not acquire the diagnostic or suppress the cleanup warning.
Missing files are harmless; all other failures are aggregated after every owned
path is attempted. Normal completion emits `DMT-W003` through the existing
SMonitor bundle, respecting caller warning filters; an operation failure receives
a catalog-rendered note with that code and the retained paths. No global warning
policy is changed. Exact binary contents and caller-owned inputs are guarded.

The selected lifecycle, support-contract, scoring, workflow-profiling,
backend-contract and reporting modules pass **129 tests** on routine Python
3.14.7 with isolated published Pytest Receptor 1.2.2. Catalog profile rendering,
exception/warning reconstruction, pickle/deepcopy and structured failure fields
pass. Existing deterministic native stand-ins and fixed-pose regression fixtures
are reused; no new scientific experiment or molecular preparation is introduced.
The updated administrative selection separately passes **38 tests**, including
#72, with its published Pytest Receptor 1.2.1 profile. The runtime profile uses
development SMonitor `0.22.0+16.gccdcace`, ArgDigest `0.17.0+5.gcd9c4f3` and
DepDigest `0.15.1+8.g0884f0c`; these are source checks, not public-provider or
installed-package qualification.

Repository Ruff and report-index checks pass. Final workspace and fresh committed
export publication/resource checks and exact source identities are handed off in
the owning issue. Molecular serialization, backend input bytes, source mapping,
scores and search algorithms remain outside this correction. #50's broader
inventory and deferred central handoff remain open; sibling issue work and live
visual acceptance remain deferred.
