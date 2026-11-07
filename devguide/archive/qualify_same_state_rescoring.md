---
summary: Qualify same-state multi-pose rescoring with explicit reference and comparison evidence.
issue: uibcdf/dockingmt#78
status: resolved
opened: 2026-11-06
closed: 2026-11-07
verification: measured
area: [scoring, provenance, scientific-validation]
guard: tests/test_score_comparison.py
normative:
blocked_by: []
supersedes: []
---

# Same-state multi-pose rescoring

## What

Complete a representative E1 workflow for several existing poses of one
declared ligand state against one rigid receptor, retaining original docking
and named Vina/Vinardo evaluations with explicit comparison/ranking admission.
The [pre-stabilization objective](../PRE_STABILIZATION_PLAN.md) remains broader.

## How

First record native fixed-score reference semantics and inspect supported
molecular tools. Request/receive missing molecular projection and identity
evidence from MolSysMT; then define and execute a bounded registered workflow.
Keep receptor/method/version/state/preparation/grid/weights/reference conditions
explicit and every actual submitted-input hash. Retain missing/refused cases.

## Why

At `530a4cf`, fixed scoring requires a prepared input already matching the pose,
and ranking requires identical declared contexts/state IDs. Distinct input-byte
hashes do not establish chemical equivalence. Vina's current-conformation
reference also differs from docking's shared best-pose convention; merely
comparing equally named numeric columns would conceal that distinction.

## What was refuted

No downstream PDBQT coordinate rewriter, graph fingerprint, molecular matcher
or repair is acceptable. State strings alone do not prove molecular identity.
Removing hashes/editing descriptors cannot establish comparability. No new
generic stage/campaign framework is needed for this bounded workflow.

## Scope and exclusions

Core/Extended functionality targets prospective 0.5.0; 1.0.0 remains after
stabilization. #78 does not accept all E1–E5, scientific accuracy or public/visual
delivery. Preserve fixed candidate `905abc9`, existing receipts and original
scientific producers. Native experiments require a separate declared population
and budget; local qualification remains light, serial and resource-guarded.

## Acceptance criteria

- New reference evidence matches the executed native policy and reported native
  component; legacy records retain their original observations and unknowns.
- Provider-supported projection and identity evidence preserve chemistry,
  source/input/output maps, actual bytes, units and unsupported/partial scope.
- Comparison/ranking admission is justified, explicit, conservative for unknown
  evidence and tested with changed method/state/inputs/reference conditions.
- A registered representative native/installed workflow retains original scores,
  all new named evaluations, failures/denominators, ranking history and detached
  JSON audits, with exact software/artifact/input provenance.
- Appropriate source/installed/scientific gates are executed for their actual
  claims. A planning or metadata slice alone cannot close this report.

## Provider receiving — 2026-11-06

Static inspection uses fetched main `ed09f64539a5af6c1dbe9bd352c7ef65dcd4a7a6`,
separate from qualified runtime pin `00abb958f`. Local sibling worktrees are
preserved behind their remotes; their unrefreshed files are not treated as main.
Public basic tools, `chemical_states.get_atom_correspondences`, PDBQT reading/
writing/maps and existing issues were inspected.

