---
summary: Offline audits accept malformed pose identities/ranks or leak array comparison errors.
issue: uibcdf/dockingmt#91
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [records, audit, provenance]
guard: tests/test_audit_pose_identity_records.py
normative: devguide/validation/result_audit.md
blocked_by: []
supersedes: []
---

# Pose identity and rank record admission

## Delivered source correction — 2026-11-08

Both offline auditors now validate current rank/identity declarations with the
existing registered pose argument rules before relational comparisons. Boolean,
floating and array ranks, non-string IDs and malformed historical observations
produce bounded inconsistent reports instead of false agreement or ambiguous
NumPy truth errors. The shared ranking-history validator also refuses malformed
observations during result admission. Unknown optional fields remain unknown;
legitimate NumPy integral ranks and existing string-content admission remain.
No new uniqueness rule, identity inference, reranking or public schema is added.

Typed declarations are carried from the shared pose check into ranking
crosschecks, so valid fields are checked once and malformed fields never reach
unsafe equality. Independent coordinate/score/history checks still run; valid
report contents/digests, ties, order, multiplicity and legacy semantics remain.
The private helper delegates to the existing ArgDigest-owned local value rules;
no provider implementation or registered rule is copied or changed.

The corrected original guard has **70 failures/33 passes**, retained FAIL.
Final complete affected gates pass **562 cases per normal/pm-fs policy**, no
failures/errors/skips, one explicitly deselected native execution case. These
include all 103 new guard cases and existing model, audit, record, ranking,
coordinate, scoring-reference, snapshot and serialization guards. Identical
final source/test bytes pass normal before pm/fs. An earlier 562-pass normal
candidate is retained separately; the final refinement carries already-validated
declarations forward instead of digesting the same field again. No test or
assertion is removed. The initial 73-failure/30-pass fixture-control population
also remains; independent AST inspection verifies all original assertions.

The [160-member primary archive](../validation/data/audit_pose_identity_admission_2026-11-08/manifest.json)
is SHA-256 `6a268c8f910abd829d36a7c828d01b7bdf32af2b088cd8e5b803247e9ceca3f7`
(565,961 stored / 4,529,029 decoded bytes). It preserves the eight-control probe,
all original/corrected failures and full Receptor overflow reports, initial/
final runtime/tests, frozen prescriptions/registrations, native JUnit, complete
published Receptor events, caller policy and resource outcomes. Existing
historical molecular/software fixture bytes and producers remain unchanged.

Independent supported Receptor/JUnit/source receiving passes in 0.612 s /
40,255,488 sampled group RSS bytes, with no test replay or molecular imports.
The [nine-member reader companion](../validation/data/audit_pose_identity_admission_reader_2026-11-08/manifest.json)
is SHA-256 `167350f87344f5b85bf6a83072ae688ca7e96918ccc36e1728df047b6e4180be`
(13,210 stored / 40,068 decoded bytes). It retains the exact reader/controller,
registration, source/event/JUnit verification and terminal resource outcome.

Final normal/pm-fs cells take 11.152/10.741 s, both peak at 186,978,304 sampled
group RSS bytes, with minimum available RAM 59,690,909,696/59,717,664,768 bytes.
Every owned group is terminal without interruption, CPU 0/nice 10/one worker,
monitored 13 GiB reserve, 1 GiB group RSS, 2 GiB address space, CPU 45/wall 60 s.
Preflight observes load about 1.65 on 20 logical CPUs, over 60 GB available RAM,
zero sampled memory pressure and no Slurm allocation. Availability is not a
reservation; no old interrupted task is restarted. Two expected Receptor
assertion-rewrite warnings per passing process are preserved.

Execution base is `d3fc5dc2db8c858a5ad8df38980c0a338184784e` plus the exact
frozen source/test changes, separate from stale installed/build labels. The
published 15-file Receptor 1.2.2 tool prefix is authenticated independently.
The 30-helper/564-data declaration, pins and shared/sibling environments remain
unchanged. Retain the private identity-admission task under #50/review 2026-11-14,
including failures and exact tool/evidence dependencies; preserve the untracked
migration and old build holds. No molecular operation or engine executes.

