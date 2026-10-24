# Roadmap

The roadmap defines direction and gates, not dates.

## Production ligand projection — 2026-10-24

[`prepare_ligand` now delegates typed-H reduction and charge aggregation](validation/ligand_projection.md)
to MolSysMT, retaining its actual reduced system, public maps and original/derived
assignments. The local H-parent/aggregation loop is removed. Provider refusals and
unknown-inventory constraints remain explicit; no general molecular helper or
implicit state repair is added. Receptor preparation is a separate migration.

Four reference preparations preserve atom records, trees and axis reports; the
1S63 total-charge remark changes only a tiny floating-point aggregation residue.
The full local run's six undeclared positive fixtures and corrected 22-case guard
selection are retained separately. Installed candidate and exact-head gates have
their own terminal handoff in [#49](https://github.com/uibcdf/dockingmt/issues/49).

**Next: native PDBQT export with a completed map bound to the actual prepared
payload, then parser replacement for that profile.** Keep explicit serial/name/
group presentation, ROOT policy, stage maps, source identity and attribution.
General permutations remain provider-owned #369; #49/#33/#5 remain partial.
Public delivery remains #30/#47 and HTML/C6 stays deferred.

MolSysMT [closed #223 on 2026-10-24](https://github.com/uibcdf/molsysmt/issues/223#issuecomment-6388413966)
with its [provider delivery guide](https://github.com/uibcdf/molsysmt/blob/8a43cb2eb/devguide/atom_correspondence_delivery.md).
Production adoption remains here under #49. Later provider source changes the
reader/composition namespaces; this checkpoint retains the qualified `128a0bbb`
entry points and does not adopt the later revision implicitly. Wider inventory
admission and full-system permutation remain separate from that delivery.

## Known-source pose qualification — 2026-10-24

The [native pose receiving](validation/known_source_poses.md) qualifies public
projection, completed native export maps and MolSysMT #226 reading against actual
DockingMT/Vina output, with default/nondefault units and strict negative controls.
The first 23 focused tests, 105-case source selection and 272-case ordinary-wheel
selection pass; the added legacy-wire boundary has separate evidence in #49.
These are overlapping software profiles, not general chemical admission.

MolSysMT #223 is broader than its delivered typed-H/map slice: that slice already
exists in our qualified source and should be consumed. **Next implementation:
integrate public projection and mapped native export into the prepared producer,
then replace parsing for that bound profile.** The current legacy serializer does
not produce the reader's completed map. Do not manufacture one from retained
indices, or use a native export map against different legacy bytes. Preserve
earlier stage maps, original/derived attribution and representation compatibility.

The prior connectivity migration is complete at its own producer: [terminal
evidence](https://github.com/uibcdf/dockingmt/issues/49#issuecomment-6373836819)
verifies 1,163 tests per Python 3.11–3.14, zero skips and actual coverage upload.
Native general permutation remains MolSysMT #369. #49/#33 and public delivery
#30/#47 stay partial; HTML/C6 review remains deferred. No release is published.

## Retained-connectivity implementation — 2026-10-23

[Flexible preparation now delegates retained connectivity](validation/retained_connectivity.md)
to MolSysMT's delivered state-aware induced-subset operation. The local traversal
and its exception are removed without changing ROOT/cut policy or source pins.
The selected 75-case fragment/torsion/flexible/format source gate passes, including
assigned/reference disagreement, omitted connectors, source preservation and
unchanged refusal. Installed candidate and exact-head CI evidence are recorded
separately in [#49](https://github.com/uibcdf/dockingmt/issues/49).

The preceding copy/stereo receiving is complete: [#51's terminal receipt](https://github.com/uibcdf/dockingmt/issues/51#issuecomment-6373232230)
verifies 1,158 cases on each Python 3.11–3.14, zero skips, dependency closure and
actual coverage publication. That count and source belong to the preceding commit.

Next functional work remains the provider-owned export/projection and pose-axis
contracts under #49/#33 (MolSysMT #223/#369). Receive delivered tools before
retiring the corresponding consumer routes. HTML review remains deferred under
#52; C6 and whole-Core scientific acceptance remain open. Public delivery remains
#30/#47, with a MolSysSuite version notice at publication closeout.

## Provider receiving checkpoint — 2026-10-23

**HTML review is deferred by the maintainer.** The scene and original producers
remain unchanged; no browser observation or C6 acceptance is claimed. The bounded
[native-copy/template-stereo receiving](validation/provider_receiving_2026-10-23.md)
uses MolSysMT `128a0bbb94e6804f5663e58a45313c77de1cc30d` and retains the ArgDigest
and Viewer pins. Ten ownership controls and the broader 174-case ordinary-wheel
selection pass, including all 24 historical rows / 167 saved poses. Updated SDF
input profiles have 18 passing format controls; optional explicit-RDKit 1IEP
export has a separate provider report, MolSysMT #436. No molecular operation is
implemented downstream, new registered 3PTB search is run or public floor raised.

Completed: [exact-head Python 3.11–3.14 gates and #51 closeout](https://github.com/uibcdf/dockingmt/issues/51#issuecomment-6373232230).
Remaining projection/maps, pose ensembles and general molecular retirement stay
provider-owned under #49; broader native-format retirement remains #33. Resume
browser review only when the maintainer chooses it. Public release/file admission
remains #30/#47, with the required version-specific MolSysSuite availability notice
at publication closeout. This source receiving block does not publish a release.

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
