# DockingMT Development Guide

Start here when joining the project or continuing on another machine. DockingMT
is the docking component of MolSysSuite: it owns docking problems, protocols,
engine integration, result meaning and docking-specific exploration. AutoDock
Vina is the first backend; its command-line vocabulary is not our scientific model.

## First reading route

| Order | Read | What you should know afterwards |
| --- | --- | --- |
| 1 | [Contributor instructions](../AGENTS.md), [MolSysSuite guide](../MOLSYSSUITE_GUIDE.md), [local instructions](AGENTS.md) | Ownership, controls and how decisions/issues are recorded. |
| 2 | [Development and onboarding](DEVELOPMENT.md) | Scientific purpose, concepts, setup, source navigation and contribution workflow. |
| 3 | [New-machine handoff](MACHINE_HANDOFF.md) | Verified checkpoint, unfinished work, custody and what a fresh clone does not contain. |
| 4 | [Complete functional plan](PRE_STABILIZATION_PLAN.md), [Core acceptance map](CORE_MVP_STATUS.md) | Implementation, evidence and remaining acceptance. |
| 5 | [Scientific model](SCIENTIFIC_MODEL.md), [architecture](ARCHITECTURE.md), [decisions](DECISIONS.md) | Why the code is organized this way and which choices must not be reopened accidentally. |
| 6 | [Operational roadmap](ROADMAP.md#current-operational-plan), [proposals](pending_proposals/README.md), [bugs](pending_bugs/README.md) | Next contributions and ownership of missing capabilities. |

For public entry points and detailed method contracts, use the
[public API guide](PUBLIC_API.md); it links source declarations and distinguishes
offline reading from molecular and engine work.

Use the [document map](DOCUMENT_MAP.md) for a particular question. Read historical
records when relevant; incorporation does not require reading every notebook or
replaying every experiment.

[Native small-fixture receiving](validation/installed_small_fixtures_2026-11-09.md)
executes the collected preparation/map/export/copy controls and exposes #103's
caller-unit copy defect. Both affected source profiles now pass; a new genuine
wheel still needs actual receiving. The original installed failure and provider
warnings stay explicit, separate from public/platform/hosted acceptance.

[Full installed collection](validation/installed_collection_2026-11-09.md) now
receives all 2,593 case imports under deliberate runtime-source isolation and
resolves #102's remaining shared-helper dependencies. Both complete offline
profiles still pass 1,267 cases; collection itself executes no scientific test.
The 104 administrative tests/26 subtests, exact input custody and provider count
feedback are recorded separately from public/full scientific/hosted gates.

The current [CI/source-context review](validation/ci_source_alignment_2026-11-09.md)
keeps #100 partial under MolSysSuite #178, while
[new private installed receiving](validation/record_wheel_inputs_2026-11-09.md)
passes 1,267 cases per unit policy and resolves #101's fixture namespace boundary.
These are separate from public delivery and executed hosted CI. The handoff
retains all original artifact and qualification identities.

The latest [source ownership/I-O checkpoint](validation/declaration_and_io_receiving_2026-11-09.md)
resolves #97/#98/#99: independent declaration snapshots, exact source-read errors
and offline batch-test collection pass complete affected receiving in both unit
policies. The [public inventory](validation/public_candidate_readiness.md#availability-refresh--2026-11-09)
still lacks covering MT/Viewer files; the public/installed and hosted gates remain.

The latest [E3 saved-pose checkpoint](validation/e3_saved_pose_study_2026-11-09.md)
receives the original three-pose comparison/clustering workflow in both unit
policies, after complete [public0.6 reference receiving](validation/e3_h5msm06_reference_receiving_2026-11-09.md).
#79/#88/#96 close their bounded scope; #558, actual canvas and public/hosted gates
remain. The full plan and handoff name the next owners and preserved evidence.

## Accepted destination and present limits

The accepted product scope is **Core C0–C6 plus Extended E1–E5**, bounded scientific
qualification, independent reproducibility and public installation. Prospective
**0.5.0** remains the functional planning milestone; stabilization uses as many
ordinary **0.x.0** releases as verified progress requires, followed by the
**1.0.0** stable-contract decision. [DMT-048](DECISIONS.md#dmt-048--let-pre-10-versions-follow-verified-progress)
records the open-ended version sequence. These are gates, not published versions. The separate
fixed private 0.1.0 candidate has [its own dossier](releases/0.1.0.md).

The starting profile is a declared single-state small molecule and rigid protein,
explicit preparation, a physical search box and Vina. Software/private installed
evidence does not certify general chemical validity, affinity, public dependency
closure or live canvas use. The complete objective is not achieved. See the
[current checkpoint](MACHINE_HANDOFF.md#current-development-checkpoint--2026-11-08).

The earlier autonomous goal was paused and cleared before the machine handoff.
The accepted product plan remains incomplete. The maintainer has resumed work
after the installed interaction-binding checkpoint; each
increment must leave an accurate developer-guide checkpoint. Follow the
[current handoff](MACHINE_HANDOFF.md#current-development-checkpoint--2026-11-08)
and operational queue; independent E4/live-observation holds and resource limits
retain their scope.

## Ownership that shapes every change

Molecular inspection, characterization, state/identity, manipulation, geometry,
matching and molecular interchange belong to **MolSysMT**. Reuse its public tools;
request uncovered reusable needs in its repository. DockingMT must not fill those
gaps with a local parser, matcher, chemistry rule or geometric algorithm.

MolSysViewer owns generic rendering/communication; DockingMT owns its addon and
docking interpretation. TopoMT, PharmacophoreMT and ElastNetMT retain their
specialized domains. ArgDigest, DepDigest, SMonitor and PyUnitWizard own their
shared boundary contracts. See the [suite contract](MOLSYSSUITE_CONTRACT.md) and
[contribution workflow](DEVELOPMENT.md#making-a-change).

## Evidence and history

| Need | Entry |
| --- | --- |
| Scientific assumptions/limits | [Scope](SCIENTIFIC_SCOPE.md), [validation strategy](VALIDATION_STRATEGY.md), [2026-11-04 audit](library_audit_2026-11-04.md). |
| Existing recovery/ranking observations | [Scientific overview](validation/scientific_evidence_overview_2026-11-04.md); its sources/populations remain frozen. |
| Installed walkthroughs | [Inspection](validation/installed_result_inspection.md), [preparation](validation/installed_3ptb_preparation.md), [execution](validation/installed_3ptb_execution.md), [evaluation](validation/installed_3ptb_evaluation.md). Check which steps execute science. |
| Extended work | [E1 bounded acceptance](archive/qualify_same_state_rescoring.md), [E2 bounded acceptance](archive/qualify_small_ligand_collection.md), [E3](archive/qualify_pose_comparison_and_clustering.md), [E4](pending_proposals/receive_docking_interaction_analysis.md). |
| E2 source receiving | [P59/P69 current source interpretations](validation/e2_source_admission_2026-11-07.md): source/axis/geometry/readiness/CIP evidence and independent saved reading pass; raw and interpreted representations retain their separate roles. |
| E2 preparation | [Named rigid preparation receiving](validation/e2_preparation_receiving_2026-11-07.md): both preparations and the fresh saved reader pass, preserving H accounting, named parameters, maps and actual exports. That separate phase adds no energies/searches. |
| E2 native acceptance and next workflow | [Native collection and independent reader](validation/e2_native_collection_2026-11-07.md) pass: three outcomes, two searches, five original poses and the declared empirical order. [#81 resolves the bounded rigid25 joint-domain workflow](archive/qualify_small_ligand_collection.md); broader science, public delivery and the complete functional objective remain separate. Next receive [E3 pose comparison/clustering under #79](archive/qualify_pose_comparison_and_clustering.md) through supported MolSysMT tools/composition. |
| Measured interaction workflow | [E4 receiving](validation/installed_3ptb_interactions.md): one case, normal/pm-fs and fresh readers; whole E4 remains partial. |
| E3 provider admission | [Source/population inspection](validation/e3_provider_admission_2026-11-07.md) identifies the retained poses/reference. [Latest H-policy and paired-control receiving](validation/e3_source_control_receiving_2026-11-08.md) reaches strict full39/prepared25 maps and exact current control bytes, then fails native persistence. #79 retains the #256 reference-storage hold; that selection’s pm/fs and final live checks remain unreceived. The separate geometry row below carries current #604/#659 state. |
| E3 geometry tools | [Complete correction receiving](validation/e3_geometry_fix_receiving_2026-11-08.md) passes the original analytic/adverse selection normal/pm-fs with byte-identical worker/assertions, clearing #659's client geometry hold. The old failed selection remains frozen; #256/reference/common-frame/full E3 remain separate. |
| E4 next receiving route | [Saved-analysis admission recipe](validation/e4_saved_analysis_admission_2026-11-07.md) reviews the provider projection/scene boundary before a new API. The separate same-carrier receiving below now passes; the original heavy selection and live visual review remain deferred. |
| E4 saved-carrier receiving | [Normal/pm-fs and independent reader](validation/e4_saved_carrier_receiving_2026-11-07.md) pass for the same complete saved carriers: real Python Viewers, explicit pose association, filtering/attachment/persistence and eleven refusals per profile. Initial receiver failure is preserved. The separate consumer API below now has source controls; whole E4, other scene projections and canvas/public delivery remain open. |
| E4 current Python integration | [Complete editable receiving and original-criterion audit](validation/e4_view_editable_2026-11-08.md): all eight original View/widget/native cells pass normal/pm-fs, retaining full original results and exact source/native custody. Failed setup/reader attempts stay preserved; final independent reading passes. #80/#60 remain partial for actual browser/comm/canvas and separate public/scientific scope. |
| Offline audit resource failures | [#95 source receiving](validation/audit_resource_errors_2026-11-09.md): native memory/control errors remain distinct from inconsistent records; 464 source cases per policy pass, with historical inputs and installed/scientific limits retained. |
| Offline coordinate audits | [Source correction #90](archive/audit_coordinate_record_admission.md) shares the existing pose-reader admission: malformed Boolean/complex coordinates are inconsistent; canonical empty snapshots remain valid with explicit length units. 409 affected record cases pass in each unit policy; no scientific or native execution acceptance follows. |
| Offline identity/rank audits | [Source correction #91](archive/audit_pose_identity_admission.md) validates current declarations and historical observations before comparison, retaining unknown values, NumPy integer ranks and valid reports. 562 affected source cases pass per unit policy; public/scientific/visual acceptance remains separate. |
| Result restoration allocation | [Bounded reader profile #28](validation/result_restore_2026-11-08.md): ordinary JSON peak Python allocations fall about 44%/56% on two fixed inputs; timing tradeoff and rejected compatibility candidate are explicit. 571 affected source cases pass per unit policy; general speed, scientific/public/installed acceptance remains unproven. |
| Public input resource errors | [Source correction #92](archive/input_normalization_masks_resource_failures.md): seven admission handlers preserve MemoryError; 549 complete affected source cases pass per caller policy, with all original failures and private test-support custody retained. |
| Public API and errors | [Source-linked guide](PUBLIC_API.md), [#94 receiving](validation/public_api_namespace_2026-11-09.md): 33 exports/13 exception aliases; 251 source cases per policy and two exact offline snippets pass. This later namespace has no new installed/public claim. |
| Current installed record API | [New private wheel/editable receiving](validation/record_wheel_editable_2026-11-09.md): 1,062 cases per caller policy, complete 67-path payload, 13 public exception aliases, four import refusals and 594-input support retirement. Original source/artifact/public/full-suite limits remain separate. |
| Earlier installed record API | [Private wheel/editable receiving](validation/record_wheel_editable_2026-11-08.md): 990 cases per caller policy, complete 66-path payload, four import refusals and 594-input support retirement. #93 fixes the descriptor; producer/public/full-suite/platform limits remain explicit. |
| Selected-pose interaction API | [`bind_interactions`/`PoseInteractions`](validation/pose_interaction_binding.md) preserve a complete result and detached carrier/analysis access. 190 source cases and [actual installed normal/pm-fs receiving](validation/e4_pose_binding_installed_2026-11-07.md) now pass, with fourteen refusals/profile, two complete carrier roundtrips and independent original-record verification. [Native unevaluated coverage](validation/e4_native_unevaluated_2026-11-07.md) now passes for empty-source invalidation. [The #642 source correction](validation/e4_evidence_catalog_fix_2026-11-07.md) is published; its exact native construction is held after a memory stop, so installed client acceptance remains pending. The explicit view route below retains separate qualification. |
| Ligand-model/source checkpoint | [Source decisions and failed anionic-reference receiving](validation/scientific_panel_ligand_models_2026-11-07.md) preserve both intended candidates and all original criteria; a separate minimal diagnostic identifies MolSysMT #644. First receive the provider correction, then complete fresh reference cells. No case/preparation/search is accepted. |
| Scientific-panel provider receiving | [Bounded normal/pm-fs occupancy and CCD reference receiving](validation/scientific_panel_provider_receiving_2026-11-07.md) passes original MK1/BTN PDB/CIF observations and eight refusals; no preparation, search or docking case is admitted. Next decide states/environment/termini and receive provider #558 public generation maps. |
| Independent workflow reconstruction | [E5 #83 resolved](archive/qualify_independent_installed_reproduction.md): [complete installed receiving](validation/e5_timed_replay_2026-11-07.md) reproduces both stored 1IEP arms normal/pm-fs with zero numerical drift, twelve pre-native/twelve version refusals, detached reader and six-criterion audit. One existing case; original failed cells/history, missing external chemistry and public/panel acceptance remain explicit. Next #33 state/environment/terminal decisions and #558 map receiving; no additional E5 search. |
| Interaction binding view | [`dmt.view(binding)`](validation/pose_interaction_view.md) retains the complete result while displaying only the admitted carrier/pose, live coverage and owned visuals. 186 source/protocol and 23 exact-ESM DOM cases pass. [Its own exact installed candidate](validation/e4_pose_interaction_view_installed_2026-11-07.md) now passes eight real-provider cells normal/pm-fs and independent saved-record reading. Remaining workflow criteria and actual canvas retain separate gates. |
| Public delivery | [Release ladder](RELEASE_MILESTONES.md), [public readiness](validation/public_candidate_readiness.md), [Conda controls](../devtools/conda-build/README.md). Distribution is Conda `uibcdf`. |
| Rationale/history | [Decisions](DECISIONS.md), [roadmap history](ROADMAP.md), [archive](archive/README.md), [original seed](FROZEN_SEED.md). |

The former chronological entry page is preserved at
[the pre-handoff source](https://github.com/uibcdf/dockingmt/blob/8e65091a0002023527ed7d3d6754a50695d2e1bd/devguide/README.md).
Its linked technical records retain their stated producers. Current navigation
does not become a new producer for old observations.

## Maintaining this directory

`NOW`, `DESIGNED FOR` and `HORIZON` distinguish requirements from protected future
possibilities. A concept's presence does not authorize a class, package or
dependency. The [original seed](FROZEN_SEED.md) preserves intent; maintained plans
and explicit decisions record subsequent experience.

Use the [reporting protocol](reporting_protocol.md): open an owning issue before
a durable report, retain failures, regenerate indexes, and archive resolved work.
Scientific evidence follows the [publication policy](validation/evidence_publication_policy.md).
Keep implementation, source qualification, installed artifacts, scientific
inference and visible acceptance distinct. A green check proves only its scope.
