---
summary: Review the contextual binding-site model and cross-component public contract before implementation.
issue: uibcdf/bindingmt#111
status: active
opened: 2026-11-11
closed:
verification: inspected
area: [architecture, public-api, interoperability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Binding-site public contract: design before implementation

## What

The maintainer commissions a careful design under #111 and requests presentation
before runtime implementation. The [design draft](../binding_site_design.md)
proposes an immutable contextual BindingSite, separate representation/definition/
application planes, portable records, explicit domain projection and a bounded
cross-component receiving route. This is not acceptance of the proposed API or
evidence of sibling adoption.

## How

Read the current BindingMT source and the related owners' actual contracts and
public seams. Distinguish TopoMT's accepted conceptual direction from its current
ProviderRecord/run delivery; preserve PharmacophoreMT's native feature/constraint
semantics; retain MolSysMT identity/selection/maps/transform ownership and
PeptideMT's permitted-information policy. Record source baselines and limitations
in the draft rather than claiming live integration from a source inspection.

The proposal has one primary scientific entity with named immutable views.
Search-domain projection returns existing BoxRegion with a separately validated
nested site-derivation profile. No universal site score, generic geometry engine,
snapshot manager, plugin framework or new shared package is proposed.

## Why

SearchDomain currently requires center, volume and box approximation. It cannot
faithfully represent a coordinate-free binding annotation. Membership alone
does not establish spatial support, and an execution adapter must not silently
turn a broad region into compulsory contacts. Other components need the same
distinctions without acquiring mandatory dependency cycles.

## What was refuted

- Treating BindingSite as a SearchDomain subtype or one pharmacophore feature.
- Implementing eight parallel class hierarchies from catalogue spellings.
- Reconstructing exact topographic support or binding meaning from atom lists.
- Treating renamed components, available source or an owner design issue's
  closure as implementation/consumer qualification.
- Requiring whole-library molecular collection machinery, all rich geometry,
  every future engine or live browser acceptance before a useful initial profile.

## Scope and exclusions

This increment delivers documentation and maintainer-review material only.
Runtime code, tests/helpers/fixtures/resources, synchronized guides, sibling
worktrees, scientific evidence and installed environments remain unchanged.
No model/engine/scientific execution or manual remote CI is commissioned.
Existing #28/#33/#49/#60 and central identity adoption retain their own scopes.

## Acceptance and next step

Present the design, proposed API and explicit decisions to the maintainer.
After disposition, obtain affected-owner review for the exercised shared
meanings and register the central agreement/adoption route. Only then implement
independently closable core/application/receiving increments and add meaningful
guards for those actual operations. #111 remains open; this draft does not
complete its implementation acceptance.

## Documentation evidence and custody

The workspace documentation checks pass: Ruff, formatting, generated report
indexes, shared installed-resource declaration validation and the Conda
publication contract. The two new documents' relative file targets exist;
this is not an exhaustive external-link/anchor audit. Run the same applicable
checks against a fresh committed export after final edits and retain its exact
source receipt in the owning checkpoint. No new runtime or scientific test pass
is claimed for this design.

Task-local source-inspection and check receipts are retained under #50 for
review on 2026-11-14. Temporary committed exports are owner-controlled and
retired after checking. Human migration files, earlier evidence and sibling
worktrees are preserved. The existing scientific full-suite resource hold is
not restarted by this documentation increment.
