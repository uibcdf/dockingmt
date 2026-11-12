---
summary: Audit revision 2 against all three owner contributions and review concrete binding-site records and consumer handoffs before implementation.
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
before runtime implementation. The [second design draft](../binding_site_design.md)
incorporates the three component contributions and subsequent maintainer feedback
about MolSys-backed definitions, changing structures and ensembles. It separates
definition, structural realization and observed coverage without requiring copied
molecular coordinates in a site. The representation/definition/application planes,
portable records, explicit domain projection and bounded receiving route remain.
This is not acceptance of the proposed API or evidence of sibling adoption.

The maintainer then requests a complete comparison with each owner contribution,
correction of gaps and an update of the existing #111 delivery comment before
circulating the proposal. The [audit and worked handoffs](../binding_site_review.md)
trace every request, three synthetic JSON specimens and the still-open executed
receiving/owner decisions. The main proposal remains revision 2, audited edition.

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

Revision 2 adds public criterion/evidence operations, explicit view relations,
operation-specific correspondence/finding checks, direct region projection and
requested/resolved/actually-used accounting. It distinguishes regional membership,
chemical recognition context and retained native pharmacophoric features. Early
receiving stays bounded by the owner's actual profile, including PharmacophoreMT's
current capture limits. Heterogeneous and ensemble cases are review/acceptance
proposals, not executed observations.

Re-inspection of MolSysMT `aee7aa65` covers independent native domains,
per-structure chemical-state associations, extraction/iteration maps and existing
named-interaction coverage/invalidation. BindingMT normally receives a native
MolSys with structures. Its site declarations need not store a second trajectory;
captured native systems and site-owned geometry have separate explicit custody.
MolSysMT's existing named-analysis invalidation does not supply an external-site
observer. Dynamic pharmacophores remain prospective owner work.

The audit corrects immutable definition/evidence references (including avoiding
silent reassignment of old observations to revised claims), source versus
target-local structure/state selectors, explicit eligibility for molecular
region projections, BindingMT ownership of its TopoMT receiving profile and
observable export/execution/enforcement facts. It adds acyclic S0→H→S1 native
hypothesis association and public owner-IO sketches without a reverse dependency.

## Why

SearchDomain currently requires center, volume and box approximation. It cannot
faithfully represent a coordinate-free binding annotation. Membership alone
does not establish spatial support, and an execution adapter must not silently
turn a broad region into compulsory contacts. Other components need the same
distinctions without acquiring mandatory dependency cycles.
The same definition can be independent of coordinates or refer to particular
structures, while its observed availability/support changes across an ensemble.
A fixed snapshot-only model would confuse these meanings and encourage redundant
coordinate storage or stale reuse.

## What was refuted

- Treating BindingSite as a SearchDomain subtype or one pharmacophore feature.
- Implementing eight parallel class hierarchies from catalogue spellings.
- Reconstructing exact topographic support or binding meaning from atom lists.
- Treating renamed components, available source or an owner design issue's
  closure as implementation/consumer qualification.
- Requiring every definition to embed coordinates or describe one fixed structure.
- Treating unchanged lining coordinates as proof of a current upstream finding,
  or native interaction invalidation as an observer for independent site records.
- Requiring whole-library molecular collection machinery, all rich geometry,
  every future engine or live browser acceptance before a useful initial profile.

## Scope and exclusions

This increment delivers documentation and owner-review material only, including
three new synthetic documentation specimens and a manifest. Runtime code,
scientific/installed-test helpers and fixtures/resources, synchronized guides,
sibling worktrees, scientific evidence and installed environments remain unchanged.
No model/engine/scientific execution or manual remote CI is commissioned.
One small synthetic QuantityRecord is authored/read using the current shared
codec; it is not a new molecular calculation or receiving implementation.
Existing #28/#33/#49/#60 and central identity adoption retain their own scopes.

## Acceptance and next step

Present the audited revision 2 and request-by-request disposition for affected
owner review. The three favorable contributions are incorporated into the draft;
revised meanings and concrete cases still need owner agreement. After disposition,
agree the exercised shared meanings and register the
central agreement/adoption route. Only then implement
independently closable core/application/receiving increments and add meaningful
guards for those actual operations. #111 remains open; this draft does not
complete its implementation acceptance.

## Documentation evidence and custody

Applicable documentation gates are Ruff, formatting, generated report indexes,
shared installed-resource declaration validation and the Conda publication
contract, in the workspace and on a fresh committed export after final edits.
Task-local inspection also checks the revised document's Python-sketch syntax,
JSON-fragment/specimen syntax, specimen digests, the shared quantity handshake
and relative file/anchor targets. These checks do not execute
the proposed API, validate a released wire schema or audit every external URL.
The #111 delivery retains the exact committed-source receipt and gate outcomes.
No new BindingMT runtime, scientific or exact-head remote test pass is claimed.

The preceding revision-2 workspace run passed all six selected documentation
checks. This audited edition repeats the checks after final edits, including
the new worked examples and shared quantity payload.
Final committed-export confirmation and the exact source identity are recorded
in the #111 delivery; a documentation gate is not a receiving implementation.

The audited edition's inspection, public review snapshots and check receipts
are retained at `.molsyssuite/binding-site-audit-111-20261111/`, preserving the
preceding `.molsyssuite/binding-site-design-v2-111-20261111/` evidence, under #50 for
review on 2026-11-14. Temporary committed exports are owner-controlled and
retired after checking. Human migration files, earlier evidence and sibling
worktrees are preserved. The existing scientific full-suite resource hold is
not restarted by this documentation increment.
