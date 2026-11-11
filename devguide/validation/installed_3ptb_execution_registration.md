# Prospective installed 3PTB two-search demonstration

Owner: [#4](https://github.com/uibcdf/bindingmt/issues/4), preparation coordination
[#33](https://github.com/uibcdf/bindingmt/issues/33). Registered before execution
on 2026-11-03. This document fixes a new workflow demonstration; it is not the
original 24-search benchmark, the original five-pose human result, or a new
scientific recovery/affinity experiment.

## Fixed source and finite population

Use the ordinary-installed private consumer `0.0.0+225.g50d8e33`, archive
SHA-256 `5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`,
with unchanged MolSysMT archive producer `de7ffad2a`, SHA-256
`4a8e58f40627ff468fab99301674429fba66362f549a31fb4cc747d9cf19a0ba`, controlled
main `00abb958f`, and Vina 1.2.7. Python is 3.14.8 on Linux. The receiving
record must bind actual installed origins/payloads and the native Vina artifact;
advertised versions alone do not identify those bytes. No package is rebuilt.
The reviewed repository baseline is `b743db0812a67dd2873cfc12128026649ea0f301`;
the committed execution notebook and registration receipt identify the new
workflow source separately from the unchanged runtime archive producer.

Replay the [preparation notebook](installed_3ptb_preparation.ipynb) once using its
existing external source/declaration identities and unchanged chemistry/maps,
including its original prepared-value controls. Its expected file identity is
`c6c5a6660b8b5d46df01cde6960129a7bc65db81d551b3ad0a4d763fc0907da9`.
Use the [inspection notebook](installed_result_inspection.ipynb), identity
`bfe922f86012834ba12bf9cb1ada5098944c6979fee00523ef9fd38ba25ee3e0`, for
saved-record reading. Both are explicit trusted code inputs, executed through
public IPython `%run`, without repository/developer helpers.

| Case / order | Receptor / partner | Box | Search / retrieval |
| --- | --- | --- | --- |
| 1: native | Same declared 2,011-atom dry receptor / rigid 13-atom benzamidinium | 20 Å cube at the provider-computed reference centre | Seed 7; exhaustiveness 1; CPU 1; at most 9 poses; 3 kcal/mol window |
| 2: displaced | Exactly the same prepared inputs | Same cube, centre displaced +60 Å on x | Exactly the same protocol |

Vina scoring, captured backend inputs and empty active cuts are explicit. No
flexible arm, new chemical state, tuning, standalone optimization, rescoring or
retry is included. Wrapper defaults remain `max_evals=0`, `min_rmsd=1.0 Å`,
map spacing `0.375 Å`, `force_even_voxels=False`; retain actual resolved calls
rather than claiming planned values were submitted. Two calls imply at most
18 returned poses, not a promise that nine poses are returned from either call.

## Attempts, persistence and inspection

The [execution notebook](installed_3ptb_execution.ipynb) writes both planned rows
before the first attempt. Each case is attempted once, in the order above.
Append progress before/after each attempt; preserve exceptions and counts. A
failed case remains in the denominator and does not prevent the second planned
attempt. Preserve any completed result before further analysis. No failed or
empty result is replaced by another seed, effort, state or repeated call.
If later inspection fails, repair/review the saved-record path without rerunning
the searches. Any scientific rerun needs a new registration.

Retain complete `DockingResult.to_dict()` JSON files, original hashes, captured
input bytes/hashes, full thirteen-atom poses, all recorded score definitions,
native energy vectors, submitted boxes and resolved calls. Inspect both records
through the unchanged eight-cell public reader, including its nondefault unit
policy and refusal controls. Validation guards count at most two Vina
initializations/maps/searches and forbid fixed-pose score/optimization,
RMSD/reconstruction/viewer calls and developer imports. Verify original
consumer/molecular payloads before and after, preserve caller policy, and close
the real kernel on success or failure. Do not rerun the execution notebook just
to qualify another unit policy: use saved-record inspection instead.

**Evaluation decision fixed before outcomes:** retain all thirteen-atom poses;
perform zero RMSD evaluations in this demonstration. The nine-heavy-atom
reference needs a separately declared comparison population/correspondence
before any future recovery measurement. Do not locally project pose metadata,
copy the private heavy-pose helper or implement molecular matching/geometry.
All molecular operations remain MolSysMT-owned. Counts, scores, consistency and
detached readback establish workflow behavior, not near-reference recovery,
experimental affinity, model suitability or whole-Core acceptance.

Raw records/diagnostics remain task-owned reproducibility evidence under #4/#50,
review 2026-11-10. Reuse the existing scientific receiver/kernel tools; preserve
all original data/results/receivers and sibling work. Public receipts contain
scientific identities/hashes and compact observations, without personal
operational paths or raw machine diagnostics. Public delivery remains #30/#47;
visible C4/C6 remains deferred under #52/#60.
