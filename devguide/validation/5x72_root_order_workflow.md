# Independent 5X72 ROOT-order challenge

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17) and
[#6](https://github.com/uibcdf/dockingmt/issues/6) own this finite follow-up to
the [1IEP conformer challenge](1iep_conformer_workflow.md). The
[prespecified plan](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6080145389)
predates docking searches. The [driver](../../devtools/qualify_5x72_root_order.py),
[raw observations](data/5x72_root_order/audit_2026-10-09.json.gz),
[saved-result notebook](5x72_root_order_workflow_2026-10-09.ipynb),
[local checkpoint](data/5x72_root_order/checkpoint_2026-10-09.json) and
[guards](../../tests/test_5x72_root_order_workflow.py) retain the actual
submitted inputs, all returned poses, reference correspondence and measured
heavy-atom positional RMSDs.

## Reference roles and identity

[RCSB 5X72](https://www.rcsb.org/structure/5X72) records the PDE-delta complex
with both P59 (R) and P69 (S). They occupy different experimental sites. The
original 24-heavy-atom SDFs match the P59 A201 and P69 A202 instances of
`5x72.pdb` exactly, in the common receptor coordinate frame. All five additional
inputs come unchanged from the same pinned AutoDock-Vina commit
`3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`; their paths, digests and Apache 2.0
attribution are in the [fixture inventory](../../tests/data/vina_torsions/README.md).

The previously retained `p59H.sdf`/`p69H.sdf` files contain prepared 39-atom
conformations near the origin. They are **not experimental geometry references**.
The explicitly selected native -> RDKit -> native bridge supplies their chemical
representation, preserving coordinates within 1e-12 angstrom. Source snapshots
and preparation audits retain that choice; it is not silent aromatic normalization
or template assignment to the original native SDF.

The original crystal SDFs have unversioned counts lines. The public native reader
rejects this dialect at the qualified source, as already tracked for 1S63 in
[MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215#issuecomment-6080146217).
The driver explicitly reads these unchanged references with RDKit, then converts
them through the public MolSysMT adapter. RDKit warns that an untagged 2D record
has nonzero Z coordinates and recognizes 3D; no header or coordinates are repaired.
MolSysMT reads the independent PDB with `get_missing_bonds=False`, without bond
inference. No sibling implementation is edited.

For this finite pair, the first 24 prepared-source indices correspond to the
24 original reference indices. The driver checks elements, all 27 indexed heavy
graph edges, stereocenter R/S at source index 7, and original SDF coordinate
equality to the named PDB atoms. The fixed name sequence is
`FAX CAS CAT CAU CAV CAW CAL CAH NAG CAE CAD CAC CAB CAA CAF CAJ OAM NAI CAK CAN CAO CAP CAQ CAR`.
This declared, independently verified fixture correspondence is not a general
molecular identity matcher. There is no pose-dependent correspondence, alignment
or symmetry correction, including the chemically symmetric phenyl-ring positions.

## Prespecified experiment

Each ligand uses named Gasteiger-Marsili charges, named AutoDock4
`chemical_environment` types, the unchanged explicit H inventory and cuts
`(6,7)`/`(17,18)`. The existing preparation tools retain 25 atoms: 24 heavy atoms
and polar H29. Fourteen nonpolar H charges are merged. Two branches and three
rigid fragments remain unchanged. Charge consistency and successful parser
admission do not establish preparation readiness.

The native ROOT has source indices `[7,8,9,10,11,12,13,14,15,16,17,29]`.
The control keeps source atom 7 (C) first and reverses only the other eleven
existing ROOT ATOM lines. Serial IDs, labels, charges/types, coordinates, ROOT
membership, branch records, torsional degrees of freedom and every other line
byte remain equal within each pair. First-atom coordinates and rigid-body origin
stay equal within each pair, but differ between the two starting conformations.
The operation is a literal fixture permutation, not a new writer or rerooting API.

The matrix is two ligands x two orders x seeds 7/42/2026 x exhaustiveness 1/8:
**24 new searches**. Vina 1.2.7 uses CPU 1 and five requested poses. Each of four
process arms retains a checkpoint after every completed search. No historical
1IEP observation is reused or counted in this scientific matrix. Separate software
guards execute their own bounded live calls.

The externally prepared rigid 5X72 receptor contains 1,481 PDBQT atoms. The
authenticated solution box uses center `(-15,15,129)` angstrom and dimensions
`(30,24,24)` angstrom, covering both experimental sites. The
[current multiple-ligand tutorial](https://autodock-vina.readthedocs.io/en/latest/docking_multiple_ligands.html)
contains a conflicting text snippet with the 1IEP center/dimensions; the pinned
solution file and its actual coordinates control this experiment. No box is
selected from search outcomes.

Each search docks **one ligand**, with the other experimental occupant absent.
It does not reproduce the upstream simultaneous-ligand experiment. Both input
geometries lie outside the original receptor box. Search admission is measured
separately from fixed-input scoring admission; no fixed-initial score, placement,
minimization or conformer selection is requested.

Every returned pose is evaluated against its own experimental 24-heavy-atom
instance through the explicit written -> prepared-source -> reference map.
Public MolSysMT `structure.get_rmsd` measures positional RMSD in this mapped
population, with independent NumPy recomputation and the existing inclusive
2.5 angstrom cutoff. Full 25-atom docking outputs remain unchanged. No experimental
hydrogen coordinate is manufactured to satisfy the full-inventory public
DockingMT evaluation contract. First-pose and returned-set recovery are separate
observations; scores retain kcal/mol units.

## Observations and interpretation — 2026-10-09

All **24 searches** complete and retain **99 returned poses**. Results under
the prespecified positional criterion are:

| Ligand | Written order | First-pose recovery | Returned-set recovery | First heavy RMSD range (angstrom) |
| --- | --- | ---: | ---: | ---: |
| P59 | Native | 0/6 | 3/6 | 9.8777–9.9106 |
| P59 | First fixed | 0/6 | 4/6 | 9.8893–9.9237 |
| P69 | Native | 0/6 | 0/6 | 5.6469–16.5991 |
| P69 | First fixed | 0/6 | 0/6 | 5.6498–5.6530 |

For P59, all three exhaustiveness-8 cells return a near-reference pose in both
orders; the additional first-fixed observation is seed 42 at exhaustiveness 1.
The closest P59 RMSDs in recovered cells are 1.1658–1.2004 angstrom. These poses
are **not ranked first** by the executed Vina protocol. P69's closest RMSD across
all returned poses is 3.8594 angstrom, above the unchanged criterion. All cells,
including poorer poses, remain in the archive and notebook table.

This independent complex does not reproduce the favorable six-of-six first-pose
observation of the original bound-like 1IEP control. ROOT-order changes affect
individual searches here, but neither order produces a near-reference first pose.
The P59 returned-set difference is one observed cell, not an estimated recovery
probability. Increasing effort changes P59 returned-set coverage in this finite
matrix without correcting the first-pose ranking result.

Experimental co-occupancy, the vacant other site, prepared versus experimental
conformation, chemical/protein preparation and scoring/ranking remain potential
contributors. This experiment does not isolate those causes or assign energies
to binding affinities. It cannot establish stereoselectivity, simultaneous-ligand
behavior, convergence or a default ROOT/torsion policy. Subsequent work should
control the experimental occupancy and distinguish sampling from ranking before
expanding automatic policy claims. #17/#6 remain partial and open.


## Reproduction and producer boundaries

Use the preserved Python 3.14.7 `molsyssuite@uibcdf_3.14` source profile:
MolSysMT `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, ArgDigest checkout input
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e` (annotated tag targeting
`57447cc4ec1f7ce85078f8a939892efd075bc919`), MolSysViewer Python 3.14 source
`ec4c71e574d798b7c8675b7e7e983da878ce9889`, RDKit 2026.03.1 and Vina 1.2.7.
Scientific execution authenticates preserved versions/source/native bytes, adding
the exercised reference adapters and RMSD source to the proof. These are new
observations from the existing profile, not a fresh native build or installed
artifact qualification. The archive records its base commit and driver/core/helper
hashes; the owning issues attach the actual scientific producer commit later.

```bash
python -m devtools.qualify_5x72_root_order --arm p59_native --output /tmp/5x72-p59-native.json.gz
python -m devtools.qualify_5x72_root_order --arm p59_first_fixed --output /tmp/5x72-p59-fixed.json.gz
python -m devtools.qualify_5x72_root_order --arm p69_native --output /tmp/5x72-p69-native.json.gz
python -m devtools.qualify_5x72_root_order --arm p69_first_fixed --output /tmp/5x72-p69-fixed.json.gz
python -m devtools.qualify_5x72_root_order --parts /tmp/5x72-p59-native.json.gz /tmp/5x72-p59-fixed.json.gz /tmp/5x72-p69-native.json.gz /tmp/5x72-p69-fixed.json.gz --output /tmp/5x72-complete.json.gz
python -m pytest --receptor=llm tests/test_5x72_root_order_workflow.py
```

The last assembly authenticates all four complete arms and the exact declared
24 cells before retaining a combined archive. Use new task-owned outputs when
rerunning; do not overwrite the original scientific record. Portable tests compare
current-runtime annotations within each input pair, while saved-output tests use
the original captured bytes. They do not require historical distribution version
remarks or promise stochastic recovery on another build.

The notebook reads saved observations only, checks all 24 cells and re-evaluates
all saved poses under pm/fs. Its temporary kernel explicitly selects the qualified
interpreter, shuts down and removes its managed directory after execution.
Local and hosted gate receipts remain distinct from the scientific search producer.

The scoped suite refresh preserves clean but behind MolSysMT/ArgDigest/viewer
worktrees. Historical 1IEP archives, source/native identities, installed artifacts,
public dependency closure and wider-platform admission remain separate. Task-owned
downloads, original per-arm archives and receipts are retained for issue follow-up;
no shared resources or human files are cleaned.

## Local qualification — 2026-10-09

All **155 distinct selected tests pass without skips**: four new input/live/version
annotation guards in 36.06 s, one saved-24-cell guard in 5.68 s, and 150 existing
reference, torsion, charge/type, format, evaluation and reporting guards in
288.22 s. The broader selected scope retains 86 existing provider warnings
(46 structural off-axis drops, 39 legacy H5MSM reads and one structural-attribute
drop). Unchanged original crystal SDFs also retain RDKit's 2D/3D diagnostic.
The notebook executes three saved-result cells without repeating searches;
kernel shutdown and managed-directory removal are verified.

Ruff lint/format (136 Python files), regenerated/current report indexes,
component-guide routing, changed local links, input/source/native/archive hashes
and diff checks pass. The original local checkpoint predates commit/hosted CI;
the owning issues retain later exact-head outcomes. The five new scientific
workflow guards do not require historical runtime-version REMARK strings, and
do not assert stochastic recovery on another installation.
