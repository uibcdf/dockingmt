# Exploratory 181L redocking regression baseline

Measured on 2026-09-22 for [DockingMT issue #10](https://github.com/uibcdf/dockingmt/issues/10).
This is a reproducibility and software regression case, **not a validated
docking-performance result**. Receptor and ligand preparation still require the
explicit provisional opt-in tracked in [issue #5](https://github.com/uibcdf/dockingmt/issues/5).

## Reproduce

```bash
python devtools/redocking_181l.py record --manifest /tmp/181l-manifest.json
python devtools/redocking_181l.py replay --manifest /tmp/181l-manifest.json --report /tmp/181l-report.json
```

The commands run separately: replay reads the saved JSON manifest, reconstructs
the file-backed molecular problem and recorded Vina protocol, and reruns docking
without the original Python objects. The report contains the complete problem,
protocol, source and submitted PDBQT fingerprints, all pose scores and RMSDs,
and the explicit replay comparison. A changed source file fails reconstruction.

## Recorded configuration

- Source: MolSysMT's `T4 lysozyme L99A/181l.pdb` fixture, SHA-256
  `77018feaaa65bb22dea47c784e8c059b0ccc09cd6dc7442b79cce83f3170985f`.
- Receptor: `molecule_type=='protein'`; ligand: `group_name=='BNZ'`, six
  retained atoms. Search box: ligand bounds plus 8 Å padding.
- Vina: scoring `vina`, exhaustiveness 1, five requested poses, seed 42,
  one CPU, energy range 3 kcal/mol, provisional preparation opt-in enabled.
- Python 3.13.14, MolSysMT `0.21.0+606.ga03eb4bf6`, Vina 1.2.7.
- DockingMT source: commit `c044de4082b5daea33e19ffdc565e63a7bba2313`, clean
  worktree, code SHA-256
  `05a56d47f22f1ae8d5bf1ca8709bd61922159f7a1454a65e236eb26dde778909`.
  The editable installation reported a stale generated package version
  (`0.0.0+14.g25b6e0b.dirty`); the commit and code digest identify the code run.
- Submitted receptor PDBQT SHA-256:
  `4e8703b050563f68a159d1b23f9b2751b86bea9edc8410eeb97eeecb2b756ebc`.
  Submitted ligand PDBQT SHA-256:
  `63ce042a0be7c733e2e1e7ef8b44e1d850043dd7486226456aa0c3a73b4b436b`.
- Saved manifest SHA-256:
  `d95cfadc1be54fa7df5aacd725050dbaec671c8359bf2af9355f42b5b2089979`.

## Observed poses

RMSD uses verified source-atom correspondence for the retained ligand atoms,
without superposition. The declared near-native cutoff is 2.5 Å. Vina returned
four poses from five requested, and the first near-native pose ranked 1. No
`no_poses` or `no_near_native_pose` failure mode occurred.

| Rank | RMSD (Å) | Vina score (kcal/mol) |
| ---: | ---: | ---: |
| 1 | 1.8993 | -5.490 |
| 2 | 2.8224 | -5.431 |
| 3 | 12.3238 | -2.998 |
| 4 | 12.2179 | -2.974 |

The score range was -5.490 to -2.974 kcal/mol. The report also retains each
pose's named `inter`, `intra`, and `torsion` scores, state IDs and identity map.

## Replay assessment

The separate replay used the same clean source revision and matched the
recorded source and PDBQT hashes, problem and protocol, software versions,
pose count, source-atom identities, ranks and state IDs. The largest score
difference, pose-to-pose coordinate RMSD, and reference-RMSD difference were
all zero. The regression tolerances are 0.05 kcal/mol for each named score and
0.25 Å for the two RMSD comparisons; all checks passed.

This one small rigid case establishes a replayable baseline for the current
implementation. It does not establish preparation correctness, behavior on
other systems, or sensitivity to search settings. Preparation decisions and
chemical validity remain under [issues #4](https://github.com/uibcdf/dockingmt/issues/4)
and [#5](https://github.com/uibcdf/dockingmt/issues/5).
