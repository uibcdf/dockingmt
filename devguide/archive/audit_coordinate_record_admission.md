---
summary: Offline coordinate audits disagree with the existing pose-record admission.
issue: uibcdf/dockingmt#90
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [records, audit, quantities]
guard: tests/test_audit_coordinate_records.py
normative: devguide/validation/result_audit.md
blocked_by: []
supersedes: []
---

# Offline coordinate-record admission

## Delivered source correction — 2026-11-08

Offline audits now share the existing pose-record xyz admission before quantity
conversion. Mixed Booleans and complex values remain malformed instead of losing
their type/imaginary part; canonical zero-row `[]` coordinates are valid with
explicit length units. Missing evidence stays incomplete and malformed units/
shapes stay inconsistent. The pose reader retains its admitted values, schema
priority and public signature. No physical unit, coordinate, state or producer
is inferred or rewritten. A shared private helper removes the divergent path.

The complete affected selection passes **409 cases per normal/pm-fs policy**,
zero failures/errors/skips, one explicitly deselected native execution case.
It includes all 41 new guard cases and the existing standalone/scored-collection/
result audit, scoring-reference, result/pose record, snapshot and serialization
guards. Original valid/native report digests and reader behavior remain. The
native test remains present with identical assertions; moving only its fixture
constant import into that test lets offline cases collect without Vina. The
independent reader verifies that complete test AST equivalence after relocation.

The corrected original guard remains FAIL with 13 failures/28 passes. Earlier
16-failure/25-pass guard, probe setup failure and first green collection failure
are retained separately. No failed selection is promoted or native gate waived.
Final identical runtime/test bytes pass normal then pm/fs; caller policy is
preserved, molecular operations are guarded and remain zero. Two expected
Receptor assertion-rewrite warnings per passing process are retained.

The [148-member primary archive](../validation/data/audit_coordinate_admission_2026-11-08/manifest.json)
is SHA-256 `fc210deb387b6323a3953b64c074b8a530e410fae71a8741021e9dfb5cfeddff`
(437,043 stored / 2,821,998 decoded bytes). It preserves original/final runtime
and tests, frozen prescriptions, all probes/failed selections, registrations,
raw logs, full published Receptor streams, native JUnit and resource outcomes.
The [nine-member reader companion](../validation/data/audit_coordinate_admission_reader_2026-11-08/manifest.json)
is `05ec7bfe41306b694df7d0ccae8a6363830a48b4bc1a538df8d808b96c85fd17`
(13,149 / 40,139 bytes). Supported `read_artifact` receiving verifies all counts,
whole selection/failure classifications, JUnit, final source/test agreement and
unchanged assertions, without replaying tests or importing molecular providers.

Final cells take 7.263 / 10.860 s, sampled group RSS 136,462,336 / 136,716,288
bytes and minimum available RAM 58,559,778,816 / 57,451,454,464 bytes. The reader
takes 0.306 s / 34,787,328 bytes. CPU 0/nice 10/one worker, monitored 13 GiB
available reserve, 1 GiB group RSS, 2 GiB address space and 45 CPU/60 wall seconds;
all owned groups terminate without resource interruption. Preflight load was
about 9.94 on 20 logical CPUs, over 56 GB available RAM, zero sampled memory
pressure and no Slurm allocation; availability is not a reservation. No heavy
restart, environment modification or provider pull/build occurs.

Execution base is `a6e636902af26fc624eb5ff60c782a75a95732b7` plus the exact
frozen changes; installed/build labels are not live source fingerprints. The
published 15-file Pytest Receptor 1.2.2 tool prefix has separate authenticated
custody. The unchanged 30-helper/564-data declaration, historical fixtures,
original E4/E3/scientific populations and dependency pins stay intact. Retain
private task records under #50/review 2026-11-14 and the untracked migration.

This resolves #90's source defect. Seven applicable workspace checks pass: Ruff/format,
report indexes, source resources/publication, whitespace and exact archive/source
scope. Fresh committed-export outcomes are recorded after the commit in #90;
workspace checks do not substitute for them. #28 hosted exact-head, installed/
public/platform, full science, E3/#256/#558 and #52/#60 canvas remain separate.
No remote CI is dispatched; routine publication uses `[skip ci]`.

## What

