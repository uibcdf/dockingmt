# BindingInterface work-plan review: revisions 3 and 4

Owner: [BindingMT #112](https://github.com/uibcdf/bindingmt/issues/112).
Reviewed: 2026-11-12. Scope: **planning completeness and implementation readiness**;
no native calculation, API emission, scientific qualification or adoption is
delivered by this review.

## 1. Sources, sequence and conclusion

The maintainer requests two actual passes: write revision 3, preserve it, then
reread the full TopoMT contribution and improve the plan as revision 4.

- The [native catalogue post](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6836773833)
  and [complete TopoMT proposal at `a13b9b2`](https://github.com/uibcdf/topomt/blob/a13b9b2725bd8a4edd851441d1a5a53720e0f3ea/devguide/binding_interface_native_catalogue_plan.md)
  are the contribution baseline, blob `722d7ea7f2b37cf257b7be0044b81a83433f3e26`.
- [Work-plan revision 2 at `d69315d`](https://github.com/uibcdf/bindingmt/blob/d69315dfebc49ddd8c2da1999955edc078fd8893/devguide/binding_interface_implementation_plan.md)
  supplies the preserved data, PISA, pharmacophoric/consumer and lifecycle work.
- [Revision 3 at `66d8ba9`](https://github.com/uibcdf/bindingmt/blob/66d8ba9ed19026ef7431aacf155d54f1eb069778/devguide/binding_interface_implementation_plan.md)
  adds the BindingMT catalogue, explicit native calculation, N0/N1/N2 contracts,
  independent controls and contact-first/surface-next milestones. It was committed
  before the second full source reading. Six selected documentation gates pass
  in its final workspace and fresh committed export; no runtime was exercised.
- The [maintained revision 4](binding_interface_implementation_plan.md) incorporates
  the findings below and is the current work order. Scientific-design revision 2
  remains the information-model basis, with the native roadmap extension explicit.

During readback of the first fourth-revision publication at `065523d`, the new
[regional-physicochemistry clarification](https://github.com/uibcdf/bindingmt/issues/112#issuecomment-6837860911)
arrived. Its [catalogue revision 2 at `0400821`](https://github.com/uibcdf/topomt/blob/04008217e6a568213c05d037ebeb6d543ca24803/devguide/binding_interface_native_catalogue_plan.md),
blob `8f1e20a0dafe962c398855d6b5d2b3a8e4b89685`, preserves the 15 main sections
and 17 original controls, adds one catalogue entry and clarifies TopoMT #198's
independent scope. Its complete diff against the frozen first edition was reviewed
and received within revision 4. The current catalogue therefore retains **17
entries**, including the original 16. Earlier source/check receipts stay intact.

The native direction fits BindingMT's accepted domain and is retained. The second
pass finds no proposed catalogue family or validation family to discard. It does
find incomplete admission details and cross-document ownership/priority wording;
revision 4 corrects those rather than merely changing a version label. Coverage
below distinguishes planned first work, separately retained obligations and later
candidates. It does not mean all entries are accepted APIs or implementation gates.

## 2. Findings from revision 3 and fourth-revision corrections

| Finding | Observed limitation or later evidence | Revision-4 correction |
| --- | --- | --- |
| R1: finite admission | Scientific facts were spread across sections; closure could omit a required field or make surface prerequisites block contacts. | The N0 admission record lists the definition, populations, actual calls, facts/preconditions, resources, outcomes, persistence and independent evidence. Its operation table separates D, N1, N2, T and H/P prerequisites. |
| R2: request versus result | Completed no-contact was defined, but an empty native calculation request and omitted/default arguments were not explicitly distinguished. | Explicit empty/duplicate/unknown requests refuse before child calculation. N0 must close the finite default or required-argument policy; known unsupported capability stays distinct from evaluated zero. |
| R3: numerical route/resources | The CSR candidate was bounded in principle, without explicit treatment of requests that fall back to dense storage or use different index/boundary semantics. | Require actual dispatch, eligibility, cutoff/fallback, index/multiplicity and resource-envelope receiving. Unsupported or over-budget fallback refuses or uses a separately qualified bounded request. |
| R4: check/use lifetime | Native calculation had actual context records, but the relationship to imported `current_finding` guarantees and the shared baseline of three SASA contexts needed precision. | Fresh native work records its own performed facts; it upgrades no other finding. Stable input or exact caller preconditions are explicit; isolated/combined surfaces retain demonstrably common geometry/chemistry/radii/maps. |
| R5: numerical/portable meaning | Surface tolerances and quantity checks existed, but signed losses, classification thresholds and field dimensions could still be conflated. | Keep raw losses/numerical status, separate tolerance from membership threshold/uncertainty, and validate lengths, areas, counts and field identity. An area-derived footprint needs its own criterion/persistence. |
| R6: ordinary/expert delivery | The request was concise, but actual user-facing acceptance artifacts were less concrete than the expert scientific tables. | Two public workflows require produced summaries/records: ordinary contacts/save/read and expert surface tracing/composition. Optional dependency absence is real task-owned isolation; shared packages remain intact. |
| R7: owner/reference continuity | Existing provider/resource/synthetic destinations were implicit, and a retained #190 hosted-scope sentence used an old identity owner for new work. | Link TopoMT #194/#165/#187, preserve adapter ownership, identify #195 for new shared science and #30 for component qualification; #190 stays historical identity receiving. Primary-method and comparative-evidence routes are explicit. |
| R8: inspectable completeness | Revision 3 contained the catalogue/controls but no separate account of every incoming section and retained/deferred item. | The first fourth-revision pass maps 15 sections, 16 entries and 17 controls; R9 extends the catalogue to the latest 17 entries, retaining finite admissions and existing obligations. |
| R9: regional physicochemistry | After the initial fourth revision was published, the owner clarified that TopoMT characterizes chemistry on its own spatial supports without requiring a binding partner. | Receive edition 2's seventeenth entry, standalone #198 ownership, qualified regional references and question/support-specific rather than exclusive chemical-descriptor ownership. Native N1/N2 remain independent. |

The corrections are documentation requirements. None declares that an installed
MolSysMT extension, optional attribution branch or new BindingMT method has passed.

## 3. Complete proposal-section disposition

The source section numbers refer to the 15 main sections in exact `a13b9b2` and
`0400821`, not a mutable branch. The later changes affect ownership, the catalogue
and owner actions; the matrix includes both editions. A row records semantic
review, not just matching headings or keywords.

| TopoMT section | Disposition in BindingMT | Maintained location |
| --- | --- | --- |
| 1: purpose/user experience | Native contact calculation is the first ordinary numerical delivery; expert tracing and routine save/read have actual future acceptance artifacts. | Plan [useful outcomes](binding_interface_implementation_plan.md#2-useful-outcomes-and-preserved-boundaries) and [user workflows](binding_interface_implementation_plan.md#ordinary-and-expert-acceptance-workflows). |
| 2: relationship to prior work | Scientific model and revision-2 lifecycle controls remain; native priority changes explicitly, while T/H/P/#111 obligations persist. | Plan [contribution disposition](binding_interface_implementation_plan.md#11-native-catalogue-contribution-and-planning-disposition), [dependencies](binding_interface_implementation_plan.md#4-dependency-order-and-current-status) and milestones. |
| 3: ownership | BindingMT association questions, MolSysMT molecular tools/chemistry, TopoMT's standalone regional physicochemistry/supports and specialist semantics retain their complementary owners; no reverse import or adapter move. | Plan sections 2, 5.2 and [regional chemistry](binding_interface_implementation_plan.md#optional-regional-physicochemistry-and-association-specific-use). |
| 4: inspected capabilities | Contact/distance/neighbor/SASA sources are inspected starting points; raw arrays are no foreign scientific receipt, and table lookup is not geometric burial. Native/import qualification remains pending. | Plan [N0 tool table](binding_interface_implementation_plan.md#92-n0-public-request-context-and-exact-owner-route) and execution boundary. |
| 5: first native profile | One Cartesian structure, two nonempty disjoint populations, explicit chemistry/H/radius/environment rules and no implicit preparation. Later domains keep separate admission. | Plan N0, its [operation facts](binding_interface_implementation_plan.md#n0-admission-record-for-each-selected-calculation) and N2. |
| 6: catalogue | All entries retain definition/method/version distinctions and individual stage/trigger; unselected families are not global gates. | Plan [catalogue](binding_interface_implementation_plan.md#91-bindingmt-catalogue-and-staged-admission); section 4 below. |
| 7: per-entry contract | Every selected calculation closes its scientific meaning, measured/occluder populations, checks, parameters/resources, statuses, portable quantities, reference controls and owner. | Plan N0 admission record, D2 and [native controls](binding_interface_implementation_plan.md#95-independent-native-receiving-controls). |
| 8: calculation/composition | Explicit native execution and supplied-evidence composition share a result model; summary/read/copy execute nothing. Footprints persist independently and historical checks remain historical. | Plan F10, D1/D2/C, N1, user workflows and T1 persistence. |
| 9: recipes/edge cases | Contact populations, both SASA losses, atomic/group contributions, chemical completeness, conditional environments, nonadditivity and distinct topographic supports are preserved. | Plan [N1](binding_interface_implementation_plan.md#93-n1-native-contacts-residue-reduction-and-participant-footprints), [N2](binding_interface_implementation_plan.md#94-n2-native-sasa-both-side-losses-and-mapped-burial), resources/later families and H/P. |
| 10: resources/attribution | Owner-versioned numerical resources, units/acquisition terms and actual reached-method bibliography survive reuse/persistence; no copied PISA resources or new execution credit. | Plan N0, resources/attribution and native attribution controls. |
| 11: staging | Data -> first native contacts -> surfaces is delivery priority. Surface, chemistry, PISA and consumers close their own real prerequisites. Existing synthetic sequence is independent. | Plan dependencies and [milestones](binding_interface_implementation_plan.md#15-milestones-acceptance-evidence-and-closeout). |
| 12: independent validation | All controls are retained with expected scientific meaning; native request/fallback/user-workflow refinements supplement them. No runtime guard exists merely because it is listed. | Plan native receiving matrix; section 5 below. |
| 13: external methods/comparison | PISA remains optional receiving/comparison, with original #194 and resource/licence #165 ownership. Comparisons match definitions/inputs/resources and classify discrepancies before claims. | Plan resources/comparison route and T0/T1; local evidence-publication policy. |
| 14: owner actions/closeout | #112 owns local programme, #195 finite shared agreements, #197 TopoMT review and #198 independent regional chemistry. Concrete reusable gaps go to their provider; each increment is independently bounded. | Plan 5.2, N0, regional chemistry, milestones and [next action](binding_interface_implementation_plan.md#17-next-actionable-checkpoint). |
| 15: sources/literature | Exact proposal and molecular-source baselines are retained; primary-method citations begin the literature work, not blanket qualification of every candidate. | Review section 1 and plan tool/method references. |

## 4. All candidate entries and their adoption state

These are planned descriptions, not delivered exports. Later BindingMT entries
stay under #112 with their trigger until selected; independent regional chemistry
is owned by TopoMT #198 and receives its own optional BindingMT handoff.

| Candidate entry | Planned disposition | Admission trigger / owner |
| --- | --- | --- |
| `atomic_contacts` | Initial N1. | BindingMT contact criterion/public molecular route and independent references. |
| `residue_contacts` | Initial N1. | Actual owner grouping/maps and explicit atom-to-group pair/count reduction. |
| `contact_footprints` | Initial N1. | Both-side member/contributor maps and actual independent persistence. |
| `steric_overlaps` | Later geometric candidate. | Admitted radius-overlap model, reference controls and owner resources. |
| `solvent_accessibility` | Next N2. | Exact owner radius/probe/occluder/input construction and sampling contract. |
| `interface_burial` | Next N2. | Common baseline for isolated/combined surfaces, both losses and mapped contributions. |
| `chemical_interactions` | Family-specific later receiving. | Selected MolSysMT recognition/state/coverage profile; not inferred from N1 distance. |
| `physicochemical_partition` | Later association-specific aggregation or qualified regional reuse. | Explicit owner classifications/support/context, membership/measure, overlap/additivity and denominators. |
| `buried_unsatisfied_polar_sites` | Later scoped inference. | Qualified burial and complete evaluated chemical partner/environment coverage. |
| `interaction_network` | Later network profile. | Defined observations/edges, multiplicity and comparison policy. |
| `topographic_organization` | Optional specialist enrichment. | Actual qualified TopoMT support/context/relations and its existing gates. |
| `topographic_physicochemistry` | Independent TopoMT #198 capability; optional BindingMT receiving. | Actual support/state/classification/weighting/coverage, spatial distributions and qualified public owner records; native contacts/surfaces do not wait for it. |
| `geometric_complementarity` | Later geometry profile. | Admitted surface/fit definition, independent reference and eligibility. |
| `pose_comparison` | Scoped comparison profile. | Observable/correspondence/coverage/frame and intended participant differences. |
| `ensemble_statistics` | Later ensemble profile. | Sampling, per-structure correspondence and justified weights. |
| `energetic_observables` | Separate future method profile. | Defined endpoint/process/states/conditions and numerical/model uncertainty evidence. |
| `assembly_inference` | Separate future predictive decision. | Explicit model/domain and appropriate predictive validation. |

Native chemical calculation is distinct from the already retained H0/H1
PharmacophoreMT receiving branch. The latter still needs its promised native
inputs and whole-feature/mapping/constraint controls; the catalogue does not
declare those supplied or fulfilled. PISA T0/T1 and consumer P retain every
previously agreed positive/empty/failure, information-role and context control.

## 5. All independent validation controls

Each row from source section 12 has a planned receiving population below. These
are acceptance obligations, not executed test counts or named guards that do not
exist yet. Freeze independent expectations/tolerances before interpreting results.

| Control | Receiving population | Required distinction retained |
| --- | --- | --- |
| C01: geometric reference | N1. | Exact pairs/distances inside, at and outside the admitted cutoff. |
| C02: participant exchange | Symmetric N1 predicate. | Total pairs conserved and mapped sides exchanged; directional chemistry excluded. |
| C03: separated participants | N1/N2 with justified surface assumptions. | Evaluated zero; contact absence alone does not prove zero burial. |
| C04: isolated sphere | N2. | Analytic area under the actual supported radius/probe construction. |
| C05: two spheres | N2. | Analytic cap/containment/separation references, independent of PISA. |
| C06: surface sums | N2. | Atom/group contributions sum to each side and explicit reporting convention; fixed-sample occlusion monotonicity. |
| C07: convergence | N2. | Independent error bounds over declared samples/rotations, without universal exact invariance. |
| C08: output/environment | N2. | Output selection preserves occluders; isolated construction changes them explicitly with intact maps. |
| C09: grouping/completeness | N1 and H/P as applicable. | Actual unrelated/internal observations excluded; recognition participants remain chemically complete. |
| C10: scientific outcomes | D/N/T/H profiles. | Computed empty, missing, unrequested, unsupported, undefined and failed stay separate. |
| C11: maps/multiplicity | Native/derived and H/P receiving. | Reordering/extraction, original structure 2 -> local 0 and repeated contributions preserve identity without independence inflation. |
| C12: footprint persistence | Native and PISA positive/empty cases. | Actual footprint save/read retains ordered source members, aligned locals, parents and all contributors. |
| C13: crossed states | D2, actual native and T recovery/use. | Original outcome, present asset/recovery and fresh use remain independent. |
| C14: context changes | C and actual native/application profiles. | Relevant edits reassess affected uses; history/other dependencies retain their own scope. |
| C15: units/records | All actual admitted quantity boundaries. | Normal/pm-fs physical values, field/dimension/identity preservation and malformed/tampered refusal. |
| C16: optional dependencies | Actual native calculation and independent readback. | No PISA/TopoMT use; selected optional enrichment keeps its own dependency contract. |
| C17: attribution | Reached native/optional branches and fresh readers. | Completed/empty/reused/failed/enclosing workflows retain actual methods without new original credit. |

The original 17 controls are retained; revision 4 additionally makes native
request admission, fallback eligibility/resource refusal and produced ordinary/
expert workflows explicit. Administrative document checks validate no geometry,
surface model, native ABI, scientific comparison or optional-attribution execution.
The later regional profile adds its own support/denominator, mixed-atom-within-
residue, equal-fraction/different-layout and persisted unknown/geometry-preservation
controls when selected. These supplement the original matrix without becoming
new prerequisites for native contacts or surfaces.

## 6. Remaining decisions and honest completion boundary

- Close actual P0a and each selected N0/C contract: public spellings/defaults,
  scientific criterion, owner calls, required observations, checked facts/caller
  preconditions and supported resource/assurance scope remain pending.
- Refresh exact source/native/import origins before runtime receiving; inspected
  source commits are not public dependency floors or native binary qualification.
- Agree exercised shared facts in MolSysSuite #195. A source signature, TopoMT's
  review or this local plan is not an acceptance message from another owner.
- Report observed or reasonably suspected reusable molecular gaps in MolSysMT,
  stating the consumer evidence and remaining uncertainty. Reuse owning work;
  preserve the complete-inventory rule before absence claims from searches.
- Keep selected N0/N1/N2 and existing T/H/P obligations visible through actual
  evidence or explicit maintainer rescoping with owner/revisit conditions. Later
  catalogue families are candidates, not hidden new release gates.

The selected documentation/resource gates run after final edits in the workspace
and a fresh committed export, serially with the recorded shared-machine limits.
Exact receipts and source/public readback are retained under
`.molsyssuite/binding-interface-native-plan-r3-r4-112-20261112/`, with #50 custody
review on 2026-11-14. Source and installed/public/platform/hosted qualification
remain distinct. The scientific full-suite hold and shared-prefix pause persist;
this review changes no environment, runtime, frozen scientific producer or release.
