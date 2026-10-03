---
summary: Execute prepared docking problems one at a time with explicit failure handling.
issue: uibcdf/dockingmt#36
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [execution, identity, validation]
guard: tests/test_batch.py
normative:
blocked_by: []
supersedes: []
---

# Incremental prepared docking

## What

Provide public `dock_many(...)` and a small `DockingOutcome` execution record
for the accepted first block of MVP E2. Reuse `dock` for each prepared problem.

## How

Execute serially as the caller advances an iterator. Snapshot existing problem
and protocol declarations for each consumed item. Preserve result-local pose
IDs, the resolved adapter name on success/failure,
and known molecular identities. Default failures propagate; explicit
`on_error='record'` yields a failure summary and continues. Source failures,
process-control exceptions and memory exhaustion always propagate.

## Why

Consumers need to process modest collections without building an ever-growing
list, losing previous results to one failed item or overloading `DockingResult`
with campaign responsibilities. Input indices identify positions only.

## Ownership and exclusions

Inputs, source iterator and supplied protocol/backend are borrowed; callers keep
them stable while an item executes. No molecular copies or automatic preparation
are introduced. Result ownership is the same as an individual `dock` call.
Returned declarations and error summaries are detached snapshots. No synthetic
run/campaign/state IDs, global ranking, parallel executor or backend-map cache.
The user lifts the MolSysMT/MolSysViewer change restriction after this block.

## Acceptance

Test lazy input consumption, mixed outcomes, preserved identities/settings,
released prior results, cancellation/source failures, admission, prepared-only
handling and offline outcome roundtrips. Compare native seeded Vina/Vinardo
executions with individual calls and their audits. Retain an executed notebook
and bounded contract; run local gates in editable `molsyssuite@uibcdf_3.14`.

## Refuted paths and integration finding

No eager list/prefetch, implicit error suppression, seed derivation, preparation
inside the batch, map cache, global pose renaming or automatic cross-ligand
ranking is introduced. None is justified by this accepted execution slice.

The first full run passed 683 tests and failed the bootstrap import assertion:
it read the shared pytest process after earlier batch controls had legitimately
executed Vina. `tests/test_bootstrap.py::test_no_leaky_optional_imports` now checks
an actual fresh DockingMT import in a subprocess. This preserves the startup
boundary and removes collection-order dependence; it does not unload Vina from
an active scientific session or suppress an actual optional import.

## Measured outcome — 2026-10-03

Public `dock_many(...)` and `DockingOutcome` implement the accepted bounded
execution slice. The 41 new batch/outcome cases cover native Vina/Vinardo
equivalence, native missing-file recovery, lazy consumption, early close,
borrowed source ownership, released previous results and failed frames,
global/item admission, prepared-only enforcement, unit policy, custom export
independence, missing selected engines and offline success/failure roundtrips.
The guard protects the new execution/ownership contracts. The corrected
bootstrap test independently protects startup imports after engine tests.

All 684 tests pass without skips in 128.69 s on Python 3.14.7 and Vina 1.2.7
in editable `molsyssuite@uibcdf_3.14`, using the unchanged CI provider source
pins. The 27 existing provider warnings remain visible. Ruff lint/format,
report-index, diff and `pip check` gates pass. All three code cells of
`devguide/validation/incremental_docking.ipynb` execute with that interpreter.
Two successes and one unsupported-constraint failure stream to JSON Lines and
restore independently; native comparison matches except wall-clock elapsed time.

No MolSysMT/MolSysViewer code was changed for this block. The user's restriction
on subsequent work requiring changes in those providers now expires. Owning
components still retain their scientific/manipulation/rendering responsibilities.
The broader screening gate remains incomplete pending aggregation/comparison
contracts and scientifically qualified workloads; #28 remains partial.
