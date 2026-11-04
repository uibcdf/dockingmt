# Installed saved-result inspection

Owner: [DockingMT #4](https://github.com/uibcdf/dockingmt/issues/4), following the
[human workflow review](../human_workflow_review.md). The maintained
[notebook](installed_result_inspection.ipynb) reads and inspects a caller-supplied
DockingResult JSON record using existing public APIs. It requires no repository
imports, developer tools, data harness or molecular reconstruction.

## Use the notebook

Select an ordinary-installed DockingMT Python environment satisfying its declared
dependencies, with Jupyter tooling available to the kernel. Work in a directory
of your choice with the notebook and your result file. Before starting Jupyter,
set the two explicit inputs:

```bash
export DOCKINGMT_RESULT_PATH="saved_result.json.gz"
export DOCKINGMT_RESULT_SHA256="DIGEST_FROM_YOUR_TRUSTED_SOURCE"
jupyter lab
```

Alternatively, replace the first cell's two configuration assignments with your
chosen path and independently expected digest. `.json` and `.json.gz` are
supported through standard JSON/gzip IO. The notebook checks the actual file's
SHA-256 before interpreting JSON. It refuses an editable/source-overlaid reader
and prints only a compact summary rather than raw provenance or captured bytes.
The output contains the reader version, pose rows and a final receipt.

For the retained public example, obtain a copy of the
[original compressed result](data/human_3ptb/native_result_2026-10-20.json.gz)
and use the externally recorded file digest:

```text
4b1f51cdeb135fd6785a181f6bb09a0d0f631ec3d9de7c169c88703748924249
```

That is the compressed-file identity recorded in the original
[qualification](data/human_3ptb/qualification_2026-10-20.json), whose externally
expected SHA-256 is
`b89b8dcb9ec296d01f12cd28cb633577e868e5c60b264c5f4bb4eefd6f3b9bf2`.
The decoded result identity is
`ed0eeb3ade25e54f8a5829729578fcbec9f0d73d6c0ceb03d146b0c3492d7fac`.
Use a trusted copy of the expected identity. Computing a fresh digest from an
untrusted replacement does not authenticate its history.

This example installation is qualified below as a private archive. It does not
establish a public installation command, published provider minimum or platform
matrix. Existing package/admission work remains #30/#47.

## What the eight cells do

1. Admit explicit caller inputs and identify the ordinary installed reader.
2. Match file bytes to the external expectation, decode JSON and retain the input.
3. Call `audit_result`, admit the result schema with `DockingResult.from_dict`,
   and use `verify_captured_inputs` when both captures have consistent evidence.
4. Inspect collection position, optional rank/ID, recorded scores/descriptors
   and stored coordinates with an explicit angstrom display. No ranking or
   score-unit inference occurs; zero and unknown values are preserved.
5. Refuse an unsupported schema and, when captures exist, a changed partner digest
   on detached copies. Catch the public SMonitor exception base and check its
   structured diagnostic fields, without importing private DockingMT exceptions.
6. Repeat reading under a pm/fs/kJ policy and restore the caller's policy.
7. Verify independent `to_dict` / `from_dict` roundtrip and unchanged input.
8. Emit a compact receipt distinguishing recorded producer from current reader.

An `inconsistent` audit stops the example. An `incomplete` audit remains explicitly
incomplete: reading a schema-admitted record is not complete provenance. Missing
captures are reported as unavailable and are not reconstructed. Unknown score
units/methods remain unknown. Quantity conversion checks physical record meaning
with relative tolerance `1e-12` and zero absolute tolerance; this is not RMSD,
alignment, atom correspondence or molecular characterization.

The result remains `problem is None`. A later `reconstruct_problem` requires the
actual necessary inputs and checks available declarations/submitted bytes; it
does not infer a complete molecular system from JSON or PDBQT. The notebook
does not call it. General molecular persistence remains MolSysMT-owned (#256),
and the remaining partial/reference reading profile stays MolSysMT #521.

## Executed receiving — 2026-11-03

The [receipt](data/result_inspection/receiving_2026-11-03.json) and
[manifest](data/result_inspection/manifest_2026-11-03.json) bind the exact notebook
bytes, each executed source cell, reader archive and original result identity.
The committed notebook has clean outputs; executed copies/raw diagnostics remain
task-owned evidence. No original notebook or scientific artifact is rewritten.

Both real-kernel profiles complete all **eight exact formatted source cells**:

| Input profile | Observed result |
| --- | --- |
| Original five-pose 3PTB record | Audit consistent; original captures verified; schema and changed-capture controls refuse with `DMT-E002`; detached result, identities/ranks/scores/units and original bytes preserved. |
| Derived software control with captures removed | Audit incomplete; captures unavailable, with no fabricated replacement; unsupported schema still refuses; the same five pose records and detached reading/roundtrip remain intact. This is not a second original scientific result. |

Execution starts outside the repository with no source/data harness or SDK in
the configured kernel path. Only task Jupyter tooling supplements the independent
scientific prefix. The original DockingMT wheel is reused: producer
`50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9`, version `0.0.0+225.g50d8e33`,
SHA-256 `5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`.
Its 63 payload files and loaded core/support/provider origins are checked before
and after execution. Runtime source equals the reviewed `8f17116` profile;
no archive is rebuilt or relabelled. Python is 3.14.8 and dependency closure passes.

The raw result retains original version `0.0.0+180.g1decee5`; the qualification
links that original artifact to producer `1decee504b112cfd92026c52dcbe22449de30f4f`.
Reading it with the newer installed wheel does not change that identity. The
notebook does not independently authenticate historical software bytes or all
members of the original case bundle; the [forensic recovery operation](saved_human_case_recovery.md)
retains its stronger separate scope.

Validation-only pre/post cells surround unchanged user cells. Required MolSysMT
bootstrap import is recorded; its public molecular operations and DockingMT
preparation/execution/RMSD/reconstruction/rendering calls are guarded afterward.
No guarded operation is attempted. Developer-tool, optional engine, Viewer,
RDKit and OpenMM imports remain blocked/absent during the receiving profiles.
These observations establish the notebook's scope, not permission to remove
declared runtime dependencies. Both kernels are shut down explicitly.

The initial validation prelude fails before any user cell because its guard
incorrectly forbids required MolSysMT bootstrap import. The corrected guard
allows initialization and blocks actual molecular calls. Both profiles pass;
after one import-order fix and shared formatting, both are re-executed against
the exact final cell hashes. These attempts are retained separately and are not
added as distinct scientific cases. No provider defect is inferred.

Existing installed audit/schema guards pass **144 tests**, zero skips, in 1.46 s
with one preimported-SMonitor assertion-rewrite warning. Their source-free test
context is `1c34392`, with the two test files byte-equal to current source. These
are software tests, not 144 scientific cases. The older full 1,449-pass receiving
keeps its own original producer/scope and is not relabelled as a new full suite.

## Remaining work and custody

The bounded installed record-inspection example is delivered. Next scope the
explicit preparation-to-execution walkthrough against an actual user need;
keep scientific prescriptions visible and any new computation separately
registered. No general archive, molecular snapshot, IO convenience API or hidden
preparation recipe is introduced here. #4 stays partial for its broader workflow.

Public publication-route decisions remain #29. This notebook does not accept
scientific chemistry/model suitability, public package/platform delivery,
browser controls or C6. Visual review stays deferred under #52/#60.

Small input copies, execution diagnostics and receipts belong to #4/#50, review
**2026-11-10**, for reproducibility. They reuse the existing scientific receiver
and task kernel tools. Original receivers, artifacts and shared/sibling work
are preserved. No kernel, server or watcher remains active.
