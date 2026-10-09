# Fixed-P69 control for P59 in 5X72

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17),
[#6](https://github.com/uibcdf/dockingmt/issues/6) and
[#33](https://github.com/uibcdf/dockingmt/issues/33) own this bounded follow-up
to the [independent ROOT-order challenge](5x72_root_order_workflow.md).
The [prespecified protocol](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6087357069)
and [pre-search addendum](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6088303810)
precede all 24 new searches. The
[driver](../../devtools/qualify_5x72_occupancy.py),
[raw observations](data/5x72_occupancy/audit_2026-10-09.json.gz),
[executed notebook](5x72_occupancy_workflow_2026-10-09.ipynb),
[local checkpoint](data/5x72_occupancy/checkpoint_2026-10-09.json) and
[guards](../../tests/test_5x72_occupancy_workflow.py) preserve the actual inputs,
all poses, reference correspondence and frozen evaluations.

## Intervention and preparation

The original independent experiment omitted the other experimental occupant.
Its first-ranked P59 poses lie near the experimental P69 site; that post-hoc
center observation motivated this intervention without changing the heavy-atom
RMSD criterion. P69 stays rigid at its original experimental 24-heavy-atom
coordinates while P59 alone is searched. This is not simultaneous docking or
flexible-receptor support.

The unmodified original P69 SDF uses the existing explicit RDKit reference
bridge for its unversioned dialect, tracked by
[MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215).
Public MolSysMT fixed-chemical-state H addition uses RDKit `addCoords=True`,
`pH=None`, no optimization, and appends 15 hydrogens. The 24 heavy coordinates,
indexed identity and S stereocenter remain unchanged. These H positions are
generated local geometry, not an experimental reference or environmental
refinement. Named Gasteiger-Marsili charges and AutoDock4 chemical-environment
types feed existing DockingMT rigid preparation. It retains 24 heavy atoms and
polar H29; fourteen nonpolar H charges are merged. Charge consistency and parser
admission do not establish readiness; preparation stays unassessed.

The original protein has 1,481 PDBQT atoms. Public MolSysMT reads the already
prepared protein and companion PDBQT projections. The companion receives the
explicit disjoint serial map 1482..1506. Public `msm.add` with `in_place=False`,
`keep_ids=True` and `attribute_policy='strict'` joins their atom axes, coordinates,
charges and AD4 labels without modifying either input. PDBQT projections do not
assert complete covalent chemistry; original chemical/H records remain separate.
Public native PDBQT writing produces a protein-only **sham** and the **occupied**
1,506-atom rigid receptor, with no ROOT/BRANCH/TORSDOF records.

Every original protein atom's serial ID, name, group name/ID, chain ID, coordinates,
numerical charge and AD4 type matches both written arms exactly. The actual text
hash changes because the public writer normalizes column padding and adds END.
The protein-only sham controls that representation change.

Two provider findings are issue-backed; no sibling source is edited:

- [MolSysMT #352](https://github.com/uibcdf/molsysmt/issues/352): public `merge`
  treats bare native charge columns as quantities, then retains the first mechanics
  table's atom-axis length when charges are cleared. Supported public `add` is used
  instead; no downstream molecular merger or writer is introduced.
- [MolSysMT #353](https://github.com/uibcdf/molsysmt/issues/353): `add` preserves
  chain indices but erases chain IDs. For these two one-chain fixtures only, the
  caller checks both A input IDs and the two output indices, then declares
  `['A','A']` through public `msm.set`. DockingMT #17/#33 own this bounded restoration;
  MolSysMT owns the fix. Review at the next provider qualification or issue closure,
  and remove it when add retains these IDs and the guard passes unaided. Both new
  arms preserve the original chain IDs; this does not define general identity repair.

## Prespecified populations and measurement

The matrix is two receptors x two unchanged P59 ROOT orders x seeds 7/42/2026 x
exhaustiveness 1/8: **24 new searches**, Vina 1.2.7, CPU 1, five requested poses.
The native/fixed-first partner bytes, source map, two selected cuts and initial
geometry match the authenticated independent experiment. The pinned box remains
center (-15,15,129) angstrom and size (30,24,24) angstrom. No box, chemical state,
torsion, placement or preparation parameter is selected from these outcomes.
Four process arms checkpoint each of six completed cells; none is replaced by a
retry or a software guard.

All 78 returned poses (50 sham, 28 occupied) are measured against the unchanged
P59 crystal reference. Public MolSysMT positional RMSD uses the explicitly mapped
24 experimental heavy atoms, independently recomputed with NumPy. Recovery is
inclusive <=2.5 angstrom, without alignment or symmetry correction. There is no
experimental H reference. First-ranked and any-returned recovery are distinct.

Every new pose is evaluated unchanged against **both** new receptor arms through
public `dockingmt.score`: **156 fixed-pose evaluations**, no search or optimization.
Public MolSysMT writes the saved coordinates with the original exact serial axis
and two-torsion tree; types, charges, atom order and tree remain checked. Original
rank, identity, geometry and prior docking scores stay detached and unchanged.
All eight fixed-score components and exact submitted input bytes/hashes are kept.

The 12 historical P59 cells and their 50 poses remain authenticated baseline
observations, not new searches. All 50 are additionally scored against the original
external protein and the sham: **100 fixed evaluations**. The full baseline gzip
SHA256 is `2129d7eed2b73bcf90737b2a6c722e3b8e9269abeba0ca3b1444df51f046634e`.
Their new sham search coordinates and all retained docking score components match
the original 50 poses exactly. Original-vs-sham fixed scores also match across
all eight components; this controls serialization in the measured populations.

## Observations

| Receptor / P59 ROOT order | First-ranked recovery | Any-returned recovery | Lowest fixed-score recovery: sham | Lowest fixed-score recovery: occupied |
| --- | ---: | ---: | ---: | ---: |
| Protein-only sham / native | 0/6 | 3/6 | 0/6 | 3/6 |
| Protein-only sham / fixed-first | 0/6 | 4/6 | 0/6 | 4/6 |
| Fixed P69 / native | 5/6 | 5/6 | 5/6 | 5/6 |
| Fixed P69 / fixed-first | 5/6 | 5/6 | 5/6 | 5/6 |

For each retained set and fixed receptor, the table explicitly selects the lowest
fixed total, breaking ties by original rank. This is a finite diagnostic across
declared same-chemistry geometries and receptor context. It does not relax public
score-comparability rules or change public ranking. `Vina.score()` components are
distinct from the post-docking `Vina.energies()` columns; their numerical totals
are not asserted equivalent.

Under the sham environment, none of its twelve first poses is recovered. Its
seven returned sets that already contain a recovered geometry all put a recovered
geometry first under the occupied fixed-score diagnostic. **The geometries do not
move** in that comparison: it demonstrates an empirical scoring preference change
within those retained populations, not additional sampling.

Searching with fixed P69 recovers first-ranked P59 in ten of twelve cells. All six
exhaustiveness-8 cells recover first-ranked P59. The two low-effort failures are
native seed 7 (first/closest RMSD 4.5368 angstrom) and fixed-first seed 2026 (first
13.8116, closest 13.2345 angstrom). No recovered pose is hidden in either returned
set. The fixed-P69 first-pose RMSD in the ten recovered cells is 0.7542–0.7834
angstrom. Returning fewer clustered/energy-window poses is not a recovery-probability
estimate or evidence of convergence.

## Execution, guards and limits

Production authenticates the original source/native profile, versions and all
baseline consumer/provider digests. The temporary source archives disappeared
between preparation probes and were reconstructed from their exact source commits;
the restoration receipt records generated version and preserved native bytes.
MolSysMT source is `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, ArgDigest source
`57447cc4ec1f7ce85078f8a939892efd075bc919`, Viewer Python-3.14 source
`ec4c71e574d798b7c8675b7e7e983da878ce9889`. The preserved native extension SHA256 is
`c535c7d2f0e2a92b6ebf8298a60b19e4b5555467b4aa087e9563c6760619827e`.
Diagnostics made while temporary archives were absent imported local source
8ae160fc93ed; they are not matrix observations. No native build, sibling upgrade,
fresh installed artifact or public/platform admission is claimed.

The guards check fixed-occupant identity, unchanged protein fields, both frozen
trees, one bounded live search and frozen scoring under pm/fs, all 24 saved cells,
all 78 new poses and all 50 historical serialization controls. Portable checks
use current runtime annotations; the scientific producer retains the authenticated
historical bytes. The checkpoint separates selected local checks from later
exact-head hosted CI, which is recorded in owning issues.

This one rigid-environment model establishes that omitted occupancy materially
changes these P59 search and score observations. It does not establish affinities,
cooperativity, stereoselectivity, general ROOT/H/charge policies, experimental H
orientation, receptor relaxation, simultaneous multi-ligand docking, dataset
recovery probability or convergence. P69 is not searched in this control. The
earlier P69 nonrecovery remains open; a reciprocal fixed-P59/P69 experiment would
need its own prespecified protocol. #17/#6/#33 remain partial/open.

## Portable dataframe annotation correction — 2026-10-09

The first hosted [CI 37985766306](https://github.com/uibcdf/dockingmt/actions/runs/37985766306)
fails during setup of three new guards at the historical snapshot comparison.
Pandas 3.0.6 annotates the chemical-state component-name/type columns as `str`,
where the original Pandas 2.3.3 producer captured `object`. Enabling
`future.infer_string=True` locally reproduces exactly these two dtype differences
without changing chemical values or coordinates. A full historical snapshot is
an original-profile check, not portable runtime equivalence.

Portable guards now pass the current runtime's P69 snapshot from `prepare_cases`,
which independently verifies heavy graph, elements, stereocenter, named PDB
instance and crystal coordinates, to `prepare_receptors(reference_snapshot=...)`.
The producer's default still requires the original historical snapshot. The
new regression executes the inferred-string policy, proves strict historical
comparison rejects the changed annotations, and verifies the admitted current
reference retains the protein and companion experimental heavy coordinates.
No generic molecular equivalence operation or public docking policy changes.

The 24 searches, 78 poses, 256 frozen evaluations, archive digest, executed
notebook and original checkpoint remain unchanged at scientific producer
`5fee9c2e5e99eb26ddc98bae529a511eb9d4ea60`. Its source digests refer to that
original commit; the amended helper has its own later source identity. The
five corrected guards plus the unchanged applicable 207 boundary results give
212 distinct locally applicable tests. Owning issues retain the first failed
CI and subsequent exact-head results separately.

## Reciprocal follow-up — 2026-10-09

The separately prespecified [fixed-P59/P69 control](5x72_reciprocal_workflow.md)
now tests the opposite role assignment. Its 24 new searches retain all 78 poses
and 254 frozen evaluations. P69 any-returned recovery changes 0/12 to 7/12,
whereas first-ranked and lowest frozen-score recovery stay zero. This bounds
the earlier favorable P59 result; the original producer/archive/checkpoint and
notebook above remain unchanged. The reused helper's later role parameters have
their own source digest in the reciprocal archive, preserving original defaults.
