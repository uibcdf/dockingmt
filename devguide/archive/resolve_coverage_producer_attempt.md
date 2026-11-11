---
summary: Resolve coverage from its actual retention step after partial reruns.
issue: uibcdf/bindingmt#68
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: measured
area: [ci, reporting]
guard: devtools/tests/test_coverage_workflow.py
normative:
blocked_by: []
supersedes: []
---

# Coverage retention across partial CI reruns

## What

Run 42059033330 at `5071731168bab30cab514fcf32142b76d732cae4` retains
Python 3.14 coverage in attempt 1. Attempt 2 reruns the failed Python 3.11/3.12
lanes successfully, but its publisher requests an attempt-2 coverage artifact.
Only `bindingmt-python-coverage-42059033330-1` exists. The overall retry fails;
the effective successful science lanes are a separate fact.

## How

Keep the existing measurement and attempt-qualified upload. Add a bounded
selection step to this workflow's trusted publisher, using official GitHub
pagination and immutable artifact-ID downloading. Require a unique effective
Python 3.14 job, completed tests, successful coverage retention and one unexpired
same-run/same-source artifact created within that retention step. Retain the
producer attempt parsed from its exact artifact name and the publisher attempt
as different identities. Reject missing, malformed or ambiguous evidence.

Read-only observation on 2026-11-05 shows that the attempt-2 API representation
changes the reused job's ID and `run_attempt`, while retaining its original
test/retention times. Neither the current attempt nor that represented job field
alone establishes the measurement attempt. The observed artifact creation time,
16:02:44 UTC, is inside the successful retention step, 16:02:33–16:02:44 UTC;
attempt 2 starts at 16:05:59 UTC. The artifact's original run and source match.

## Why

Partial reruns must reuse the retained measurement when its producer is reused.
A newly executed producer with missing/failed retention must not fall back to
an older measurement. Failed tests can still produce useful coverage without
turning their failure into a successful suite.

## Ownership and scope

This is specific identity selection in the existing BindingMT workflow, using
official GitHub actions/API operations. The shared starter's coverage pattern
and tool catalogue do not supply this partial-rerun binding. Any reusable
cross-component custody tool remains MolSysSuite-owned; work and issue updates
in other components remain deferred at the maintainer's request. Replace this
local binding when a qualified shared workflow covers these controls; reassess
under this issue if its producer/job/retention contract changes.

No molecular operation, scientific campaign, runtime/package dependency,
source-provider pin, credential distribution to tests or new publication route
is introduced. Keep existing trusted-main/PR guards, failed-test XML retention,
exact Codecov commit/file and visible publication errors.

## Acceptance criteria

Exercise the actual workflow selection body against the sanitized historical
partial-rerun metadata, complete reruns and adverse missing/expired/ambiguous/
wrong-run/wrong-source/new-producer cases. Keep existing measurement/security
guards. Verify local administrative, publication/resource and committed-export
checks. Publish source and distinguish that correction/controlled API receiving
from later exact-head hosted observation under #28. Do not rerun the superseded
scientific matrix merely to repair its historical conclusion.

## Resolution and receiving — 2026-11-05

The publisher now uses the official pinned GitHub Script v8 action to paginate
this run's effective jobs and artifacts. The unique artifact must match the
Python 3.14 retention interval (inclusive UTC bounds), the original run/source,
an unexpired immutable ID and a canonical producer attempt no later than the
publisher attempt. Missing timing or other uncertainty fails explicitly. The
official download action receives that single ID and explicit current run,
rather than constructing a name from the publisher attempt. Only the publisher
gains `actions: read`; tests retain their existing permissions and suite.

The administrative job explicitly selects Node 26 to execute the actual inline
selection body in its Python controls. Nine top-level coverage controls pass,
including 21 adverse evidence mutations, alongside 24 existing reporting,
distribution and support controls: 33 tests with published Pytest Receptor 1.2.2
on routine Python 3.14 / Node 26.3.1. Ruff, generated indexes and shared
publication/resource preflights pass. The ordinary workflow's reviewed route
hash is refreshed; all sibling pins, scientific assertions and runtime payload
declarations remain unchanged.

Read-only receiving executes the exact selection body against fresh historical
API responses and correctly selects artifact `13431816891`, producer attempt 1,
for publisher attempt 2. Independent ID-based acquisition verifies a ZIP
containing only `coverage.xml` (189,622 bytes). Its XML SHA-256 is
`b77d0a50b6bfe6e5c54e469cf1fad34f38b63ec61b4a50167f53da7768f36c92`.
The [sanitized receipt](../artifacts/coverage_binding_20261105.json) distinguishes
the original source and failed run from the new selection-body fingerprint.
No old workflow is rerun, and no coverage is uploaded during this receiving.

This resolves the source/workflow defect with controlled API/artifact receiving.
The historical attempt remains failed. #28 retains exact-head hosted
binding/download/Codecov execution; local Node 26 execution is not a claim that
the GitHub Script action's Node 24 runtime has executed here. Existing #22
public-report evidence retains its original producer. Other components' issues,
new scientific work, package qualification and visible C4/C6 remain separate.

Hosted receiving: exact `ae2a9a924bf860e8c2f4315f2beaabb6eb6c23a7`
[CI 42094443810, attempt 1](https://github.com/uibcdf/bindingmt/actions/runs/42094443810/attempts/1)
passes 7/7, including actual binding, download and Codecov upload. This adds
normal-attempt hosted integration to the historical partial-rerun controlled
receiving; it does not turn the original failed attempt into success.

## Primary contracts

- [Official workflow-job API](https://docs.github.com/en/rest/actions/workflow-jobs#list-jobs-for-a-workflow-run): effective-job selection and pagination.
- [Official artifact API](https://docs.github.com/en/rest/actions/artifacts#list-workflow-run-artifacts): run/source metadata, creation time and expiry.
- [Official GitHub Script v8](https://github.com/actions/github-script/tree/ed597411d8f924073f98dfc5c65a23a2325f34cd): authenticated client and inline action body.
- [Official download-artifact v4](https://github.com/actions/download-artifact/tree/v4): immutable ID selection and explicit run.
