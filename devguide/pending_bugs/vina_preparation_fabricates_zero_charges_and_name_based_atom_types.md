---
summary: Vina preparation fabricates zero charges and name-based atom types
issue: uibcdf/dockingmt#5
status: open
opened: 2026-09-22
closed:
severity: high
verification: inspected
area: [preparation, vina]
guard:
normative:
blocked_by: []
supersedes: []
---

# Vina preparation fabricates zero charges and name-based atom types

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; DockingMT Core MVP work.

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
