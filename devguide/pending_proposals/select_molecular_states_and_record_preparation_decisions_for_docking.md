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
