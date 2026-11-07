---
summary: Qualify a bounded multi-ligand study with isolated outcomes and explicit comparison policy.
issue: uibcdf/dockingmt#81
status: partial
opened: 2026-11-06
closed:
verification: measured
area: [screening, provenance, scientific-validation]
guard:
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
