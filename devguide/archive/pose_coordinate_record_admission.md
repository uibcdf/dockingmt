---
summary: Pose records reject their empty output and leak coordinate field/unit errors.
issue: uibcdf/dockingmt#86
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [core, arguments, serialization, units]
guard: tests/test_pose_record_admission.py
normative:
blocked_by: []
supersedes: []
---

# Pose coordinate record admission

## Delivered correction and source qualification — 2026-11-08

The reader now requires a complete coordinate value/unit mapping and checks the
existing finite-real xyz invariant before constructing the quantity. The
serializer's canonical empty list restores its schema-defined `(0, 3)` shape;
other malformed empty axes still reject. This creates no atoms or coordinate
values and does not qualify a zero-atom scientific/native input.

Missing/malformed fields and invalid unit construction identify `coordinates`
through DMT-E002. A provider exception remains the cause where one was raised;
MemoryError propagates unchanged. PyUnitWizard owns unit parsing/conversion and
the existing constructor retains length/shape admission. Valid numeric/legacy
records, scores, ranks, IDs, metadata, array detachment and caller policy survive.
The same correction applies through result/outcome readers without a new schema
or quantity codec.

The 46 new source cases expose **21 failures / 25 passes** on the old reader.
That complete selection remains FAIL. The complete final source selection
passes **302 cases per policy**, normal and pm/fs with J/mol, zero failures/
errors/skips. It includes original coordinate #63, schema, protocol #84, box #85
and search-domain guards. These are two executions of one software-case
population, not independent molecular observations. The six watched molecular
entry points and optional engine imports remain uncalled. Owned per-profile
pytest caches keep this task's reporter state separate from other sessions.

The [57-member primary evidence](../validation/data/pose_record_admission_2026-11-08/manifest.json)
has SHA-256 `b9ef65d78d650b245be48756f8e09f49ec943d0274534cef4e09945fcd99e65a`,
89,639 stored bytes. Original diagnosis/red/green snapshots, raw JUnit, policies,
producer identities and resource outcomes remain intact. The
[17-member reader/publication companion](../validation/data/pose_record_admission_reader_2026-11-08/manifest.json)
has SHA-256 `9bdcf3398d971f5f9d75b6a4950594c2a78b6bfdce58d7dce6341a7b9ea7c820`,
21,031 stored bytes. Independent stdlib reading authenticates the stored/decoded
members, original failures, source identities, final JUnit and policy/resource
facts without rerunning the tests.

Probe/red/green durations are 1.434/2.769/4.520 s. Final-green sampled peak
group RSS is 102,461,440 bytes, minimum available 58,175,627,264 bytes. CPU 0,
nice 10, one worker, monitored 13 GiB reserve and 1 GiB group-RSS/2 GiB address-
space/45 s CPU/60 s wall bounds cover descendants. All groups are terminal with
no resource interruption; the original red FAIL is a functional outcome. Retain
`.molsyssuite/pose-record-admission-20261108` under #50/review 2026-11-14.

Final local checks cover source/evidence/index/Ruff/resource/reporting contracts;
actual committed-export checks separately verify resource/index/publication and
qualified blob identities. Exact receipts remain in the task. This is source
record qualification, not a new installed wheel, full suite, independent science
or public/platform admission. #28 retains missing exact-head hosted evidence
under the authorized `[skip ci]` route. #19 and the full #73 objective remain
partial; provider artifact/clustering/generation, canvas and native-build holds
remain. No dependency/helper/data/pin, scientific input, build/install or CI change.

## What

At `c1be0466d1f0371461e9715759bd4dee84df3675`, a supported explicitly shaped
empty pose serializes its `(0, 3)` coordinates to `[]`, then its own reader
rejects that generated record. The result reader inherits the failure. Missing
coordinates and invalid unit construction also leak uncoded errors. Six pure
record observations retain these outcomes and a valid positive control.

## How

Interpret the canonical empty wire list as its schema-defined zero-row xyz
shape. Admit complete coordinate mappings, retain scalar/shape/finite invariants
and delegate units to PyUnitWizard. Local diagnostics identify coordinates and
preserve provider causes; resource failures propagate. Keep record detachment,
valid/legacy inputs, IDs/scores/metadata and active caller policy.

## Why

An object admitted by the record model must survive its own serializer/reader
route. This extends #19's saved-record review after #84/#85 and retains #63's
existing shaped-empty constructor contract. Whole functional acceptance is #73.

## What was refuted

Restoring a zero-row array creates no atoms, coordinates or scientific evidence.
It does not admit a zero-atom native docking input. This is not a provider
quantity-codec or molecular reconstruction task.

## Scope and exclusions

Only component-owned pose coordinate records and inherited result/outcome
reading. No schema/output, molecule, engine policy, provider/helper/data pin,
build/install, public artifact or remote CI changes. Native-build and visual
holds, original failed scientific populations and broader goals remain.

## Acceptance criteria

Qualify canonical/shaped empties and nested roundtrips, invalid empty axes,
malformed/missing mappings/units, scalar integrity and unit/resource failure
identity. Keep valid/legacy records, caller arrays and policies intact. Show
original failures and complete affected offline gates under both unit profiles,
retain raw evidence, archive and synchronize after publication checks. No
installed/public/scientific acceptance follows.
