# Pinned AutoDock Vina ligand examples

These eight unmodified example files come from
[`ccsb-scripps/AutoDock-Vina` commit `3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`](https://github.com/ccsb-scripps/AutoDock-Vina/tree/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example).
The upstream repository distributes them under Apache License 2.0; see its
[`LICENSE`](https://github.com/ccsb-scripps/AutoDock-Vina/blob/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/LICENSE).
They are reference inputs for DockingMT tests, not chemically validated ground
truth. DockingMT does not depend on Meeko to read or compare them.
The root `.gitattributes` keeps their upstream trailing spaces intact while
allowing `git diff --check` to validate the surrounding source changes.

| Local file | Upstream path below `example/` | SHA-256 |
| --- | --- | --- |
| `1iep_ligand.sdf` | `basic_docking/solution/1iep_ligand.sdf` | `051b8742c32adc05c07fb486a4e7c9327f84e131cee33ac4e6a568d07553eb38` |
| `1iep_ligand.pdbqt` | `basic_docking/solution/1iep_ligand.pdbqt` | `15fb35648d8c18c70317842f3a0631b73a19429c710a037ab07310084d579bb8` |
| `1s63_ligand.sdf` | `docking_with_zinc_metalloproteins/data/1s63_ligand.sdf` | `6eb488b5770df7f132745249e64000fcfe394acf938b45f0e082f44365f59119` |
| `1s63_ligand.pdbqt` | `docking_with_zinc_metalloproteins/solution/1s63_ligand.pdbqt` | `04fb28c75bc5a8b32fd7f985ef8ac9a9b4581a40141f4f5b1b3951c2051fb7dc` |
| `5x72_ligand_p59H.sdf` | `mulitple_ligands_docking/solution/5x72_ligand_p59H.sdf` | `ef26c05a198a16972efcf8baae644f6b38fd953561f130ee230626088766b08a` |
| `5x72_ligand_p59.pdbqt` | `mulitple_ligands_docking/solution/5x72_ligand_p59.pdbqt` | `67cf462419372e365b8129bc1047f94598f3a1f3c495375781c1c1100e95c92e` |
| `5x72_ligand_p69H.sdf` | `mulitple_ligands_docking/solution/5x72_ligand_p69H.sdf` | `637a992134b2038a0ea3cff0c1f8355ea232720c9eae5347100b7186170fcdf1` |
| `5x72_ligand_p69.pdbqt` | `mulitple_ligands_docking/solution/5x72_ligand_p69.pdbqt` | `276a991d56ddc7778ed36c10aba6b7231de00b87294a7f77e2fceb9a96ae08e5` |

The tests check these digests before use. Positional atom alignment is permitted
only when a PDBQT coordinate has exactly one source atom of the same element
within 0.002 Å. The tolerance accommodates the final decimal rounding observed
in the 5X72 files; it is not a general atom-mapping method.