This closes #91's source defect only. Final source/documentation/resource checks
and fresh committed-export outcomes retain separate receipts in #91. No remote
CI is dispatched; use `[skip ci]` and retain missing exact-head evidence under
#28. Scientific, public/installed/platform, E3 persistence and actual canvas
remain separate. The maintainer requests continued waiting for MolSysMT #256;
no provider poll, pull/build or alternate transport is introduced.

## What

At execution base `d3fc5dc2db8c858a5ad8df38980c0a338184784e`, the offline audit
accepts Boolean/floating ranks and integer pose IDs that the public pose reader
refuses. Coordinating malformed IDs with ranking observations does not make
the types valid. Historical ranks/IDs are not typed before comparison; arrays
can raise ValueError instead of producing an inconsistent report.

## How

An eight-control probe observes seven failures and a legitimate NumPy-integral
rank control, with source preservation and zero molecular operations. Register
the durable guard before runtime changes and retain the original complete red
pytest/Receptor/JUnit outcome. Reuse the existing registered rank/ID digesters
through one private schema helper for current declarations and history records.
Add bounded malformed-field diagnostics and avoid relational comparisons on
invalid identities. Preserve valid report contents and unrelated checks.

## Why

The initial red selection has 73 failures/30 passes, no errors/skips. Preserve
that FAIL population and its full Receptor overflow report. Three failures are
test setup mistakes: two scored fixtures have optional rank=None, which cannot
be passed to NumPy's integer constructor; the historical fixture also has an
extra documentary root field outside the reader's structured export. Register
a fresh red guard on unchanged runtime: explicitly declare rank 1 before the
NumPy-equivalence comparison, and obtain the history control through the public
result reader before modifying it. No assertion or invalid case is removed.
Existing optional ID digesters admit any string, including empty/blank content;
preserve that contract instead of imposing a new nonempty-string requirement.
Existing scoring-state semantic checks retain their own stricter scope.

Offline inspection must not turn malformed scientific identity/ranking claims
into internally consistent evidence or raise ambiguous NumPy truth-value errors.
Existing class admission already defines the scalar contract; no new identity
model or public API is needed.

## What was refuted

No ArgDigest, SMonitor, molecular correspondence or ranking-geometry provider
defect is established. NumPy integral ranks are valid and remain supported.
Unknown optional IDs/ranks, repeated poses and legacy history do not acquire
invented identities, uniqueness requirements or new mandatory evidence.

## Scope and exclusions

Standalone, docking and scored-collection identity/rank fields, plus recorded
ranking observations. Keep order/ties/multiplicity, native and legacy valid audit
digests, missing evidence, schema priority, nonmutation and resource-error
identity. No molecular operation, record migration, helper/data/pin change,
native build, environment repair or remote CI. The maintainer asks to wait for
MolSysMT #256; this work neither polls it nor replaces its H5MSM gate.

## Acceptance criteria

The original guard must fail and the corrected runtime must pass the complete
affected model/record/audit/ranking selection normal then pm/fs, with identical
final source/test bytes. Preserve invalid scalars/arrays, valid NumPy ranks,
unknown IDs, coordinated false claims, history refusal, field-specific paths,
native resource-error identity and every original valid assertion/digest.
Use authenticated published Pytest Receptor 1.2.2 and native JUnit; independently
receive the records without test/molecular replay.

Run serial CPU 0/nice 10/one worker, monitored 13 GiB available reserve, 1 GiB
group RSS, 2 GiB address space, 45 CPU/60 wall seconds. Estimated record-test
peak is 256 MiB. Preserve interruptions without automatic heavy restart. Task
custody: `.molsyssuite/audit-identity-admission-20261108`, #50/review 2026-11-14.
Update contracts, roadmap/plan/handoff, archive the resolved record, regenerate
indexes and synchronize #91. Run Ruff/resource/publication and fresh committed
export checks. Source qualification does not accept installed/scientific/public/
platform/canvas or the full objective; commit with `[skip ci]`.
