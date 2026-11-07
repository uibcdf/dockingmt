---
summary: Receive MolSysMT structured interactions and associate them with existing docking poses for E4.
issue: uibcdf/dockingmt#80
status: partial
opened: 2026-11-06
closed:
verification: measured
area: [analysis, provenance, visualization, scientific-validation]
guard:
normative: devguide/MVP.md
blocked_by: [uibcdf/molsysmt#642]
supersedes: []
---

# Structured interaction analysis for docking poses

## Concrete workflow

E4 in the [complete functional plan](../PRE_STABILIZATION_PLAN.md) needs a minimal
structured analysis useful for filtering and eventual visualization. For a
selected existing pose, use a supported MolSysMT assembly of its known ligand
and receptor states, disjoint ligand/receptor selections and the original
Cartesian frame, with explicit structure selection and `pbc=False`.

The first profile considers hydrogen bonds (`baker_hubbard`/`nitrogen_oxygen`)
and hydrophobic typed proximity (`atom_pair_distance`/`smarts_hydrophobic_atoms`).
Preserve the provider's exact definitions, cutoffs/inequalities, units, chemistry
and H inventory. These experimental molecular definitions are not interaction
energies, affinity or biological validation, and do not imply all families.

## Existing provider tools

The [dated inspection](../validation/extended_provider_scope_2026-11-06.md)
identifies public detectors, sparse `molsysmt.Interactions`, explicit coverage,
source maps, queries and typed interchange. Their availability in source does
not establish actual qualified receiving. No missing-detector proposal is
warranted by this inspection; reuse delivered MolSysMT #252 and existing tools.

MolSysMT owns assembly, chemical state/site recognition, molecular geometry,
detection and molecular serialization. PharmacophoreMT owns pharmacophore model
interpretation. MolSysViewer owns generic rendering/communication. DockingMT
selects its scientific population, associates provider results with actual
docking records and supplies docking-specific interpretation/filtering policy.

## Receiving and association

1. Prove the actual public molecular assembly/projection route on the qualified
   dependency, preserving source atom maps, frame/state and H inventory. Report
   uncovered reusable needs in MolSysMT; do not add a merger, coordinate editor,
   atom matcher, typing rule or interaction engine here. Existing #49 bridges
   retain their receiving/removal obligations.
2. Preserve the complete provider analysis with participant roles/source indices,
   structure/state coverage, assumptions, method/profile, original versions and
   bibliography. Evaluated-empty, unevaluated and unsupported are distinct.
   Missing H or failed chemical admission cannot establish biological absence.
3. Link the new analysis to its actual result/pose, receptor/partner states and
   coordinate/input identities. Preserve original scores and producer identities.
   Use the provider's supported typed interchange/persistence; `to_dict()` and
   `to_page()` are inspection projections, not complete persistence codecs.
4. Register the bounded representative calculation and informative positive,
   adverse and empty controls before execution. Receive actual provider calls,
   filtering, nondefault units, immutability, source/installed provenance and
   detached records, keeping molecular numerical and consumer-association
   evidence distinct.
5. Pass structured data to the addon through supported provider contracts.
   Actual comm/canvas acceptance remains #52/#60 and the maintainer's scheduling
   decision; no Python object or static export proves it.

## Current disposition

The [six-cell installed notebook](../validation/installed_3ptb_interactions.ipynb)
and [finite prescription](../validation/installed_3ptb_interactions_registration.md)
are implemented. Early local [receiving](../validation/installed_3ptb_interactions.md)
does not pass: the initial process lacks notebook tooling before cells; the corrected
tooling attempt is stopped by the RAM-reserve guard. Its final counters and
association are absent/unverified; pm/fs is not attempted. No automatic heavy
restart occurs. These are nonpassing observations, not empty interactions.

A separate [hosted registration](../validation/installed_3ptb_interactions_hosted_registration.md)
now defines current-source installed Linux/Python 3.14 receiving, normal then
pm/fs, with a fresh saved reader per profile. The manual caller preserves the
local hold, registers at most twelve new detector calls and reserves the old
unknown six-call budget separately. Its record/source/archive admission controls
have focused administrative guards. The first hosted run `42203647830` at
`988d8a1` completes preparation, then refuses omitted-element XYZ coordinate
extraction; final detector counts are zero, payloads remain unchanged and pip
closure passes. Fresh readers and pm/fs are not reached. The separate
[hosted receipt](../validation/data/interaction_hosted_receiving_2026-11-06.json)
preserves the failed population. MolSysMT #610 receives the public composition
question. The explicit-atom public getter amendment is separately registered at
`5952053`; run `42206087852` then passes normal/pm-fs and both independent readers.
Its [success record](../validation/data/interaction_hosted_success_2026-11-06.json)
retains all twelve detector calls, 3/2 named retained-pose observations, evaluated-
empty translation controls and 1/0 analytic H-bond controls under both policies.
Original pose atoms/coordinates/scores, caller policy, provider typed/H5MSM
roundtrips, filtering and installed bytes remain. Eight provider files and
selected original receipts/diagnostics are preserved byte-exact compressed.
The bounded workflow passes; usable structured consumer/addon admission and
whole E4/functional/public/visual qualification remain unproven.

All 63 fixed private consumer payloads and the applicable active provider file
records remain identical before/after; pip check passes. Four preliminary
file-authority audit stops remain separate. Seven isolated Conda notebook tools
supply 208 verified files without modifying the scientific prefix. The later
progress-journal refinement preserves started/failed/completed phases; an isolated
standard-library SIGTERM control retains its valid started event. Its molecular
cells are unexecuted at that checkpoint. Later hosted variants retain their
separate producers and observations above. Review/register any further
computation separately; the full E4 contract remains unproven.

The route reuses the prepared native
source's retained virtual H counts and MolSysMT's delivered fixed-state H tool;
it does not infer missing chemistry or introduce a molecular reconstruction
algorithm in DockingMT. Existing #49 obligations remain.

Selected detector signatures exist at the
qualified pin, but current main has internal coordinate-delivery changes.
Unchanged signatures do not prove behavioral equivalence. Receive the actual
selected profile before changing a provider pin or making E4 acceptance claims.

## Saved-analysis consumer admission — 2026-11-07

The [new source-reviewed recipe](../validation/e4_saved_analysis_admission_2026-11-07.md)
identifies supported complete-carrier/layer reads, extraction/remap and Viewer
attachment at the original qualified pins. It adds no API or molecular run.
The original association's ligand indices `3220..3237` distinguish the analysed
3238-atom carrier (receptor_h3220 plus ligand18) from the prepared receptor2011.
That corrects the former handoff's carrier arithmetic without altering its
original evidence. The current destination scene's axes are unreceived.

First receive the same saved complete carrier as a baseline; projection to a
different docking scene additionally needs admitted receptor/ligand/frame maps,
lost-participant/coverage controls and physically checked retained coordinates.
`assume_aligned=True` declares a relationship; it does not authenticate it.
Do not repeat a saved analysis to label the other four poses as evaluated or
reconstruct full persistence from a query/page.

The recipe is not ready for execution: select exact destination/maps and controls,
seal finite artifacts/resources/call caps, and resolve the original local hold's
execution venue before running. No local replay or automatic manual CI follows.
Existing molecular receiving remains passing in its own bounded scope; this
consumer/addon admission and whole E4 remain partial. E3's provider-blocked
workflow does not waive any of these requirements.

## Same-carrier receiving passed — 2026-11-07

The [separately registered saved-carrier selection](../validation/e4_saved_carrier_receiving_2026-11-07.md)
passes normal/pm-fs and fresh independent saved-record reading. Original 3238-atom
carriers load in real Python Viewers, retain full molecular/analysis state, support
queries/pages and independent attachment/loading, and persist through complete
provider layers. Each profile receives two carriers, closes two views, performs
50 typed exports and passes eleven refusals with zero new detectors, H,
preparation, energies, searches, alignment or RMSD. The retained thirteen-atom
pose binds only to its actual geometry; the translated control is separate and
the other four poses remain unevaluated.

The [238-member archive](../validation/data/e4_saved_carrier_receiving_2026-11-07/manifest.json)
is SHA-256 `73c8114368f0d7011d2e27d229662bf29be1f99bea27c0e0a24065f077e04b4d`;
the [reader companion](../validation/data/e4_saved_carrier_reader_2026-11-07/manifest.json)
receives exact records and numerical witnesses without molecular imports or
restoration. Original diagnostic receiver failure, administrative sealing failure
and process controls are retained. No resource stop occurs. This new light
selection does not restart the suspended heavy attempt or launch manual CI.

The next product increment can choose the smallest docking-specific binding of
the admitted carrier to an explicitly selected original pose. Preserve the full
result, original scores/producers and missing/general scene correspondence;
do not broadcast one analysis over unmeasured poses. This issue remains partial
for that API/addon admission and whole E4; actual canvas/public/scientific gates
remain separate. The task-local launcher stays outside the runtime payload;
[MolSysSuite #173](https://github.com/uibcdf/molsyssuite/issues/173) requests
qualified reusable execution support for future receiving rather than a local
general tool or mandatory new scientific gate.

## Public binding implemented; installed receiving pending — 2026-11-07

[`bind_interactions` and `PoseInteractions`](../validation/pose_interaction_binding.md)
now implement the selected original-pose association. One explicitly admitted
one-frame carrier and ordered integer map must match the selected pose's verified
atom labels/elements, physical coordinates and declared known state/frame.
The complete original result and provider analyses remain detached; source pose
position is independent of rank/ID. Provider coverage distinguishes evaluated-
empty and unevaluated analyses. No molecular matching, detection or frame
replication is introduced; caller declarations do not authenticate chemistry,
unmapped receptor geometry or producers.

[Source qualification](../validation/data/pose_interaction_binding_source_2026-11-07.json)
passes 44 new synthetic protocol-double controls and 146 existing regressions.
All 190 complete, under registered CPU/RAM limits, with real provider operations
forbidden and no Vina import. Two initial fixture failures are retained separately.
These are consumer logic/contract tests, not actual native-system, artifact or
whole-E4 acceptance. Next register the exact new candidate and original saved
carriers for normal/pm-fs receiving, then the actual addon/scene association.
The original `a7422df` consumer has no new binding API and cannot certify it.
This issue remains partial; no public/provider pin or remote CI change follows.

The initial collection report also reproduces known Pytest Receptor #46
(miscounted collection errors as executed tests). Its exit/verdict is correctly
nonpassing; exact component event/JUnit receipts govern counts. Consumer evidence
is handed to that existing owner rather than opening a duplicate issue or
changing shared-tool code here.

## Bounded actual installed binding received — 2026-11-07

[The new candidate receiving](../validation/e4_pose_binding_installed_2026-11-07.md)
passes normal/pm-fs and independent standard-library record reading. The actual
consumer is source `cfff386`, wheel `0.0.0+307.gcfff386`, SHA-256
`bc6da61abcb51a6950b2c5ed388616a70dd7cd393056c2b98d3665f9a40d1c51`.
Its 74-file private prefix plus 3794 exact transported provider files excludes
the old consumer; borrowed MolSysMT `9e1f1b1` and original producer `5952053`
retain distinct identities. No provider checkout/pin or shared environment changes.

Both profiles accept the original retained pose and a separately derived
evaluated-empty control, receive all named models/filtering/accessor detachment,
and pass fourteen refusals. Two complete H5MSM 0.5 carrier roundtrips preserve
present topology/chemistry/geometry/structure links, analyses and mechanical
absence. The complete five-pose original JSON remains exact; no original pose
is replaced by the derived control or unmeasured pose labelled analysed.
All finite caps and unit-authority/restoration gates pass; no new scientific
preparation/detection/metric/native-energy/search work occurs.

The [119-member archive](../validation/data/e4_pose_binding_installed_2026-11-07/manifest.json)
is SHA-256 `0dc17c3dd7c6e2db8f03ca0756603a016694537195394dc758c6909b34592c45`;
the [34-member reader companion](../validation/data/e4_pose_binding_installed_reader_2026-11-07/manifest.json)
is `ee54ee5e6d42e5e1e0b25584cc40544f07d57e79d80ae4a3a436fd7c2706685f`.
Both early client parameter stops and two overstrict reader comparisons remain
failed and preserved. Each complete analysis equals its own frozen original;
the pre-existing cross-profile roundoff and distinct control source hashes are
preserved, with explicit physical-unit agreement checks. The reader imports no
molecular/scientific package or restores molecular models.

This accepts the bounded installed consumer composition, not whole E4. A native
named family with zero evaluated frames is still unreceived; the False-coverage
source-double guard cannot replace that case. Register/receive it through
supported MolSysMT operations, then admit the single-frame binding in the actual
addon without guessing other scene mappings or broadcasting observations.
The original four other poses, canvas, independent science/public/platform/minor
and full #73 gates keep their scope. This issue remains partial; hosted exact-head
evidence stays missing under #28 and `[skip ci]`, without manual CI dispatch.


## Native unevaluated-family receiving — 2026-11-07

The [registered native information-state receiving](../validation/e4_native_unevaluated_2026-11-07.md)
now passes its separately declared focused empty-source population normal/pm-fs
and independent record reading. Public MolSysMT invalidation on the translated
control's already empty `hbonds` yields no evaluated frames; its `hydrophobic`
remains evaluated-empty. The retained original carrier stays positive (3/2).
Both bindings preserve complete original result/source/analysis state, detached
copies, query coverage and two complete-carrier H5MSM 0.5 roundtrips/profile.
No new measurement, runtime implementation or provider pin change occurs.

Two positive-source invalidation attempts fail complete persistence because the
provider reader discards the unused evidence-label catalog. Their exact one-field
delta is reported in [MolSysMT #642](https://github.com/uibcdf/molsysmt/issues/642).
That composition remains failed; the empty-source pass does not clear it. The
first expanded empty-source attempt also remains interrupted at the 60 s wall
limit. A fresh focused selection retains preservation/coverage and two relevant
refusals while the earlier fourteen general refusals keep their unchanged
installed evidence. No resource limit or equality assertion is weakened.

Focused normal/pm-fs complete in 36.733/37.048 s with sampled group RSS
723,906,560/725,893,120 bytes. The standard-library reader passes in 9.112 s/
325,423,104 bytes, verifies all 210 primary stored/decoded records and imports
no scientific package or restores molecular data. The primary manifest is
`b4a676022aa26f0508fadd87bb5f1dee21d9e7650edf4ebe085599c4313793ef`;
the 17-member reader companion is
`3981244aeef9c31d8a08b8d4c00100718195bf8cdf449dbc19a3ddba635bffa0`.
All failures/interruption and owned terminal resource receipts remain. The
original producer `5952053`, actual consumer `cfff386`/wheel `bc6da61a` and
borrowed provider `9e1f1b1` retain their separate identities. #50 custody review
is 2026-11-14; #28 hosted evidence is missing under `[skip ci]`, no manual CI.

**Next:** admit an actual single-frame addon/scene binding without replacing the
full result by a one-pose collection or broadcasting analysis onto other poses.
The existing renderer builds one structure per pose and is not that route.
#642 still owns positive-invalidation persistence; whole E4/#73, other-carrier
correspondence, E3 #604, canvas #52/#60, independent science/reproduction and
public/minor/platform delivery remain unproven. Keep this report partial.


## Interaction view implemented and source-qualified — 2026-11-07

[The explicit `dmt.view(binding)` route](../validation/pose_interaction_view.md)
loads the complete admitted one-frame carrier through public Viewer APIs and
creates provider-owned visuals for stored analyses. The addon retains every
original result record and maps frame 0 only to the actual bound collection
position, including nonfirst poses. Explorer metadata/live coverage, Python/
context/panel actions, callbacks and summary/export use that mapping; unavailable
geometries remain listed with reasons and disabled controls. Matching dimensions
cannot admit a replacement scene. No matcher, codec, detector or geometry
projection is added here.

The final source selection passes 186 cases (28 new view controls, seven frontend
contracts, 151 other regressions), zero skips. The initial accidental real-provider
case is blocked by the molecular-operation guard and retained as failed; that
case is explicitly excluded from the repeated source-only selection and remains
required for actual receiving. Source failures are not erased. Final selection:
4.299 s/201,863,168 sampled group-RSS bytes. The exact served ESM passes 23 locked
Node26/jsdom DOM cases, 2.689 s/314,146,816 bytes. No molecular operation, actual
View loading, browser, comm or canvas is executed. All groups are terminal with
no resource interruption. Conda and provider pins remain unchanged; isolated
verified Node supplies the declared engine.

The [receipt](../validation/data/pose_interaction_view_source_2026-11-07.json) and
[178-member immutable archive](../validation/data/e4_pose_interaction_view_source_2026-11-07/manifest.json)
retain all raw attempts, exact source objects, collected/native/JUnit reports,
DOM logs and guard/tool identities. Manifest SHA-256 is
`9fbdb4081342dc80e117ff731837acc7be8a91edf690c157325a4e5173c4a04a`.
The resource inventory adds the new runtime adapter path; historical helper/data
hash declarations remain exact. #50 task custody review is 2026-11-14.

**Next:** build and identify a new consumer artifact and receive this actual
route normal/pm-fs on original carriers/results, including provider visuals/live
metadata, nonmutation, frame/pose axes and the excluded native regression. The
old `cfff386` wheel cannot count for this new route. MolSysMT #642 has provider
triage but no delivered correction; receive that separately. #80/#60 stay
partial; #28 skipped hosted evidence, full E4/#73, canvas, other-carrier projection,
E3 #604, independent science/reproduction and public/minor/platform keep their
separate gates. No manual CI is dispatched.
