# External PDBQT adapter check: 1IEP

This case exercises DockingMT's Vina adapter with a flexible ligand and receptor
already prepared by the [official AutoDock Vina basic-docking
example](https://github.com/ccsb-scripps/AutoDock-Vina/blob/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/docs/source/docking_basic.rst).
It checks backend-input identity, pose atom order and the documented search box.
The source ligand SDF is converted through RDKit to a MolSysMT molecular system.
For this fixed, aligned example, element and coordinate checks map each prepared
PDBQT atom to one source atom. The pose metric uses that molecular source as its
reference, while the ligand graph and omitted atoms remain identifiable.
The external chemistry is recorded as `unassessed`; DockingMT's own preparation
remains provisional under [issue #5](https://github.com/uibcdf/dockingmt/issues/5).

## Pinned inputs

Source: `ccsb-scripps/AutoDock-Vina` commit
`3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`,
`example/basic_docking/solution/`. The files are fetched from upstream rather
than copied into DockingMT.

| File | SHA-256 |
| --- | --- |
| `1iep_receptor.pdbqt` | `f13cf3b36f61d87c3b58983e0b8ecf1c3456a685eb86dfe9ccfb139c7bdc2586` |
| `1iep_ligand.pdbqt` | `15fb35648d8c18c70317842f3a0631b73a19429c710a037ab07310084d579bb8` |
| `1iep_ligand.sdf` | `051b8742c32adc05c07fb486a4e7c9327f84e131cee33ac4e6a568d07553eb38` |

```bash
curl -L --fail -o /tmp/1iep_receptor.pdbqt https://raw.githubusercontent.com/ccsb-scripps/AutoDock-Vina/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/basic_docking/solution/1iep_receptor.pdbqt
curl -L --fail -o /tmp/1iep_ligand.pdbqt https://raw.githubusercontent.com/ccsb-scripps/AutoDock-Vina/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/basic_docking/solution/1iep_ligand.pdbqt
curl -L --fail -o /tmp/1iep_ligand.sdf https://raw.githubusercontent.com/ccsb-scripps/AutoDock-Vina/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/basic_docking/solution/1iep_ligand.sdf
python devtools/validate_1iep_pdbqt.py --receptor /tmp/1iep_receptor.pdbqt --ligand /tmp/1iep_ligand.pdbqt --ligand-source /tmp/1iep_ligand.sdf --manifest /tmp/1iep-manifest.json --report /tmp/1iep-report.json
```

The script refuses files with different hashes. Its manifest retains the exact
PDBQT bytes submitted to Vina; the concise report records their hashes,
software versions, protocol, source-to-PDBQT atom indices, omitted atoms and pose
metrics. The positional map is valid for this pinned bound-ligand pair; general
source-to-PDBQT correspondence belongs to MolSysMT
[issues #223](https://github.com/uibcdf/molsysmt/issues/223) and
[#226](https://github.com/uibcdf/molsysmt/issues/226).

## Measured result, 2026-09-26

Vina 1.2.7, scoring `vina`, seed 42, one CPU, exhaustiveness 1, five requested
poses. The box is centered at `(15.190, 53.903, 16.917)` Å and has dimensions
`(20, 20, 20)` Å, as in the official tutorial. The adapter rounds projected
box numbers to six decimal places after unit conversion and records the exact
values sent to Vina.

The original adapter measurement used clean DockingMT source commit
`c519cca60a451c100def46ec448c4d42889eff7b` and MolSysMT
`0.21.0+606.ga03eb4bf6`. The editable DockingMT installation reported a
stale generated package version (`0.0.0+14.g25b6e0b.dirty`); the clean source
commit in the report identifies the implementation tested.

The source SDF contains 69 atoms and 73 bonds, which remain in the MolSysMT
conversion. The prepared ligand PDBQT retains 40 atoms, including
37 heavy atoms, and omits 29 source hydrogens. All retained atoms have unique
same-element coordinate matches within 0.02 Å; their order differs from the
SDF. Vina returned one pose. Its PDBQT atom labels matched the input order;
Vina's separate coordinate array contained the same coordinates in a different
order. The submitted input hashes matched the pinned PDBQT hashes.

| Rank | Vina score (kcal/mol) | Heavy-atom positional RMSD (Å) |
| ---: | ---: | ---: |
| 1 | -13.286 | 0.897 |

RMSD compares mapped heavy PDBQT atoms against the upstream SDF ligand converted
to MolSysMT, without alignment or symmetry correction. The source-linked rerun
returned the same score and RMSD as the original adapter measurement. The result
demonstrates the adapter's ability to use the external flexible ligand and
recover a near-native pose in this seeded run. It does not establish general
success rates or validate the input preparation scheme. The official tutorial
describes 1IEP as a challenging ligand and recommends greater exhaustiveness
for consistent docking.

The check exposed two adapter defects: [#12](https://github.com/uibcdf/dockingmt/issues/12)
concerns coordinate-array ordering, and [#13](https://github.com/uibcdf/dockingmt/issues/13)
concerns box numbers after unit conversion. Before the box correction, the
same nominal box reached Vina as `19.999999999999996` Å per side and yielded
two poses with best score -7.531 kcal/mol. Direct Vina reproduced that result
with those exact values; its internal reason for this sensitivity remains
unconfirmed.
