---
summary: Select molecular states and record preparation decisions for docking
issue: uibcdf/dockingmt#4
status: partial
opened: 2026-09-22
closed:
verification: measured
area: [preparation, provenance]
guard: tests/test_redocking.py::test_direct_molsysmt_input_reaches_vina
normative:
blocked_by: []
supersedes: []
---

# Select molecular states and record preparation decisions for docking

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial; DockingMT Core MVP work.

## What

Make the chosen ligand and receptor states and preparation decisions explicit in a docking run.

## How

Record ligand chemical state and conformer, receptor state, pH and residue variants, retained waters/cofactors, the named charge and atom-typing schemes, hydrogen projection, active torsions, and any transformation parameters; associate each result with those inputs.

## Why

The Core MVP requires prepared states and backend representations to be traceable to source systems.

## What is measured and what is assumed

**Inspected:** Inspected devguide/MVP.md and current preparation/result model. No end-to-end provenance audit was run.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Implicit selection from a current coordinate frame was rejected because the same source can have several valid experimental states.

## Scope and exclusions

Selection and provenance for the initial protein–small-molecule workflow; chemical-state enumeration and receptor repair remain MolSysMT capabilities.

## Acceptance criteria

- A run can identify the selected source states, structure indices, named charge and atom-typing methods, hydrogen and torsion policies, preparation choices, and backend artifacts.
- Ambiguous state selection fails or requires an explicit documented policy; redocking tests verify traceability.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#217, uibcdf/molsysmt#218, uibcdf/molsysmt#220, uibcdf/molsysmt#221, uibcdf/molsysmt#222, uibcdf/molsysmt#223, uibcdf/molsysmt#229, uibcdf/molsysmt#230.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## 2026-09-22 progress

DockingProblem now records source form, atom selection and indices, chosen
structure and chemical-state identifiers, conversion report, and file content
fingerprint. Vina preparation records source charge availability, temporary
typing, retained atoms, omitted hydrogens, the polar-hydrogen policy, and the
rigid torsion policy. The backend now records SHA-256 digests of the exact
receptor and partner PDBQT bytes submitted to Vina. The chosen protocol and
preparation assessments remain in result provenance.

The proposal stays open. Named validated charge and atom-typing methods,
protonation and pH choices, residue variants, and explicit water/cofactor
decisions require provider capabilities or a documented preparation workflow.
An artifact digest proves which bytes were used when retained elsewhere; it
does not by itself preserve the generated PDBQT for later reconstruction.

## 2026-09-26 progress

`VinaProtocol(capture_backend_inputs=True)` now retains the exact receptor and
ligand PDBQT bytes in result provenance, alongside their SHA-256 digests. Vina
reads staged snapshots of file inputs to make the captured bytes the submitted
ones. The file-backed 181L manifest enables capture; replay checks each saved
payload against its digest before running and compares the new run's payloads
with the saved ones. Capture is opt-in because receptor PDBQT can make result
manifests large. These records strengthen backend-input auditability but do not
establish chemical validity or replace the remaining state and preparation
decisions in this proposal.

The 181L case was recorded and replayed in separate commands. The manifest was
197,158 bytes, retaining 103,120 receptor PDBQT bytes and 503 ligand PDBQT
bytes. Both recorded and replayed payloads matched, and the replay comparison
remained within tolerance. A deliberately changed ligand payload failed digest
validation before a docking rerun in the regression test.

## 2026-09-26 redocking state-selection correction

`DockingProblem.for_redocking()` no longer silently chooses structure 0 for a
multi-structure MolSysMT source. It requires `structure_index` in that case and
uses the chosen structure for receptor and ligand extraction and the search box.
A two-structure regression test gives the second structure a different position
and chemical-state ID, then checks the selected coordinates, box containment,
recorded state, and reconstruction. Single-structure input still selects index
0 by default. This resolves the ambiguity within DockingMT; the broader issue
remains partial until validated preparation methods and their decisions can be
recorded through the provider workflow.

## 2026-10-03 explicit chemical-template consumer qualification

The [consumer record](../validation/chemical_template_consumption.md), executed
notebook and raw indexed reports qualify public MolSysMT assessment/application
from exact source `c19a47ada0`. The existing `prepare_ligand` boundary consumes the
returned native system. Original 181L BNZ accepts a declared heavy-only template;
permuted 5X72 P59/P69 absent-field controls preserve both poses, IDs and chosen
state while receiving the expected R/S assignments. Original native SDF versus
adapter-template aromatic encodings remain unassessed; no normalization is added.

Fourteen focused consumer cases protect conflicts, absent edges, exhaustive H
mapping, matching explicit fields, unselected state preservation and non-default
units. A real Vina test retains default provisional rejection and saved-result
assessment after explicit exploratory opt-in. Reports remain separate workflow
records because MolSysMT #298 has no native report attachment. Charge/type
qualification and general preparation remain open; this issue stays partial.

The full source-qualified gate passes 538 tests without skips in 108.31 s on
Python 3.14.7, using an isolated MolSysMT archive and the existing CI viewer pin.
The executed notebook asserts the requested Conda interpreter. The initial live
viewer profile exposed an in-progress explicit frame-pairing requirement under
molsysviewer#151; its checkout is preserved and the separate consumer migration
is retained in the validation record. Ruff, indexes and diff checks pass.

