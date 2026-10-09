---
summary: Define ligand torsion policy across RDKit and Vina reference differences
issue: uibcdf/dockingmt#17
status: partial
opened: 2026-09-26
closed:
verification: measured
area: [preparation, vina]
guard: tests/test_torsion_policy_consumption.py
normative:
blocked_by: []
supersedes: []
---

# Define ligand torsion policy across RDKit and Vina reference differences

## What

Decide the DockingMT protocol policy for ligand torsions when RDKit descriptors,
published Vina PDBQT branches, and explicitly selected bonds differ. The current
API accepts explicit bonds after bounded structural checks; it has no automatic
chemical classifier.

## How

Keep a small pinned [comparison matrix](../validation/vina_torsion_matrix.md)
with source atom IDs, selected branch bonds, rigid fragments, explicit hydrogen
differences, RDKit descriptor mode, and Vina parser acceptance. Define which
explicit requests remain valid, which fail or warn, and whether any automatic
policy can be justified. Preserve the chosen policy and source bond IDs in
preparation provenance.

## Why

For 1IEP, the published PDBQT has seven branches and RDKit `Strict` counts
seven, but the published bonds were supplied explicitly to DockingMT. In 1S63,
the published PDBQT has six branches while RDKit `Strict` counts five; the extra
branch is aryl–C≡N (source atoms 26–27). For ethyl acetate, DockingMT permits
an explicit ester acyl C–O torsion while RDKit `Strict` excludes it. Matching
one descriptor count cannot establish a general docking torsion policy.

## What was refuted

Treating RDKit `Strict` as the Vina branch oracle was refuted by 1S63. Treating
published Vina branches as chemically necessary was refuted as an unsupported
inference; they are comparison inputs. Comparing only `TORSDOF` counts was
refuted by tests where an incorrect cut has the same branch count.

## Scope and exclusions

