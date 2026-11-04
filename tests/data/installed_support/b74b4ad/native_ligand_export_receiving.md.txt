# Prepared native ligand export receiving — 2026-10-24

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), related to
[#33](https://github.com/uibcdf/dockingmt/issues/33). This checkpoint receives the
actual reduced system from production ligand preparation through the public
native writer. It does **not** replace `PreparedLigand.to_pdbqt`, change a source
pin or implement a molecular builder, serializer or completed-map rebinder.

## Delivered route and explicit docking fixtures

The [eleven controls](../../tests/test_native_ligand_export_receiving.py) use
public MolSysMT conversion, fixed-state H addition, named charges/types,
production `prepare_ligand`, public copy/set and native PDBQT export with
`return_atom_map=True`. Literal rigid methanol, one-cut hexane and nested hexane
trees declare finite docking choices. No chemistry, atom correspondence, general
permutation or H inventory is discovered downstream.

The native copy gets explicit positive serial IDs through public setters.
Those setters preserve the actual derived assignments. The completed export
map binds that renamed copy, not the original preparation's earlier ID labels;
no earlier identity transformation or H-generation map is invented. Source and
prepared systems remain unchanged.

Under angstrom and pm/fs/coulomb policies, native output preserves the declared
prepared/written axes, ROOT/branches/TORSDOF, finite charges in elementary charge,
types, names and coordinates in angstrom. Actual fixed-column values are checked
independently, allowing only 0.000501 angstrom coordinate rounding. Both map
directions, full-precision/written charges, actual payload SHA-256, detached JSON,
derived attribution and source immutability are guarded. Vina 1.2.7 parses each
native payload. Unrepresentable atom names refuse without changing the prepared
source. These are representation/software controls, not biological geometry,
affinity or chemical-preparation admission.

## Remaining presentation and final-byte contract

Native small-molecule sources can correctly have no groups or chains. The native
writer preserves that absence. The existing DockingMT writer instead emits its
explicit LIG/A/1 presentation, occupancy 1.00/B-factor 0.00, and bounded original
charge/type attribution remarks. Native short-name alignment and branch whitespace
also differ; whitespace need not remain byte-identical. The meaningful fields,
attribution and exact identity of the newly emitted payload need an explicit
compatibility route before production retirement.

The current native writer exposes `typing_scheme`, `torsion_tree` and
`return_atom_map`; no supported caller-remark/output-presentation option was found.
Public calls with guessed `remarks` / `presentation` keywords refuse through the
argument contract. These guessed spellings are diagnostics, not proposed APIs.
Atom-level public hierarchy setters on the zero-group control fail with
`ValueError: cannot convert float NaN to integer`; setters do not establish an
absent hierarchy. A builder round trip is not accepted without a provider contract
preserving all required native domains and attribution.

Prepending the existing `REMARK DOCKINGMT_PARTIAL_CHARGES` and
`REMARK DOCKINGMT_ATOM_TYPES` lines to successful native output changes its hash
without changing atom records. The completed map still binds the original native
payload. The controls demonstrate this mismatch; they neither repair the map nor
claim the pose reader authenticates comments or necessarily rejects an added remark.
There is no new postprocessing route in production.

The [provider-owned request](https://github.com/uibcdf/molsysmt/issues/214#issuecomment-6389119365)
asks for an existing public composition or a reusable explicit output-presentation/
caller-remark contract. MolSysMT owns API choice and implementation, field/shape
validation, safe REMARK inclusion and computation of the completed map from final
actual bytes. Output-only labels must not fabricate scientific hierarchy in the
original system. This is a capability/documentation request, not a defect claim
against the writer's correct preservation of native absence. It reuses #214 and
does not reopen delivered #223.

## Executed evidence and scope

The first eleven-case run reports six failures / five passes in 9.93 seconds:
the new test incorrectly expected the assignment directly inside mechanics
`to_dict()`. Reading its public `partial_charge_assignment` property corrects that
assertion without a runtime change. The corrected module passes **11 tests** in
11.26 seconds, zero skips, with 11 retained structural warnings. Initial diagnostics
remain separate from passing qualification. The combined writer, known-source
reader and production-projection source selection passes **47 cases** in 39.65
seconds. Its source-free ordinary-installed selection passes the same **47 cases**
in 39.17 seconds, with 31 retained structural warnings and zero skips in each.
Exact-head CI has its terminal handoff in #49; overlapping selections are not summed.

The [compact evidence](data/native_ligand_export_2026-10-24/manifest.json) retains
the probes, original/native payloads, first/final reports and runtime identities.
Executed MolSysMT is the already normally compiled/installed
`128a0bbb94e6804f5663e58a45313c77de1cc30d`, Python 3.14.8 and Vina 1.2.7. Read-only
inspection of later `3502232d802ee2927f6b6f5d19f0ae045777ecb5` finds the native writer
and string adapter byte-identical; it does not qualify that later runtime. Later
reader/composition namespaces and public `permute_atoms` need separate receiving.

The ordinary unchanged DockingMT wheel remains producer
`16ff157e5b9d5b816e2315c650e0ff66c84329e9`, SHA-256
`41274abc433c34e7fcdb3565a747a0fc4a291f895b175ac2e16edfdc55f7041e`.
The intervening `2ffc2d5` adds only provider-delivery status documentation. This
checkpoint changes tests/guidance, not package code or the original wheel. The
source-free harness guards actual DockingMT imports in that receiver's prefix;
all 58 package/addon Python files (excluding generated version metadata) also
match the original wheel and current source byte-for-byte.
Its producer must not be relabelled as this checkpoint's later commit.

## Next steps and recovery

For this writer route, receive the provider's supported output composition or
explicitly accept native presentation as a consumer compatibility change. Then
retire the writer for the qualified input profile, preserving finite field
validation, native source/map identity and original/derived attribution. Adopt
the known-source pose reader for those actual bound bytes afterward. Receptor
projection and receiving the now-delivered general permutation remain independent
work under #49; all MVP development is not blocked on this request.

The previous [ligand projection terminal handoff](https://github.com/uibcdf/dockingmt/issues/49#issuecomment-6388864917)
remains 1,194 passing tests per Python 3.11–3.14 and 319 installed cases at its own
producer. No registered 3PTB search is added and no historical scientific archive,
scene, notebook or ordinary wheel is rewritten. HTML/C6 remains deferred under #52.
Public file/pair/platform admission remains #30/#47; no package or Release is
published. A future package/release notice in MolSysSuite remains required.

Task-owned harness, probes and full CI receipts are retained under #50 for review
by 2026-10-31. Scientific execution reuses the previous ordinary receiver read-only;
its inherited dependency base retains review by 2026-10-27. Shared routine
environment and sibling worktrees are preserved. Review dates are not automatic
deletion; the versioned resource receipt records recovery identities.
