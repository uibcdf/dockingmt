---
summary: Select active ligand torsions for Vina preparation
issue: uibcdf/dockingmt#6
status: partial
opened: 2026-09-22
closed:
verification: measured
area: [preparation, vina]
guard: tests/test_rigid_fragment_consumption.py::test_original_matrix_preserves_tree_and_consumes_provider
normative:
blocked_by: []
supersedes: []
---

# Select active ligand torsions for Vina preparation

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial; DockingMT Core MVP work.

## What

Allow the docking protocol to choose which candidate ligand bonds are active torsions.

## How

Consume MolSysMT rotatable-bond and rigid-fragment information, expose explicit selection or a documented default, and pass the selected torsions to the PDBQT writer.

## Why

The present ligand preparator defaults to zero torsional degrees of freedom, while flexible-ligand Vina input requires a valid torsion tree.

## What is measured and what is assumed

**Inspected:** Inspected dockingmt/preparation/ligand.py; no flexible-ligand validation fixture was measured.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

An unrecorded hard-coded torsion count was rejected because it cannot identify which bonds were flexible.

## Scope and exclusions

Docking protocol choice and provenance remain in DockingMT. General
rotatable-bond classification and rigid-fragment derivation belong in MolSysMT
under molsysmt#224. The current local graph bridge is temporary. PDBQT
ROOT/BRANCH serialization is also a temporary local implementation pending
MolSysMT's general PDBQT form in molsysmt#214.

## Acceptance criteria

- The selected active bonds and resulting torsion degree of freedom are inspectable for each ligand state.
- A flexible ligand reaches Vina with a valid tree, and invalid or unavailable torsion choices fail explicitly.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#214, uibcdf/molsysmt#224.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## 2026-09-22 progress

DockingMT's current PDBQT writer emits a rigid ROOT block and no BRANCH records.
It now rejects nonzero `torsion_dof` at preparation and export, rather than
writing a misleading TORSDOF count. The rigid policy is recorded in prepared
ligand metadata and therefore in Vina run provenance. This does not implement
active torsion selection or flexible-ligand PDBQT writing; the proposal stays
open pending the provider capabilities in molsysmt#214 and molsysmt#224.

## 2026-09-26 explicit torsion bridge

