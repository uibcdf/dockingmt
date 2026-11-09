# Bounded result restoration profile — 2026-11-08

Owner: [DockingMT #28](../pending_proposals/review_extensibility_and_performance.md).
Execution base: `cadb16b146555faae0e0c87e1221e787797f2306`.
Status: **bounded source profile received; #28 remains partial**. The original
prescription below was registered before execution (comments 6731206101 and
6731422086). Existing export timings and scientific producers retain their
original identities; this measures another operation.

## Question and fixed selection

Does `DockingResult.from_dict` spend material time/memory copying complete pose
records twice, once through its whole-result snapshot and once through each
pose reader? First measure the unchanged runtime. Reuse the existing unshipped
`dmt_test_support.benchmark_result_export._synthetic_result` builder without
changing its helper, data or molecular definitions. These are deterministic
serialization fixtures, not molecular systems or scientific cases.

Start with its mapped 9-pose × 64-atom fixture. After a complete safe pilot,
measure one fixed mapped 64-pose × 256-atom fixture. Each fresh process receives
five uninstrumented restoration samples and separate single cProfile and
tracemalloc calls. Keep the exact worker/helper/case/profile/method bytes and
fixture strict-JSON digest fixed before/after. Require full canonical restored
export equality and source nonmutation; never change a payload to improve timing.
Run one unmeasured restoration warm-up first. Eight restoration calls per cell
are permitted in total. Freeze the builder's ordinary JSON snapshot in the before
cell; after cells receive those same authenticated bytes rather than regenerate
different inputs. The builder and input construction remain outside measurement.

Use normal nm/ps caller policy for comparable timing; final source correctness
receiving must also use pm/fs. Record build/distribution labels separately from
actual mutable source SHA inventories. All scientific/molecular/engine/viewer
operations remain forbidden; no new docking, scoring, RMSD or preparation.

## Measurement and conditional implementation

Elapsed samples time only `DockingResult.from_dict(record)` with perf_counter.
Imports, fixture construction, source hashing, GC between trials, canonical
export/hash and snapshot disposal are excluded. Record every raw sample and
median, process load observations and environment. OS caches remain warm;
background work is uncontrolled on the shared host. No portable speed guarantee.

Tracemalloc records peak Python allocations during one separate restoration,
excluding pre-existing input storage. It is not RSS or a complete memory budget.
The worker owns and stops only its own tracing. A separate cProfile records
function-call counts and cumulative/self time; cumulative values overlap.
The external guard independently records sampled owned-group RSS and headroom.

Only if measured costs justify it, remove the redundant whole-pose traversal
while leaving each pose reader responsible for its own independent snapshot.
Detach all declared result-context fields together so their existing internal
aliases survive. Preserve order, duplicates, inherited factories, NumPy/tuple/set
metadata, nondefault units, schema/member checks before copying, and native
resource exceptions. No cache, schema migration or new public API. Verify with
existing complete affected model/record/audit/snapshot guards and meaningful
ownership regressions, without wall-clock thresholds.

## Resources and stop rule

Serial CPU 0, nice 10, one native/build worker; 13 GiB monitored available-memory
reserve, 1 GiB group RSS, 2 GiB address space, CPU 45/wall 60 seconds per cell.
Estimated pilot peak 256 MiB, fixed medium case 512 MiB. Inspect RAM, CPU/load,
swap and memory pressure first; the earlier Slurm applicability probe remains
inconclusive and no allocation exists. Availability is not a reservation.
Proceed to the fixed medium cell only after a safe pilot and fresh headroom
check. Preserve failures/interruptions and never automatically restart a
headroom stop or increase limits. Stop without optimizing if the evidence does
not justify a change; report the measured limit honestly.

Retain `.molsyssuite/result-restore-20261108` under #28/#50, review 2026-11-14.
Seal original/final producers, input hashes, logs, metrics, exact source/method
and resource outcomes; independently read records without benchmarking again.
Update roadmap/plan/handoff and run applicable source/resource/publication checks
including a fresh committed export. No remote CI or provider polling/building.
Full scientific/installed/public/platform/canvas acceptance remains separate.

## Pre-final compatibility amendment

Registered in #28 comment 6731422086 before final execution. Initial measured
cells and both 570-case source profiles pass, but review identified observable
nested custom copy hooks. Restrict the optimized route to ordinary acyclic JSON
trees without repeated container identities and with known root fields. Rich
Python values, aliases, unknown extensions and custom hooks retain the original
whole-record copy route. Add a nested custom mapping control against the original
reader. Keep the initial candidate records separately; repeat the same frozen
worker, inputs and method for final candidate cells and complete source profiles.

## Executed result and implementation decision

The final reader removes the second traversal of pose records only for ordinary
JSON trees with known root fields. Each pose reader owns its detached snapshot;
related result context is copied together. Other Python payloads retain the
original whole-record route, including aliases, NumPy/tuple/set values, unknown
root extensions, custom mappings and nested copy hooks. Existing schema/axis/
member admission runs first. The complete module AST changes only inside
`DockingResult.from_dict`; no public signature, schema or scientific operation
changes. The existing fixture helper and 594 declared installed-test inputs
(30 helpers/564 data files) remain unchanged.

The initial candidate passed the original eight new ownership controls and 570
complete affected source cases per caller policy. Review then identified a
nested custom mapping whose copy hook appends to its history. Its original
reader control passes nine cases; the initial candidate fails exactly that new
control (one failure/eight passes). Both outcomes are retained. The final
conservative route passes all **571 cases normal, then 571 pm/fs**, including all
nine new controls. No failures/errors/skips; one existing real native execution
case is explicitly deselected per complete source profile. Every original test
assertion remains. This is source qualification, not another molecular case.

Published Pytest Receptor 1.2.2 is authenticated through the existing reviewed
15-file tool prefix, separately from the unchanged shared development runtime.
Native JUnit, Receptor outcomes, source bytes and unit policies agree. The routine
environment's editable Receptor metadata remains 1.2.0; no environment reinstall
or source/runtime substitution is claimed. Two known pre-import assertion-rewrite
warnings occur per complete source cell. Molecular operations are guarded and
no search or optional engine executes.

### Final comparable observations

Each median uses the five raw samples retained in its receipt. Allocation peaks
come from a separate call and exclude pre-existing inputs; do not interpret them
as process RSS. Rows use the exact same frozen input, worker, helper, environment,
units and method before/after. Only the result reader source changes.

| Fixture | Median before → final (ms) | Peak Python allocations before → final (bytes) | Recursive deepcopy calls before → final |
| --- | --- | --- | --- |
| 9 poses × 64 atoms, mapped | 20.151 → 24.188 | 371,576 → 208,301 | 21,781 → 10,950 |
| 64 poses × 256 atoms, mapped | 212.414 → 205.881 | 9,360,360 → 4,118,120 | 596,671 → 298,491 |

Final peak Python allocations fall about **44%/56%** on these two fixed inputs.
The compatibility scan costs time: the small-case median increases about 20%,
while the larger median decreases about 3%. Five samples on a shared host do not
establish a stable speed improvement or uncertainty interval. Accept this bounded
change for lower restoration allocation peaks with preserved extension behavior;
**do not advertise general acceleration**, whole-workflow memory savings or
campaign scalability. Revisit timing only when a concrete workload warrants it.

For transparency, the initial candidate medians were 8.528/140.935 ms with
177,640/4,117,864 peak Python bytes. Those faster numbers belong to the rejected
compatibility candidate, not the delivered reader. No input, producer method or
old observation is changed to obtain a preferred result. The final comparison
is separately named `final-comparison.json` in the primary archive.

Input strict-JSON SHA-256, unchanged for all candidates:

- Small: `54b468a5b36eb3d72acab1af0bfe23099283f627d40ec076428d80ea16e04bb7`.
- Mapped: `cf2c0791424ee4e575429407077abb3222236b5af5ad3ae33d5d3673650ac5b9`.

### Resources and independent record receiving

All six benchmark cells and seven test attempts terminate with no resource
interruption or live owned descendants. The deliberately rejected compatibility
attempt remains FAIL; every other selection passes. Before starting, this host
had about 60 GB available, load about 2 on 20 CPUs and zero memory-pressure
averages. Free resources were never treated as reserved. All cells retain CPU 0,
nice 10, one worker, monitored 13 GiB available reserve, 1 GiB group RSS, 2 GiB
address space and CPU 45/wall 60 second limits. No Slurm allocation or provider
build is started.

Final test cells take 10.545/10.846 s and reach sampled group peaks
186,765,312/187,015,168 RSS bytes. Minimum available memory stays above 58 GB
across the six benchmark cells. Benchmark process RSS includes imports/input and
measurement instrumentation; its separate samples cannot be attributed solely
to the reader's allocations. All raw resource outcomes remain in the archive.

The [278-member primary manifest](data/result_restore_2026-11-08/manifest.json)
is SHA-256
`50ce2d23523be94cc758a44b7e43171dbcbb84173b5087e49d5675e5993c8df3`.
Its immutable inputs, original/final producers, initial and final observations,
complete events/JUnit/logs, source inventories and failed compatibility control
are retained. The [nine-member independent-reader companion](data/result_restore_reader_2026-11-08/manifest.json)
is SHA-256
`611b5e54dc1873cc512520965a2e1014ae7020bdeda6f890bac55304e51ac61d`.
Receiving verifies every stored/decoded digest, exact input/method/environment,
all raw medians, native Receptor/JUnit counts, source scope, AST and unchanged
assertions without importing molecular packages, replaying tests or timing again.

## Checkpoint, limits and next action

Owner remains #28 (partial); retained private resources stay under #28/#50 for
review on **2026-11-14**. The migration directory, shared environment, historical
build interruption and scientific producer identities are preserved. All seven final local
checks pass: Ruff lint/format, report indexes, shared resource and publication
contracts, diff and exact source/archive receiving. Fresh committed-source export
must pass the corresponding six checks before the authorized push; its exact
commit/check receipt is reported in #28 and retained with the private published
checkpoint. This document records the execution base and immutable frozen source
bytes rather than relabeling old producers with the later documentation commit. These checks do not establish installed artifacts,
public dependency closure, Linux/macOS × Python 3.11–3.14 qualification or actual
browser/canvas acceptance. No remote CI was dispatched; current-head hosted
full-suite evidence remains pending under #28 and needs a maintainer-selected
checkpoint. A skip marker is not a passing workflow.

Continue the accepted Core/Extended plan. Respect the maintainer's wait for
MolSysMT #256 and its original lossless-reference gate; #558 still owns panel
maps/history. No provider polling/pull/build, alternate persistence transport or
new scientific run follows from this profile. The next performance increment
needs a concrete workflow and comparable prescribed measurements rather than
another speculative optimization.
