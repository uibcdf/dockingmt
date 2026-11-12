---
summary: Record the detailed BindingSite work plan after favorable owner reviews, with P0 agreements and independently qualified core/projection/receiving increments.
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

# Binding-site public contract: reviewed design and implementation plan

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

The three follow-up responses support the design and bounded B/C work. The
maintainer authorized proceeding and then requested a detailed written plan
before implementation. The [work plan](../binding_site_implementation_plan.md)
records P0 decisions/requests, B1/B2 core, C1/C2 projections, T/H/P receiving,
ownership, dependencies, exit criteria and execution discipline. This checkpoint
records that plan; all runtime increments remain pending.

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

The current public sketch also exposes the proposed `assurance_scope` separately
from `context_policy`, as TopoMT requested. P0 settles the admitted mechanism and
profile checks. This is a documented API decision proposal, not a new callable.

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

This checkpoint delivers the written plan and synchronized development state.
The preceding audit retains its three synthetic documentation specimens/manifest.
Runtime code,
scientific/installed-test helpers and fixtures/resources, synchronized guides,
sibling worktrees, scientific evidence and installed environments remain unchanged.
No model/engine/scientific execution or manual remote CI is commissioned.
The preceding audit authored/read one small synthetic QuantityRecord; its
limited codec evidence remains separate from the still-pending implementation.
Existing #28/#33/#49/#60 and central identity adoption retain their own scopes.

## Acceptance and next step

Next execute P0: the finite MolSysMT/central coordination requests, explicit
assurance decision and offered T/H/P inputs. Close the local data-only contract
and advance B1/B2 while the operation-specific molecular guarantees are agreed.
Implemented projections use those agreed guarantees; each receiving case has
its own concrete acceptance. Register real guards as operations are delivered.
#111 remains open; favorable reviews and this written plan do not complete its
runtime implementation or establish component adoption.

## Documentation evidence and custody

Applicable documentation gates are Ruff, formatting, generated report indexes,
shared installed-resource declaration validation and the Conda publication
contract, in the workspace and on a fresh committed export after final edits.
Task-local inspection also checks the design/review/plan documents' Python-sketch syntax,
JSON-fragment/specimen syntax, specimen digests, the shared quantity handshake
and relative file/anchor targets. These checks do not execute
the proposed API, validate a released wire schema or audit every external URL.
The #111 delivery retains the exact committed-source receipt and gate outcomes.
No new BindingMT runtime, scientific or exact-head remote test pass is claimed.

The preceding audited revision passed its six selected documentation checks.
This plan checkpoint repeats applicable checks after final edits, including
the new plan's relative targets and unchanged worked examples/quantity payload.
Final committed-export confirmation and the exact source identity are recorded
in the #111 delivery; a documentation gate is not a receiving implementation.

The plan's public-response snapshots and check receipts are retained at
`.molsyssuite/binding-site-plan-111-20261111/`. Preserve the preceding audit/
design task evidence under #50 for
review on 2026-11-14. Temporary committed exports are owner-controlled and
retired after checking. Human migration files, earlier evidence and sibling
worktrees are preserved. The existing scientific full-suite resource hold is
not restarted by this documentation increment.