`VinaProtocol(active_torsion_bonds=[...])` now passes explicit selected-ligand
bond pairs into automatic MolSysMT ligand preparation. `prepare_ligand` accepts
the same selection directly. The temporary graph bridge in
`dockingmt/preparation/_temporary_torsions.py` consumes MolSysMT's public bond
pairs and orders, rejects non-single, ring, amide C–N, hydrogen, and terminal
heavy-atom bonds, and derives a deterministic rigid-fragment tree. The PDBQT
writer emits matching `ROOT`/`BRANCH` records and `TORSDOF`; it records the exact
PDBQT atom permutation so Vina poses reconstruct against source MolSysMT atom
identity. This bridge must be removed in favor of MolSysMT's implementation of
[#224](https://github.com/uibcdf/molsysmt/issues/224) once that API passes the
same cases and preserves the source map. The default remains rigid; there is no
unqualified automatic torsion-perception policy.

The [pinned 1IEP audit](../validation/1iep_preparation_audit.md) maps the seven
published BRANCH bonds to the molecular source and selects those bonds explicitly.
The native flexible writer retains all 40 matched atoms and emits seven branches
and `TORSDOF 7`. A separate conventional hexane case is accepted by Vina and
reconstructs its returned pose against MolSysMT after the PDBQT atom-order
permutation. These are software and reference-conformance results; they do not
validate ligand charges or atom types. The proposal remains partial until the
MolSysMT provider operation replaces the temporary graph bridge.

The expanded audit compares undirected branch bonds and rigid-fragment atom sets,
independently of root orientation and PDBQT serials. The native 1IEP projection
matches all seven published branch bonds and eight fragment sets. This confirms
tree serialization for explicitly supplied reference bonds, not automatic
torsion perception. RDKit 2025.09.5 counts seven `Strict` rotatable bonds on the
hydrogen-suppressed source and eight with `NonStrict`. A separate ethyl-acetate
probe (`CC(=O)OCC`) shows that the current bridge permits selecting the ester
acyl C–O bond while RDKit `Strict` excludes it. Chemical eligibility rules
therefore need an explicit provider policy; this discrepancy was reported in
[MolSysMT #224](https://github.com/uibcdf/molsysmt/issues/224#issuecomment-5844981980).
MolSysMT's existing `get_covalent_blocks(remove_bonds=...)` already supplies
basic bond-cut connectivity; the provider gap includes chemical classification
and a stable atom-identity-preserving fragment contract.

The [minimal pinned matrix](../validation/vina_torsion_matrix.md) adds Vina
1S63 and the 5X72 P59/P69 stereoisomer pair. All four reference-selected
trees match the published branch bonds, source-index rigid fragments, and
MolSysMT covalent blocks; Vina accepts the native PDBQT. In 1S63 the published
aryl–C≡N branch gives six Vina torsions versus five RDKit `Strict` torsions.
Docking-specific handling of that difference and the ester case is tracked in
[DockingMT #17](https://github.com/uibcdf/dockingmt/issues/17). The matrix
exposed and guarded a separate four-character PDBQT atom-name defect, archived
under [DockingMT #18](https://github.com/uibcdf/dockingmt/issues/18).

## 2026-10-03 provider partition migration

The final local partition now consumes public `msm.topology.get_rigid_fragments`
on the complete structure-assigned graph, followed by explicit retained-axis
membership projection and DockingMT ROOT orientation. All four original reference
cases preserve pre-migration atom permutations and PDBQT byte hashes. Thirteen
new controls pass on Python 3.14.7, including nonmonotonic axes, ROOT ties,
incomplete graph rejection and a structure-assigned chemical state distinct from
the reference. Source coordinates, bonds and IDs remain unchanged.

The [migration record](../validation/rigid_fragment_consumption.md), executed
notebook and captured baseline retain the evidence. The old final partition loop
is removed; temporary connectivity/individual-cut chemical checks and PDBQT
serialization remain. No automatic torsion policy is qualified; #6 stays partial.

## 2026-10-06 chemical eligibility migration

The [explicit policy contract](../validation/explicit_torsion_policy.md) now
consumes public `get_rotatable_bonds` on the complete structure-assigned graph,
retaining criteria/exclusions/software and selected positions/IDs in
`torsion_selection`. Local amide/ring/order/terminal duplication is removed.
Explicit ester/thioester and triple-adjacent cuts remain recorded docking
exceptions; restricted C–N rejects amidine and tertiary-amide controls too.
Default preparation remains rigid.

All four original generated byte hashes/permutations stay exact. The
[executed notebook](../validation/explicit_torsion_policy_2026-10-06.ipynb)
retains full reports and written maps; real default Vina automatic preparation
keeps them with named charge/type provenance through result JSON. Scientific
preparation/barriers remain unassessed.

One retained-connectivity traversal remains under
[MolSysMT #348](https://github.com/uibcdf/molsysmt/issues/348), with assigned-state
and subset removal conditions and review date 2027-01-06. PDBQT/H/charge-preserving
export stays #33/provider #223. This issue remains partial for those migrations
and publication/checkpoint boundaries. No automatic selection is qualified.

Final local source evidence: **977 passed without skips in 271.81 s** on Python
3.14.7/Vina 1.2.7, including 25 new policy cases. Eight notebook code cells,
Ruff/report/index/link/hash/identity/component-guide/diff gates pass. See the
[checkpoint](../validation/data/torsion_policy/checkpoint_2026-10-06.json) for
source/test digests and outstanding installed/hosted/public scope.

## 2026-10-07 matched real 1IEP sensitivity

The [named 1IEP workflow](../validation/1iep_flexibility_workflow.md) supplies twelve actual matched searches: rigid versus seven explicit provider-candidate axes, seeds 7/42/2026 at exhaustiveness 1/8. Original SDF chemistry/H, named charges/types, source identity and the same external receptor are fixed. Exact submitted bytes, full 40-atom source-key evaluation and separate independently guarded 37-heavy-atom RMSDs are retained. The bound-like rigid starting conformation is a favorable control; no affinity, general flexibility advantage, automatic torsion choice or native receptor-preparation qualification is claimed. The existing MolSysMT #348/#223 migrations and wider scientific criteria remain open; this report stays partial. Prior qualification receipts are unchanged.

## 2026-10-07 ROOT/order sensitivity

The [1IEP representation controls](../validation/1iep_representation_workflow.md) keep chemistry, selected cuts and rigid fragments fixed while comparing published/native bytes and an eight-atom ROOT reversal. Input score components agree, but returned near-native sets differ across the matched seeds/efforts. The first ROOT atom determines Vina's rigid-body origin, so serialization order is part of the executed search representation. Exact bytes and source maps remain necessary; no new default root policy or reusable downstream writer is introduced. #6 remains partial for the documented provider migrations and wider scientific scope.
