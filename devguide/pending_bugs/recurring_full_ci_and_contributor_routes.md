---
summary: Recurring full CI and protected contributor routes are missing.
issue: uibcdf/dockingmt#21
status: partial
opened: 2026-09-30
closed:
severity: medium
verification: inspected
area: [ci, governance]
guard: tests/test_ci_backlog.py
normative:
blocked_by: []
supersedes: []
---

# Recurring full CI and protected contributor routes

## What

At `ac91b22`, CI executes the full Linux Python 3.11–3.13 suite on pushes
and PRs but has no scheduled or manual matrix. The [current push CI](https://github.com/uibcdf/dockingmt/actions/runs/36349574106)
passed; `main` has no branch protection and skipped pushes have no recovery.

## How

Preserve the existing CI, supported Python range and source-pinned sibling
environment. Add `full-matrix.yml` with weekly Tuesday 09:17 UTC, manual
dispatch and daily conditional 01:19 `America/Mexico_City` routes. Run the
three supported Linux minors plus a macOS arm64 Python 3.13 representative.
Assert the interpreter, macOS architecture and Vina backend before pytest.

Recognize an executed successful complete Linux matrix from either full
push CI or the periodic/manual workflow. Require all three named jobs and
their actual pytest step; reject PRs, other branches, failed runs and probes
whose heavy jobs were skipped. Keep skipped commits due across ordinary
commits and failed runs. Run the full suite when history or the API is
uncertain; filter branches locally rather than through GitHub's stale
branch-filtered listing observed under `uibcdf/molsyssuite#39`.

Require the existing stable quality and full-suite checks, plus explicit
PR integration for external contributors. Administrators `dprada` and
`LMMV`, the only current collaborators, retain direct-push bypass.

## Why

Implements `uibcdf/molsyssuite#39` without adding a full-suite requirement
before internal pushes or changing scientific assertions. The existing
source dependency route is the local variation tracked by
`uibcdf/molsyssuite#31`; changing sibling generations would conflate this
CI-routing change with a separate compatibility migration.

## What was refuted

A configured cron is not executed evidence. A green probe cannot clear
debt. A later green full push matrix can clear debt because all supported
Linux minors actually executed the suite; a routine smoke lane could not.
`noarch` metadata does not certify macOS runtime compatibility.

The first local checkout-only run had 92 passing tests, three addon
registration failures and eight skips because the shared environment did
not install DockingMT's entry point or Vina. This is not the hosted pinned
environment and does not establish a scientific regression. Local gates
use an isolated editable installation; hosted evidence uses the complete
existing Conda closure, including Vina.

## Scope and exclusions

Owns CI routing, protection and skip recovery. Scientific assertions,
sibling API upgrades, public platform claims and release-candidate evidence
remain separate reviews. The representative macOS lane alone does not
certify all Python minors or published packages.

## Acceptance criteria

- External integration requires PRs and the existing full-suite checks.
- Internal maintainers retain direct pushes, including CI-skip commits.
- An initial manual matrix executes all four cells.
- Hosted probes prove zero debt, skipped debt and debt cleared by a green matrix.
- Actual daily execution, hosted PR enforcement and publication claims are reviewed.

## Resolution

Local gates pass: Ruff check/format, generated report indexes and the central
repository conformance check. An isolated editable installation passed 99
tests with eight Vina skips in 25.39 seconds; the hosted closure includes
Vina and the new matrix checks its import explicitly. The four new detector
regressions cover persistent debt, executed full-minor coverage, rejection
of probes/PRs/other branches and fail-open recovery on API uncertainty.

At `1dd86ec`, the [initial probe](https://github.com/uibcdf/dockingmt/actions/runs/36685765426)
recognized `ac91b22` as an executed full push-CI watermark, found zero
skipped commits and omitted heavy jobs. [CI](https://github.com/uibcdf/dockingmt/actions/runs/36685744582)
passed all four quality/full-suite jobs on the new source. The
[suite policy](https://github.com/uibcdf/dockingmt/actions/runs/36685745455)
passed on the new source.

Protected `main` now requires strict Quality and all three supported-minor
Test checks. The explicit PR rule requires zero mandatory approvals;
administrators retain the direct-push route. Hosted skip and full recovery
evidence is being collected. Keep this issue open until actual daily
execution, hosted PR enforcement and publication platform claims are reviewed.
