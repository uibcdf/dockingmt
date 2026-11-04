# Saved-input distance contrasts in 5X72

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17),
[#6](https://github.com/uibcdf/dockingmt/issues/6) and
[#33](https://github.com/uibcdf/dockingmt/issues/33) own this follow-up to the
[original-rigid control](5x72_rigid_workflow.md). The
[prespecified protocol](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6094190056)
precedes all new fixture distances and proximity summaries. The
[driver](../../devtools/qualify_5x72_contact.py),
[raw archive](data/5x72_contact/audit_2026-10-09.json.gz),
[original producer](data/5x72_contact/producer_2026-10-09.py),
[local checkpoint](data/5x72_contact/checkpoint_2026-10-09.json),
[executed notebook](5x72_contact_workflow_2026-10-09.ipynb) and
[guards](../../tests/test_5x72_contact_workflow.py) retain the declared populations.

## Exact inputs and public measurement

This diagnostic compares original-rigid placement with the earlier
experimental-heavy/generated-H reference. It authenticates both archives and
both original receptor archives, then reads the exact PDBQT bytes captured by
successful fixed evaluations. It does not use unrounded pose coordinates,
regenerate H, prepare molecules or reconstruct scoring inputs. All 16 original
fixed-score captures remain unchanged. There are **zero new scores, searches,
energy optimizations or historical-pose contact measurements**.

Both ROOT orders must have equal atom fields and submitted coordinates on the
explicit original source axis, and exactly equal saved score components.
Only after that check does the declared native order represent each input.
The canonical ligand rows are source indices 0..23 and 29: 24 heavy atoms and
one retained polar H. Native MolSysMT PDBQT conversion explicitly discards the
ligand torsion tree to project its prepared coordinates. It does not recover
complete chemistry; original trees and raw inputs remain captured separately.

Public `structure.get_distances` compares separate ligand and receptor
projections, using explicit row selections, Cartesian pairs, CPU and no PBC.
PyUnitWizard explicitly extracts angstrom values regardless of application
units. Finite NumPy differences independently verify all entries within
1e-10 angstrom. Input projections remain unchanged.

Exactly **eight rectangular matrices / 298,700 distances** are retained:
two ligands × two coordinate arms × sham/occupied receptor. Each matrix has
25 ligand rows and 1,481 or 1,506 receptor rows. The occupied protein prefix is
identical to sham; its appended 25 rows are the fixed companion, not protein.
Correspondence is source index × receptor row/serial, never residue proximity
or an inferred atom match. Group summaries use partition, chain, group ID and
group name while retaining each original row and atom table.

## Descriptive proximity and complete contrasts

Counts use strict thresholds **<1.5, <2, <2.5, <3, <4 and <5 angstrom**.
All matrices, minima, per-source-atom and per-receptor-group summaries remain
saved. Every pair for which either arm is <5 angstrom is retained as a contrast:
353/415 sham/occupied rows for P59; 300/356 for P69. These overlapping context
populations are not independent observations.

Heavy–heavy, ligand-H/receptor-heavy, ligand-heavy/receptor-H and H–H populations
are separate. Receptor H identity uses the prepared H/HD/HS types; omitted
nonpolar H cannot be inferred. The protein has 1,207 heavy atoms and 274 retained
H. The companion has 24 heavy atoms and one retained H. The original-rigid
ligand H travels with its original fragment; earlier-reference H was generated.
That difference remains a confound, even when heavy-pair summaries are separate.

| Ligand | Coordinate arm | Protein heavy-pair minimum (angstrom) | Protein heavy pairs <2.5 | <3 | <4 | <5 | Companion heavy-pair minimum (angstrom) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| P59 | Earlier reference | 2.537896 | 0 | 2 | 57 | 225 | 3.018935 |
| P59 | Original rigid | 2.389969 | 2 | 3 | 47 | 234 | 3.021996 |
| P69 | Earlier reference | 2.796309 | 0 | 3 | 44 | 227 | 3.018935 |
| P69 | Original rigid | 2.223982 | 2 | 10 | 56 | 219 | 3.086132 |

Protein values are the same in both contexts because the exact protein rows and
ligand coordinates are unchanged. Companion values apply only to occupied.
Neither companion heavy-pair population contains a pair <3 angstrom.

The full set of original-rigid heavy pairs below 2.5 angstrom is:

| Ligand/source index | Ligand atom/type | Protein chain/group/atom/type | Earlier reference (angstrom) | Original rigid (angstrom) |
| --- | --- | --- | ---: | ---: |
| P59/16 | O17/OA | A ARG61 NH1/N | 2.537896 | 2.389969 |
| P59/16 | O17/OA | A GLN78 NE2/N | 2.950850 | 2.439326 |
| P69/4 | C5/A | A GLN116 OE1/OA | 2.942091 | 2.223982 |
| P69/16 | O17/OA | A TYR149 OH/OA | 2.796309 | 2.420689 |

These are explicit native prepared-input identities; the type A means the
original AutoDock aromatic-carbon type. No hydrogen bond or steric-clash
classification is assigned. P69 also has source21 C22/A–GLN116 H/HD at
2.260521 angstrom versus 2.590783, and its source29 H30/HD–companion C21/A
at 2.419509 versus 3.100838. P59's shortest all-atom protein distance is
O17/OA–GLN78 HE21/HD, 1.608495 versus 2.136099 angstrom. The notebook and
raw archive retain every original-rigid pair under 2.5, including H classes.

## Association with existing scores and limits

| Ligand | Context | Saved rigid-minus-reference total (kcal/mol) | Saved ligand-inter difference (kcal/mol) |
| --- | --- | ---: | ---: |
| P59 | Sham | +2.043 | +2.281 |
| P59 | Occupied | +1.983 | +2.215 |
| P69 | Sham | +7.960 | +8.890 |
| P69 | Occupied | +7.832 | +8.748 |

P69's large score difference already exists without the fixed companion.
Its short heavy protein distances identify GLN116/TYR149 as concrete geometry
candidates for a future controlled sensitivity experiment. They do not prove
that either pair contributes a particular score term or causes the difference.
P59 also has two heavy pairs <2.5 angstrom but a smaller score change; that
threshold count alone does not establish an energy explanation. Companion
heavy minima above 3 angstrom do not exclude effects of other pairs or H.

A descriptive distance bin is not an interaction definition. No radii,
scoring kernel, atom-pair energy decomposition, causal attribution or production
remedy is introduced. The constructed points remain unrelaxed and are not
returned poses or torsion/energy optima. One complex and two ligands do not
establish affinity, cooperativity, scientific preparation correctness or a
general torsion/H/ranking policy.

A next bounded candidate is a prespecified local rigid-displacement score
control preserving each arm's original geometry and H, to measure local
sensitivity. It requires its own fixed offsets, maps, retained full population
and interpretation before execution; it must not claim to optimize docking
or fix the identified pairs. It is not executed in this diagnostic.

## Evidence and validation scope

Gzip SHA256:
`84ad1212925bd0765f99b5e9a8932d5b7976e887f51a14964ec295b501aa5490`.
Uncompressed JSON SHA256:
`f6765c5daa0c09923058c399b10e295f664aee266b1791558f9a4e6454425098`.
The original producer, all prior archives and scientific/native inputs remain
unchanged. Provider/source/native authentication covers the preserved
MolSysMT5bd893c85 profile and public cross-system distance/PDBQT routes.
Source inspection and finite executed compatibility are not newer-provider
qualification, a fresh native build or public/platform admission.

Local guards exercise exact saved axes, both ROOT orders, all distances,
current and pm/fs/degree plus inferred-string policies, unchanged inputs,
absence of new search/scoring, receptor/map drift and strict boundary counts.
Local validation passes **86 distinct tests** (78 relevant existing boundaries
plus eight new guards), the three-cell executed notebook, Ruff, reporting
indexes, seven registered guide routes and 67 local links. The checkpoint
records those results before commit; later terminal CI receipts belong in the owning issues.
Existing provider #215/#352/#353/#349/#357 and MolSysSuite #31/#106 ownership
and removal conditions remain unchanged. No new provider limitation was found;
no sibling source was edited or upgraded. #17/#6/#33 remain partial/open.
