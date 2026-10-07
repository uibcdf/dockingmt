---
summary: The declared py.typed resource is absent from source and installed wheels.
issue: uibcdf/dockingmt#45
status: resolved
opened: 2026-10-07
closed: 2026-10-07
severity: low
verification: measured
area: [packaging]
guard:
normative: https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_distribution_policy.md#generated-resources-in-release-artifacts
blocked_by: []
supersedes: []
---

# Missing installed typing marker

## What

`pyproject.toml` declares `dockingmt/py.typed` as package data, but producer
`365668e30f5f519adf4abc5c5e5e387d50af00a1` has no such tracked file. Its ordinary
wheel also lacks the marker. Add the already declared resource and qualify its
actual installed bytes; broader delivery remains owned by #30.

## How

A separate clean clone produced
`dockingmt-0.0.0+131.g365668e-py3-none-any.whl` with SHA-256
`7a0c0dbefb6e134f20e3e9b8a4a56442114a13f45d94fd0557cf54a7ed0eb374`.
An ordinary installation into an isolated consumer prefix verifies the consumer
and addon origins, matching archive payload and Python metadata. The declared
marker is absent. Retain this original artifact identity while testing a new
producer's corrected file.

## Why

The delivered resource inventory should agree with the package declaration.
This marker does not certify that every public callable has type annotations.

## What was refuted

Source import and successful wheel construction do not establish resource
delivery. This local environment inherits Conda dependencies and uses reviewed
sibling source archives; it does not establish clean public-channel closure.

## Scope and exclusions

Owns the declared marker only. No public package upload, complete typing claim,
dependency upgrade or provider-native build qualification.

## Acceptance criteria

- The marker is tracked and present in the exact corrected wheel.
- The installed marker bytes match that wheel outside the source checkout.
- Version, Python bounds, addon discovery and scientific execution are recorded.

## Resolution — 2026-10-07

Producer `8741fb2e104814e6f1012e0cb7073689e710f982` adds the already declared
marker. Its ordinary wheel `dockingmt-0.0.0+132.g8741fb2-py3-none-any.whl`, SHA-256
`12f2ac10e0b6c44d2b1da8e9f3e100c394596897f0c1924d23a210fe82a8e1a6`, contains it;
all 64 inspected payload members match installed bytes. Consumer/addon origins,
entry-point discovery, generated version and Python bounds are verified. The
complete installed consumer selection passes 986 tests with no skips in 366.95 s.
See the [checkpoint](../validation/installed_integration_checkpoint_2026-10-07.md)
and [receipt](../validation/data/installed_integration/checkpoint_2026-10-07.json).

This closes the marker defect only. #30 retains public/clean dependency closure,
installed Conda artifact and admission work; no package is published. The common
resource-delivery policy remains normative for future candidate inventories.
