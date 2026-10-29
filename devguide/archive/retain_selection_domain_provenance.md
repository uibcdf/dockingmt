---
summary: Retain derivation provenance for selection-based search domains
issue: uibcdf/dockingmt#55
status: resolved
opened: 2026-10-28
closed: 2026-10-28
verification: measured
area: [domains, provenance, mvp]
guard: tests/test_domain_derivation.py
normative: devguide/MVP.md
blocked_by: []
supersedes: []
---

# Selection-derived search-domain provenance

## What

The [Core acceptance audit](../validation/core_mvp_audit_2026-10-28.md) finds a
nonvisual C4 gap: the box geometry roundtrips, but its domain record omits the
source, selection, structure/frame and padding used to construct it. This is
missing derivation evidence, not a demonstrated bounds error.

## How

Define a detached explicit construction descriptor for `BoxRegion.from_selection`
and the redocking factory, retaining appropriate source identity, resolved axis,
frame/state, method, padding and units through domain/problem/result records and
backend projection. Preserve old geometry-only records and explicit boxes without
fabricated provenance. Reject malformed bindings without embedding mutable native
systems or implementing a molecular snapshot. Public MolSysMT owns molecular
access/selection; DockingMT owns its docking-domain decision and record.

## Why

C4 requires the converted domain to retain source/provenance. Correct geometry
alone does not explain which scientific selection and construction policy produced
it; caller-specific sidecars currently carry that information.

## Measured evidence

Ordinary installed `0.0.0+205.gc9c8196`, MolSysMT `e395e52646`: a public two-atom
source, selection `[1]`, frame 0 and padding 3 angstrom yield only schema/type/name/
center/lengths in `to_dict`. The geometry roundtrip succeeds. The exact
[probe record](../validation/data/core_mvp_audit_2026-10-28/domain-probe.json) and
producer are retained with the audit. `for_redocking` separately preserves partner
selection but does not store a complete domain recipe.

## What was refuted

A successful geometry roundtrip is not proof that a derivation descriptor exists.
The observed absence is not a demonstrated error in the numerical bounds.

## Scope and exclusions

Selection-derived docking-domain decisions and serialization only. Do not create
a molecular reader, selector, fingerprint or snapshot implementation downstream.

## Acceptance criteria

- Preserve the derivation through supported serialization and actual backend
  projection without changing geometry or caller unit policy.
- Cover source-derived and redocking domains, nondefault units, caller/source
  immutability, malformed records and legacy geometry-only inputs.
- Retain explicit missing provenance for old or manually geometric domains.
- Keep molecular operations in MolSysMT; report any actual missing reusable tool
  there before implementing it downstream.

Design precedes runtime changes. Browser acceptance stays #52. No new scientific
search, reranking or archive regeneration is needed for this proposal.


## Resolution — 2026-10-28

[The implemented contract](../validation/domain_derivation.md) provides an optional
validated/detached selection recipe, original redocking axes, canonical padding/
geometry binding and legacy-compatible restoration. Public MolSysMT owns all
molecular resolution. The 22-case guard covers the observed missing record and
its mutation/roundtrip/backend boundaries; the source selection passes 188 cases.
Installed/exact-head receipts remain separately recorded on #55. This resolves
the nonvisual derivation requirement, not C4/C6 visible acceptance or broader
scientific preparation, public distribution or original-source snapshot contracts.
