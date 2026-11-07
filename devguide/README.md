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
[current checkpoint](MACHINE_HANDOFF.md#verified-development-checkpoint).

The earlier autonomous goal was paused and cleared before the machine handoff.
The maintainer has now resumed the accepted product plan and requires each
increment to leave an accurate developer-guide checkpoint. Follow the
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
| Extended work | [E1 bounded acceptance](archive/qualify_same_state_rescoring.md), [E2](pending_proposals/qualify_small_ligand_collection.md), [E3](pending_proposals/qualify_pose_comparison_and_clustering.md), [E4](pending_proposals/receive_docking_interaction_analysis.md). |
| Measured interaction workflow | [E4 receiving](validation/installed_3ptb_interactions.md): one case, normal/pm-fs and fresh readers; whole E4 remains partial. |
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
