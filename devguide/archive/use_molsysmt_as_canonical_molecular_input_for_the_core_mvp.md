---
summary: Use MolSysMT as the canonical molecular input for the Core MVP
issue: uibcdf/dockingmt#9
status: resolved
opened: 2026-09-22
closed: 2026-09-22
verification: measured
area: [core, preparation, provenance]
guard: tests/test_redocking.py::test_direct_molsysmt_input_reaches_vina
normative:
blocked_by: []
supersedes: []
---

# Use MolSysMT as the canonical molecular input for the Core MVP

**Reported:** 2026-09-22, from comparison with TopoMT and review of the DockingMT input pipeline.
**Status:** Resolved for the input-normalization scope; chemical preparation remains separately tracked.

## What

Let users supply receptor and partner in molecular forms convertible by MolSysMT. A
DockingProblem should keep independently selected MolSys working objects, source inputs,
atom indices, and structure choices. Vina should prepare these systems internally.

## How

Normalize both molecular inputs at the problem boundary. Offer separate selections and
structure indices, including two selections from one complex. Keep prepared-state inputs
usable. Make the Vina adapter use the normalized systems through preparation, with PDBQT
confined to the adapter. Record input and preparation choices in problem/result provenance.

## Why

Currently DockingProblem stores arbitrary input values, while preparation converts
separately and Vina accepts prepared objects or PDBQT. Direct MolSysMT-compatible input
does not flow through the Core MVP. This prevents the native MolSysMT boundary described
in the suite integration contract and obscures source identity and selected atoms.

## What was refuted

Adding unused MolSys properties without moving the preparation path does not provide a
working molecular-input workflow. A declared MolSysMT form is not proof that this
environment can convert a particular input or that it contains valid docking chemistry.

## Scope and exclusions

The scope is input normalization, selection, inspectable correspondence and a direct
molecular-input workflow. Valid charge/atom-typing chemistry remains #5; explicit
chemical-state policy remains #4; verified pose atom maps remain #8. Generic PDBQT
support belongs to MolSysMT (uibcdf/molsysmt#214).

## Evidence and follow-up from the implementation review

- PDB 181L converts with a `lossy` report for `bond_order`; the direct-input
  benchmark cannot establish complete ligand chemistry. DockingMT now retains
  conversion evidence and identifies placeholder charges and heuristic atom types.
- A group-free RDKit benzene with embedded coordinates and Gasteiger charges
  converts to MolSys, but `group_name` is absent. DockingMT temporarily supplies
  a local PDBQT residue label after checking attribute availability. MolSysMT's
  raw `IndexError` for the absent attribute is tracked in uibcdf/molsysmt#233;
  remove the consumer guard once its general query contract is fixed.
- Multiple chemical states require a resolved association with the chosen
  structure. The problem records that association and selects against it.
- Prepared-object coordinates and source MolSys coordinates could diverge;
  `to_molecular_system()` now applies the current prepared coordinates.
- The viewer rejects a supplied partner whose atom count differs from the pose.
  DockingMT verifies Vina's returned PDBQT atom labels and rounded coordinates
  against the coordinate array and supplied PDBQT order. The local hydrogen
  reduction has an explicit retained-atom map and is used when constructing
  a pose or viewer complex from its source MolSys. General lossy exports and
  other atom changes remain tracked in uibcdf/dockingmt#8 and
  uibcdf/molsysmt#223. Remove the local mapping rule when the provider offers
  a validated general projection contract.
- A redocking factory derives the search box from the same selected partner and
  structure as the docking problem.
- File-backed inputs carry a content fingerprint and reconstruction rejects
  changed files. In-memory MolSys inputs still require the original object:
  H5MSM round-trips currently drop atomic partial charges without reporting
  their loss (uibcdf/molsysmt#234). A chemically faithful snapshot must be
  validated before replacing that explicit requirement.

## MolSysMT provider handoff

The DockingMT implementation evidence was added to the owning MolSysMT issues:

| Temporary local behavior or limit | Provider issue | Removal condition |
| --- | --- | --- |
| PDBQT input detection, writer, and atom-record parsing | uibcdf/molsysmt#214 | Validated file/string PDBQT conversion covers the supported layouts. |
| Small local chemistry evidence dictionary | uibcdf/molsysmt#217; uibcdf/molsysmt#218 | Selected ligand and receptor readiness reports distinguish assessed, missing, partial, and unassessed chemistry. |
| Zero-charge fallback and source-charge use without an assigned-model contract | uibcdf/molsysmt#221 | Named charge assignment and complete coverage are available for the chosen chemistry. |
| Element/aromaticity/residue AutoDock typing heuristics | uibcdf/molsysmt#222 | Named typing validates all exported atoms. |
| Rigid single-root ligand with zero torsions | uibcdf/molsysmt#224 | Rotatable bonds and rigid fragments are classified with source identity. |
| Local hydrogen projection and retained-atom mapping | uibcdf/molsysmt#223 | A post-export projection reports retained, omitted, and merged atoms and charge transfer. |
| Vina-output PDBQT atom-record interpretation | uibcdf/molsysmt#226 | A source-aware pose-ensemble reader returns mapped structures. |
| Guard against querying group attributes on group-free MolSys | uibcdf/molsysmt#233 | The public query returns a documented unavailable-attribute outcome or diagnostic. |
| In-memory snapshot deferred because H5MSM loses partial charges | uibcdf/molsysmt#234 | A validated H5MSM round-trip preserves the required chemistry or reports loss. |

Vina execution, scoring, ranking, search-domain choice, and acceptance policy for
provisional preparation remain DockingMT responsibilities.

## Acceptance criteria

- A direct MolSysMT-convertible input can be docked without manually calling preparation
  when ligand atom membership is preserved.
- Receptor and partner working objects are MolSys instances with independent selections
  and structure choices; source atom indices remain inspectable.
- Existing prepared-object workflows remain usable.
- Conversion, empty selection, ambiguous structure, and unmapped ligand atom loss errors
  occur before Vina.
- A direct-input regression and the local gates pass.

## Resolution

`DockingProblem` now normalizes MolSysMT-convertible receptor and partner inputs to
selected `molsysmt.MolSys` working objects while retaining the original inputs,
source atom indices, structure and chemical-state choices, conversion reports,
and file fingerprints. The Vina adapter prepares the selected systems and
records preparation provenance. Its output order is checked against PDBQT text;
the controlled nonpolar-hydrogen reduction carries source atom correspondence.
Prepared-state and legacy PDBQT workflows remain usable. A redocking factory
derives the box from the chosen ligand selection and structure.

The guard `tests/test_redocking.py::test_direct_molsysmt_input_reaches_vina`
exercises the direct PDB/MolSys-to-Vina path and its recorded atom identities.
Additional tests cover RDKit group-free ligands with explicit hydrogens, chemical
state association, conversion loss, ambiguous inputs, changed files, coordinate
consistency, and viewer atom-count failures. The full local suite passed 60 tests
with `pytest --receptor=llm`; Ruff lint and format, generated report indexes,
and `git diff --check` passed.

The rigid PDBQT preparation is provisional: missing charges may still use zero
placeholders, atom types are heuristic, and ligand torsions default to zero.
These scientific limitations remain in uibcdf/dockingmt#5, #6, and #8, with
provider work linked in the handoff table above. Passing this input-path guard
does not establish chemically validated docking scores.
