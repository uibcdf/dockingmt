---
summary: Qualify a bounded multi-ligand study with isolated outcomes and explicit comparison policy.
issue: uibcdf/dockingmt#81
status: resolved
opened: 2026-11-06
closed: 2026-11-07
verification: measured
area: [screening, provenance, scientific-validation]
guard: tests/test_batch.py::test_recorded_failure_preserves_prior_results_and_next_item
normative: devguide/MVP.md
blocked_by: []
supersedes: []
---

# Small ligand collection qualification

## What

Complete E2 in the [functional plan](../PRE_STABILIZATION_PLAN.md): a small
declared ligand collection against one fixed receptor/domain, serial execution,
isolated failures, traceable identities and scientifically bounded aggregation
and prioritization. The accepted scope requires distinct ligands; several poses,
conformers or seeds of one ligand do not become a multi-ligand study.

## How

First admit actual source/state/preparation evidence for a finite collection.
Use public MolSysMT tools for all molecular acquisition/conversion, chemical
inspection, identity, transformations and geometry. Request uncovered reusable
needs in MolSysMT and receive supported existing compositions before proposing
new APIs. Existing #49/#33 and relevant provider issues retain their owners.
Do not generate missing chemical evidence in DockingMT.

Reuse `dock_many`, `DockingOutcome` and individual result records. A caller-owned
manifest associates study/run/ligand/state identities with each input position,
outcome, original result and input hash; an iterator index is not any of those
identities. Store all submitted/attempted/completed/returned/evaluated counts and
missing/refused/failed/successful-empty dispositions. Retain one informative
failure between successful items without weakening propagation of memory,
process-control or source-iterator failures.

