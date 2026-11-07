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
blocked_by: []
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
