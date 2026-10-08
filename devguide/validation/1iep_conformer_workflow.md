# 1IEP alternative-conformer challenge

[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17) and
[#6](https://github.com/uibcdf/dockingmt/issues/6) own this finite follow-up to
the [fixed-first-ROOT control](1iep_root_order_workflow.md). The
[prespecified plan](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6068927987)
was recorded before searches. The [driver](../../devtools/qualify_1iep_conformers.py),
[original observations](data/1iep_conformers/audit_2026-10-08.json.gz),
[executed notebook](1iep_conformer_workflow_2026-10-08.ipynb),
[checkpoint](data/1iep_conformers/checkpoint_2026-10-08.json) and
[guards](../../tests/test_1iep_conformer_workflow.py) retain actual input/output
bytes, geometry and independent positional metrics.

## Declared intervention and evaluation

Starting from the authenticated original 69-atom SDF, public MolSysMT
`structure.set_dihedral_angles` changes quartet `[9,10,12,13]` by +60 or -60
degrees, with `pbc=False`, `in_place=False`. Its central 10–12 bond is one of
the seven previously selected acyclic cuts. Both geometries have initial
37-heavy-atom positional RMSD **6.6994 angstrom** from the original reference.
No minimization, energy filter, clash rejection or outcome-based selection is
applied: these are unminimized torsion perturbations, not a conformer ensemble
or a general conformer-generation tool.

Public MolSysMT bond-angle and dihedral operations verify the requested shift
and the unchanged six other selected dihedrals. Independent numerical checks
verify all 73 covalent distances and every local signed triple-product
orientation. Public snapshots verify unchanged topology, chemical states,
original H inventory, source identities and frame metadata, and input
immutability. Native source geometry checks precede three-decimal PDBQT rounding.

Each geometry is prepared through the existing named charge/type route with
the same seven explicit cuts and 40 retained atoms (37 heavy and three polar H).
Only coordinate columns differ from the original native input; serials, labels,
charges/types, ROOT membership, branch records, TORSDOF and other bytes agree.
Each input is paired with the previous fixed-first-atom permutation, reversing
only the other seven ROOT lines. Source atom N28 stays first and its origin is
equal **within each order pair**; coordinates/origins change across conformers.

The factorial matrix is two geometries x two written orders x seeds 7/42/2026
x exhaustiveness 1/8: **24 new searches**, plus four fixed-initial score attempts.
Vina 1.2.7 uses CPU 1, five requested poses, the same externally prepared rigid
receptor and the existing 20 angstrom box centered at `(15.190,53.903,16.917)`.
Every returned pose is retained.

All poses are evaluated against the **unchanged original crystallographic SDF
geometry**, never against the perturbed input. Public full-inventory evaluation
uses the explicit 40-atom written/source map; independently recomputed
37-heavy-atom positional RMSD uses the existing 2.5 angstrom cutoff, without
alignment or symmetry correction. Exact submitted ligand/receptor bytes are
captured and verified. Charge/type and receptor scientific assessment remain
separate from successful execution.

## Historical producer boundary

The twelve bound-like native/fixed-first cells are referenced through the
unchanged [fixed-first archive](data/1iep_root_order/audit_2026-10-07.json.gz),
gzip SHA-256 `cfea8e331a9d3b53fe8adf6ca766bfaf68a8483f0d8984aae28949e6084b5eba`.
Its six fixed-first observations retain producer
`2f2ee8f7cebe9b07e5ac240937896dfaf9df197e`; the original native cells retain
`7b11391e153f77f340fd039bc799352f90da83d3` through authenticated historical
references. Neither historical arm is rerun or counted as fresh evidence.
Published/full-reversal arms and the earlier native repeat are outside this
36-row comparison.

Scientific reuse authenticates existing consumer/helper bytes, source snapshots,
versions, selected provider sources and preserved native-extension digest.
New geometry provider sources receive separate hashes. The driver/test additions
leave all historical producers and archives unchanged. The preserved native
artifact is not a fresh native-build receipt. Portable regression tests use
current runtime behavior and do not require exact stochastic pose recovery.

## Original observations — 2026-10-08

| Input geometry | Written ROOT order | Near-native first / returned set | First heavy RMSD range (angstrom) | Producer |
| --- | --- | --- | --- | --- |
| Original bound-like | Native | 1/6 / 1/6 | 0.2928–12.3663 | Historical |
| Original bound-like | First atom fixed, others reversed | 6/6 / 6/6 | 0.2561–0.9099 | Historical |
| +60 degrees | Native | 0/6 / 0/6 | 6.4088–12.3447 | New |
| +60 degrees | First atom fixed, others reversed | 3/6 / 3/6 | 0.2923–12.6683 | New |
| -60 degrees | Native | 4/6 / 4/6 | 0.2646–12.3290 | New |
| -60 degrees | First atom fixed, others reversed | 3/6 / 3/6 | 0.9056–12.3130 | New |

All six first-fixed near-native new cells occur at exhaustiveness 8, three per
geometry. For -60 native, seed 2026 also recovers at exhaustiveness 1 and all
three exhaustiveness-8 cells recover. The +60 native arm recovers in neither
effort group. These are actual finite observations, not estimated probabilities.
The notebook shows every cell, score and returned-pose count.

The +60 fixed-input score is **175.436 kcal/mol**, identical under both written
orders at returned precision; its large positive value describes this
unoptimized ligand/receptor placement, not an affinity estimate. Both -60
fixed-input scores are refused outside the unchanged grid. Searches return poses
under all 24 declared cells, including inputs with refused fixed scores.

The previously favorable fixed-first 6/6 result does not persist under either
perturbation, and -60 native returns more recovered cells than its paired
permutation (4 versus 3). Choosing a general ROOT default from the original 6/6
would therefore lack support from this expanded fixture. Input geometry and
written representation are material to these search observations. This does
not isolate engine internals or establish a universal order/geometry effect.

The original gzip SHA-256 is
`52ccfc30cd0feb98e169b6625290664aa32ee58d9cee278d6313f3de55774e8f`.
All 24 new cells and twelve historical references have independently checked
full-inventory and heavy positional metrics against the original reference.

## Interpretation limits

This challenges the favorable bound-like input in one complex with two declared
torsion perturbations. It can establish observations about these input/order
pairs, not recovery probabilities, convergence, a general ROOT policy, ligand
conformer robustness or binding affinity. Equal fixed-initial scores establish
one scoring comparison, not identical energy landscapes.

Rigid covalent geometry and chemical identity preservation do not prove that
the unminimized inputs are low-strain conformers. Nonbonded overlaps and receptor
contacts are not optimized or filtered. Vina's search uses its own initialization;
changing input coordinates is not a claim that the engine starts every search
at that exact pose. The external receptor remains unassessed. Independent
complexes remain the next scientific challenge.

The unchanged box admits fixed scoring of the +60 input but Vina rejects fixed
scoring of the -60 input as outside the grid, under both written orders. The
driver records those refusals with actual input hashes and preserves unrelated
failures. Search admission and returned poses are recorded separately. No box
translation/enlargement or replacement input follows from this observation.

No new public preparation/conformer API or default ROOT policy follows here.
Existing general lossy-export/correspondence work stays in
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223), and assigned-state
subset connectivity stays in [#348](https://github.com/uibcdf/molsysmt/issues/348).
This fixture uses existing public geometry operations; no sibling code changes
or new provider capability proposal are needed to execute it.

## Reproduction

Use the preserved qualified Python 3.14.7 source profile: MolSysMT
`5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, ArgDigest annotated checkout input
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e` targeting source
`57447cc4ec1f7ce85078f8a939892efd075bc919`, and MolSysViewer Python 3.14 source
`ec4c71e574d798b7c8675b7e7e983da878ce9889`. Preserve original distribution
versions/native bytes and existing consumer/helper hashes for historical reuse.

```bash
python -m devtools.qualify_1iep_conformers --output /tmp/1iep-conformers.json.gz
python -m pytest --receptor=llm tests/test_1iep_conformer_workflow.py
```

The original execution uses four independent six-cell processes via `--arm`
(`plus60_native`, `plus60_first_fixed`, `minus60_native`,
`minus60_first_fixed`), each with Vina CPU 1 and a per-cell saved checkpoint.
`--parts` authenticates their producer/profile identities and complete Cartesian
matrix before joining them. Four simultaneous CPU-1 searches do not change the
per-search CPU setting. The default command also permits sequential execution.

The first uncommitted sequential attempt was stopped after three completed +60
native e1 cells and during its first e8 cell when the independent fixed-score
guard exposed the -60 outside-grid refusal. Those preliminary pose payloads were
only in memory and are not reconstructable or counted in the final matrix. The
[execution clarification](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6069044113)
records the limit. The full unchanged declared matrix is rerun with per-cell
retention; successful final cells and all fixed-score refusals are preserved.

Concurrent remote commits through `8da5bbcede2101c3f4b0e058cd5b0711a8522cc9`
are preserved: guide/policy synchronization and coverage instrumentation do not
change the scientific consumer bytes or qualified dependency commits. Sibling
working trees remain untouched; their newer upstream heads are not silently
substituted into the historical profile. Local, hosted-source, installed-artifact
and public/platform qualification retain separate evidence scopes.

## Local validation and retention

Four new guards and 62 existing representation/flexibility/fixed-origin/reference/
evaluation/reporting cases pass: **66 distinct tests, no skips**. Three notebook
code cells execute, including original-reference saved-result re-evaluation
under pm/fs with an explicit 250 pm (2.5 angstrom) cutoff and verified actual
captured inputs. Ruff check/format (134 files), indexes, changed-document local
links, consumer/provider/native/input hashes, component guidance and whitespace
checks pass. Hosted exact-head source gates are recorded later in owning issues;
no new installed artifact or wider platform/public support is claimed here.

The initial notebook draft used an absent `criterion.rmsd_unit` field and a
tenfold-too-large pm cutoff. Its third cell failed before any output notebook
was saved. The corrected cell uses the documented fixed-angstrom report and
250 pm, asserts the complete criterion matches the original saved evaluation,
and independently measures each returned geometry. No search or scientific
archive changes follow from this notebook correction.

The local checkpoint retains original four-arm producers, the preliminary
unretained-attempt limitation, test/receipt hashes and temporary ownership.
Managed notebook kernels close and their temporary directories are removed.
Qualified source/native archives and task-owned original arm records, JUnit,
preflight and inspection receipts remain available for follow-up. Sibling work,
shared environments, historical evidence and human resources are preserved.

Concurrent export-tool tracing fix `03281126e658d5b39aa5369b09e1bb40a8211134`
is also preserved beneath the scientific change. It touches no authenticated
consumer/helper, experiment input or provider bytes; retained local scientific
results remain applicable. The final unskipped head supplies fresh hosted gates.

## Portable annotation correction after first hosted CI — 2026-10-08

The [first exact-head CI](https://github.com/uibcdf/dockingmt/actions/runs/37846351830)
fails the three portable input/live guards in fixture setup. The driver compared
runtime REMARK metadata with historical annotation bytes. Ordinary installation
of the same pinned MolSysMT source reports `1.0.0` in CI, while the preserved
scientific profile reports `0.22.4+215.g5bd893c85`. Requiring that historical
version in portable annotations was a consumer assertion defect.

`prepare_cases(verify_profile=False)` now prepares its unperturbed comparison
input in the current runtime, retaining exact actual annotations and checking
the perturbation against that input. `verify_profile=True` continues to
authenticate the historical versions/bytes for scientific reproduction. A fifth
guard simulates only the installed version annotation, verifies that both
exported annotation records retain it, and confirms baseline immutability.
All five current guards pass locally in 70.94 s; with the applicable unchanged
62 boundary cases, the current scope is **67 distinct tests, no skips**.

Original observations and scientific driver bytes remain attached to producer
[27a18ef](https://github.com/uibcdf/dockingmt/commit/27a18ef0781016957e4ecc8c523314973be52b37).
Its driver hash is authenticated at that commit, rather than claiming the changed
portable driver has the old hash. The current strict-profile preparation
reproduces all saved case dictionaries exactly. Scientific archive/digest,
notebook, input bytes, counts and earlier producers remain unchanged; no searches
are rerun. This corrects a DockingMT guard, not a demonstrated provider molecular
operation or public-version defect. The corrected head requires fresh hosted CI,
recorded separately in the owning issues.
