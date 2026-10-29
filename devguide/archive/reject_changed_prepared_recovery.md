---
summary: Reject changed prepared inputs during saved-result recovery
issue: uibcdf/dockingmt#57
status: resolved
opened: 2026-10-29
closed: 2026-10-29
severity: high
verification: measured
area: [provenance, preparation, recovery]
guard: tests/test_prepared_recovery.py
normative: devguide/validation/prepared_recovery.md
blocked_by: []
supersedes: []
---

# Reject changed prepared inputs during saved-result recovery

## What

`DockingResult.reconstruct_problem` accepts a supplied prepared ligand with a
changed state label and charge despite their original values remaining in the
saved problem. The saved source axes/native-state association do not bind those
prepared declarations. This is a concrete #4 recovery gap.

## How

At `12b5360`, save an empty software-control result with one-atom prepared inputs
using supplied zero charges and state `partner-A`. Change the supplied partner
to `different-state` / 0.5 e. Recovery succeeds and attaches the changed object.
The probe performs no native calculation or search.

Compare the recorded prepared declaration before attachment. Where a saved Vina
PDBQT digest exists, use the existing public MolSysMT-backed prepared writer to
check the supplied representation. Validate captured-byte integrity when present;
propagate provider errors and retain failed-recovery atomicity. Missing evidence
remains explicit rather than being invented.

## Why

A caller can otherwise recover a different scientific input while retaining the
old result's problem/provenance. Replay comparison after a new search is too late
to protect recovery itself.

## What was refuted

Matching counts, atom axes or absent native state IDs do not establish that the
supplied prepared state, parameters or submitted coordinates match the record.
A backend-byte match is not full molecular identity or native persistence.

## Scope and exclusions

Existing saved-result recovery for prepared roles only. No molecular parser,
matcher, snapshot, generic archive or implicit preparation. Provider persistence
remains MolSysMT #256; #4 stays partial beyond this fix. No new scientific search,
visual acceptance or public publication.

## Acceptance criteria

Both roles reject changed recorded declarations and available submitted-byte
bindings before attaching a problem. Matching and legacy missing-evidence routes
remain usable with documented limits. Provider errors, caller/source immutability,
unit policy, corrupt records and result preservation have meaningful controls.


## Resolution — 2026-10-29

[The implemented contract](../validation/prepared_recovery.md) binds finite saved
object declarations and available Vina input hashes before attaching a recovered
problem. Recorded object declarations cannot be bypassed by supplying backend
text. Retained artifact integrity is checked before native exports; provider
errors propagate. Legacy missing evidence establishes no additional identity.

The 38-case guard covers the original state/charge mismatch, both-role metadata/
representation changes, corruption, atomicity, public native writer consumption,
unit policy, source preservation and explicit precision/missing-evidence limits.
The final source selection passes 271 cases, zero skips. Ordinary installed and
exact-head receipts are recorded separately on #57; #4 remains partial for the
broader source-bundle/persistence contract. No molecular snapshot or original
scientific result is reconstructed or rewritten by this fix.


## Mixed-input preflight completion — 2026-10-29

A two-case ordinary-installed control on the initial `37d83d0` candidate exposes
missing validation of the external role's capture when the other role is prepared.
The correction checks both retained roles before rendering either prepared input.
The final source selection passes 273 cases, including all 40 guards. The earlier
271-case/38-guard receipts retain their source/artifact identities and do not
qualify this newly tested boundary. Separate final installed/exact-head receipts
remain on #57; no historical artifact or molecular provider implementation changes.
