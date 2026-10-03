# Incremental prepared docking

`dockingmt.dock_many(problems, protocol=None, backend=None, on_error='raise')`
returns an iterator of public `DockingOutcome` records. It executes already
prepared problems locally, sequentially, by calling the existing public `dock`.
Advance the iterator to execute one item; no later item is consumed first.

```python
for outcome in dmt.dock_many(prepared_problems, protocol, on_error='record'):
    if outcome.status == 'success':
        consume_result(outcome.index, outcome.result)
    else:
        record_failure(outcome.index, outcome.problem_info, outcome.error)
```

The [executed notebook](incremental_docking.ipynb) uses captured inputs from the
existing [minimal Vina software control](data/audit/minimal_vina_result.json).
It streams successful and failed outcomes to JSON Lines, restores them offline
and checks native equivalence with an individual call. This is the first
execution block of [issue #36](https://github.com/uibcdf/dockingmt/issues/36),
not completion of MVP E2's aggregation or scientific qualification gates.

## Inputs and execution

Supply an iterable of `DockingProblem` instances with matching
`PreparedReceptor`/`PreparedLigand` objects or existing PDBQT inputs, including
file paths, raw text and MolSysMT's explicit `pdbqt_text:` form. Recognition
reuses the existing input boundary. Automatic preparation is rejected inside
this route. Prepared input does not mean qualified chemistry; the existing
provisional/unassessed policies still apply.

Global arguments are admitted when `dock_many` is called. A non-iterable, string
or mapping source, invalid policy, protocol or backend fails immediately.
Individual inputs are admitted at consumption time. An empty source executes
no backend. The supplied source can produce problems lazily; construction errors
raised by that source remain source failures.

Backend resolution follows `dock` and happens once. Each item calls `dock` with
the resolved adapter and protocol. Vina creates a fresh native calculation and
uses its existing exact-input snapshots and cleanup; no affinity maps are
shared. Seeds, CPU settings, capability checks, units, ranking and provenance
have the same meaning as individual calls. A fixed seed is reused unchanged
for each item; an absent/zero seed retains the original backend rules. Different
inputs do not acquire a new seed policy or a scientific comparability claim.

## Outcomes and identity

`DockingOutcome` exposes these properties:

| Property | Contract |
| --- | --- |
| `index` | Zero-based position in this input stream. |
| `status` | `success` if a result was returned; otherwise `failure`. |
| `backend` | Resolved adapter name; manually constructed outcomes may leave it unknown (`None`). |
| `result` | The existing `DockingResult` on success, otherwise `None`. |
| `error` | A detached `type`, `message`, `code` summary on failure, otherwise `None`. |
| `problem_info` | Detached problem declarations captured before execution, when available. |
| `protocol_info` | Detached resolved protocol declarations for this item. |

Error `type` is module-qualified. `code` retains a nonempty string catalog code
when available and is otherwise `None`. Summaries hold no original exception
or traceback. Ordinary exception messages are retained without reinterpretation;
the record does not provide a complete causal-chain or diagnostic bundle export.
The adapter name records the selected route even when it fails; it does not
establish an external provider version. Successful native provenance retains
the existing provider/version evidence.

Known ligand/state labels remain in their existing problem/preparation/pose
fields; unknown identity stays unknown. No synthetic molecular, run or campaign
IDs are assigned. Index identifies a position only. Pose IDs remain local to
their result, so use `(outcome.index, pose.pose_id)` within this stream rather
than merging repeated `pose_1` labels into one identity. Separate streams need
caller-managed scope. Success means that execution returned a result, including
a result with zero poses; it does not mean scientific validation.

`to_dict()` exports schema `1.0` with the fields above and a serialized result.
`DockingOutcome.from_dict(record)` restores it using the existing result reader,
without reconstructing a molecular problem or rerunning an engine. Explicit
unsupported outer/nested result versions and inconsistent status/payloads are
rejected. Existing result-schema admission is preserved. Scientific declarations
are still caller/provider evidence; restoring a record does not audit them.
Use `audit_result(outcome.result.to_dict())` for a successful saved result.
Writing JSON requires JSON-compatible user metadata, as with individual results.

## Failure and ownership policy

The default `on_error='raise'` propagates the original item exception, closes the
batch iterator and leaves previously delivered outcomes with their consumer.
Explicit `on_error='record'` yields an ordinary item failure and continues.
This includes native execution, validation and capability failures; it can also
record unexpected ordinary exceptions, so consumers must review failures.
Source-iterator failures, shared protocol serialization failures, memory
exhaustion and process-control exceptions propagate in both modes. No fallback
engine, silent skip or successful replacement is chosen.

The iterator retains no growing outcome history and does not prefetch. Its
additional orchestration storage is independent of collection length; input,
result size, native engine allocations and objects retained by the source or
consumer still determine actual memory use. Materializing `list(dock_many(...))`
deliberately retains every outcome. Release or persist each outcome to keep the
consumer's storage bounded. This is a tested ownership property, not a measured
peak-memory or speed guarantee.

Input objects, supplied protocol/backend and source iterator are borrowed. Keep
them stable during each item execution. Declarations/errors are detached, while
the successful result has the same ownership as an individual `dock` call,
including its live borrowed `result.problem` reference. Custom backends retain
their existing responsibilities for independent scientific outputs. Early
`close()` consumes no later item and does not close a caller-owned source.
An abandoned iterator never performs more work in the background.

Cross-ligand aggregation/ranking, parallel execution, checkpoint/resume, campaign
models and cache reuse need separate accepted contracts and validation. General
molecular work remains in MolSysMT. No sibling implementation is changed here.

## Reproduction

Run `python -m pytest tests/test_batch.py --receptor=llm` in editable
`molsyssuite@uibcdf_3.14`. Native controls use Vina 1.2.7, CPU 1, seed 123,
exhaustiveness 1 and at most two requested poses. The tiny overlapping input
is software evidence, not a docking-quality benchmark. Comparison excludes only
wall-clock elapsed time; scores, coordinates, identities, input bytes/hashes,
descriptors, protocol and the remaining provenance match individual calls.

Select the notebook's explicit Python 3.14 Conda kernel. Full-suite source
qualification uses the unchanged CI pins: MolSysMT
`c19a47ada0c2279029abfa296cf915560610ad9a` and MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889`. Validation publication remains #29.

## 2026-10-03 qualification result

All **684 tests pass without skips in 128.69 s**, including 41 new batch/outcome
cases, on Python 3.14.7 and Vina 1.2.7. The unchanged 27 provider warnings remain
visible. Ruff lint/format, report indexes, diff and `pip check` gates pass.
The notebook's three code cells execute successfully in the requested Conda
interpreter. It persists and restores two successful results and one capability
failure, and its native comparison matches an individual call except elapsed time.

The first full run exposed a collection-order-dependent startup test, rather
than an optional-import leak. `test_no_leaky_optional_imports` now inspects a
fresh Python import, independently of preceding native execution. Both its
targeted engine-first selection and the full gate pass. This is source-qualified
software evidence within the scope above, without a performance/scientific claim.
