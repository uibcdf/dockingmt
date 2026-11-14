---
summary: Review the BindingSite work plan with operation-specific prerequisites, explicit selection/import work, structural and check/use controls, and evidenced core/application/receiving milestones.
issue: uibcdf/bindingmt#111
status: active
opened: 2026-11-11
closed:
verification: reproduced
area: [architecture, public-api, interoperability]
guard: tests/test_binding_site.py
normative:
blocked_by: []
supersedes: []
---

# Binding-site public contract: audited design and reviewed implementation plan

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
ownership, dependencies, exit criteria and execution discipline.

At the maintainer's request, a second review improves that work plan. P0a's local
contract, P0m's molecular agreement, P0s's shared coordination and each consumer's
inputs now have operation-specific dependencies. Identity/version decisions
precede construction; actual emitted-record evidence follows it. Selection and
the T0 foreign import adapter have explicit work, followed by T1 receiving.
Structural-scope, actual normalized-input and check/use controls are explicit.
M1/M2/M3 distinguish useful core, application and initial receiving delivery;
missing agreed cases cannot silently disappear at closeout. These are planning
corrections. Runtime was pending at that plan-review checkpoint; the dated
delivery entries below record the subsequently implemented profiles.

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
from `context_policy`, as TopoMT requested. The admitted mechanism and checks
are settled before C2; that decision does not block unrelated data construction.
Offline geometry and placement on an actual molecular problem retain distinct
conditions. Source inspection at BindingMT `5694f55` shows that DockingProblem
normalizes a selected source structure into a one-structure input. The plan
therefore checks the actual consumed input and source/local relationship,
including original structure 2 becoming local structure 0. Existing file/text
fingerprints are not native-MolSys mutation receipts. These observations motivate
future acceptance controls, not a claim of a delivered runtime fix.

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
- Treating every P0 decision/consumer asset as one global core prerequisite,
  or requiring API-emitted evidence before implementing the first constructor.
- Assuming import/selection adapters appear implicitly in later receiving, or
  that valid offline geometry proves placement on the actual normalized input.

## Scope and exclusions

This checkpoint delivers the reviewed written plan and synchronized development
state.
The preceding audit retains its three synthetic documentation specimens/manifest.
Runtime code,
scientific/installed-test helpers and fixtures/resources, synchronized guides,
sibling worktrees, scientific evidence and installed environments remain unchanged.
No model/engine/scientific execution or manual remote CI is commissioned.
The preceding audit authored/read one small synthetic QuantityRecord; its
limited codec evidence remains separate from the still-pending implementation.
Existing #28/#33/#49/#60 and central identity adoption retain their own scopes.

## Acceptance and next step

Next close P0a's minimal local data contract, then complete the first B1/B2
declaration/replay slice. Deliver the finite P0m MolSysMT request, register P0s
shared coordination and request the offered T/H/P inputs for their respective
operations while the core advances. Implemented projections use their agreed
guarantees; T0 implements the import adapter before T1 can qualify its workflow.
Each initial receiving case keeps its concrete acceptance. Register real guards
as operations are delivered; scope changes need an explicit maintainer disposition.
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

The preceding audited revision and initial plan passed their six selected
documentation checks. This review repeats applicable checks after final edits,
including the reviewed plan's relative targets and unchanged worked examples/
quantity payload.
Final committed-export confirmation and the exact source identity are recorded
in the #111 delivery; a documentation gate is not a receiving implementation.

The initial plan's public-response snapshots and check receipts are retained at
`.molsyssuite/binding-site-plan-111-20261111/`; this review's records are under
`.molsyssuite/binding-site-plan-review-111-20261111/`. Preserve the preceding audit/
design task evidence under #50 for
review on 2026-11-14. Temporary committed exports are owner-controlled and
retired after checking. Human migration files, earlier evidence and sibling
worktrees are preserved. The existing scientific full-suite resource hold is
not restarted by this documentation increment.


## First implemented declaration/persistence slice — 2026-11-13

[The admitted data-core contract](../binding_site_data_core.md) selects the local
P0a decisions for coordinate-free source-residue and unevaluated-definition
factories, with immutable original-evidence associations, explicit structural
references and experimental 0.1 save/read. It records actual public source
receiving: 59 new controls and 257 complete selected passes per normal/pm-fs
policy, plus six original/six sorted records read cold under unyt/pm-fs without
molecular/optional tools or new originating uses. The proposed shared `@1`, other
B1 factories, molecular/application and consumer profiles are not frozen/delivered
by that result. #111 remains active.

Next admit atom/group declarations and C1's bounded owner facts/preconditions.
Exact inputs, attempts, source/provider/native/resource and final committed-export/
public readback receipts retain #50 custody in
`.molsyssuite/site-data-core-111-20261113/`, review 2026-11-14. No original review
fixture/helper/resource producer is rewritten, prefix/native rebuild performed,
held evaluator restarted or hosted/installed/public/platform pass claimed.


## Source-index declaration increment — 2026-11-13

[The atom/group profile](../binding_site_membership.md) now receives actual public
source membership construction/inspection/revision/save/read with no molecular
query. New wire 0.2 and unchanged old 0.1 have explicit admission and actual
old-reader refusal. The new 64-control module and complete affected selection
report 321 passes per normal/pm-fs policy, with independent 20-record unyt/pm-fs
cold read and zero originating uses. Five new compatibility support inputs retain
actual original file/producer identities and exact resource declarations.

