# Minimal ligand torsion reference matrix

The cases in `tests/test_vina_torsion_matrix.py` use verbatim files from a
single pinned AutoDock Vina commit. Their source paths, SHA-256 digests, and
Apache License 2.0 attribution are in
[`tests/data/vina_torsions/README.md`](../../tests/data/vina_torsions/README.md).
The files are comparison inputs, not chemically validated ground truth. The
test uses MolSysMT as DockingMT's molecular source and does not install Meeko.

| Case | Source atoms | PDBQT atoms | Published branches | Rigid fragments | RDKit `Strict` / `NonStrict` |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1IEP | 69 | 40 | 7 | 8 | 7 / 8 |
| 1S63 | 29 | 30 | 6 | 7 | 5 / 5 |
| 5X72 P59 | 39 | 25 | 2 | 3 | 2 / 2 |
| 5X72 P69 | 39 | 25 | 2 | 3 | 2 / 2 |

The RDKit numbers were measured with RDKit 2025.09.5 after `Chem.RemoveHs`.
The test checks the mode-specific counts and will expose a descriptor change.
It maps each PDBQT atom to a *unique source atom of the same element* within
0.002 Å. This bound handles final-decimal rounding in the 5X72 files; it is
not a general molecular identity algorithm. The 1S63 PDBQT contains one polar
hydrogen absent from the source SDF. That reference-only hydrogen is counted
and excluded from source-index fragment comparison. No other unmatched atom
is accepted.

The selected bonds come from the published PDBQT. The test checks that
DockingMT's tree has the same undirected source bonds and rigid source-atom
fragments, and that those fragments equal MolSysMT
`get_covalent_blocks(remove_bonds=...)` after the selected cuts. Vina's parser
is also exercised when its optional package is present. This is evidence for
tree serialization and atom mapping, **not automatic torsion perception**, a
charge model, or docking affinity.

The 1S63 reference includes the aryl–C≡N bond (source atoms 26–27) as a branch;
RDKit `Strict` excludes it. In ethyl acetate (`CC(=O)OCC`), DockingMT accepts
an explicitly selected ester acyl C–O bond while RDKit `Strict` excludes it.
Both differences are tracked in [DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17)
for an explicit docking policy. The reusable classifier and fragment contract
remain tracked in [MolSysMT #224](https://github.com/uibcdf/molsysmt/issues/224).
