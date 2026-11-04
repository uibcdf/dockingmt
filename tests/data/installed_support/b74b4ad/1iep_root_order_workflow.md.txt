# 1IEP ROOT order with a fixed first atom

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17) and
[#6](https://github.com/uibcdf/dockingmt/issues/6) own this finite follow-up to
the [rooted-representation experiment](1iep_representation_workflow.md).
The [driver](../../devtools/qualify_1iep_root_order.py),
[original six-search archive](data/1iep_root_order/audit_2026-10-07.json.gz),
[executed notebook](1iep_root_order_workflow_2026-10-07.ipynb),
[local checkpoint](data/1iep_root_order/checkpoint_2026-10-07.json) and
[guards](../../tests/test_1iep_root_order_workflow.py) retain the actual inputs,
written/source correspondence, fixed-conformation score and every returned pose.

## Declared intervention

The earlier complete ROOT reversal changed both written order and the first
ROOT atom, which supplies Vina's ligand rigid-body origin. This control keeps
the first ROOT ATOM line unchanged and reverses only the other seven lines.
The source index sequence changes from `[28,29,30,31,32,33,34,58]` to
`[28,58,34,33,32,31,30,29]`. Source atom 28 (N) remains first, at
`(16.917,46.907,20.219)` angstrom. Every line byte, serial, label, ROOT member,
branch record, TORSDOF and all remaining text are preserved.

The same original SDF chemical state and H inventory, 40 exported atoms
(37 heavy + 3 polar H), coordinates, three-decimal charges, AD4 types,
seven undirected cuts/eight fragments, pinned external rigid receptor and
20 angstrom box centered at `(15.190,53.903,16.917)` are fixed. Searches use
Vina 1.2.7, CPU 1, five requested poses, seeds 7/42/2026 and exhaustiveness 1/8.
The declared heavy positional cutoff remains 2.5 angstrom, without alignment
or symmetry correction. No seed, ROOT or criterion is selected from the outcome.

This is a literal finite-fixture permutation authenticated by the native input
SHA-256 `43e3219134099eee7d388b0f49ca90e5a46afea9b6b54a754276b21fab48761e`.
It adds no general molecular writer, matcher or torsion classifier. The existing
public MolSysMT declared-tree writer is already qualified separately; original
source correspondence through lossy H projection remains
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223).

## Comparison and producer boundaries

Only six new searches and one new fixed-conformation score are executed in this
matrix. The eighteen historical native/published/full-ROOT-reversal cells are
referenced through the unchanged authenticated
[earlier archive](data/1iep_representation/audit_2026-10-07.json.gz), gzip SHA-256
`a7ba98a15191b7345e55c2de01533efe22a917d1c948bccd735970bf5d868436`, published
at `dd571ef4dd0a1ddc9142e399a6da3683299a1db4`. Original native producer
`7b11391e153f77f340fd039bc799352f90da83d3` remains attached to those six
observations. The earlier native repeat remains separate from the matrix.

Scientific reuse checks unchanged consumer/helper bytes, original producer
versions and source snapshot, regenerated native input, selected provider source
hashes and the preserved native-extension digest. This does not claim a fresh
native build. Provider worktrees and newer remote commits are preserved. Portable
software tests use current runtime behavior on the frozen inputs; they do not
require historical version strings or exact stochastic recovery.

The existing public docking and fixed-scoring operations capture actual submitted
bytes. The earlier bounded already-aligned fixture map supplies the declared
written-to-source axis. Public full-inventory RMSDs and separate 37-heavy-atom
RMSDs are independently checked against every returned geometry. The notebook
also re-evaluates one saved result under pm/fs without rerunning searches.

## Original observations — 2026-10-07

| Exhaustiveness | Seed | Poses | First heavy RMSD (angstrom) | Closest heavy RMSD (angstrom) | First Vina score (kcal/mol) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 7 | 1 | 0.9099 | 0.9099 | -13.170 |
| 1 | 42 | 1 | 0.2561 | 0.2561 | -13.203 |
| 1 | 2026 | 1 | 0.9088 | 0.9088 | -13.195 |
| 8 | 7 | 4 | 0.2740 | 0.2740 | -13.313 |
| 8 | 42 | 2 | 0.2786 | 0.2786 | -13.294 |
| 8 | 2026 | 3 | 0.3209 | 0.3209 | -13.224 |

## Interpretation and limits

The fixed-first-atom permutation returns near-native first poses and returned
sets in **6/6** observed cells; first heavy RMSDs range from **0.2561 to 0.9099
angstrom**. The unchanged historical counts are native **1/6**, published
**5/6**, and complete native ROOT reversal **4/6**. All eight fixed-initial score
components equal the native observation at returned precision, including total
**-12.513 kcal/mol**.

The native/fixed-first comparison differs in seven ROOT line positions while
holding the first atom/origin and all other bytes fixed. The observed search
change therefore does not require a changed ROOT origin. Written order is part
of the executed search representation in this bounded case. This does not
apportion the earlier complete-reversal difference between order and origin,
nor make the better observed recovery a supported general ROOT policy.

A difference from the native observation with the first atom and origin held
fixed demonstrates order sensitivity for this particular permutation and
profile. Agreement would not establish general order invariance or prove that
origin alone caused the previous complete-reversal difference. The published
comparison still changes ROOT membership, traversal, labels and order together.
An equal fixed-initial score establishes one scoring observation, not an equal
energy landscape or affinity.

One complex, one favorable bound-like starting conformation, three seeds and
one permutation do not establish recovery probabilities, convergence or a
general ROOT policy. The receptor remains externally prepared/unassessed.
Alternative starting conformers and independent complexes are the subsequent
scientific challenges. No preparation/default/root policy changes follow here;
the wider #17/#6/#4/#5/#33 scope remains open.

## Reproduction and local scope

Use the same qualified Python 3.14.7 profile as the previous experiment:
MolSysMT source `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, the preserved
ArgDigest checkout input `1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e`
(annotated tag targeting `57447cc4ec1f7ce85078f8a939892efd075bc919`),
MolSysViewer Python 3.14 source `ec4c71e574d798b7c8675b7e7e983da878ce9889`,
and the original recorded distribution versions/native bytes.

```bash
python -m devtools.qualify_1iep_root_order --output /tmp/1iep-root-order.json.gz
python -m pytest --receptor=llm tests/test_1iep_root_order_workflow.py
```

The final local scope passes **62 distinct tests without skips**: four new
fixed-origin/input/scoring/live/saved-evidence guards and 58 existing
representation/flexibility/reference/evaluation/reporting cases. Three notebook
code cells execute, including independent saved-result pm/fs re-evaluation.
Ruff check/format (130 files), report/index, changed-document links, finite
receipt/source digests and whitespace checks pass.

The first component-guide check found a newer canonical MolSysSuite guide;
the central synchronizer copied its exact bytes and the repeated check passes.
This instruction delivery is separate from the unchanged automated policy pin
and wider support-library adoption. The initial notebook attempt found no
registered custom kernel; an owned managed temporary kernel explicitly selects
the recorded interpreter and is cleaned after execution. No engine search is
repeated for notebook execution.

Earlier installed artifact producers/digests, public dependency-closure limits
and synchronized-guide drift are unchanged. The local checkpoint records its
capture stage; owning issues retain subsequent commit and exact-head CI state.
