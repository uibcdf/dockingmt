# Production known-source pose reading — 2026-10-28

Owners: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49) and
[#33](https://github.com/uibcdf/dockingmt/issues/33). This consumes the qualified
MolSysMT `e395e52646dab2ecb480d3d67aa7254be99b8524` reader delivered under
[MolSysMT #226](https://github.com/uibcdf/molsysmt/issues/226), after
[prepared writer adoption](prepared_writer_consumption.md). Dependencies and
provider pins do not change.

## One actual export

The private prepared-export record retains the native view, final raw PDBQT text
and completed provider map returned by one writer operation. Public `to_pdbqt()`
still returns a string. Its existing torsion guard now lives in the shared export
operation, so staging cannot bypass it. No map is rebound or constructed locally.

Vina staging exports a prepared ligand once, retains that record through engine
execution, and sends its exact text to Vina. Input hashes and optional captured
bytes still describe that same payload. Source-free pose keys are read through
public conversion of the already staged bytes, preserving their existing written
IDs/hierarchy without another export. Source-backed keys come from the actual
exported view, including an independent value-adjusted copy when needed. The
caller source remains unchanged; an unchanged source can be shared read-only.
This record is an operation result, not a new molecular snapshot implementation.

## Reader and result axes

Before Vina starts, public MolSysMT queries select the supported profile: a
prepared native source with exactly one chemical state and connectivity declared
complete. That choice is retained; a later damaged source cannot silently switch
the operation to another parser.

For this profile, the adapter checks the completed map's hash against the staged
payload and calls `msm.form.string_pdbqt_text.read_poses` with the actual view and
unchanged completed map. Provider validation and errors propagate. The reader
owns MODEL grammar, atom fields, chemical source/tree binding and molecular
reconstruction. There is no local parser call or recovery after a reader refusal.

The reader returns native source-axis coordinates. Its explicit
`pdbqt_to_output_atom_indices` report orders the result coordinate array onto
DockingPose's existing written axis. Existing prepared/selected/source indices,
source keys, units, scores and ranks retain their meaning. Vina's independently
returned numeric array may have another order; the adapter retains only the
finite, three-decimal coordinate-multiset consistency check between the two
backend outputs. This does not infer atom identity or molecular correspondence.

`provenance.backend_output.pose_reading` records the public method and detached
native report, including original export-map and output-payload hashes. It
survives normal result serialization. Earlier result files remain readable;
no historical result or scientific population is rewritten.

## Explicit remaining profiles

External/unmapped PDBQT, incomplete source chemistry (including source-free
prepared objects), and sources with more than one chemical state retain the
existing local order verifier. This is selected before execution, never used as
a reader-error fallback. Provenance names `legacy_pdbqt_order` and the specific
reason: `unmapped_input`, `incomplete_source_connectivity` or
`multiple_source_states`. No missing graph or state is inferred to enter the
complete-source reader.

This bounded remaining duplication is owned by DockingMT #49/#33, with the
complete-source contract owned by MolSysMT #226. The executed partial/reference
extension is proposed in [MolSysMT #521](https://github.com/uibcdf/molsysmt/issues/521);
multiple native states retain a separate qualification question. Review
**2026-11-04**; remove it when
public provider operations are qualified for the actual remaining profiles,
including external written identity/grammar and partial source chemistry. The
existing complete-source API does not cover them, and complete-profile adoption
does not authorize expanding or duplicating that molecular API downstream.

## Evidence and limits

[Production guards](../../tests/test_prepared_pose_reading.py) exercise actual
Vina output for rigid/flexible complete sources under angstrom and pm policies,
nonidentity traversal and original source IDs, actual view/map object identity,
one export, manual value-adjusted copies, result roundtrip, source immutability,
reader failures and staged-file cleanup. Negative controls cover changed staged
bytes, a later damaged source, later-model charge/type/grammar failures and Vina
numeric disagreement. Explicit external/partial controls retain their known route.

The first 63-case run had 59 passes and four failed new assertions: three assumed
the actual exported view must be the original object even across unit roundoff;
one attempted an unsupported setter syntax in a damage fixture. The assertions
now require the actual writer-produced view/map pair, original source immutability
and explicit native test-state damage. Those diagnostics do not qualify a run.
A separate read-only probe reproduced an existing exact-comparison defect:
converting the public getter's coordinates back to the prepared unit could add a
round trip and falsely require copying unchanged data. Comparing the prepared
quantity directly in the getter's unit removes that round trip, without a
numerical tolerance. The existing uncopyable-resource guard now covers nm,
angstrom and pm; actual edits still require copying and propagate refusal.

The compact [source evidence](data/prepared_pose_reading_2026-10-28/manifest.json)
retains the corrected 209-case selection and 18-case reader/ownership controls,
with 29 administrative cases separately; counts overlap. Passing
ordinary-installed and exact-head CI receipts are recorded
separately under #49; overlapping counts are not summed. The package must be built
normally from its own producer and checked without checkout import shadows.

Task-owned resources are retained at `/tmp/dockingmt-pose-adoption-20261028`,
review **2026-11-04**, no automatic disposal, under #49/#50. Earlier artifacts,
receivers and provider binaries retain their own hashes and producers. No shared
environment or sibling source is modified. These are software/integration controls,
not biological preparation or affinity validation. #49/#33/#5 remain partial;
HTML/C6 #52 stays deferred, and public delivery remains #30/#47. No package or
GitHub Release is published.
