# Fixed-P59 reciprocal control for P69 in 5X72

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17),
[#6](https://github.com/uibcdf/dockingmt/issues/6) and
[#33](https://github.com/uibcdf/dockingmt/issues/33) own this bounded reciprocal
of the [fixed-P69 control](5x72_occupancy_workflow.md). The
[prespecified protocol](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6088973811)
precedes every new search and fixed evaluation. The
[driver](../../devtools/qualify_5x72_reciprocal.py),
[raw archive](data/5x72_reciprocal/audit_2026-10-09.json.gz),
[executed notebook](5x72_reciprocal_workflow_2026-10-09.ipynb),
[local checkpoint](data/5x72_reciprocal/checkpoint_2026-10-09.json) and
[guards](../../tests/test_5x72_reciprocal_workflow.py) retain all populations.

## Preparation and controlled intervention

P59 remains rigid at its original experimental heavy coordinates while P69
alone is searched. The original protein-only independent experiment is an
authenticated baseline, not a repeated search population. Its unchanged gzip
SHA256 is `2129d7eed2b73bcf90737b2a6c722e3b8e9269abeba0ca3b1444df51f046634e`.
P69's prepared hydrogenated near-origin geometry is not its experimental
reference: the independent heavy SDF and named PDB instance supply that reference.

The existing finite occupancy helper now accepts either explicitly named 5X72
companion and searched ligand; original defaults stay fixed P69/search P59.
It reuses public MolSysMT fixed-state H addition, named charge/type assignment,
prepared native composition and rigid/tree writing, plus DockingMT preparation,
search, fixed scoring and source-mapped measurement. No molecular writer,
merger or matching algorithm is duplicated in the reciprocal driver.

The fixed P59 reference uses the existing explicit RDKit bridge for the original
unversioned SDF dialect, owned by
[MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215).
Public fixed-chemical-state H addition uses RDKit, `pH=None`, no optimization,
and appends 15 H while preserving all 24 heavy coordinates and the R stereocenter.
Gasteiger-Marsili charges and AutoDock4 chemical-environment typing feed existing
rigid receptor preparation. It retains 24 heavy atoms and polar H29, merging
fourteen nonpolar H charges. Charge consistency passes; readiness remains
unassessed. Generated H orientation is a model assumption, not experimental
geometry or environmental refinement.

Public native PDBQT conversion reads the already prepared protein and companion
projections. Companion serials are explicitly 1482..1506. Public detached
`msm.add(..., keep_ids=True, attribute_policy='strict')` composes their atom axes,
coordinates, charges and labels. The finite checked A/A chain declaration through
public `msm.set` remains owned by
[MolSysMT #353](https://github.com/uibcdf/molsysmt/issues/353); review it at the next
provider qualification or issue closure and remove it when `add` preserves those
IDs unaided. [MolSysMT #352](https://github.com/uibcdf/molsysmt/issues/352) retains
the recorded native mechanics-merge defect. Neither sibling source nor general
identity/composition policy changes.

The same public rigid writer produces a protein-only **sham** (1,481 atoms) and
protein plus fixed-P59 **occupied** receptor (1,506 atoms), without torsion records.
Every original protein serial, name, group name/ID, chain ID, coordinate, numerical
charge and AD4 label stays exactly equal in both arms. The sham controls normalized
padding and the added END record. These prepared PDBQT projections do not assert
complete covalent chemistry; original chemical and H reports remain separate.

## Prespecified populations and interpretation

The 24 new searches cross two receptor arms, two unchanged P69 ROOT orders,
seeds 7/42/2026 and exhaustiveness 1/8, using Vina 1.2.7, CPU 1 and five requested
poses. The pinned box is center (-15,15,129) and size (30,24,24) angstrom.
P69 chemistry, starting conformer, charges/types, two selected cuts, atom maps,
native/fixed-first bytes and reference remain those of the original independent
experiment. No outcome-selected retry, parameter or reference change is allowed.

All returned poses use inclusive <=2.5 angstrom positional RMSD against P69's
24 experimental heavy atoms, without fitting or symmetry correction. Public
MolSysMT and independent NumPy calculations agree. First-ranked and any-returned
recovery are separate observations. Requested pose count is a maximum, not a
guaranteed population size or probability estimate.

Every new geometry is scored unchanged in both receptor contexts. Public native
writing retains the original tree, serial axis, names, types and charges; fixed
scoring preserves rank, coordinates and previous docking scores. All eight fixed
components and exact submitted bytes/hashes are retained. Lowest fixed total in
each declared retained set is a diagnostic with original-rank tie breaking, not
a change to public ranking or score-comparability policy. `Vina.score` and
`Vina.energies` components are distinct and their totals are not equated.

All 49 historical P69 poses from 12 cells are additionally scored in original
external-protein and sham contexts: 98 serialization evaluations. They remain
historical searches, distinct from all 24 new searches and software guard calls.
Every corresponding new sham pose and docking component is checked, and every
historical eight-component fixed-score pair is retained without discarding a
mismatch.

## Observations

The 24 searches return **78 poses**: 49 sham and 29 occupied. All 78 geometries
are evaluated unchanged in both contexts (156 fixed evaluations), plus the
98 historical serialization evaluations: **254 scientific fixed evaluations**.

| Receptor / P69 ROOT order | First-ranked recovery | Any-returned recovery | Lowest fixed-score recovery: sham | Lowest fixed-score recovery: occupied |
| --- | ---: | ---: | ---: | ---: |
| Protein-only sham / native | 0/6 | 0/6 | 0/6 | 0/6 |
| Protein-only sham / fixed-first | 0/6 | 0/6 | 0/6 | 0/6 |
| Fixed P59 / native | 0/6 | 4/6 | 0/6 | 0/6 |
| Fixed P59 / fixed-first | 0/6 | 3/6 | 0/6 | 0/6 |

Fixed P59 changes any-returned P69 recovery from **0/12 to 7/12**, including all
six occupied exhaustiveness-8 cells. Native seed 7 is the only recovered low-effort
cell. The closest occupied pose is 1.5374 angstrom; the closest sham pose is
3.8594 angstrom. None of the 24 first poses is recovered. Ten occupied first
poses have RMSD 5.5202–5.5321 angstrom; the two seed-2026 low-effort cells have
first RMSD 16.6320–16.6331 angstrom. All twelve occupied cells are retained.

Every recovered occupied set still selects a nonrecovered geometry as the lowest
fixed score in either receptor context. The occupied-context diagnostic selects
original rank 1 in all twelve occupied cells. Thus a near-reference geometry is
sampled and retained in seven cells but is not preferred by either original
docking rank or the declared frozen-score diagnostic. Five occupied sets contain
no recovered pose. These are distinct retained-population observations; absence
from a returned set is not proof that an unretained trajectory never visited it.

The reciprocal differs from the earlier P59 result: fixed P69 recovered first
P59 in 10/12 cells, whereas fixed P59 does not recover first P69 here. Occupancy
alone therefore does not remove the measured P69 ranking discrepancy. The finite
result motivates a separate reference-geometry/score diagnostic with an explicit
H/atom map and prespecified local-optimization policy, before changing production
preparation, scoring, ROOT order or search defaults. No such extra optimization or
reference scoring belongs to this matrix.

The 49 new sham pose geometries and every retained docking component exactly
match their historical counterparts. All 49 original-vs-sham fixed evaluations
also agree across all eight components. Serialization therefore accounts for
none of the measured differences in these populations. The reciprocal gzip
SHA256 is `323a5cb7a826368eb4914219c3a29c2fdf440956a792f9ebf7812e2cc228083d`;
the uncompressed JSON SHA256 is
`d61ecc11544e65e7548f743627995ed585607e78bf128b8b9f4cf3d53ca7e127`.

## Local execution and guards

Six reciprocal guards cover both current dataframe string policies, fixed P59
identity/coordinates, unchanged protein fields, both P69 frozen trees under
pm/fs, one bounded live search plus frozen evaluations and the complete saved
matrix/history. They add no stochastic recovery promise to CI. Five existing
occupancy guards and 207 affected scoring, native-format, ROOT-order, RMSD,
named-charge/type and reporting boundary tests also pass: **218 distinct selected
tests**, no skips. The selected sessions pass 153 tests in 170.77 s, 64 in
53.35 s and the saved-population guard in 7.78 s; their JUnit identities remain
in the checkpoint.

The notebook executes three saved-result cells without docking, scoring,
preparation or optimization. It independently verifies all 78 heavy-atom RMSDs,
all 254 captured frozen evaluations and unchanged historical fixed-score pairs.
Its managed kernel shuts down and its temporary directory is removed. Ruff
lint/format (140 files), reporting/index/link, synchronized-guide and diff checks
are recorded separately from scientific evidence. The local checkpoint precedes
commit; later exact-head hosted Python 3.11–3.14 source CI belongs in owning issues.

## Provenance and scope

The original MolSysMT source profile is
`5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, with the preserved native artifact
SHA256 `c535c7d2f0e2a92b6ebf8298a60b19e4b5555467b4aa087e9563c6760619827e`.
ArgDigest source is `57447cc4ec1f7ce85078f8a939892efd075bc919`; Viewer Py3.14
source is `ec4c71e574d798b7c8675b7e7e983da878ce9889`. The driver authenticates
original provider/core/ROOT-helper bytes and records the extended occupancy and
new reciprocal helper digests separately. Historical producer Git blobs and
separately preserved generated version/native bytes remain their own identities;
the old archives, checkpoints and notebooks are unchanged.

The refreshed bounded inventory reports clean/current DockingMT and clean
MolSysMT/ArgDigest/Viewer worktrees behind origin by 24/3/67 commits. They are
explicitly preserved. Newer provider heads, new builds, full installed-artifact
qualification and public/platform admission are not claimed. Portable guards use
independently verified current-runtime reference annotations, including inferred
string policy; strict scientific production requires the historical snapshots.

This is one rigid-environment model with generated H and declared charge/type
assumptions. It cannot establish affinity, cooperativity, stereoselectivity,
general ROOT/H/preparation policy, receptor relaxation, simultaneous docking,
recovery probability or convergence. #17/#6/#33 remain partial/open.

## Current-policy guard correction — 2026-10-09

The original [CI 37990568260](https://github.com/uibcdf/dockingmt/actions/runs/37990568260)
fails one reciprocal guard in each minor: 1,020 pass and the forced
`future.infer_string=False` case raises `assignment destination is read-only`
in the pinned provider's PDB COMPND name restoration. The guard unintentionally
requires an optional legacy-string policy under Pandas 3 Copy-on-Write, beyond
the ordinary runtime profile used by this experiment. The same failure is
reproduced locally with Pandas 2.3.3, Copy-on-Write enabled and inferred strings
disabled, through direct public PDB conversion; no search or scoring is involved.

This is the already resolved
[MolSysMT #349](https://github.com/uibcdf/molsysmt/issues/349): provider fix
`eab7aeb79` uses a copied molecule-name array. Fresh origin source contains that
fix, but the immutable original `5bd893c85` pin does not. No current-provider
regression, new provider build or migration is inferred. #33 retains receiving
qualification; the provider receives this additional old-pin evidence in #349.

The portable guard now compares **current application string policy** (without
changing it) and explicitly **inferred strings**. On local Pandas 2 these exercise
object and string annotations; on hosted Pandas 3 they retain its supported
ordinary profile. Each still checks the independent reference, R identity,
protein fields and experimental heavy coordinates. No provider reader workaround,
policy reset, silent xfail or scientific equivalence relaxation is introduced.

Scientific producer `3b8258f8a34fbb32dc8d5d09207553bff4b47bf5`, its 24 searches,
78 poses, 254 fixed evaluations, archive, notebook and original 218-test local
checkpoint stay unchanged. The later test correction has its own source identity;
fresh exact-head source CI is required and its terminal receipt belongs in owning
issues separately from the failed run and original local capture.

All six corrected reciprocal guards pass locally in 48.82 s. The unchanged
212 applicable existing occupancy/boundary results remain valid, giving 218
distinct currently applicable local tests. Lint, format, reporting/index/link,
canonical-guide routing and diff checks pass; these later results do not rewrite
the original pre-commit checkpoint.
