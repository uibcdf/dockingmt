---
summary: Complete the local resource disposition and retain the deferred central handoff.
issue: uibcdf/dockingmt#50
status: partial
opened: 2026-11-05
closed:
verification: inspected
area: [tooling, governance, evidence]
guard: tests/test_vina_staging_lifecycle.py
normative: https://github.com/uibcdf/molsyssuite/blob/main/devguide/temporary_resources.md
blocked_by: []
supersedes: []
---

# Temporary-resource review — 2026-11-05

## Source 0.1.0 closeout custody — 2026-11-11

Keep `.molsyssuite/current-0.1.0-puw-receiving-20261111` under #74/#50 until the
2026-11-14 review: original API-digest-verified artifact ZIPs, decoded provider
wheels/receipts and JSONL/JUnit, original failed attempts, bounded reader/
source-export records and the published-reporter dependency. Four installed
cells and every owned local reader are terminal; no local resource interruption
or native-build restart occurs. The tag-specific read-only conformance run is
separately tracked under #74. Managed source exports are retired. Preserve the
human migration backup, shared environments and historical native holds.
Retirement requires verified receipt/owner/dependency references; source-event
publication alone does not authorize deleting the original qualification bytes.

## CI/private installed custody increment — 2026-11-09

Retain `.molsyssuite/ci-alignment-20261109` and
`.molsyssuite/record-wheel-inputs-20261109` under #100/#101/#47/#30/#50,
review 2026-11-14. Preserve the original 157,431-byte wheel/source producer 9a40e385,
actual private receiver, original/qualification-only descriptors/tests/helpers,
594-to595 exact support relation, every failed collection/context/reader and
intermediate/final test outcome. Independent415/25-member records pass without
replay; all owned groups terminate without resource interruption. No shared
install, provider/native build, new scientific work or Git-origin rewrite. Keep
old artifacts/helpers/input producers, human migration and shared environments;
cleanup remains subject to exact owner/dependency checks and central deferrals.

## Declaration/source custody increment — 2026-11-09

Retain `.molsyssuite/plan-push-20261109` under #97/#98/#99/#47/#50, review 2026-11-14:
original 61-failure population, collection error, three-failure ownership refinement,
intermediate 518-case and final 521-case profiles, initial/final seals and readers,
ten normalized registry documents, original/final source and published test-only
prefix identities. All owned groups terminate without interruption. The local
controller syntax failure is preserved before any worker/replay. No shared
install, native build, search, environment removal or automatic retry occurs.
Old wheels/helpers/data/migration/scientific producers and central deferrals remain.

## Pose identity/rank audit custody increment — 2026-11-08