[MolSysMT #599](https://github.com/uibcdf/molsysmt/issues/599) requests a supported
prepared-conformation projection/composition, including partial representations,
map completeness, chemical field/tree preservation and precision/metadata losses.
Existing [#447](https://github.com/uibcdf/molsysmt/issues/447) receives the same-state
identity/equivalence use case; #521 remains the partial/reference reading owner.
These are provider requests, not new-source/runtime acceptance.

## Reference-evidence implementation slice — 2026-11-06

Implementation `49a7729` adds explicit native reference declarations and shared
record crosschecks under DMT-047, preserving public signatures/native numbers,
frozen observations, canonical legacy reports and strict ranking. The
[contract/receiving](../validation/scoring_reference.md) records 155 selected
source tests with the published receptor, one native case deselected, and 106
private installed record tests. Source substituted-engine controls retain the
existing MolSysMT geometry reads; installed guards make zero external-operation/
optional-import attempts. Exact source/wheel/inputs, original base preservation,
warning and initial guard/development-tool diagnostics are retained separately.

This completes one record-semantics slice, not the E1 workflow. Provider
projection/identity, comparison admission and representative native/installed
execution remain required; no molecular implementation is introduced here.

The separate prescribed installed native control executes two fixed-score calls
on the unchanged overlapping software inputs, preserving 16 values/two histories,
original byte identities and unassessed preparation. Its new producer remains
`49a7729`; this is not the representative multi-pose E1 study. Refinement
`36c526c` then rejects nonscalar reference declarations, passes 157 source/108
installed tests and receives the prior native producer with unchanged audit
reports and no new native calls. Both artifacts/receipts and all initial
outcomes remain separate in the linked contract. The routine workspace pip
check retains unrelated known closure gaps; private receiving passes closure.

## New-machine contract review — 2026-11-06

The [source-inspection receipt](../validation/data/e1_provider_contract_review_2026-11-06.json)
records consumer `2fda6238e6b1cb3742f5d30b8ed3af699f9ed748`, the preserved clean
editable MolSysMT `9e1f1b1ad8bf09446374ab6f04ca7208e2717936`, freshly fetched
provider main `34b8c09e267683037045004d1897951da8761d80`, and the separate
qualified pin `00abb958fb93649131d5ce5fe5e12e90cf4900e9`. The installed provider
is five commits behind that main; its checkout and all runtime pins remain
unchanged. All twenty inspected files in the installed checkout equal fetched
main. Five differ from the qualified pin: copy/get/convert, the known-source
pose reader helper, and chemical-graph context handling. Per-file identities are source evidence,
not executed compatibility or a qualified dependency closure.

MolSysMT [#599](https://github.com/uibcdf/molsysmt/issues/599),
[#447](https://github.com/uibcdf/molsysmt/issues/447) and
[#521](https://github.com/uibcdf/molsysmt/issues/521) remain open at this
inspection. That status alone does not establish that every E1 profile lacks a
supported composition. Existing public
tools offer the following candidates; none has been received on the actual
representative E1 inputs by this review.

### Prepared-conformation projection candidate

For a complete prepared native source, retain the actual export view, its
native-axis torsion tree and the completed source-to-written atom map. Copy the
source with `msm.copy`, apply explicitly unit-bearing pose coordinates with
`msm.set(..., element='atom', coordinates=...)` on the admitted native axis, and
export with `msm.convert(..., to_form='string:pdbqt_text',
typing_scheme='autodock4', torsion_tree=..., return_atom_map=True)`. Preserve
the new bytes/hash and map separately from the original input.

DockingMT already composes much of this in
[`preparation/_export.py`](../../dockingmt/preparation/_export.py):
`PreparedExport` retains the actual molecular view and export map, and
`_declared_tree` binds the existing docking tree to native IDs. The public
`pose.to_molecular_system(prepared)` also applies admitted pose coordinates
through MolSysMT, but does not return a newly prepared scoring input. These
pieces are not yet an accepted multi-pose projection workflow.

An original PDBQT tree returned by the provider's `get_torsion_tree` belongs to
the original PDBQT IDs/order. It cannot be attached directly to a differently
ordered native source or to original native IDs after serial presentation has
changed. Retain the correct axis/tree/export relationship; do not infer a map.

For an external/partial PDBQT, public conversion with explicit
`discard_torsion_tree=True`, a separately retained original tree, copy/set and
native export provide a source-inspected representation-preserving candidate.
It keeps partial chemistry partial. Known-source `read_poses` still requires a
complete chemical graph and does not transfer MolecularMechanics; it cannot
stand in for the partial-reference reader in MolSysMT #521. Unknown input
chemistry is not supplied by an export map.

The writer canonicalizes presentation and rounds coordinates in angstrom and
charges in elementary charge to three decimals. Format-level tree and REMARK
metadata are not automatically native molecular state. Preserve their
disposition, available pre-write values and actual output bytes; do not carry
stale score remarks as fresh evaluations or
claim a byte-identical rewrite. The public writer/tree contracts and their
existing negative/roundtrip controls are identified in the receipt.

### Molecular identity candidate and limits

`msm.chemical_states.get_atom_correspondences` already provides a coordinate-
independent `declared_graph_isomorphism` witness. For a complete admitted
chemical context it checks declared elements, isotopes, formal charges,
radicals, H inventory/policy, bond orders/aromaticity and assigned stereo. A
known candidate correspondence can be validated without guessing an atom map.
Retain the complete witness, source/selection/state axes, search coverage and
provider identity. Its digests detect consistency changes; they do not
authenticate that the witness belongs to the submitted scoring inputs.

This may satisfy a bounded complete single-component, same-H-encoding E1
profile without requiring the broader canonical identity/scaffold proposal in
MolSysMT #447. It rejects incomplete/unknown chemistry and does not establish
equivalence between different H encodings or experimental preparation validity. The actual
retained 3PTB source has not passed this admission in the present review.
Partial PDBQT alone cannot establish the full-state equivalence required here.

`basic.compare` compares available attributes and can omit unavailable fields;
matching unknown values does not prove chemistry. It is not the E1 identity
certificate. Graph correspondence also does not establish preservation of
partial charges, AutoDock `atom_ff_type`, assignment provenance or torsion-tree
meaning. Those prepared-representation contracts need separate receiving.

### Comparison admission remains DockingMT work

[`_vina_scoring.py`](../../dockingmt/engines/_vina_scoring.py) retains each
evaluation's actual `partner_sha256` in its context. Different conformations can
also round to identical PDBQT bytes; the hash does not certify their identity.
For explicitly described scoring evaluations,
[`_scores.py`](../../dockingmt/core/_scores.py) deliberately requires identical
definitions, contexts and state IDs for `rank_by`; its existing refusal and the
separate entirely undescribed legacy route remain unchanged. A received chemical
witness does not make different input hashes identical or demonstrate a common
native energy reference. Equal rounded
reference values do not establish a common reference either.

The next comparison design should retain three separate observations:

| Question | Evidence / disposition |
| --- | --- |
| Are the saved records internally consistent? | Existing pose/result audits, with their declared limits. |
| How are the actual submitted inputs related? | Exact per-input identities plus received projection, chemical witness and preparation preservation; distinct bytes may be expected, without proving that only coordinates differ. |
| Is a comparison scientifically admitted? | A declared study question/policy and receptor, method/version/component, units, preparation, weights, box/grid and native-reference evidence; incompatible and unevaluated cases remain explicit. |

Initially record that diagnosis without manufacturing a numerical ranking or
selecting a new public API. Keep original scores, descriptors, hashes and all
evaluation histories. Any later study-level ordering needs its own justified
comparison policy and retained evidence; it must not weaken `rank_by`, drop
input hashes or adjust saved scores to fabricate a reference not executed.

### Next receiving boundary

Prepare a bounded projection/identity receiving prescription using an actual
complete prepared source and saved poses, before native rescoring. Cover rigid
and flexible trees, a nonidentity written/native map, source nonmutation,
charges/types/assignment preservation, explicit coordinate rounding and
nondefault units. Include incompatible/missing/duplicate maps, partial chemical
authority, mismatched state/chemistry and unsupported metadata as refusal or
unassessed controls. Do not silently drop the separately owned partial-input
requirements. Give the existing MolSysMT #599/#447 owners the concrete
composition and remaining contract questions rather than requesting a duplicate
molecular tool.

Only after receiving those boundaries and defining comparison admission should
the representative E1 native/installed population, references, budgets and
failure policy be registered and executed. This review runs zero molecular or
native operations, changes no runtime code and accepts neither E1 nor a new
provider composition. The separate local E4 computational hold remains intact.

## Supplied-reference projection receiving — 2026-11-06

The separately registered
[bounded notebook and receiving](../validation/e1_partial_projection_2026-11-06.md)
now pass on the actual editable development composition: all five saved human
3PTB poses, thirteen atoms each, under normal and pm/fs policies. Ten projected
PDBQT records preserve the checked coordinates, IDs/names/elements, types,
charges, tree, output maps and original pose/score associations. Corresponding
outputs are byte-identical between policies; the enumerated source-field and
original-record nonmutation checks pass.

Six adverse refusals pass: partial reference cannot prove complete chemical
identity, an old tree cannot follow a permuted native axis implicitly, and NaN
geometry cannot be exported. The four registered code cells finish in 14.75 s
with one CPU and sampled peak RSS 204.19 MiB, without a resource interruption.
No new search, score, preparation, H generation or interaction detection runs.
Original producers, captures and observations retain their identities.

This is receiving of the listed fields for a rigid supplied-PDBQT projection,
not a complete native-source or positive chemical-identity result. The inspected
custody set has no directly reusable complete prepared thirteen-atom snapshot;
the later E4 ligand has five added H and cannot silently replace it. Retain
full-source/identity, flexible/nonidentity export, comparison policy and native/
installed workflow admission as outstanding. A newly reconstructed complete
source would need its own declared recipe and producer, not a historical label.
MolSysMT #521 and the remaining #599/#447 contracts stay separately owned.

## New declared chemical authority receiving — 2026-11-06

The [new-authority notebook and receiving](../validation/e1_declared_authority_2026-11-06.md)
now pass under both unit policies. Public conversion of the originally declared
benzamidinium SMILES constructs a new nine-heavy-atom authority with its actual
stored-H/stereo representation. The original template-to-source declaration is
inverted through the explicit public permutation; only coordinates from the
five supplied-reference projections are transferred through public extraction
and copy/set. Historical labels, scores and chemical unknowns remain intact.

Fourteen positive graph witnesses cover ten coordinate variants, two nonidentity
atom maps and two source H5MSM roundtrips. Two carbon-13 controls reject the
incompatible supplied map. The four independent legacy JSON conversion controls
fail at typed preparation-history transport, as prescribed; these are not
chemical identity negatives. The original eighteen-atom snapshot also retains
nine unknown heavy-atom stereo values and lacks MolecularMechanics. No legacy
history codec, metadata filling or source reconstruction is introduced here.

All four registered cells finish in 8.16 s with one CPU, sampled peak RSS
335.16 MiB and no resource interruption. Monitored correspondence calls are
exactly sixteen, each bounded to one supplied candidate. Full witnesses, actual
coordinate checks, source H5MSM files, readiness, native-module identity and
all diagnostics remain in the linked evidence.

The existing correspondence API can satisfy this bounded new-source identity
profile; the open provider issues are not a universal waiting condition. The
new source is not the original prepared thirteen-atom input. Next receive
complete prepared-state chemistry/mechanics and flexible/nonidentity export
boundaries using that explicitly declared authority, then define comparison
admission before representative rescoring. Preserve original producers,
per-input hashes, native reference semantics and strict `rank_by` throughout.

## New-source preparation receiving — 2026-11-06

The [registered preparation notebook and receiving](../validation/e1_prepared_authority_2026-11-06.md)
now receive the new authority through fixed-state H expansion, named
Gasteiger–Marsili charges and AutoDock4 chemical-environment typing. The complete
attempt prepares four views from two eighteen-atom models, one per unit policy:
rigid and explicit one-cut flexible thirteen-atom projections. Each merges five
nonpolar H and retains four polar H, with full-precision charge conservation,
original provider assignments and generated-atom lineage preserved.

Ten bounded chemical witnesses, eight export refusals and two inconsistent
edited-charge audits pass. The flexible writer has an actual nonidentity axis;
the public native writer map binds its own bytes, independently of DockingMT's
remark-bearing export. Rounded PDBQT charges sum to 1.001 e, within the declared
0.0065 e bound, while unrounded totals remain +1 e within provider tolerance.
Corresponding PDBQT bytes agree between unit policies. The complete attempt
takes 9.55 s with sampled peak RSS 311.63 MiB and no resource interruption.

The first attempt remains preserved: it completes one policy and stops on an
overstrict exact-coordinate assertion in pm/fs, maximum difference
`2.22e-16 nm`. A separately registered amendment uses `1e-12 nm` numerical
conservation tolerance and repeats the full selection. Attempts, partial
outputs and actual cumulative work remain separate; no failed population is
erased or spliced into the complete receiving.

H5MSM files explicitly contain only chemistry/structures, with mechanical values
and named reports retained separately as inspection evidence. No complete MM
codec, pose-reader MM transfer, historical H correspondence or original
prepared13 identity is claimed. The remaining immediate work is comparison and
native-reference admission, plus an explicit policy for constructing each new
complete pose before representative rescoring. Keep strict ranking contexts,
original descriptors/input hashes and the separate E4 hold unchanged. #78
remains partial; this receiving does not accept full E1 or public artifacts.

## Complete-pose construction and comparison prescription — 2026-11-06

The [new registered population and comparison matrix](../validation/e1_comparison_admission_2026-11-06.md)
now construct all five complete poses from the received heavy-coordinate sets.
Each receives its own fixed-state local H generation, named charges/types,
explicit flexible tree, provider reduction and actual export maps. Ten complete
preparations and thirty supplied-map checks pass across two unit policies,
with mechanically equivalent values/types and exact corresponding PDBQT bytes.
These are new locally completed conformations, not restoration of historical H.

The first attempt preserves a concrete domain refusal: four poses complete
association/reading, while the fifth fails the conservative check on all
thirteen atoms within the original 20-angstrom requested box. Source inspection
distinguishes that check from Vina's heavy-atom/effective-voxel grid check; no
native grid operation is run. A separately registered amendment uses one
24-angstrom requested box for every new pose and repeats the full population.
The completed run takes 20.53 s, sampled peak RSS 315.55 MiB, without a resource
interruption. Failed/completed denominators and all cumulative work remain
separate. Original input bytes, scores, producers and box are preserved.

The matrix identifies the fixed provided-receptor hash, new per-pose hashes,
method/version/component/units, box, weights, grid/refinement expectations,
prepared chemistry/mechanics and reference evidence. It keeps historical
docking, new fixed scoring, Vina and Vinardo distinct. Source-derived expected
defaults do not stand in for actual future native parameters. The new dataset
is ready for a separately registered native-input receiving; it does not yet
admit numerical energy comparison or a new public comparison API.

Distinct described partner contexts still refuse through current `rank_by`.
Do not remove hashes, relabel descriptors, invent common references or merge
legacy/modern routes to obtain an ordering. Next qualify the actual backend
artifacts and register the finite native evaluations against these exact inputs.
Broader partial/legacy provider questions remain separately owned; no universal
provider wait is required for this received new-source composition. #78 remains
partial, without accepting full E1, complete MM persistence or E4 restart.

## Finite source/native rescoring receiving — 2026-11-06

The [registered native notebook and receiving](../validation/e1_native_rescoring_2026-11-06.md)
now complete ten public scoring evaluations: five exact new complete inputs,
Vina and Vinardo, one common 24-angstrom requested box. An isolated verified
Vina 1.2.7 Python-3.14 artifact and its required Boost 1.86 borrow the routine
source runtime without changing its installed packages. Publisher/archive,
installed-file and actually loaded native identities are retained. The separate
two constructor/info probes compute no energies; no new preparation or search runs.

All eighty finite empirical components, two histories per pose, exact input
captures, reported weights/spacing, reference records and phase timings remain
available. Ten standalone audits and finite-JSON roundtrips pass. The collection
audit is incomplete without collection-stage provenance, with no inconsistent
checks. Both `rank_by` attempts correctly refuse distinct described input
contexts and leave the collection intact. No common-reference claim, score
offset, historical pooling or numeric ordering is manufactured.

The single nondefault-unit native population completes in 29.86 s on one CPU,
with sampled peak RSS 517.69 MiB, no resource interruption/signal and unchanged
engine payload/borrowed Conda metadata. Installation's optional environment-list
warning is retained separately. This is controlled source/native integration,
not a standalone/private whole-environment closure, public artifact, independent
energy accuracy or full supported matrix. Native grid bounds and source/build
correspondence retain their explicit observational limits.

Next specify and receive a study-level comparison/ordering contract for the
actual evidence, with changed-input/method/state/reference refusals, preserving
strict existing `rank_by`. A suitable installed representative workflow gate
also remains required. These new five-pose observations do not authenticate
historical prepared H or close #78/E1; the E4 hold remains separate.

## Finite interaction-component study ordering — 2026-11-06

The [case-specific comparison policy and offline receiving](../validation/e1_lig_inter_ordering_2026-11-06.md)
now admit the five existing `lig_inter` observations separately within Vina
and Vinardo, explicitly lower reported value first. It consumes the exact
previously received construction/scoring roots, graph witnesses, mechanical
assignments, axes/trees and native capture/parameter evidence. It retains each
different legitimate partner hash and every original descriptor, score, pose
rank and ranking history. No molecular kernel, chemistry codec or new public
comparison API is introduced.

The two method-local orders are source positions **1–2–3–4–5** for Vina and
**1–2–4–3–5** for Vinardo. Four admissions are the two studies repeated under
normal and pm/fs/coulomb reader policies, with byte-identical positive reports.
All 66 documentary controls refuse; two synthetic tie and two actual returned-
report detachment checks pass. Four public `rank_by` requests on these described
component scores still refuse distinct contexts and preserve the collection.

The registered reader completes in 3.92 s, sampled peak RSS 75.43 MiB, with no
resource interruption/signal. It recomputes no empirical value and imports no
Vina, RDKit or MolSysViewer. This is exploratory secondary analysis of already
inspected scores, not prospective/blinded prediction validation. Preparation
validity, native source/build correspondence, effective-grid observations,
total/shared-reference comparisons, historical equivalence and cross-method
scales are not upgraded by the finite order.

The bounded study comparison/ordering policy is now received. Next qualify a
representative installed workflow while preserving these explicit semantics;
broader reusable interface decisions remain separately scoped. #78/E1 remain
partial, without closing broader provider questions or restarting E4.

## Finite private installed workflow — 2026-11-06

The [registered installed receiving](../validation/e1_installed_receiving_2026-11-06.md)
now passes for a private DockingMT wheel built from unchanged runtime
`2fda6238e6b1cb3742f5d30b8ed3af699f9ed748`. Five support members also use private
wheels. MolSysMT remains an explicitly borrowed, hashed runtime snapshot with its
existing extension: its separate offline wheel build fails before compilation
because Cargo lacks `faer`. The failure is preserved and does not certify that
provider build or a wholly installed/public dependency composition.

Attempt 01 fails the overbroad file-origin guard on PyUnitWizard's documented
in-memory compatibility module before any probes or scores. A registered guard
amendment preserves the owning shared checker and checks every provider origin,
including that generated module's binding to its installed initializer.
Attempt 02 repeats the complete selection with unchanged notebooks/scientific
criteria. Both attempts and their diagnostics remain available.

The complete attempt executes ten public scores, saving eighty new components
and two named histories per pose. All eighty published values and five full pose
records match the earlier source receiving exactly, excluding only timings in
detached comparison copies. Actual captures, contexts, references and versions
remain intact. Ten standalone audits and exact JSON roundtrips pass; collection
incompleteness and strict total-ranking refusals remain explicit.

The new native manifest is sealed before a fresh installed JSON reader starts.
That process receives both component orders under two unit policies, with all
66 documentary negatives, tie/detachment controls and four strict component-
ranking refusals passing. Payload and origin checks reject checkout/shadowed
provider imports. Native stage takes 23.24 s with sampled peak 534.04 MiB; the
reader takes 9.60 s and 82.58 MiB. No resource interruption or signal occurs.
Original provider/runtime/input files and routine environment metadata remain
unchanged. The external reports do not manufacture public ranking histories.

This receives the bounded private installed workflow. Next review #78's five
acceptance criteria against the complete evidence chain and the intended user
workflow: distinguish the delivered case-specific external component policy
from a documented supported public composition. Preserve the simple ordinary
workflow and coherent deeper public controls as product review concerns; no
new general framework/API follows automatically from the qualification harness.
Keep #78 partial until that explicit profile/acceptance decision is recorded.
Public artifact/matrix work remains #30/#47, and whole E1, independent scientific
validation, broader provider contracts and the E4 hold remain separate.

## Public-workflow acceptance review — 2026-11-06

The [five-criterion review](../validation/e1_public_workflow_review_2026-11-06.md)
receives the finite reference, provider-composition, external study-policy and
actual source/private-installed gates within their stated limits. Criterion 4
remains partial for the intended user workflow. The representative native run
starts with five score-free, unranked new poses, retaining sixteen new values
and two new histories each. Old docking scores/ranks survive as associations to
another preparation; that run does not demonstrate inline preservation while
rescoring the same original prepared poses. Separate public controls establish
the additive primitive, not the missing complete collection workflow.

The positive component admission is also an external case-specific report,
without a public study-comparison operation or a new `ranking_history` entry.
Strict `rank_by` refusals are correct. Do not remove input hashes/descriptors,
copy historical scores onto a different model or invent a ranking decision to
declare E1 delivered.

The [public usage guide](../validation/same_state_rescoring_workflow.md), linked
from the root README, shows the current matching-prepared-input route and deeper
controls without exposing qualification supervisors as user tools. It is a
source-reviewed guide, not a new native execution or user-acceptance receipt.
The [vision](../VISION.md#user-experience-and-public-api) records the maintainer's
explicit ordinary/advanced usability objective.

Next receive a maintained public composition from a complete prepared source
and existing scored result through per-pose reconstruction/preparation,
additive named scoring, persistence and explicit study-comparison decisions.
Preserve the original collection, model/axis/assignment evidence and all failures.
First test the existing provider/public composition; introduce a small owned
operation only if that concrete task demonstrates a missing reusable boundary.
No batch API, molecular fallback or general framework is justified merely by
the existence of the finite qualification notebook.

The received complete-source profile no longer waits on MolSysMT #599/#447 as
blanket blockers, so `blocked_by` is empty. Their broader provider requests and
#521's partial/reference scope remain linked and unresolved here; this does not
claim those issues closed or all their profiles delivered. The remaining local
functional work is owned by #78. Public delivery remains #30/#47, not a new
condition imposed on this bounded acceptance review.

## Public continuity on an actual returned pose — 2026-11-06

The [public composition receiving](../validation/e1_public_composition_2026-11-06.md)
now exercises the maintained [user notebook](../../examples/rescore_existing_poses.ipynb)
through a complete prepared source and an actual scored docking result. Its
three code cells use only public operations and explicit caller inputs.

The small registered search requests two poses and returns one; its minimum-two
qualification remains incomplete. A separate receiving reuses that exact saved
result and reproduces its prepared source through named public assignment,
requiring the original input hash and graph/field agreement before reconstruction.
It adds two real fixed-score evaluations without another search. Four original
scores, rank 1, original metadata/descriptors and backend ranking history survive;
sixteen new components/two histories are added. Four graph witnesses and two
charge audits receive the actual source/reconstruction/preparation fields.

The native qualification then fails an overstrict expectation on standalone
`audit_pose`: original docking origins belong to result-level provenance, so
the four old scores correctly remain incomplete in isolation. The portable
collection audit is consistent. A separately registered record-only adjudication
passes both reader policies, four collection audits, four appropriately incomplete
standalone audits, capture binding, canonical roundtrips and detachment. Its
staging copies do not overwrite/reclassify the failed generator. Native state
negative, final native mappings/context cleanup and multi-pose receiving remain
unexecuted/unreceived; no passing qualification is manufactured for them.

The first private-copy error, incomplete N2 population and failed N1 qualification
are retained. Cumulative new work is one search/one returned pose and two fixed
evaluations. This receives the observed single-pose public continuity, improving
criterion 4 without accepting its multi-pose or positive-comparison boundary.
Next choose an informative admitted population and receive comparison/decision
consumption, retaining scientific selection and all original evidence. There is
no need for a new batch/campaign framework established by this example. #78
remains partial; public delivery/CI admission keep their separate owners.

## Public comparison implementation — 2026-11-07

The [new comparison contract](../validation/score_comparison.md) provides
`compare_scores(result, score_name, problems=..., ascending=...)` for a bounded
Vina/Vinardo 1.2.7 fixed `lig_inter` profile. It consumes the matching complete
preparations, binds their actual provider exports/maps to captured scoring bytes,
and delegates chemical correspondence and assignment validation to MolSysMT.
The public caller supplies existing objects rather than constructing a trusted
evidence packet. Different per-pose input hashes and the original scores, ranks
and ranking history remain intact; a separate report records values and ties.

The [software controls](../../tests/test_score_comparison.py) pass 54 tests with
explicitly simulated molecular seams and unchanged real saved score records.
The selected existing score/reference/collection-audit/model argument regressions
pass 139 tests. An initial broader selection stops during collection because
`test_pose_audit` imports the unavailable optional Vina package; it runs no
scientific case. Its diagnosis is retained separately, and that selection is
not represented as passing. No new energy or molecular receiving follows from
these software controls.

The exact five historical score inputs are declared for installed-test support
with their original SHA-256 identities, outside the runtime payload. The new
runtime module is included in the current package resource declaration. Neither
source checks nor that declaration qualifies an installed/public artifact.
A separately frozen, resource-bounded receiving will reproduce matching inputs
through explicit named preparation and exercise the actual public comparison.
Full multi-pose reconstruction/additive continuity, whole E1, public delivery and
the separate E4 hold remain unchanged. Remote checkpoint evidence is still
deferred under the maintainer's `[skip ci]` instruction.

## Public comparison receiving — 2026-11-07

The [registered private receiving](../validation/e1_public_comparison_2026-11-07.md)
now passes for public `compare_scores`: five freshly reproduced complete
preparations exactly bind to old captured inputs, and four calls return the two
method-local interaction orders under two unit policies. All eight informative
refusals, twenty correspondence/assignment-validation checks, charge/geometry
checks, nonmutation and JSON controls pass within the resource budget. A fresh
standard-library reader recovers the four reports with identical bytes and
decisions. Zero new energies, searches or H-generation operations occur.

The first private wheel exposes a migration-prefix discovery defect and is
rejected before science; #30 records its correction and nineteen distribution
controls. The separately received wheel from `a7422df` has exactly 64 runtime
paths and borrows the identified support/provider composition. Rejected/failed
preflights and the earlier incomplete two-pose population remain preserved.

The bounded public comparison is received. Criterion 4 and whole E1 remain
partial: complete multi-pose original docking result → reconstruction → explicit
preparation → additive evaluation continuity is still required. This comparison
does not restore historical prepared H or supply missing original docking
history. Broader profiles, public #30/#47 delivery and the E4 hold retain their
separate owners.

## Complete rigid public continuity — 2026-11-07

The [new registered rigid profile](../validation/e1_rigid_continuity_2026-11-07.md)
receives the remaining concrete user task: both actual original docking poses
complete the unchanged portable example through public reconstruction,
preparation, additive Vina/Vinardo scoring and public method-local component
comparison. Eight old scalar values, IDs/states, ranks, descriptors and backend
history survive alongside 32 new values and two histories per pose. The whole
collection audit is consistent. Nine provider witnesses, seven charge audits,
source/payload nonmutation, two informative pre-native refusals and two strict
ranking refusals pass. Fresh persistence receiving performs no molecular work.

The original search is made once, with a preregistered rigid ordinary model and
a request for at most three poses; it returns two. Its qualification remains
**FAIL** after saving that return: a Python tuple from `Vina.info()['weights']`
becomes a JSON list, so an excessively strict Python-container equality assert
fails. A registered amendment receives the saved finite wire records in a new
process without retrying the search. The original generator's later live-source
and final origin checks were not reached and remain unreceived. Its failed
receipt and earlier incomplete/failed populations remain unchanged; the fresh
receiver passes its own full controls. No reconstructed MM inspection sidecar
or invented historical H/state authority is introduced.

The previous public review's criterion 4 is now received **for this bounded
rigid profile**, including positive public comparison and all actual original
members. Criteria 1–3 and 5 retain the earlier finite reference/provider/control
receipts and their stated limits. The next action is the explicit bounded
acceptance/disposition review and synchronized issue closeout, rather than
another scientific search or a larger API. Keep this report partial until that
review is recorded; do not add whole-E1, broad provider identity or public
package qualification as new conditions on this local profile. Those boundaries
retain their existing owners.


## Bounded acceptance and resolution — 2026-11-07

Accept this proposal for the complete-source rigid prepared13 profile, one
explicit ligand/receptor state, Vina/Vinardo 1.2.7, and separate per-method
`lig_inter` comparison reports. The public example receives every actual original
pose. Original ranks/backend decisions remain intact; comparison reports carry
the new ordering decision separately. This completes the concrete #78 task.

| Owning criterion | Received evidence | Acceptance boundary |
| --- | --- | --- |
| Executed reference semantics and preservation of legacy observations | [Reference contract](../validation/scoring_reference.md), original native/reference receiving and refined record auditors. | Current-conformation reference and eighth component are explicit; docking/shared-reference totals and cross-method affinity remain distinct. |
| Provider projection/identity, chemistry, mechanics, maps, bytes and units | [Complete-source admission](../validation/e1_comparison_admission_2026-11-06.md), [public comparison](../validation/e1_public_comparison_2026-11-07.md), [rigid continuity](../validation/e1_rigid_continuity_2026-11-07.md). | Current complete18/prepared13 source authority and actual exported views are checked through supported MolSysMT operations; historical missing H/MM and partial inputs remain unknown. |
| Conservative comparison with informative changed-condition controls | Public `compare_scores` and its [contract](../validation/score_comparison.md), 54 software controls, actual positive reports and state/geometry/method/context refusals. | Method-local fixed `lig_inter` observations on admitted inputs; distinct hashes remain, strict `rank_by` remains unchanged. |
| Complete native/installed original-result continuity, original/new scores and detached persistence | Both actual rigid poses pass the unchanged public notebook: eight original values, 32 added values, four native evaluations, two comparison reports, nine graph witnesses and seven charge audits. A separate standard-library reader receives all originals/intermediates/finals and decisions. | All members of this registered two-pose population complete the route; no new energy/search is used for closeout. |
| Gates match the actual claim and resource/ownership boundaries | Exact private consumer payload/origins, borrowed identified providers, native overlay and installed support checks pass for the receiver; monitored serial resources and independent persistence are retained. | Public dependency/platform delivery, independent scientific accuracy, live visualization and the complete product remain separately owned under #30/#47, #33/#49, #52/#60 and #73. |

The [rigid archive](../validation/data/e1_rigid_continuity_2026-11-07/manifest.json)
retains all 159 members and its exact root
`ac270bddf7a95c4f219fec91771bea3f76fb258785b457f569ce3bf4178f32b2`.
The independent [public-comparison archive](../validation/data/e1_public_comparison_2026-11-07/manifest.json)
retains its five-pose/two-method/two-policy profile and eight informative
refusals. Producers and populations are not pooled or relabelled.

`generation-01` remains FAIL after saving two actual poses: its Python tuple/list
transport equality assertion was excessive. Original post-search live-source
and final origin checks were not reached and remain unreceived. The registered
fresh receiver reproduces the exact source capture, checks its own complete
live/payload invariants, and passes the rescoring/comparison task on those saved
outputs. Closing this rescoring proposal does not retroactively qualify that
generation attempt or erase the earlier incomplete/failed populations.

The module guard `tests/test_score_comparison.py` collectively protects the
public comparison contract: separate method-local orders, original ranks and
records unchanged, complete selection, finite detached reports, conservative
context/state/method refusals, and actual render/map/capture binding. Its
molecular seams are explicitly synthetic; it cannot substitute for the retained
native/provider receiving. Existing guards in `tests/test_scoring.py`,
`tests/test_scored_result_audit.py` and `tests/test_scoring_reference.py` protect
additive history, pre-native refusals, collection-origin preservation and
reference/context semantics. No destructive mutation or new scientific run is
needed to review these assertions.

The next independent implementation work is #81's distinct-ligand study
admission and explicit study comparison, preserving this same-state profile.
Whole E1 and Core+Extended completion remain governed by #73. The maintainer's
open-ended 0.x stabilization clarification is [DMT-048](../DECISIONS.md#dmt-048--let-pre-10-versions-follow-verified-progress).


## Closeout local qualification — 2026-11-07

The current module guard and lifecycle selection pass **55 tests** through
Pytest Receptor on routine Python 3.14, one CPU/native worker, nice 10 and
monitored 8 GiB RAM reserve. Elapsed time is 11.77 s with sampled group peak
149.96 MiB; no resource interruption occurs. These are software/lifecycle
controls, with no new scientific population, molecular calculation or energy.
The original native and independent-reader observations remain their own
producers. Final source/document/index/archive/resource/publication checks and
fresh committed-source export validation accompany publication. Skipped remote
CI remains missing evidence under #28, not a passing check or a closure blocker
silently moved into this bounded workflow.
