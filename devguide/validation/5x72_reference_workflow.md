# Experimental-reference score diagnostic for P59 and P69 in 5X72

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17),
[#6](https://github.com/uibcdf/dockingmt/issues/6) and
[#33](https://github.com/uibcdf/dockingmt/issues/33) own this bounded follow-up to
the [fixed-P69](5x72_occupancy_workflow.md) and
[reciprocal fixed-P59](5x72_reciprocal_workflow.md) controls. The
[prespecified plan](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6089648793)
and [admission addendum](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6089744224)
precede every new fixed evaluation and pair-distance measurement. The
[driver](../../devtools/qualify_5x72_reference.py),
[raw archive](data/5x72_reference/audit_2026-10-09.json.gz),
[executed notebook](5x72_reference_workflow_2026-10-09.ipynb),
[original local checkpoint](data/5x72_reference/checkpoint_2026-10-09.json) and
[guards](../../tests/test_5x72_reference_workflow.py) retain the complete evidence.

## Reference admission

The unchanged 24-heavy-atom experimental SDF for each ligand is read through
the existing explicit RDKit bridge, with dialect ownership in
[MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215). The earlier
independent checks against the named PDB instance, indexed heavy graph and R/S
stereo remain required. Public fixed-state hydrogen addition uses the original
RDKit policy, `pH=None` and no optimization, appending 15 H without moving the
experimental heavy coordinates. Generated H orientation is a model assumption.

Direct preparation failed before scoring because this reference's generated
names differ from those in the original hydrogenated SDF: P59's first written
atom would be `C7` instead of `C8`. This is retained as a rejected representation
path. Names and coordinates are not used to infer correspondence. Public
indexed queries check all 39 elements, formal charges, stereochemistry and
aromatic flags, all 42 bond endpoint pairs and available bond orders. Nullable
orders stay unknown. Every H-parent assignment agrees, including polar H29
bonded to source N8; H28 on stereocenter C7 is a distinct, merged nonpolar H.

After those checks, public `msm.copy` detaches the original source and public
`msm.set` places all 39 independently verified reference coordinates on that
axis. Original topology and chemical-state records remain exactly unchanged.
The same public DockingMT ligand preparation uses Gasteiger-Marsili charges,
AutoDock4 chemical-environment typing and cuts (6,7)/(17,18). The original
retained/source map, all 25 serial/name/group/chain/charge/type fields and the
native torsion-tree record must agree before either order is admitted. Public
native writing binds the reference to each original native/fixed-first tree,
within 0.000500001 angstrom of the input coordinates. No writer, matcher,
reader, renaming adapter or provider patch is added. Charge consistency passes;
readiness remains unassessed. Original sources and unranked score inputs stay
immutable and contain no fabricated docking score.

Strict production authenticates the original runtime/native bytes, all older
archive digests and original producer Git blobs, with the ignored generated
version file checked separately. The newly generated reference snapshots equal
the previously saved opposite-companion preparation. Current-runtime guards
check molecular values rather than pinning historical dataframe dtype
annotations; they cover ordinary and inferred string policy without forcing
the known old-provider legacy/Copy-on-Write gap in MolSysMT #349.

## Fixed populations and observations

There are **eight new fixed evaluations**, two ligands × two original ROOT
orders × two previously captured receptor contexts. P59's occupied receptor
contains fixed experimental P69; P69's contains fixed experimental P59. The
same-writer protein-only sham is unchanged. Vina 1.2.7, CPU1, seed42 and the
original box (center -15,15,129; size 30,24,24 angstrom) are used with exact
submitted-byte capture. There is no new docking, relaxation, local optimization,
parameter change or outcome-selected retry.

All eight fixed components agree **exactly** between ROOT orders for both
contexts and both ligands; the prespecified 0.001 kcal/mol reporting-resolution
comparison passes. This finite agreement does not establish a general ROOT policy.

| Reference geometry | Protein-only fixed total (kcal/mol) | Occupied fixed total (kcal/mol) | Ligand intra component (kcal/mol) |
| --- | ---: | ---: | ---: |
| P59 | -9.661 | -10.534 | -0.296 |
| P69 | -9.626 | -10.499 | 0.559 |

No cross-ligand affinity ranking is implied. The intra component equals the
reported best-pose intra component in each unchanged fixed evaluation; its
sign alone does not explain the total-score ordering. Fixed `Vina.score`
components remain distinct from docking `Vina.energies` observations.

The diagnostic reuses **all 156 retained poses**, 78 per ligand from the two
24-cell occupancy experiments, and their **312 already saved fixed evaluations**.
Historical protein-only searches remain reused observations. Every corresponding
eight-component pose-minus-reference difference, original rank, seed, effort,
recovery, source map and retained-set first/minimum/closest record is saved.
Negative total differences favor the returned geometry in that specific
ligand/order/receptor context; numeric ties remain ties. Finite minima use
original-rank tie breaking and do not change public ranking/comparability defaults.

| Ligand | Search receptor | Score receptor | Returned poses with lower fixed total than reference |
| --- | --- | --- | ---: |
| P59 | Sham | Sham | 48/50 |
| P59 | Sham | Occupied | 0/50 |
| P59 | Occupied | Sham | 0/28 |
| P59 | Occupied | Occupied | 0/28 |
| P69 | Sham | Sham | 16/49 |
| P69 | Sham | Occupied | 0/49 |
| P69 | Occupied | Sham | 0/29 |
| P69 | Occupied | Occupied | 10/29 |

Thus P59's occupied experimental reference has a lower total than every retained
pose. For P69, ten occupied retained sets contain a pose with lower occupied
total than the experimental reference. All ten are first-ranked geometries
outside the recovery criterion. The seven recovered P69 poses have occupied
pose-minus-reference totals between +0.179 and +0.505 kcal/mol.

A concrete native-order P69 cell, seed42/exhaustiveness8, has:

| Geometry | Positional heavy RMSD (angstrom) | Occupied fixed total | Ligand inter | Ligand intra | Torsions |
| --- | ---: | ---: | ---: | ---: | ---: |
| Experimental heavy reference + generated H | 0 | -10.499 | -11.727 | 0.559 | 1.228 |
| Original rank1 | 5.529 | -11.000 | -12.286 | -0.830 | 1.286 |
| Original rank3 | 2.020 | -10.320 | -11.526 | 1.102 | 1.207 |

Components are kcal/mol. This particular inter score favors the incorrect
rank1 geometry. Evaluating the unrelaxed crystal reference alone therefore
does not restore P69 ordering. This is a component diagnostic, not proof of
the physical cause or an environmental/affinity assessment.

## Prepared-versus-experimental rigid geometry

Public MolSysMT distances are independently checked against NumPy without PBC,
fitting or symmetry correction. Public explicit-cut rigid fragments provide
the indexed partition: heavy populations 0..6 (7), 7..17 (11) and 18..23 (6).
All **276 unordered heavy pairs and 27 heavy bonds per ligand** are retained,
with coordinates, fragment labels, within-fragment flags and full summaries.

| Ligand / pair population | Pair-distance RMS difference (angstrom) | Maximum absolute difference (angstrom) |
| --- | ---: | ---: |
| P59, all 276 pairs | 0.661 | 2.348 |
| P59, fragment 0 (21 pairs) | 0.058 | 0.130 |
| P59, fragment 1 (55 pairs) | 0.089 | 0.186 |
| P59, fragment 2 (15 pairs) | 0.022 | 0.048 |
| P69, all 276 pairs | 0.745 | 2.498 |
| P69, fragment 0 (21 pairs) | 0.014 | 0.029 |
| P69, fragment 1 (55 pairs) | 0.122 | 0.312 |
| P69, fragment 2 (15 pairs) | 0.019 | 0.043 |

Selected torsion rotations preserve intrafragment pair distances. The original
prepared fragments therefore cannot reproduce every experimental pair distance
exactly using those rotations alone. This does not establish failure at the
2.5 angstrom recovery tolerance: the earlier occupied experiment already
contains seven recovered P69 poses. No chemical-acceptability threshold is
introduced; source preparation, unrelaxed heavy coordinates and generated H
remain distinct assumptions. Pair-distance differences alone do not prove
steric cause, chemical correctness or global reachability.

## Evidence and next scope

The gzip SHA256 is
`8b53aac76447951737e0f477124fa11b074c8e0d6ae4244eac686968d471c1d3`;
the decompressed JSON SHA256 is
`b9ef59927caff00ebee26145bdab1a64ff5ced94342cf5f762638cb8953c309e`.
The original local checkpoint records selected executed gates and the notebook
at pre-commit capture. Exact-head hosted Python3.11–3.14 source-CI receipts are
recorded later in the owning issues without rewriting that checkpoint.

Selected local validation passes **225 distinct tests**: 154 existing
scoring/native/ROOT/occupancy/reciprocal/RMSD/reporting boundaries, 64 named
charge/type checks and seven new reference guards. The three notebook code
cells are executed with no errors. Ruff lint/format, report indexes, seven
registered guide routes and 61 local links pass. The existing exact Conda
source-profile variation remains tracked by MolSysSuite #31; it is unchanged.

The initial seven-guard run passed four and failed three at the reference
snapshot equality under pm/fs. An independent field comparison found only
last-digit coordinate differences on conversion to nm, with unchanged chemistry
and all other snapshot fields. The portable helper now compares fixed-nm
reference coordinates within 1e-13 nm and all other fields exactly. The
[original producer source](data/5x72_reference/producer_2026-10-09.py) is preserved
at its captured digest; the scientific archive and all eight original scores
are unchanged. This software roundoff correction does not relax prepared
identity, source immutability, H-parent, tree or serialized-coordinate gates.

The matched controls support a separately prespecified diagnostic of geometry
and fixed-score basins, rather than a production-default change. Its protocol
must distinguish an experimentally placed geometry from one attainable with
the original rigid fragments, retain identity/H assumptions and any local
refinement explicitly, and define the measured score components. Local
optimization would require a separately accepted operation and protocol; none
is introduced here. One complex and two named stereoisomers do not establish
affinity, cooperativity, stereoselectivity, convergence, recovery probability,
general preparation/H/torsion/scoring policy or public/platform admission.

The new driver authenticates additional public copy/distance/fragment source
routes against the same qualified MolSysMT commit and preserves the existing
native binary. This is bounded consumer evidence, not qualification of newer
provider source, a fresh native build or a complete installed-artifact suite.
MolSysMT #352/#353 retain composition ownership; #17/#6/#33 remain partial/open.
