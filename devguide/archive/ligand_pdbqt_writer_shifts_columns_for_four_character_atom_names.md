---
summary: Ligand PDBQT writer shifts columns for four-character atom names
issue: uibcdf/dockingmt#18
status: resolved
opened: 2026-09-26
closed: 2026-09-26
severity: medium
verification: measured
area: [preparation, vina]
guard: tests/test_preparation.py::test_ligand_pdbqt_preserves_fixed_columns_for_four_character_atom_name
normative:
blocked_by: []
supersedes: []
---

# Ligand PDBQT writer shifts columns for four-character atom names

## What

The temporary ligand writer emitted a variable-width atom-name field. The
four-character name `Cl23` shifted the residue and coordinate columns in the
1S63 ligand PDBQT record.

## How

`PreparedLigand.to_pdbqt()` formatted names with a minimum width of three,
followed by a space. A four-character name overflowed the field. Use a fixed
four-column atom-name field and reject names longer than four characters.

## Why

The pinned Vina 1S63 source produces one chlorine atom named `Cl23`. Its
generated coordinate field included `4 131.71` where one floating-point value
was expected. The 1S63 matrix exposed this defect; Vina parser acceptance is
the downstream integration check.

## What was refuted

The initial 1S63 failure was not a coordinate-alignment tolerance issue. The
atom-name overflow directly changed fixed PDBQT column positions.

## Scope and exclusions

This fixes DockingMT's temporary ligand writer. General PDBQT form ownership
belongs to MolSysMT [#214](https://github.com/uibcdf/molsysmt/issues/214).
The chemical choice of 1S63 torsions is tracked in DockingMT #17.

## Acceptance criteria

- One- through four-character atom names preserve atom, residue, and coordinate
  columns; longer names fail explicitly.
- The 1S63 native flexible ligand passes Vina's PDBQT parser.
- The named guard and full local gates pass.

## Resolution, 2026-09-26

The temporary writer now reserves the exact four-character atom-name field and
rejects longer names. The named guard checks the `Cl23` atom, residue, and all
three coordinate slices and verifies explicit failure for a five-character
name. The pinned 1S63 matrix reconstructs the full ligand and Vina 1.2.7
accepts the generated PDBQT. The full local pytest-receptor gate passed with
103 tests, and Ruff and devguide-index checks passed.
