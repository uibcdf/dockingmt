---
summary: Portable evaluation CI assumes recovery from a low-budget stochastic search.
issue: uibcdf/dockingmt#46
status: resolved
opened: 2026-10-07
closed: 2026-10-07
severity: medium
verification: measured
area: [tests, ci, validation]
guard: tests/test_redocking_evaluation.py::test_native_181l_external_1iep_and_displaced_box_reports
normative:
blocked_by: []
supersedes: []
---

# Stochastic redocking CI expectations

## What

Scheduled matrix [37491745012](https://github.com/uibcdf/dockingmt/actions/runs/37491745012)
at `d419feeb70a09e9f27035fc5b759f38e1793fbeb` fails on macOS arm64 Python 3.13
and 3.14 at `tests/test_redocking_evaluation.py:295`. Each cell has 886 passing
tests and one false assertion that the first live 1IEP pose is recovered.
The Vina 1.2.7 search uses seed 42, one CPU and exhaustiveness 1. The failed
RMSD and the precise native numerical cause are not retained by those logs.

## How

Keep the live searches, unchanged inputs, 2.5 angstrom declaration and displaced
domain control. Capture actual results in the test and independently compute
positional RMSD from their returned coordinates and the recorded reference,
respecting the verified atom keys. Check recovery against the declared cutoff,
first/closest positions and captured backend bytes. Preserve the earlier
measured positive and displaced observations in a separate retained-data guard.
Existing analytic translations test both recovered and unrecovered evaluations.

## Why

A recorded low-budget search outcome does not establish a portable requirement
that every platform must recover its first pose. The software contract is the
faithful evaluation of whatever poses the search actually returns. Scientific
recovery rates still require explicit experiments and informative hypotheses.

## What was refuted

Do not change the cutoff, retry until a pose passes, skip macOS or tolerate a
failed cell. Linux success does not certify macOS. Logs establish the failed
recovery expectation, not its precise numerical cause.

## Scope and exclusions

Owns the evaluation integration test. No search parameter, production RMSD,
preparation policy, engine algorithm or historical observation is changed.
Installed delivery and recurring recovery remain with #30 and #21.

## Acceptance criteria

- Live report geometry agrees with an independent positional calculation.
- Deterministic controls cover recovery and nonrecovery at the unchanged cutoff.
- Earlier recorded scientific observations remain unchanged and guarded.
- Corrected required Linux and representative macOS lanes actually execute.

## Corrected checkpoint — 2026-10-07

At `8741fb2e104814e6f1012e0cb7073689e710f982`, the installed consumer passes all
986 tests without skips, and [required CI](https://github.com/uibcdf/dockingmt/actions/runs/37581673369)
passes 986 tests on each supported Linux Python minor. The
[manual matrix](https://github.com/uibcdf/dockingmt/actions/runs/37581760344)
also passes all four Linux cells; both macOS jobs remain pending without a
runner assigned at inspection. This report stays partial until those corrected
platform controls actually execute and pass. Their state is not interpreted as
scientific success or failure. Evidence and remaining limits are retained in
the [checkpoint](../validation/installed_integration_checkpoint_2026-10-07.md).

## Resolution — 2026-10-07, 06:57 UTC

The same [manual matrix](https://github.com/uibcdf/dockingmt/actions/runs/37581760344)
now completes successfully on producer
`8741fb2e104814e6f1012e0cb7073689e710f982`. Both macOS arm64 cells actually run
all 986 tests without skips: Python 3.13 in 197.41 s and Python 3.14 in 188.14 s,
with 382 warnings each. All four Linux cells also pass 986 tests without skips.
Interpreter/architecture/Vina and ordinary installed-import checks execute in
every scientific cell. The earlier pending observations remain historical.

This resolves the portable evaluation guard defect. The live geometry guard and
retained-data/analytic controls remain durable. No recovery cutoff, search
parameter, production algorithm or recorded scientific observation is changed.
Public artifact/dependency qualification stays in #30; these source/import
cells do not certify chemistry or an entire public installed OS/Python matrix.