## 2026-10-03 public preparation assessment

`dockingmt.assess_preparation` now exposes the existing provisional preparation
classification before engine execution. Vina consumes the public operation and
retains its bounded, detached `assessment_report` with stable reason codes and
declared charge/type sources, preserving the existing provenance fields and
default rejection policy. External PDBQT representations stay unassessed;
explicit zero charges alone do not imply placeholders. No molecular operations
or provider chemistry checks are duplicated.

The [contract](../validation/preparation_assessment.md) and executed notebook
document the public boundary. Thirty focused cases pass; the full source-qualified
gate passes 564 tests without skips in 100.53 s on Python 3.14.7 using unchanged
CI provider pins. Fresh-process absence of engine/viewer, malformed declarations,
detachment, real Vina persistence and template-transfer safeguards are covered.
This issue remains partial: public inspection does not deliver validated chemical
parameterization or scoring compatibility.

## 2026-10-04 explicit fixed-state H/charge stages

The [bounded consumer contract](../validation/ligand_preparation_stages.md),
tracked by dockingmt#41, adds opt-in provider option mappings to existing public
`prepare_ligand`. MolSysMT H addition precedes named charges, defaults to strict
attribute preservation and retains original reports/credit and composed input,
expanded, prepared and written correspondence. Generated H has no original input
index; no local chemistry or geometry algorithm is introduced.

The supported methanol control preserves original identity/coordinates, adds four
H, retains the polar H and conserves 0 e in the existing charge projection.
Idempotence, explicit attribute loss, non-default units, unchanged provider errors,
result persistence and the default provisional typing gate are guarded. The full
source-qualified suite passes 887 tests without skips on Python 3.14.7/Vina 1.2.7.
Original 181L BNZ remains a negative control pending MolSysMT #314 bond aromaticity;
the notebook retains the rejection and unchanged pose. #41 and this owning issue
remain partial. Published source pins are unchanged and sibling work is preserved.

## 2026-10-06 explicit real receptor hypothesis

The [181L workflow](../validation/181l_receptor_workflow.md) composes existing
public provider peptide templates, native OXT repair, fixed-state H, Gasteiger
charges and named AutoDock types. It explicitly declares HIE at original HIS31,
ammonium/carboxylate termini, no pH prediction, no retained waters/cofactors and
rigid BNZ. Source IDs and observed coordinates survive; generated OXT/H,
structural attribute loss, explicit generated-H naming and the charge/type
projection are retained with complete maps and original provider reports.

Six real Vina searches (three seeds, exhaustiveness 1/8) use default admission
and save exact backend inputs with the workflow decisions. Independent saved
result evaluation uses original BNZ source keys and a declared 2.5 angstrom
cutoff without alignment/symmetry correction. Five first poses and all six
returned pose sets satisfy that criterion; one top-1 failure is preserved.
This is one bounded hypothesis, not environmental protonation, water-policy,
affinity or general scientific validation. The issue remains partial, alongside
provider #223/#323 and installed/hosted qualification. Writer width defect #44
was discovered in this consumer workflow and has its own durable guard.

## Independent prospective state hypothesis — 2026-10-10

The [3PTB protocol](../validation/3ptb_prospective_protocol.md) declares
benzamidinium +1 separately from neutral CCD BEN, HID57/HIE40/HIE91,
charged termini, six deposited disulfides and excluded waters/calcium before
preparation or search. Public MolSysMT conversion/template assessment must admit
the original source and preserve every observed heavy coordinate. Fixed-state
H and named models require their original reports and full maps; no pH inference,
chemical overwrite, environmental refinement or implicit repair is authorized.
The sources and scientific prescription are recorded, while molecular admission
and all 24 searches remain unexecuted. #4 remains partial.


## 2026-10-10 executed 3PTB admission

3PTB admission executes the registered HID57/HIE40/HIE91, six CYX links, charged termini and benzamidinium +1 hypothesis through public MolSysMT tools. Fixed-state H requires explicitly reported occupancy/B-factor loss with original arrays retained. Source identities remain unchanged. No pH prediction, alternative state selection or environmental refinement is qualified.

The [executed admission](../validation/3ptb_admission.md), [notebook](../validation/3ptb_admission_2026-10-10.ipynb) and separate receipt retain measured scope. Owning issues remain partial/open.

## 2026-10-10 3PTB searches with the frozen state hypothesis

All [24 registered searches](../validation/3ptb_search.md) reuse admitted dry
HID57/HIE40/HIE91/CYX/charged-terminus receptor and benzamidinium +1 input bytes.
Separate reception measures all 167 saved poses under the original cutoff,
retaining original reporting failures. Native-box rank-1 recovery in both arms
is bounded evidence for this declared hypothesis, not experimental protonation,
model/valence certification, affinity or a state-selection rule. Calcium/waters
remain excluded; environmental H and other hypotheses are unassessed.
No preparation default changes and #4 remains partial/open.
