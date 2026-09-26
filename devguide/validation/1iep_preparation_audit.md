# Native preparation audit: 1IEP

This audit compares DockingMT's native MolSysMT-based preparation with the aligned
PDBQT files published in the [AutoDock Vina basic-docking example](https://github.com/ccsb-scripps/AutoDock-Vina/blob/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/docs/source/docking_basic.rst).
It identifies the chemistry still needed for [DockingMT #5](https://github.com/uibcdf/dockingmt/issues/5).
The published PDBQT is a comparison input, not an independently validated chemical
ground truth. No Meeko package is used or installed by this audit.

## Reproduce

Use AutoDock Vina commit `3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`.
The files come from `example/basic_docking/solution/`; the audit checks their SHA-256
digests before processing. It needs MolSysMT and RDKit to read the source molecules;
the optional parser check also needs Vina.

```bash
curl -L --fail -o /tmp/1iep_receptorH.pdb https://raw.githubusercontent.com/ccsb-scripps/AutoDock-Vina/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/basic_docking/solution/1iep_receptorH.pdb
curl -L --fail -o /tmp/1iep_ligand.sdf https://raw.githubusercontent.com/ccsb-scripps/AutoDock-Vina/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/basic_docking/solution/1iep_ligand.sdf
curl -L --fail -o /tmp/1iep_receptor.pdbqt https://raw.githubusercontent.com/ccsb-scripps/AutoDock-Vina/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/basic_docking/solution/1iep_receptor.pdbqt
curl -L --fail -o /tmp/1iep_ligand.pdbqt https://raw.githubusercontent.com/ccsb-scripps/AutoDock-Vina/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example/basic_docking/solution/1iep_ligand.pdbqt
python -m devtools.audit_1iep_preparation --source-receptor /tmp/1iep_receptorH.pdb --source-ligand /tmp/1iep_ligand.sdf --reference-receptor /tmp/1iep_receptor.pdbqt --reference-ligand /tmp/1iep_ligand.pdbqt --report /tmp/1iep-preparation-audit.json --check-vina-parser
```

The script converts both sources to `molsysmt.MolSys`, selects the receptor protein,
uses `molsysmt.build.get_missing_bonds` to recover two source hydrogen bonds, then
calls DockingMT's public preparation functions. It also maps the seven published
`BRANCH` bonds back to source-ligand atom indices and requests those bonds explicitly
for a second, flexible native projection. This tests the writer with a known selection;
it does not infer a general torsion policy. The coordinate comparison is exact at
PDBQT's 0.001 Å precision. It is valid only for these pinned, already aligned inputs;
matching coordinates does not prove chemical equivalence or general atom mapping.

## Measured result, 2026-09-26

| Observation | Ligand | Receptor |
| --- | ---: | ---: |
| Source atoms selected | 69 | 4,412 |
| PDBQT atoms in each preparation | 40 | 2,702 |
| Atoms matched by coordinate | 40 | 2,702 |
| Atoms with nonzero charge, native / published | 0 / 40 | 0 / 2,669 |
| Atom type disagreements | 4 (`N` vs `NA`) | 24 (19 `NA` vs `N`; 5 `SA` vs `S`) |
| Mean absolute charge difference of matched atoms | 0.140 e | 0.199 e |
| Torsional degrees of freedom, native / published | 0 / 7 | not applicable |
| PDBQT branches, native / published | 0 / 7 | 0 / 0 |

With the seven reference-mapped source bonds explicitly selected, the native
flexible ligand contains the same 40 coordinate-matched atoms and emits seven
branches with `TORSDOF 7`. Its charges and four atom-type disagreements remain
as shown above. The flexible projection passed Vina's ligand parser. DockingMT's
temporary rigid-fragment bridge is linked to
[MolSysMT #224](https://github.com/uibcdf/molsysmt/issues/224) and will be removed
when the provider operation can supply the same verified fragment and atom map.

The native ligand omits 29 nonpolar hydrogens. The native receptor omits 1,710
hydrogens under its polar-hydrogen policy. MolSysMT recovered the absent `HB2`–`CB`
bond in SER 438 and `C`–`HC` bond in GLN 498; there was no need for a DockingMT
bond-inference implementation. The source receptor still lacks bond-order information.

The charge differences are distances to the published file, not charge-model accuracy
or a score/affinity assessment. The native files are explicitly provisional: their
charges are placeholders and their atom types are heuristic. The ligand writer currently
supports rigid output only. MolSysMT [#221](https://github.com/uibcdf/molsysmt/issues/221),
[#222](https://github.com/uibcdf/molsysmt/issues/222), and
[#224](https://github.com/uibcdf/molsysmt/issues/224) track reusable charge assignment,
AutoDock typing, and torsion classification respectively. DockingMT owns the PDBQT
projection and Vina safety policy. Its default Vina path rejects provisional native
preparation; an explicit exploratory opt-in remains available. This audit does not
resolve [DockingMT #5](https://github.com/uibcdf/dockingmt/issues/5).
