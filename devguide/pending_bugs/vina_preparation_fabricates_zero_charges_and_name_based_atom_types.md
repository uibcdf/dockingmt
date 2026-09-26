---
summary: Vina preparation fabricates zero charges and name-based atom types
issue: uibcdf/dockingmt#5
status: partial
opened: 2026-09-22
closed:
severity: high
verification: asserted
area: [preparation, vina]
guard: tests/test_engines.py::test_vina_rejects_provisional_chemistry_from_automatic_and_prepared_inputs
normative:
blocked_by: []
supersedes: []
---

# Vina preparation fabricates zero charges and name-based atom types

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Partial; DockingMT Core MVP work.

## What

Current preparation writes zero partial charges, guesses AutoDock types from names, and drops hydrogens by name, including polar receptor hydrogens.

## How

Replace these assumptions with validated MolSysMT parameters and a documented PDBQT projection. Check that charge and typing schemes are declared and compatible with the selected Vina scoring mode; until available, reject incomplete inputs with actionable diagnostics.

## Why

The generated PDBQT can be syntactically accepted while misrepresenting the prepared receptor or ligand chemistry.

## What is measured and what is assumed

**Inspected:** Source inspected at dockingmt/preparation/ligand.py and receptor.py; scientifically validated impact and numerical score differences have not been measured.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

A passing docking run was rejected as proof of chemical correctness because Vina can process a chemically misparameterized PDBQT.

## Scope and exclusions

Vina input chemical parameterization; general charge models, AutoDock typing, and atom mapping are owned by MolSysMT.

## Acceptance criteria

- No supported Vina preparation path silently substitutes zero charges or name-derived chemistry when required input is absent.
- Focused ligand and conventional protein-receptor tests cover nonzero charges, polar hydrogen retention, chemically distinct atom types, and the selected scoring mode; unsupported inputs fail clearly.

## Dependencies and risks

Related tracked work: uibcdf/dockingmt#3
Cross-component implementation links: uibcdf/molsysmt#214, uibcdf/molsysmt#221, uibcdf/molsysmt#222, uibcdf/molsysmt#223.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## 2026-09-22 progress

The MolSysMT input implementation now derives element identity from the source,
retains polar hydrogen atoms, preserves source partial charges when present, and
records when zero placeholders or heuristic AutoDock types were used. The
remaining heuristic is based on element, group, and available aromaticity, not
atom names. Neither this heuristic nor the zero-charge fallback is a validated
parameterization.

Vina now rejects DockingMT-generated provisional preparations by default, for
both automatic MolSysMT input and previously created prepared objects. The
caller can explicitly opt into exploratory docking with
`VinaProtocol(allow_provisional_preparation=True)`; the policy and assessment
are serialized in result provenance. Existing external PDBQT inputs remain
accepted with an `unassessed` chemistry assessment. This addresses silent use
of DockingMT's known placeholders, but does not satisfy the full acceptance
criteria: validated receptor and ligand parameterization, scoring compatibility,
and scientific preparation tests are still needed. The provider requirements
remain tracked by molsysmt#221 and molsysmt#222.

## 2026-09-26 pinned 1IEP preparation audit

The [reproducible audit](../validation/1iep_preparation_audit.md) compares native
MolSysMT-based preparation against the official example's aligned PDBQT files. All
40 ligand and 2,702 receptor PDBQT atoms match by coordinate. Native charges are
zero for all retained atoms, whereas the published files have nonzero charges on
40 ligand and 2,669 receptor atoms. Four ligand and 24 receptor atom types differ.
The native ligand has zero branches and torsional degrees of freedom; the published
ligand has seven of each. This measures disagreement with a published input, not
the scientific accuracy of either parameterization or a docking score effect.

MolSysMT's public `build.get_missing_bonds` repaired the two absent receptor
hydrogen bonds required by the native writer. No local replacement was needed.
The general missing capabilities remain MolSysMT
[#221](https://github.com/uibcdf/molsysmt/issues/221) for charges,
[#222](https://github.com/uibcdf/molsysmt/issues/222) for named AutoDock typing, and
[#224](https://github.com/uibcdf/molsysmt/issues/224) for rotatable bonds and rigid
fragments. Until a scientifically supported path is available, the default Vina
rejection and this issue remain open.

The subsequent explicit-torsion implementation can reproduce seven 1IEP PDBQT
branches, but leaves the zero-charge and atom-type differences in this report
unchanged. Flexible-tree acceptance is therefore not a resolution of this issue.
