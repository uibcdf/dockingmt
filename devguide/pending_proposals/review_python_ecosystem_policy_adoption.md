---
summary: Review DockingMT Python ecosystem policy adoption.
issue: uibcdf/dockingmt#19
status: active
opened: 2026-09-27
closed:
verification: measured
area: [governance, tooling]
guard:
normative:
blocked_by: []
supersedes: []
---

# Review Python ecosystem policy adoption

**Reported:** 2026-09-27 under `uibcdf/molsyssuite#56`; inspected
`9c5d56a4288af1e2dedd4c99f3a9bf7987592f6c` on `origin/main`.

## What

Support-library and developer-tool adoption are both **partial**. Runtime
paths use three of the four declared support libraries, while public argument
contract applicability remains to be checked. CI uses the Pytest Receptor
profile but its maintained test dependency has no exact pin.

## How

`pyproject.toml` declares ArgDigest, DepDigest, SMonitor, and PyUnitWizard.
Optional Vina/viewer handling, diagnostics, and quantities have runtime paths
and tests. `_argdigest.py` configures ArgDigest, but package source contains no
call sites. Audit representative public docking inputs and either add focused
ArgDigest-backed guards or document a bounded applicability decision.

CI run `36310576692` passed all four jobs at the inspected source, and suite
policy run `36310577050` passed. The maintained test command already selects
`--receptor=ci`. Published GH Run Receptor `1.0.0` inspected both runs.
`devtools/conda-envs/test_env.yaml` and the test extra leave
`pytest-receptor` unpinned. Pin the reviewed published version and confirm
the exact installed version in a new hosted run.

## Why

The green CI route supports test outcomes but does not establish an exact
reproducible tool version or coverage of public argument contracts.

## What was refuted

The ArgDigest configuration module is present, but no call sites were found
in package source. Its presence alone does not prove a public boundary.

## Scope and exclusions

This record owns DockingMT's adoption evidence and implementation decisions.
Suite-wide policy remains under `uibcdf/molsyssuite#56`.

## Acceptance criteria

Record applicable argument guards or a bounded exception, verify support
boundaries with focused tests, pin a published exact receptor version, and
record an exact-commit hosted run with unchanged test selection.
