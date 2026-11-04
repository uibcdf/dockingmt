# Source-free flexible reconstruction — 2026-10-24

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49); provider
[MolSysMT #369](https://github.com/uibcdf/molsysmt/issues/369) is delivered.
`PreparedLigand.to_molecular_system` now delegates flexible source-free
reconstruction to public PDBQT conversion and `msm.permute_atoms`. The local PDB
builder, duplicate-name rewriting, group truncation and unused temporary-file
conversion utility are removed. Native source-backed copy/set remains unchanged.

## Actual public composition

The existing prepared writer supplies its declared written atom traversal.
MolSysMT converts those PDBQT bytes with explicit `discard_torsion_tree=True`.
DockingMT inverts its known traversal as index accounting; public
`msm.permute_atoms(..., atom_indices=inverse)` transports the available native
domains back to the prepared axis. Its contract is `atom_indices[new] = old`.
No molecular matching, coordinate-only molecular reorder or general permutation
implementation is added here. Identity traversal on a flexible tree still uses
the public operation. Provider failures propagate without a PDB fallback.

Public `msm.set` then restores the original prepared coordinate quantity and
charges explicitly in elementary charge. The returned native system retains
representable AutoDock labels, element labels, names (including duplicates),
groups and IDs. IDs are the serialized PDBQT serial labels on the restored
prepared axis; they are not claimed to be unknown original experimental IDs.
Coordinates and charges retain prepared precision rather than PDBQT rounding.
Explicit replacement does not fabricate a charge/type calculation report.

This is still partial PDBQT chemistry, including its declared branch connectivity.
No absent bond, bond order, H coordinate, chemical state, interaction or original
preparation history is recovered. Preserving duplicate names in conversion does
not relax pose identity checks or discover correspondence between ambiguous keys.
The supplied preparation, its data and the intermediate parsed source are unchanged.

## Exact provider receiving

The new required source context is MolSysMT
`3502232d802ee2927f6b6f5d19f0ae045777ecb5`, the delivered public permutation revision.
It is normally built into
`molsysmt-0.23.0+201.g3502232d8-cp311-abi3-linux_x86_64.whl`, 61,335,729 bytes,
SHA-256 `f85b06b1297f2967510a806f7ac1c95a7914fbb96357ea45336e8076b6084841`.
Its normally installed native binary has SHA-256
`feb001379201b92690eadf04fd0be6b710cdfe50bad240feba26cf666e19b41b`.
These are new provider artifacts, not copied native bytes or relabelled old wheels.
The task-owned Python 3.14.8 receiver passes dependency closure; prior receivers,
native artifacts and the shared routine environment are preserved.

Both source workflows and the dependency inventory use that exact revision;
workflow digests follow the actual changed bytes. ArgDigest/Viewer pins and public
package metadata floors remain unchanged. This does not certify a published
dependency pair or advertise new platform admission. Public file/pair qualification
remains #30/#47.

That provider source moves pose reading to form-owned public entry points.
Current consumer guards now explicitly use `msm.form.file_pdbqt.read_poses` for
paths and `msm.form.string_pdbqt_text.read_poses` for text. No old-name alias,
namespace detection or runtime reader fallback is introduced. Production Vina
parsing remains unchanged; the prior dated `128a0bbb` reader/writer receipts keep
their original provider and historical spelling.

## Behavioral evidence

[Eight new guards](../../tests/test_flexible_reconstruction.py) check nonidentity
and nested/identity traversal under nm and pm/fs/coulomb policies, exact public
conversion/permutation calls, detached input preservation, duplicate/four-character
names, available mechanics and independent full-precision values. Conversion and
permutation failures retain exception identity. A native-source control bypasses
both tools, and a real synthetic Vina run reconstructs its returned pose on the
source-free prepared axis without losing charges or AutoDock labels.

Correctly scoped pre-change guards report **six failures / two passes**, 4.77 s:
the old route does not call public permutation and loses AutoDock mechanics.
The corrected final module passes **eight cases**, 4.76 s. The combined
reconstruction/reader module selection passes **32 cases**, 26.44 s, 22 retained
structural warnings; the broader preparation/engine/result/viewer/format/torsion/
historical-search selection passes **316 cases**, 180.22 s, 108 retained warnings.
These two file selections cover 348 distinct cases without skips; the eight
focused controls are included, not additional cases. Administrative contracts
pass 29 cases, 2.59 s.

Exploratory diagnostics are retained separately: the initial source-backed spy
intercepted its own snapshot helper; a later conversion spy intercepted native
inspection; cross-policy exact snapshots differed by conversion roundoff. Scoped
observations under the same unit policy fix those test-only assumptions. An initial
administrative run correctly exposed the removed file still listed in package
resources; the obsolete required path is now removed. Those failures are not
relabelled passing gates or provider defects.

The [versioned evidence](data/flexible_reconstruction_2026-10-24/manifest.json)
retains original/final reports, provider identities, source hashes and scoped
resources. Ordinary installed candidate and exact-head unskipped four-minor
terminal gates are separate post-commit evidence in #49. A passing focused/source
selection does not substitute for those gates or scientific admission.

## Remaining work and recovery

Receptor projection remains a consumer migration under #49/#5. Native writer
presentation and final-byte composition remains the separate
[MolSysMT #214 request](https://github.com/uibcdf/molsysmt/issues/214#issuecomment-6389119365);
then adopt the known-source reader against those actual bound bytes. No completed
map is attached to a different payload. #49/#33 remain partial/open.

Existing historical scientific archives and producers, ordinary wheels, scene and
notebooks are preserved. All 24 historical rows / 167 poses are received by the
broader software selection with historical preparation/scoring/search forbidden.
The synthetic Vina guard is not biological redocking or affinity evidence; no
registered 3PTB search is added. HTML/C6 remains deferred under #52. No public
package or Release is published; its future MolSysSuite notice remains required.

Task-owned source/build/wheels/receiver and full terminal receipts are retained
under #50 for review by 2026-10-31. The inherited dependency base retains review by
2026-10-27. Shared/sibling environments and human edits observed in the refreshed
suite inventory are preserved. Review dates do not trigger automatic deletion.
