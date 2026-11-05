---
summary: Assess DockingMT technical correctness, scientific approach and improvement priorities
issue: uibcdf/dockingmt#28
status: partial
opened: 2026-11-04
closed:
severity: medium
verification: inspected
area: [architecture, science, validation, documentation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Technical and scientific library audit — 2026-11-04

Requested by the maintainer on **2026-11-04**. Reviewed repository head:
`07fc26920fcee0e00b204867a985820a8215b1cd`.
Coordination: [DockingMT #28](https://github.com/uibcdf/dockingmt/issues/28).
Scientific/profile follow-up belongs to [#33](https://github.com/uibcdf/dockingmt/issues/33),
and evidence presentation to [#29](https://github.com/uibcdf/dockingmt/issues/29).
This dated audit supports the existing [#28 work record](pending_proposals/review_extensibility_and_performance.md);
it is not a second independently closable queue item. The requested review and
its same-day methodological expansion are recorded here. This is a bounded
technical and scientific assessment, **not an exhaustive audit or certification
of all library behavior**. `partial` describes the owning work and outstanding
follow-up, not a new acceptance gate.

## What

Assess whether DockingMT is technically sound, scientifically appropriate for its
declared purpose, progressing in the right direction, and where improvement would
provide the most value. This records the audit discussed with the maintainer;
recommendations remain proposals rather than executed fixes or approved experiments.

**Verdict:** DockingMT has a serious technical foundation and a sensible scientific
approach. Its strongest demonstrated contribution is traceable, inspectable docking
within explicit supported profiles. General predictive performance is not yet
established. The next emphasis should be usability, compatible public distribution
and broader bounded scientific evidence, rather than another engine or abstraction.

| Dimension | Assessment at the reviewed head |
| --- | --- |
| Purpose and architecture | Appropriate for the molecular docking layer of MolSysSuite. |
| Technical correctness | Substantial evidence within qualified input and dependency profiles; no blanket defect-free claim. |
| Molecular ownership | General molecular operations predominantly delegated to MolSysMT; a documented partial/external pose verifier remains. |
| Experimental practice | Explicit hypotheses, informative controls, retained failures and separate sampling/ranking observations. |
| General predictive performance | Insufficiently established across independent complexes and preparation choices. |
| Usability and distribution | Less mature than the technical core; current and historical instructions need clearer separation. |

## How

The review inspected the scientific scope/model, validation strategy, roadmap and
Core acceptance map; principal preparation, Vina execution, result, scoring and
evaluation code; representative molecular-delegation, backend and score-contract
tests; retained experimental and installed-package receipts; and open owning issues.
It also consulted the primary Vina and PoseBusters documentation linked below.

This was a read-only code/document/evidence review, not an exhaustive line-by-line
audit. It ran no new tests, molecular preparation, docking, RMSD campaign or visual
session. Previously executed test counts and scientific outcomes below retain their
original producers and compositions. The documentation work recording this audit
does not convert those receipts into tests of a new source head.

The same-day expansion additionally inspected representative numerical and
reference controls in `test_redocking_evaluation.py`,
`test_1iep_conformer_workflow.py`, `test_5x72_root_order_workflow.py` and
`test_vina_output.py`. It adds evidence classification, experimental-design review
and proposed decision rules; it does not add measured outcomes.

### Audit coverage and confidence

The unit of assessment is a claim within a declared workflow, not the library as
an indivisible pass/fail object. In the tables below:

- **Observed** means directly inspected code, instructions or a retained receipt.
- **Supported within profile** means named evidence supports that bounded claim.
- **Unestablished** means the reviewed evidence does not justify the broader claim;
  this is not evidence that the capability is impossible or necessarily incorrect.
- **Proposed** identifies future work with no execution or scientific acceptance.

Confidence is strongest for explicit code/document contradictions and recorded
finite outcomes. Judgments about generalization, usability and development balance
are qualitative. This review does not quantify defect prevalence, audit every test
oracle, measure user effort or independently reproduce the complete benchmark.
There was no new cross-platform, performance, security or browser audit.

Relative links below are navigation aids. Historical source inspection is anchored
to [the reviewed Git tree](https://github.com/uibcdf/dockingmt/tree/07fc26920fcee0e00b204867a985820a8215b1cd);
experiment and artifact records retain their own older producers. Live provider
issues and external documentation describe the context consulted on 2026-11-04,
not immutable proof of later availability. Future revisions should append dated
dispositions rather than silently upgrading this audit's evidence.

## Claim-to-evidence matrix

This complements, rather than replaces, the criterion-by-criterion
[Core acceptance map](CORE_MVP_STATUS.md).

| ID / scientific or technical claim | Evidence inspected | Assessment and limit | Evidence needed for a stronger claim |
| --- | --- | --- | --- |
| E1. Submitted inputs and returned atoms retain their declared correspondence. | [Prepared reader contract](validation/prepared_pose_reading.md), actual export/map binding and [reader tests](../tests/test_prepared_pose_reading.py). | Supported within the complete single-state known-source profile; partial/external paths retain a separate verifier. Equal counts or hashes alone do not prove chemical identity. | Provider delivery and receiving for the missing partial/reference profiles, including malformed and mismatched inputs. |
| E2. Molecular pose reconstruction preserves available identity and geometry. | [Reconstruction contract](validation/flexible_reconstruction.md) and [delegation tests](../tests/test_molecular_delegation.py). | Supported for the retained mapped representation; absent PDBQT chemistry and omitted atoms are not recovered. | A separately qualified provider persistence/reconstruction contract for any richer claim. |
| E3. The adapter preserves backend scores, units and executed settings. | [Native-output tests](../tests/test_vina_output.py), [score semantics](validation/score_semantics.md), external 1IEP observations. | Supported for inspected Vina/Vinardo paths and recorded versions; not proof that the score estimates experimental affinity. | Exact-input differential receiving for any changed backend/version or new scoring mode. |
| E4. Saved results can be inspected and recovered without changing their scientific identity. | [Installed inspection](validation/installed_result_inspection.md), [prepared recovery](validation/prepared_recovery.md), linked case records. | Supported bounded recovery; detached JSON is not a complete molecular snapshot or guaranteed re-execution. | Actual broader user recovery requirements and provider-owned molecular persistence. |
| E5. The workflow can generate a pose close to an experimental reference. | Registered 3PTB and external 1IEP observations; mixed 5X72 outcomes. | Demonstrated in particular cases, not an estimated general success rate. | Prespecified independent-complex panel with explicit preparation, initial-conformation and metric strata. |
| E6. The first returned pose is reliably the scientifically relevant pose. | 3PTB first-pose recovery; 5X72 P59 returned-set recovery without first-pose recovery. | General reliability unestablished; generation and ranking demonstrably differ in this corpus. | Separate top-1/top-k/any-returned measurements and ranking diagnostics over a common admitted cohort. |
| E7. Preparation choices are chemically and biologically suitable. | [Declared profile](validation/preparation_profile.md), named assignment reports, charge/map controls. | Traceability and representation admission are supported; environmental state/model suitability remains unassessed. | Scientifically justified alternative hypotheses, independent reference review and controlled sensitivity studies. |
| E8. A recovered pose is physically plausible. | Explicit graph/stereo admission in selected cases, mapped positional RMSD, optional provider symmetry evaluation. | No systematic output-plausibility acceptance across the corpus is established by this audit. Input stereo checks alone do not qualify every output. | Provider-backed output chemistry/geometry/contact checks with known positive and adverse controls and documented applicability. |
| E9. Scores rank different ligands, affinities or binders correctly. | Named score semantics and within-result ranking APIs. | Unestablished; those APIs and redocking observations are not a screening or affinity benchmark. | A separately scoped experimental dataset, appropriate negatives/metrics and a justified comparison/calibration protocol. |
| E10. Ordinary users can install and use the complete supported workflow. | Full private installed qualification and [failed public Viewer receiving](validation/public_viewer_receiving.md). | Private composition supported; complete public composition and actual frontend behavior remain separate unresolved boundaries. | Compatible public artifacts, actual candidate/platform gates and deferred end-to-end visual observation. |
| E11. Multiple backends or molecular-landscape guidance improve results. | Backend contracts and [scientific horizons](SCIENTIFIC_HORIZONS.md). | Architectural intent only; no comparative improvement claim is established. | A concrete accepted workflow, real provider/backend support and controlled comparisons against a simple baseline. |

## Why: findings and evidence

### A1. The purpose and architectural separation are sound

Problem, protocol, domain and result objects preserve scientific meaning beyond
Vina files. Separating domain, guidance and constraints is appropriate. The current
adapter rejects unsupported nonempty guidance/constraints instead of silently
executing a different scientific question. Named score semantics and preserved
ranking history are useful protections against comparing unlike quantities.

Backend independence is currently an architectural provision, not a claim tested
through a second real engine. Adding an engine is not required merely to prove the
abstraction. The [scientific scope](SCIENTIFIC_SCOPE.md) correctly postpones that
expansion until a concrete workflow needs it.

### A2. Technical evidence is substantial but composition-specific

Identity maps, quantity conversion, serialization, recovery, incompatible-score
refusal and provider-error propagation have meaningful guards. The latest
[full private installed receipt](validation/installed_support_receiving.md) records
**1,450 passing tests**, zero failures/errors/skips, on Linux/Python 3.14.8 with
specified private consumer/provider artifacts. Its test/helper source is
`3bf7abf5a72609f70ab730989a666f64a36585e7`; the consumer wheel producer remains
`50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9`.

Those are software tests, not 1,450 independent scientific cases. They do not
qualify arbitrary public dependency versions or unexecuted platforms. The
[Core map](CORE_MVP_STATUS.md) appropriately separates implemented behavior,
scientific evidence, installed qualification and deferred visual acceptance.

### A3. Molecular ownership is largely implemented, with an explicit remainder

The inspected paths use public MolSysMT for molecular conversion, selection,
coordinate modification, hydrogen projection, bond classification, native PDBQT
export and geometry. DockingMT retains docking choices and orchestration.

The partial/external PDBQT pose-order verifier remains a bounded local exception
under [#49](https://github.com/uibcdf/dockingmt/issues/49), pending the applicable
[MolSysMT #521](https://github.com/uibcdf/molsysmt/issues/521) contract. Complete
single-state known-source poses already use the provider reader; provider failures
do not fall back to local parsing. See [prepared pose reading](validation/prepared_pose_reading.md).
Finish that migration through provider delivery rather than expanding the verifier.

### A4. Positive and negative scientific evidence are both retained

The registered [3PTB experiment](validation/3ptb_search.md) attempted 24 searches
and returned 167 poses. Both native-box torsion arms recovered a near-reference
first pose in their six rows; displaced boxes recovered none. These are repeated
conditions of one complex and one declared chemical hypothesis. A displaced box
is a spatial control, not a nonbinder or a virtual-screening specificity test.

The [5X72 challenge](validation/5x72_root_order_workflow.md) is informative in the
opposite direction. P59 produced near-reference poses in some returned sets but
none ranked first; P69 did not meet the registered recovery criterion in any
returned set. The preserved population contains 24 searches and 99 poses.
These observations distinguish returned-set sampling from ranking without
isolating the physical cause or establishing general recovery probabilities.

The [181L baseline](validation/181l_redocking_exploratory.md),
[external 1IEP check](validation/1iep_external_pdbqt.md) and subsequent conformer
and representation challenges add useful evidence with different purposes.
They should not be pooled as if they shared preparation, metrics and populations.
The current corpus demonstrates bounded behavior and failure analysis, not a
broad benchmark of predictive accuracy, affinity or screening enrichment.

### A5. Preparation integrity and scoring relevance need clearer separation

DockingMT's molecular preparation requires complete finite partial charges. That
can be defended as an explicit representation/provenance policy. It must not be
presented as proof of improved Vina predictions: Vina's documented scoring ignores
user-supplied partial charges, and its documentation says charge assignment is not
needed for Vina/Vinardo. See the [Vina FAQ](https://autodock-vina.readthedocs.io/en/stable/faq.html)
and [official introduction](https://autodock-vina.readthedocs.io/en/latest/).

Distinguish object integrity, PDBQT representation requirements and inputs actually
used by each scoring function. This recommendation does not remove the current
charge contract, authorize fabricated zeros, or equate partial charges with
protonation. Protonation and donor/acceptor representation remain scientifically
relevant. Successful field coverage and charge conservation do not validate a
chemical hypothesis or scoring model.

### A6. User-facing scientific choices and documentation need refinement

Rigid ligand preparation is the default unless torsions are explicitly selected.
That is a controlled choice, but users should see it before interpreting a run as
flexible docking. Similarly, `assess_preparation` examines declared metadata; its
`unassessed` result is not chemical validation. Surface effective flexibility,
chosen states, excluded receptor components and assessment limits clearly.

Two concrete documentation inconsistencies were observed at the reviewed head:

- [VinaProtocol](../dockingmt/core/protocol.py) still describes
  `allow_provisional_preparation` as permitting temporary zero-charge/heuristic
  typing generation. Those generation mechanisms have been removed; historical
  provisional-input inspection/opt-in has a different meaning.
- The root [README](../README.md) presents historical 181L record/replay commands
  without the prominent current-code restriction documented in the
  [baseline](validation/181l_redocking_exploratory.md). That baseline states that
  raw-PDB replay now refuses absent named assignments. Some README prose also
  treats the original #5 mechanism as unresolved after its closure.

These are inspected documentation defects, not demonstrated numerical errors.
Correct current guidance while preserving historical evidence. A short current
user route should lead to detailed contracts and archives, instead of requiring
the user to reconstruct current behavior from successive checkpoints.

## Prioritized findings and risks

Priority refers to the proposed order of response, not a measured probability of
failure. **P1** deserves attention before broad user/scientific claims; **P2**
should shape the next bounded development slice; **P3** is a conditional horizon.
An unknown is not promoted to a confirmed software defect.

| ID / priority | Classification and basis | Consequence | Disposition / owner |
| --- | --- | --- | --- |
| R1 / P1 | Confirmed documentation defects: A6, directly inspected. | Users can misunderstand provisional opt-in or follow an incompatible historical recipe. | Correct current instructions and verify the documented route; preserve original historical instructions in their dated context. #28/#33. |
| R2 / P1 | Measured integration limitation: specific public Viewer receiving failed; public molecular delivery is separately unresolved. | Private qualification cannot serve as a general installation promise. | Receive covering immutable artifacts and qualify the complete public composition. #30/#47 and existing provider issues. |
| R3 / P1 | Scientific evidence limitation: few independent complexes with heterogeneous purposes and protocols. | Overstated recovery or ranking claims, particularly if seeds/poses are counted as independent systems. | Keep claims bounded; prespecify a panel and analysis plan before broader conclusions. #33/#29. |
| R4 / P1 | Interpretation risk: preparation completeness, partial charges and score units can be mistaken for physical validity. | Users can overinterpret an admitted calculation or score as a validated model or affinity. | Explain representation versus scoring requirements and preserve `unassessed`; do not relax current contracts through this audit. #33. |
| R5 / P2 | Known ownership exception: local verifier for remaining pose-reading profiles. | A growing downstream molecular implementation could drift from MolSysMT. | Keep the bounded exception and receive MolSysMT #521 before removing covered code; no expanded local parser. #49. |
| R6 / P2 | Validation gap: complete output plausibility has not been systematically qualified here. | Positional recovery may conceal a chemically or geometrically unsuitable pose. | Inventory provider checks, define applicability and controls, then assess outputs without repairing them silently. #33/#49. |
| R7 / P2 | Qualitative usability risk: effective flexibility and assessment limits require substantial reading. | An apparently simple run can answer a different question from the user's intended flexible/state-aware experiment. | Expose actual scientific choices in the existing workflow; measure user friction before designing another abstraction. #28/#4. |
| R8 / P2 | Qualitative development-balance risk, not a measured cost regression. | Maintenance/evidence machinery could consume effort without increasing scientific knowledge or usable workflows. | Require each new mechanism to serve a concrete user question or observed failure; reuse present APIs and report scientific outcomes. #28/#29. |
| R9 / P3 | Deliberate scope limitation: richer guidance, receptor ensembles and new engines are horizons. | Premature implementation would expand unsupported scientific claims and coupling. | Activate only for a defined question, provider contract and discriminating experiment. #28 with the responsible providers. |

## Independence of checks and test oracles

Tests are not all evidence for the same proposition. The inspected sample supports
the distinctions below; a full inventory of all 1,450 test oracles was not performed.

| Check family | What is independently constrained | What remains shared or untested |
| --- | --- | --- |
| [External 1IEP PDBQT control](validation/1iep_external_pdbqt.md) | Upstream prepared inputs and direct Vina observations constrain adapter projection and normalization. | The reference engine is the same; this does not independently validate Vina physics or DockingMT's molecular preparation. |
| [5X72 workflow tests](../tests/test_5x72_root_order_workflow.py) and [1IEP conformer tests](../tests/test_1iep_conformer_workflow.py) | Explicit NumPy RMSD recomputation checks numerical geometry independently of the provider's RMSD implementation; reference/atom-map checks are retained separately. | The recomputation still consumes the declared map/reference. It cannot prove that the chosen chemical hypothesis or reference population is scientifically appropriate. |
| [Evaluation controls](../tests/test_redocking_evaluation.py) | Known translations, permutations, malformed inputs and changed unit policies constrain correspondence and reporting behavior. | Synthetic geometry does not estimate experimental pose recovery. |
| [Native-output capture](../tests/test_vina_output.py) | Captured actual Vina energy output is checked against retained/serialized values. | It validates transport and meaning preservation, not independent accuracy of native energies. |
| Serialization, hash and round-trip controls | Changes, corruption, detachment and declared identity mismatches are detectable. | A writer and reader can share an incorrect assumption; equal bytes or round trips do not establish physical truth. |
| Provider-delegation and refusal controls | Calls reach the correct owner, and unsupported intent or provider failures do not silently fall back. | A mocked response proves orchestration only. Real provider receiving is still necessary. |
| Installed origin/payload checks | The executed packages and declared inputs are the intended artifacts. | Authentic artifacts can still implement an unsuitable scientific model. |

For follow-up, review critical invariants rather than maximizing test count. Where
feasible, compare them with an independent external reference, a simple analytical
control or a deliberately corrupted input. Do not create a second production
molecular implementation as an oracle. Independent small test calculations have a
different role from reusable scientific routines, which remain provider-owned.

## Experimental-design assessment

The existing registered populations, retained adverse outcomes and immutable
references are strengths. The following boundaries must be preserved or made
explicit in any expanded validation:

| Design question | Current evidence / concern | Required treatment in a new study |
| --- | --- | --- |
| Case selection | 3PTB was prospectively selected; other cases include upstream tutorials and diagnostic controls. Their combined corpus is not a representative sampling design. | Freeze inclusion/exclusion reasons before outcomes; include admitted failures and distinguish development cases from untouched evaluation cases. |
| Initial conformation | Bound-like rigid cases primarily test placement/orientation. The existing [1IEP alternative-conformer challenge](validation/1iep_conformer_workflow.md) already probes a different difficulty. | Report bound-conformation and independently prepared/perturbed-conformer strata separately; never replace the experimental reference with the perturbed input. |
| Receptor and chemical state | The 3PTB dry receptor and declared ligand/residue states are hypotheses. 5X72's experimental co-occupancy differs from its single-ligand search context. | Record excluded waters/cofactors/occupants and state assumptions; do not interpret these experiments as isolating their effects. |
| Search-domain knowledge | Native boxes use known site information; displaced boxes test a spatial negative control. | State that local redocking supplies site knowledge. Blind docking and nonbinder discrimination require different questions and controls. |
| Metric and symmetry | Existing cases use different cutoffs and positional atom populations; optional symmetry evaluation has its own provider admission. | Freeze frame, atom population, map, cutoff and symmetry policy. Report continuous RMSDs as well as threshold decisions; do not change correspondence to rescue a result. |
| Sampling and ranking | Some cases generate a close pose without ranking it first. | Separate generation, ordering and output filtering. Record requested/returned counts and energy-window/clustering settings. “Any returned” is not all poses visited internally. |
| Replication | Seeds and effort levels repeat a complex, not independent biology. Related ligands/receptor structures may also be correlated. | Keep within-case variability separate from between-case evidence; define the independent analysis unit and any uncertainty method before execution. |
| Failures and denominators | Existing receipts preserve admission, search and reporting failures distinctly. | Report selected, admitted, attempted, completed and evaluated counts. Keep failed/unknown evaluations distinct from observed nonrecovery; never drop failed cases to inflate a rate. |
| Comparisons and tuning | Diagnostic representation changes can affect a stochastic search. | Predeclare paired inputs and budgets, changes allowed, tolerances and endpoints. Reserve separate cases for evaluating choices tuned on development cases. |

No defensible sample size, uncertainty interval or universal success threshold can
be inferred from the current audit alone. A future design should justify these
against its intended claim and feasible resources. Any small panel remains a bounded
pilot unless its sampling and size support a stronger inference.

## Scientific growth: questions and decision rules

DockingMT can grow scientifically by improving knowledge of current workflows,
comparing explicit molecular hypotheses, and eventually testing information-guided
protocols. These are research proposals, not promises of better prediction.

| Question / stage | Proposed comparison and measurements | How the result would guide a decision |
| --- | --- | --- |
| Q1. Is a changed outcome introduced by the adapter or already present in Vina? Immediate diagnostic. | Feed identical authenticated prepared bytes, box and resolved options to the adapter and direct backend under a controlled version/seed; compare poses, score components and mapping within predeclared precision expectations. | A discrepancy attributable to the adapter requires correction before interpreting it scientifically. Agreement supports interface fidelity only; it does not validate the preparation or scoring model. |
| Q2. Is the current failure mainly in returned-pose coverage or ranking? Near-term scientific panel. | For fixed declared preparations, measure any-returned, top-1/top-k, continuous RMSD and failure stage across prespecified seeds/effort. Use the same evaluation population and retain all cases. | If close poses repeatedly appear but rank poorly, prioritize ranking/model diagnosis. If none are returned, investigate sampling, preparation and filtering; absence alone does not uniquely identify inadequate search. |
| Q3. How dependent are results on starting conformation and preparation hypotheses? Controlled follow-up. | Hold the reference and comparison protocol fixed; vary one justified conformer/state decision at a time, with provider-owned generation and equivalent budgets. Retain admissibility failures and per-state results. | Robustness supports only the examined range. Strong sensitivity should narrow recommendations and make the relevant choice visible; it does not identify the experimentally correct state. |
| Q4. Does geometric recovery also satisfy applicable plausibility checks? Near-term provider-led assessment. | Evaluate the same retained poses with declared chemistry, geometry and clash checks; use known valid/adverse controls and report unavailable checks separately. Preserve original poses and scores. | If low RMSD and plausibility disagree, report both and restrict the claim. Missing molecular information means unassessed, not pass. Any repair/refinement becomes a separate attributed operation. |
| Q5. Does a receptor/state ensemble add useful coverage beyond spending more search effort? Later accepted workflow. | Compare prespecified state sets with a single-state baseline at a declared comparable total budget, including preparation overhead. Report per-state performance and aggregation choices. | Better results only under a larger budget do not establish an ensemble-specific benefit. A minimum docking score across states is not a state population or calibrated binding free energy. |
| Q6. Does topographic, pharmacophoric or flexibility information improve a docking protocol? Research horizon. | Compare a concrete information-guided protocol against a simple baseline; remove each information source separately, account for total cost, and evaluate on cases not used for tuning. | Accept a bounded benefit only for a prespecified meaningful improvement without unacceptable failures/cost. If the benefit disappears under budget matching or held-out evaluation, restrict or abandon that approach. |

For Q5/Q6, document what “comparable budget” means: time/hardware, number of engine
calls, or another justified resource measure. Report overhead rather than hiding it.
No numerical superiority threshold is selected by this audit. The design must choose
its endpoint, meaningful effect and decision rule before seeing the evaluation data.

The current Vina adapter rejects nonempty guidance/constraints. A future box-selection
or postprocessing procedure must be described as such; it must not be advertised as
native guided sampling. Actual search bias or constraints require supported backend
semantics and their own qualification.

### Ownership of scientific growth

| Responsibility | Owner and DockingMT's role |
| --- | --- |
| Molecular states, conformers, identity, transformations and general geometry/characterization | MolSysMT; DockingMT consumes explicit systems, reports and maps and organizes docking comparisons. |
| Pharmacophoric features and reusable pattern operations | PharmacophoreMT; DockingMT specifies how an accepted protocol consumes them. |
| Pocket/topographic descriptors | TopoMT; DockingMT records their use in domain selection or a supported protocol. |
| Reusable flexibility models | ElastNetMT and the relevant molecular providers; DockingMT defines the docking question and comparison. |
| Docking execution, supported backend semantics, ranking interpretation and study reports | DockingMT, using provider contracts and retaining scientific limitations. |
| Generic viewer rendering and communication | MolSysViewer; DockingMT retains its docking-specific addon and presentation. |

These are responsibility boundaries, not a claim that every future provider tool
already exists. Inventory existing APIs before proposing new capabilities and file
missing reusable work in the owning repository. Do not expand the first release
scope of a provider merely to satisfy a speculative DockingMT horizon.

## Proposed follow-up and acceptance criteria

The order below is a recommendation. It does not replace the operational roadmap,
register a new experiment, select a release, or reopen completed provider work.

| Priority | Proposed action | Observable completion and owner |
| --- | --- | --- |
| 1 | Reconcile current documentation and scientific decision visibility. | Current protocol descriptions and runnable examples agree; rigid/flexible and unassessed meanings are explicit; historical commands are labelled. #28, with #33 for scientific wording. |
| 2 | Qualify a compatible public installation. | Covering provider artifacts are received and actual dependency/candidate gates pass. #30/#47; public Viewer #294 and MolSysMT #334 retain provider ownership. Private success alone is insufficient. |
| 3 | Design a small independent scientific panel within the admitted profile. | Prespecified cases, preparation hypotheses, comparison population, cutoffs, seeds/effort and failure accounting; separate any-pose and first-pose recovery. Review under #33 before execution. |
| 4 | Complement RMSD with molecular plausibility evidence. | Define useful stereo/geometry/clash checks and their interpretation; inventory existing MolSysMT tools and propose missing reusable capabilities there before integration. #33/#49. |
| 5 | Publish a concise synthesis of existing and future validation. | Readers can distinguish software regression, scientific cases, independent complexes and evidence limits without pooling incompatible observations. #29. |

For the proposed panel, choose complexes before observing DockingMT outcomes and
include variation in flexibility and chemistry within the supported scope. Treat
seeds as within-complex variability, not additional independent complexes. Distinguish
bound-conformation rigid redocking from independent-conformer recovery, reusing
existing conformer challenges and public evaluation APIs. Do not tune cases or
cutoffs after inspecting favorable outcomes.

Unaligned positional RMSD is appropriate in a shared receptor frame, with explicit
atom correspondence. It is not sufficient by itself to establish physical
plausibility. [PoseBusters](https://posebusters.readthedocs.io/en/latest/) provides
a primary documented precedent for complementary stereochemistry, bond geometry,
clash and overlap checks. This is methodological inspiration, not an adopted
dependency or a proposal to implement those molecular algorithms in DockingMT.
General characterization belongs to MolSysMT; pharmacophore-specific needs belong
to PharmacophoreMT. DockingMT owns docking interpretation and reporting.

### Concrete work packets and completion evidence

The packets make the recommendation actionable without authorizing their execution
through this document. Dependencies and provider availability determine scheduling;
the operational roadmap remains authoritative.

1. **Current user path and wording (#28/#33):** inventory current examples and
   historical commands; correct R1 and explain R4/R7 in the existing workflow.
   Completion requires consistent public descriptions and a documented, applicable
   installed route, with its actual execution evidence or an explicit delivery
   blocker. Do not claim general ease of use without user observation.
2. **Public compatibility (#30/#47):** receive the covering provider files and
   qualify the actual combination and existing candidate gates. Completion is
   artifact-specific passing evidence, not a version string, symbol inventory
   or successful private composition. The visual gate remains separate.
3. **Scientific panel design (#33):** specify Q2 and, if justified, a bounded Q3
   comparison; list frozen sources/cases, states, correspondence, reference,
   protocols, metrics, budgets, failure handling and analysis units. Record the
   owner-reviewed design before execution. A completed design is not a completed
   experiment; execute and interpret under a separate recorded population.
4. **Plausibility inventory and proposal (#33/#49):** identify available provider
   checks, missing chemistry and proposed outputs. Register missing reusable tools
   in MolSysMT (or the specific provider) before any downstream implementation.
   Completion of this packet is an explicit applicability/ownership plan; actual
   molecular and scientific qualification follows separately.
5. **Evidence synthesis (#29):** publish the E1–E11 distinctions with a compact
   case/protocol/outcome/limit table linking original records. Completion requires
   reproducible provenance and explicit failures/denominators, not a new website
   or another copy of every historical artifact.

Reassess this audit after these packets or a material provider/backend/profile
change. Record which risk was reduced, which claim gained evidence and which
uncertainty remains. Neither additional metadata nor increased test count alone
is a scientific progress criterion.

## What was refuted

- Passing the software suite does not establish general predictive accuracy.
- Repeated poses/seeds from one complex are not independent validation complexes.
- A low docking score or successful redocking does not measure binding affinity.
- The existence of failures in 5X72 is not by itself an adapter defect; the
  recorded experiment does not isolate sampling, scoring and preparation causes.
- Complete metadata, charge conservation and successful parsing are not chemical
  or biological validation.
- A second engine, a new molecular helper or a broad redesign is not justified
  merely by the architectural horizon or this review.

## Scope and exclusions

The intended starting scope remains one declared small-molecule state, a rigid
protein, explicit preparation and box choices, and Vina, with a rigid or explicitly
cut ligand. No general receptor flexibility, water/metal model, screening accuracy,
affinity calibration or landscape-aware method is accepted by this audit.

Public readiness remains distinct from the qualified private composition; the
[public receiving record](validation/public_viewer_receiving.md) documents the
actual incompatible Viewer file. Issue comments reviewed on this date did not
provide a new covering delivery; this audit did not repeat a package-registry
inventory. Visible C4/C6 observation remains deferred under #52/#60.

No runtime, dependency, original experiment, producer identity or existing gate is
changed. This dated assessment should remain readable as evidence at the stated
head; subsequent implementation and qualification should be linked separately.

## Follow-up 1 — current instructions and scientific choices, 2026-11-04

After completing the audit, the maintainer requested implementation of its
improvements. This first bounded slice addresses R1 and the documentation portions
of R4/R7. The findings above retain the reviewed `07fc269` state; this is a later
disposition, not a rewrite of that evidence or completion of all work packets.

- The root README now starts with the four existing installed walkthroughs and
  states which ones prepare, search or only inspect/evaluate saved data. It names
  the private-composition/public-delivery boundary and the declared rigid/dry case.
- `VinaProtocol` now describes provisional opt-in as acceptance of supplied
  provisional declarations, not generation of removed placeholder chemistry.
  Its flexibility documentation distinguishes automatic preparation from supplied
  prepared/PDBQT torsion trees. The README torsion example no longer requests
  unnecessary provisional opt-in.
- `assess_preparation` and the README explicitly distinguish absent provisional
  markers from positive chemical validation. The README separates the complete-
  charge representation contract from the charges used by Vina scoring, without
  changing preparation requirements.
- Historical raw-PDB 181L replay and default profiling commands are no longer
  presented as the current preparation route. Their original records remain
  untouched, and scientific follow-up points to #33 rather than reopening #5.

Validation of this slice: **104 existing tests pass**, zero failures/skips,
19.30 s, in the routine editable Python 3.14.7 environment. Selection:
`tests/test_protocol.py`, `tests/test_preparation_assessment.py`,
`tests/test_backend_contracts.py`, `tests/test_required_partial_charges.py` and
`tests/test_required_autodock_types.py`, using `--receptor=llm`. Fourteen
`StructuralAttributeOffAxisWarning` warnings remain visible. Ruff lint/format
checks pass. AST comparison against `07fc269`, excluding docstrings, verifies
unchanged executable statements in both edited Python files.

These are source contract checks, not a repeated private installed qualification,
new benchmark or notebook/visual execution. Python file bytes changed through
docstrings; original wheel bytes/receipts are not rebound to this source. The
routine environment's installed version metadata may lag its editable source.

Documentation indexes and diff checks pass; 246 relative links resolve across the
six edited Markdown documents. All 570 declared installed-support source digests
remain unchanged. Shared SDK `95f693be` publication-contract and noarch resource
preflights pass in the separate minimal administrative environment. These commands
validate the example plan only; no actual candidate, package build or release is
created. Committed-export and hosted observations belong to the #28 closeout.

`pip check` exits 1 for the seven already-owned shared-environment requirements:
missing `pdb2pqr`, NumPy ceilings in `ndfes`/`edgembar`/`fetkutils`/`proprep`, and
the `proprep` Biopython ceiling. This matches the existing
[MolSysSuite #82 ownership record](https://github.com/uibcdf/molsyssuite/issues/82#issuecomment-6595036857).
The passing selection does not certify clean environment closure. No environment,
provider or scientific artifact is repaired, replaced or relabelled here.

R1's two inspected documentation defects are corrected in this slice. User
observation for R7, broader scientific wording/model acceptance under R4, public
receiving, the panel design and provider plausibility inventory remain open.
No new acceptance threshold, molecular implementation or experiment is introduced.

## Follow-up 2 — scientific design and provider inventory, 2026-11-04

The [small-panel design](validation/scientific_panel_design_2026-11-04.md)
addresses the planning part of Q2/Q3 and R3/R6: two named public candidates,
separate historical case roles, explicit admission decisions, a proposed maximum
of 24 searches, per-case recovery/ranking endpoints and preserved failure
denominators. Its proposed 2-angstrom criterion is not a reinterpretation of
historical results. Input acquisition, molecular admission, chemical hypotheses,
exact software and resource registration remain pending; this is not yet a
registered experiment or new scientific evidence.

The [molecular plausibility inventory](validation/molecular_plausibility_inventory_2026-11-04.md)
addresses the discovery part of Q4/R6. It separates available MolSysMT coverage,
correspondence, coordinate-CIP and geometry primitives from an unestablished
complete rule-based assessment contract. The reusable missing capability is
proposed in [MolSysMT #555](https://github.com/uibcdf/molsysmt/issues/555), with
consumer ownership in DockingMT #33/#49. No local molecular validator, provider
update, calculation or mandatory new dependency is introduced.

These are partial dispositions, not closure of the scientific risks. Next work
is source/assembly/state admission before searching, and provider review of #555.
Unavailable plausibility checks must remain unassessed in any interim scoped
RMSD study. Exact documentation checks and committed-source CI observations are
recorded in the owning issues; previous runtime and installed receipts retain
their original source/artifact identities.

## Follow-up 3 — first source-admission observations, 2026-11-04

The [source-admission record](validation/scientific_panel_admission_2026-11-04.md)
retains four acquired input representations and molecular observations obtained
through public MolSysMT tools, including assembly 1 construction. The observed
45/16-atom ligand populations, terminal missing-residue report for 1STP and
incomplete declared chemical fields make the remaining admission choices concrete.
No case is admitted and no preparation/search/RMSD is executed. A producer JSON
encoding failure and its pre-continuation correction are preserved separately.

Observed CIF occupancy loss is reported in
[MolSysMT #556](https://github.com/uibcdf/molsysmt/issues/556), with no downstream
parser or repair. Explicit chemistry, source/CCD revisions, binding-environment
choices and terminal truncations must be resolved before preparation. This is
progress on Q2/Q3/R3/R6, not scientific recovery or general model acceptance.

## Follow-up 4 — environment observations and template request, 2026-11-04

The [environment/template record](validation/scientific_panel_environment_2026-11-04.md)
adds provider-only water shells, other ligand-copy and observed endpoint distances,
plus before/after coordinate/readiness digests. It exposes missing OXT before
peptide-template application and keeps truncation, waters and states unresolved.
No distance cutoff is promoted to a hydrogen-bond, water-retention or safe-truncation
rule. No chemical completion, preparation or search is executed.

[MolSysMT #557](https://github.com/uibcdf/molsysmt/issues/557) owns the reusable
CCD/template/correspondence request. #555 is owner-triaged for post-freeze study;
#556 occupancy remains separate. Q2/Q3/R3/R6 are still partial, with the concrete
next prerequisite now being supported templates and explicit state/environment
decisions before provider-only completion and application.

## Follow-up 5 — terminal reconstruction receiving boundary, 2026-11-04

One [provider-only terminal software control](validation/scientific_panel_terminal_probe_2026-11-04.md)
adds the two OXT atoms missing from an unadmitted 1HSG protein copy. Source/input
snapshots remain unchanged; the output reorders atoms and diagnoses occupancy/
B-factor loss. A new public completion map/history is not established, so old
output-coordinate preservation remains unassessed rather than reconstructed by
consumer matching. MolSysMT #558 owns the missing provenance contract.

This is one explicitly counted diagnostic molecular reconstruction, not zero
molecular work, an admitted preparation or a new docking outcome. Q2/Q3/R3/R6
remain partial. Receive provider maps and CCD/templates, decide states/environment,
then assess preparation before any search registration.

## Follow-up 6 — reproducible scientific evidence presentation, 2026-11-04

The [evidence overview](validation/scientific_evidence_overview_2026-11-04.md)
delivers packet 5's compact case/protocol/outcome/limit presentation under #29.
A standard-library producer authenticates four existing files and regenerates
ten separate strata with continuous saved-RMSD ranges and first/any-returned
recovery. Original 3PTB reporting failures and later receiving stay distinct;
documented-only 181L/1IEP observations are separated from regenerated records.
No molecular operation, new geometry, native call or scientific case is executed.

This improves discoverability and bounded interpretation for R3/R4/R8 without
adding a website or changing scientific evidence. E1–E11 retain their original
limits. The broader #29 publication/lifecycle decision, provider-dependent panel
admission and public/visual qualification remain open.

## Follow-up 7 — evidence publication decision, 2026-11-04

[DMT-044](DECISIONS.md#dmt-044--publish-evidence-through-a-staged-repository-first-route)
and the [local evidence publication policy](validation/evidence_publication_policy.md)
resolve #29's route/lifecycle decision: repository-first presentation linked from
the root README, one authoritative evidence source and explicit reader, metadata,
maintenance, correction, rerun, retention and reconsideration boundaries. The
comparison with a documentation section and dedicated site records why new
infrastructure is deferred. The resolved report is archived, and directory
instructions carry the accepted evidence-maintenance action.

This reduces the organization/discoverability part of R3/R4/R8. It creates no
scientific measurement, provider workaround, new web service or qualification.
Provider-dependent panel admission and public/visual gates remain open.

## Follow-up 8 — explicit all-returned recovery summaries, 2026-11-04

Current source `summarize_redocking` adds the `any_returned` aggregate under #61,
using validated saved observations and unchanged exact compatibility/top-N rules.
This directly supports E6/Q2's returned-set versus ordering distinction when a
recovered pose appears beyond the largest requested N. Empty evaluated results
and failed cases retain their distinct denominators; absent policy yields null.
No molecular operation, geometry, reranking or seed-pooling policy is introduced.

Six selected pre-implementation controls fail for the missing field. After the
change, 135 existing/new summary and evaluation checks pass in 81.27 s, with
39 LegacyH5MSMWarning and one StructuralAttributeDropWarning retained. These are
source contract checks; prior installed/scientific artifacts are unchanged and
do not inherit the new field. The panel's template/map/state/environment admission,
public delivery and visible C4/C6 remain separate.

## Follow-up 9 — exact-input native interface fidelity, 2026-11-04

The [#62 control](validation/vina_adapter_fidelity_2026-11-04.md) addresses Q1/E3
with one adapter and one independently prescribed direct Vina invocation, using
authenticated captured 3PTB bytes. Both complete once, returning five poses each
with identical native energies/arrays/PDBQT and matching calls, input hashes,
score projection and provenance. This is two new searches in a separate software
population, not a new preparation, recovery calculation or independent complex.

The first gate fails 14/16 because the newly written observer assumes an abbreviated
unit spelling and filters the wrong temporary-path keys. Its failed summary and
producer remain intact. A separately attributed offline assessment reproduces
that failure, corrects only those observer rules and passes 16 checks with 12
adverse mutations rejected. No search is repeated; all numerical comparisons
remain exact. The new evidence supports this bounded interface question, while
chemical/source mapping, physical/model accuracy, known environment closure,
new panel admission and public/visual acceptance retain their separate limits.
The rigid-only ligand and zero internal/torsional terms do not qualify flexible
or nonzero-term normalization behavior.

## Follow-up 10 — finite real pose-record admission, 2026-11-04

The continuing #19 public-boundary review reproduces a concrete defect in
DockingPose at `8087603`: nonfinite values are accepted, complex values lose
their imaginary part during float coercion, and malformed saved/mutated values
can reach result snapshots. [#63's correction](validation/pose_coordinate_contract.md)
checks numerical schema contents before coercion and after normalization, using
PyUnitWizard for units and the existing local coordinate diagnostic. It adds no
molecular inspection, geometry, matching or repair; MolSysMT retains that work.

Before the fix, 18 new controls fail/four valid cases pass. Afterward all 22
coordinate controls pass within 453 relevant result/evaluation/audit/export/
native-output checks, retaining the 40 warnings in their original selected gate.
Valid schema/units/snapshots and shaped-empty behavior are preserved. These are
new source checks; previous scientific producers and installed artifacts remain
unchanged and do not inherit this correction's qualification.

The bounded four-form probe passes 16 pose roundtrips and nine non-Astropy
protocol-energy pairs, while seven Astropy energy pairs refuse kcal/kilocalorie
parsing. The provider-only reproduction/request is PyUnitWizard #137, tracked
under #19/MolSysSuite #127 without a local alias or caller-policy override. This
is not full public-provider closure or a new molecular/model validity claim.

## Follow-up 11 — actual support-library use and installer guidance, 2026-11-04

The maintainer-requested [comparative review](validation/support_library_review_2026-11-04.md)
checks actual ArgDigest plans, delayed dependency imports, SMonitor wiring and
application-policy preservation, with inspected examples in our sibling clones.
Initial representative tests pass 70 cases and source SMonitor checks pass, but
these do not certify full adoption: public model/factory contracts and preparation/
addon diagnostic coverage still need #19 work. Private model-integrity checks
remain valid and must not disappear merely to move admission into ArgDigest.

The review exposes incorrect member installation advice in DepDigest metadata,
including a test that required an unprovided pip route. #64 explicitly disables
PyPI and selects uibcdf Conda for MolSysMT/Viewer through supported provider fields.
Three corrected controls fail before the fix; 72 selected cases pass afterward.
An unrelated shared scanner false positive for `from .vina import VinaBackend`
is reproduced with absolute/lazy controls and filed as DepDigest #47. No local
scanner workaround, provider copy, molecular operation or scientific run is added.
Our Viewer source delivery is received; its covering public artifact remains #294.

## Follow-up 12 — core model and factory argument contracts, 2026-11-04

The [#19 receiving follow-up](validation/support_library_review_2026-11-04.md#core-modelfactory-receiving-follow-up)
extends ArgDigest to core pose/result/problem constructors and record factories,
BoxRegion factories, the redocking factory and protocol record recovery.
Constructor-specific optional values survive inheritance without weakening
with_scores or dock. Existing pose/box validators supply digesters; independent
mutable-output/schema/ranking checks remain. MolSysMT still interprets molecular
forms, selections, frames and chemical states. No molecular kernel is added.

The original 47 new controls fail 44/pass three before implementation. The final
50-case model module passes, within 477 relevant source cases passing both with
routine providers and verified exact CI ArgDigest/MolSysMT source exports.
Pre-initialization tracing no longer emits local repr summary warnings. A selected
state fixture replaces a removed private charge setter with public msm.set.
These are Python 3.14 source/compatibility checks, not public delivery or complete
support-library/scientific qualification. Prepared constructors, owned view
arguments, diagnostic coverage and dependency audit receiving remain under #19.

## Follow-up 13 — preparation and addon structured diagnostics, 2026-11-04

The [#19 diagnostic receiving block](validation/support_library_review_2026-11-04.md#preparation-and-addon-diagnostic-receiving-follow-up)
adds preparation/addon signals, eight owned Viewer diagnostic identities and
panel error_code state. Catalog wording and typed occurrence fields replace raw
owned errors; existing ValueError/RuntimeError catch families, foreign exception
identities and scientific/molecular delegation are preserved. Expected idle
visual absence stays quiet. Current DOM examples now use emitted refresh states.

The original thirteen controls reproduce twelve failures/one pass; the final
module has fourteen cases. All 264 affected cases pass with the exact existing
ArgDigest/MolSysMT/Viewer CI source pins, plus 21 DOM cases. Forty-four focused
checks pass with routine providers. Fifteen broader failures with older routine
provider clones are independently reproduced on the original DockingMT source;
the selected controlled composition succeeds without changing the scientific pins.
These checks establish neither public/installed delivery nor visual C4/C6.

A provider-only control exposes filtered DEBUG suppressing an outer ERROR under
SMonitor #59. Trace tests explicitly enable DEBUG; ordinary-threshold delivery
for that ArgDigest composition remains unqualified. The issue owns the shared
correction; no local emission-marker or decorator workaround is introduced.
#19 remains partial for that receiving work and remaining argument/dependency
boundaries. Original scientific producers, frozen inputs and installed artifacts
retain their own identities and qualification.

## Follow-up 14 — SMonitor source correction receiving, 2026-11-04

The [#19 source checkpoint](validation/support_library_review_2026-11-04.md#smonitor-filtered-signal-source-receiving)
receives the ordinary nested-signal correction already integrated in SMonitor
main `82dad5a7`. Twenty consumer controls pass on two selected ArgDigest source
generations, versus twenty reproduced failures with the old provider. Ten more
controls pass in the updated routine editable environment. The frozen producer
and receipts preserve exact identities, native exceptions/foreign codes,
metadata-only behavior and application policy without running molecular work.

A separately reproduced callback-emission bug belongs to SMonitor #61 and its
PR #60. The provider maintainer integrates it independently as `5ee88c1`, with
final accepted record/guards at `ccdcace`. That accepted source passes 812 tests
and another ten routine consumer controls. Parallel proposal `11116e2` retains
its distinct 813-source/44-private-installed receipt; the branch is not claimed
merged and no public artifact is qualified. Shared handoffs are MolSysSuite #163
and ArgDigest #49. No public floor,
scientific pin, historical artifact or visual gate changes. #19 continues with
prepared/owned-view contracts and DepDigest #47/inventory receiving; routine
environment closure remains MolSysSuite #82.