Define a study-level comparison policy before new implementation or scientific
execution. Declare the fixed receptor/site, method/version/weights, preparation
scope, units, native score-reference meaning, selected named score, missing
values, ties and per-ligand representative selection. Preserve original scores,
pose ordering and provenance. Different ligands are intentionally different
states: cross-ligand prioritization is a separate scientific policy, not evidence
of same-state identity. E1 [#78](../archive/qualify_same_state_rescoring.md) owns related
native reference evidence. Any needed extension remains docking-specific.

Then register exact inputs/artifacts/producer, finite serial resources/calls,
controls, tolerances and failure policy before computation. Keep the current
local E4 computational hold and shared-machine resource constraints. This report
registers no dataset, numerical hypothesis, scientific budget or execution.

## Why

Inspection at `988d8a1cd9cc069d2d44d3bd229cd1ff10fc780f` establishes:

- Closed #36 delivered the incremental prepared executor and explicitly excluded
  whole E2/cross-ligand ranking. Its controls are useful software evidence.
- `DockingOutcome.index` is a zero-based position; original result-local pose IDs
  are not globally unique study IDs. Detached declarations preserve caller data.
- `DockingResult.rank_by` requires compatible score declarations and equal
  molecular-state identities. Preserve that conservative within-result contract.
- `summarize_redocking` aggregates compatible reference-recovery observations.
  Its fractions are not affinity, enrichment or general screening rankings.

The inspected `moli-vertical-pilots` source
`2e90db1ef20a12b9207c4713340809b01bd0f020`, TcTIM Phase 1 section 10,
suggests justified target/site choice, traceable Candidates, chemical context
and explicit ranking/refinement limitations. Its target-exclusion control treats
a traceable STOP as useful science. These guide the composition; no TcTIM
discovery campaign or biological admission is inferred. Project decision/history
and reusable workflow semantics remain with their platform owners, Nextia and
Praxis. Specialized pocket/pharmacophore work retains TopoMT/PharmacophoreMT.

## What was refuted

Do not concatenate different ligands into a fabricated single result, erase
state/byte identities, weaken `rank_by`, invent chemical equivalence from labels
or use the best score name as universal affinity. Pose/conformer counts cannot
inflate independent ligand or experimental denominators. Unknown experimental
activity is not an inactive control. Biological enrichment/selectivity needs
suitable separate labelled evidence.

No generic scheduler, growing batch cache, automatic preparation/retry, compound
database downloader, chemical deduplicator or platform campaign model is needed
to qualify this accepted small study. Notebook code composes scientific choices;
reusable provider functionality stays with its owner.

## Scope and exclusions

This report owns E2 workflow and concrete study-comparison admission. No runtime
API or changed schema is selected before the actual admitted workflow needs it.
An existing supported composition may suffice. No molecular fallback, dependency
pin change, native run, public package or release is introduced by scoping.
The full Core+Extended, E3/E4/E5, scientific panel and public/visible gates remain
separate. Preserve fixed private 0.1.0 and all original producers.

## Acceptance criteria

- A transparent bounded distinct-ligand collection has traceable source/license,
  explicit chemical states/provider evidence, intended question and limitations.
- Existing serial execution and records retain correct identities, all outcomes,
  original bytes/producers, denominators and informative adverse controls.
- Study prioritization has explicit comparable/incomparable conditions, honest
  native score meaning, units, missing/tie policy and selected-pose attribution.
  Original per-result score/ranking histories and strict APIs remain intact.
- Exact-source installed receiving and fresh detached readers verify the actual
  composition and immutable records, including nondefault units and failures.
  Register resources and computational populations before calculation.
- Required software/scientific evidence matches the claimed workflow. Planning,
  one helper or a substituted backend alone does not accept E2 or screening
  effectiveness. Any uncovered molecular need has an owning MolSysMT issue.


## Current two-source admission — 2026-11-07

The [candidate declaration](../validation/e2_ligand_collection_admission_2026-11-07.md)
selects existing licensed 5X72 P59/P69 inputs, a common protein-only receptor and
joint two-site domain, for functional collection receiving. P59/P69 are distinct
stereochemical entities, one complex and no activity labels. Historical fixed-
companion receptors and reference geometries remain separate populations.

The [registered source-only receiving](../validation/e2_source_admission_2026-11-07.md)
now passes for both exact SDFs through explicit public native/RDKit/native
interpretation: R/S, 39 atoms, 42 bonds, 15 indexed H, preserved axes/coordinates,
source nonmutation, four readiness reports and two complete new-authority self-
witnesses. Missing H/aromatic declarations become explicit; integer bond-order
coverage becomes partial under the recorded aromatic representation. Preserve
that transformation, non-exhaustive conversion reports, raw SD properties and
all unassessed science. A fresh standard-library reader receives the sealed
records without molecular work. No new H, charges, types, preparation, energies,
searches, H5/MM restoration or Vina import occurs.

This is partial source admission, not E2 execution or chemical/biological
validation. The next increment must register exact source reproduction and named
charge/type/preparation receiving before any native collection call. It then
needs the three-item success/refusal/success composition, actual native protocol/
resource prescription, explicit study comparison and independent saved receiving.
Keep the proposed total-score display separate from E1 same-state comparison,
preserve all five native energy columns and the four public scores, and retain
failure/empty/unknown denominators. No API expansion is justified by this source
receiving alone.

## Named rigid preparation received — 2026-11-07

The [separately registered preparation receiving](../validation/e2_preparation_receiving_2026-11-07.md)
now passes for both reproduced admitted authorities. Two fresh named
Gasteiger–Marsili/AutoDock4 calculations and rigid preparations retain R/S,
source chemistry/coordinates, derived mechanical lineage and complete source/
prepared/export mappings. Each output has 25 atoms and 28 bonds, with fifteen
represented H: one indexed and fourteen virtual after provider nonpolar-H
projection. Public charge audits, full-precision conservation, exact exports,
rigid trees, public readback, retained-axis self-witnesses, nonmutation and the
pm/fs/coulomb policy pass. Named parameters and an available stored H inventory
do not clear chemical/experimental validity questions; partial bond-order
coverage and readiness's unassessed checks remain explicit.

Both the molecular selection and fresh standard-library reader pass without
interruption. The [120-member archive](../validation/data/e2_preparation_receiving_2026-11-07/manifest.json)
has root SHA-256 `bd4f34c7c696efa1c864c9ea410630398b5ec164726eeaaf6462ea9d9b78d326`.
Qualification base is `782fe9e`, notebook is `76df8d7`, and the installed
consumer remains `a7422df` with the same identified providers. Zero H generation,
energies, searches, H5/MM restoration or Vina import occurs. Public delivery,
hosted CI and complete E2 retain their separate gates.

Next prescribe the three-item native collection and empirical study policy.
Fresh source/assignment/preparation reproduction must match the received P59/
P69 PDBQT hashes before any new native call. Keep the common receptor/joint
domain, actual five-column native energies and all outcome denominators. Reuse
serial `dock_many`; no generic framework, molecular codec or relaxed E1 ranking
contract is justified by this receiving.

## Bounded acceptance and resolution — 2026-11-07

The original five acceptance criteria are received for the declared two-ligand
rigid25 joint-domain workflow. This closes #81's finite qualification theme;
it does not accept arbitrary ligands, general screening effectiveness, public
package delivery, whole E2 in every profile or the complete #73 objective.

| Original criterion | Actual receiving evidence / limits |
| --- | --- |
| Transparent distinct-ligand collection | Source archive `a5a60b6` and preparation archive `bd4f34c` receive licensed P59(R)/P69(S), declared states and source/prepared maps. One complex/two experimental sites, no activity labels; receptor preparation remains external/unassessed. |
| Serial execution, identities, all outcomes and adverse control | [Original native receiving](../validation/e2_native_collection_2026-11-07.md) returns success/refusal/success at positions 0/1/2, preserving run/state/result/pose identities, three terminal outcomes, two native searches and 3+2 original poses. `DMT-E003` adds no native/writer calls and the final item completes. Byte gates, live nonmutation, temporary cleanup and all denominators pass. |
| Explicit study comparison | Policy `d7bae710` is frozen before search. Unique original-rank-1 representatives yield native totals -11.462/-10.787 kcal/mol, with all five columns and original four public scores/histories retained. Per-search reference zeros are not a common unbound reference. Missing/tie/empty/incompatible rules remain declared; those adverse scientific branches are not observed in this two-row order. No E1 cross-state ranking API is relaxed. |
| Installed and independent saved receiving | Exact consumer source `a7422df`, 3,867-file private payload, 103-path Vina/Boost overlay, source/provider identities, both input archives, pm/fs/coulomb policy/restoration and staged support pass. Three public outcome reconstructions pass. A fresh standard-library reader receives all 166 native members plus 80 source/120 preparation members, original NPY/JSON arrays, outcomes, maps, policies and records with zero molecular/native calls. This is controlled private evidence; actual public/platform delivery stays #30/#47. |
| Evidence matches workflow and ownership | The real native selection and independent reader pass, followed by eleven selected software controls. General molecular work remains public MolSysMT; existing DockingMT composition suffices without a new API, codec or campaign framework. Core, E3/E4/E5, independent science, public delivery and stable-release gates keep their owners. |

The [193-member immutable native archive](../validation/data/e2_native_collection_2026-11-07/manifest.json)
has SHA-256 `4535ecab26c9fbe4d80bf50fabb48ec3a74ae067979f4e970f5523f703c98e46`.
Native selection is 28.21 s/652.48 MiB sampled peak group RSS; the fresh reader
is 3.80 s/51.78 MiB, with no resource interruption. Native stderr preserves the
expected capability diagnostic. These are finite receiving timings with their
recorded/missing host context, not portable performance claims. All original
source/preparation/native producers and raw data remain unchanged.

The durable guard directly asserts that an ordinary item failure preserves the
prior result and permits the third item. Its source-iterator/exception behavior
remains the existing executor contract. The additionally executed
`tests/test_backend_contracts.py::test_vina_rejects_unsupported_intent_before_hooks_or_execution`
asserts the actual DMT-E003 pre-execution refusal across list/dict intent and
both direct/public dispatch. These selectors protect the mechanisms exercised
by the native middle control; they do not establish ligand chemistry or all
unobserved ranking branches. Both named targets are mechanically addressable.

The [software guard receipt](../validation/data/e2_collection_guard_receiving_2026-11-07.json)
preserves the first collection failure (missing Vina Python path) and the
complete corrected 11-pass selection. The correction uses the existing
received overlay, with no environment installation, changed scientific
protocol, repeated preparation or additional search. The original failed
attempt is not relabelled as a pass.

Thirteen applicable local documentation/index/archive/resource/publication
checks pass, including a fresh source export with the exact final changes.
Publication also requires fresh receiving of the actual committed source.
Exact-head hosted evidence
stays missing under #28 and `[skip ci]`; no manual remote workflow is launched.
The next independent Extended workflow is provider-owned pose comparison/
clustering under #79/MolSysMT #604. Keep E4/live-visual holds and the remaining
full-plan requirements unchanged.
