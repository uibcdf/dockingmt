---
summary: Evaluate redocking with explicit RMSD policy and detached comparison evidence.
issue: uibcdf/dockingmt#38
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [analysis, validation]
guard: tests/test_redocking_evaluation.py
normative:
blocked_by: []
supersedes: []
---

# Public redocking evaluation

## What

Provide a reusable finite JSON report for a single docking result and reference.
The caller supplies the RMSD cutoff and explicitly declares a common receptor
coordinate frame. Preserve current result order separately from stored ranks.

## How

Reuse public `DockingResult.get_rmsds` and MolSysMT geometry. Molecular/pose
references require existing verified atom keys. Explicit coordinate quantities
are a caller-selected positional comparison and are labelled accordingly;
they never certify molecular correspondence. All poses use the same atom
population/count, with no conflicting known ligand/receptor state IDs.

Retain per-pose RMSD/identity, first/closest pose, first-N recovery, atom and
reference coordinate evidence, caller reference declarations, provider version
and detached problem/protocol/preparation/ranking context. Never align the
ligand, silently rerank, correct symmetry or infer chemical readiness.

## Why

Existing RMSD calculations and example scripts lack a common reusable evaluation
report. Single-case recovery must remain distinguishable from dataset success
rates and scientific preparation validation.

## What was refuted

No default numerical success threshold, general matching implementation,
clustering framework, engine rerun inside evaluation or local RMSD formula.

## Scope and exclusions

One result against one reference frame, retained pose atoms, explicit <= cutoff,
first-N positions. General molecular operations remain owned by MolSysMT.
Sibling worktrees are preserved. Missing capabilities receive provider issues.
Chemically constrained symmetry correspondence is handed off in
[MolSysMT #310](https://github.com/uibcdf/molsysmt/issues/310), without blocking
this explicitly uncorrected operation.

## Acceptance criteria

Known geometric controls, identity/population checks, error propagation,
non-default unit policy, strict JSON detachment and a real Vina notebook using
181L provisional preparation and external 1IEP/displaced-box controls. Local
gates pass in the qualified shared Python 3.14 profile.

## Measured outcome — 2026-10-03

Public `dockingmt.evaluate_redocking` returns the independently serializable
report described in [the contract](../validation/redocking_evaluation.md).
The 44 new guard cases cover independent translation/permutation expectations,
first-position versus closest pose, ties, recorded order/ranks, known/unknown
states, population/count admission, reference selection, literal cutoff,
non-default units, finite real measurements, original provider errors, detached
JSON and saved-reader operation without Vina/MolSysViewer imports. The native
guard checks provisional 181L, unassessed external 1IEP and a displaced domain.

All **750 tests pass without skips in 183.19 s**, in editable
`molsyssuite@uibcdf_3.14` on Python 3.14.7/Vina 1.2.7 with unchanged exact
provider pins. All three notebook code cells execute, retaining three native
reports and their fixed-unit comparison evidence. Ruff lint/format, generated
indexes, reporting guard and diff checks pass. The 96 known provider warnings
remain visible; more legacy H5MSM reads come from the new controls.

The first focused run exposed an invalid test fixture that set both coordinates
and an existing finite score to NaN; it was corrected to alter only geometry.
A subsequent test of a boolean provider measurement initially used an invalid
boolean quantity constructor at collection. It now uses a supported scalar
array representation. No provider errors or test cases are suppressed; the
final full gate checks real/boolean/complex measurement admission explicitly.

MolSysMT #310 receives the future symmetry-correspondence requirement. Its
positional distinction probe executes against the exact provider pin: circular
permutation of the six C1..C6 181L coordinates gives 1.367 Å positional RMSD.
This is a method distinction, not proof of arbitrary chemical equivalence.
No sibling implementation, dependency metadata or CI pin changed.

## Shared host dependency closure

The separate `python -m pip check` exits **1** after an unrelated concurrent
installed-source change: Sabueso `0.11.0+19.g01d5bf2` requires Ackredit >=0.9.0,
while installed Ackredit is `0.8.0+68.g93b5989.dirty`. This finding is reported
to the shared-workspace owner in
[MolSysSuite #82](https://github.com/uibcdf/molsyssuite/issues/82#issuecomment-5974182219),
which already routes joint Sabueso qualification to MOLI #40/Sabueso #109.
The earlier successful host closure receipt remains historical. No package
floor/version was fabricated and no provider installation or worktree changed.
This bounded DockingMT gate does not certify the complete current host or a
public dependency release; that closure remains provider/workspace-owned.

### Correction — withdrawn metadata diagnosis, 2026-10-03

The maintainer clarified that the mismatch above came from stale editable-install
metadata, refreshed by reinstalling the editable package. The interpretation as
a provider dependency incompatibility and its requested owner follow-up are
withdrawn in the linked MolSysSuite comment. The historical `pip check` output
only describes installed metadata at that moment; it did not demonstrate a code
or API incompatibility. The maintainer is refreshing the installation. No claim
of a newly verified successful dependency check is made in this correction.

### Refreshed installation verified — 2026-10-03

After the maintainer's reinstall, the same Python 3.14.7 environment records
editable Ackredit `0.9.0+7.g3c6e77c.dirty` from its local checkout.
`python -m pip check` now exits **0**, `No broken requirements found.`
The stale installed-metadata mismatch is resolved. This is dependency-metadata
evidence and does not extend the earlier scientific qualification.

### Full regression after metadata refresh — 2026-10-03

The full local gate is repeated after the refreshed Ackredit installation in
the same editable Python 3.14.7 environment and with the unchanged MolSysMT
and MolSysViewer qualification pins: **750 passed, no skips, 198.37 s**,
with the same 96 provider/existing warnings. Ruff lint/format, generated report
indexes and diff checks pass; `pip check` remains successful. The original
implementation commit `a5fb97b763012eb0df7fd3eb9206ce10c784fb1c` also has
successful [CI](https://github.com/uibcdf/dockingmt/actions/runs/37159093062)
and [suite policy](https://github.com/uibcdf/dockingmt/actions/runs/37159093232)
runs. This correction changes documentation only; no scientific implementation,
provider pins or previously retained notebook measurements are changed.
