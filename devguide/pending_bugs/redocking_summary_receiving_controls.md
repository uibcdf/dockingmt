---
summary: Existing summary controls fail on frozen producer fields and pm/fs floating equality.
issue: uibcdf/bindingmt#113
status: open
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [tests, persistence, units]
guard:
normative:
blocked_by: []
supersedes: []
---

# Redocking-summary receiving controls

## What

First #112 regression exploration reproduces two existing failures on unchanged
`630f6d6f5595723135fb934d0afdefeea5dce8b2` in fresh source exports:

- `test_retained_native_reports_show_positive_and_displaced_controls` receives
  required evaluator-metadata refusal before its expected `Incompatible` error.
  The frozen producer uses `dockingmt_version`; the reader requires `bindingmt_version`.
- `test_any_returned_recovery_can_occur_beyond_every_requested_top_n` observes
  `8.999999999999998` versus exact `9` under pm/fs.

## How and evidence

Both guards are in `tests/test_redocking_summary.py`. Baseline witnesses and
original expanded selections are retained at
`.molsyssuite/interface-data-core-112-20261112/` (`baseline-01`,
`baseline-pmfs-01`); temporary exports retire. Preserve frozen `cases.json` bytes
and original producer identity. The normal baseline records 27 passes/5 failures:
these include four missing-`unyt` cases, an independent test-environment prerequisite.
The pm/fs baseline independently reproduces the exact floating assertion. The
maintainer subsequently installed `unyt`; the original failed attempts remain
preserved and final complete core-helper controls are rerun with that backend.

## Why and what was refuted

These do not originate in BindingInterface or the unchanged finite-JSON helper
relocation. They prevent calling the broader exploratory selection green. Missing
optional test backends do not establish a PyUnitWizard defect. No docking, molecular
preparation, new native operation or scientific campaign was executed.

## Scope and acceptance

BindingMT owns an explicit historical-input receiving/translation policy and a
meaningful numerical tolerance for the analytical test. Retain independent
recovery/count/hash controls, test both intended retained-report branches, and
qualify normal/pm-fs. Do not rewrite old evidence, relax scientific cutoffs, hide
failures with skips or repair the shared prefix automatically. #30 keeps broader
qualification. #112's bounded source record profile remains separately evidenced.
Custody owner #50 reviews retained input/check receipts on 2026-11-14.
