# Binding-interface characterization: first design for review

Revision **1**, 2026-11-12. Owner: [BindingMT #112](https://github.com/uibcdf/bindingmt/issues/112).
Status: **review draft; no runtime implementation or frozen schema**.
The maintainer requested a reviewed first design and a public response, then
specified the same repository-document/public-post route used for BindingSite.
This document is that detailed design; the issue carries its review and disposition.
The [owning record](pending_proposals/binding_interface_public_contract.md)
tracks scope, evidence and the next action.

The design incorporates the [TopoMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6812846154),
[PeptideMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6813153779)
and [PharmacophoreMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6814109974)
contributions. Their agreement on a direction does not freeze this proposal,
select a Python class or demonstrate compatibility. MolSysMT has no contribution
in the three-comment review baseline inspected for this edition.

Names, fields, examples and signatures below are proposals. Symbolic records
are authored review material, not API-emitted artifacts or scientific results.
The [BindingSite design](binding_site_design.md) and its
[reviewed work plan](binding_site_implementation_plan.md) retain their own scope.

## 1. Scientific purpose and useful first outcome

Propose one binding-domain characterization result, working name
`BindingInterface`, that relates a binding question to specified molecular
participants and available owner observations. Its value is contextual coherence,
explicit applicability, interpretation and faithful inspection. It need not add
a numerical kernel.

A researcher should recover the question, participants/grouping, molecular
contexts, actual observations, effective application inputs and limitations
through the public result, without reconstructing them from unrelated artifacts.
The result can reference evidence retained elsewhere and explain unavailable
recovery; it does not promise that every referenced asset is locally present.

The minimum useful workflow is:

`explicit question/context + supplied owner observations → characterization → inspection → save/read → one qualified footprint or comparison`

Composition does not run missing detectors. Optional later calculations require
an explicit operation/profile and keep their numerical owners. A declaration
with no observations retains unknown support, rather than an evaluated-empty
interface. An inferred association retains the criterion and evidence supplied
by its owner.

The working result name does not prescribe a class hierarchy. A small value
returned by a public operation may suffice. The concrete representation follows
from owner review and an exercised receiving profile.

## 2. Scientific distinctions

| Concept | Meaning | What it does not establish |
| --- | --- | --- |
| BindingSite | A contextual region hypothesis/annotation, possibly independent of partner or coordinates. | A complete interface, mandatory contacts or binding competence in every structure. |
| Association | Specified participants related under a declared or inferred criterion. | Localized geometry, an experimentally supported interaction or biological function merely from registered endpoints. |
| Spatial realization | Supported patches, contact boundaries, intervening regions or other owner-defined localization. | A cavity, recoverable volume or a complete functional site. |
| Observation | An attributed result with its criterion, source/context, coverage and provenance. | An equivalent observation under another criterion or independent evidence when copied. |
| Binding characterization | BindingMT's question, evidence relationships, applicability and interpretation. | A competing topographic registry, universal quality score or new calculation by wrapping owner results. |
| Application | How a particular operation consumes selected information. | An intrinsic active restraint or permission attached permanently to the evidence. |

An interface-related descriptor can coexist with a feature's primary
classification: an interfacial pocket can remain a pocket. A tight interface
need not contain a cavity, a mouth or two distinct dry geometric banks. Molecular
participants and geometric banks are separate populations.

Geometric/crystal-packing evidence does not automatically establish biological
binding. Supporting, challenging and conflicting evidence retain their original
claim and context. A negative observation for one partner/state/criterion does
not exclude another possible association or erase a general site annotation.

Contact membership, buried-area membership and topographic support retain their
definitions. Contact counts, model confidence, pharmacophoric fit and energetic
endpoints have distinct meanings. Binding free energy belongs to a defined
process, states, conditions and method, not intrinsically to a geometric patch.

## 3. Ownership and dependency direction

| Concern | Authority |
| --- | --- |
| Binding question, characterization, interpretation and links to sites/applications | BindingMT |
| Topographic associations/realizations, support, classification and evaluations | TopoMT |
| Molecular representation, chemistry, selections, correspondence, contacts and surface observables | MolSysMT |
| Pharmacophoric construction, hypotheses and matching | PharmacophoreMT |
| Permitted information, comparison, aggregation and scientific selection policy | Consuming researcher/component |
| Shared meanings, compatibility and coordinated adoption | MolSysSuite |

BindingMT references exact owner results rather than maintaining an independently
editable copy of their relations or geometry. TopoMT and MolSysMT need no
mandatory BindingMT import. Optional adapters compose public owner objects or
records and keep dependency checks on the selected route.

A BindingMT question can precede any topographic analysis. Its declared relation
does not register or promote a TopoMT association. Linking later owner evidence
creates an explicit association with that evidence, preserving authority and
identity. Shared interpretation is agreed before freezing that boundary.

No shared package, molecular snapshot engine, generic graph service or universal
execution/provenance framework is proposed.

## 4. Minimal information model

These are record roles, not required public classes:

| Group | Information and invariant |
| --- | --- |
| Identity/question | Declaration identity, optional label, binding question, declared/inferred status, process and relevant states/conditions. Observation origin is retained separately. |
| Participants/grouping | Molecular source occurrences, granularity, selections, available membership, contextual roles and the sides chosen for this question. |
| Contexts | Source/assembly/symmetry occurrence, source and local structure/state/frame, correspondence maps, actual check scope and trust assumptions. |
| Owner references | Exact association, realization, analysis, observation and native-artifact references; each retains its own context. |
| Evidence/interpretation | Original claim associations, supporting/challenging evidence, attributed interpretations, supplied uncertainty and limitations. |
| Site relationships | Source-qualified links to site hypotheses and criterion-dependent participant footprints; many-to-many relationships are allowed. |
| Applicability/coverage | Requested/evaluated/resolved scope, availability, omissions, failed or missing prerequisites and operation-specific assessment. |
| Derivation/provenance | Exact parents, effective operations/parameters, producer versions, definitions, quantities, original attribution and explicit losses. |

A field is required only by an admitted profile that can give it a meaningful
value. Missing information has an explicit state/cause. Required contradictions,
malformed known payloads or unsupported required semantics refuse the affected
typed admission/application; they are not successful missing values.

The characterization may legitimately relate observations from different
contexts. Reference-receptor topography, evaluation against a partner pose and
topography of the assembled complex remain separately scoped even when aligned.
A single top-level default context must not silently retarget them.

## 5. Participants, grouping and multimolecular questions

Participant profiles can include small molecules, peptides, proteins, nucleic
acids and explicitly admitted combinations. This catalogue does not establish
provider support for every combination. Molecular type, contextual role and
granularity remain separate; there is no universal peptide/protein length rule.

A participant can address a molecule, chain, domain or owner-supported selection.
Retain the declared granularity, original addresses and resolved element axis.
Selections and their maps remain MolSysMT-owned. Participant labels are local
labels, not chemical identity or persistent assembly-occurrence identifiers.

| Example | Interpretation |
| --- | --- |
| Binary A–B | Two molecular participants, independently of geometric bank count or available cavity geometry. |
| A–B and B–C in one complex | Two association occurrences; shared complex membership does not create a localized joint interface. |
| Composite `(A+B) \| C` | Three molecular participants and two chosen sides. The internal A–B interface has a distinct context. |
| Localized A–B–C realization | Joint support/criterion/evidence must be declared; pairwise projections remain projections. |
| Unlocalized association | Participant relationship/question can be retained without fabricated support. |

Membership overlap and grouping do not imply disjoint partitions. Each observable
retains its contribution/counting policy. Donor–hydrogen–acceptor roles do not
establish three molecular participants. A site spanning receptor subunits is
not automatically their internal interface or their association with a ligand.

Grouping is not geometric union. A joint structural realization does not prove
energetic cooperativity. `AB + C ↔ ABC` and assembly formation from independent
participants are different questions and retain their own thermodynamic context.

## 6. Molecular, structural and coordinate contexts

Ordinary localized work receives a native `molsysmt.MolSys` and selects a
structure explicitly when the input has several. MolSysMT owns its coordinates,
per-structure chemical-state associations and general molecular operations.
BindingMT does not store a second trajectory.

Retain, where applicable:

- Source occurrence, assembly/symmetry occurrence and available artifact identity.
- Selection syntax/element, original addresses, resolved membership and atom/group
  source-to-local maps, including removed/generated entries and causes.
- Original structure positions, delivery/occurrence maps and effective local
  structure/state selectors with their source associations.
- Frame/image convention, units and explicit owner transform when used.
- Actual checked facts, their coverage/authority and remaining caller preconditions.

A state selector such as `structure` is a policy, not a chemical identity.
State-dependent membership cannot be reinterpreted by simply overriding that
selector. An original structure 2 may be local structure 0 after extraction;
numeric equality of indices is not the required correspondence.

Source labels, matching counts and a live handle do not authenticate molecular
origin. An artifact digest identifies bytes and is not a universal molecular
equivalence check. Use existing qualified MolSysMT facts and operations; retain
missing proof rather than build a new authentication/snapshot algorithm.

Unlocalized declarations can retain unresolved source references without a
common coordinate frame. Their preservation needs no molecular lookup. A spatial
comparison or projection needs the frame/relationship required by its profile.
The first localized profile may restrict itself to one declared Cartesian
structure/image. PBC, assembly generation and alignment require explicit owner
operations and qualification, not implicit coordinate concatenation.

Native-system custody is explicit. Reproducible captures use qualified MolSysMT
persistence with original-to-captured maps. Provider/site-owned geometry retains
its own owner-defined payload or recovery reference. A selected excerpt does not
prove recovery of a complete prepared source or producer input.

## 7. Identity and immutable revision

Distinguish these identities:

| Identity | Scope |
| --- | --- |
| Binding declaration | This question/interpretation and its revision; a name is only a label. |
| Owner association | The canonical association in the owner result, if supplied. |
| Realization | One scoped localization/observation context and its owner support. |
| Analysis/observation occurrence | An observation in its originating analysis; local index 0 is not global. |
| Saved characterization | Exact admitted content, separate from scientific equivalence and biological identity. |

Use exact record references plus scoped keys. Faithful copy/read preserves
identity. New observations, changed grouping, remapping or a revised interpretation
create a new immutable record with explicit parents and reasons.

Old observations retain their original claim/context associations. Reusing one
for a revised claim is a new attributed interpretation, not a new measurement.
Do not retarget a relative claim reference to the latest definition silently.
Original source, producer and bibliography survive every composition.

The parent graph is bounded and acyclic; general scientific relations need not
be acyclic. Retain exact parent references rather than recursively embedding
every ancestor or copying native assets. Equal membership/centers or repeated
delivery do not establish equivalent or independent evidence.

## 8. Realizations, ensembles and changing inputs

An association can have no localization, several coexisting patches or attributed
realizations across structures/states. Preserve those relationships. Alternative
poses/states are not automatically simultaneous constraints or consensus.

Record requested, evaluated, evaluated-empty, unknown and failed scope separately.
Appending structures does not expand old coverage. A delivery such as `[2, 0, 2]`
retains occurrence maps without creating extra independent evidence. Weights or
times have meaning only when explicitly supplied with their owner policy.

No default union, average geometry, consensus, prevalence, thermodynamic population
or kinetic interpretation is implied. Aggregation requires its own correspondence,
frame/weight/coverage policy and qualification. Dynamic methods retain their owners.

| Change | Required disposition |
| --- | --- |
| Coordinates or frame | Historical result remains readable; reassess dependent geometric/application facts or use a qualified captured input. |
| Chemistry/completion/refinement | New derived context, explicit maps/losses and reassessment of affected observables; generated members inherit no old evidence. |
| Participant grouping or criterion | New interpretation/evaluation context; unchanged owner geometry can be referenced under its original scope. |
| Partner pose | New pose-dependent observations; receptor-only reference geometry remains its own result. |
| Added unrelated view/observation | New record; earlier evidence retains its original associations. |
| Display name | No implied change to scientific support or chemical identity. |

Unchanged footprint coordinates do not verify the complete producer input/query.
Each reuse/application checks the facts required by its requested guarantee
against the actual selected/exported input and source/local maps at the point of
use. Record performed checks separately from unchanged-input caller preconditions.
No generic external mutation observer or atomic behavior under concurrent edits
is promised. Missing required proof, contradiction and unsupported guarantee
remain different outcomes; a stronger request is not weakened silently.

## 9. Sites and criterion-dependent footprints

Use composition and explicit many-to-many references:

- A BindingSite can relate to several interface occurrences/partners/poses.
- An interface can cite several site hypotheses or participant footprints.
- A footprint derives from an identified observation and retains its participants,
  criterion, structure/state/frame, coverage and provenance.
- A footprint can motivate a site declaration without delimiting its complete
  functional region or asserting membership beyond the observed criterion.

Interface is not a BindingSite subtype, the union of two sites or a container
that expands BindingSite into the whole complex. Preserve the
[existing declaration/representation/application distinction](binding_site_design.md#1-design-decision-proposed).

Footprint projection requires an admitted membership/support operation. A source
annotation, contact footprint, buried-area population and topographic support
cannot become interchangeable because they use similar containers. Missing map
or geometry leaves the relevant operation unavailable, not computed empty.

## 10. Observation states, applicability and comparisons

There is no universal `valid=True` field meaning that every interpretation is
supported. Assessment belongs to an operation, its requested guarantee and the
dependencies of each observation it uses.

Preserve value states such as computed nonzero/zero, unevaluated, unsupported,
undefined and failed, with owner causes. Availability, coverage, check outcome
and biological support are separate dimensions. Evaluated-empty is not a usable
positive pharmacophore query merely because it is a successful calculation.

Required malformed/contradictory data refuse the operation; a failed required
conversion cannot yield an apparently complete partial result. Explicit partial
profiles retain every omission and changed meaning. A missing chemistry-dependent
observable need not invalidate unrelated geometric observations.

Complete coverage is the ordinary default for a requested projection. Partial
use requires an explicit admitted policy and reported omissions; retaining an
incomplete declaration is not successful application of its missing information.

Each comparison retains the observable/definition, participant identities/grouping
and intentional differences, states, criterion, source/frame relationships,
effective coverage and normalization when used. Prerequisites are observable-
specific. Comparing poses of one molecular pair and comparing different candidate
partners require different policies; identical participants are not universally
required for a justified comparison.

Different criteria can remain legitimate parallel observations without becoming
directly comparable. No default summing, averaging, ranking or universal interface
quality is introduced. Consumer aggregation and selection remain explicit.

## 11. Effective information and pharmacophoric applications

Information role belongs to a particular use. Preserve supplied priors,
candidate-derived observations and evaluation-only references at the consuming
request/result boundary. The same observation may be an explicit prior in a later
application; it cannot retrospectively become an input to an earlier prediction.

Applications retain exact requested/resolved/exported or submitted populations,
selected structures, parameters, permitted origins, omissions and observed
execution/enforcement where available. Exported data do not by themselves prove
scientific influence inside a provider. Keep those evidence boundaries distinct.

A separately constructed absent-site request must not inherit localization from
an evaluation reference, previous request or viewer. Retained provenance is not
permission to consume it. The characterization is not an access-control or
general leakage-certification framework. These rules compose with the
[BindingSite application seam](binding_site_design.md#81-effective-inputs-and-information-roles).

A pharmacophoric projection identifies whether it describes A, B or a complementary
hypothesis. One interface does not determine one unique pharmacophore. Preserve:

`association/realization → owner analysis/observation → molecular feature → hypothesis site`

This is many-to-many: several observations may support one feature; some yield
no site; the same evidence may support different explicitly constructed hypotheses.
Retain local indices qualified by the original analysis, chemical roles, source/
state/frame, construction decisions and omissions. Regional membership, chemical
recognition context and retained features stay separate, with owner profile limits.

Repeated observations do not automatically add constraints, weights or energetic
importance. Equal atom membership or coincident centers do not equate observations
or features. Conflicting geometry, essential status or weights need an explicit
owner-supported choice. Directions, tolerances, exclusions and assignment semantics
remain native. Joint composition, alternatives and consensus require distinct
policies; mutually exclusive poses cannot silently become simultaneous constraints.

A positive fit alone does not establish a match when essential-site or exclusion
criteria fail. Deriving a query from a candidate and evaluating that same candidate
is a consistency control, not independent prediction validation.

## 12. Proposed public surface and ordinary workflow

The first localized operation composes already supplied observations on a chosen
native molecular context. It resolves admitted selections through MolSysMT,
records actual checks and refuses unsupported required guarantees. It does not
run missing detectors or infer a biological association.

Illustrative syntax, not an implemented callable:

```python
characterization = bmt.characterize_interface(
    molecular_system=system,
    structure_index=chosen_structure,
    chemical_state="structure",
    question=association_question,
    participants={
        "A": selection_a,
        "B": selection_b,
        "C": selection_c,
    },
    grouping=(("A", "B"), ("C",)),
    observations=owner_records,
    site_refs=site_references,
)
```

`question` holds the declared scientific question/process; its concrete minimal
fields need review. Participant labels are local. Selections, effective state
and context facts use admitted owner operations; the signature does not establish
that a universal descriptor/check API already exists.

The final signature must expose the requested guarantee and admitted context/
trust policy, reusing BindingSite's scoped-check meanings where applicable.
Data-only preservation, current molecular correspondence and applicability of
an original producer finding have different requirements. Their exact public
mechanism is a profile decision before implementation, not a hidden import mode.

| Public capability | Proposed behavior and first-profile limit |
| --- | --- |
| Declare/import | Construct a data-only question or compose admitted owner records; keep unresolved context and declared/inferred status explicit. Factory spellings remain open. |
| Inspect | Expose question, observations, coverage, prerequisites and exact owner references; no implicit geometry calculation or asset fetch. |
| Copy/revise | Detached ownership, faithful copy and explicit immutable derivation; preserve original observation/claim associations. |
| Save/read | Safe, versioned portable record with exact context/references and owner attribution; no original scientific engine required. |
| Project footprint | Separate admitted operation naming participant and original observation/criterion; preserve maps, omissions and meaning. |
| Compare | Explicit observable/policy/context requirements; initial comparison only if the chosen receiving input supports it. |
| Pharmacophoric projection | Explicit optional owner operation/profile retaining native construction semantics; not implied by import. |

Data-only declarations remain readable without resolving molecular data. The
localized signature is not a mandate to require live MolSys for every record.
Add only implemented public callables at runtime; avoid empty classes, duplicate
aliases or automatic discovery of every catalogue/provider.

## 13. Portable record and reference lifecycle

Proposed semantic outline, not a released schema or assigned format identifier:

```text
BindingInterface characterization
  format/version         explicit experimental/admission policy, still to agree
  identity/question      declaration, optional label, claim/process and conditions
  contexts[]             scoped molecular/structure/state/frame facts and checks
  participants[]         source occurrences, selections, axes and available maps
  grouping               participants grouped for this question, not geometric union
  association_refs[]     exact owner associations, or explicit declared-only status
  realization_refs[]     localizations with context and coexistence/alternative roles
  observations[]         exact owner results/occurrences, definitions and provenance
  evidence_links[]       original claim scope and attributed supporting/challenging use
  site_links[]           exact site/view/definition refs and footprint derivations
  applicability[]        operation/guarantee, dependencies, coverage and causes
  application_refs[]     optional exact consuming request/result receipts, not active settings
  derivation             exact parents, changes and losses
  extensions             preserved optional namespaced owner information
```

Known physical quantities use shared PyUnitWizard codecs and explicit reader
field/unit/dimension handshakes. Preserve owner-native artifacts and their original
conventions; do not infer units or interpret unknown raw fields by their names.
Equivalent physical values need not share a content hash after unit re-encoding.

Core discriminants/known fields are validated. Optional opaque owner data can
survive faithfully; unsupported required semantics refuse typed admission or
the affected operation. Compatibility, migration and experimental status must
be agreed before emitting an admitted format; no silent reinterpretation.

Save writes use exclusive creation by default and preserve existing valid files
on failure. Reading is detached and performs no automatic lookup, dynamic import
from record contents or asset fetch. Replaying sufficient saved data requires no
original engines/models/GPU/network and earns no new originating-engine credit.
BindingMT's declared core installation remains required.

Foreign-artifact decoding uses its admitted owner reader. An unavailable reader
or artifact leaves a readable reference-only record, not a recovered native
result. External references retain owner/format/content identity and scoped keys;
a URI alone does not prove source identity or availability. Native molecular and
provider saves remain explicit, not implied by saving the characterization.

## 14. Symbolic examples for review

These examples specify meaning and expected behavior. `Q0`, `C0`, `O0`, `S0`
and similar names are local explanatory labels, not new global identifiers,
real artifacts, hashes or an implemented interchange vocabulary.

### 14.1 Binary association and incomplete localization

```text
Q0: question about A associating with B; one declared grouping A | B
C0: identified assembly occurrence, chosen source structure/state/frame
O0: owner observation for A/B on C0, with criterion and coverage
R0: optional owner localization reference; unavailable volume remains unavailable
S0: optional pre-existing site hypothesis on A, in its own declared scope
I0: characterization Q0 + C0 + O0 + available R0/S0 references
F0: derived A footprint from O0's stated criterion; parent I0/O0, exact coverage
```

Two molecular participants remain distinct with one dry bank or no cavity.
Without O0/R0, the same question is an unlocalized declaration with no computed
footprint. A completed zero-contact O0 is a different observation from absent O0.
F0 does not declare the complete functional extent of S0.

### 14.2 Composite receptor and separate or joint interfaces

```text
C1: assembly containing A, B and C on one explicitly chosen structure
Q1: association of composite (A+B) with C; three participants, two sides
O_AB: observation for the internal A/B association, context and criterion retained
O_RC: admitted observation between the composite receptor and C
I1: Q1 with O_RC; O_AB remains separately attributed contextual evidence
F_C: projection toward C from explicitly selected contributing O_RC observations
```

Do not relabel O_AB as receptor–C evidence or infer three-body participation from
atomic chemical roles. A different question containing A–B and B–C retains two
binary associations. A genuine joint realization requires its own owner criterion
and support; summing the two observations does not create it or cooperativity.

### 14.3 Native versus chemically completed context

```text
C2/O2/I2: provider-native configuration, original observation and characterization
C3: explicit owner-derived completion/refinement with source/local maps and losses
I3: new characterization referring to I2 and C3
O3: affected chemistry/geometry reevaluated through the owner, or unavailable
```

Original evidence remains on C2. Generated atoms acquire no O2 membership or
confidence. An unaffected observation can be reused only with its original context
and adequate dependency guarantee. Missing O3 is not zero, and does not erase
unrelated useful geometry. The example commissions no completion calculation.

### 14.4 Repeated evidence, alternatives and information roles

```text
O4a/O4b: labelled observations supporting one compatible native chemical feature
H4: explicit owner hypothesis construction; provenance retains both observations
C5/O5/H5: alternative pose/state, retained as an alternative hypothesis
A4: application using a supplied prior, followed by candidate-derived observations
A5: independent absent-site request; evaluation reference remains provenance only
```

Reusing one compatible feature does not add its weights. Native constraint
conflicts require an explicit decision. H4/H5 do not silently become a joint
query. A same-candidate construction/fit is labelled consistency evidence.
The evaluation reference and A4's derived data remain outside A5's effective
localization inputs under the consumer's policy.

## 15. Acceptance and review matrix

| Control | Independent expected observation |
| --- | --- |
| Unlocalized declaration | Readable question/participants with explicit unknowns; no geometry/footprint fabricated. |
| Binary/composite/joint grouping | Molecular participants, groups, atomic roles and banks stay distinct; joint claims retain criterion/support. |
| Context and source maps | Nonidentity atom/group/structure maps, original 2 → local 0, effective state and partial/generated members are independently inspected. |
| Frames/quantities | Equivalent-unit readback and admitted transforms preserve definitions; missing frame proof, wrong quantity field/dimension and unsupported geometry refuse. |
| Revision/evidence | Detached copy/read preserves identity; new interpretation leaves old claim associations and owner artifacts unchanged. |
| Changes and selective applicability | Relevant source/query edits require reassessment; unrelated history/observations survive under their actual guarantees. |
| Comparison | Matching and differing criteria/participants have explicit policies; unavailable observables never become numbers. |
| Pharmacophoric semantics | Perspective, evidence-to-feature references, repeated contributions, alternatives and essential/exclusion decisions stay native. |
| Information use | Effective supplied and independently absent payloads follow consumer policy; consistency controls differ from independent evaluation. |
| Saved lifecycle | New-file protection, malformed/unsupported records, missing artifacts/readers and optional opaque owner data have distinct outcomes. |
| Attribution/replay | Public saved readback preserves original producer/run/occurrence/quantity definitions without new engine execution or credit. |

For each admitted case retain source/artifact identities, small input records,
expected behavior, actual public outputs and saved readback. Add a contradictory
or unsupported variant. Authored examples, syntax checks and successful parsing
are not executed scientific/consumer qualification.

This matrix does not make every future adapter an initial implementation gate.
First select a useful data profile and one complete owner-supported receiving
case; preserve pending initial commitments explicitly rather than silently
dropping them at closeout.

## 16. First receiving profile and work order

1. Agree the minimal local declaration/identity/version contract and finite
   molecular/owner handshakes. Record which facts are checked and which remain
   caller preconditions; no universal receipt is required before data-only work.
2. Deliver useful data-only declaration/inspection/copy/revision/persistence,
   with real emitted records and focused tests when implementation is authorized.
3. Receive one source-pinned saved owner result through public recovery,
   BindingMT composition, inspection and save/read, followed by one available
   footprint or comparison and its refusal controls.
4. Expand to further consumer profiles only with their own owner inputs and
   meaningful qualification; record shared agreement/adoption separately.

A candidate first input is an owner-admitted saved original PISA interface record
under [TopoMT #194](https://github.com/uibcdf/topomt/issues/194), with its required
original molecular source and recovery route. Choose observations whose actual
context/mapping support the selected downstream operation. Do not manufacture
a missing map, geometry or measurement to complete the route.

TopoMT's broader neutral context/participant/evaluation work under
[#60](https://github.com/uibcdf/topomt/issues/60),
[#61](https://github.com/uibcdf/topomt/issues/61) and
[#62](https://github.com/uibcdf/topomt/issues/62) remains separate from original
provider receiving. Original PISA records do not imply native Topography
promotion or universal support for all multimolecular profiles.

The first detailed implementation plan follows this review, not the reverse.
Runtime class/adapter work, numerical calculations, model/engine acquisition,
scientific campaigns and releases are outside this documentation increment.
The existing scientific full-suite resource hold is unchanged.

## 17. Contribution coverage and open decisions

| Contribution | Design coverage | Remaining review/receiving |
| --- | --- | --- |
| TopoMT: association/realization/descriptor and no bank/cavity equivalence | Sections 2–5 separate those meanings and keep canonical owner references. | Confirm association boundary and available first saved record/profile. |
| TopoMT: complementary binding question, context and interpretation | Sections 1, 4, 6–8 retain question, exact contexts, immutable evidence and operation-specific guarantees. | Agree additional binding-domain guarantees without a second spatial registry. |
| TopoMT: sites, footprints and multimolecular grouping | Sections 5, 9 and 14 retain many-to-many references, composite questions and joint evidence. | Confirm representative binary/composite/joint interpretations. |
| TopoMT: bounded public receiving before freeze | Sections 13, 15–16 separate saved provider receiving, native promotion and adoption. | Supply source-pinned public receiving input and expected limitations. |
| PeptideMT: supplied/candidate/evaluation origins | Section 11 and example 14.4 scope roles per application and inspect effective payloads. | Consumer supplies allowed information and final export seam. |
| PeptideMT: native versus completed chemistry | Sections 6, 8 and example 14.3 preserve original evidence, maps and selective applicability. | Owner-supported dependency facts and an admitted derived-context control. |
| PeptideMT: interpretable comparisons | Section 10 and the acceptance matrix name observable-specific policy and intentional participant differences. | Select one useful comparison with independently stated expectations. |
| PharmacophoreMT: perspective and evidence-to-site path | Section 11 separates sides, recognition context, source/occurrence references and construction. | Agree one admitted native projection profile and its limits. |
| PharmacophoreMT: multiplicity, alternatives and consensus | Sections 7–8, 11 and example 14.4 retain provenance without default weighting or joint constraints. | Native repeated/alternative/conflicting controls and saved readback. |
| PharmacophoreMT: native matching and independent evidence | Sections 10–11 preserve essential/exclusion decisions and distinguish same-candidate consistency. | Qualify exact native query/assignment and consumer-use policies. |

Specific decisions still requested:

- **BindingMT/consumers:** settle the minimum useful public operation and whether
  its result needs the working class name; close required fields and failure
  semantics before runtime implementation.
- **TopoMT:** confirm the canonical association/realization boundary and propose
  the saved source/record, recovery route, downstream operation and limitations.
- **MolSysMT:** identify public facts/checks and preconditions for selections,
  axes/maps, structure/state/frame, transforms and selective reassessment.
- **PeptideMT:** specify permitted information, native/derived contexts and the
  first interpretable comparison, without imposing target-specific public fields.
- **PharmacophoreMT:** review perspectives, occurrence/feature references,
  recognition scope and repeated/alternative/native-constraint controls.
- **MolSysSuite:** route exercised shared meanings and separately track actual
  consumer adoption. Favorable reviews are not a shared format freeze.

## 18. Sources, evidence limits and next action

This edition starts from BindingMT `268eec8086a3c67d66dd37bf7e3d644e5eae74e3`
and the three #112 comments linked above. Referenced owner design baselines are
TopoMT `3a8ee979db8de6f6345de74558a878bb96ba3234` and PharmacophoreMT
`ecd16946d64dd5cdc64132b026aaf12be2c0ef3a`; these are review/source identities,
not advertised dependency floors or qualified BindingMT integrations.

The [TopoMT conceptual contract](https://github.com/uibcdf/topomt/blob/3a8ee979db8de6f6345de74558a878bb96ba3234/devguide/topography_conceptual_contract.md#6-relations-and-spatial-interfaces)
and PharmacophoreMT's [composition](https://github.com/uibcdf/pharmacophoremt/blob/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a/devguide/interaction_composition_workflow.md)
and [native constraint](https://github.com/uibcdf/pharmacophoremt/blob/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a/devguide/native_constraint_semantics.md)
contracts supply their respective meanings. MolSysMT context ownership follows
the finite facts/questions already identified by the
[BindingSite work plan](binding_site_implementation_plan.md#5-p0-coordinate-the-finite-contract-and-inputs),
not an assumed universal descriptor or invalidation observer.

Live owner-issue inspection for this draft finds TopoMT #60/#61/#62 open and
#194 closed. This is a dated review observation, not a guarantee of later state
or complete neutral adoption. Refresh exact participating source/native closure
and input/artifact identities before an executed receiving profile.

No runtime implementation, molecular computation, compatibility receiving or
consumer adoption is demonstrated here. Documentation syntax/reference/resource
checks retain their limited scope. Native hypotheses, coordinates and quantities
in the symbolic examples have not been generated or measured.

Next obtain owner review of this document and one concrete input/operation for
the first receiving profile. Record accepted/deferred decisions with their owner
and revisit condition before preparing a bounded implementation plan. The useful
BindingSite core under #111 remains independent unless a concrete incompatibility
is identified and explicitly resolved.
