---
summary: Qualify retained MolSysMT preparation history and successful fixed-state benzene hydrogen addition.
issue: uibcdf/dockingmt#42
status: partial
opened: 2026-10-05
closed:
verification: measured
area: [preparation, validation, molsysmt]
guard: tests/test_ligand_preparation_stages.py::test_original_181l_declared_template_supports_fixed_state_h_and_named_charges
normative:
blocked_by: []
supersedes: []
---

# Update chemical preparation qualification

## What

Adopt the provider handoff from resolved MolSysMT #298/#318: retain chemical
preparation history in audit snapshots and positively qualify the original 181L
BNZ fixed-state hydrogen and named-charge route. This is DockingMT #42; broader
preparation stays in #5/#33 and the explicit-stage workflow in #41.

## How

Capture public topology and structure domains with explicit nm/ps units, plus
ChemicalStatesDict including original history. Do not authorize history loss to
MolSysDict 0.1. Replace the stale aromatic rejection with independent assertions
for added H, source identity/coordinates, charge transfers and provisional typing.
Qualify a named committed provider and align consumer source pins after checks.

## Why

The original source-qualified record used MolSysMT 7894435e. Provider #318 now
admits declared aromatic-only bonds without inventing integer Kekule orders;
provider #298 now retains template evidence in ChemicalStates and H5MSM 0.5.
The old audit snapshot and negative BNZ expectation no longer match those tools.

## Initial reproduction — 2026-10-06

Unchanged DockingMT d419fee, Python 3.14.7, MolSysMT 5bd893c85: the three affected
modules produce 58 passes and eight failures. Five fail on MolSysDict's explicit
history-loss rejection; one expects the resolved H failure. Two further controls
require absent Vina. This reproduces the handoff and separates engine absence
from molecular correctness. No sibling worktree is changed.

## What was refuted

Discarding history, bypassing strict loss checks, inventing aromatic orders,
adding local chemistry or treating absent Vina as successful qualification.
The first ArgDigest 0.13 source selection also fails the new PyUnitWizard 0.28.1
dependency contract (`argdigest>=0.14.0`), even when execution controls pass.
The candidate therefore selects published-tag ArgDigest 0.15.0 source.

## Scope and exclusions

Audit/test/helper and controlled-source integration work. Keep historical
receipts intact; retain new measurements separately. Generated H has local modeled
geometry; types remain heuristic, preparation provisional. No typing/torsion
policy migration, provider source edits, public artifact or biological claim.

## Acceptance criteria

- Original BNZ adds six H with unchanged input IDs/coordinates, explicit loss
  declarations, conserved named charges and composed input/prepared/written maps.
- Audit snapshots retain original preparation history, structures and chemical
  state associations under non-default units and public H5MSM recovery.
- Retained finite evidence and executed notebook match the qualified provider.
- Relevant contracts, full consumer regression and local quality/reporting gates
  pass; unexecuted interpreter/installed/hosted evidence remains explicit.

## 2026-10-06 measured adoption candidate

Public native-domain snapshots use schema `dockingmt.chemical_template_snapshot@2`
and retain original preparation history with declared nm/ps structure units.
The new regression checks template history through H5MSM 0.5 recovery under pm/fs,
including indexed original reports, input immutability and independently editable
audit copies. Topology/chemistry/history/associations remain exact. Two empty
component text columns acquire nullable string dtypes; the finite receipt names
that encoding change. Geometry uses an absolute `1e-12 nm` conversion tolerance.

Original BNZ now has positive fixed-state H/named-charge evidence: six input C,
six added H, 12 expanded atoms, six retained A types, six nonpolar-H charge
transfers, composed maps 0–5 and charge conservation within `1e-10 e`. Original
carbon IDs/coordinates remain unchanged. Intersection explicitly records dropped
B-factor/occupancy; Vina 1.2.7 accepts the PDBQT. Generated geometry and typing
remain provisional, and the default Vina gate remains in force.

The CI/full-matrix candidate selects MolSysMT
`5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, released-tag ArgDigest 0.15.0
`1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e`, and the existing viewer lanes.
Support-library floors in the test environment match provider requirements.
All tracked imported package files match the selected commits; the source profile
records native-extension bytes separately from producer/build provenance.

New dated [template](../validation/chemical_template_consumption_2026-10-06.ipynb)
and [stage](../validation/ligand_preparation_stages_2026-10-06.ipynb) notebooks and
finite receipts preserve previous historical records. No sibling source, molecular
algorithm or automatic chemical policy changes. This is a local, unpublished
consumer candidate; publication and exact-head hosted evidence remain pending.

## Final local gate — 2026-10-06

The final ArgDigest 0.15.0 / MolSysMT 5bd893c85 / existing Python 3.14 viewer
profile passes **888 tests without skips in 242.56 s**, with 98 warnings in ten
reported groups. Warnings retain legacy H5MSM, structural-loss, viewer, provider
inference/encoding and unrelated TopoMT syntax evidence. Both new notebooks
execute all eight code cells under Python 3.14.7. Ruff lint/format (115 files),
report/index, changed-document links, finite receipt/source hashes, installed
editable-checkout identity and diff checks pass. The
[source profile](../validation/data/chemical_templates/source_profile_2026-10-06.json)
retains the selected sources, gate outcome and unexecuted/failed scopes separately.

## Outstanding evidence and recovery

Python 3.11–3.13, macOS, clean installed artifacts and new hosted CI are not
executed here; CI/full-matrix workflows retain those recovery lanes. The native
extension is retained by digest, without a fresh producer build. Local `pip check`
fails on unrelated AmberTools metadata: missing pdb2pqr, NumPy <2 requirements,
and proprep's Biopython <1.86 requirement. No host-wide dependency closure is claimed.

The component-guide check passes. Canonical-byte comparison finds pre-existing
SMonitor/ArgDigest guide drift; both local copies are unchanged. Their new scoped
API/guide receiving remains coordinated in
[MolSysSuite #106](https://github.com/uibcdf/molsyssuite/issues/106), with the local
support-layer adoption in [DockingMT #19](https://github.com/uibcdf/dockingmt/issues/19).
Archive/close this record and #41 only after the owning publication/checkpoint
decision; general preparation, named typing and provider export remain separate.


## Public state synchronization — 2026-10-06

- [Owning #42 update](https://github.com/uibcdf/dockingmt/issues/42#issuecomment-6026692859).
- [Positive #41 consumer follow-up](https://github.com/uibcdf/dockingmt/issues/41#issuecomment-6026702174).
- [Provider #298 evidence](https://github.com/uibcdf/molsysmt/issues/298#issuecomment-6026704320).
- [Central #106 guide/source receiving notice](https://github.com/uibcdf/molsyssuite/issues/106#issuecomment-6026703587).

The consumer issues remain open; the candidate and new receipts are local, with
no commit/push or new hosted result claimed.
