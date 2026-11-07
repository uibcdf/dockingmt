# New-machine development handoff

Owner: [DockingMT #82](https://github.com/uibcdf/dockingmt/issues/82).
Checkpoint date: **2026-11-06**. The destination is another **machine**, using the
same `uibcdf/dockingmt` repository, issue history and scientific producers.
No repository rename, issue transfer or new release is part of this handoff.

Read [development/onboarding](DEVELOPMENT.md) for setup and code navigation.
[PRE_STABILIZATION_PLAN.md](PRE_STABILIZATION_PLAN.md) owns the full product
requirements; this file explains how to resume without recovering chat history.

## Verified development checkpoint

| Boundary | Evidence / disposition |
| --- | --- |
| Pre-handoff source | `8e65091a0002023527ed7d3d6754a50695d2e1bd`, committed/pushed before documentation work. The handoff documentation has its own later source identity. |
| Exact-source CI | [42208588851](https://github.com/uibcdf/dockingmt/actions/runs/42208588851): terminal success, all seven jobs and one artifact, checked through published GH Run Receptor 1.4.0 and individual job facts. |
| Other source gates | [Policy](https://github.com/uibcdf/dockingmt/actions/runs/42208589332), [publication controls](https://github.com/uibcdf/dockingmt/actions/runs/42208589352) and [DOM](https://github.com/uibcdf/dockingmt/actions/runs/42208588821) succeed. They qualify their own scope. |
| E4 scientific producer | `5952053328aac6f737e22906e984c0f9eb938dd7`; [run 42206087852](https://github.com/uibcdf/dockingmt/actions/runs/42206087852) passes normal/pm-fs and two fresh saved readers. Its own CI 42205979421 passes 7/7. |
| E4 observation | One original pose of one 3PTB case: 3 named H-bond observations and 2 typed hydrophobic proximities under both unit policies; translated controls 0/0 and analytic H-bond controls 1/0. Twelve detector calls total, zero in fresh readers. This is not biological validation or whole E4 acceptance. |
| Earlier failures | Tooling absence, local RAM-reserve interruption and first hosted XYZ-getter refusal retain their own producers/diagnostics. The interrupted local final count is unknown; the first hosted final count is verified zero. |
| Automation | The previous autonomous implementation goal was paused and cleared. This documentation task does not reactivate it. The interrupted continuation made only source/contract inspections, with no runtime patch or new scientific execution. |
| Version/public status | Full Core+Extended completion targets prospective 0.5.0, then stabilization 0.9.0 and later 1.0.0. Fixed private 0.1.0 candidate 905abc9 stays fixed. Source/private receiving is not public Conda delivery. |

The [E4 interpretation](validation/installed_3ptb_interactions.md) and
[original success receipt](validation/data/interaction_hosted_success_2026-11-06.json)
retain actual methods, units, software, maps, scores, files and limits.
Original data are not relabelled with the handoff documentation commit.
A later head needs its own applicable gates; consult
[#82](https://github.com/uibcdf/dockingmt/issues/82) and
[#28](https://github.com/uibcdf/dockingmt/issues/28) for this handoff's
final source/CI rather than treating the pre-handoff result as its proof.

## Decisions to preserve

| Decision | Why it matters / where to recover context |
| --- | --- |
| Scientific model richer than Vina | Problems/domains/protocols remain scientific concepts; backend limitations are explicit. [Vision](VISION.md), [model](SCIENTIFIC_MODEL.md), [engines](ENGINES.md). |
| General molecular work belongs to MolSysMT | Writers, graph operations, correspondence, H/charge/type operations and geometry must be reused/requested there. [#49 migration record](pending_proposals/retire_general_molecular_operations.md). |
| Preparation choices and uncertainty are explicit | No fabricated charges/types or inferred missing chemistry. `unassessed` does not establish chemical validity. [Preparation profile](validation/preparation_profile.md), [assessment](validation/preparation_assessment.md). |
| Saved records do not synthesize missing molecular state | Detached results retain provenance; supplied sources/maps/bytes need admission. [Recovery](validation/saved_human_case_recovery.md), [prepared recovery](validation/prepared_recovery.md). |
| Named scores and comparison admission are conservative | Preserve original scores/history; equal labels do not establish comparability. [Score semantics](validation/score_semantics.md), [reference evidence](validation/scoring_reference.md). |
| Scientific observations keep their original populations | Poses/seeds/complexes, failed/evaluated-empty/unevaluated and software/scientific/visual proofs differ. [Audit](library_audit_2026-11-04.md), [validation strategy](VALIDATION_STRATEGY.md). |
| Core+Extended is accepted scope | DMT-045/046 select scope and pre-stabilization delivery; DMT-047 records score-reference evidence. [Decisions](DECISIONS.md), [release ladder](RELEASE_MILESTONES.md). |

The [roadmap](ROADMAP.md) preserves earlier checkpoint detail. Historical
“next” instructions are not the current queue. The former entry-page chronology
is also recoverable from the pre-handoff Git revision.

## Controlled sources, not public minima

The authoritative current declarations are
[dependency_routes.toml](../devtools/dependency_routes.toml) and actual workflows.

| Controlled input | Exact source |
| --- | --- |
| ArgDigest | `3d1ec53c374098016452abab74706e9d80df5462` |
| MolSysMT | `00abb958fb93649131d5ce5fe5e12e90cf4900e9` |
| MolSysViewer | `78ede79e2e345593db5bfe80d246d3f6c70bd005` |
| Dependency/source SDK | `738fe8dd731abb99dac421b0bb2acc8564110180` |
| Publication/resource/installed SDK | `95f693be10c9205ab9b912cb53453710a207bf45` |

Do not use whichever sibling checkout happens to be beside the new clone as
though it were the qualified source. Inspect its actual commit/dirty state.
Development editables, normal-source receiving and public Conda installation
are different contexts. The [developer controls](../devtools/README.md) explain
clean SDK acquisition; [Conda controls](../devtools/conda-build/README.md) own
actual candidate/publisher gates. Do not mechanically bump all pins together.

Public installation is through Conda `uibcdf`. The last recorded public-provider
receiving has uncovered gaps (#30/#47 and provider-owned dispositions); refresh
actual artifacts before a new public claim. Old registry snapshots and a new
dependency solve do not prove the required behavior is available.

## New-machine continuation — 2026-11-06

The continuation now has separate [E1 receiving](validation/e1_installed_receiving_2026-11-06.md)
and [public-workflow records](validation/e1_public_composition_2026-11-06.md).
Actual runtime source remains DockingMT `2fda6238e6b1cb3742f5d30b8ed3af699f9ed748`
with the separately identified development MolSysMT; private snapshots/wheels
and Vina/Boost retain their exact identities and missing public-closure limits.
Original qualified pins and scientific producers above remain unchanged.

Finite five-pose source/native and private installed rescoring, external
interaction-component ordering and fresh saved readers have receiving evidence.
The maintained public reconstruction/scoring example additionally completes
continuity for one actual returned docking pose: four old scores/rank/history
survive with sixteen added components. The requested two-pose population remains
incomplete; later qualification failures and record-only adjudication remain
separate. Multi-pose continuity and positive user comparison are still #78 work.
Do not infer restoration of historical prepared H or whole E1/E5 acceptance.

The maintainer authorizes direct commit/push with `[skip ci]` for incremental
work, using focused local checks and separate explicit remote checkpoints.
Do not dispatch manual CI to bypass that instruction. The pre-handoff CI runs
above do not become evidence for a later head; skipped remote gates remain
missing under #28/#30 rather than passing. See the current root `AGENTS.md`.
The original local E4 computational hold and the cleared autonomous goal remain
unaffected by this individually authorized continuation.

## Next work, by owner

| Work | Next meaningful action | Owner / limits |
| --- | --- | --- |
| E4 structured consumer/addon admission | Bind saved provider analyses to the actual original pose/result and declared axes; preserve coverage, methods, units and provenance without recalculation. | [#80](pending_proposals/receive_docking_interaction_analysis.md). Whole E4 stays partial. |
| E1 representative rescoring | Extend received singleton public continuity to an admitted multi-pose population and positive user comparison/decision consumption. | [#78](pending_proposals/qualify_same_state_rescoring.md). Provider-wide #599/#447 remain separate; no blanket wait or relaxed strict ranking/PDBQT rewrite. |
| E2 distinct-ligand study | Admit actual sources/states and study comparison conditions before API expansion/calculation. | [#81](pending_proposals/qualify_small_ligand_collection.md). Reuse serial `dock_many`; no generic campaign framework. |
| E3 comparison/clustering | Receive the supported provider composition/tools before implementation. | [#79](pending_proposals/qualify_pose_comparison_and_clustering.md), MolSysMT [#604](https://github.com/uibcdf/molsysmt/issues/604). No local molecular clustering/matching. |
| Scientific panel | Resolve source/state/environment/template/reconstruction admission before searches. | [Panel admission](validation/scientific_panel_admission_2026-11-04.md) and [environment](validation/scientific_panel_environment_2026-11-04.md) retain #33/#49 and MolSysMT #555–#558. Proposed candidates are not admitted complexes. |
| E5 reproduction | Qualify a whole independent representative workflow to its documented degree. | Full plan #73; existing readers/captures are pieces, not whole E5. |
| Public/platform delivery | Refresh artifacts, qualify the actual compatible public combination and exact staged Conda file/cells. | #30/#47. No source fallback or private-wheel proof substitutes. |
| Live visualization | Schedule/observe actual controls, communication and canvas when the maintainer chooses. | #52/#60. Python/DOM success is separate; #291 notifications are already received in the qualified source/private combination. |

The maintainer's provider-issue authorization permits reporting uncovered
molecular needs in MolSysMT, not implementing them in DockingMT. Other deferred
cross-component work and live observation do not resume automatically.

### Last unfinished E4 investigation

The saved interaction model materializes five additional nonpolar H. For this
profile it has 2,029 atoms, whereas the prepared thirteen-atom pose scene has 2,024
with the same 2,011-atom receptor. Its analysis covers one structure; the original
docking result has five poses. Counts, labels or `assume_aligned=True` cannot
authenticate or fix those axes.

At the qualified Viewer source, public independent interaction loading
extracts/reorders source axes but does **not** embed a subsystem into a larger
target. See the [actual load contract](https://github.com/uibcdf/molsysviewer/blob/78ede79e2e345593db5bfe80d246d3f6c70bd005/molsysviewer/interactions.py).
MolSysMT already offers extraction/remapping and structure append with old
observation/coverage preservation; its [native controls](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/tests/native/test_molsys_interactions.py)
are a source-inspected candidate composition. This particular addon composition
has **not** been executed/accepted. No new binding API was selected or implemented.
Confirm supported provider contracts and actual retained/lost participants and
unevaluated frames before any scene integration. Never duplicate one pose's
analysis across five different poses or add an index/geometry repair here.

## Evidence that does not arrive with Git

A fresh clone contains maintained guidance, source, frozen test support,
prescriptions and committed scientific records. E4 includes thirty exact exports
and eight provider H5MSM models with original/compressed digests. Those can be
transport-decompressed and read through the recorded compatible MolSysMT tools.

Git does **not** contain every scientific prefix, private wheel, original Actions
ZIP, ignored launcher/log or package cache. `.molsyssuite/`, `.molsyssuite-tools/`,
venvs and frontend `node_modules/` are ignored. Historical `/tmp` or old machine
paths in receipts identify past custody; they are not portable setup requirements.

Before retiring the original machine, review existing #50 custody and protect
unique required artifacts. The narrow recent set includes:

| Artifact | Identity / custody |
| --- | --- |
| First E4 hosted original ZIP | `dockingmt-e4-42203647830-1.zip`; SHA-256 `e4f12b46f1255141cefe621f9959c54c7432cb68ced49849ac35dddaed9a6700`. Failure and selected exports are in Git. |
| Successful E4 hosted original ZIP | `dockingmt-e4-42206087852-1.zip`; SHA-256 `67af4078fd942b6c7cef1aadd61f5c2318f2ba4cef4c9439b2e9c9447959c690`. Full pip inspection, preparation bulk outputs and private wheel remain in this ZIP. |
| Successful E4 consumer wheel | `dockingmt-0.0.0+293.g5952053-py3-none-any.whl`; SHA-256 `d5038470712a4c1203088b28f973be5466e95aca2781a4288bc02606c84ab88b`, also within that ZIP. |
| Fixed private 0.1.0 populations | Follow [the dossier](releases/0.1.0.md) and its manifests. There are separate archive populations: preserve actual files/hashes and their distinct closures, not one invented universal lock. |
| Older private qualification resources | Follow the existing [#50 inventory/dispositions](pending_proposals/review_temporary_resources.md) and linked manifests. They are not automatically included in the recent E4 set. |

Custody review: **2026-11-13**. Recent Actions artifacts expire **2026-11-20**.
Review/download and independently verify before expiry; after expiry, use
verified retained originals, not replacement bytes manufactured from a rebuild.
Copy the required archives/unique records to the new machine or an agreed retained
location and compare SHA-256 there before declaring transfer complete.
Do not publish local paths, credentials or unrelated project material.

Do not copy a Conda/venv prefix as the installation strategy. Recreate environments
from recipes/explicit records and install compatible artifacts for the destination
OS/Python/architecture. A source pin alone does not reproduce a native binary
byte-for-byte. An old native wheel may be incompatible with the new machine.
SDK/tool clones are reconstructible from their published revisions; unique
scientific artifacts/receipts require explicit custody.

No artifact transfer or destination installation is claimed by this document.
The original machine must retain the required originals until the receiver
verifies them. Do not purge shared environments or other projects.

## Resume checklist on the new machine

1. Clone/fetch the same repository, verify its full commit/status and read this
   guide. Distinguish the code/scientific producers above from later doc commits.
2. Verify required retained artifacts against their manifests; identify missing
   materials explicitly. Check for any still-live **specific** remote run before
   repeating it; expired observation time is not a stopped process.
3. Build/select the admitted 3.14 development environment and correct provider
   context using [DEVELOPMENT.md](DEVELOPMENT.md). Verify versions, origins,
   dependency closure and clean SDK provenance.
4. Run applicable lightweight checks. Do not replay old molecular notebooks,
   searches or the full native suite as a machine-change smoke test.
5. Choose an accepted task with its owner and refresh related issue/provider
   state. The table is a dated handoff, not a promise that providers remain blocked.
6. Before any scientific work, review the old local E4 hold and register fresh
   source/artifact/input identities, resources, population and failure policy.
   Moving machines does not itself authorize an automatic restart.
7. Keep public/visual/release claims within actual evidence. A new package/release
   eventually requires its version-specific MolSysSuite notice; none is created here.
