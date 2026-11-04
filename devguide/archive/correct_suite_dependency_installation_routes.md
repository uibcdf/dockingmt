---
summary: Advertise the actual MolSysMT and MolSysViewer installation routes.
issue: uibcdf/dockingmt#64
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: measured
area: [dependencies, diagnostics]
guard: tests/test_support_contracts.py::test_suite_dependency_installation_routes_match_actual_distribution
normative:
blocked_by: []
supersedes: []
---

# Actual suite dependency installation guidance

## What

At `edf72ce`, DepDigest inventory and the missing-Viewer diagnostic advertise
pip/default conda-forge commands for MolSysMT/MolSysViewer. Their actual suite
publication route is the uibcdf Conda channel; Viewer explicitly has no PyPI
distribution. The existing missing-dependency test incorrectly requires pip.

## How

Use DepDigest's existing declaration fields: disable PyPI explicitly, declare
the Conda package and channel. Check actual inventory and missing-dependency
wording while retaining Vina's valid routes and existing catalog semantics.

## Why

An availability guard should provide usable acquisition guidance. A passing
test that requires an unprovided route does not establish a correct diagnostic.

## What was refuted

No missing DepDigest API prevents correct routing. This is consumer metadata,
not a request to publish providers or implement another dependency manager.

## Scope and exclusions

No install/upgrade, runtime floor, provider pin or scientific behavior changes.
An available Conda route does not certify the current public files' compatibility
with DockingMT; that remains #30/#47. Broader ArgDigest/SMonitor adoption remains
#19; the scanner's relative-import false positive is separately DepDigest #47.

## Acceptance criteria

Both suite entries expose disabled PyPI/uibcdf Conda routes. A missing Viewer
uses its actual channel hint; Vina retains its legitimate pip advice. Relevant
support/argument/import checks pass without loading optional scientific tools.

## Resolution — 2026-11-04

Both suite entries now explicitly disable PyPI and select their actual uibcdf
Conda names/channel through DepDigest. The missing-Viewer message and inventory
use that route; Vina retains its valid pip/Conda advice. Three corrected controls
fail before implementation; the final argument/support/coordinate selection
passes 72 tests, no failures/skips/warnings, 1.20 s.

The [comparative review](../validation/support_library_review_2026-11-04.md)
records remaining ArgDigest/model and SMonitor/orchestration adoption under #19.
It preserves the distinction between a correct acquisition hint and qualified
public provider compatibility. No install, pin/floor change, molecular operation,
new science or artifact qualification occurs. Publication/hosted recovery is
recorded in #64/#28; the shared scanner correction remains DepDigest #47.
