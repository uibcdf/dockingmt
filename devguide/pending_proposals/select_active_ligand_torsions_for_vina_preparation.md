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

## 2026-10-07 fixed-first-ROOT order control

The [fixed-origin 1IEP workflow](../validation/1iep_root_order_workflow.md) adds six declared searches and one initial score. Only the seven ROOT ATOM lines after unchanged source N28 are reversed; its origin, all line bytes/serials/labels, ROOT membership and branch records remain fixed. Near-native first poses/returned sets occur in 6/6 cells versus 1/6 in the authenticated native observations, with equal initial score components. Order sensitivity in this case therefore does not require an origin change. All 18 earlier matrix cells and their producers remain unchanged by reference. No default ROOT policy, recovery probability or general preparation validity is selected. Alternative starting conformers and independent complexes remain next scientific challenges; existing provider #223/#348 migrations and wider acceptance remain open.

## 2026-10-08 alternative-conformer challenge

The [1IEP input challenge](../validation/1iep_conformer_workflow.md) uses public
MolSysMT to shift one declared central torsion by +/-60 degrees, preserving
original chemistry/H, covalent geometry, exact cuts and source/written identity.
Twenty-four new matched searches evaluate against the original crystallographic
reference, not the perturbed input. First/returned-set recovery counts are
+60 native 0/6 versus fixed-first 3/6, and -60 native 4/6 versus fixed-first 3/6.
The historical native 1/6 and fixed-first 6/6 remain authenticated original
observations. No ROOT default or general conformer robustness follows.

The +60 fixed score agrees across orders; both -60 fixed scores are refused
outside the unchanged grid while docking succeeds. Unminimized-input and
preliminary unretained-attempt limits are documented. All final cells, captured
bytes and independently checked reference metrics are retained. Local scope
passes 66 distinct tests without skips and three saved-result notebook cells.
Existing provider #223/#348 migrations and broader scientific acceptance remain
open; independent complexes are the next challenge.

A dated consumer guard correction compares portable annotation bytes within
the current runtime instead of requiring historical installed-version strings.
Strict-profile controls reproduce the original saved cases exactly; science
stays at producer `27a18ef` without new searches. Five current guards pass and
the unchanged 62 boundary cases remain applicable (67 total). The corrected
head requires fresh exact-head CI; this issue remains partial.

## Independent 5X72 ROOT-order challenge — 2026-10-09

The [prespecified plan](https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6080145389)
adds an independent complex after the 1IEP conformer controls. The
[workflow](../validation/5x72_root_order_workflow.md), raw 24-cell/99-pose archive,
executed saved-result notebook and `tests/test_5x72_root_order_workflow.py` retain
both P59/P69 inputs, original experimental references and all explicit
written/source/reference mappings. The other experimental ligand is absent in
each search; this does not reproduce simultaneous-ligand docking.

