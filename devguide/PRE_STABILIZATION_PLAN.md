# Core and Extended delivery before stabilization

Owner: [DockingMT #73](https://github.com/uibcdf/dockingmt/issues/73).
Accepted maintainer objective: 2026-11-06, [DMT-046](DECISIONS.md#dmt-046--deliver-the-complete-functional-objective-before-stabilization).
Status: **active; completion unproven**. Inspected starting source: `530a4cf`.

## Outcome and version boundary

Deliver the complete Core C0–C6 and Extended E1–E5 workflows, bounded scientific
qualification, independent reproducibility and public installation as the
prospective **0.5.0** functional milestone in the existing
[release ladder](RELEASE_MILESTONES.md). Then stabilize the accepted surface under
0.9.0; reserve 1.0.0 for the subsequent stable-release decision. This identifies
the development target, not a selected candidate, completed gate, tag or package.
Earlier milestones may consolidate genuinely qualified subsets. The separate
fixed 0.1.0 candidate `905abc9` is not advanced by this plan.

A scientist must be able to start from declared receptor/ligand sources and
states, prepare explicit inputs, dock/redock, evaluate and interpret poses,
inspect interactions and compare alternatives within supported scope. Stored
records must explain inputs, transformations, methods, parameters, mappings,
failures and unknown information. Another installation must be able to inspect
and reconstruct the representative workflow to the documented degree.

## Requirements and current evidence

The [35-criterion Core map](CORE_MVP_STATUS.md), [MVP](MVP.md),
[scientific model](SCIENTIFIC_MODEL.md), [validation strategy](VALIDATION_STRATEGY.md)
and [Core/Extended comparison](CORE_EXTENDED_COMPARISON.md) retain their detailed
authority. The table maps the whole objective to its remaining work; an
implemented API or record-only test is not acceptance of a scientific workflow.

| Requirement | Evidence that would establish completion | Starting disposition / next action |
| --- | --- | --- |
| C0 foundations and support contracts | Qualified public model/protocol/backend, quantities, validation, availability and diagnostic contracts in complete workflows. | Representative source/private evidence exists; #19 and actual public/minor admission remain partial. |
| C1 explicit preparation | A declared conventional protein/small-ligand profile, selected states, source/output maps, preparation assessment and reproducible supported transformations. | Worked preparation exists; #4/#33/#49 retain broader source/state and independent admission questions. Reuse provider operations. |
| C2/C3 redocking/local docking | Complete reproducible searches, normalized poses/scores, input/domain provenance and explicit reference recovery within the admitted scientific profile. | Existing 3PTB/1IEP and other finite controls retain their producers. Receive changed boundaries and panel admission separately; do not relabel old observations. |
| C4 selection-derived domain | Provider-owned selection/geometry, stored derivation/projection and observed domain/reference/pose correspondence. | Construction/record evidence exists; visible acceptance remains #52/#60. |
| C5 results/provenance | Saved scores/rankings/evaluations, actual input identities/maps, traceable preparation/protocol and explicit recoverable/missing information. | #75–#77 deliver bounded reading/audits. General source restoration and partial/reference coverage remain #4/#49 and MolSysMT #521. |
| C6 visualization | Real addon controls, communication and canvas display correctly paired receptor/domain/poses/reference, with actual interaction evidence. | Python/DOM/export/private evidence exists; live acceptance is still unproven. Respect the maintainer's scheduling decision. |
| E1 named rescoring/ranking | Existing poses acquire distinct named evaluations; original scores survive; declared comparable collections can be ranked and audited reproducibly. | #78 owns native reference semantics, provider identity/projection, explicit comparison admission and the representative execution. Strict current ranking remains. |
| E2 modest ligand collections | A declared study isolates individual failures, retains ligand/state/run identity and supports scientifically delimited aggregation/ranking. | #81 scopes actual distinct-ligand admission and study comparison, reusing serial `dock_many` and outcomes. Preserve strict within-result ranking and provider-owned chemistry; collection execution/qualification remains unproven. |
| E3 comparison/clustering | Supported pose/reference and pose/pose measurements and useful clustering with explicit populations, correspondence, units, method/thresholds and degeneracies. | #79 scopes the concrete positional workflow. MolSysMT #604 requests supported bounded pairwise/clustering tools or an existing composition; no local molecular algorithm. |
| E4 interaction analysis | A minimal structured interaction record supports interpretation/filtering/visualization with named molecular definitions, selections, units, identities and unsupported cases. | #80 implements the provider-only notebook. Local receiving stops at the resource guard; first hosted receiving completes preparation but refuses XYZ extraction before detectors (MolSysMT #610). Register/receive the explicit-atom public getter amendment, preserving the local hold. Assembly/detection/persistence and pose association remain unproven; no local contact/chemistry engine. |
| E5 independent reproduction | A separate receiving installation reconstructs a representative stored workflow from documented inputs, with observed agreement/tolerances, failures and missing information. | Captures/replay/recovery supply pieces; a whole independent workflow audit remains unproven. |
| Bounded scientific qualification | An admitted transparent independent panel and informative positive/adverse controls, explicit preparation/search/ranking hypotheses, denominators, budgets and all outcomes. | Audit Q2–Q4 and #33/#49 own admission. Existing within-case repetitions do not become independent complexes. |
| Public delivery and support | Actual compatible public dependencies, exact staged Conda artifact, required source/native gates and eight Linux/macOS arm64 × Python 3.11–3.14 installed cells, same-byte promotion and public receiving. | #30/#47 remain partial. Refresh artifact availability before acquiring/receiving; old private receipts do not certify a new public file. Distribution is Conda `uibcdf`. |
| Usable API/records and documentation | Coherent documented public contracts, examples, schema/quantity/diagnostic behavior, migrations for intentional changes and explicit scientific limits. | Preserve existing contracts and receive changes with applicable guards. Functional delivery precedes the later stabilization/final-compatibility decision. |
| Resource control | Caller-visible execution limits, isolated failures and measured representative CPU/RAM behavior without silent global caches or whole-machine assumptions. | Reuse serial execution; local agent qualification remains one logical CPU, low priority, one native/build worker, monitored reserve and no automatic heavy restart. #28/#50 own evidence/custody. |

## Immediate sequence

1. Receive exact-source CI under #28, preserving nonterminal/failure states.
2. Advance [same-state E1](pending_proposals/qualify_same_state_rescoring.md):
   record the actual native energy-reference convention, retain old records,
   and define comparison conditions without changing molecular identities.
3. Receive provider-owned prepared-conformation projection
   [MolSysMT #599](https://github.com/uibcdf/molsysmt/issues/599) and the relevant
   identity evidence in [#447](https://github.com/uibcdf/molsysmt/issues/447).
   A supported existing public composition can satisfy a request. Keep #521's
   partial/reference reader boundary explicit.
4. Register the small representative E1 execution after those contracts are
   received. Preserve original docking scores, named new evaluations and ranking
   history. Define reference policy, comparison population, controls, units,
   resources and failure rules before computation.
5. Scope and qualify E2–E5 with their owners and receive the remaining Core,
   scientific, visual and public-delivery evidence. Independent requirements may
   progress while another provider or hosted run is pending. E3's
   [provider-backed contract](pending_proposals/qualify_pose_comparison_and_clustering.md)
   is #79/MolSysMT #604; E4's
   [existing-tool receiving](pending_proposals/receive_docking_interaction_analysis.md)
   is #80. Their [dated inspection](validation/extended_provider_scope_2026-11-06.md)
   is not runtime/scientific acceptance. E2's
   [bounded collection plan](pending_proposals/qualify_small_ligand_collection.md)
   is #81; its study-level prioritization must not weaken strict pose ranking or
   move molecular work into DockingMT.
6. Select/qualify the actual functional release candidate only when every row's
   evidence supports the complete declared scope; perform the version-specific
   release/package/notice route. Enter stabilization afterwards.

## Ownership and completion discipline

DockingMT owns docking protocols, backend result meaning, score/ranking policy,
workflow orchestration and interpretation. Molecular inspection, characterization,
editing, coordinate projection, identity, matching and reusable geometry belong
to MolSysMT. Inspect existing supported APIs/issues first; report missing tools
in their provider with concrete consumer evidence and receive their contracts.
Specialized capabilities retain their own component owners; MolSysViewer owns
generic rendering/communication, while DockingMT owns its addon semantics.

The maintainer explicitly reaffirmed this boundary and the MolSysMT issue route
on 2026-11-06. It remains a requirement throughout the active goal. Preserve local
sibling work and inspect immutable remote/provider sources separately from
qualified runtime pins. No molecular fallback or guessed chemistry can satisfy
a missing provider requirement.

The remaining general molecular bridges tracked by #49 must be received from
their provider for the accepted input profiles. Do not obtain completion by
silently dropping an accepted prepared/partial-input workflow or treating an
unknown molecular state as verified. Numerical admission of DockingMT's own
serialized records and backend-specific score interpretation remain consumer
responsibilities; reusable molecular work does not move here.

Completion requires a requirement-by-requirement evidence audit, with the actual
candidate/artifact, dependency closure, native/software/scientific/installed and
visible scope matched to each claim. Pending evidence remains pending. Scope
selection, tests of a helper, source equality or a private installation cannot
substitute for another acceptance category. The goal stays active until the
complete functional objective and appropriate 0.x.0 consolidation are verified.
