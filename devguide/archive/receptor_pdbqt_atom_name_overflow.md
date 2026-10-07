---
summary: Reject receptor atom names that overflow fixed PDBQT columns
issue: uibcdf/dockingmt#44
status: resolved
opened: 2026-10-06
closed: 2026-10-07
severity: medium
verification: measured
area: [preparation, export]
guard: tests/test_preparation.py::test_receptor_pdbqt_rejects_overwide_names
normative:
blocked_by: []
supersedes: []
---

# Reject receptor atom names that overflow fixed PDBQT columns

## What

The explicit 181L receptor workflow under #4/#5 materializes provider hydrogens
named `H1291`, etc. `PreparedReceptor.to_pdbqt()` uses minimum width four rather
than a bounded atom-name field. A five-character name shifts the coordinate
columns. Installed Vina 1.2.7 rejects coordinate text `8  10.14` although the
actual atom coordinates are `[44.104, -3.558, 10.141]` angstrom.

## How

Reject atom names outside one to four characters with an actionable argument
error, matching the existing ligand writer constraint. Preserve valid receptor
bytes and source names; no implicit truncation or renaming. The separate
fixture-specific workflow may declare new generated-atom labels through the
public MolSysMT setter before charge/type binding and retain its full map.

## Why

Malformed fixed-column representations cannot reach the docking engine.
Hydrogen inventory, typing and charge success do not establish export validity.

## What was refuted

The error is reproduced with a single synthetic receptor atom, independently
of molecular chemistry, Vina search or MolSysMT conversion. Merely assigning
AutoDock types or changing the Vina protocol cannot repair shifted fields.

## Scope and exclusions

This consumer writer defect covers the atom-name width. Other fixed-column
limits and provider export/name projection remain distinct; MolSysMT #223 owns
the general transformation. No scientific preparation qualification follows.

## Acceptance criteria

The addressable guard rejects empty/five-character names without mutating the
preparation. A valid four-character name retains exact coordinate/charge columns
and parses with installed Vina. Existing preparation/export regressions pass.

## Resolution — 2026-10-07

The receptor writer now rejects names outside one to four characters before
constructing an ATOM line. The guard reproduces both empty and generated
`H1291` names and asserts unchanged source labels. The companion valid-name
control checks fixed coordinate/charge columns and installed Vina parsing.
The real 181L workflow records explicit generated-H label choices and yields
six default Vina results without malformed coordinates.

Final local Python 3.14 source gate: 985 passed, no skips, 338.86 seconds, with
171 retained warnings. Ruff lint/formatting and the six-cell evidence notebook
pass. This is a local fix, without a push or hosted/public artifact claim.
Scientific preparation qualification remains under #4/#5/#33; the width defect
is resolved independently. See the
[workflow and original evidence](../validation/181l_receptor_workflow.md).
