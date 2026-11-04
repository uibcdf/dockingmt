# Preparation correspondence delegated to MolSysMT

## Consumer migration — 2026-10-24

[DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49) owns this bounded
adoption of public `msm.compose_atom_maps` at the already qualified MolSysMT
source `3502232d802ee2927f6b6f5d19f0ae045777ecb5`. Both preparation roles pass
their actual completed typed-H projection report. When fixed-state H addition
was requested, its actual completed report precedes that projection. Charge/type
assignment does not change the atom axis and retains its separate attribution.
No provider source, dependency floor, workflow pin or scientific method changes.

`finish_stage_maps` no longer builds an old-to-new dictionary from hydrogen
correspondence or fabricates an identity correspondence when no H stage ran.
MolSysMT validates and composes the declared axes. Its errors propagate without
a consumer fallback or another molecular matching/permutation algorithm.

## Stored contract and compatibility

`metadata.preparation_workflow.atom_map` is a detached, JSON-finite
`molsysmt.atom_map@1` record. Its source is the selected input **before requested
stages**; its output is the prepared native atom order. This is not the global
unselected input axis. Normalized stages retain original producer, parent,
merge and charge-transfer evidence. Original H-addition, projection and named
assignment reports remain separately available; composition credits no chemical
calculation anew and moves no coordinates or charges.

The provider uses `-1` for absent direct correspondence. Generated polar H has
no original source index. Merged original H is absent directly, with its
surviving parent recorded only by the separate representative map. A merged H
does not acquire the parent's coordinates or become directly retained.

Existing `prepared_to_input_atom_indices` and
`pdbqt_to_input_atom_indices` remain compatible, converting provider `-1` to
JSON `null`/Python `None`. The latter presents those indices in DockingMT's
declared legacy ROOT/BRANCH traversal. That ordering is consumer accounting,
**not a completed native export map or payload binding**. No export report is
fabricated from it. `source_n_atoms`, retained indices and charge/type projection
continue to describe the post-stage system before H reduction. With no requested
stage, the existing absence of `preparation_workflow` is unchanged.

For heavy-only methanol, two original atoms become six after H addition and
three after projection: native inverse `[0, 1, -1]`, legacy `[0, 1, None]`.
For six already indexed methanol atoms and charge/type stages, the inverse is
`[0, 1, 5]`; omitted carbon H indices 2–4 are `merged`, represented by output 0.
The flexible pentanol fixture retains a generated O-H while writing nested
branches in a different order. Its legacy input order remains
`[4, 5, None, 3, 2, 1, 0]`.

## Behavioral evidence and limits

[Eight consumer guards](../../tests/test_preparation_map_consumption.py) cover
real public calls/reports, generated and merged atoms, selected-input scope,
both preparation roles, default and pm/fs/coulomb policies, nested legacy order,
finite JSON, detached reports, source immutability, provider refusal identity
and malformed H correspondence. All eight fail before migration (5.90 s).
The initial integrated run passes 55 cases and fails two overstrong test
assertions that mutate the consumer's own composition arguments. Corrected
guards mutate the original public H result to test the promised report
detachment; those initial diagnostics are retained, not qualifying evidence.

The final focused selection passes **57 cases**, 45.00 s, with 17 retained
structural warnings and zero skips. Those cases are included in the broader
selection, not added to its total. The broader source selection passes **363
cases**, 222.44 s, with 135 retained warnings and zero skips. Administrative
reporting/distribution/coverage controls pass separately (29 cases, 2.81 s).
Ordinary installed and exact-head results are retained
in the [owning issue](https://github.com/uibcdf/dockingmt/issues/49) and
[compact evidence](data/preparation_atom_maps_2026-10-24/manifest.json).
Four ordinary baseline preparations at producer `489d0c2e2e3f0097ffa5579060d601de4d396195`
retain their original PDBQT bytes, charges, legacy maps and traversal. This is
representation/software qualification, not biological protonation, docking
quality, affinity or whole-Core acceptance. Original scientific archives and
their producers are preserved; no historical preparation/scoring/search is rerun.

## Remaining work and resources

Native writer presentation/caller remarks must be composed before final payload
binding under [MolSysMT #214](https://github.com/uibcdf/molsysmt/issues/214).
Receive that provider contract, retire the covered writer and consume the known-source
reader against its actual bytes. Earlier terminal/template lineage outside the
selected preparation input is not silently included in this map. #49/#33/#5
remain partial; HTML/C6 stays deferred under #52 and public admission remains
#30/#47. A future public version still requires its MolSysSuite notice.

The task-owned receiver, wheels, source/harness and terminal receipts are retained
under #50 for review by 2026-10-31; the inherited dependency base retains review
by 2026-10-27. No automatic deletion is scheduled. Older receivers, immutable
artifacts, the shared routine environment and sibling human work are preserved.
The routine environment compatibility exception remains under #49. The canonical
GH Run Receptor guide is synchronized for 1.3.0; runtime tool receiving and guide
delivery are distinct from any scientific or public package admission.
