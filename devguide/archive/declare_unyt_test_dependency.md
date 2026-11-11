---
summary: Declare the alternate unit backend required by box-export tests
issue: uibcdf/bindingmt#66
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: measured
area: [testing, dependencies, units]
guard: tests/test_core_helper_contracts.py::test_backend_box_retains_explicit_unit_and_caller_policy
normative:
blocked_by: []
supersedes: []
---

# Declare unyt for the unit-policy test profile

## What

Source `e50ce1065aeb0ec19eb30f3f8050d9db3c00a347` adds Pint/unyt box-export
controls but omits unyt from the maintained test requirements. All four science
jobs in CI `42062774711`, attempt 1, fail in the unyt cases before exercising
the export. Published GH Run Receptor 1.4.0 identifies the missing backend;
native job facts confirm test-step failures. These are distinct from the earlier
Conda transport failures at 5071731.

## How

Declare unyt in the test extra and source-CI Conda environment. The shared
installed-test caller resolves its tools from `installed_tests.conda_dependencies`,
independently of the extra, so add the observed unyt 3.1.0 snapshot there too.
Keep all tests/assertions, runtime requirements, scientific pins and historical
qualification unchanged. #65 remains resolved for its source/API defect.

## Why

The routine development environment already contains unyt 3.1.0. Its passing
local checks did not establish closure of the declared hosted test environment.
This is a consumer test-profile omission; no provider change is required.

## What was refuted

Skipping the unyt cases would remove intended unit-policy coverage. Adding the
backend to runtime requirements would change product optionality unnecessarily.
The installed-test pin is a tool snapshot, not a public runtime minimum or a
new installed/platform qualification.

## Acceptance criteria and remaining observation

Keep the existing unit-policy controls passing, validate the three declared test
routes and applicable publication/resource checks, then observe the corrected
exact head's four hosted Python science lanes. Leave this issue open until that
hosted closure is verified; #28 tracks the source/run handoff. Original failed
attempts and earlier source/scientific/installed receipts remain unchanged.

Local receiving passes 90 focused unit-policy, support/bootstrap, distribution,
installed-support and reporting cases with published Pytest Receptor 1.2.2.
Shared declared-route inspection confirms unyt in all four source contexts;
the shared installed-tool resolver retains `unyt==3.1.0`. Runtime requirements
remain unchanged. The existing distribution control now checks the four selected
test backends/tools while retaining its exact core-runtime assertion. Hosted
four-minor qualification remains pending and is not inferred from these checks.

## Hosted closure — 2026-11-05

[CI 42079300841](https://github.com/uibcdf/bindingmt/actions/runs/42079300841)
at exact source `d1435ff8662787afa29798fc0824ac30d9d0c6b6` completes successfully
in all seven jobs. Published GH Run Receptor 1.4.0 and native run/job facts
confirm successful dependency closure and test steps on Python 3.11, 3.12, 3.13
and 3.14, plus quality, distribution and coverage publication. This supplies the
previously pending hosted test-profile evidence. Original e50ce10 failures and
earlier local observations remain unchanged; this source-CI closure is not a
new installed artifact or scientific qualification.
