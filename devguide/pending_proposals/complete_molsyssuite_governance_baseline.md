---
summary: Complete the MolSysSuite governance baseline omitted from the initial seed.
issue: uibcdf/dockingmt#1
status: active
opened: 2026-09-21
closed:
verification: reproduced
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
pass, and the two hosted workflows execute on the resulting commit. The current Conda
matrix provides Python 3.11 and 3.12 lanes; adding its 3.13 lane remains explicitly
dependent on the MolSysMT package work tracked centrally by `uibcdf/molsyssuite#31`.
