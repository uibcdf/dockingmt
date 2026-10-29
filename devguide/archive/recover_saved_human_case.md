---
summary: Recover the saved 3PTB human result from verified linked evidence
issue: uibcdf/dockingmt#58
status: resolved
opened: 2026-10-29
closed: 2026-10-29
verification: measured
area: [provenance, recovery, human-workflow]
guard: tests/test_saved_3ptb_case_recovery.py
normative: devguide/validation/saved_human_case_recovery.md
blocked_by: []
supersedes: []
---

# Recover the saved 3PTB human case offline

## What

Promote the already executed task-local file/record checks into one reproducible
case-specific developer operation returning the saved `DockingResult` and an
explicit verification report. This follows #57 without creating a generic bundle
format or a native molecular snapshot under #4.

## How

Verify the externally expected qualification digest, all existing member byte/
decoded identities, source/admission/result links and original producers. Reuse
public result reading, captured-input verification and saved-result audit. Read
members relative to the supplied bundle, ignoring old operational source paths.
Recover the result record only, preserving `problem is None` and absent original
file fingerprints. Write a new report exclusively after success.

## Why

The frozen notebook and qualification already preserve the necessary evidence,
but resuming inspection currently requires task-local scripts or notebook cells.
A relocated retained case should be verifiable without preparing again or running
a molecular engine. MolSysMT #256 remains the molecular persistence owner.

## What was refuted

Manifest self-consistency is not external authentication or chemical validation.
Recovered result coordinates are not a restored complete molecular system. No
PDB/PDBQT parser or new molecular correspondence tool is needed for record links.

## Scope and exclusions

The existing 2026-10-20 five-pose human case and its saved file layout. Original
notebooks/archives/registrations remain immutable. No new scientific search,
preparation, energy, viewer call, generic archive API or public package release.

## Acceptance criteria

A documented command verifies/reloads the real saved case and relocated copies;
meaningful controls reject bad files, decoded evidence, source and record links.
No molecular or native computation occurs. CLI failures create no report and
existing caller files are protected. Reports retain original/current identities
separately and omit machine-specific paths. Broader #4 remains partial.

## Outcome

The developer operation and documented CLI recover the original five-pose case
after verifying its 16 members and linked records. The 26-case guard covers real
recovery, relocation, corrupt evidence, contradictory records and safe output
handling. The focused source selection passes 137 tests without skips. Ordinary
installed-consumer and exact-head hosted receipts are recorded separately on #58;
the unchanged runtime retains its qualified c384ed2 artifact. All 389 historical
evidence files remain byte-identical. Broader #4 remains partial.
