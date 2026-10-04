---
summary: Consume explicit fixed-state ligand hydrogen and charge stages with provenance.
issue: uibcdf/dockingmt#41
status: partial
opened: 2026-10-04
closed:
verification: measured
area: [preparation, validation]
guard: tests/test_ligand_preparation_stages.py
normative:
blocked_by: [uibcdf/molsysmt#314]
supersedes: []
---

# Consume fixed-state ligand hydrogens

## What

Extend existing public `prepare_ligand` with explicit opt-in `hydrogen_options`
and `charge_options` mappings delegated to public MolSysMT builders. Preserve
producer reports and compose input/H-expanded/prepared/written atom indices.

## How

Require fixed-state mode, explicit engine and pH=None for requested H addition;
require a named charge method. Default expanded-attribute policy is strict.
Perform H addition before charge assignment. Molecular manipulation remains in
MolSysMT; DockingMT selects and records the workflow. Absent options preserve
existing preparation. No implicit state/model, fallback or chemistry repair.

## Why

MolSysMT #300 provides supported fixed-state H addition; #221 provides named
charges. The accepted consumer workflow needs traceability across these stages
rather than losing the added-H provenance before docking.

## What was refuted

The compatible heavy-only 181L BNZ template is insufficient for H addition on
qualified provider 7894435e748bc55254b6c3d2b63ae82c101e5774: missing bond aromaticity
is rejected before attribute-policy handling. This is reported in MolSysMT #314,
not repaired by downstream flags or a local RDKit bridge.

## Scope and exclusions

One explicitly prepared state/frame. Local H placement is not environmental or
energy refinement. AutoDock typing remains heuristic under #5/MolSysMT #222.
Existing consumer H/export projection remains pending MolSysMT #223. Preserve
provider dirty/unpublished work; use the same published archive as #40.

## Acceptance criteria

Positive polar control and negative original BNZ control; retained original pose,
idempotence, charge conservation, full source correspondence, strict attribute
loss, provider failure identity, default provisional gate, saved-result reports,
nondefault units, executed notebook and appropriate local checks. Positive BNZ
qualification remains provider-dependent and explicitly partial.

## 2026-10-04 measured consumer slice

The public boundary now delegates requested stages and retains their reports/maps.
Twenty-six new guards cover the supported methanol control (2 input atoms, 4 added
H, 3 prepared atoms), unchanged source identity/coordinates, explicit-H inventory
idempotence, manual public-pipeline equivalence, non-default units, strict versus
explicit intersection attribute handling, unchanged provider errors, absence of
implicit stages and real Vina exploratory/result persistence. Numeric charge
audit is consistent at 0 e. Default heuristic-typing rejection remains in force.

The [contract](../validation/ligand_preparation_stages.md), executed three-code-cell
notebook and finite raw receipt retain original reports, qualified provider file
hashes and the negative original 181L BNZ control. Both chemistry and added-H
geometry remain provider-owned; no dirty/unpublished sibling code is consumed.
The complete source-qualified local suite passes **887 tests without skips in
202.89 s** on Python 3.14.7/Vina 1.2.7, with 107 warnings in seven reported groups.

This issue stays partial. Positive original BNZ acceptance requires explicit
covalent bond aromaticity from MolSysMT; the reproducible rejection and unchanged
experimental pose are handed off in [molsysmt#314](https://github.com/uibcdf/molsysmt/issues/314#issuecomment-5978374154).
Named AutoDock typing and provider export projection have separate owners and
acceptance criteria (#222/#223); this slice does not qualify complete preparation.

Local Ruff lint/format (115 Python files), installed editable-checkout identity,
`pip check`, report/index and diff checks pass. All three notebook code cells
execute under the requested Conda interpreter; the finite 119,587-byte receipt
matches the current implementation hashes. Exact-head hosted evidence is obtained
after publication; local results alone do not establish the supported matrix.
