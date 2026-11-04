# Prepared native receptor export receiving — 2026-10-24

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), related to
[#33](https://github.com/uibcdf/dockingmt/issues/33) and the existing
[MolSysMT #214 request](https://github.com/uibcdf/molsysmt/issues/214#issuecomment-6389119365).
This qualifies the actual reduced 181L receptor through the public native writer.
Production writing/parsing, output policy and dependency pins are unchanged.

## Real protein and completed maps

[Three guards](../../tests/test_native_receptor_export_receiving.py) reuse the
declared HIE/ammonium/carboxylate fixture, public terminal/template/H/charge/type
operations and production receptor projection. The prepared native system has
**1,615 atoms**, with aggregate charges and derived charge/type assignments.
The native writer preserves its positive, nonconsecutive IDs without a renaming
copy. Actual fixed-column names, residue labels/IDs, AutoDock types, coordinates
in angstrom and charges rounded to three decimal places are checked independently.

Public `msm.convert(..., to_form='string:pdbqt_text', typing_scheme='autodock4',
return_atom_map=True)` produces a rigid receptor and a completed export map bound
to its actual final payload. Both index directions, full-precision Q in elementary
charge, finite JSON, truthful derived REMARK methods/status and source immutability
are guarded under angstrom and pm/fs/coulomb policies. Real Vina parses the receptor;
there is no scoring/search or pose generation in these controls.

Public `msm.compose_atom_maps` joins the existing preparation map to that export:
**2,603 input atoms → 1,615 written atoms**, with 988 original H marked merged.
The map source is the already H-expanded selected input before requested typing,
not the original experimental heavy-only protein. No atom generation is claimed
inside this particular map. The receptor's earlier terminal/template/H reports
remain separate fixture evidence.

## Serial presentation boundary

An explicit public copy/set can number the 1,615 atoms consecutively without
changing the prepared source. Its export map correctly binds the renamed copy.
Composing that map directly with the original preparation map fails with
`StructuralInconsistencyError: Adjacent atom-map ids disagree`.
This is correct provider validation: identical counts/order do not establish
unchanged identity labels. No fake rename report, label stripping or completed-map
rebinding is introduced downstream.

MolSysMT #214 therefore needs to distinguish molecular source IDs from explicit
output serial presentation when retaining the existing DockingMT contract.
The original request also covers names, hierarchy/optional fields and caller
REMARK inclusion before the final payload hash. The current native writer works;
this does not classify its faithful native presentation as a defect.

Read-only inspection of fetched provider
`99cb831076c4725ddac0c6ab23fdcb5c3257fac0` finds the text adapter, writer and
export-axis adapter byte-identical to qualified `3502232d802ee2927f6b6f5d19f0ae045777ecb5`.
The newer revision is not adopted. #214 is still open/partial, with the requested
extension undelivered. Adopting native presentation instead is an explicit
consumer compatibility decision; this checkpoint leaves the current policy intact.

## Evidence and recovery

The focused module passes **3 cases**, 28.68 s, zero skips, with one retained
structural attribute-drop warning from the fixture's explicit upstream workflow.
The writer/reader/projection/map source selection passes **58 cases**, 96.44 s,
with 37 retained structural warnings and zero skips. Ordinary-installed and unskipped exact-head results have their
separate terminal handoff in #49. Overlapping selections are not summed.
The [compact evidence](data/native_receptor_export_2026-10-24/manifest.json)
retains original/native serial-policy probes, wire bytes, identities and diagnostics.

Qualification reuses the unchanged ordinary DockingMT wheel from producer
`fe8ad1351b8661b43957132236715115d495d795`, SHA-256
`962ce548821ee37a7b2cf986280de720ad39c989059da2dc3daa2c95c7ade05e`, with normally
installed MolSysMT `3502232d8`, Python 3.14.8 and Vina 1.2.7. This tests representation
and map composition, not biological protonation, geometry quality, affinity or
whole-Core acceptance. The original 181L legacy wire retains SHA-256
`c372bbb4a83414cc82ddbc2263424dfe18b20df8ae6d5362f978c0d445a82ccc`.
Original scientific archives/producers are preserved. No registered 3PTB search,
public release or C6 acceptance occurs; #49/#33/#5 remain partial.

Next receive provider-owned presentation/remark composition under #214 or accept
native presentation as a product compatibility change, then retire covered
production writing and adopt known-source pose reading for its actual bytes.
HTML/C6 remains deferred under #52; public delivery stays #30/#47.
Task probes/harness/receipts are retained under #50 for review by 2026-10-31;
the reused receiver retains its existing ownership and inherited dependency-base
review by 2026-10-27. Review dates are not automatic deletion.