At execution base `a6e636902af26fc624eb5ff60c782a75a95732b7`, an audit of the
minimal saved software result incorrectly accepts a mixed Boolean coordinate.
The existing pose reader rejects it. A canonical empty `DockingPose.to_dict()`
coordinate value `[]` roundtrips through that reader, but the standalone audit
incorrectly marks it inconsistent. These are record-boundary defects; no new
molecular measurement is involved.

## How

A nine-control record-only probe observes both defects and seven already
inconsistent malformed controls. It preserves inputs and makes zero molecular
calls. An earlier probe setup fails before observations because the task guard
forbids the package's required MolSysMT import; retain that failure separately.
The corrected probe permits ordinary imports and forbids actual molecular calls.

The initial durable guard records 16 failures/25 passes, no errors/skips. Nine
failures corroborate Boolean/complex coercion through all three audit routes;
four corroborate canonical-empty rejection. Three others expose a test setup
mistake: its deliberately malformed-unit collection omitted the required root
provenance container, so the audit correctly stopped as incomplete before pose
inspection. Preserve that complete FAIL population. Register a corrected red
selection with the empty provenance mapping present, retaining every assertion
and malformed-unit case, before changing runtime. The imaginary component is
also silently discarded by the old conversion, with three ComplexWarnings.

Register the new durable guard before changing runtime. Run it against the
original runtime and retain the complete red pytest/Receptor/JUnit evidence.
Extract the existing xyz-record scalar/shape admission from `DockingPose.from_dict`
into a shared private helper; use it in the offline audit before unit conversion.
Do not change the reader's admitted values, root/nested schema priority, explicit
unit policy or public signature. Empty xyz width is fixed by this existing schema.

## Why

The corrected red guard has 13 failures/28 passes, no errors/skips, on the
unchanged original runtime. A first green candidate stops during collection:
the pose-audit module imports native-engine test constants at module scope,
transitively importing Vina before its explicitly deselected native test. Keep
that collection failure and its frozen unqualified candidate. Move only that
constant import inside the native test; retain all test functions/assertions
and the exact native-test deselection. Review also corrects the first helper
extraction's object-array shadowing before successful execution. The new
candidate preserves the reader's original numerical input separately from its
object-typed scalar inspection. Register fresh whole source gates; do not
accept the first green candidate or reinterpret its collection error as tests.

The report must distinguish a valid empty coordinate snapshot from absent
evidence, and reject malformed recorded numbers before conversion hides their
types. Users need the reader and offline audit to agree on the same schema.

## What was refuted

Seven other malformed magnitude/context probe controls are already inconsistent;
they do not establish extra product failures. No PyUnitWizard, ArgDigest,
SMonitor or molecular-provider implementation defect is established. No general
quantity codec, molecular geometry or source normalization belongs in this fix.

## Scope and exclusions

Standalone, docking and scored-collection coordinate records only. Preserve
canonical valid audit digests, unrelated missing/inconsistent evidence, exact
producer identities, source nonmutation, report isolation, resource exceptions,
all previous tests and historical inputs. Do not drop contradictory fields,
recompute chemistry, migrate records or change helpers/data/pins. MolSysMT #256
is being worked on according to the maintainer; no polling/build/transport work.

## Acceptance criteria

The new Boolean and canonical-empty guards fail on the original runtime, then
pass through all applicable public audit paths. Retain numeric-string/complex/
nonfinite/wrong-shape and invalid/missing-unit refusals, plus valid units and
resource-error identity. Run the complete affected record/audit/serialization
selection normal then pm/fs with identical final source/test bytes and native
pytest completion. Use the published authenticated Pytest Receptor 1.2.2 tool
prefix without changing the shared environment.

Run serial CPU 0/nice 10/one native worker, monitored 13 GiB available reserve,
1 GiB group RSS, 2 GiB address space, 45 CPU/60 wall seconds. Estimate 256 MiB
for record tests; stop/preserve an interruption, never restart heavy work
automatically. Retain task `.molsyssuite/audit-length-admission-20261108` under
#50, review 2026-11-14. Update contracts/roadmap/plan/handoff, regenerate indexes,
run Ruff and applicable resource/publication checks including fresh committed
export, archive this record and synchronize #90. No remote CI or full scientific/
installed/public/canvas/objective acceptance follows.
