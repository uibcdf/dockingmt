# Roadmap

The roadmap defines direction and gates, not dates.

## Current execution checkpoint — 2026-10-23

The maintainer accepted the minimal 3PTB scene after the pause. The
[executed notebook and scene evidence](validation/3ptb_scene.md) use the unchanged
ordinary wheel/provider composition and original saved result. Five code cells
verify identities, original coordinates, box geometry, Python visibility/navigation,
nondefault units and immutable inputs, then export a self-contained HTML. No new
search or scoring is executed. Forty-one installed viewer/delegation controls pass
without skips; this is a bounded Python/installed result.

**Next: inspect the actual scene in an enabled browser.** The execution session
has no browser available, so visible rendering, framing, controls and C6 remain
pending under [#52](https://github.com/uibcdf/dockingmt/issues/52). Open the retained
HTML or live notebook, compare receptor/reference/rank-1 pose/domain and record the
observation before deciding C6 or reviewing whole-Core acceptance. No renderer or
general molecular workaround belongs downstream.

MolSysMT #390 has delivered explicit template stereo transfer; the newer native
copy contract is tracked by DockingMT #51. Both require separate consumer adoption
and do not silently replace this scene's qualified providers. Public delivery
remains #30/#47; after a new public package and matching Release exist, announce
the available version by an issue in MolSysSuite, as recorded in
[the release closeout](release_titles.md#availability-announcement).

## Current execution checkpoint — 2026-10-20

**Paused at the user's request, before visualization.** The
[current pause handoff](validation/pause_handoff_2026-10-20.md) is the resumption
entry point. The installed environment was reconstructed and qualified; MolSysMT's
compressed input and [optional declared-state symmetry evaluation](validation/symmetry_redocking.md)
were consumed with the positional baseline preserved separately.

The [human 3PTB notebook](validation/human_3ptb_workflow_2026-10-20.ipynb) completed
input, explicit preparation, domain, one preregistered search, evaluation and
saved-result recovery. Two recorded executions preserve the initial stereo-metadata
refusal and successful recovery of the same native result; no second search was
run. All 24 historical rows / 167 poses were received without repeating searches.
Source CI at `4695041` passes 1,145 tests without skips on each Python 3.11–3.14;
the original ordinary wheel independently passes its 277-case installed selection.
See the handoff for exact producers and limits.

**Next: discuss the purpose, scene and observable acceptance criteria with the
maintainer before implementing visualization.** A suggested first scene contains
the receptor, reference ligand, rank-1 pose under its named ranking criterion and
search domain in the original coordinate frame. This suggestion is not an accepted
design. C6 and whole-Core acceptance remain open. An installed control or green CI
does not establish general scientific validity.

Missing projection/maps and native pose/permutation operations remain provider-owned
under [#49](https://github.com/uibcdf/dockingmt/issues/49); do not implement those
molecular operations downstream. Public distribution remains #30/#47. Advance
Extended-MVP or peer integrations only when an accepted human workflow requires
them, following the vertical pilots' human-before-agent progression.

## Phase 0 — Foundations and MolSysSuite-native bootstrap

Status: **NOW**

- establish scientific model;
- establish molecular-state/preparation concepts;
- establish search-domain/guidance/constraint distinctions;
- establish backend capability contract;
- choose and validate Vina integration;
- adopt MolSysSuite shared infrastructure contracts (PyUnitWizard, ArgDigest, DepDigest, SMonitor);
- establish provenance and identity policies;
- make scientific defaults explicit;
- define initial package boundaries;
- select redocking validation cases.

**Exit condition:** architecture can express the Core MVP without leaking Vina-specific
concepts into the public scientific model and DockingMT behaves as a native MolSysSuite
component rather than a parallel software stack.

## Phase 1 — Core canonical docking

Status: **NOW**

- preparation;
- redocking;
- explicit local docking;
- search domain from selection;
- normalized poses/results;
- named scores/ranks;
- provenance;
- basic MolSysViewer visualization.

**Exit condition:** all Core MVP gates pass and redocking validation is scientifically credible.

## Phase 2 — Extended scientific MVP

Status: **NOW after Core**

- explicit scoring/rescoring;
- small virtual screening;
- campaign-level aggregation as needed;
- pose comparison/clustering;
- basic interaction analysis;
- reproducibility audit;
- regression/validation suite;
- user-facing examples and API stabilization.

**Exit condition:** Extended MVP gates pass.

## Phase 3 — Advanced scientific integration with MolSysSuite peers

Status: **DESIGNED FOR**

- TopoMT-derived domains and guidance;
- PharmacophoreMT filtering/scoring/constraints/guidance;
- richer MolSysViewer Docking Explorer;
- ensemble workflows from MolSysMT;
- first meaningful ElastNetMT bridge when scientifically mature.

**Exit condition:** integrations demonstrate scientific value without fragile package coupling.

## Phase 4 — Advanced protocols and multiple backends

Status: **DESIGNED FOR**

Potential work:

- GNINA/ML backends;
- multi-stage protocols;
- consensus docking;
- receptor flexibility;
- macrocycle/peptide-specialized engines;
- ensemble/dynamic-pocket workflows;
- water/metal-aware protocols;
- blind docking.

## Phase 5 — Native scientific innovation

Status: **HORIZON**

Investigate original DockingMT methods, especially:

- molecular-landscape-aware sampling;
- topography-aware search;
- pocket decomposition;
- flexibility-aware search;
- pharmacophore-guided search;
- dynamic-pocket docking;
- fragment placement/growth/linking support;
- hybrid physics/ML scoring/refinement;
- uncertainty-aware pose landscapes.

## Roadmap governance

A feature should enter implementation only when:

1. its scientific purpose is clear;
2. it fits or deliberately revises the scientific model;
3. required dependencies are mature enough;
4. a validation criterion can be stated.

Do not promote horizons merely because the architecture can represent them.
