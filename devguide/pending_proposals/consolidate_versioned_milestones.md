---
summary: Consolidate meaningful intermediate source and package releases toward 1.0.0.
issue: uibcdf/dockingmt#73
status: partial
opened: 2026-11-05
closed:
verification: inspected
area: [roadmap, releases, distribution]
guard:
normative: https://github.com/uibcdf/molsyssuite/blob/main/devguide/release_version_policy.md
blocked_by: []
supersedes: []
---

# Consolidate versioned milestones

## What

The maintainer requests intermediate tags on the way to 1.0.0, even when a public
Conda package is not ready. The [proposed release ladder](../RELEASE_MILESTONES.md)
defines source, public-package, accepted-Core, scientific and stabilization
milestones with prospective numeric identities and concrete evidence.
The maintainer then requests a [Core/Extended comparison](../CORE_EXTENDED_COMPARISON.md)
before deciding the 1.0 boundary; this reminder is delivered with current
implementation/acceptance distinctions and leaves that decision open.

## How

Review remote tags/Releases, actual version parsers, publisher triggers, current
CI and official package inventories. Use existing #28/#30/#47 and scientific/
visual owners rather than inventing another release framework or molecular tool.
An exact release candidate/route remains a separate preparation from this plan.

## Why

Useful checkpoints should not remain indistinguishable development snapshots
until 1.0.0. Conversely, a numeric tag must not claim public installation, Core
acceptance or broad predictive validation that has not occurred.

## What was refuted

No remote tag or GitHub Release is observed at `37e3771`. A tag push and GitHub
Release publication have different current publisher effects. Source-only
releases still require their central notice. New public prerelease spellings
are not the suite's candidate route. Existing private qualification does not
repair the identical public MolSysMT/Viewer artifacts.

## Scope and exclusions

Roadmap, milestone/readiness guidance and a read-only availability refresh only.
No source/package release, real plan, version floor, dependency pin, workflow,
provider, environment, molecular operation or scientific producer is changed.
The Core-versus-Core-plus-Extended 1.0 boundary is explicitly pending the
maintainer preference; neither original MVP part is rewritten.

## Acceptance criteria and current handoff

The draft ladder and first-tag checklist are delivered and linked from the
operational roadmap. A dated registry receipt preserves official response and
artifact identities while leaving the prior observations intact. Final local
administrative/index/publication/resource checks and a fresh committed export
must pass; their exact-source receipts are recorded in #73/#47.

The issue stays partial until the scope decision and first concrete candidate/
version consolidation are received. Preparation of prospective `0.1.0` is next;
tagging is not performed on an incompletely qualified source or with the
required central handoff silently omitted. #30/#47 keep actual Conda delivery,
#28 exact-source CI, #33 scientific admission, and #52/#60 visible acceptance.

## Planning verification — 2026-11-05

The final documentation/availability selection passes 38 administrative tests
with the existing published Pytest Receptor 1.2.1 profile. Canonical Ruff,
report indexes, local links and the seven-Core/five-Extended row coverage pass.
Workspace publication/resource preflights pass. This is plan/receipt validation,
not execution or acceptance of the listed capabilities. Final committed-export
receipts and exact-source hosted receiving are handed off in the owning issues.

The seven-package API/three-index observation preserves response identities and
checks highest-version file sets in both directions against the API's complete
main inventories for six providers. Frozen November 3/4 inspections and failed
receiving remain unchanged. No numerical public minimum is selected. Only local
registry/CI evidence is retained for review by 2026-11-12; managed test/export
scratch is retired after the durable handoff.
