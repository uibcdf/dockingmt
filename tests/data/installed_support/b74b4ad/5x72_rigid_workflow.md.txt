# Original rigid geometry at experimental torsions in 5X72

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17),
[#6](https://github.com/uibcdf/dockingmt/issues/6) and
[#33](https://github.com/uibcdf/dockingmt/issues/33) own this bounded follow-up to
the [experimental-reference diagnostic](5x72_reference_workflow.md). The
[prespecified protocol](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6090156888)
precedes every new fixture angle, conformer, distance, RMSD and score. The
[driver](../../devtools/qualify_5x72_rigid.py),
[raw archive](data/5x72_rigid/audit_2026-10-09.json.gz),
[captured producer source](data/5x72_rigid/producer_2026-10-09.py.txt),
[original local checkpoint](data/5x72_rigid/checkpoint_2026-10-09.json),
[executed notebook](5x72_rigid_workflow_2026-10-09.ipynb) and
[guards](../../tests/test_5x72_rigid_workflow.py) retain the full populations.

## Prescribed construction and admission

Each original hydrogenated source has 39 atoms and 42 bonds. Its chemistry,
named source axis, R/S stereo, partial-charge/type choices and cuts (6,7)/(17,18)
remain those of the earlier independent experiment. The original experimental
24-heavy-atom SDF remains independently verified against its named PDB instance
through the existing explicit RDKit bridge (MolSysMT #215).

Public MolSysMT `get_dihedral_angles` reads experimental heavy quartets
(1,6,7,8) and (7,17,18,19) with PBC/GPU disabled. Each quartet is checked against
the original graph and its central bond against the declared cut. Public
`set_dihedral_angles` applies each target once in that order, deriving moving
blocks through the provider's covalent graph. Targets and achieved angles are
recorded in radians and independently checked with finite NumPy projections.
There is no torsional optimization, alternative-order selection or retry.

Public `least_rmsd_fit` then applies one proper rigid superposition of the
explicitly paired 24 heavy atoms, moving all 39 atoms, on CPU in double precision.
An independent NumPy/SVD verification checks the full transformed coordinates
and proper rotation. That verification never supplies or repairs the molecular
coordinates submitted to scoring. The fit is optimal for this one prescribed
conformer, not over all permitted torsion values or an energy landscape.

All 15 original H move with their original fragments, including polar H29 on
N8 and H28 at stereocenter C7. No H is regenerated or independently oriented.
The earlier experimental-reference arm used generated H, so this comparison
measures the prepared rigid geometry **including H**. It does not isolate a
pure heavy-coordinate effect. The chemical/H-parent axis stays identical.

Every detached operation must preserve its input, original source and reference.
Original topology, chemical-state records, H parents and prepared fields are
checked before admission. The full-atom rigid fragments have 11/17/11 atoms,
corresponding to heavy populations 7/11/6. All **741 unordered full-atom pairs
per ligand** are retained. All **246 within-fragment distances** and **42 bond
lengths** agree with the original within 1e-9 angstrom. The observed largest
changes are below 2e-14 angstrom. The signed volume around C7, using neighbors
6/8/17 and H28, preserves its magnitude and handedness. Negative guards reject
a stretched cut bond, altered central fragment and whole-molecule mirror image.

Target angles agree within 1e-9 radians. Full source/reference/intermediate/
fitted snapshots, moving blocks, fragment maps, distances and signed volumes
remain in the raw record. Proper fitting cannot substitute for covalent or
handedness checks. Positional RMSD is measured after the declared construction
against the experimental heavy coordinates, using public MolSysMT and independent
NumPy without further fitting or symmetry matching. Exceeding the earlier
2.5 angstrom criterion would remain a measured outcome, not an admission failure.

Public DockingMT ligand preparation uses the original named Gasteiger/AutoDock4
choices and two cuts. The original retained/source map, all 25 serial/name/
group/chain/numerical-charge/type fields and native tree must remain equal.
The existing public native writer binds the fitted geometry to either original
ROOT order within 0.000500001 angstrom. Charge consistency passes; readiness
remains unassessed. Score inputs are unranked and have no prior docking score.

## Eight fixed scores and complete comparisons

Vina 1.2.7, CPU1, seed42, the original box and both unchanged receptor contexts
produce exactly **eight new fixed evaluations**: two ligands × two ROOT orders
× sham/occupied. P59's occupied receptor contains fixed P69; P69's contains
fixed P59. Coordinates and scores capture exact submitted bytes. No docking,
energy minimization, relaxation or optimization is performed.

Every fixed component agrees exactly between ROOT orders in both contexts for
both ligands; the 0.001 kcal/mol reporting-resolution comparison passes. This
is finite control evidence, not a general ROOT policy. All **156 previously
retained poses** and their **312 saved fixed evaluations** are reused unchanged,
with all eight component contrasts, original ranks/seeds/efforts/recovery/maps,
and per-cell first/minimum/closest records. No historical geometry is rescored.

| Ligand | Constructed heavy RMSD (angstrom) | Sham total (kcal/mol) | Occupied total (kcal/mol) | Occupied prepared-minus-experimental total (kcal/mol) |
| --- | ---: | ---: | ---: | ---: |
| P59 | 0.513138 | -7.618 | -8.551 | +1.983 |
| P69 | 0.679452 | -1.666 | -2.667 | +7.832 |

These are constructed within-ligand contrasts, not cross-ligand affinity
rankings or new returned-pose recovery counts. Both conformers satisfy the
earlier positional criterion, showing that the original rigid geometry can
be placed near the reference. This does not establish global reachability
statistics, convergence or the best achievable near-reference energy.

| Ligand | Search receptor | Score receptor | Retained poses with lower fixed total than constructed conformer |
| --- | --- | --- | ---: |
| P59 | Sham | Sham | 50/50 |
| P59 | Sham | Occupied | 0/50 |
| P59 | Occupied | Sham | 25/28 |
| P59 | Occupied | Occupied | 25/28 |
| P69 | Sham | Sham | 49/49 |
| P69 | Sham | Occupied | 9/49 |
| P69 | Occupied | Sham | 29/29 |
| P69 | Occupied | Occupied | 29/29 |

Negative pose-minus-constructed totals favor the retained pose in the same
declared context; exact numerical ties remain ties. Finite minima break ties
by original rank and do not change public ranking/comparability policy.

For P69 in the occupied context, the ligand-inter component changes from
-11.727 in the experimental-reference arm to -2.979 kcal/mol in the constructed
prepared-geometry arm: +8.748 kcal/mol. Its intra component changes from 0.559
to 2.183, while the reported best-pose intra is identical to intra in both fixed
evaluations. The intra sign alone therefore does not explain the total-score
ordering. P59's ligand-inter difference is +2.215 kcal/mol. Fixed `Vina.score`
components remain distinct from docking `Vina.energies` observations.

A small positional heavy RMSD thus coexists with a large interaction-score
change for this unrelaxed prescribed point. This suggests a separate
contact/geometry or score-basin diagnostic; it does not identify a physical
contact, establish a preparation defect or choose a production remedy.
Original-versus-generated H orientation remains part of that uncertainty.

## Evidence and scope

The gzip SHA256 is
`f0e91b99793bc61403aedf660016f532e1a46c5815f92441f511dbac8ffb4179`;
the decompressed JSON SHA256 is
`a2ae7e8f6b5b9cb2cfd663bd2a5907a6f5edfc4a0d903074c2bee082141905eb`.
The original source capture retains the producer's initial import ordering.
Ruff corrected that ordering in the maintained helper after capture; no
operation, scientific input, original score or archive byte was changed.
The captured source is text evidence with its authenticated original digest.

Additional public dihedral/fit/rotation/translation/covalent-block source
routes authenticate against the same qualified MolSysMT5bd893c85/native profile.
Source inspection and executed finite compatibility evidence remain distinct
from newer-provider qualification, a fresh native build, a complete
installed-artifact suite or public/platform admission. Clean MolSysMT/ArgDigest/
Viewer worktrees behind origin26/3/68 remain preserved; no sibling code changes.

The provider's getter documentation still claims degree output irrespective of
session policy. A minimal public call returns 0.785398 radians under a radians
policy and 45 degrees under a degrees policy, with equal explicit radian values.
That documentation finding is reported in
[MolSysMT #357](https://github.com/uibcdf/molsysmt/issues/357), with the current
origin prose inspected separately from the executed preserved runtime.
DockingMT explicitly extracts radians and tests a degree policy; no behavior
workaround or provider change is needed for this experiment.

The original local checkpoint records selected executed gates and the saved-result
notebook at pre-commit capture. Later exact-head unskipped Python3.11–3.14
source-CI receipts belong in the owning issues without rewriting that capture.
Selected local validation passes **234 distinct tests**: 161 existing
scoring/native/ROOT/occupancy/reciprocal/reference/RMSD/reporting boundaries,
64 named charge/type checks and nine new rigid-control guards. The three
saved-result notebook code cells execute without errors. Ruff lint/format,
report indexes, seven registered guide routes and 65 local links pass.
Existing MolSysMT#215/#352/#353/#349 and MolSysSuite#31/#106 retain ownership
and removal conditions. #17/#6/#33 stay partial/open.

This experiment admits no local energy-optimization API or general molecular
matching/fitting wrapper. A next contact or score-basin diagnostic needs its
own explicit maps, H policy, method and interpretation before execution.
One prescribed conformer per ligand and one complex do not establish affinity,
cooperativity, stereoselectivity, recovery probability, convergence, chemical
correctness or general torsion/H/preparation/scoring/comparability defaults.

The subsequent [saved-input distance diagnostic](5x72_contact_workflow.md)
locates short protein pairs in both ligands while preserving every original
score. Its eight complete matrices describe geometry associations, without
identifying an energy term, cause or preparation remedy.
