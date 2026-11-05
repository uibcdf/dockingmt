# Core and Extended MVP: scope of the 1.0 target

Requested by the maintainer on 2026-11-05 under
[#73](https://github.com/uibcdf/dockingmt/issues/73). Definitions come from
[`MVP.md`](MVP.md); implementation/evidence status comes from
[`CORE_MVP_STATUS.md`](CORE_MVP_STATUS.md), the current source and linked
qualification records. This comparison changes no gate or acceptance decision.
It accompanies the [prospective version ladder](RELEASE_MILESTONES.md).
After this reminder, the maintainer explicitly selected **Core plus Extended
for 1.0.0** on 2026-11-05; see
[DMT-045](DECISIONS.md#dmt-045--require-core-and-extended-mvp-for-100).
The definitions and evidence distinctions below remain unchanged.

## Core: a complete, traceable docking workflow

The Core MVP takes a receptor and small-molecule ligand through explicit
preparation, local docking/redocking, result inspection, reference comparison
and basic visualization, retaining the scientific choices and provenance.
It is judged by a credible complete workflow, not by a function count.

| Gate | Included functionality | Present implementation and remaining acceptance |
| --- | --- | --- |
| C0 — Foundations | Scientific problem/protocol/domain/pose/result objects; isolated backend; molecular identity; provenance; capability checks; units, validation, optional dependencies and diagnostics; inspectable defaults. | Substantial implemented/tested support through Vina, MolSysMT, PyUnitWizard, ArgDigest, DepDigest and SMonitor. Representative evidence is bounded; support-library/public-artifact admission has separate owners. |
| C1 — Preparation | Reproducibly prepare a conventional protein receptor and small ligand, with explicit inputs/transformations, identifiable states, source-to-backend traceability and visible preparation errors. | Explicit prepared objects, provider reports/maps, admission and installed examples exist. The first path need not solve all chemistry. General protonation/state selection, missing-chemistry/template coverage and independent scientific admission remain profile/provider questions. |
| C2 — Redocking | Starting from an experimental complex, identify/extract the reference ligand, prepare states, derive its search domain, search, normalize multiple poses, retain scores/ranks/state identity and compare with the reference by RMSD. Reconstruct the run configuration. | Real saved searches, provider-backed evaluation and installed workflows exist. Their bounded observations and failures do not establish general predictive accuracy or complete restoration from an arbitrary standalone JSON record. |
| C3 — Explicit local docking | Dock one ligand into a user-specified local box through the same scientific problem/result model, with inspectable backend conversion and limitations. | Implemented box/Vina path and contracts. Richer domains/backends require their own accepted workflows. |
| C4 — Domain from selection | Deterministic domain construction from a molecular selection, retaining source/frame/selection/geometry provenance, with a visualizable domain and explicit Vina projection. | Provider-owned selection/geometry and the domain-derivation record are delivered. Actual visible observation remains deferred. |
| C5 — Results and provenance | Explain which molecules/states, receptor, preparation, domain, backend/version/options/seed and score producer generated each result. Preserve poses, scores, units and rankings. | Structured records, captured inputs, audits and linked saved-case recovery exist. An integrity audit is not chemical validation; detached records do not automatically restore all molecular/environment state. |
| C6 — Basic MolSysViewer integration | Display receptor, searched domain and chosen pose(s) together; optionally compare a native/reference ligand without ad hoc user conversions. | Addon, saved-result explorer, player, Python/DOM/private-installed controls and scene artifacts exist. Live browser comm/canvas observation remains unaccepted. |

Core includes the backend scores produced by docking and their recorded ranks.
Extended E1 adds a separate evaluation of an already existing pose, multiple
named scoring histories and explicit reranking choices.

The maintained Core map has **35 criteria**. Whole-Core completion requires
C0–C6 acceptance and scientifically credible redocking within the declared
profile. Implemented APIs, passing software tests and actual scientific/public/
visible acceptance are different evidence. Whole Core is not currently accepted.

## Extended: collections, additional scoring and richer analysis

Extended builds on Core rather than replacing its obligations. It expands from
the basic complete docking workflow toward small collection studies and richer
pose interpretation, while preserving identities, error handling and provenance.

| Gate | Additional functionality | Present implementation and remaining acceptance |
| --- | --- | --- |
| E1 — Explicit scoring/rescoring | Evaluate an existing pose with a named method; keep multiple named scores; choose a ranking explicitly without assuming one universal score. | `score`, `DockingPose.with_scores` and `DockingResult.rank_by` exist, including bounded fixed-pose Vina/Vinardo evaluation and score/ranking histories. This is not unrestricted engine support or calibrated affinity/cross-ligand comparability. |
| E2 — Small virtual screening | Dock a modest ligand collection; isolate individual failures; retain ligand/state identity; aggregate/rank within a declared study; keep campaign/run/result boundaries clear. | `dock_many` is an existing serial, incremental prepared-problem executor with explicit failure outcomes. `summarize_redocking` aggregates compatible reference-evaluation records. These do not yet establish an accepted multi-ligand screening/enrichment workflow, generic cross-ligand ranking or a campaign scheduler. |
| E3 — Pose comparison and clustering | Compare against references and between poses; group meaningfully similar poses when scientifically appropriate. | Provider-backed RMSD/reference and explicit symmetry-aware evaluation paths exist. General pose clustering has no accepted delivered workflow/API in the reviewed public surface. Reusable geometry/comparison/clustering operations belong to MolSysMT. |
| E4 — Basic interaction analysis | A minimal structured representation of ligand–receptor interactions useful for interpretation, filtering and visualization. | No accepted general interaction-analysis API/workflow is delivered in the reviewed surface. Existing distance observations are not a general contact or interaction definition. General detection/characterization belongs to MolSysMT; specialized pharmacophore/topography work remains with its providers. DockingMT owns docking-specific interpretation and presentation. |
| E5 — Reproducibility audit | Independently reconstruct a stored representative workflow to the degree supported by its backend and environment, with observable missing information and limitations. | Captured bytes/options, input/result audits, linked-case recovery and bounded replay/installed records provide substantial pieces. Full arbitrary molecular/physical reconstruction and universal deterministic replay are not delivered guarantees. |

Existing Extended pieces must be reused, not implemented again. Their existence
does not accept E1–E5 as a whole. In particular, generic reference-summary support
is not evidence of screening enrichment, and named empirical scores do not
establish comparable binding free energies across ligands or receptor states.

## What changes in the 1.0 choice

| Target | What 1.0 promises | Consequence for remaining work |
| --- | --- | --- |
| Core consolidated | A stable, publicly installable, scientifically delimited complete docking/redocking workflow, provenance and basic visualization. | Finish Core/public/visible/scientific qualification and stabilize the promised API/schema. Existing Extended functionality can remain available with explicit support limits; the whole Extended gate set is not a hidden prerequisite. |
| Core plus Extended | The same Core foundation plus accepted modest screening, explicit rescoring, pose clustering, structured interaction analysis and reproducibility-audit workflows. | Also qualify E1–E5, including missing clustering/interaction contracts, provider receiving and actual screening studies. This expands both implementation and scientific validation before 1.0. |

Public Conda delivery, platform/minor support, scientific evidence, documented
limitations and API/record stability remain obligations for a credible 1.0 under
either option. Requiring Extended does not establish general docking accuracy;
choosing Core does not waive scientific validation or public installation.

The maintainer selected **Core plus Extended for 1.0.0** after reviewing these
options. Both C0–C6 and E1–E5 are therefore required before stabilization and
release. The earlier Core-only recommendation was not selected. The comparison
table retains the alternatives to explain that choice; it is not an unresolved
scope question. #73 tracks consolidation and the concrete version milestones.

Later horizons retain their own scope: additional engines/ML, receptor
flexibility, broad ensembles, TopoMT/PharmacophoreMT/ElastNetMT-guided protocols,
large campaigns and specialized ligands are not implicitly added to either MVP
by this comparison. General molecular work remains in MolSysMT throughout.
