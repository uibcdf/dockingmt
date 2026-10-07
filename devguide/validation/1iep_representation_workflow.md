# 1IEP rooted-representation sensitivity

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17) owns this bounded
follow-up to the [matched torsion experiment](1iep_flexibility_workflow.md).
The [driver](../../devtools/qualify_1iep_representation.py),
[original evidence](data/1iep_representation/audit_2026-10-07.json.gz),
[executed notebook](1iep_representation_workflow_2026-10-07.ipynb),
[checkpoint](data/1iep_representation/checkpoint_2026-10-07.json) and
[guards](../../tests/test_1iep_representation_workflow.py) retain complete input
bytes, source correspondence, individual searches and fixed-conformation scores.

## Controlled question

Does an equivalent rooted representation change the observed search under
matched seeds and sampling settings? All cases share the original 69-atom SDF
state/H inventory, externally prepared rigid 1IEP receptor, 40 exported atoms
(37 heavy and 3 polar H), seven selected covalent cuts and eight rigid fragments.
The receptor bytes, 20 angstrom box centered at (15.190, 53.903, 16.917), Vina
1.2.7 scoring model, CPU 1, five requested poses, seeds 7/42/2026 and
exhaustiveness 1/8 are fixed. The declared positional recovery cutoff is
2.5 angstrom. No alignment, symmetry correction or outcome-based tuning occurs.

| Representation | ROOT source atoms | Intervention |
| --- | --- | --- |
| Native, original | 28, 29, 30, 31, 32, 33, 34, 58 | Reuse six exact previously qualified native flexible searches. |
| Published Vina | 19, 20, 35, 47 | Use the unchanged pinned upstream ligand. ROOT, branch traversal, atom labels and written order differ together. |
| Native ROOT reversed | 58, 34, 33, 32, 31, 30, 29, 28 | Reverse only the eight existing ROOT ATOM lines. Preserve every line byte, serial, label, ROOT membership, branch record and all remaining text. |

Source positions are zero-based original SDF indices. All 40 coordinates, types
and three-decimal charges match under the existing pinned-fixture comparator;
all seven undirected branch bonds and all eight fragment sets match. Vina admits
the three trees. The ROOT permutation is a finite fixture intervention protected
by the exact native byte digest. It implements no general PDBQT writer,
rerooting operation, chemical classifier or atom matcher. Those molecular
operations remain provider-owned.

The fixed-conformation control composes public `dockingmt.score` without search
or optimization. It retains all eight Vina components, original geometry,
scoring history and actual submitted bytes. Equality at the initial conformation
checks one scoring observation; it does not establish equivalence of the full
energy landscape or affinity.

## ROOT order also defines the coordinate origin

