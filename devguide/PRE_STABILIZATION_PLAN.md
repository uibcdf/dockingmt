# Core and Extended delivery before stabilization

Owner: [DockingMT #73](https://github.com/uibcdf/dockingmt/issues/73).
Accepted maintainer objective: 2026-11-06, [DMT-046](DECISIONS.md#dmt-046--deliver-the-complete-functional-objective-before-stabilization).
Status: **active; completion unproven**. Inspected starting source: `530a4cf`.

## Outcome and version boundary

Deliver the complete Core C0–C6 and Extended E1–E5 workflows, bounded scientific
qualification, independent reproducibility and public installation as the
prospective **0.5.0** functional milestone in the existing
[release ladder](RELEASE_MILESTONES.md). Then stabilize the accepted surface across the
ordinary 0.x.0 releases actually needed; reserve 1.0.0 for the subsequent
stable-release decision. [DMT-048](DECISIONS.md#dmt-048--let-pre-10-versions-follow-verified-progress)
removes a mandatory 0.9.0 endpoint; 0.23.0 is illustrative, not selected. This identifies
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
| E1 named rescoring/ranking | Existing poses acquire distinct named evaluations; original scores survive; declared comparable collections can be ordered and audited reproducibly. | [#78 resolved](archive/qualify_same_state_rescoring.md#bounded-acceptance-and-resolution--2026-11-07) for the full-source rigid prepared13 profile: both actual original poses complete public reconstruction/preparation/additive Vina/Vinardo 1.2.7 scoring and separate method-local interaction comparison. Eight old values/ranks/history survive with 32 new values; native receiving and independent persistence pass. The original generator qualification remains failed with unreached original live checks. Broader E1, total/reference comparisons, independent science and public delivery retain their owners. |
| E2 modest ligand collections | A declared study isolates individual failures, retains ligand/state/run identity and supports scientifically delimited aggregation/ranking. | [#81 resolved](archive/qualify_small_ligand_collection.md#bounded-acceptance-and-resolution--2026-11-07) for the P59(R)/P69(S) rigid25 joint-domain profile. Source/preparation reproduction and exact PDBQT gates precede native success/refusal/success, 3+2 poses and two original-rank-1 representatives. Five native columns, own per-run references, original scores/histories, three public outcome reconstructions and fresh independent receiving pass. The receptor remains externally prepared/unassessed; other E2 profiles, screening effectiveness, #73 and public delivery remain unaccepted. |
| E3 comparison/clustering | Supported pose/reference and pose/pose measurements and useful clustering with explicit populations, correspondence, units, method/thresholds and degeneracies. | #79 scopes the concrete positional workflow. MolSysMT #604 requests supported bounded pairwise/clustering tools or an existing composition; no local molecular algorithm. |
| E4 interaction analysis | A minimal structured interaction record supports interpretation/filtering/visualization with named molecular definitions, selections, units, identities and unsupported cases. | #80 receives one bounded installed 3PTB workflow at `5952053`: normal/pm-fs, twelve detector calls, typed/H5MSM persistence, original-pose association and two fresh readers pass. Preserve prior failures and the local hold. Structured consumer/addon admission and whole E4 remain unproven; molecular operations stay in MolSysMT (#610 documents explicit XYZ atom extraction). |
| E5 independent reproduction | A separate receiving installation reconstructs a representative stored workflow from documented inputs, with observed agreement/tolerances, failures and missing information. | Captures/replay/recovery supply pieces; a whole independent workflow audit remains unproven. |
| Bounded scientific qualification | An admitted transparent independent panel and informative positive/adverse controls, explicit preparation/search/ranking hypotheses, denominators, budgets and all outcomes. | Audit Q2–Q4 and #33/#49 own admission. Existing within-case repetitions do not become independent complexes. |
| Public delivery and support | Actual compatible public dependencies, exact staged Conda artifact, required source/native gates and eight Linux/macOS arm64 × Python 3.11–3.14 installed cells, same-byte promotion and public receiving. | #30/#47 remain partial. Refresh artifact availability before acquiring/receiving; old private receipts do not certify a new public file. Distribution is Conda `uibcdf`. |
| Usable API/records and documentation | Coherent documented public contracts, examples, schema/quantity/diagnostic behavior, migrations for intentional changes and explicit scientific limits. | Preserve existing contracts and receive changes with applicable guards. Functional delivery precedes the later stabilization/final-compatibility decision. |
| Resource control | Caller-visible execution limits, isolated failures and measured representative CPU/RAM behavior without silent global caches or whole-machine assumptions. | Reuse serial execution; local agent qualification remains one logical CPU, low priority, one native/build worker, monitored reserve and no automatic heavy restart. #28/#50 own evidence/custody. |

## Immediate sequence

1. Keep exact-source hosted evidence missing under #28 while the incremental
   `[skip ci]` route applies; run applicable local checks without manual CI
   dispatch. The [machine handoff](MACHINE_HANDOFF.md) identifies the passing
   pre-handoff head; a later head needs its own applicable evidence.
2. Preserve the [bounded resolved E1 profile](archive/qualify_same_state_rescoring.md)
   and its original reference/provider/native/persistence records. No repeat
   search or relaxed ranking is needed for its acceptance. The old generator
   remains failed; the complete fresh receiving passes its own controls.
3. Preserve the [bounded resolved E2 workflow](archive/qualify_small_ligand_collection.md)
   and its [native/persistence evidence](validation/e2_native_collection_2026-11-07.md).
   Two source/named-preparation reproductions match the admitted exact bytes;
   the three-item public serial selection receives two searches, the intervening
   DMT-E003 refusal, five original poses and two representatives under the frozen
   caller-owned policy. Native totals -11.462/-10.787 kcal/mol retain five columns
   and separate per-run references; no common unbound reference or affinity is
   inferred. All three public outcome roundtrips and the fresh saved reader pass.
   No repeat search, runtime expansion or relaxed same-state ranking is needed.
   Next advance independent E3 under #79/MolSysMT #604 by receiving its actual
   supported composition/tools before implementation or new molecular work.
4. Keep complete-source public MolSysMT compositions as the received route.
   [MolSysMT #599](https://github.com/uibcdf/molsysmt/issues/599),
   [#447](https://github.com/uibcdf/molsysmt/issues/447) and #521 retain broader
   provider/partial-input scope. Request demonstrated gaps there; no local
   molecular fallback or guessed historical chemistry follows.
5. Scope and qualify the remaining E3–E5 workflows with their owners and receive
   outstanding Core, broader E1/E2, scientific, visual and public-delivery evidence.
   Independent requirements may progress while a provider or hosted run is pending.
   E3's [provider-backed contract](pending_proposals/qualify_pose_comparison_and_clustering.md)
   is #79/MolSysMT #604; E4's
   [existing-tool receiving](pending_proposals/receive_docking_interaction_analysis.md)
   is #80. Their [dated inspection](validation/extended_provider_scope_2026-11-06.md)
   is not runtime/scientific acceptance. E2's
   [bounded resolution](archive/qualify_small_ligand_collection.md)
   preserves strict pose ranking and molecular ownership; it does not accept all
   E2 profiles or the complete #73 objective. Keep E4/live-visual holds unchanged.
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
on 2026-11-06. It remains a requirement throughout the accepted development
scope. Preserve local sibling work and inspect immutable remote/provider sources separately from
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
substitute for another acceptance category. The accepted product objective stays
incomplete until the full functional outcome and appropriate 0.x.0 consolidation
are verified. Session/automation status is separate: the previous autonomous goal
was paused and cleared before the [new-machine handoff](MACHINE_HANDOFF.md).
This product plan does not restart execution.
