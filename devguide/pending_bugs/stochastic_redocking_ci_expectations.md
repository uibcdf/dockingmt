---
summary: Portable evaluation CI assumes recovery from a low-budget stochastic search.
issue: uibcdf/dockingmt#46
status: partial
opened: 2026-10-07
closed:
severity: medium
verification: reproduced
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