DockingMT owns protocol-level selection and user-facing policy. MolSysMT
[#224](https://github.com/uibcdf/molsysmt/issues/224) owns reusable bond
classification and fragment contracts; MolSysMT
[#214](https://github.com/uibcdf/molsysmt/issues/214) owns eventual PDBQT
serialization. No Meeko runtime dependency or affinity-score claim is part of
this proposal. The temporary four-character atom-name defect was resolved
separately in [DockingMT #18](https://github.com/uibcdf/dockingmt/issues/18).
The 1S63 reference-only polar hydrogen has separate provider handoffs in
MolSysMT [#223](https://github.com/uibcdf/molsysmt/issues/223) for atom
correspondence and [#220](https://github.com/uibcdf/molsysmt/issues/220) for
state identity when hydrogen inventory changes.

## Acceptance criteria

- Document the exact torsion-selection policy and whether explicit overrides
  can include ester and aryl–nitrile bonds.
- Preserve source bond identity, hydrogen projection, and selected policy in
  preparation and docking provenance.
- Keep representative conformational and reference-tree tests; explain every
  RDKit–Vina discrepancy instead of enforcing numerical equality.
- Replace temporary graph classification only after MolSysMT #224 passes the
  same bounded cases and preserves atom identity.

## Progress, 2026-09-26

Pinned 1IEP, 1S63, and both 5X72 stereoisomers are covered by
`tests/test_vina_torsion_matrix.py`. The test compares branch bond IDs and rigid
fragments with the published PDBQT and MolSysMT's independent covalent blocks.
RDKit `Strict` and `NonStrict` counts are recorded separately after removing
explicit hydrogens. `tests/test_flexible_ligand.py` captures the ethyl-acetate
difference. Chemical-policy acceptance criteria remain open.

## 2026-10-03 Meeko source comparison

The [native capability review](../validation/meeko_native_capability_review.md)
inspects Meeko's amide/thioamide/amidine, tertiary-amide and nitrile-chain rules.
These are concrete policy comparison cases for MolSysMT #224 and this issue,
not a request to import Meeko or copy its defaults. Compare exact eligible bond
identities and induced fragments, with reasons for exclusions; descriptor or
TORSDOF counts alone remain insufficient. Chemical classification belongs in a
public provider operation; DockingMT chooses the docking policy and records it.

## 2026-10-06 public classifier and explicit docking policy

The [contract](../validation/explicit_torsion_policy.md),
[executed notebook](../validation/explicit_torsion_policy_2026-10-06.ipynb) and
[receipt](../validation/data/torsion_policy/qualification_2026-10-06.json) adopt
public `get_rotatable_bonds(method='conjugation_restricted',
chemical_state='structure', structure_indices=0)` before H projection. Original
criteria, full masks, state, software and attribution remain finite saved evidence.
Local amide/ring/order/terminal classification and per-cut traversal are removed.
Provider fragments and local ROOT retain the prior written order.

Named `explicit_docking_cuts@1` accepts provider candidates and caller-selected
restricted C–O/S or triple-adjacent axes as recorded `explicit_override`, without
clearing the provider rejection. Restricted C–N, ring, nonsingle, H and terminal
bonds fail. Amidine rejection is stricter than the former carbonyl-only guard;
amide/thioamide/tertiary amide stay restricted. No automatic cuts, symmetry
exceptions, macrocycle pseudoatoms, RDKit Strict equality or barriers are claimed.
Default rigidity and existing public signatures remain compatible.

Original 1IEP/1S63/5X72 P59/P69 keep exact hashes/permutations. Restricted provider
candidates are 7/5/2/2 versus selected 7/6/2/2; 1S63 source pair 26–27 records the
triple-adjacent exception. Six admitted analytical controls and four restricted
C–N failures retain independent expectations. Immutable inputs, complete H
context, reordered axes, assigned states and unchanged provider failures are guarded.

One retained-axis traversal remains under
[MolSysMT #348](https://github.com/uibcdf/molsysmt/issues/348): current public
connectivity tools cannot request the structure-assigned induced subset. The
two-state probe gives assigned offsets `[0, 3, 6]` versus one reference block and
retains the unsupported explicit request. Owner: DockingMT contributors; review
2027-01-06. Remove after public assigned-state/subset acceptance; documented
reference defaults are not alleged incorrect.

The sibling stays at committed `5bd893c85`; fetched remote is 14 commits ahead
with consumed topology files unchanged through `8ae160fc9`. Earlier #42/#43
receipts stay intact. Real default Vina automatic named/charged preparation,
two protocol cuts, pm/fs units, saved reports/maps and captured exact inputs are
exercised; scientific assessment remains unassessed. The helper's unrelated
5X72/1IEP combination is software evidence only. Publication/installed/hosted
checkpoints and scientific qualification remain separate.

## Refuted fixture assumptions — 2026-10-06

The first reordered-axis test assumed assigning a reversed table through the
native Topology property would retain row order; that supported setter normalizes
it. The final declared fixture reorders the state table as in the provider's own
axis tests, checking real source positions and preserved IDs. The first pose
reconstruction assertion indexed the returned 25-atom retained system with
indices from the original 39-atom input. The documented pose conversion omits
removed H; the corrected independent comparison uses atom IDs and verifies both
original-input correspondence and reconstructed coordinates. These were consumer
test assumptions, not demonstrated provider or pose-conversion defects.

## Final local gate — 2026-10-06

The final source candidate passes **977 tests, no skips, 271.81 s, 169 warnings**,
including 25 new controls and the strengthened four-reference provider guard.
Eight notebook code cells execute, retaining four original comparisons, six
admitted analytical cases and four C–N rejections. Ruff (120 files), report/index,
changed-document links, finite receipt/hash, installed editable identity,
component guidance and diff checks pass. The
[checkpoint](../validation/data/torsion_policy/checkpoint_2026-10-06.json) retains
exact consumer/test/evidence hashes and separate unexecuted/limited scopes.
Canonical SMonitor/ArgDigest drift and host AmberTools conflicts remain unchanged.
The issue stays partial/open; no push, hosted gate or public scientific admission
is claimed.

## 2026-10-07 matched real 1IEP sensitivity

The [named 1IEP workflow](../validation/1iep_flexibility_workflow.md) supplies twelve actual matched searches: rigid versus seven explicit provider-candidate axes, seeds 7/42/2026 at exhaustiveness 1/8. Original SDF chemistry/H, named charges/types, source identity and the same external receptor are fixed. Exact submitted bytes, full 40-atom source-key evaluation and separate independently guarded 37-heavy-atom RMSDs are retained. The bound-like rigid starting conformation is a favorable control; no affinity, general flexibility advantage, automatic torsion choice or native receptor-preparation qualification is claimed. The existing MolSysMT #348/#223 migrations and wider scientific criteria remain open; this report stays partial. Prior qualification receipts are unchanged.

## 2026-10-07 rooted-representation controls

The [matched rooted-representation workflow](../validation/1iep_representation_workflow.md) preserves the six original native flexible observations and adds twelve declared published/ROOT-reversed searches, three fixed-conformation scores and a separate native repeat. The same chemical payload and seven undirected cuts give near-native returned sets in 1/6 native, 5/6 published and 4/6 ROOT-reversed cases; all initial score components agree. The official Vina parser initializes the rigid body at the first ROOT atom, so the eight-line reversal also changes the origin. It establishes sensitivity of this representation/parametrization without isolating a cosmetic order effect or selecting a better general ROOT policy. Earlier evidence remains immutable; wider scientific cases, a fixed-first-atom order control and public provider export/correspondence remain open. #17 stays partial.

## 2026-10-07 fixed-first-ROOT order control

The [fixed-origin 1IEP workflow](../validation/1iep_root_order_workflow.md) adds six declared searches and one initial score. Only the seven ROOT ATOM lines after unchanged source N28 are reversed; its origin, all line bytes/serials/labels, ROOT membership and branch records remain fixed. Near-native first poses/returned sets occur in 6/6 cells versus 1/6 in the authenticated native observations, with equal initial score components. Order sensitivity in this case therefore does not require an origin change. All 18 earlier matrix cells and their producers remain unchanged by reference. No default ROOT policy, recovery probability or general preparation validity is selected. Alternative starting conformers and independent complexes remain next scientific challenges; existing provider #223/#348 migrations and wider acceptance remain open.

## 2026-10-08 alternative-conformer challenge

The [prespecified 1IEP challenge](../validation/1iep_conformer_workflow.md) shifts
original-source quartet 9–10–12–13 by +/-60 degrees through public MolSysMT,
retaining chemistry/H, covalent geometry and source identity. Each input starts
6.6994 angstrom from the original heavy reference and crosses native/fixed-first
written order with the same three seeds and two efforts: 24 new searches,
plus twelve authenticated historical bound-like references. Every final result
is evaluated against the original crystallographic geometry, with independent
full/37-heavy metrics and actual captured bytes.

Near-native first poses/returned sets are +60 native 0/6, +60 fixed-first 3/6,
-60 native 4/6 and -60 fixed-first 3/6. The earlier fixed-first 6/6 does not
persist across these inputs; no general ROOT default is selected. The +60
fixed-input score agrees under both orders (175.436 kcal/mol); both -60 scores
are refused outside the unchanged grid while their searches complete. Those
admission boundaries and unminimized-input limits remain explicit. An initial
uncommitted attempt's three in-memory preliminary outputs were not retained;
the complete declared matrix was rerun with per-cell retention and the limitation
is recorded rather than reconstructed.

Four new guards plus 62 scientific/reporting boundary tests pass without skips;
three saved-result notebook cells execute, including independent pm/fs
original-reference evaluation. Historical producers, archives and existing
provider #223/#348 migration scope remain unchanged. This issue stays partial;
independent complexes are the next scientific challenge.

The first hosted conformer run exposes a portable guard requiring historical
version-bearing REMARK bytes from an ordinary installed provider. The
[dated correction](../validation/1iep_conformer_workflow.md#portable-annotation-correction-after-first-hosted-ci--2026-10-08)
compares portable inputs within their actual runtime while keeping strict-profile
science authenticated. Five current guards pass locally; the unchanged boundary
scope brings the applicable total to 67. The 24 observations and original
producer `27a18ef` remain unchanged, and the corrected head needs fresh CI.

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

The [prespecified matched control](../validation/5x72_occupancy_workflow.md)
adds 24 new P59 searches against a same-writer protein-only sham and protein
plus fixed experimental P69. All protein fields and P59 chemistry/cuts/order
remain checked. All 78 new poses are scored unchanged in both environments;
50 authenticated historical P59 poses also control original-vs-sham serialization.
Sham trajectories reproduce those historical coordinates and docking scores.

First-ranked recovery changes from 0/12 sham to 10/12 occupied, including all
six occupied effort-8 cells. All seven sham returned sets containing a recovered
pose put a recovered pose first under occupied fixed scoring without moving any
geometry. The two remaining occupied low-effort failures contain no recovered
pose. This separates scoring changes within retained populations from sampling
changes under this fixed environment; it does not establish a general ROOT
policy, affinity, cooperativity or convergence.

Public MolSysMT `add` and native writing compose prepared rigid records.
[Provider #352](https://github.com/uibcdf/molsysmt/issues/352) owns mechanics merge
failures; [#353](https://github.com/uibcdf/molsysmt/issues/353) owns chain-ID loss
in add. The finite two-chain A/A declaration through public set is tracked in
the workflow with its removal condition. No sibling implementation is edited.
Wider complexes, the earlier P69 nonrecovery, provider migrations and preparation
qualification remain; this proposal stays partial/open.

The [dated portable correction](../validation/5x72_occupancy_workflow.md#portable-dataframe-annotation-correction--2026-10-09)
addresses Pandas 3 `str` annotations versus the original `object` snapshot in
three guard setups. Current-runtime references remain independently checked;
strict production retains the historical snapshot. A regression reproduces the
annotation change. The original scientific producer, archive and local capture
remain unchanged; five corrected guards and 207 retained applicable boundaries
give 212 local tests, and the corrected head requires fresh hosted CI.

## Reciprocal fixed-P59 control — 2026-10-09

The [prespecified reciprocal workflow](../validation/5x72_reciprocal_workflow.md)
adds 24 P69 searches with the original two ROOT orders, same box/chemistry/cuts
and matched receptor writing. Fixed experimental P59 changes any-returned P69
recovery from 0/12 sham to 7/12 occupied, including all six occupied effort-8
cells. First recovery remains 0/12 in both environments. All 78 new poses are
evaluated unchanged in both receptor contexts; neither frozen diagnostic selects
a recovered pose in the seven occupied sets containing one.

All 49 historical P69 poses control original-vs-sham serialization. The reciprocal
driver reuses the existing finite public composition/scoring/measurement tools;
historical archives and producers stay immutable. Provider #352/#353/#215 and
the checked finite A/A restoration retain their ownership/removal conditions.
This differs from the earlier favorable P59 first-recovery result and rules out
occupancy alone as a remedy for the measured P69 ranking discrepancy. A separate
reference-geometry/local-score control must state H mapping and optimization
policy before execution. No general ROOT, preparation, scoring or convergence
policy is established; the proposal remains partial/open.

The [dated guard correction](../validation/5x72_reciprocal_workflow.md#current-policy-guard-correction--2026-10-09)
records the original hosted failure when forcing legacy strings under Pandas 3
on the old scientific provider pin. MolSysMT #349 already owns the resolved
COMPND Copy-on-Write defect. Current/inferred string guards preserve the accepted
ordinary runtime and checked identity; original scientific bytes and checkpoint
remain unchanged. Newer-provider qualification is a separate receiving task.
