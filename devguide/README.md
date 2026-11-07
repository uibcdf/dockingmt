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

Use the [document map](DOCUMENT_MAP.md) for a particular question. Read historical
records when relevant; incorporation does not require reading every notebook or
replaying every experiment.

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
[current checkpoint](MACHINE_HANDOFF.md#current-development-checkpoint--2026-11-07).

The earlier autonomous goal was paused and cleared before the machine handoff.
The accepted product plan remains incomplete. The maintainer has resumed work
after the installed interaction-binding checkpoint; each
increment must leave an accurate developer-guide checkpoint. Follow the
[current handoff](MACHINE_HANDOFF.md#current-development-checkpoint--2026-11-07)
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
| Extended work | [E1 bounded acceptance](archive/qualify_same_state_rescoring.md), [E2 bounded acceptance](archive/qualify_small_ligand_collection.md), [E3](pending_proposals/qualify_pose_comparison_and_clustering.md), [E4](pending_proposals/receive_docking_interaction_analysis.md). |
| E2 source receiving | [P59/P69 current source interpretations](validation/e2_source_admission_2026-11-07.md): source/axis/geometry/readiness/CIP evidence and independent saved reading pass; raw and interpreted representations retain their separate roles. |
| E2 preparation | [Named rigid preparation receiving](validation/e2_preparation_receiving_2026-11-07.md): both preparations and the fresh saved reader pass, preserving H accounting, named parameters, maps and actual exports. That separate phase adds no energies/searches. |
| E2 native acceptance and next workflow | [Native collection and independent reader](validation/e2_native_collection_2026-11-07.md) pass: three outcomes, two searches, five original poses and the declared empirical order. [#81 resolves the bounded rigid25 joint-domain workflow](archive/qualify_small_ligand_collection.md); broader science, public delivery and the complete functional objective remain separate. Next receive [E3 pose comparison/clustering under #79](pending_proposals/qualify_pose_comparison_and_clustering.md) through supported MolSysMT tools/composition. |
| Measured interaction workflow | [E4 receiving](validation/installed_3ptb_interactions.md): one case, normal/pm-fs and fresh readers; whole E4 remains partial. |
| E3 provider admission | [Current source/population inspection](validation/e3_provider_admission_2026-11-07.md) identifies three P59 poses and an experimental-reference candidate. #79 is blocked on MolSysMT #604; reference/H/correspondence admission and all E3 controls remain required. No molecular calculation occurs. |
| E4 next receiving route | [Saved-analysis admission recipe](validation/e4_saved_analysis_admission_2026-11-07.md) reviews the provider projection/scene boundary before a new API. The separate same-carrier receiving below now passes; the original heavy selection and live visual review remain deferred. |
| E4 saved-carrier receiving | [Normal/pm-fs and independent reader](validation/e4_saved_carrier_receiving_2026-11-07.md) pass for the same complete saved carriers: real Python Viewers, explicit pose association, filtering/attachment/persistence and eleven refusals per profile. Initial receiver failure is preserved. The separate consumer API below now has source controls; whole E4, other scene projections and canvas/public delivery remain open. |
| Selected-pose interaction API | [`bind_interactions`/`PoseInteractions`](validation/pose_interaction_binding.md) preserve a complete result and detached carrier/analysis access. 190 source cases and [actual installed normal/pm-fs receiving](validation/e4_pose_binding_installed_2026-11-07.md) now pass, with fourteen refusals/profile, two complete carrier roundtrips and independent original-record verification. [Native unevaluated coverage](validation/e4_native_unevaluated_2026-11-07.md) now passes for empty-source invalidation. [The #642 source correction](validation/e4_evidence_catalog_fix_2026-11-07.md) is published; its exact native construction is held after a memory stop, so installed client acceptance remains pending. The explicit view route below retains separate qualification. |
| Independent workflow reconstruction | [E5 #83](pending_proposals/qualify_independent_installed_reproduction.md): [installed attribution](validation/e5_installed_replay_2026-11-07.md) now works without Git, with 24 passing source cases/two real SDK contexts. Next admit the current producer and independent normal/pm-fs replay/adverse matrix; six searches remain unspent. Historical #16 remains resolved; whole E5 is unproven. |
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
