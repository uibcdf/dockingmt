# Offline recovery of the saved 3PTB human case

Owning issue: [DockingMT #58](https://github.com/uibcdf/dockingmt/issues/58),
a bounded follow-up under [#4](https://github.com/uibcdf/dockingmt/issues/4).

## Supported operation

The case-specific developer tool
[`recover_saved_3ptb_case.py`](../../devtools/recover_saved_3ptb_case.py) verifies
the retained 2026-10-20 human workflow and returns its saved five-pose result.
It reads evidence files and existing result records, with no molecular parsing,
preparation, energy evaluation, search or viewer call. It is not a new package API
or a general archive format.

From a checkout with the qualified DockingMT consumer available:

```bash
python -m devtools.recover_saved_3ptb_case \
  --bundle devguide/validation/data/human_3ptb \
  --source devguide/validation/data/3ptb_prospective/3PTB.pdb.gz \
  --report saved-3ptb-verification.json
```

Choose a new report filename: existing output is never overwritten. Verification
failure writes no report. A failed write removes only the newly created partial
file; a failed cleanup is explicitly reported. Newly created parent directories
may remain after an output-write failure.

Python callers can inspect the result directly:

```python
from devtools.recover_saved_3ptb_case import recover_saved_case

result, report = recover_saved_case(bundle_directory, original_compressed_source)
assert result.problem is None
assert len(result.poses) == 5
```

The supplied directory may be relocated. Members are resolved relative to it;
historical operational `source` paths and import locations are ignored. Absolute
member paths, traversal, duplicate resolved files and escaping symlinks reject.

## Evidence and trust boundary

The default externally expected qualification SHA-256 is
`b89b8dcb9ec296d01f12cd28cb633577e868e5c60b264c5f4bb4eefd6f3b9bf2`.
The tool verifies that manifest before reading its members, then verifies all
16 member lengths and SHA-256 values, including declared decoded identities.
An explicit `--qualification-sha256` override is a caller trust decision; a
self-consistent replacement manifest does not establish external authenticity.

It checks the actual supplied compressed original-source hash against admission
and execution records, the decoded result identity against the summary, original
producer/version agreement, the rigid/native protocol and domain, prepared object
declarations and submitted PDBQT identities. Existing public
`verify_captured_inputs`, `audit_result` and `DockingResult.from_dict` provide
captured-byte validation, saved-record consistency checks and result reading.
The uncompressed source digest is explicitly an original admission declaration;
the verifier does not parse or independently read that molecular source.

The report distinguishes original producer
`1decee504b112cfd92026c52dcbe22449de30f4f` from the current verifier's version
and script hash. Original provider sources, versions and wheel receipt are
retained as recorded evidence. Historical package files are **not** independently
reverified by this operation. The report omits old machine-specific paths and
accounts; it does not copy the raw qualification or execution records.

## Recovery limits and ownership

The result remains detached: `problem is None`. Existing absent standalone-input
fingerprints remain absent. Recovery does not invent a native system, chemical
state, mechanical assignment or replayable molecular problem. The separate
[prepared-input recovery checks](prepared_recovery.md) apply when callers supply
actual prepared objects to reconstruct a problem.

General molecular persistence remains MolSysMT-owned, including
[MolSysMT #256](https://github.com/uibcdf/molsysmt/issues/256). Broader source
families and reusable workflow/persistence remain partial under #4. Partial/
reference pose reading remains #49/#33 with MolSysMT #521. The provider migration
notice #56 does not change dependency pins. Visible C4/C6 remains deferred under
#52; public delivery retains #30/#47. File integrity and record agreement establish
neither chemical validity, affinity accuracy nor whole-Core scientific acceptance.

## Verification

[`test_saved_3ptb_case_recovery.py`](../../tests/test_saved_3ptb_case_recovery.py)
guards real-case recovery, relocation, immutable originals, non-default units,
forbidden molecular/engine operations, wrong trust roots, source/file/decoded
damage, escaping paths, contradictory record links despite updated file hashes,
output protection and write/cleanup failures. Source, ordinary-installed consumer
and exact-head hosted evidence are recorded separately on #58. The unchanged
58-file runtime retains the original qualified `c384ed2` wheel and its digest;
this developer-tool change does not rebuild or relabel it.

Temporary verification resources belong to #58/#50, review 2026-11-05, without
automatic deletion. Public records retain resource classes; operational details
stay local. Original notebooks, archives and scientific producers are unchanged.