The [official Vina 1.2.7 parser](https://github.com/ccsb-scripps/AutoDock-Vina/blob/8eb40404f4f45608acb3b01427587ac049f27c1f/src/lib/parse_pdbqt.cpp#L440-L444)
constructs the ligand rigid body from `p.atoms[0].a.coords`: the first ROOT atom
supplies its origin. The inspected tag resolves to
`8eb40404f4f45608acb3b01427587ac049f27c1f`; the checkpoint authenticates the
inspected source bytes. This is source inspection, separate from proof of the
installed binary's build provenance.

| Representation | First ROOT source atom | Origin (angstrom) |
| --- | ---: | --- |
| Native | 28, N | (16.917, 46.907, 20.219) |
| Published | 19, N | (16.600, 51.810, 14.798) |
| Native ROOT reversed | 58, H | (17.519, 46.907, 23.437) |

The line-order intervention therefore changes both ROOT order and this origin.
It holds initial physical geometry and ROOT membership fixed while changing the
search parametrization. It cannot isolate a cosmetic order effect at a fixed
origin. The published/native comparison also cannot isolate ROOT membership
alone. A further permutation that keeps the first ROOT atom fixed would be an
informative distinct control. No new default ROOT policy follows from this case.

The qualified MolSysMT provider already supports explicit declared-tree writing
through `msm.convert(..., to_form='string:pdbqt_text',
typing_scheme='autodock4', torsion_tree=tree)`. A separate public-API probe reads
the native PDBQT tree, reverses its eight packed ROOT indices and writes it again.
It preserves all 40 coordinates, types, charges, seven cuts and fragment sets,
and leaves the native source unchanged. The checkpoint retains the output and
digest. This canonical writer output is separate from the literal frozen-line
permutation used in the searches; it adds no search observation. The remaining
provider integration concerns original-source correspondence and the explicit
lossy H projection, rather than a missing PDBQT writer.

## Original observations — 2026-10-07

| Representation | Exhaustiveness | Seed | Poses | First heavy RMSD (angstrom) | Closest heavy RMSD (angstrom) | First Vina score (kcal/mol) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| native | 1 | 7 | 3 | 12.3453 | 12.3453 | -10.899 |
| native | 1 | 42 | 1 | 12.3663 | 12.3663 | -10.779 |
| native | 1 | 2026 | 3 | 12.3183 | 12.1256 | -10.888 |
| native | 8 | 7 | 3 | 0.2928 | 0.2928 | -13.302 |
| native | 8 | 42 | 5 | 12.3349 | 12.0659 | -10.827 |
| native | 8 | 2026 | 5 | 12.3183 | 12.0296 | -10.888 |
| published | 1 | 7 | 1 | 0.2718 | 0.2718 | -13.293 |
| published | 1 | 42 | 1 | 0.8969 | 0.8969 | -13.286 |
| published | 1 | 2026 | 3 | 12.3188 | 12.1504 | -10.945 |
| published | 8 | 7 | 4 | 0.9045 | 0.9045 | -13.227 |
| published | 8 | 42 | 4 | 0.8969 | 0.8969 | -13.286 |
| published | 8 | 2026 | 2 | 0.9045 | 0.9045 | -13.193 |
| native_root_reversed | 1 | 7 | 2 | 12.3274 | 12.3274 | -10.858 |
| native_root_reversed | 1 | 42 | 2 | 12.1680 | 12.1680 | -11.218 |
| native_root_reversed | 1 | 2026 | 1 | 0.9067 | 0.9067 | -13.275 |
| native_root_reversed | 8 | 7 | 3 | 1.2120 | 1.2120 | -12.801 |
| native_root_reversed | 8 | 42 | 3 | 0.9469 | 0.9469 | -13.035 |
| native_root_reversed | 8 | 2026 | 3 | 0.9067 | 0.9067 | -13.275 |

Observed near-native returned sets: native **1/6**, published **5/6**, native ROOT reversed **4/6**; first-pose counts are the same. All failures remain in the archive. These are matched observations on one complex, not recovery probabilities or a policy ranking.

All eight fixed-conformation Vina components agree across the three representations at returned precision: total -12.513, ligand interaction -17.634, ligand intra -0.485, torsion term 5.121 kcal/mol, with the other interaction components zero and best-pose intra -0.485. The same initial physical geometry has different observed searches. The ROOT reversal also changes its origin, as established by the inspected parser. A larger sample and a fixed-first-atom order control are required before choosing or attributing a general ROOT policy.

## Saved-results and producer boundaries

The six original native searches retain their original result dictionaries,
verified source-key reports and producer
`7b11391e153f77f340fd039bc799352f90da83d3`. The earlier gzip digest is
`a8e7891094593223e5b8518d6a0695cce673022182cde2eaa076fba397755eca`.
Scientific reuse requires unchanged consumer/provider helper bytes, producer
versions, original source snapshot and exact native ligand bytes. The new search
arms use independent Python processes, each with Vina CPU 1. A separate native
seed-42/exhaustiveness-1 repeat tests the present raw-input route against the
original native result; it is not counted as another independent matrix cell.

New PDBQT inputs enter through the existing raw-input route and retain their
verified written pose order. The existing aligned-fixture mapper supplies an
explicit correspondence to the original SDF. Public full-inventory evaluation
uses caller-declared positional matching, while the existing heavy-atom metric
uses the same written-to-source axis. Independent guards compute both directly
from every returned geometry. This does not extend the public molecular-key
contract to an arbitrary PDBQT input or supply a general matcher.

Live software guards use the frozen input bytes on the current test runtime;
they do not require matching historical software version strings or historical
developer-generated `_version.py` bytes. The scientific driver separately
requires the exact reviewed local profile before reusing older observations.
Tests check actual metric arithmetic and mappings without a portable positive
recovery or exact stochastic-pose guarantee.

The local candidate passes 101 selected tests without skips: five new guards,
95 existing engine/scoring/reference/replay/evaluation tests and the reporting
guard. Three notebook code cells execute, including saved-result pm/fs
re-evaluation. Ruff check/format, report indexes, changed-document
links, component guidance and evidence/source digests pass. The checkpoint
records this local scope before commit and hosted CI; the owning issues retain
subsequent exact-head CI state. Earlier installed-artifact qualification remains
separate.

Remote distribution-controls commit
`1d67d3838bb1fd18a59fad8800c317767f7683a6` arrived during qualification and
is preserved beneath this scientific change. It leaves the measured consumer
and fixture bytes and scientific environment unchanged. After integration,
19 distribution/reporting tests pass without skips, declaration preflight and
report indexes pass, and Ruff checks all 128 files. These administrative results
do not extend the scientific or installed-artifact observations.

A further remote correction, `50f0abbdf14a08b77d26b293d1b670d6dfc204a0`,
distinguishes the preserved ArgDigest checkout input (annotated tag object
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e`) from its actual source commit
`57447cc4ec1f7ce85078f8a939892efd075bc919`. It changes no scientific source or
workflow checkout input. The final integrated administrative selection passes
20 collected tests without skips, including its new annotated-tag guard;
declaration preflight, report indexes and Ruff checks pass again.

## Scope and reproduction

Use the qualified Python 3.14.7 source profile from the
[earlier checkpoint](data/1iep_flexibility/checkpoint_2026-10-07.json): MolSysMT
`5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, ArgDigest
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e`, and the existing Python 3.14
MolSysViewer source. The newer fetched MolSysMT commits record release/public
qualification; the sibling worktree, qualified pins and native artifacts are
preserved. No newest-provider or fresh native-build qualification is inferred.

```bash
python -m devtools.qualify_1iep_representation --variant published --output /tmp/1iep-published.json.gz
python -m devtools.qualify_1iep_representation --variant native_root_reversed --output /tmp/1iep-reversed.json.gz
python -m devtools.qualify_1iep_representation --parts /tmp/1iep-published.json.gz /tmp/1iep-reversed.json.gz --output /tmp/1iep-representation.json.gz
python -m pytest --receptor=llm tests/test_1iep_representation_workflow.py
```

The notebook inspects the saved results and re-evaluates one original observation
under pm/fs units; it does not rerun the searches. The original bound-like
conformer remains a favorable starting point. One complex and three seeds do
not establish a recovery probability, convergence, preferred ROOT, general
flexibility policy, chemical-state validity or affinity. The receptor stays
externally prepared/unassessed. Wider native preparation, alternative conformer
starts and environmental refinement remain separate scientific work.

Public export/correspondence remains [MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223);
state-aware induced connectivity remains
[#348](https://github.com/uibcdf/molsysmt/issues/348). Existing installed wheel
producers/digests, public dependency-closure limits and synchronized-guide drift
remain intact. The owning consumer issues #17/#6/#5 remain partial.
