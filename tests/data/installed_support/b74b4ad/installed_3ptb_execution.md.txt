# Installed 3PTB execution and saved-record inspection

Owner: [#4](https://github.com/uibcdf/bindingmt/issues/4), coordinated with
[#33](https://github.com/uibcdf/bindingmt/issues/33). The
[notebook](installed_3ptb_execution.ipynb) delivers the separately registered
two-search follow-up to [preparation/admission](installed_3ptb_preparation.md).
**Run All executes two new Vina searches.** It saves complete results and reads
them through the unchanged public inspection notebook. No RMSD, fixed-pose
rescoring or viewer action is included.

## Run the example

Use an ordinary-installed scientific kernel with the required providers, IPython
and Jupyter notebook IO (`nbformat` and its dependencies). Copy all three clean
notebooks to your working directory. Set the five explicit source/declaration/
preparation-output variables in the [preparation guide](installed_3ptb_preparation.md),
using a fresh preparation directory. Add these five inputs before launching
Jupyter:

```bash
export BINDINGMT_3PTB_PREPARATION_NOTEBOOK="installed_3ptb_preparation.ipynb"
export BINDINGMT_3PTB_PREPARATION_NOTEBOOK_SHA256="c6c5a6660b8b5d46df01cde6960129a7bc65db81d551b3ad0a4d763fc0907da9"
export BINDINGMT_RESULT_INSPECTION_NOTEBOOK="installed_result_inspection.ipynb"
export BINDINGMT_RESULT_INSPECTION_NOTEBOOK_SHA256="bfe922f86012834ba12bf9cb1ada5098944c6979fee00523ef9fd38ba25ee3e0"
export BINDINGMT_3PTB_EXECUTION_OUTPUT="new-execution-output"
jupyter lab
```

Expected notebook hashes identify trusted executable code; checking them is
distinct from admitting data. Public IPython `%run` executes the companion
notebooks and exposes their explicitly named outputs through `user_ns`. No
repository/developer module, data harness or SDK is used. An existing execution
directory is refused before preparation; the preparation notebook independently
refuses an existing preparation directory. A rerun requires new destinations
and a separately justified scientific registration, not replacement of records.

The six outer code cells admit configuration, replay the nine preparation cells
once, retain the prospective ledger, attempt both searches, inspect both saved
records through eight reader cells each, and emit a compact receipt. The progress
ledger appends before/after attempts and retains both planned rows and failures.
Completed raw JSON is written before later inspection. If inspection fails,
receive the saved files; do not rerun successful searches to fix reporting.

The tested archives are private receiving artifacts. This is not a public
installation recipe, provider-minimum decision or platform admission (#30/#47).

## Registered and observed execution — 2026-11-03

The [prospective contract](installed_3ptb_execution_registration.md),
[source/artifact registration](data/installed_3ptb_execution/registration_2026-11-03.json)
and [pre-search issue registration](https://github.com/uibcdf/bindingmt/issues/4#issuecomment-6619228750)
precede both attempts. Frozen workflow source is
`1ef85cbdcbe75fb0c8a2f4dd37228f52a987f020`; the exact execution notebook SHA-256
is `9ee4394a17ebb369d75783f19e2ae523b651e4fc4c2c18f70b5d208611e89734`.

Both cases reuse the declared 2,011-atom dry receptor / rigid 13-atom ligand,
20 Å cube, seed 7, exhaustiveness 1, CPU 1, Vina scoring and 3 kcal/mol retrieval
window. The displaced centre is +60 Å x. Actual submitted centres, rounded to
six decimals in angstrom, are `[-1.759111, 14.461, 16.915778]` and
`[58.240889, 14.461, 16.915778]`; both actual box sizes are `[20,20,20] Å`.
Resolved native calls retain `max_evals=0`, `min_rmsd=1.0 Å`, spacing `0.375 Å`
and `force_even_voxels=False`.

| Case | Planned / attempted / returned calls | Returned poses | First recorded Vina score (kcal/mol) | Saved-record audit |
| --- | --- | --- | --- | --- |
| Native | 1 / 1 / 1 | 5 | -6.422 | Consistent; captures verified |
| Displaced | 1 / 1 / 1 | 4 | 0.0 | Consistent; captures verified |

All nine poses retain thirteen atoms, original order/rank/identity, complete
recorded scores and descriptors. Zero scores remain zero. The finite count is
**two searches / nine poses**, not eighteen guaranteed poses. No search fails
or repeats; the native search's internal optimization/energy work is part of
Vina docking, distinct from a separately requested fixed-pose score/optimization.
There is no RMSD or near-reference recovery claim and no inference of affinity
or chemical-model suitability. The old 24-search/167-pose and five-pose human
populations retain their original producers, bytes and denominators.

The [receiving receipt](data/installed_3ptb_execution/receiving_2026-11-03.json)
binds all six exact outer cells, the completed nine-cell preparation and two
eight-cell inspections. One real kernel completes and shuts down. Each reader
checks the new file digest, schema/audit/captures, refusal controls, detached
roundtrip and pm/fs policy conversion/restoration. There is no second search
execution under another unit policy. Submitted receptor/partner hashes match
the actual preparation files and the previous admitted representations.

Validation-only pre/post cells verify the ordinary consumer's 63 payloads,
MolSysMT's 3,415 payloads and native Vina files before/after. Loaded core/support/
provider/engine origins belong to the independent scientific prefix. Counters
observe exactly two public `dock` calls and two Vina initializations, map builds,
searches and energy retrievals; guards observe zero standalone score, RMSD,
reconstruction, viewer or developer-import attempts. The unchanged BindingMT
archive remains producer `50d8e33`, SHA-256
`5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`;
MolSysMT remains producer `de7ffad2a` / controlled main `00abb958f`, archive
SHA-256 `4a8e58f40627ff468fab99301674429fba66362f549a31fb4cc747d9cf19a0ba`.
Python is 3.14.8; Vina 1.2.7's actual native extension is bound in registration.
Dependency closure passes. No runtime, dependency, package or CI workflow is changed.

The [public observations](data/installed_3ptb_execution/observations_2026-11-03.json)
are an explicit allow-list projection of unchanged scientific fields: all full
poses, descriptors, energy vectors, boxes, resolved calls and input identities.
They are **not** standalone DockingResult files or substitutes for the original
raw records. Both raw JSON files retain their hashes and task-owned custody;
operational staging paths and raw diagnostics are not published. The
[manifest](data/installed_3ptb_execution/manifest_2026-11-03.json) binds the
maintained source and public evidence.

## Receiving corrections and checks

A restricted controller initially stalls before scientific cells and is stopped.
The corrected launch diagnoses missing `nbformat` in the task's minimal kernel
tooling before preparation. Its kernel closes; the
[tooling amendment](https://github.com/uibcdf/bindingmt/issues/4#issuecomment-6619316784)
supplies notebook IO outside the unchanged scientific prefix. A controller-only
string-escaping syntax stop is corrected before launching the final kernel.
These stops create no preparation output, search ledger or scientific attempt.
The registered notebook/code hashes, chemistry, protocol and denominator remain
unchanged; the final run completes all cells. No provider defect is inferred.
Two provider warnings retain the explicitly allowed occupancy/B-factor loss.

Existing installed audit/schema guards pass **144 tests**, zero skips, in
1.624 s, with one preimported-SMonitor assertion-rewrite warning. Test context
`1c34392` is source-free and both selected files equal current source; loaded
scientific/support origins are checked. These are software cases, not new
scientific searches or a new full suite. Exact-head hosted CI keeps its own
observed status and recovery on #4.

## Next boundary and custody

Preparation → execution → detached saved-record inspection is delivered for this
declared case. Before later RMSD, fix the comparison population and verify the
public route for the nine originally observed heavy atoms. Use MolSysMT for
selection/correspondence/geometry and BindingMT for docking-result/evaluation
semantics; do not copy the private heavy-pose projection helper. Missing reusable
provider capabilities, if encountered, belong in their owning repository.
No new molecular operation is needed for the present execution/inspection slice.

This does not accept general chemistry, whole Core, public delivery, native
mechanics persistence or visible C4/C6. #4/#33 remain partial; #30/#47 and the
deferred #52/#60 observation retain their owners. Raw executions/results, failed
startup evidence and isolated notebook tooling remain #4/#50-owned, review
2026-11-10. Original scientific data, shared receivers and sibling work are
preserved; no task kernel, server or watcher remains active.
