# Installed saved-pose nine-atom evaluation

Owner: [#4](https://github.com/uibcdf/bindingmt/issues/4), coordinated with
[#33](https://github.com/uibcdf/bindingmt/issues/33) and
[#28](https://github.com/uibcdf/bindingmt/issues/28). The
[notebook](installed_3ptb_evaluation.ipynb) completes the explicit evaluation
follow-up to the [two-search demonstration](installed_3ptb_execution.md).
Run All measures the nine saved poses without repeating preparation or searches.
MolSysMT owns selection, coordinate extraction and RMSD; public BindingMT
constructors/evaluation/summary APIs own the comparison records and interpretation.

## Caller inputs

Select an ordinary-installed scientific kernel and supply the original source
and **raw** native/displaced result JSON files with trusted expected identities,
plus a fresh output directory:

```bash
export BINDINGMT_EVALUATION_SOURCE="3PTB.pdb.gz"
export BINDINGMT_EVALUATION_SOURCE_SHA256="75b1b8e73b4c197b7dcb217fbcfdd39c451860c0fd5a86cdef587c4dbd9972be"
export BINDINGMT_EVALUATION_NATIVE="native_result.json"
export BINDINGMT_EVALUATION_NATIVE_SHA256="3dcbebda7d816c097f6e61dbea429fd7eea82389ea172d2220748bbd49913b27"
export BINDINGMT_EVALUATION_DISPLACED="displaced_result.json"
export BINDINGMT_EVALUATION_DISPLACED_SHA256="b43f9612c4fff73d7be24c2124dda1a08b2dc81cb3af0295bc2ba91885b7e6b3"
export BINDINGMT_EVALUATION_OUTPUT="new-evaluation-output"
jupyter lab
```

The [public source](data/3ptb_prospective/3PTB.pdb.gz) is retained. Raw results
remain task-owned evidence under the execution record's custody; its labelled
public observations are not replacement DockingResult files. For another run,
retain that run's actual external identities and declare its scientific scope
rather than assigning these historical hashes to new bytes. Existing outputs
are refused. No repository/developer import, private helper or data harness is
needed. The qualified archives remain private; public installation/provider
minimum/platform admission stays #30/#47.

## Seven cells and the ownership boundary

1. Admit explicit configuration and ordinary installed origins/version/policy.
2. Check file identities, original audit/captures and detached records. Preserve
   all five native and four displaced thirteen-atom poses and original snapshots.
3. Let MolSysMT read the original BEN reference and captured partner PDBQT,
   explicitly discarding the format-specific tree. Select non-H atoms with the
   provider. For this case written indices 0..8 must match original reference
   source IDs 1632–1640, names C1..C6/C/N1/N2, elements and group fields in order,
   for every pose. This verifies a declared axis; it discovers no molecular match.
   PDBQT remains a partial representation, not complete native chemistry.
4. Ask public `evaluate_redocking` to compare the full 13-atom result with the
   nine-atom coordinate reference; retain its `BMT-E002` / `reference` refusal.
   Validation confirms this calls RMSD zero times.
5. Use `msm.get(..., selection=..., coordinates=True)` for coordinate subsets;
   construct fresh public coordinate-only DockingPose/DockingResult views with
   explicit parent hash/position/population/producer/input bindings. Preserve
   parent IDs/ranks/scores/descriptors. Do not slice preparation metadata,
   fabricate verified source keys or attach 13-atom captures to a nine-atom view.
   Views claim no new engine producer/captures; original provenance remains
   explicitly parent evidence and the original full results remain unchanged.
6. Call public `evaluate_redocking` and `summarize_redocking`: positional RMSD
   **<=2.0 Å**, no fit/alignment/symmetry, first-N positions **1 and 5**. The
   coordinate reference honestly declares positional correspondence after the
   identity checks. MolSysMT performs all nine measurements.
7. Save independent views, axes, reports, summary and receipt by exclusive
   creation. Verify original full records/files and caller policy again.

This is case orchestration through existing public APIs, not a new molecular
routine or copied private heavy-pose projector. No provider gap or new runtime
API is needed for this route.

## Registered receiving — 2026-11-03

The [prospective contract](installed_3ptb_evaluation_registration.md) and
[pre-measurement registration](https://github.com/uibcdf/bindingmt/issues/4#issuecomment-6619642093)
freeze the criterion/population. Source is
`d026434f6e1171f52ef513436fc46bf4e766a382`, notebook SHA-256
`ad56bda7b1a6d9f858622746c8ca20dcb04fc7e125db2f41ea6f8d2c4018c25f`.
Search outcomes/scores and older benchmarks were already known; this is
retrospective receiving of one hypothesis, not a blinded independent benchmark.

| Case | Saved poses | First RMSD (Å) | Closest RMSD (Å) | First / first-5 contains <=2 Å |
| --- | --- | --- | --- | --- |
| Native | 5 | 1.933697408 | 0.228345742 | Yes / yes |
| Displaced | 4 | 65.312390922 | 62.073958093 | No / no; first-5 considers all four |

First and closest are different observations; no reranking occurs. Native's
first pose is close to the specified threshold. Phenyl/amidinium ambiguity is
uncorrected. These finite observations do not estimate independent-complex
success rates, experimental affinity, environmental protonation or model quality.

Both real kernels complete the exact seven cells on their first receiving
attempt, with no kernel warnings, and shut down. Normal and pm/fs profiles each
measure the same nine poses: **18 measurements, nine distinct poses**. The
maximum absolute physical difference is `1.4210854715202004e-14 Å`, within the
registered `1e-12 Å`; criteria/order/counts/recovery agree exactly. Actual
geometry/report digests remain separate. The [receiving receipt](data/installed_3ptb_evaluation/receiving_2026-11-03.json)
and [manifest](data/installed_3ptb_evaluation/manifest_2026-11-03.json) bind source,
registration and exact [normal reports](data/installed_3ptb_evaluation/normal_evaluations.json),
[pm/fs reports](data/installed_3ptb_evaluation/pm_fs_evaluations.json) and summaries.

Validation-only pre/post cells verify original 63 consumer / 3,415 molecular
payloads and loaded core/support/provider/engine origins before/after. The
unchanged consumer remains `0.0.0+225.g50d8e33`, producer `50d8e33`, archive SHA
`5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`; MolSysMT
remains archive producer `de7ffad2a` / controlled main `00abb958f`, SHA
`4a8e58f40627ff468fab99301674429fba66362f549a31fb4cc747d9cf19a0ba`.
Python is 3.14.8 and dependency closure passes. Per kernel, counters observe
three evaluation requests (one refusal), two result RMSD calls, nine pose/provider
RMSD calls and one summary. Preparation/engine/reconstruction/viewer guards
observe zero attempts; developer imports are blocked. No source/harness/SDK is
on the configured kernel path. Runtime, dependencies and CI workflows are unchanged.

The final installed software selection passes **131 tests**, zero skips, with
two engine-entry tests explicitly deselected. Forty warnings comprise 39 legacy
H5MSM reads and one preimported-SMonitor assertion-rewrite warning. Source-free
context `1c34392` contains byte-equal evaluation/summary tests and installed
origins are checked. Initial software selections failed because an absolute
deselect did not match and a legacy producer also entered docking; all three
requests were blocked before native execution. The first selection entered an
out-of-scope 181L preparation fixture. Those failed software receipts are
retained separately; the corrected offline selection excludes both engine
entry points. They are distinct from the two successful 3PTB scientific kernels,
and no original input, criterion or expected result was changed to obtain a pass.

## Remaining work and custody

The installed preparation → execution → saved-record inspection → explicit
nine-atom evaluation path is delivered for this case, without needing a browser
or new molecular tool. Continue with exact-head hosted-gate recovery and actual
public dependency/candidate readiness under #30/#47. #4/#33 retain their broader
source/replay and scientific-profile scopes. Visible C4/C6 remains deferred under
#52/#60; no whole-Core, general chemistry, molecular persistence or public
distribution acceptance follows from this example.

Small input copies, executed notebooks, raw views/receipts and failed software
selections remain #4/#50-owned reproducibility evidence, review 2026-11-10.
Original scientific files/receivers and sibling worktrees are preserved. No
task kernel, server or watcher remains active; operational paths/diagnostics
are not published.
