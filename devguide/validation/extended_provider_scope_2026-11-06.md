# Extended molecular-provider scope inspection — 2026-11-06

Owners: [DockingMT #79](https://github.com/uibcdf/dockingmt/issues/79) (E3) and
[#80](https://github.com/uibcdf/dockingmt/issues/80) (E4), under the
[complete pre-stabilization objective](../PRE_STABILIZATION_PLAN.md).
Classification: **static source/contract inspection, not runtime receiving or
scientific acceptance**. Inspected consumer: `2a2168d4b7ccd382f0cd4ac0e9e6f78009d71979`.

## Actual sources and preservation

Scoped central `suite_status.py` refreshes DockingMT, MolSysMT and PharmacophoreMT.
DockingMT is clean/current. MolSysMT's clean local main `71fbe4f46d3c` is 123 commits
behind fetched main; PharmacophoreMT's clean main `c4c31a89a61d` is one commit
ahead. Both worktrees/local commits are explicitly preserved. Read immutable
remote Git blobs rather than pulling, checking out, installing or editing them.
PharmacophoreMT remote `aa837dcea5c9317e36660c333a9d0a1607e74105` supplies ownership
context; no pharmacophore runtime dependency or new capability is required here.

MolSysMT inspected main is
[`ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6`](https://github.com/uibcdf/molsysmt/tree/ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6).
Qualified DockingMT CI/private runtime remains
[`00abb958fb93649131d5ce5fe5e12e90cf4900e9`](https://github.com/uibcdf/molsysmt/tree/00abb958fb93649131d5ce5fe5e12e90cf4900e9).
No pin, shared environment or frozen producer changes. The
[blob/signature receipt](data/extended_provider_scope_2026-11-06.json) records
these separate inputs without importing the provider.

## E3: reuse metrics; request clustering

Public `structure.get_rmsd` measures positional deviations without fitting.
`get_symmetry_corrected_rmsd` admits declared chemical correspondences and records
complete/anchored/candidate search scope. Their inspected files are byte-identical
between the two provider commits; that does not qualify their entire dependency
closure or this new workflow. Existing consumer reference/RMSD evaluation remains.

The inspected structure exports/tree contain no cluster-named operation. Before
filing #604, issue searches for cluster/clustering/pairwise find no clustering request;
correspondence #310/#387 and identity #447 have separate established purposes.
This bounded search is not proof that every public composition is absent.

[MolSysMT #604](https://github.com/uibcdf/molsysmt/issues/604) asks first for a
supported existing composition, otherwise minimal bounded pairwise positional
RMSD/clustering tools. Their geometry, correspondence and grouping remain in
MolSysMT. The [consumer contract](../pending_proposals/qualify_pose_comparison_and_clustering.md)
defines ordered populations, no implicit fitting, units, linkage/threshold and
tie behavior, meaningful controls and representative receiving. No molecular
algorithm is added to DockingMT; no E3 execution has occurred.

## E4: existing structured interactions are usable candidates

Public `interactions.hbonds.get_hbonds` and
`interactions.hydrophobic.get_hydrophobic_interactions` accept selected structures,
explicit state, disjoint between selections and named method/profile. Sparse
`Interactions` retains participant/source maps, evaluated coverage, measurements,
criteria, assumptions and original software/bibliography. MolSysMT #252 is
closed/delivered. The old #250 namespace proposal body is not evidence that the
current implemented namespace is absent; no duplicate detector issue is filed.

Both detector signatures exist at the qualified pin. Their current files differ
in forwarding `with_structures=not index_selections` to the internal chemical
context; unchanged signatures are not behavioral-equivalence evidence.
`interactions/result.py` and `native/interactions_dict.py` are byte-identical in
this inspection. Full supported receiving and actual source-map/pose association
remain unproven.

An important public contract distinction: `Interactions.to_dict()` exposes
selected occurrence columns and metadata; its docstring directs complete typed
serialization to `InteractionsDict`. `to_page()` is a bounded inspection page,
not a standalone persistence codec. Reuse public typed conversion/H5MSM where
supported rather than writing a consumer molecular codec. Queries preserve
coverage; empty observations do not erase unevaluated/unsupported scope.

[#80's receiving contract](../pending_proposals/receive_docking_interaction_analysis.md)
starts with explicitly named hydrogen-bond and hydrophobic-proximity profiles.
All assembly, recognition, geometry, detection and interchange remain provider
operations. DockingMT owns actual pose/result associations and interpretation;
specialized pharmacophore work retains PharmacophoreMT ownership. No current
detector calculation, new molecular preparation or native docking runs here.

## Evidence limits and next work

This scoping advances missing workflow ownership and provider feedback. It does
not accept E3/E4, a public package/platform, visible frontend, scientific panel or
the complete functional 0.5.0. Receive #604 when supported, and independently
advance #80's actual provider assembly/detection/persistence and consumer
association controls. Preserve #49's remaining molecular bridges, E1 #78 and its
MolSysMT #599/#447 needs. Existing live-visual scheduling remains deferred.

