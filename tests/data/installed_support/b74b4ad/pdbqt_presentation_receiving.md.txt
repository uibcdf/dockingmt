# PDBQT output-presentation receiving — 2026-10-28

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), with
[#33](https://github.com/uibcdf/dockingmt/issues/33) and provider
[MolSysMT #214](https://github.com/uibcdf/molsysmt/issues/214).
This resumes the [pause checkpoint](pause_handoff_2026-10-26.md).

## Delivered contract and consumer scope

MolSysMT delivered the requested public `output_presentation` and `remarks`
options at `e395e52646dab2ecb480d3d67aa7254be99b8524`. The native file/text
converters accept explicit serials, atom names, group/chain display fields,
occupancy and quantity-valued B factors without changing molecular identity or
creating hierarchy. The provider includes caller REMARKs before completing the
export map/hash. Its known-source reader separates original labels from written
labels and restores the original source axis. The provider's
[receipt](https://github.com/uibcdf/molsysmt/blob/e395e52646dab2ecb480d3d67aa7254be99b8524/devtools/data/pdbqt_presentation_20261026.json)
records its own bounded tests, not DockingMT installation or scientific admission.

The [consumer module](../../tests/test_pdbqt_presentation_receiving.py) uses real
production preparations and the public converter. Rigid methanol, one-cut hexane
and nested hexane retain the existing explicit ROOT/cut decisions. Native sources
stay unchanged, including their absent group/chain hierarchy; display fields are
declared on the prepared atom axis. Independent fixed-column comparison verifies
the meaningful fields of the current DockingMT output, allowing name alignment
and branch whitespace differences. Original DockingMT charge/type REMARKs coexist
with truthful native derived attribution. No molecular builder, serializer,
atom-record patcher, ID renaming or completed-map rebinding is added downstream.

Controls cover default and pm/fs/coulomb policies, exact file/text bytes, final
SHA-256, original and written IDs, actual traversal, native projection/export
composition, finite JSON and real Vina parsing. Renamed output labels and two
explicit MODEL labels are read through the public known-source reader, preserving
source labels and rounded coordinates. A small seeded hexane/minimal-receptor
Vina software control checks actual returned poses and composed maps against the
existing engine-array coherence guard. It is not a new historical scientific run.

The real 181L preparation additionally preserves all 1,615 written atom fields
while consecutive output serials differ from its original nonconsecutive IDs.
Its preparation/export chain spans 2,603 already H-expanded atoms to 1,615 output
atoms, with 988 H merged. The source is the same pre-typing input axis used by the
[previous receptor receiving](native_receptor_export_receiving.md), not the original
experimental heavy-only protein. The previous renumbered-copy refusal stays valid;
output presentation now supplies the separate supported route.

## Executed qualification

The old qualified provider `3502232d8` fails the new rigid/angstrom control with
`UnknownArgumentError` for `output_presentation`: one expected failure, 14 cases
deselected, 2.63 s. The new normally built/installed provider passes all **15 new
controls**, zero skips, **34.52 s**, with 14 retained structural warnings.

The source-free ordinary-installed writer/reader/projection/map selection passes
**66 tests**, zero skips, **84.28 s**, with 49 retained structural warnings.
This includes the 15 new cases; overlapping counts must not be summed. The first
harness attempt copied an unrelated untracked kernel IPC socket and failed before
test collection. The corrected harness copies only declared tracked test/evidence
inputs plus the new test module; no socket or caller resource is removed.

Full source, administrative and exact-head hosted receipts are recorded separately
under #49. No full-matrix result is inferred from the focused selection.

The ordinary MolSysMT wheel is
`molsysmt-0.23.0+232.ge395e5264-cp311-abi3-linux_x86_64.whl`, **61,375,025 bytes**,
SHA-256 `d08672224095fc23f078728040f061e678269aa1a41b3463409decbe01ad7b8c`.
Seven converter/writer/reader files match the exact source, wheel and installed
prefix. Its actual native library has SHA-256
`f7db4906514c407775dd2a4e1d4911729b9ba233d49044e17330cf3a01fc240a`.
The receiver is Python 3.14.8/Vina 1.2.7 with unchanged compatible ArgDigest
`3d1ec53c374098016452abab74706e9d80df5462` and Viewer
`a61b75bc994e3ad674c3e7eafe53bb6b2a989c5f`. Inherited and new receiver dependency
closures pass; the shared environment is preserved and not used to qualify this
new provider. Its separate reconciliation remains outside this receiving change.

DockingMT's ordinary artifact keeps original producer
`fe8ad1351b8661b43957132236715115d495d795`, filename
`dockingmt-0.0.0+196.gfe8ad13-py3-none-any.whl`, **122,993 bytes**, SHA-256
`962ce548821ee37a7b2cf986280de720ad39c989059da2dc3daa2c95c7ade05e`.
All 57 runtime/addon Python files excluding generated version metadata match that
producer, wheel, installed prefix and current source. Installed tests have no
consumer source package in their harness and verify actual imported origins.
No new consumer artifact is built or relabelled.

## Adoption boundary and next implementation

Both source CI workflows and their reviewed dependency-route inventory select
the exact received provider revision. ArgDigest/Viewer pins, required interpreters,
workflow commands, schedules, recipe and public requirements remain unchanged.
Source pins support controlled integration; they are not public package admission.

The production `PreparedLigand.to_pdbqt`, `PreparedReceptor.to_pdbqt` and pose parser
are still unchanged. Next replace the covered writers with this public composition,
preserving explicit ROOT choices, presentation, prepared coordinate/Q precision
and original/derived attribution. Receive the actual completed export map in the
engine path before adopting native pose reading. Directly constructed source-free
prepared objects need an explicit supported producer contract; the current
writer-to-reader reconstruction must not become a circular replacement writer.
Public failures must propagate, and no consumer molecular fallback is authorized.

The compact evidence manifest belongs in
`data/pdbqt_presentation_2026-10-28/manifest.json`. Full build logs, source-free
harness, original/final diagnostics, exact wheel and receipts are retained under
task owner #49 and resource owner #50, review **2026-11-04**. Review dates are not
automatic deletion. Historical archives, producer wheels, scene and notebook
identities are preserved. HTML/C6 stays deferred under #52. #49/#33/#5 remain
partial; public delivery stays #30/#47. No public package or Release is published.
