# Native receptor projection in production — 2026-10-24

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), related to
#5/#33 and delivered [MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223).
`prepare_receptor` now delegates typed-H reduction and charge transfer to public
`msm.build.merge_nonpolar_hydrogens`, as ligand preparation already does. Its local
H-parent/eligibility/charge-aggregation loop is removed. No molecular repair,
normalizer, alternate model or fallback is implemented downstream.

## Actual native output and attribution

After selection and the existing explicit charge/type stages, the provider receives
`typing_scheme='autodock4', selection='all', chemical_state='structure',
structure_indices=0, return_report=True`. It owns H-label eligibility, parent
validation, charge transfer, retained graph/coordinates, virtual-H counts and
derived assignment binding. The preparation consumes its actual reduced object
and maps, retaining the existing receptor serial/name/group presentation.

`PreparedReceptor.source_molsys` and source-backed reconstruction now carry the
actual aggregate charges and updated virtual-H inventory. Previously the stored
source was an extraction with unaggregated charges, despite aggregate values in
`prepared.charges`. This native-return compatibility change is intentional.
Original caller systems remain unchanged.

Metadata adds detached `molecular_projection`,
`projected_partial_charge_assignment` and `projected_atom_type_assignment` reports.
Original `partial_charge_assignment` / `atom_type_assignment`, charge accounting,
stage maps and pre-projection residue coverage keep their established scopes.
The native assignment is derived, with the original producer/calculation nested;
no new Gasteiger/type calculation is credited. The projection axis refers to the
selected post-stage source, not an inferred map through earlier H generation.

## Strict input boundary

The same public preconditions now apply to both roles: a complete prepared state,
finite charges, valid named AutoDock4 types, and known virtual explicit-H / zero
implicit-H counts on merged parents. Indexed H and named parameters alone do not
establish that stored inventory. Raw native SDF with unassessed parent counts
refuses before Vina, including provisional opt-in. No missing count is assumed
zero and no unrequested H/charge/type stage is selected.

Inspect inventory with public `msm.physchem.get_hydrogen_inventory` and prepare or
declare the molecular state through MolSysMT. Fixed-state H addition itself also
requires declared inventory; it is not a generic repair for unknown counts. The
existing [provider boundary feedback](https://github.com/uibcdf/molsysmt/issues/223#issuecomment-6388367762)
retains that distinction. Finite CH4O positive controls declare their known fixture
hypothesis through public setters; raw unresolved controls remain negative.
This does not admit arbitrary native SDF/PDB or certify biological protonation.

## Actual protein receiving and behavioral guards

The unchanged ordinary wheel at producer
`45e721bf7c56bdbf1c3ed6acfe539fed203d1155` supplies the baseline. The existing
181L fixture composes public terminal geometry, explicit HIE/ammonium/carboxylate
template hypotheses, fixed-state H addition and named charge/type assignment.
No new preparation model or registered search is introduced. Its 2,603-atom
post-stage source projects to **1,615 atoms**, merging **988 H**; public retained
axes match the old route and charges agree within **1e-12 elementary charge**.
Total charge remains 8 e within the declared fixture tolerance. The source is
unchanged. These are representation/software controls, not biological admission.

[Seven new guards](../../tests/test_receptor_projection_consumption.py) exercise
actual public delegation, default/nondefault units, independent methanol charge
expectations, aggregate native/reconstructed values, both map directions,
virtual-H counts, detached original/derived reports, source immutability and
provider failure identity. Unresolved inventory rejects before engine construction
under both provisional policies. The protein control observes the real public
call in the existing 181L workflow and retains its unassessed scientific status.
Ligand/receptor outputs have independent native objects and report snapshots.

All seven pre-change guards fail (18.84 s): no receptor projection call, missing
refusal, and unsafe admission to engine construction relative to the new inventory
contract. The migrated preparation/charge/native-export/ownership selection passes
**63 cases**, 60.24 s, with two retained structural warnings, zero skips. The broad
source selection passes **355 cases**, 225.38 s, with 131 retained warnings and
zero skips; the 63 focused cases are included. Ordinary installed candidate and unskipped exact-head results have their
separate terminal handoff in #49; overlapping selections are not summed.

The [compact versioned evidence](data/receptor_projection_2026-10-24/manifest.json)
retains original/final diagnostics, the ordinary baseline protein wire and probe,
provider identity, source hashes and scoped resources. The normally compiled and
installed provider stays at `3502232d802ee2927f6b6f5d19f0ae045777ecb5`; ArgDigest,
Viewer, dependency floors and workflow pins do not change in this slice.

## Remaining work and recovery

H projection/charge transfer is now delegated for both roles. Production PDBQT
writers and Vina pose parsing remain separate. Receive the supported presentation/
caller-remark/final-byte composition requested in
[MolSysMT #214](https://github.com/uibcdf/molsysmt/issues/214#issuecomment-6389119365),
or explicitly accept native presentation as a consumer compatibility change;
then retire the qualified writer and adopt its known-source reader. Do not bind
a native map to different legacy or decorated bytes. #49/#33/#5 remain partial.

Original scientific archives, ordinary wheels, scene and notebooks retain their
producers and bytes. No new registered 3PTB search, public package/Release or
whole-Core scientific acceptance is claimed. HTML/C6 remains deferred under #52;
public file/pair/platform admission remains #30/#47, with a future MolSysSuite
version notice required at publication closeout.

Task-owned receiver, candidate wheel/source/harness and terminal evidence are
retained under #50 for review by 2026-10-31. The inherited dependency base retains
review by 2026-10-27. Shared routine environment, prior receivers and sibling human
work are preserved. Review dates are not automatic deletion.
