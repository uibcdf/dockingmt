# Named 1IEP preparation and matched torsion sensitivity

This bounded experiment advances [DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17),
[#6](https://github.com/uibcdf/dockingmt/issues/6) and
[#5](https://github.com/uibcdf/dockingmt/issues/5). The
[driver](../../devtools/qualify_1iep_flexibility.py),
[original evidence](data/1iep_flexibility/audit_2026-10-07.json.gz),
[executed notebook](1iep_flexibility_workflow_2026-10-07.ipynb),
[checkpoint](data/1iep_flexibility/checkpoint_2026-10-07.json) and
[guards](../../tests/test_1iep_flexibility_workflow.py) retain each actual search,
the complete source snapshot, preparation reports, atom maps and submitted bytes.

## Hypothesis and controlled inputs

The question is how allowing seven explicitly selected axes changes observed
redocking under one declared preparation, for this real matched ligand/receptor
pair. The original [pinned Vina inputs](../../tests/data/vina_torsions/README.md)
remain unchanged. The ligand SDF contains 69 atoms and 73 edges; its original
chemical state has formal charge +1 and includes 32 indexed H. The existing
explicit RDKit SDF adapter supplies chemistry through public MolSysMT conversion.
No H are generated, no protonation or tautomer alternative is chosen and pH is
unspecified. The receptor is the unchanged external 1IEP PDBQT, whose preparation
chemistry is unassessed. This isolates ligand torsions without claiming a native
receptor-preparation workflow.

Both variants use public named Gasteiger-Marsili charge assignment and AutoDock4
`chemical_environment@1` typing through MolSysMT. Projection retains all 37
heavy atoms and the three polar H (original source indices 43, 47, 58). The 29
nonpolar-H charge transfers conserve +1 e; three-decimal export totals 0.999 e.
The charge audit records that precision loss without renormalization. Source
coordinates, IDs, chemical state and H inventory remain unchanged. Both variants
have identical prepared coordinates, retained inventory, charges and types.

| Choice | Rigid control | Flexible experiment |
| --- | --- | --- |
| Selected axes (zero-based SDF indices) | None | 17–19, 12–13, 10–12, 2–6, 20–21, 24–27, 27–28 |
| Degrees of freedom | 0 | 7 |
| Selection policy | Default rigid | `explicit_docking_cuts@1`; all seven are provider candidates |
| PDBQT order | Retained source order | Recorded ROOT/BRANCH permutation |

The exact axes come from the earlier independently mapped
[reference matrix](vina_torsion_matrix.md). They are caller choices rather than
automatic perception; the published branch count alone is insufficient. The
full provider eligibility/fragment evidence survives in preparation provenance.
No consumer chemistry classifier or provider source change is introduced.

Each variant uses seeds 7, 42 and 2026 at exhaustiveness 1 and 8: twelve searches
specified before inspecting outcomes. All use Vina 1.2.7, `vina` scoring, CPU 1,
five requested poses, the default 3 kcal/mol energy range and the original box
center (15.190, 53.903, 16.917) angstrom with 20 angstrom sides. Default admission
requires no provisional opt-in; preparation remains scientifically `unassessed`.
AutoDock4 typing does not establish support for the AD4 scoring function.

The same receptor bytes and each variant's fixed ligand bytes are authenticated
in every saved result. JSON recovery preserves decisions, original producer
reports and verified source keys. The public full-inventory evaluation measures
all 40 retained atoms against the original SDF. A separate 37-heavy-atom metric
reuses the existing reference driver's operation with explicitly retained source
indices; tests independently calculate both from returned coordinates. Neither
metric aligns the ligand or corrects symmetry. The cutoff remains 2.5 angstrom.

## Original observations — 2026-10-07

| Variant | Exhaustiveness | Seed | Poses | First heavy RMSD (angstrom) | Closest heavy RMSD (angstrom) | First Vina score (kcal/mol) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rigid | 1 | 7 | 1 | 13.2896 | 13.2896 | -7.029 |
| flexible | 1 | 7 | 3 | 12.3453 | 12.3453 | -10.899 |
| rigid | 1 | 42 | 1 | 13.2777 | 13.2777 | -6.996 |
| flexible | 1 | 42 | 1 | 12.3663 | 12.3663 | -10.779 |
| rigid | 1 | 2026 | 1 | 0.2164 | 0.2164 | -18.377 |
| flexible | 1 | 2026 | 3 | 12.3183 | 12.1256 | -10.888 |
| rigid | 8 | 7 | 1 | 0.2195 | 0.2195 | -18.359 |
| flexible | 8 | 7 | 3 | 0.2928 | 0.2928 | -13.302 |
| rigid | 8 | 42 | 1 | 0.2082 | 0.2082 | -18.385 |
| flexible | 8 | 42 | 5 | 12.3349 | 12.0659 | -10.827 |
| rigid | 8 | 2026 | 1 | 0.1945 | 0.1945 | -18.378 |
| flexible | 8 | 2026 | 5 | 12.3183 | 12.0296 | -10.888 |

Rigid: 4/6 first poses and 4/6 returned sets satisfy the declared heavy-atom cutoff. Flexible: 1/6 first poses and 1/6 returned sets satisfy the declared heavy-atom cutoff. These are observed counts for this one declared complex/profile; failed cells remain in the original record.

## Interpretation and boundaries

The existing pinned-fixture comparator matches all 40 native flexible atoms to
the upstream ligand at three-decimal coordinate precision: zero type differences
and zero charge differences. All seven undirected branch bonds and all eight
rigid-fragment sets agree too. The checkpoint retains the complete diagnostic,
both byte digests and comparator identity. This resolves the earlier provisional
ligand's measured type/charge discrepancies for this declared named preparation;
the upstream input remains a comparison reference, not chemical ground truth.
The native ROOT contains the eight-atom piperazine fragment; the published ROOT
contains the four-atom amide fragment. The PDBQT bytes and atom order differ too. The earlier external result
cannot establish how those choices affect sampling: that requires a matched
current-profile comparison. Chemical payload conformity does not guarantee the
same seeded search or near-native recovery.

The starting SDF conformation is close to the bound conformation. Holding it
rigid is a favorable control, not a challenge requiring conformational recovery.
More flexible degrees of freedom can change sampling and Vina's torsional score
term; scores across the variants do not establish binding affinity or a better
chemical model. Twelve runs on one complex are observations, not independent
benchmark samples or recovery probabilities. Greater exhaustiveness alone does
not prove convergence. No settings or cutoff are tuned from these results.

This case complements the earlier [external 1IEP experiment](1iep_external_pdbqt.md)
and [real 181L receptor workflow](181l_receptor_workflow.md). Their original
observations and files remain intact. Different preparation bytes and metric
populations prevent a direct scientific improvement claim over those records.

Nondefault pm/fs units preserve molecular coordinates within 1e-12 angstrom,
charge values and exact atom axes. Some original SDF coordinates lie exactly at
half of the PDBQT 0.001 angstrom text step: binary conversion roundoff can select
either neighboring printed value. The unit control retains this bounded
0.001 angstrom export difference rather than promising byte identity across
unit policies. All twelve searches here use one fixed unit profile and retain
the exact actual bytes individually.

The initial focused guard attempt passed one test and failed three: two assumed
one-based RDKit-adapter atom IDs although the declared IDs are zero-based; one
assumed byte-identical rounding across unit policies. Independent RMSD checks
already agreed. The corrected guards preserve the actual ID contract and
separate coordinate preservation from export precision; production behavior,
search settings and scientific cutoff are unchanged.

State-aware induced connectivity remains [MolSysMT #348](https://github.com/uibcdf/molsysmt/issues/348),
general export [#223](https://github.com/uibcdf/molsysmt/issues/223), environmental
H geometry [#323](https://github.com/uibcdf/molsysmt/issues/323) and symmetry-aware
correspondence [#310](https://github.com/uibcdf/molsysmt/issues/310). This experiment
does not resolve those provider capabilities or qualify protonation, native
receptor preparation, alternative conformer starts, environmental H refinement,
affinity, screening enrichment or public dependency closure. The owning consumer
issues remain partial.

## Reproduce

Use the existing qualified read-only MolSysMT source profile
`5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, ArgDigest
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e`, and the Python 3.14 MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889` in `molsyssuite@uibcdf_3.14`.
The [prior source profile](data/chemical_templates/source_profile_2026-10-06.json)
retains dependency origins, stale editable-distribution metadata and ambient
dependency conflicts. The new receipt authenticates exercised consumer source
and selected provider files; inherited version strings do not identify an entire
source tree. The preserved native extension has a digest, without a fresh-build
claim. New MolSysMT release-record commits were inspected without changing the
sibling worktree or the qualified pins.

```bash
python -m devtools.qualify_1iep_flexibility --output /tmp/1iep-flexibility.json.gz
python -m pytest --receptor=llm tests/test_1iep_flexibility_workflow.py
```

The notebook inspects retained evidence and re-evaluates a saved result under
pm/fs units. It does not rerun twelve searches. The previous installed wheel
checkpoint remains a separate artifact producer; new fixture evidence does not
alter its bytes or reinterpret its qualification.

## Local checkpoint

The five new scientific guards pass with the 180 existing charge/type/torsion/
fragment/evaluation controls and the reporting guard: **186 tests without skips**,
across bounded selections. Three notebook code cells execute on Python 3.14.7;
Ruff, regenerated report indexes, local links, current component-guide and diff
checks pass. Production modules, required CI pins and original qualification
records are unchanged. The checkpoint is captured before publication/hosted CI;
the owning issues retain subsequent exact-head CI state. These scoped local
gates do not claim a new complete local-suite or installed-artifact run.
