# Binding-interface characterization: second design for review

Revision **2**, 2026-11-12. Owner: [BindingMT #112](https://github.com/uibcdf/bindingmt/issues/112).
Status: **scientific design; first data-only runtime profile delivered separately**.
The [implemented first data profile](binding_interface_data_core.md) owns the actual
public spellings and experimental persistence. Numerical and typed-provider
sketches below remain proposals, without a stable schema freeze.
The maintainer requests a corrected second design after the three component
follow-ups, ready for another review round. This is the maintained detailed
proposal; the issue carries the first delivery and owner responses.
The [owning record](pending_proposals/binding_interface_public_contract.md)
tracks scope, evidence and the next action.

Revision 2 was shared from exact source `5aa21b1aaf27ee7708e5a7bb4fe58bd0300d49f0`
in the [second review post](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6834362774).
The [implementation/work plan](binding_interface_implementation_plan.md) now
records evaluation of the three favorable second-round replies and the proposed
bounded increments. Its later native catalogue extension records ordinary contact
calculation followed by surfaces/burial, preserving this scientific information
model and the separate saved-PISA receiving branch. The sketches below retain
their supplied-evidence execution boundary. This is planning evidence; runtime
implementation and executed receiving remain pending.

The final collaborator round supports proceeding within work-plan revision 4.
Its [recorded contributions and readiness ledger](binding_interface_plan_review.md#7-final-collaborator-round-and-recorded-contributions)
add finite H/P receiving details and the restricted MolSysMT offer, distinguishing
available inputs/contracts from decisions and actual client evidence still due.
This scientific information model remains revision 2; public spellings below
stay proposed until the corresponding implementation admission.

The design incorporates the [TopoMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6812846154),
[PeptideMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6813153779)
and [PharmacophoreMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6814109974)
contributions and their subsequent [TopoMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6817022945),
[PeptideMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6817091832)
and [PharmacophoreMT](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6816948272)
reviews of the [first design at `204f812`](https://github.com/uibcdf/bindingmt/blob/204f8120e60be4ac7b6272b46afc940c5ab703a2/devguide/binding_interface_design.md).
All three follow-ups are favorable at design level. They do not freeze a class,
shared profile or schema, or demonstrate executed compatibility. MolSysMT has
no contribution in the seven-comment review baseline inspected for this edition.

Revision 2 preserves the architecture and makes the first profiles concrete:

- Preserve completed analysis evidence even when no interface records exist.
- Name the saved PISA inputs and the participant reported-contact footprint,
  keeping it distinct from buried-area membership and continuous support.
- Propose explicit public assurance requests and a fact/check/precondition matrix.
- Start the ordinary API example with A | B and inspectable analysis outcomes.
- Make grouping select the observations consumed, including a C–D exclusion
  control and original analysis/occurrence correspondence.
- Specify the independent native pharmacophoric and K/N/native-derived/comparison
  consumer cases without making all of them prerequisites for the first core.

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

`explicit question/context + supplied analysis evidence/findings → characterization → inspection → save/read → one qualified footprint or comparison`

Composition does not run missing detectors. The current work plan adds a separate
explicit native calculation request using public molecular tools, returning this
same inspectable result model. Its first numerical route is contacts, followed by
surfaces/burial; names/defaults and each profile remain admission decisions.
Calculation retains its numerical owners. A declaration
with no supplied analysis or other evidence retains unknown support. Completed
analysis with zero findings has its own preserved outcome, not that no-evidence
state. An inferred association retains the criterion and evidence supplied
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
| Topographic associations/realizations, support, regional physicochemical observations, classification and evaluations | TopoMT |
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

TopoMT's regional physicochemistry can describe its own pocket/wall/channel or
supported interface without selecting a binding partner. MolSysMT keeps generic
chemistry/annotations; BindingMT interprets qualified regional observations for a
specified association or directly composes molecular tools. Descriptor names do
not create exclusive ownership across these different questions/supports. The
work plan receives [TopoMT's clarification](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6837860911)
and tracks optional regional receiving under TopoMT #198 separately from native
contact/surface qualification and the unchanged information model.

No shared package, molecular snapshot engine, generic graph service or universal
execution/provenance framework is proposed.

## 4. Minimal information model

These are record roles, not required public classes:

| Group | Information and invariant |
| --- | --- |
| Identity/question | Declaration identity, optional label, binding question, declared/inferred status, process and relevant states/conditions. Observation origin is retained separately. |
| Participants/grouping | Molecular source occurrences, granularity, selections, available membership, contextual roles and the sides chosen for this question. |
| Contexts | Source/assembly/symmetry occurrence, source and local structure/state/frame, correspondence maps, actual check scope and trust assumptions. |
| Analyses | Exact owner/run references, evaluated criterion/context/coverage, outcome and available result set, including completed analyses producing no records. |
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

### 4.1 Analysis evidence and its individual findings

An analysis is not the list of findings it produced. Preserve an analysis-level
reference even when that list is empty. Its outcome and the availability of its
native artifacts are separate facts. A supplied reference can be readable while
its outcome remains unknown until sufficient owner evidence is recovered.

| Analysis state | Retained meaning | Interface/footprint consequence |
| --- | --- | --- |
| Completed with findings | Owner/run, criterion, context, evaluated scope and exact result references. | Admit only the selected finding and downstream operation whose facts are available. |
| Completed with zero interfaces | Positive evidence that this analysis completed and reported zero under its criterion/context. | No positive realization is created; no interface-specific footprint exists to project. |
| No supplied analysis | No evaluated evidence for this question/context. | Unknown/unevaluated, not completed-empty or evidence against binding. |
| Failed original analysis | Original failure evidence, source/run references and available diagnostics. | No successful empty analysis or invented realization. |
| Reference-only or unrecovered analysis | Exact available reference and unresolved outcome/availability where necessary. | Preserve inspection; refuse operations needing unavailable evidence. |

Missing correspondence and contradictory source/context are admission/application
assessments, not replacements for the original analysis outcome. A contradiction
does not turn completed evidence into unknown or successful empty. The current
application refuses the contradicted claim while historical evidence remains
attributed to its original context.

The first public composition profile must accept an analysis carrier/reference
as well as individual observations. Requiring only `output.interfaces[0]` would
make completed zero-interface results impossible to receive faithfully. Counts
alone do not establish completion; retain the owner's outcome and evaluated scope.

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
| Owner analysis | The original run/analysis and its evaluated criterion/context, independently of whether it has findings. |
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

### 10.1 Proposed public assurance requests

Use a public `assurance_scope` separately from `context_policy`. The following
spellings are review proposals, not implemented modes or a frozen vocabulary:

| Request | Required promise | Missing prerequisite or contradiction |
| --- | --- | --- |
| `preserved_evidence` | Validate the core record and preserve admitted declared fields, analysis outcomes, references and original attribution. No molecular lookup is required. | Refuse malformed required data; retain honest unknown/reference-only context without claiming applicability. |
| `molecular_correspondence` | Establish the membership/structure/state/frame relationships needed by the requested projection on the actual supplied context. | Missing required facts or contradictory maps/context refuse that application. Preserved evidence remains inspectable through its own explicit route. |
| `current_finding` | Additionally establish the owner finding's relevant full input/query dependencies for the context of use. | Unsupported profile or missing proof refuses this stronger request; unchanged footprint coordinates are insufficient. |

These are scoped promises, not one global ordered validity score. Native evidence
recovery is a separate explicit owner operation: recovering a result on its
original source does not automatically verify transfer to another current context.

The proposed first context policy is `require_match`: the selected profile's
required checks must succeed. For `preserved_evidence`, no molecular match is
requested and the assessment says so. No trust option makes an observed
contradiction disappear. Caller preconditions name their scope; they cannot be
relabeled as checks that were not performed. Additional policies need a concrete
workflow and owner agreement rather than an unrestricted bypass flag.

The first implementation need only admit the selected promises it can qualify.
An unimplemented stronger promise reports unsupported before scientific execution;
an implemented profile lacking necessary evidence reports missing proof. Neither
silently returns a weaker successful application. This does not make every
stronger profile a data-core prerequisite.

### 10.2 Fact, check and caller-precondition matrix

This is the finite review matrix requested by PeptideMT. Source inspection
identifies candidates, not executed BindingMT guarantees. Exact profile admission
and any still-unnamed owner accessor remain pending MolSysMT/owner agreement.

| Required fact | Public operation/source | Actual check to qualify | Caller precondition | Unavailable or contradictory outcome |
| --- | --- | --- | --- | --- |
| Saved evidence integrity | `topomt.provider_output.ProviderRun.load`, TopoMT `3a8ee979` | Owner checks archive members, artifact hashes and run identity. | The selected bundle is the intended original evidence; integrity alone authenticates no molecular meaning. | Missing internal manifest-declared artifacts or corrupt ZIP data refuse native recovery. An unavailable external asset may leave an admitted BindingMT reference-only record; it is not a partially recovered native result. |
| Source-bound PISA recovery/outcome | `tmt.load_provider_output(bundle, molecular_system=original_source)`, TopoMT `3a8ee979` | Owner reader checks its supported saved source/context and supplied-assembly policy, preserving completed-empty output. | Supply the complete unchanged original source; do not override saved selection/frame/reference chemistry. | Missing/contradictory context refuses claimed recovery. Failure capture remains failure evidence through its owner route. |
| Participant selection and axes | `msm.select`/`msm.get`, candidate MolSysMT `ff25f120` | Resolve admitted selection on the chosen structure/state; inspect actual membership and relevant axes. | Caller source association is retained with its actual authority; matching labels/counts are not proof. | Unresolved declaration remains readable; a required selection/axis mismatch refuses projection. |
| Source/local atom and structure correspondence | Maps from the actual qualified MolSysMT conversion/extraction operation; exact accessor/profile still to agree | Independently check nonidentity maps, original 2 → local 0, unmapped/generated entries and ordering. | Retain owner report/source identities; declare any caller map without upgrading its authority. | Missing required map gives missing proof; contradictory map refuses. No numeric-identity assumption. |
| Effective chemical state | Public MolSysMT state/structure facts via `msm.get` and the selected consumer's contract | Resolve the effective state associated with the selected local structure and original evidence; check the admitted chemistry profile. | Source/state preservation conditions remain explicit. PISA and atomic H-bond/hydrophobic conversion retain their reference-state restrictions. | Unsupported or contradictory state refuses the affected operation, without erasing unrelated observations. |
| Frame/image/transform | Public owner coordinate/frame facts and qualified MolSysMT transform; exact required accessor/profile still to agree | Check the required relationship and retained transform/image convention, rather than only equal coordinates. | No unrecorded source edits or assumed alignment. | Missing frame proof blocks spatial use; contradictory context refuses. |
| Observations belonging to requested groups | `Interactions.between_selections`, MolSysMT `ff25f120` | Check disjoint resolved sets, selected relation/occurrence scope, exclusivity and retained coverage; exclude C–D in the declared receptor–C profile. | Source and full chemical participants satisfy the native consumer's admitted contract. | Unsupported grouping refuses conversion; do not split chemical participants or keep out-of-scope relations silently. |
| Original observation correspondence | Native query views and `Interactions.to_dict`, MolSysMT `ff25f120`; native hypothesis maps, PharmacophoreMT `ecd16946` | Inspect analysis-qualified relation/occurrence IDs and output-site/contribution maps before and after each query, serialization or remap. | A new analysis/remap may renumber; retain its explicit correspondence. | Missing correspondence gives unresolved/reference-only evidence; required projection refuses. |
| Check/use lifetime and finding dependencies | Selected owner receipt/sufficient captured input plus explicit boundary checks; no universal API assumed | Check the actual selected/exported input and the required producer input/query scope at use. | Preserve any admitted unchanged-input interval; live handle equality supplies no receipt. | Reassess relevant changes or refuse. Unsupported `current_finding` is not downgraded to correspondence. |

Data-only construction does not wait for unresolved molecular rows. Implemented
projections must close the rows they actually need. A cell naming a candidate
operation is not a claim of general authentication, snapshot support or qualified
cross-component compatibility.

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

### 11.1 Grouping must select the observations consumed

For `(A+B) | C`, the requested receptor–C projection must consume admitted A–C
and B–C observations, retaining internal A–B evidence separately. Add an unrelated
participant D and C–D observations as a negative control. A grouping label alone
does not establish that the conversion excluded D.

At PharmacophoreMT `ecd16946`, `from_interactions` selects the ligand and treats
all remaining source atoms as its counterpart population. Selecting C therefore
does not itself exclude C–D observations. Supply an owner-supported scoped native
view while keeping the complete unchanged source/axes needed by that constructor.

MolSysMT `ff25f120` provides a candidate public selection route:

```python
scoped_observations = interactions.between_selections(
    atoms_ab,
    atoms_c,
    structure_indices=[local_structure],
    exclusive=True,
)
```

This sketch has not been executed here. Its two sets must be disjoint. The
proposed first strict-group policy requires all relation atoms to lie in their
union; the owner's default nonexclusive query can retain additional participant
atoms. This is an explicit projection policy, not a universal rule for every
multimolecular observation. Do not cut compound chemical participants into
artificial smaller features. If the chosen conversion cannot express a required
participant under the admitted scope, refuse or use an explicit owner-supported
policy with its omissions; do not return apparently complete partial chemistry.

Retain original analysis identity, local relation/occurrence keys, the query and
its effective structures/coverage, every exclusion and the output-site map.
In-memory native query views expose original occurrence positions; serialization,
remapping or a new analysis must retain explicit correspondence if indices change.
Equal numbers are not proof of identity. Qualify these facts at each handoff.
`Interactions.to_dict` exposes selected numeric columns and coverage for
inspection; it is not the complete typed native serialization. Use the owner's
admitted full record/persistence route for saved interactions.

The control passes only if the submitted/consumed observation population excludes
C–D and internal A–B for this projection, while original analyses remain intact
and their context remains inspectable.

### 11.2 Independent native PharmacophoreMT receiving specification

The first native observed-participant route uses public `from_interactions` or
`from_interaction_collection`, not a fabricated conversion from PISA measurements.
A complementary receptor-derived hypothesis is a separate construction choice.

| Item | First proposed native receiving requirement |
| --- | --- |
| Inputs | Native `molsysmt.Interactions`, the same unchanged complete molecular source, explicitly scoped observations and admitted chemical participants. |
| Structure/state | One common evaluated local structure and explicit common chemical state for a collection, with original/local maps. Atomic H-bond/hydrophobic conversion retains the source reference-state requirement; other routes keep their own state contract. |
| Construction | Public owner API with explicit projection perspective, recognition context, retained features and omissions; consistency checks and caller preservation conditions are separate guarantees. |
| Repeated evidence | Two labelled analyses support one compatible typed feature/site; contributions survive without automatic weight inflation. Native conflicts refuse or use an explicit admitted policy. |
| Alternative | A different pose/state hypothesis remains separate unless a qualified combination policy is deliberately selected. |
| Persistence | Native hypothesis artifact and exact output-site references retain original analysis/relation/occurrence, chemical roles, source/frame/state and construction decisions. |
| Refusal controls | Incompatible state/maps, incomplete chemical participants, unscoped C–D contributions, failed required conversion, unsupported profile and missing native artifact/reader. Evaluated-empty remains distinct from a usable positive query. |

Keep the association acyclic by constructing H0 from an exact I0 characterization/
analysis context, then deriving I1 that references the saved H0 and its site map.
Do not rewrite H0 to point at a future/latest I1 interpretation. Replay performs
no new detection and retains original attribution.

Observed-interaction and explicit receptor-projection constructors initially emit
positive sites as essential with weight one. Separate curated native-hypothesis
controls must demonstrate an essential site with zero weight, an exclusion veto
and a positive fit accompanied by a failed matching decision. Do not invent these
settings as options of every constructor or interpret them as binding importance.
This native receiving remains independent of the first PISA footprint workflow.

### 11.3 PeptideMT K/N, derived-context and comparison specifications

| Case | Proposed inputs and observation boundary | Required control |
| --- | --- | --- |
| K: permitted localization | Independent request with an explicitly permitted site reference; reference partner pose retained only for evaluation. | Final selected/exported payload contains only the admitted localization fields and source structures. |
| N: absent supplied localization | Separately constructed request; evaluation reference and earlier K result remain available as separately identified provenance. | No localization inherited from those references, K-derived poses/contacts/crops/restraints or viewer state. No supplied site differs from evaluated-empty and evidence against binding. |
| Native → derived chemistry | Original native context, owner-derived completion/refinement with retained/removed/generated maps, one dependent observation and a separately scoped receptor-reference observation. | Original evidence survives; both new atoms and moved existing atoms require appropriate reassessment. Missing reevaluation is unavailable. Unaffected historical evidence retains its actual dependency scope. |
| Pose comparison | Two poses of the same molecular pair, one declared observable/criterion, frame relationships, coverage and normalization if used. | State whether comparison is admitted; add a changed-criterion/coverage/partner variant with an explicit policy, not a universal identical-participant rule. |

Export inspection qualifies that boundary, not a provider's complete internal
scientific influence. Holo geometry, training/template exposure and human knowledge
still preclude claiming a blind benchmark from these controls. Any independently
required global-domain policy keeps its own provenance. Exact MDM2–p53 site,
thresholds and provider configurations remain consumer decisions; this design
selects none and commissions no scientific execution.

## 12. Proposed public surface and ordinary workflow

Two explicit routes share the result model. The current work plan's first
ordinary numerical route requests admitted native contacts on a chosen MolSys
context, followed by surfaces/burial under their own profile. Its exact public
spelling/defaults remain N0 decisions. Supplied-evidence composition separately
resolves admitted selections/references, records actual checks and refuses
unsupported required guarantees without calculating missing observations.

The native user workflow is molecular context + participants + admitted profile
-> actual calculation -> concise/expert inspection -> result/footprint save/read.
The work plan records the required produced artifacts and limitations for that
workflow. Summary, copying and saved reading calculate nothing. The code example
below retains the explicit saved-provider composition route; it is not a new
automatic PISA dependency or the numerical priority of the native programme.

### 12.1 Binary recovery, composition and inspection

The supplied-evidence localized example uses A | B. The TopoMT reader below exists
at the pinned source; the BindingMT operations are proposed syntax and have not
been executed. `system` is the complete unchanged original source, ordinarily
a native MolSys; `chosen_structure` and the state must agree with the saved
profile. The reader restores its context and accepts no frame/state override.

```python
output = tmt.load_provider_output(pisa_bundle, molecular_system=system)

characterization = bmt.characterize_interface(
    question=association_question,
    participants={"A": selection_a, "B": selection_b},
    grouping=(("A",), ("B",)),
    molecular_system=system,
    structure_index=chosen_structure,
    chemical_state="reference",
    analyses={"pisa": output},
    site_refs=site_references,
    assurance_scope="molecular_correspondence",
    context_policy="require_match",
)

print(characterization.summary())
```

`analyses` receives the owner analysis carrier, including successful output with
no interface records. `observations` may additionally receive admitted individual
results with their exact analysis association; it does not replace analysis-level
evidence. The adapter stores exact owner references and resolved outcomes, not
an independently editable ProviderOutput copy. Multiple owner contexts remain
distinct rather than inheriting this example's one molecular context.

The proposed `summary()` exposes at least the following information. This is an
authored inspection outline, not an observed API response:

```text
question and grouping: caller's association question, A | B
analyses: original PISA run/context, completed outcome and result count
observations: exact run-scoped record references, or completed zero-interface state
available projections: participant reported-contact footprint if correspondence exists
assessment: requested assurance, checks, coverage and remaining preconditions
limitations: no recovered continuous patch, buried-atom membership or binding proof
```

The positive PISA case can then request a proposed footprint operation:

```python
footprint = characterization.project_footprint(
    analysis="pisa",
    source_id="1",
    participant="A",
    method="reported_contacts",
    contact_groups=chosen_contact_groups,
    molecular_system=system,
    assurance_scope="molecular_correspondence",
    context_policy="require_match",
)
```

`source_id` is resolved within the exact stored analysis/run, not globally.
The selected contact groups are explicit and the operation follows their mapped
participant endpoints. A zero-interface analysis remains importable and
inspectable; a request for a nonexistent positive finding/footprint reports
that prerequisite, rather than inventing a realization.

### 12.2 Declaration-only and later composite profiles

Data-only construction need not resolve molecular data:

```python
declaration = bmt.characterize_interface(
    question=association_question,
    participants={"A": declared_source_a, "B": declared_source_b},
    grouping=(("A",), ("B",)),
    analyses={},
    assurance_scope="preserved_evidence",
)
```

This records no supplied analysis and unknown support. No context-match policy
is requested; inspection must show molecular checks as `not_required`, not a
performed `match`. The work plan records the proposed explicit-policy admission
rule before implementation. Completed-zero analysis
instead supplies its actual analysis carrier/reference. The same ordinary
construction can later express `(A+B) | C` with explicit groups and the scoped
observation policy in section 11.1; it does not reinterpret A | B or silently
select from unrelated contexts.

`question` holds the declared scientific question/process; its concrete minimal
fields need review. Participant labels are local. Required selections, effective
state and context facts use admitted owner operations. The exposed assurances
in section 10.1 remain proposals until the first profile is agreed/qualified;
the sketches do not establish a universal descriptor/check API or an executed
stronger guarantee.

| Public capability | Proposed behavior and first-profile limit |
| --- | --- |
| Declare/import | Construct a data-only question or compose admitted analysis carriers/references and findings; keep completed-zero, no analysis, failure, unresolved context and declared/inferred status explicit. |
| Inspect | Expose question, analysis outcomes, observations, available footprints, coverage, prerequisites and exact owner references; no implicit geometry calculation or asset fetch. |
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
  analyses[]             exact owner/run/criterion/context, completion/outcome and result refs
  association_refs[]     exact owner associations, or explicit declared-only status
  realization_refs[]     localizations with context and coexistence/alternative roles
  observations[]         exact analysis-qualified results/occurrences, definitions and provenance
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
AN0: exact owner analysis/run on C0, with outcome, criterion and evaluated scope
O0: owner finding/observation within AN0 for A/B, with criterion and coverage
R0: optional owner localization reference; unavailable volume remains unavailable
S0: optional pre-existing site hypothesis on A, in its own declared scope
I0: characterization Q0 + C0 + AN0/O0 + available R0/S0 references
F0: derived A footprint from O0's stated criterion; parent I0/O0, exact coverage
```

Two molecular participants remain distinct with one dry bank or no cavity.
Without AN0/O0/R0 or other evidence, the same question is an unlocalized
declaration with unknown support and no computed footprint. A completed
zero-contact observation differs from an absent observation; an analysis
producing zero findings is the separate section 14.5 control.
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

### 14.5 Completed analysis with no interface records

```text
Q6/C6: declared A | B question and the complete evaluated owner context
AN6: exact original analysis/run, completed, zero interface records
I6: Q6 + C6 + AN6; no fabricated positive association/realization/footprint
I7: separate declaration with no supplied analysis; outcome unevaluated/unknown
AN8/I8: original failed analysis evidence and its characterization, no successful-empty claim
```

I6, I7 and I8 cannot collapse to the same empty observations list. AN6's
criterion/context/completion remain inspectable after save/read. A query for
AN6's positive footprint reports that no such finding exists. Missing map or
contradictory current source creates an application assessment without rewriting
the original outcome of AN6 or AN8. These are symbolic cases, not executed output.

## 15. Acceptance and review matrix

| Control | Independent expected observation |
| --- | --- |
| Unlocalized declaration | Readable question/participants with explicit unknowns; no geometry/footprint fabricated. |
| Analysis-level evidence | Completed nonempty, completed-zero, no supplied analysis and original failure survive as distinct outcomes with their criterion/context and owner references. |
| Binary/composite/joint grouping | Molecular participants, groups, atomic roles and banks stay distinct; joint claims retain criterion/support. |
| Actual grouping consumption | Scoped `(A+B) \| C` projection uses the admitted receptor–C observations, excludes C–D and internal A–B, and retains original analysis/occurrence correspondence and chemical participant integrity. |
| Context and source maps | Nonidentity atom/group/structure maps, original 2 → local 0, effective state and partial/generated members are independently inspected. |
| Frames/quantities | Equivalent-unit readback and admitted transforms preserve definitions; missing frame proof, wrong quantity field/dimension and unsupported geometry refuse. |
| Revision/evidence | Detached copy/read preserves identity; new interpretation leaves old claim associations and owner artifacts unchanged. |
| Changes and selective applicability | Relevant source/query edits require reassessment; unrelated history/observations survive under their actual guarantees. |
| Comparison | Matching and differing criteria/participants have explicit policies; unavailable observables never become numbers. |
| Pharmacophoric semantics | Perspective, evidence-to-feature references, repeated contributions, alternatives and essential/exclusion decisions stay native. |
| Information use | Effective supplied and independently absent payloads follow consumer policy; consistency controls differ from independent evaluation. |
| Saved lifecycle | New-file protection, malformed/unsupported records, missing artifacts/readers and optional opaque owner data have distinct outcomes. |
| Public guarantee | Preservation, native recovery, molecular correspondence and finding applicability expose their actual facts/checks/preconditions; stronger unsupported or unproven requests refuse without downgrade. |
| Attribution/replay | Public saved readback preserves original producer/run/occurrence/quantity definitions without new engine execution or credit. |

For each admitted case retain source/artifact identities, small input records,
expected behavior, actual public outputs and saved readback. Add a contradictory
or unsupported variant. Authored examples, syntax checks and successful parsing
are not executed scientific/consumer qualification.

Keep the frozen PISA inputs unchanged. Nonidentity maps and original structure
2 → local 0 can be exercised in separately identified native/derived-context
controls; do not alter an original provider source and claim the same saved
source-bound recovery. Any transfer needs its own admitted correspondence profile.

This matrix does not make every future adapter an initial implementation gate.
First select a useful data profile and one complete owner-supported receiving
case; preserve pending initial commitments explicitly rather than silently
dropping them at closeout.

## 16. First receiving profile and work order

1. Agree the minimal local declaration/identity/version contract. Initiate finite
   molecular/owner handshakes for their respective profiles in parallel with the
   data core. Record checked facts and caller preconditions; unresolved molecular
   rows are not global data-only prerequisites.
2. Deliver useful data-only declaration/inspection/copy/revision/persistence,
   with real emitted records and focused tests when implementation is authorized.
3. Close the actual native contact/context/tool profile and deliver explicit
   public calculation, characterization, inspection and saved replay without
   PISA/TopoMT. Qualify surfaces/burial next under its own molecular contract.
4. Receive one source-pinned saved owner result through public recovery,
   BindingMT composition, inspection and save/read, followed by one available
   footprint or comparison and its refusal controls.
5. Expand to further consumer profiles only with their own owner inputs and
   meaningful qualification; record shared agreement/adoption separately.

### 16.1 Saved PISA profile and a participant contact footprint

TopoMT supplied the concrete saved-provider candidate in its
[follow-up](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6817022945),
supported by PeptideMT. Use the frozen
[PISA inputs/results/protocol](https://github.com/uibcdf/topomt/tree/3a8ee979db8de6f6345de74558a878bb96ba3234/tests/data/original_local/pisa)
at TopoMT `3a8ee979db8de6f6345de74558a878bb96ba3234`; preserve the owner's
`protocol.json` and artifact hashes. This design identifies those immutable
inputs; it has not executed their BindingMT receiving or independently measured
their scientific outputs.

| Input/control | Owner-supported fact and required BindingMT behavior |
| --- | --- |
| `input.pdb` + `pisa.zip` | Completed original supplied-assembly PISA result, one interface with run-scoped `source_id == '1'`; recover, compose A \| B, inspect and save/read. |
| `empty_input.pdb` + `pisa-empty.zip` | Completed zero-interface analysis, retaining original run/context/criterion and supplied-assembly summary; no positive realization fabricated. |
| `pisa-failed.zip` | Original failed-analysis capture; preserve owner failure evidence through its admitted evidence-reader route, not a successful ProviderOutput or empty interface result. |
| No supplied analysis | Explicit unknown/unevaluated declaration, independent of the completed-empty input. |
| Correspondence unavailable | Reference-only/unresolved evidence remains inspectable where admitted; a required participant footprint refuses missing correspondence. |
| Wrong source/context or corrupted evidence | Refuse the affected admission/recovery/application without weakening it to unknown or successful empty. |

The positive and empty source-bound route is the existing
`tmt.load_provider_output(bundle, molecular_system=complete_original_source)`.
It restores and verifies its supported saved context and needs neither PISA nor
its runtime resources. Saved selection/frame/reference chemistry are not caller
override options. The strict successful-output reader need not turn a failed
capture into a ProviderOutput: `topomt.provider_output.ProviderRun.load` preserves
verified original evidence for inspection. The first failed-analysis adapter
must agree the owner's actual status/diagnostic interpretation; archive integrity
or a file name alone does not establish scientific completion/failure.
A present-day recovery/parser error is not automatically proof that the original
scientific analysis failed; preserve the actual error and original evidence
without rewriting that outcome.

The proposed complete path is:

`recover original PISA output → compose A | B with analysis evidence → inspect → save/read → derive A's reported-contact footprint`

The footprint is the source-indexed contact endpoints on one explicitly named
participant, from explicitly selected PISA contact groups. Combined
`interface.atom_indices` covers both sides; it is not automatically A's set.
Retain original run/record/group identities, mapped endpoints, participant/source
correspondence, effective population/coverage, quantities and derivation.

The owner's positive control reports **28 mapped contact atoms** and **20 buried
atoms**. These are different populations across the reported interface, not
asserted per-participant footprint sizes. Buried counts/residue areas do not
recover an exact buried source-atom set, continuous surface patch or complete
functional site. Keep the original PISA measurement definitions, units and
attribution; this control validates neither biological-interface prediction nor
energy accuracy.

Qualify source correspondence and check/use scope against the complete original
input required by the owner route, not just the smaller footprint. An initial
implementation may support preservation and the chosen correspondence profile
while explicitly refusing unqualified `current_finding` requests. The first
admission decision records exactly which scopes are delivered; no general
producer-input revalidation follows from footprint success.

TopoMT's broader neutral context/participant/evaluation work under
[#60](https://github.com/uibcdf/topomt/issues/60),
[#61](https://github.com/uibcdf/topomt/issues/61) and
[#62](https://github.com/uibcdf/topomt/issues/62) remains separate from original
provider receiving. Original PISA records do not imply native Topography
promotion or universal support for all multimolecular profiles.

### 16.2 Independent increments and receiving ownership

| Increment | Independently useful outcome | What it does not wait for |
| --- | --- | --- |
| Data core | Explicit declaration/analysis identity, inspection and faithful versioned persistence with real emitted records/tests. | Universal molecular receipts, every owner adapter or all consumer profiles. |
| Native contacts | Public calculation-to-characterization round trip, exact atom/residue contacts and both footprints, independent saved replay. | PISA, TopoMT, surface/chemical recognition or every future molecular profile. |
| Native surfaces/burial | Both participant SASA losses, mapped contributions, explicit area convention and independent numerical/readback controls. | All chemical/topographic/ensemble/energy families; its own radius/context/tool admission remains required. |
| PISA receiving | One complete saved positive/empty/failure and participant-footprint route with exact supported guarantees/refusals. | Neutral native Topography promotion, dynamic methods or the native pharmacophoric route. |
| Native pharmacophoric receiving | The section 11.1/11.2 compatible native input/subset/site-map/persistence and constraint controls. | PISA being converted into native interactions or a general interface-to-pharmacophore algorithm. |
| Consumer controls | Section 11.3's admitted K/N/native-derived/comparison specifications at the actual public export boundary. | Every later provider, target-specific parameter selection or a blind-benchmark claim. |

Each operation closes only its actual fact/profile prerequisites. Preserve
agreed initial obligations and their owner/status; a delayed profile is pending
or explicitly rescoped by the maintainer, not silently dropped. Shared acceptance,
implemented receiving and each consumer's adoption remain separate evidence.

The first detailed implementation plan follows this review, not the reverse.
Runtime class/adapter work, numerical calculations, model/engine acquisition,
scientific campaigns and releases are outside this documentation increment.
The existing scientific full-suite resource hold is unchanged.

## 17. Contribution coverage and open decisions

| Contribution | Design coverage | Remaining review/receiving |
| --- | --- | --- |
| TopoMT: association/realization/descriptor and no bank/cavity equivalence | Sections 2–5 separate those meanings and keep canonical owner references; the follow-up supports this boundary. | Close the exercised public profile and execute its actual receiving. |
| TopoMT: complementary binding question, context and interpretation | Sections 1, 4, 6–8 retain question, exact contexts, immutable evidence and operation-specific guarantees. | Agree additional binding-domain guarantees without a second spatial registry. |
| TopoMT: sites, footprints and multimolecular grouping | Sections 5, 9 and 14 retain many-to-many references, composite questions and joint evidence. | Confirm representative binary/composite/joint interpretations. |
| TopoMT: bounded public receiving before freeze | Sections 13, 15–16 separate saved provider receiving, native promotion and adoption; fixed positive/empty/failure PISA inputs and the contact-footprint definition are now identified. | Qualify BindingMT composition/persistence/footprint and all admitted refusal controls; existing provider tests are not client receiving. |
| PeptideMT: supplied/candidate/evaluation origins | Section 11 and example 14.4 scope roles per application and inspect effective payloads. | Consumer supplies allowed information and final export seam. |
| PeptideMT: native versus completed chemistry | Sections 6, 8 and example 14.3 preserve original evidence, maps and selective applicability. | Owner-supported dependency facts and an admitted derived-context control. |
| PeptideMT: interpretable comparisons | Section 10 and the acceptance matrix name observable-specific policy and intentional participant differences. | Select one useful comparison with independently stated expectations. |
| PharmacophoreMT: perspective and evidence-to-site path | Section 11 separates sides, recognition context, source/occurrence references and construction. | Agree one admitted native projection profile and its limits. |
| PharmacophoreMT: multiplicity, alternatives and consensus | Sections 7–8, 11 and example 14.4 retain provenance without default weighting or joint constraints. | Native repeated/alternative/conflicting controls and saved readback. |
| PharmacophoreMT: native matching and independent evidence | Sections 10–11 preserve essential/exclusion decisions and distinguish same-candidate consistency. | Qualify exact native query/assignment and consumer-use policies. |

Disposition of the three follow-up reviews:

| Follow-up refinement | Revision-2 correction | Still pending |
| --- | --- | --- |
| TopoMT: completed analysis without findings | Sections 4.1, 12–14 and 16.1 make analysis-level intake/outcome first-class, separate from finding records and current-context assessments. | Owner-agreed failed-capture interpretation and actual positive/empty/no-analysis/failure readback. |
| TopoMT: participant reported-contact footprint | Section 16.1 fixes the source/bundle/profile and retains endpoint groups, run-scoped record identity and the 28-contact/20-buried distinction. | Actual endpoint/participant correspondence and complete public route; no continuous support inferred. |
| TopoMT/PeptideMT: public assurance and finite facts | Sections 10.1/10.2 and 12 expose provisional requests, exact check scope, source revisions, preconditions and refusal. | Owner disposition of pending molecular accessors/facts and qualification of each delivered scope. |
| TopoMT: binary ordinary example and inspection | Section 12 starts with A \| B, analysis-aware composition and a small inspection outline before composite cases. | API spelling/admission and real emitted/reader output; the sketches remain authored. |
| PharmacophoreMT: effective grouping including unrelated D | Section 11.1 scopes observations through the owner query, proposes explicit exclusivity, and requires original analysis/occurrence correspondence and actual consumption checks. | Execute the admitted C–D/compound-participant and correspondence controls. |
| PharmacophoreMT: native input and saved observation-to-site route | Section 11.2 selects existing native APIs, common local structure/state, source-preservation scope, I0/H0/I1 references and separate native-constraint fixtures. | Concrete native source/analysis artifacts and owner-specific construction/persistence/refusal receiving. |
| PeptideMT: K/N, native-derived and comparison cases | Section 11.3 states effective exports, retained evaluation provenance, source/member changes, permitted comparison and non-blind evidence limits. | Actual consumer inputs/export seam; target-specific choices remain unselected. |

The replies support retaining the architecture, not freezing the revised
requests, input schema or a class. TopoMT has supplied a concrete saved-data
candidate. PharmacophoreMT and PeptideMT have offered bounded specifications;
their concrete execution inputs and results are not deemed received merely
from those offers.

Specific decisions still requested:

- **BindingMT/consumers:** settle the minimum useful public operation and whether
  its result needs the working class name; review the proposed assurance/intake
  spellings and close required fields/failure semantics before implementation.
- **TopoMT:** confirm the exact PISA footprint/contact-group and failed-analysis
  evidence handshakes for the supplied frozen inputs; the scientific ownership
  direction and concrete receiving candidate are already supported in its reply.
- **MolSysMT:** identify public facts/checks and preconditions for selections,
  axes/maps, structure/state/frame, transforms and selective reassessment.
- **PeptideMT:** specify permitted information, native/derived contexts and the
  first interpretable comparison, without imposing target-specific public fields.
- **PharmacophoreMT:** review perspectives, occurrence/feature references,
  recognition scope and repeated/alternative/native-constraint controls.
- **MolSysSuite:** route exercised shared meanings and separately track actual
  consumer adoption. Favorable reviews are not a shared format freeze.

## 18. Sources, evidence limits and next action

This edition starts from revision 1 at BindingMT
`204f8120e60be4ac7b6272b46afc940c5ab703a2`, the three original #112 contributions
and the three follow-up comments linked above. Referenced owner design baselines are
TopoMT `3a8ee979db8de6f6345de74558a878bb96ba3234` and PharmacophoreMT
`ecd16946d64dd5cdc64132b026aaf12be2c0ef3a`; these are review/source identities,
not advertised dependency floors or qualified BindingMT integrations.

MolSysMT `ff25f120243319ca9515009b4971e24a2eb0dc22` is an additional inspected
source baseline for its public `Interactions.between_selections` and `to_dict`
contracts. The [query implementation](https://github.com/uibcdf/molsysmt/blob/ff25f120243319ca9515009b4971e24a2eb0dc22/molsysmt/interactions/result.py)
offers explicit exclusivity and analysis-qualified occurrence positions; it is
not an executed BindingMT/PharmacophoreMT handoff or complete owner agreement.

The [TopoMT conceptual contract](https://github.com/uibcdf/topomt/blob/3a8ee979db8de6f6345de74558a878bb96ba3234/devguide/topography_conceptual_contract.md#6-relations-and-spatial-interfaces)
and PharmacophoreMT's [composition](https://github.com/uibcdf/pharmacophoremt/blob/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a/devguide/interaction_composition_workflow.md)
and [native constraint](https://github.com/uibcdf/pharmacophoremt/blob/ecd16946d64dd5cdc64132b026aaf12be2c0ef3a/devguide/native_constraint_semantics.md)
contracts supply their respective meanings. MolSysMT context ownership follows
the finite facts/questions already identified by the
[BindingSite work plan](binding_site_implementation_plan.md#5-p0-coordinate-the-finite-contract-and-inputs),
not an assumed universal descriptor or invalidation observer.

The first edition's owner-issue inspection found TopoMT #60/#61/#62 open and
#194 closed; the new replies keep neutral native adoption distinct from the
offered original-provider route. This is dated review context, not a guarantee of later state
or complete neutral adoption. Refresh exact participating source/native closure
and input/artifact identities before an executed receiving profile.

No runtime implementation, molecular computation, compatibility receiving or
consumer adoption is demonstrated here. Documentation syntax/reference/resource
checks retain their limited scope. Native hypotheses, coordinates and quantities
in the symbolic examples have not been generated or measured.

All three second-round replies support preparing the
[bounded implementation/work plan](binding_interface_implementation_plan.md).
It records the supplied exact contact/empty/failure controls, these persistence
and declaration-example clarifications, proposed first-profile decisions and
independent receiving increments. Next close the minimal local data contract,
coordinate the actual molecular/profile prerequisites and obtain the promised
native/consumer inputs. The useful
BindingSite core under #111 remains independent unless a concrete incompatibility
is identified and explicitly resolved.
