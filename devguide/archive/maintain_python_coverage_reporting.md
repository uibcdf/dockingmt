---
summary: Measure the existing Python suite and publish truthful exact-source coverage.
issue: uibcdf/dockingmt#22
status: resolved
opened: 2026-10-01
closed: 2026-10-08
verification: measured
area: [ci, governance]
guard: devtools/tests/test_coverage_workflow.py
normative:
blocked_by: []
supersedes: []
---

# Meaningful Python coverage with separate trusted publication

## What

The initial default-branch source has tested executable Python packages but no
coverage producer or accepted public report. uibcdf/molsyssuite#69 owns the common
percentage/cadence and evidence rule; this issue owns DockingMT's implementation.
An absent public report is not evidence that coverage is inapplicable.

## How

Reuse the exact existing unfiltered `pytest --receptor=ci` suite in the ordinary
Linux/Python 3.14 lane. Only measurement options are added through
`PYTEST_ADDOPTS`: `dockingmt` plus `molsysviewer_dockingmt`, including branches,
with one XML file. The original four supported-minor lanes, independent six-cell
full matrix, scientific sibling pins, runtime floors and tests selected are retained.
The environment already declares pytest-cov; no runtime dependency is introduced.

Retain the XML after success or failure as an attempt-qualified artifact. The
separate publication job runs automatically after the test matrix on trusted
main, excludes PRs, and owns its OIDC permission. It uses the official Codecov
Action v7.1.1 at `303a32d7a59b442fa8d48b6a1cc6825c09c847a5`, explicit
retained file/current SHA/main, disabled file search and visible transport errors.
No publication credentials are supplied to the tests. The ordinary CI content
hash is explicitly refreshed in the existing reviewed route inventory; immutable
source pins and all other workflow hashes retain their original values.

## Why

Coverage should describe the executable package boundary and its actual tests.
Keeping publication separate permits useful coverage evidence from a failing
suite without converting a scientific failure into success. A configured upload,
passing administrative guard or cached SVG alone is not accepted report evidence.

## Measurements and limits

Read-only baseline `cd684cc77f28ebd97bfb8e7fcdc492736725661b` has no
configured coverage producer/uploader. Public Codecov reports no completed main
report, no rendered numeric badge and a missing branch endpoint. Four workflow
contract regressions fail before implementation: measurement absent, retained
XML absent, trusted publisher absent and exact file/source binding absent.

The local guards inspect workflow boundaries without importing scientific packages.
Their assertions retain the original unfiltered suite/minors, failure-safe artifact
custody, PR/credential isolation and exact-source/file publisher. Existing
source-context/distribution guards independently preserve sibling/dependency pins.
Local development uses the qualified `molsyssuite@uibcdf_3.14`, Python 3.14.7;
accepted workspace conflicts under uibcdf/molsyssuite#82 remain unchanged and do
not establish scientific dependency closure.

Hosted test/upload evidence and independent complete service acceptance are
required before a live README percentage or completion claim. Package coverage
excludes sibling scientific packages, compiled/native internals, browser/JavaScript
runtime and broader scientific validation campaigns. Coverage is not scientific
correctness, a support admission, a published artifact or a coverage threshold.

## What was refuted

Adding another mandatory suite on every internal push or changing sibling source
pins is unnecessary: current test execution is already suitable for measurement.
A static percentage, unknown badge or inferred service acceptance would violate
the evidence rule. Selecting only administrative code would not represent the
chosen executable package boundary. TopoMT's independently approved maturity
deferral under uibcdf/topomt#81 is not automatically applied to DockingMT.

## Scope and exclusions

This work changes CI measurement/report custody/publication and its reviewed hash,
contract guards and documentation. It does not fix scientific bugs, change
package/runtime APIs, dependencies, release plans, build/promotion routes or
internal skip/recovery rules. Primary sibling clones remain preserved.

## Acceptance criteria

- Execute the unchanged existing suite with selected coverage and retain its XML.
- Verify the native exact-source upload, attempt and required executed steps.
- Independently confirm complete main report for that source and numeric SVG.
- Deliver the live repository-specific badge with scope/cadence/last-report limits.
- Archive this record and close the owner issue only after those distinct facts.

## Resource lifecycle

Owned isolated clone and immutable SDK are temporary qualification resources.
Remove them and generated caches after the accepted evidence or bounded pending
handoff; preserve the primary clone and caller-owned shared environment.


## Resolution — 2026-10-08

Producer `9db7074828083da03094eae091e84bb4ae6caa61` completes native ordinary
CI [37799841269](https://github.com/uibcdf/dockingmt/actions/runs/37799841269)
with all seven jobs, including the unchanged four supported-minor suites,
measurement/retention and automatic independent publisher. Native policy
37799842358 passes its actual required conformance/lint/format steps.
Independent acquisition verifies repository, source, workflow, push event,
current attempt, complete job inventory, every selected executed step and the
original artifact ZIP digest/XML SHA-256. The complete public main report is
**87.93%** and its live SVG **88%**. Coverage.py XML separately records 3,310/3,574
covered lines (92.61%) and 1,084/1,284 covered branches (84.42%); these counts and
Codecov's filtered/partial-line percentage are distinct, not interchangeable.

The guard `devtools/tests/test_coverage_workflow.py` failed four cases before the
producer existed and passes after its addition; it protects the actual repaired
measurement/custody/credential/source mechanisms. The related twenty existing
controls also pass and protect unchanged dependency/source selection. Immutable
native/service receipt: `devguide/artifacts/python_coverage_20261008.json`.
The live badge and scope/cadence/last-report limits are delivered in the README;
no numeric percentage is hardcoded. No scientific correctness, new support
admission, release/public package or cleared unrelated scientific debt is claimed.
Final guide-only administrative gates are recorded in the owning issue.