The finite C1 molecular-fact review is requested in
[MolSysMT #746](https://github.com/uibcdf/molsysmt/issues/746). No owner acceptance,
source authentication, group expansion or native projection is claimed by these
declarations. Next receive that profile and implement C1; independent B1 geometry
retains its own gate. Exact attempts/source/native/support/resource/publication
receipts retain #50 custody in `.molsyssuite/site-membership-111-20261113/`, review
2026-11-14. #111 stays active; hosted/installed/public/platform/shared/consumer
and the prior #30 evaluator hold remain separate.


## Static geometry declaration and bounded M1 increment — 2026-11-13

[The elementary geometry profile](../binding_site_geometry.md) now receives
`from_sphere` and `from_box`, explicit quantities/frame/scope, preserved box
orientation, detached inspection and immutable experimental 0.3 persistence.
Earlier 0.1/0.2 factories and original outputs remain unchanged/readable.
473 complete selected controls pass per normal/pm-fs policy, including 72 new
geometry and two saved-box OS-error controls; 16 original/sorted records cold-read
under unyt/pm-fs, and the actual previous reader refuses new 0.3 before molecular
work. [#115](../archive/length_quantity_oserror.md) preserves original OS/resource
exceptions at reused shared length and saved-box boundaries.

M1's admitted static/single-view data profiles are source-received. This is not
completion of the full catalogue, molecular application, shared agreement or
consumer adoption. C1 still awaits MolSysMT #746; next settle C2's offline
geometric derivation/assurance separately from actual problem placement. T/H/P
retain owner-input and actual receiving gates; #111 remains active.
Exact attempts, original producer/support identities, source/provider/resource
hashes and workspace/committed-export/publication receipts retain #50 custody in
`.molsyssuite/site-geometry-111-20261113/`, review 2026-11-14. The earlier evaluator
hold, installed/public/platform/hosted evidence and immutable 0.1.0 tag remain
unchanged. No prefix/native rebuild or consumer adoption is claimed.


## Internal C2 offline derivation increment — 2026-11-13

[The independent geometry recipe](../binding_site_domain_geometry.md) implements
sphere enclosure and axis-aligned box enlargement with sealed padding/output,
complete original site/evidence references, exact retained-input recomputation
and explicit unassessed placement. BoxRegion preserves the separate experimental
0.1 recipe and refuses numerical backend use; no public `to_search_domain` stub
or molecular applicability is claimed. Existing strict selection recipes remain
unchanged. 557 complete selected cases pass per normal/pm-fs policy, including
62 new controls; 18 files cold-read with original units/claims and zero molecular
operations/optional engines/originating uses. The actual older decoder refuses
new recipes; seven exact support entries preserve original 0.3 outputs/producers.

M1's admitted profiles stay received; M2 remains pending. The separate authored
ENOMEM normalization finding is owned by
[#116](../archive/molecular_input_os_resource_error.md). Next correct that
boundary, receive MolSysMT #746's C1 facts and qualify actual public C2 placement/
assurance/lifetime; T/H/P/shared/consumer gates remain active. Exact source,
resources, final workspace/committed-export/publication receipts retain #50
custody in `.molsyssuite/site-domain-geometry-111-20261113/`, review 2026-11-14.
No prefix/native build, original scientific input/producer change, new tag/package,
held-evaluator restart or hosted/installed/public/platform pass is claimed.


## Reviewed molecular offer and normalization correction — 2026-11-14

[The finite C1 offer review](../binding_site_molecular_contract_receiving.md)
receives MolSysMT #746's disposition and #750 bounds fix at exact source
27ba3d4c8d63a6a40a2d77f0190309ff15f4deef. It records source/query/group/map/
occurrence/state facts and the caller's asset/check-use preconditions. Provider
review is complete; actual client source/native qualification and public
`resolve_region` remain pending, independently of the delivered static M1/internal C2.

[The #116 correction](../archive/molecular_input_os_resource_error.md) preserves
original ENOMEM with a one-branch runtime change and 135 new controls. Original
receiving has 27 failures/263 passes; final smaller complete software selections
pass 500 cases per normal/pm-fs policy. A broader 498-case native selection was
RSS-interrupted, remains unqualified under #30 and is not automatically restarted.
Next receive the authorized updated development combination through a small
registered profile and implement the real C1 result. C2/M2, T/H/P/shared/consumer/
installed/public/platform/hosted evidence and original scientific producers retain
their scope. #111 stays active. Exact evidence retains #50 custody in
`.molsyssuite/molecular-input-enomem-116-20261114/`, review 2026-11-21.


## Finite client receiving of #746/#750 — 2026-11-14

[The exact client receipt](../binding_site_molecular_contract_receiving.md)
records the authorized clean MolSysMT source update to 27ba3d4c8 and unchanged
native file. Its two complete owner-authored modules pass 18 membership/map/
state/H5MSM and 18 selection-bounds cases, followed by 500 complete BindingMT
software controls per normal/pm-fs policy on the updated source. Package origins
and source/native/input bytes are checked; no native replacement/rebuild or
prefix install is needed for this measured profile.

The finite P0m facts are received. Next implement/qualify actual public C1
native region output with explicit map/group/occurrence/state/coverage and caller
preconditions. Public C2/M2, richer profiles, T/H/P/shared/consumer and installed/
public/platform/final-pair gates remain pending. No public C1 stub, full-suite or
native-build authenticity claim is made. The old 498-case native interruption
and earlier evaluator hold are preserved and not automatically rerun. #111 stays
active. Exact source/frozen-guard/XML/resource/gate/export/publication receipts
retain #50 custody in `.molsyssuite/site-molecular-owner-746-20261114/`, review
2026-11-21; the new small task has no resource interruption.
