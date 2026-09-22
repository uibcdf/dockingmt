---
summary: Complete the MolSysSuite governance baseline omitted from the initial seed.
issue: uibcdf/dockingmt#1
status: resolved
opened: 2026-09-21
closed: 2026-09-22
verification: measured
area: [governance, ci, documentation]
guard: tests/test_governance_baseline.py
normative:
blocked_by: []
supersedes: []
---

# Complete the MolSysSuite governance baseline

## What

Add the hosted CI, pinned central policy gate, canonical badges, synchronized integration
guides and issue-backed developer-guide lifecycle absent from the initial repository
seed.

## How

Adopt the current central starter-kit surfaces selectively, preserving the frozen
scientific documents and existing flat package layout. Register and synchronize every
guide implied by DockingMT's declared shared-tool dependencies.

## Why

Incubating maturity permits scientific and API evolution; it does not exempt a primary
member from the common governance and validation baseline.

## What was refuted

The central admission issue initially asserted that the policy workflow and full shared
bootstrap were already present. Inspection reproduced their absence; only the central
suite guide, Python/Ruff settings and dependency integrations existed.

## Scope and exclusions

This work does not implement docking engines, change the frozen design seed, authorize
Python 3.14 or claim scientific validation.

## Acceptance criteria

The local governance guards, package tests, Ruff checks and central conformance checker
pass, and the two hosted workflows execute on the resulting commit. The Conda matrix
covers Python 3.11--3.13. Until the channel publishes a mutually compatible ArgDigest,
MolSysMT and MolSysViewer set for 3.13, every lane installs exact source commits so the
matrix does not test different dependency generations; standardizing that fallback
remains tracked centrally by `uibcdf/molsyssuite#31`.

## Resolution

DockingMT now carries the canonical identity badges, six registered read-only guides,
the pinned MolSysSuite policy caller, the shared issue-backed reporting lifecycle and
local guards for these surfaces. The CI retains the common quality job and uses one
Conda/Mamba test topology on Python 3.11, 3.12 and 3.13. Exact compatible ArgDigest,
MolSysMT and MolSysViewer source commits bridge the current channel publication gap;
this explicit workaround is removable when `uibcdf/molsyssuite#31` provides the common
sibling-dependency mechanism.

Local evidence on Python 3.13.15: 35 tests passed and 3 Vina-dependent tests skipped;
Ruff lint/format, report indexes, the central repository checker and six guide-copy
checks passed. `mamba env create --dry-run` resolved the complete Python 3.13 environment.
Hosted policy run `35693043000` and four-job CI run `35693042602` both passed at
commit `25b6e0b`.
