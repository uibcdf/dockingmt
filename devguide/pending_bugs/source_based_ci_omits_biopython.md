---
summary: Source-based CI omits Biopython needed by the scientific test stack.
issue: uibcdf/dockingmt#11
status: active
opened: 2026-09-22
closed:
severity: medium
verification: reproduced
area: [ci, dependencies]
guard: tests/test_governance_baseline.py::test_source_based_ci_includes_exercised_biopython_dependency
normative:
blocked_by: []
supersedes: []
---

# Source-based CI omits Biopython

## What

All three supported Python lanes fail during pytest with
`ModuleNotFoundError: No module named 'Bio'`. The policy workflow is green.

## How

The CI workflow installs pinned ArgDigest, MolSysMT and MolSysViewer sources with
`--no-deps`. Its Conda test environment must therefore explicitly include the
Biopython dependency exercised by this integrated test stack.

## Why

The same error appears before and after the `policy-v1.4.6` caller update, in
hosted runs `35795373825` and `35823049829`. The pinned MolSysMT source lists
Biopython as an optional dependency, but the test environment does not install it.

## What was refuted

The policy pin did not cause this failure: the preceding CI run has the same
error, and the independent policy workflow passes.

## Scope and exclusions

This repair covers the missing CI test dependency, not the separate local
MolSysViewer addon integration failures or a change to product runtime metadata.

## Acceptance criteria

- The Conda test environment includes Biopython.
- A local guard protects the explicit dependency while source installs use
  `--no-deps`.
- The hosted Python 3.11, 3.12 and 3.13 test lanes pass.