Keeping the first ROOT atom/origin fixed and reversing the other eleven ROOT
lines gives first-pose recovery **0/6 in all four arms**. P59 returned sets recover
**3/6 native, 4/6 first-fixed**; P69 returned sets recover **0/6 in both orders**.
All exhaustiveness-8 P59 cells include a near-reference pose, but it is not ranked
first. The prepared hydrogenated SDF geometries are not experimental coordinates;
the original heavy-only SDFs and independent PDB instances supply the references.
The original unversioned crystal SDF dialect is reported in
[MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215#issuecomment-6080146217),
with an explicit existing RDKit reference bridge, unchanged fixture bytes and no
sibling source edits. The pinned solution box controls the experiment.

These observations refute adopting the favorable original 1IEP ROOT permutation
as a generally supported recovery policy. They do not isolate occupancy,
preparation, conformer or ranking causes, or establish affinity/stereoselectivity,
convergence or recovery probability. Source/native profile and historical producers
remain unchanged; local guards and hosted source CI qualify software separately
from the scientific observations. The proposal remains partial/open. Control
experimental co-occupancy and distinguish sampling from ranking in subsequent
work before changing defaults.

## Fixed-P69 occupancy and frozen-score control — 2026-10-09

The [matched 5X72 workflow](../validation/5x72_occupancy_workflow.md) keeps the
same P59 cuts, two torsions, ROOT orders and chemical inputs while comparing
protein-only sham against protein with fixed experimental P69. The 24 new
searches recover first-ranked P59 in 0/12 sham and 10/12 occupied cells. Frozen
evaluation of all returned geometries changes the lowest-score choice to a
recovered pose in each of the seven sham sets that already contain one.
Search sampling and within-set score preference are reported separately;
no automatic torsion/root policy changes. The earlier P69 recovery problem and
broader scientific/provider acceptance remain open, so #6 stays partial.

## Reciprocal fixed-P59/P69 control — 2026-10-09

The [reciprocal workflow](../validation/5x72_reciprocal_workflow.md) searches
P69 against protein-only sham and fixed experimental P59, preserving its two
cuts, both original ROOT orders and all other declared inputs. Any-returned
recovery changes 0/12 to 7/12, including all six occupied effort-8 cells; first
recovery stays zero. Both frozen-score diagnostics select a nonrecovered pose
in every returned set containing a recovered geometry. All 78 new poses and
49 historical serialization controls are retained. This limits the earlier P59
inference and motivates separate reference-score/preparation work; no automatic
torsion, ROOT or ranking policy changes, and #6 remains partial/open.

## Experimental-reference and explicit-fragment diagnostic — 2026-10-09

The [reference workflow](../validation/5x72_reference_workflow.md) scores both
experimental heavy geometries with declared generated H, both original ROOT
orders and both saved receptors: eight fixed evaluations, no searches or
optimization. All 156 historical returned poses and 312 saved evaluations remain
in the comparison. P69's occupied reference is still beaten by ten nonrecovered
first-ranked poses, whereas P59's occupied reference beats every retained pose.
Public explicit-cut fragments and independently checked distances retain all
552 heavy pairs. Their internal differences limit exact experimental congruence
under the existing cuts, without establishing recovery failure or a new torsion
choice. This supplies evidence for separately prespecified geometry/score-basin
work, not an automatic classifier, optimization API or default. #6 stays partial.

## Reference-torsion conformer with original rigid fragments — 2026-10-09

The [rigid placement workflow](../validation/5x72_rigid_workflow.md) preserves
all original fragment/H geometry and bonds, applying only the two declared
experimental torsions and one public proper fit. Heavy positional RMSD is
0.513 angstrom for P59 and 0.679 for P69. Eight fixed scores and all 156 old poses
retain complete component/context evidence; the new P69 occupied point scores
7.832 kcal/mol worse than its earlier experimental-reference point. A valid
near-reference placement is therefore not enough to obtain a favorable fixed
score for this prescribed unrelaxed conformer. No optimized torsion or adaptive
selection policy follows. Original/generatedH differences and local contact
geometry need their own bounded diagnostic. MolSysMT#357 owns the inspected
angle-unit documentation finding; explicit quantity handling remains valid.
#6 stays partial/open.

## Exact prepared-input distance slice — 2026-10-09

The [saved-input contact diagnostic](../validation/5x72_contact_workflow.md)
checks both original ROOT maps before measuring eight complete cross-system
distance matrices. No cuts, tree, geometry, preparation or score is changed.
P69 short heavy protein pairs occur in the original-rigid placement at GLN116/
TYR149; descriptive bins neither identify energy terms nor select a flexibility
remedy. Original/generated H remains a confound. All old scientific evidence
is preserved; #6 remains partial/open.

## Prespecified displacement control — 2026-10-10

The [receiving qualification](../validation/5x72_displacement_workflow.md)
preserves the original 112 fixed evaluations and producer bytes. Both original
cuts/ROOT orders, chemistry/H, maps and internal geometry remain fixed while
public MolSysMT moves all 39 atoms through seven declared offsets. Full score
curves retain lower and non-improving points without introducing new cuts,
optimization, search or ranking policy. The three-cell saved-result notebook and
127 local controls pass; hosted exact-head evidence remains separate. This
scientific slice does not retire the provider #223/#348 boundaries. #6 stays partial.

## Independent prospective case — 2026-10-10

The [3PTB protocol](../validation/3ptb_prospective_protocol.md) prescribes a
rigid arm and exactly one explicit phenyl–amidine `C1–C` cut, with common
coordinates/state/H/charges/types and provider-validated fragments. It freezes
24 searches across two boxes, three seeds and two effort levels before execution.
ROOT/torsion alternatives cannot be selected after results; unsupported chemistry
or cuts stop admission and require provider evidence. No preparation or search
has yet executed, and the plan adopts no automatic torsion or ROOT policy.
#6 remains partial; existing molecular projection/connectivity migrations stay
separate.


## 2026-10-10 executed 3PTB admission

3PTB admission consumes MolSysMT candidate classification and rigid fragments for the sole explicit C1–C cut. Rigid and flexible arms have identical source-axis fields and saved ROOT/BRANCH representations, including their different first ROOT atoms. The 24-row population is frozen but unexecuted; no automatic torsion/default policy changes.

The [executed admission](../validation/3ptb_admission.md), [notebook](../validation/3ptb_admission_2026-10-10.ipynb) and separate receipt retain measured scope. Owning issues remain partial/open.
