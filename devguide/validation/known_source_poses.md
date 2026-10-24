# Known-source PDBQT pose receiving — 2026-10-24

Owners: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49) and
[#33](https://github.com/uibcdf/dockingmt/issues/33). This qualifies the native
projection → mapped export → actual DockingMT/Vina output → public known-source
reader workflow. Production `VinaBackend` still uses its existing PDBQT parser;
its prepared-input serializers do not yet produce the reader's completed maps.
The test makes that remaining boundary explicit instead of fabricating a map.

## Delivered provider capabilities

The already qualified MolSysMT
`128a0bbb94e6804f5663e58a45313c77de1cc30d` contains both:

- `build.merge_nonpolar_hydrogens`, producing an independent reduced molecular
  system, charge aggregation with original/derived attribution and explicit
  `molsysmt.atom_projection@1` axes;
- native PDBQT export with `return_atom_map=True` and
  `form.read_pdbqt_poses`, receiving a complete known chemical source and the
  completed `molsysmt.atom_export@1` report.

[MolSysMT #226](https://github.com/uibcdf/molsysmt/issues/226) is delivered.
[#223](https://github.com/uibcdf/molsysmt/issues/223) remains open for its broader
scope, including earlier generated-atom map composition and downstream adoption;
its public typed-H projection and completed export-map slice is already delivered.
Earlier consumer text treating all of #223 as undelivered was too broad. No source
pin or dependency floor changes are needed to qualify this slice.

## Actual consumer workflow and independent controls

[The consumer module](../../tests/test_known_source_pose_consumption.py) calls
only public MolSysMT operations for molecular building, copying, projection,
conversion and reading. Literal ROOT/branch fixtures specify docking choices;
they do not discover atom correspondence or reimplement a molecular transform.

Rigid methanol and explicitly flexible hexane exercise a nonidentity writer
axis, three displaced MODEL records with labels 9/2/51, default/nondefault physical
units, file/text inputs and JSON-decoded maps. Independent source-coordinate
expectations allow only PDBQT's 0.000501 angstrom serialization tolerance. Returned
coordinates are on the known source axis; public report arrays bind them back to
the written axis and then to the pre-projection source. No coordinates are assigned
to merged H, and no earlier H-generation correspondence is invented.

Four immutable Vina SDF references exercise the existing explicit RDKit input
bridge followed by fixed-state H materialization, named charges/types, explicit
positive serial-ID presentation and public reduction/export/read. The two 5X72
inputs are the hydrogenated `p59H`/`p69H` files, not their different heavy-only
geometries. The reader retains the staged source's chemical-state tables and
rounded coordinates. This does not claim untreated native SDF is already ready
for charge assignment or projection, nor certify original published chemistry.

Two real DockingMT/Vina software controls, under angstrom and pm/fs/coulomb
policies, submit the public native payload with its completed map. They capture
the actual ensemble returned to the existing adapter, then read it publicly
against the known reduced source. Mapped coordinates agree with every normalized
DockingMT pose within `1e-10 angstrom`. Input/export and output/reader hashes bind
the actual bytes. Vina's numeric-array comparison stays an engine-boundary guard;
scores/ranks retain their existing producer and are not inferred by the reader.
These synthetic receptor/hexane controls are not biological redocking, registered
3PTB searches or affinity validation. Their result assessment remains unassessed.

All-model validation rejects malformed/unbalanced or duplicate MODEL records,
changed types/charges and nonfinite coordinates even in an unselected later pose.
Selection preserves positions/repetitions and supports an empty structure axis.
Incomplete legacy maps, duplicate correspondences and a changed source identity
reject without repair or source mutation. Explicit `missing_atoms='omit'` returns
a subsystem; it does not create the virtual-H inventory produced by actual typed-H
merging. Source states, coordinates, assignments and caller maps remain unchanged.
The result intentionally carries neither old mechanics nor source time/box/analyses;
its report retains written charges/types without calling them new calculations.

## Production integration boundary

Existing preparation can consume a publicly reduced input: native derived
assignments project correctly, the three-atom methanol preparation and charge
audit succeed. Its legacy PDBQT serialization still uses a different serial/
presentation axis and different bytes from the completed native export.
`test_legacy_preparation_does_not_acquire_a_native_export_map` demonstrates that
passing those legacy bytes with the native writer's map rejects. Equal atom
counts and existing retained indices do not bind a new map to another payload.

Therefore the next implementation is producer-first: consume the public molecular
projection and mapped native writer in the supported prepared-input path, preserve
stage/source/export axes and original/derived attribution, and explicitly qualify
serial IDs, group/name presentation, ROOT/branch layout and numerical rounding.
Then replace pose parsing for that bound profile while retaining Vina consistency
checks. Do not add a consumer molecular snapshot, projection/permutation helper,
completed-map constructor or silent reader fallback. External/unmapped inputs
keep their tracked limitations. Native permutation remains provider-owned #369.

## Evidence and runtime limits

The [versioned manifest](data/known_source_poses_2026-10-24/manifest.json) retains
compact executed reports, real native-reader audits and runtime/source identities.
The initial 23-case module passes in 25.76 seconds (19 existing structural warnings);
the 105-case engine/export/format/result/flexibility source selection passes in
91.40 seconds. A broader source-free selection of 272 tests passes in 164.19
seconds, zero skips, including all 24 historical rows / 167 poses with repeated
historical preparation/scoring/search forbidden. The added legacy-map boundary
has separate focused and installed evidence: the final module passes all 24 cases
in 25.26 seconds, and the additional installed boundary passes in 2.86 seconds
with the same in-process import guard (272 other cases deselected). The installed
profile covers 273 distinct cases across the two runs. Overlapping focused/source
counts are not summed, and the earlier 272-case run is not relabelled.

The ordinary installed producer remains DockingMT
`173319a71b17b70bc6d13ecc68eb413edfd08640`, wheel SHA-256
`81e12debc9c3c32c1fae7cf9cdade32f593af79ef4a73859a4850a6caaa4147f`.
This task changes tests/guidance, not runtime package code; the original wheel and
receiver are preserved. Its Python 3.14.8, pandas 3.0.6 and normally compiled
MolSysMT wheel/native identities remain those of the
[retained-connectivity receiver](retained_connectivity.md). Ordinary import origins
are checked in the same test process. Local source selection and exact-head hosted
source CI are separate; final outcomes are recorded in #49 after the unskipped push.
No public artifact/pair/platform admission follows from these bounded controls.

Initial failed fixture attempts are retained separately: invalid zero/generated
serial IDs, the wrong 5X72 filename/hash pair, missing raw-input H-inventory
prerequisites and expecting an iterable structure-ID field on an empty structure
axis. The final profile declares valid serials and uses the existing explicit
H stage; empty labels remain in the report with no invented structure. These are
corrected qualification assumptions, not failures of the delivered reader.

Task resources belong to #50, review by 2026-10-31. Preserve its dependency on the
preceding task receiver (review 2026-10-30) and original scientific runtime (review
2026-10-27) while used. Dates do not authorize automatic deletion. The refreshed
suite inventory preserves sibling worktrees and human edits. Original scientific
archives and scene/notebooks remain unchanged. HTML/C6 review stays deferred,
public delivery remains #30/#47, and no package or Release is published.