Retain [#91's task and original/final source records](../archive/audit_pose_identity_admission.md),
owners #91/#50, review 2026-11-14. Initial red 73-failure and corrected 70-failure
populations stay failed; the first and final 562-pass normal candidates retain
separate source identities, with complete final pm/fs and independent reading.
All owned groups are terminal without interruption. Preserve full Receptor
overflow reports, event/JUnit/source/AST evidence and the separate published
15-file tool dependency before any verified owner cache-disposal decision.

The 160-member primary manifest is SHA-256
`6a268c8f910abd829d36a7c828d01b7bdf32af2b088cd8e5b803247e9ceca3f7`;
the nine-member reader companion is
`167350f87344f5b85bf6a83072ae688ca7e96918ccc36e1728df047b6e4180be`.
Independent reading replays no test/molecular operation. Shared/sibling work,
original migration, old build interruptions and central-handoff deferral remain
unchanged. No provider polling/building or remote CI is started.

## Offline coordinate audit custody increment — 2026-11-08

Retain [#90's source receiving](../archive/audit_coordinate_record_admission.md)
task, owned by #90/#50, review 2026-11-14. It contains the initial probe setup
failure, original/corrected red populations, first green collection failure,
two complete 409-pass unit-policy selections and reader/admin records. All
owned groups are terminal without resource interruption. Preserve original
failures and exact source/test/tool dependencies; the published 15-file Receptor
prefix remains separate from the shared environment. No molecular/native
execution, provider build/pull or environment repair occurs.

The 148-member primary manifest is SHA-256
`fc210deb387b6323a3953b64c074b8a530e410fae71a8741021e9dfb5cfeddff`;
the nine-member reader companion is
`05ec7bfe41306b694df7d0ccae8a6363830a48b4bc1a538df8d808b96c85fd17`.
The independent reader verifies original/final classifications, native JUnit,
published Receptor events and test AST custody without test/molecular replay.
Cache disposal awaits exact dependency/owner checks. No original migration,
shared/sibling work, old interrupted build or central-handoff disposition changes.

## Editable E4 integration custody increment — 2026-11-08

Retain the three task contexts for
[complete editable View receiving](../validation/e4_view_editable_2026-11-08.md),
owned by #80/#60/#50, review 2026-11-14. Two zero-operation setup campaigns stay
failed; the third completes all eight normal/pm-fs cells. Its first independent
reader stays failed and the prospectively amended second reader passes. All
owned groups are terminal without resource interruption. Original molecular
inputs are authenticated by reference, with no duplicate search/detector run,
native build or shared-environment modification.

The 351-member primary archive is SHA-256
`87bf805d6dd1ba2f6ed9075043c1e09f655d1d7d10be9e10e8b0a594905e57ca`;
the 17-member reader companion is
`3436ee960ffcc0fe6665c8ad52503b1306272b2aa5f0d105f4178cd91096e58e`.
Keep the original task producers/failures, native/session/JUnit witnesses,
source/data/import custody and exact published test-tool prefix until their
independent archive/consumer dependencies and owner disposition are verified.
Private task/cache removal needs that exact dependency check; none is removed
here. Preserve the original untracked migration, older interrupted native build,
shared/sibling work and existing central-handoff deferral. The maintainer reports
MolSysMT #256 is being worked on; no polling/building or automatic restart occurs.

## What

The local review requested in #50 is complete for the operation classes and
explicit task contexts below. This is a custody/disposition checkpoint, not a
host-wide inventory or a new scientific/package qualification. The issue stays
partial because the handoff to MolSysSuite #104 is deferred by the maintainer.
No issue, comment, implementation or adoption state in another repository is
changed by this review.

The existing common policy is inspected read-only at MolSysSuite
`b9852d973e96613a68cab7278491ff647bfd0b7d`,
[`devguide/temporary_resources.md`](https://github.com/uibcdf/molsyssuite/blob/b9852d973e96613a68cab7278491ff647bfd0b7d/devguide/temporary_resources.md),
document SHA-256
`d1a38cd1feca561631a625e3c97651bbd4b3a49984145588c42ad13afe428cc5`.
The local policy file is clean. No new policy, reusable tool or provider
adoption is introduced.

Inspected source is `837de4b82c67189a3ef1b43fe938d238b8bd9d02`. The preceding
[#71 lifecycle repair](../archive/vina_staging_lifecycle.md) and
[#72 guard correction](../archive/restore_export_resource_guards.md) resolve the
two concrete implementation defects found during this review. Their original
failure evidence and executed checks retain their own source identity.

## How

### Later source-milestone execution checkpoint — 2026-11-05

The new #74 lower-minor contexts have a separate bounded custody ledger; they
are not added retroactively to the frozen inventory below. After the maintainer
requested shared-workstation headroom, the owned parallel 3.11/3.13 tests were
stopped and 3.12 completed with one logical CPU and low priority. A guarded
serial 3.11 retry then reached its RAM reserve and was stopped; 3.13 was not
restarted. No test, controller or watcher remains active, and no heavy restart
is automatic. Interrupted progress does not qualify a passing gate.

Local heavy work now uses serial cells, one logical CPU, low priority, limited
native/build workers and monitored RAM headroom, as recorded in root
[AGENTS.md](../../AGENTS.md#local-gates). The inactive 3.11/3.13 preparations are
held for complete runs only when stable capacity exists. The completed 3.12
prefix is held for low-priority retirement after receipt handoff, with review
on 2026-11-12; avoiding cleanup I/O under current shared load is deliberate.
Exact wheels and interrupted/completed diagnostics remain through the first-tag
decision. No shared environment or pre-existing resource is removed. The
[source dossier](../releases/0.1.0.md) and separate minor receipt preserve the
actual outcomes. This local checkpoint does not perform the deferred central
handoff.

### Later collection-audit checkpoint — 2026-11-05

[#76](../archive/audit_result_scoring_stages.md) adds a separate small custody
context for record-only tests and a private borrowing-wheel receiving. An
initial full source export reached local disk quota before build/environment
creation; only its owned partial archive was retired. The replacement materializes
only the committed runtime package, two test modules and two saved JSON fixtures.
No original record, qualified receiver, shared environment or cache is purged.
Source and installed controls run serially on one logical CPU at low priority;
the installed run monitors RAM reserve and finishes without interruption.

The new runtime wheel, source/input hashes, test/receiving receipts, warning and
resource diagnostic stay available through review on 2026-11-12. Its owned
minimal build/source, harness, borrowing environment and test scratch are retired
after receiving. The original 0.1.0 base consumer retains all 63 runtime files,
version and archive metadata. Final committed-source governance uses a fresh
tracked file tree sharing verified committed file bytes to avoid another large
copy; only read-only checks execute there, with before/after Git-blob verification.
This bounded resource adaptation is neither independent copied-byte reproduction
nor a replacement installed/scientific gate. No local test/controller/watcher
remains active after handoff, and no heavy restart is scheduled. Central reporting
and unrelated resource dispositions remain deferred/unchanged.

### Installed collection-example checkpoint — 2026-11-06

[#77](../archive/inspect_saved_scoring_collections.md) reuses the exact #76 wheel
in a new small borrowing installation of the retained Python 3.12 dependency
base. Thirteen standalone-example invocations, including the old-example
comparator and a separate intentional source-overlay child, finish serially on
one logical CPU at low priority with native threads limited and RAM reserve
monitored. No molecular/native/ranking/viewer operation or heavy suite runs.
Metadata/pip checks pass, and original base consumer bytes/metadata remain intact.

Owned venv and disposable example/input/runtime copies are retired after receipt
handoff; unique outputs, input hashes/derivations, launcher and resource diagnostic
are held through review on 2026-11-12. The reused wheel, original scientific
fixtures and qualified base retain their prior custody. Final committed-source
governance again uses a fresh tracked tree with shared verified committed bytes,
read-only checks and before/after blob verification, then retires that tree.
This is a resource adaptation, not independent copied-byte reproduction or a
full installed gate. No test/controller/watcher or heavy retry remains active
at handoff. The wider central handoff and existing historical holds stay deferred.

### Pre-stabilization reference-evidence context — 2026-11-06

#73/#78 own a new bounded context for the initial 155 source/106 installed
checks and the refined 157 source/108 installed checks. A minimal package/test/data
export and small borrowing venv avoid duplicating a whole scientific corpus or
dependency solve. Source
work uses the routine 3.14 interpreter; a task-local copy of unchanged published
Receptor 1.2.2 files, verified against the retained Conda record, supplies the
required test tool without changing the development environment. Initial guard
failure and exploratory development-tool evidence remain separate diagnostics.

Local runs use one logical CPU, low priority, one native/build worker and a
monitored RAM reserve. The pytest adapter controls substitute the engine; existing
MolSysMT geometry reads stay provider-owned. A separately prescribed installed
control performs exactly two fixed-score calls on the original overlapping
inputs, without search/optimization/new preparation/repair/ranking/viewer work.
The later type refinement receives that producer unchanged, without additional
native calls. There is no independent campaign, heavy restart or resource
interruption. The original base consumer and prior artifacts remain intact.

Retire owned package/build/harness/venv/test and committed-tree scratch after
handoff. Keep both exact new wheels, source/input/tool hashes, launchers and unique
diagnostics through review on 2026-11-13. Final committed-source governance uses
the verified shared-byte tracked-tree materialization, then retires it. No global
cache, source worktree or qualified shared resource is purged. Other historical
holds and the broader central handoff retain their own state.

### Original operation review

Review actual allocation, output, subprocess and cleanup paths in the Vina
adapter, addon, developer helpers, frontend tests and publication wrappers.
Compare the existing #50 custody history with explicit current task locations,
their metadata, declared receiver dependencies and registered Git worktrees.
Discovery by a name is not ownership or permission to remove it.

The ignored local custody ledger records **38 task directories, six operational
files and six pre-existing ignored task/tool contexts**, with 30 local ownership
or closeout metadata records fingerprinted. It also records generated checkout
classes, shared development/SDK dependencies and one absent registered worktree.
Its exact-path/process details stay local. Snapshot SHA-256:
`6e723925a5a1f4410d87da5f6593e00761d3b975eebf29dad6d648782b9721b4`.
This snapshot excludes this review's own new ledger and disposable scratch.

The observation does not rehash every installed payload or establish new
compatibility. Earlier complete receiver inventories retain their original
receipts. Current inspection does not substitute for those executed checks.

## Reviewed operations and dispositions

| Operation / resource | Ownership and purpose | Disposition and release condition | Evidence / boundary |
| --- | --- | --- | --- |
| Vina staging for `dock` and `score` | DockingMT backend owns only newly allocated input copies. Caller input paths remain caller-owned. | Attempt every owned removal on success/failure; missing files are harmless. Retained paths are reported; the same primary error survives. | `engines/vina.py`, `engines/_vina_scoring.py`; #71's 19 controlled lifecycle cases. No molecular export change. |
| Addon shapes, state and DOM fixtures | Addon owns its registered domain handles; MolSysViewer owns molecular scene/render/comm resources. The DOM test owns its emulated windows. | `clear_docking` removes owned shapes and releases binding; failed deletion preserves remaining handles for retry. DOM teardown closes its windows in `finally`. | `molsysviewer_dockingmt/adapters/complex.py`, `tests/test_viewer_state.py`, `devtools/frontend/panels.test.mjs`. This neither closes caller scene data nor certifies a live canvas. |
| Profile/replay and preparation qualification scratch | Each helper owns its managed temporary input/output directory; report/input destinations belong to the caller or declared case. | Existing `TemporaryDirectory` scopes dispose scratch on success/failure. Persistent reports remain outside that scope for their declared evidence use. | `profile_workflow.py`, `replay_1iep_pdbqt.py`, `qualify_named_types.py`, `qualify_chemical_templates.py`, `qualify_3ptb_admission.py`, and `devtools/qualify_named_charges.py`. Source inspection only; no rerun of their molecular/native operations. |
| Export memory profiling | Benchmark owns tracing only when it starts tracing. | Stop owned tracing on success/failure; preserve an already active caller tracer. | #48 mechanism, #72's five restored isolated child guards. No benchmark population rerun. |
| Saved-case recovery report | Recovery writer owns only a newly created report, never an existing output. | Exclusive creation protects existing files; a failed new write removes the partial file or exposes its cleanup failure. | `recover_saved_3ptb_case.py::_write_report` and its existing failed-write guard. No general molecular serialization or reconstruction is added. |
| Administrative tests and installed-test support | Each test owns its managed fixture/child; the shared installed-support mechanism owns its declared staging. | Test/child contexts finish and dispose managed scratch. Support is unshipped; retain exact fixtures and original failed/corrected receiving evidence. | Distribution/support/resource guard modules; [installed support receiving](../validation/installed_support_receiving.md). No new installer, test framework or environment is introduced. |
| Documentation, notebooks, HTML and scientific records | Owning case issues retain originals, producers, package identities, executed notebooks and both positive/adverse observations. | Retain for reproducibility, deferred visual observation or admission. Remove only an explicitly redundant working copy after preserving its unique evidence and checking dependencies. | [Evidence policy](../validation/evidence_publication_policy.md), #4/#33, #52/#60 and #62. This review launches no kernel/server and reruns no experiment or HTML export. |
| Private wheels, receivers and source/build contexts | #47/#49/#56 and originating case issues own exact artifacts, molecular lineage, dependency SDKs and installed compatibility diagnostics. | Retain originals and dependent receivers until covering receiving/admission and an owner-reviewed archival/disposal decision. A finished task does not authorize deleting a reused environment. | Existing artifact/closeout records; [public readiness](../validation/public_candidate_readiness.md), [public Viewer failure](../validation/public_viewer_receiving.md), [prepared recovery](../validation/prepared_recovery.md). No package build/install or provider mutation. |
| Hosted CI/publication workspaces and artifacts | Existing jobs and immutable shared publisher own their runner workspaces, caches and exact candidate/coverage receipts. | Preserve run/attempt/artifact identity and service retention. No local deletion claim is inferred from an ephemeral runner or a shared workflow reference. | Existing CI, DOM, source/dependency and shared `95f693be...` publisher/installed wrappers; #21/#28/#30/#47. No workflow dispatch, upload, promotion, cache purge or credentials operation. |
| Editable checkout metadata, caches and legacy build output | Routine development owns editable metadata, generated version and tool caches. Historical build/output attribution requires exact owner review. | Keep active development inputs/caches. Preserve local build/dist material on hold until its originating artifact and possible human edits are compared. No blanket cache/build purge. | Ignored local inventory; follow-up #47/#50. Current tracked tree cleanliness is separate from ignored retained resources. |

## Retained evidence and review dates

The reviewed task lineage covers the original human runtime and molecular
writer/projection/map receivers; prepared recovery/domain/admission and Core
audits; saved-result/scene/addon receiving; the installed preparation, execution,
inspection and evaluation walkthroughs; source-panel observations; and public
artifact/installed-support diagnostics. These have distinct scientific producers
and dependencies. Keeping a later receiver does not automatically replace an
earlier wheel, failure record or reproducibility environment.

The local ledger retains an earlier future review when one already exists:
one context on **2026-11-09**, 11 on **2026-11-10**, and seven on
**2026-11-11**. The 31 entries with elapsed dates or no future date in their
inspected metadata have now been reviewed and are next reviewed by
**2026-11-12**. An earlier original retention contract still takes precedence if
recovered during follow-up. These counts refer to the
50 explicit task entries, not all files/environments on the host. Original
metadata is unchanged; the new ledger records the current decision separately.
No date grants automatic deletion.

The earlier #55 domain, #57 prepared-recovery and #33 preparation-profile
review dates are elapsed. Current inspection confirms their custody/closeout
records and retained contexts. Keep their original wheels, initial/final
diagnostics, frozen prescriptions and reused receiver chain for the open
provenance/admission/public-receiving work. The next review is 2026-11-12; removal
requires checking that no retained workflow depends on the exact environment and
that any unique original evidence has a verified retained copy.

## Explicit holds and unresolved handoff

| Hold / remaining work | Responsible owner | Interim procedure, review and removal condition |
| --- | --- | --- |
| Six loose operational snapshots and local build/dist attribution | #50 with originating task owners; #47 for package material | Preserve. Compare exact receipts/artifacts and possible human changes before treating a target as redundant. Review by 2026-11-12. An unverified snapshot is not proof of ownership. |
| One registered ecosystem-review worktree is absent | #19/#50 | Preserve its branch and Git registration; absence/cause is not a deletion attribution. Inspect branch/worktree ownership and recover any needed human work before an owner-approved Git cleanup. Review by 2026-11-12. No prune was run. |
| Original compatibility/pre-human locations and older 55-entry inventory | #50 / existing historical receipts | Two explicitly checked early locations remain absent; the historical inventory's earlier absence report is preserved. Do not infer cause, actor, disposal or global completeness. Preserve the surviving versioned receipts. |
| Shared scientific environment, private archives and immutable SDKs | Maintainers and #19/#47/#49/#56 | Protect their independent lifecycle and consumer dependencies; this component review does not authorize changes to shared/sibling resources. Existing earlier reviews remain due. |
| Central coordination closeout | #50, then MolSysSuite #104 | Local dispositions and gaps are ready. Keep #50 partial; deliver the sanitized handoff when the maintainer resumes other-repository issue work. Do not silently reopen that work. |

No matching active local task runtime was observed in the declared task paths
and runtime-command check. Unrelated activity and the agent/tool host are
preserved. This is a bounded observation, not a claim that the whole machine is
idle. No pre-existing resource was deleted, no process was terminated and no
scientific/provider operation was executed by this review.

## Why

The missing piece was a consolidated disposition across operations and retained
task contexts, rather than another directory sweep or molecular implementation.
The prior issue history contained useful separate closeouts but no single local
review covering the present dependencies, elapsed review dates and remaining
holds. This record makes continuation possible without converting temporary
location, age, an absent path or a completed experiment into disposal authority.

## What was refuted

- #71/#72 do not alone complete #50's full operational review.
- Managed scratch is not the same resource as a caller report, scientific
  artifact, private receiver or shared persistent environment.
- No evidence establishes a new scientific leak, a returned tracing-ownership
  defect, or the cause of historical absent resources.
- This review needs no new resource framework, universal matrix, molecular
  routine, experiment, browser observation or provider change.

## Scope and exclusions

Local DockingMT operations and explicitly identified retained contexts only.
Machine paths, account/environment diagnostics and process details stay in the
ignored local ledger. Public records contain categories, owners, decisions,
counts, source identities and this ledger's digest. Runtime code, existing
scientific/fixture/helper bytes, dependency pins and synchronized guides remain
unchanged. There is no release, public installation or C4/C6 acceptance.

## Acceptance criteria and verification

The local part is complete when applicable operations have an owner/disposition,
retained resources have a follow-up purpose/review/removal condition, unknown
attribution is protected, gaps have owners, and the sanitized checkpoint is
published under #50. Final report/index, relevant administrative and shared
publication/resource checks must pass, including a fresh committed export.
Their exact-source receipts belong in #50; hosted recovery remains #28.

The unchanged 38-test administrative selection passes with its existing published
Pytest Receptor 1.2.1 profile. Canonical Ruff, report indexes and the workspace
publication/resource preflights pass. The checks require no new environment,
scientific import/experiment or molecular/native execution. Fresh committed-export
receipts are delivered in #50 after the final documentation commit.

At the inspected runtime checkpoint `837de4b`, policy run 42118256374,
publication-governance run 42118256683 and DOM run 42118256185 are successful;
main CI 42118256218 is in progress at the latest observation. These are source-specific
facts, not terminal success for this new documentation head. No repeated
scientific gate is needed solely for this custody document.

The full issue closes after the maintainer-authorized central handoff. Neither
the local review nor the assigned holds silently grants disposal or clears the
separate scientific, installed/public or visible workflow gates.
