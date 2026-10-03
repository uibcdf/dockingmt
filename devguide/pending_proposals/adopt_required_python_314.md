---
summary: Adopt the mandatory four-minor contract and qualify normal installed delivery
issue: uibcdf/dockingmt#30
status: partial
opened: 2026-10-03
closed:
verification: inspected
area: [compatibility, packaging, ci, governance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Required Python 3.14 adoption

## What

The suite maintainer requires Python 3.11–3.14 from every Python member under
uibcdf/molsyssuite#51 and immutable `policy-v1.5.3`. Inspected source `c25c53c6db94f34b2e4eff2f2dd8f077c55a651d`
still excluded 3.14. This record separates required adoption from scientific
qualification and public delivery.

## How

Metadata, contributor instructions, required full CI, applicable recipe and
installed-candidate matrices now cover `>=3.11,<3.15`. Routine development
stays on 3.13. Recovery requires successful **executed** Linux full tests on
all four minors before advancing its watermark. PR/internal-push schedules
and all existing scientific assertions/test selection are preserved.

The new 3.14 lane uses the existing controlled-source mechanism, with MolSysMT
`3eb5afd1de087f775b78d7fa45ad69cca3a02d43` and MolSysViewer `ec4c71e574d798b7c8675b7e7e983da878ce9889` (metadata inspected to admit 3.14;
the suite transition records their qualified source pair). Older minors keep
their prior source revisions. Where needed, the 3.14 environment keeps the
3.13 scientific dependency surface and uses published Pytest Receptor 1.1.0.
These source routes remain test evidence, not publicly delivered closure;
replace them after reviewed compatible public packages are independently
installed. Do not bypass Requires-Python.

## Why

Old provider revisions cap Python below 3.14, so changing only the consumer
bound would leave ordinary installation blocked. A three-minor matrix must
not clear the new required four-minor CI debt.

## What is measured and what is assumed

Source metadata, exact provider bounds, existing CI and prior recipe/resource
gates have been inspected. New solver, installation and full-test outcomes
are recorded as obtained; configuration alone proves none of them.

## Alternatives and refuted paths

Metadata overrides and tolerated/skipped scientific failures cannot establish
support. Replacing older-minor dependency generations globally would expand
the compatibility surface unnecessarily; the new route is scoped to 3.14.

## Scope and exclusions

Governance and ecosystem compatibility only. Scientific defects remain with
the owning component team and are neither suppressed nor fixed here. Source
configuration does not authorize public upload or a delivered-support badge.

## Acceptance criteria

- Coherent four-minor metadata/recipe/full-CI/installed-artifact contract.
- Ordinary installed 3.14 import and full relevant tests, or concrete owned
  blockers that preserve actual failure and bounded pending adoption.
- Historical three-minor evidence cannot clear skipped-CI debt.
- Candidate/channel and fresh public clean-install evidence precede admission.

The recovery regression is
`tests/test_ci_backlog.py::test_a_previous_three_minor_matrix_cannot_clear_314_debt`.

### First hosted results and administrative corrections — 2026-10-03

The first hosted run 37105649739 installed and imported the normal wheel
on all four Linux minors, then reproduced an overly literal Requires-Python
string comparison in the new administrative step. Setuptools can reorder
the equivalent bound. The correction compares parsed `packaging` specifier
sets, retaining the exact required range without accepting a metadata override.
Full tests were not reached in that first run; corrected execution is required.

## Integration guard correction (2026-10-03)

Integrating adoption commit `1731b5c` into the score/ranking block exposed three
stale assertions in `tests/test_governance_baseline.py`. A complete local Python
3.13 run returned 411 passed and 3 failed in 58.02 seconds: the governance workflow
guard still required `policy-v1.5.2`, the CI matrix guard still required three
minors, and the metadata guard still required `<3.14`. Those assertions now
require the already adopted `policy-v1.5.3`, four-minor matrix and `<3.15` bound.
No scientific assertion or dependency pin is changed by this correction.

This updates existing source-governance guards and remains distinct from installed
Python 3.14 qualification or public admission. The implementation and evidence for
the separate score/ranking extension are owned by #31.

After the guard correction, the complete local Python 3.13 suite passes all 414
tests in 57.32 seconds with the same twelve provider warnings. Ruff lint/format,
current report indexes and diff checks pass. Python 3.14 installed/hosted evidence
and public admission remain the separate pending acceptance above.

### Additional hosted evidence

Corrected run 37106343585 and six-cell manual matrix 37106422013
passed the normal installed-package gate. Their full tests exposed three
stale governance-baseline assertions: policy tag, matrix and Python bound.
Linux/Python 3.14 reported 366 passes and only those three administrative
failures. All three guards now assert the new required contract; no scientific
assertion or test selection changes. The ordinary built wheel declares
`<3.15,>=3.11`, reproducing the prior literal-comparison failure and passing
the corrected semantic comparison.

### Completed source qualification — 2026-10-03

Concurrent component work and its guard correction were preserved by rebase.
Source `ff64d84239dbadd030ac1ba5f82eb0a60b5517b4` passes all four Linux
full-test jobs in [37107875583](https://github.com/uibcdf/dockingmt/actions/runs/37107875583).
Documented source `0c48cf73f5b1f89dc374d1628e3a0d0f7c547ca0` passes
[full matrix 37108673271](https://github.com/uibcdf/dockingmt/actions/runs/37108673271):
four Linux minors and macOS ARM 3.13/3.14. All six cells executed ordinary
installation, isolated import/metadata validation, interpreter/architecture
and required Vina checks, followed by full tests. No metadata override is used.

Main retains strict protection with five checks, adding Linux/Python 3.14;
macOS runs remain in the full matrix. Administrator bypass is preserved.
Central state is `authorized` with public delivery/admission still pending.
This documentary skipped commit must not clear recovery debt.
