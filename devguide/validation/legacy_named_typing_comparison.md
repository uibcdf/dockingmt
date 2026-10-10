# Legacy and named AutoDock typing comparison

The [2026-10-10 compatibility implementation](required_named_typing.md) now
requires named typing. This document and its producer retain the original
pre-change comparison; replay requires its recorded consumer source.

The 2026-10-10 comparison under [DockingMT #5](https://github.com/uibcdf/dockingmt/issues/5)
and [#49](https://github.com/uibcdf/dockingmt/issues/49) measures the compatibility
cost of retiring consumer typing. **Fourteen of 23 paired preparations change
labels or retained H.** MolSysMT's explicit named scheme already supplies the
classification; DockingMT needs no replacement molecular algorithm. Preparation
defaults are unchanged in this evidence slice.

## Controlled method

Both existing preparation paths receive the same untyped native source, declared
pose, indexed H and assigned Gasteiger–Marsili charges. The legacy call has no
`typing_options`; the named call requests
`{'typing_scheme': 'autodock4', 'method': 'chemical_environment'}`. Source-index
maps join supplied identities; names, proximity and counts do not infer identity.
Neither call changes the source. Each retained position equals its declared source
position within 1e-12 angstrom; each preparation conserves source total charge
within 1e-10 e and passes the existing attributed charge audit.

Nine declared chemical controls run in both ligand and receptor roles (18 pairs).
The existing public fixed-state H tool materializes their H before assigning
charges, without selecting protonation. Their poses are synthetic test geometry.
Native 181L BNZ uses the existing explicitly corresponded benzene template, fixed
H inventory and charge stages. The original hydrogenated 5X72 P59/P69 SDFs use
public native reading with `stereo_engine='rdkit', discard_properties=True` and
charge assignment. These three real-input cases run in ligand role. Two further
methylamine pairs exercise a pm/coulomb policy. No typing comparison uses a newly
written classifier, molecular reader, projection, repair or geometry routine.

## Observations

| Declared case | Legacy → named result | Inventory consequence |
| --- | --- | --- |
| Neutral methylamine | N → NA | Same four retained atoms |
| Protonated methylamine | N → N | Same five retained atoms |
| Amide | N → N | Same six retained atoms |
| Pyridine | N → NA | Same six retained atoms |
| Pyrrole | N → N | Same six retained atoms |
| Thioether | SA → SA | Same three retained atoms |
| Sulfone | SA → S | Same five retained atoms |
| HF | F unchanged; H classified HD | One → two retained atoms |
| PH3 | P unchanged; three H classified HD | One → four retained atoms |
| Declared 181L BNZ | Six A unchanged | Same six retained atoms |
| Native 5X72 P59 and P69, separately | 18 C → A in each case | Same 25 retained atoms from each 39-atom input |
| Methylamine, pm/coulomb | Same N → NA difference in both roles | Same four retained atoms |

The native 5X72 chemical-state snapshot has null aromaticity entries. The legacy
path does not perceive its complete bond graph and falls back to C. The provider
named scheme classifies the graph; its original attribution and full evaluated
coverage remain in the record. These results measure a representation-dependent
legacy limitation, not an independently established chemical ground truth.

For HF/PH3 the same charge input has different aggregation: legacy H omission
merges all charges onto the heavy atom (0 e total there); named preparation retains
the indexed polar H and its separate charges. Total charge is conserved in both.
One cannot require equal per-atom charge arrays across different retained axes.
The methylamine unit controls reproduce the same labels, inventory and charge
conservation under the alternate policy.

## Input requirements and limits

Four negative controls cover both roles. Methanol with virtual H fails named
preparation with the provider requirement to materialize all H as indexed atoms.
Original PDB-only 181L BNZ fails because connectivity is not declared complete.
Legacy preparation still returns provisional objects for these inputs. No implicit
H addition, graph repair or fallback occurs in the explicit named call.

The unchanged original 1IEP SDF (SHA-256
`051b8742c32adc05c07fb486a4e7c9327f84e131cee33ac4e6a568d07553eb38`)
fails native reading at atom 32's nonzero valence flag. This is the existing subset
limit in [MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215), reproduced
on the adopted provider. It is **excluded from the 23 type comparisons**. Earlier
[1IEP evidence](1iep_flexibility_workflow.md) used its declared existing RDKit
source bridge; this producer introduces no bridge or field stripping. Inspection
of fetched provider `072aa9bdb` still finds that rejection rule, but no runtime
qualification of that newer revision is claimed.

The receptor-role controls are synthetic small molecules, not a native protein
qualification. Experimental `chemical_environment@1`, fixed chemical-state choices
and generated H geometry remain unassessed scientifically. Label agreement or
charge conservation does not qualify protonation, donor/acceptor universality,
AutoDock4 scoring, sampling or affinity. This producer runs no Vina parser, scores,
searches or torsion experiments. The separate 5X72 displacement producer/archive
remain byte-identical and outside this slice.

## Evidence and replay

Original retained files:

- [Raw paired observations](data/typing_comparison/audit_2026-10-10.json.gz),
  SHA-256 `eadbbff0145873634ca14edda90eb076e145ff38bb3a01c208596e540e1ecc8a`.
- [Original producer](data/typing_comparison/producer_2026-10-10.py.txt),
  SHA-256 `c5c192fb7f8be17e7444d9e09aee73952bcd9591607f92b3bcb45f97080f136b`.
- [Producer output, including provider warnings](data/typing_comparison/producer_2026-10-10.log).

The original consumer is `4675486904b73caa2c9e0e72ed17efd3704dc1fc`;
MolSysMT is `739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac`, ArgDigest source
`57447cc4ec1f7ce85078f8a939892efd075bc919`, and Viewer source
`ec4c71e574d798b7c8675b7e7e983da878ce9889`. Python is 3.14.7, RDKit 2026.3.1.
The raw record binds actual import origins, source hashes, original file digests,
source snapshots, charges, maps and provider reports. Archive files of ArgDigest
and Viewer were compared byte-for-byte to their owning committed sources.

This uses isolated source composition in the development Conda environment and
the authenticated unchanged provider native binary (SHA-256
`c535c7d2f0e2a92b6ebf8298a60b19e4b5555467b4aa087e9563c6760619827e`).
It is not a new ordinary-installed candidate or public admission. Preserve the
original source and native receipts; generated provider metadata is distinct from
installation evidence. Sibling worktrees and the shared environment are unchanged.

Replay with that original consumer checkout, the recorded committed provider/
support sources on `PYTHONPATH`, and the same qualified native binary. The producer
verifies source identities and refuses to overwrite output. Paths in the original
record describe the original run; a replay requires available owning Git repositories
for archive verification. For example, from the original consumer checkout:

```bash
python /path/to/producer_2026-10-10.py.txt /tmp/new-typing-comparison.json.gz
```

Existing independent named-type, charge and failure contracts plus reporting
checks pass **89 tests, no skips, 60.98 s**, with 47 provider warnings. The raw
comparison assertions establish this finite experiment; those tests do not turn
its observations into scientific equivalence. No executable product source,
metadata or dependency pin changes in this slice.

## Migration decision

Retire the legacy classifier in a separate compatibility change: require a valid
preassigned named provider report or explicit `typing_options` on molecular inputs.
If neither is supplied, fail with an actionable explanation of the public MolSysMT
route. Do not choose an experimental typing model automatically, materialize H,
repair chemistry or introduce another opt-in consumer classifier. Preserve valid
projected parent labels and source/assignment identities. Charge-model choice and
missing-charge rejection retain their own scope under #5; external prepared
PDBQT and source-free conversion are separate boundaries.

The change needs updated public examples and user-visible failure contracts for
both preparators and automatic engine preparation. Named provider failures must
continue to propagate; the existing provisional Vina policy remains until its
own chemistry acceptance is met. General H/charge projection remains owned by
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223), native writer/order
qualification by #214/#226/#369. Keep consumer #5/#49 partial.
