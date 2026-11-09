---
summary: Expose existing diagnostic identities through a public exception namespace.
issue: uibcdf/dockingmt#94
status: resolved
opened: 2026-11-08
closed: 2026-11-09
verification: reproduced
area: [api, diagnostics, usability]
guard: tests/test_public_exceptions.py
normative:
blocked_by: []
supersedes: []
---

# Public exception namespace

## What

Public callers currently need `dockingmt._private.smonitor` to catch local
ArgumentError. That class belongs to the catalog hierarchy, not native ValueError.
The API-reference review at `457eb090f0e36b6d2b34e1b7d90cbab4d43a4c00`
identifies a concrete supported-import gap; #28's initial documentation-only
scope is amended to deliver an additive namespace, not another error framework.

## How

Expose `dockingmt.exceptions` at the root with explicit aliases to the existing
13 local classes. Keep exact identities, implementation module paths, native
families, catalog codes/context/causes and provider/resource/control propagation.
Add complete resource coverage and a source-linked public API map. Use public
imports to catch actual record/protocol/viewer failures without molecular work.

## Why

A supported API should let callers handle its own diagnosed failures without
private implementation imports or an inaccurate generic native catch family.

## What was refuted

No provider defect, new exception class, implementation move, wrapping policy,
scientific operation or dependency is needed. ArgDigest/provider errors retain
separate ownership. The previously qualified private wheel is unchanged and
cannot certify this later namespace.

## Scope and acceptance

Pass the public consumer controls and existing bootstrap/support/model/diagnostic
selection under normal and pm/fs policies. Preserve original missing-namespace
failures and all old assertions, qualified identity/causes and resource behavior.
Document all actual root exports and supported model methods, ownership and work
boundaries; verify against source declarations. Run final local shared resources/
publication checks and fresh committed export before [skip ci] publication.
Keep #19/#28/#73 partial and #256/#558/canvas/public holds. Custody #50, review2026-11-14.

## Delivered and qualified — 2026-11-09

[Exact source/reference receiving](../validation/public_api_namespace_2026-11-09.md)
passes 251 complete affected cases normal then pm/fs and the exact offline
snippets/13 alias identities under both policies. The 12-case public guard
catches actual library failures, preserving codes/fields/native hierarchy/causes
and exact resource/process-control objects. Original missing-namespace failures
and fourteen harness-only probe failures remain. Independent primary157/reader9
receiving verifies native/Receptor/source/AST/descriptor agreement without replay.
The source map covers all 33 root exports/13 model classes and 42 local links.
Runtime descriptor adds exceptions.py (67 paths), with 594 support inputs unchanged.
Final local/fresh-export checks and [skip ci] publication preserve missing remote
and installed/public qualification. No provider defect or new scientific work.

## Subsequent private installed receiving — 2026-11-09

[Separate installed qualification](../validation/record_wheel_editable_2026-11-09.md)
now receives the later behavior from one genuine wheel at producer `841a34d`,
with 1,062 complete offline cases normal then pm/fs and the original explicit
native-test exclusion. Exact payload/source/metadata/import/support checks and
independent primary 130/reader 9 receiving pass. This later receipt does not change
or relabel the original source failures, old wheel, producer or evidence above.
No public/full scientific/platform/canvas/hosted acceptance is inferred.
