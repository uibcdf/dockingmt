# Binding existing interaction analyses to a selected pose

Owner: [DockingMT #80](../pending_proposals/receive_docking_interaction_analysis.md).
The [saved-carrier receiving](e4_saved_carrier_receiving_2026-11-07.md) admits the
underlying one-frame provider composition. This increment implements its
docking-specific public association. Qualification of the new API on an actual
installed artifact remains separate from that earlier receiving and the source
boundary tests below. Whole E4, addon/canvas and public delivery remain open.

Later source correction: [DockingMT #89](../archive/interaction_binding_partial_carrier_diagnostic.md)
now reports absent carrier atom/frame counts or coordinate quantities as DMT-E002
for `molecular_system`, before scalar/unit extraction. Both public entry points
pass the complete 78-case binding/view selection normal and pm/fs; the original
six failures remain frozen. This is source admission through provider doubles,
not a new real molecular, installed or canvas acceptance. The later
[complete editable catalog receiving](e4_evidence_catalog_editable_2026-11-08.md)
separately clears the historical #642 persistence hold for its original profile.

Subsequent [installed candidate receiving](e4_pose_binding_installed_2026-11-07.md)
now passes normal/pm-fs on the original retained and separately derived
evaluated-empty carriers, plus independent record reading. Its actual source,
artifact, domains, refusals and limits remain separate from source tests below.
The separate [native information-state receiving](e4_native_unevaluated_2026-11-07.md)
now passes empty-source invalidation with no evaluated frames. Positive-source
invalidation persistence fails under MolSysMT #642; complete label preservation
and actual addon/scene admission remain open. These bounded outcomes are not
whole E4, public delivery or producer authentication.

## Public operation and ownership

```python
binding = dmt.bind_interactions(
    result,
    admitted_carrier,
    pose_index=1,
    pose_atom_indices=original_pose_atom_indices,
    partner_state_id=known_partner_state_id,
    receptor_state_id=known_receptor_state_id,
    assume_aligned=True,
)
analysis = binding.get_analysis('hbonds')
```

`PoseInteractions` is the returned public type; its constructor accepts the same
arguments and performs the ArgDigest contract once. The convenience function
delegates that validation. Position 1 is the second collection member; it is
independent of scientific rank and pose ID. Each supplied map entry identifies
one carrier atom in original pose order. Nonmonotonic maps retain that order.
No molecular matching, atom reordering inference or geometry transformation occurs.

The operation preserves a complete detached result snapshot. `binding.result`
restores all original poses, scores, rankings and provenance with the existing
DockingResult codec. `binding.pose` restores only the selected pose. Their edits
cannot change the source result or the retained binding. An in-memory molecular
problem handle is not recreated by that record restoration.

The carrier must have one structure and existing named full analyses. Its public
MolSysMT accessor owns analysis type/full-domain/axis validation. The binding
copies the complete carrier through MolSysMT, preserving its native domains and
producer declarations. `get_analysis(name)` returns the provider's independent
analysis copy for its supported filtering and interchange APIs.
`to_molecular_system()` returns a detached complete carrier for MolSysMT's
supported molecular persistence. These accessors neither create observations
nor attach anything to a Viewer. Numeric observation blocks may remain shared
under MolSysMT's immutable-storage copy contract; mutable metadata is independent.

## Declarations, checks and limits

The caller supplies an **already admitted carrier**, its known partner/receptor
state IDs, an explicit pose-to-carrier atom map and the common-frame declaration
`assume_aligned=True`. The IDs must equal nonmissing selected-pose state IDs.
These are declarations, not proof of chemical equivalence, original receptor
geometry, frame authenticity or scientific validity of stored analyses.

The binding validates a nonnegative integer position, nonempty unique integer
map, map length/bounds, verified pose atom records, ordered mapped carrier atom
labels/elements and physical mapped coordinates. Only the mapped pose atoms are
coordinate-checked. The existing DockingMT atom-key bridge reads provider data;
its optional explicit axis is accounting, not a new molecular matcher. Existing
[#49](../pending_proposals/retire_general_molecular_operations.md) provider/bridge work
retains its separate scope.

Coordinate comparison has relative tolerance zero and a default absolute
tolerance of **1e-12 angstrom**. An explicit override requires a finite
nonnegative scalar length. Conversion/comparison use PyUnitWizard with explicit
angstrom boundary units, preserving the caller's active unit policy.
`association` records the actual tolerance and its limited scope. It also records
each original analysis's evaluated-frame flag: evaluated-empty and unevaluated
remain distinct. An association does not establish evaluation of other poses.

The operation rejects unknown pose maps/states, incompatible mapped identities
or coordinates, missing named analyses and multi-frame carriers. It neither
projects an analysis to another scene nor replicates a saved frame across a pose
collection. No hydrogen generation, preparation, typing, charge assignment,
detector, RMSD, alignment, scoring or native search is part of this operation.
MolSysMT owns all molecular serialization; the association dictionary is an
inspection snapshot, not a complete persistence codec or authenticated receipt.

Absent atom/structure counts and absent coordinates are also rejected with the
local `ArgumentError` for `molecular_system`, identifying the domain the caller
must supply. A valid partial molecular representation is insufficient for this
specific association. Errors actually raised by the provider propagate unchanged;
the binding does not replace their exception type or generate missing data.

## Registered source qualification

Before executing the new tests, select `tests/test_interaction_binding.py` and
the existing pose-coordinate/result/argument-contract regressions applicable to
the shared helper and registry. New binding tests use explicitly synthetic
provider protocol doubles, not molecular detectors or scientifically received
MolSysMT objects. They establish consumer selection/association, fail-fast
validation, units, evaluated/unevaluated distinctions, detachment and source
nonmutation. They cannot establish real provider/artifact compatibility.

Execute the finite source selection serially in routine Python 3.14, with one
logical CPU, nice 10, one native/build worker and an 8 GiB available-RAM reserve.
Use a task-owned monitored process group, 1 GiB group RSS, 2 GiB address space,
45 CPU seconds and 60 wall seconds; stop only owned work and preserve resource
interruptions without an automatic retry. Pytest uses `--receptor=llm`; retain
raw output, exact source/selection, exit status and final test counts. Scientific
preparation/H/typing/charge/detector/metric/search budgets are all zero.

The next receiving registers the new actual candidate source/artifact and
original one-frame carriers, then qualifies this public API and its refusals
normal first, pm/fs second. Do not relabel the earlier `a7422df` private consumer
as an implementation of this new API. Actual addon/scene association additionally
requires its own admitted axes and source relationship; canvas remains deferred.

## Source qualification outcome — 2026-11-07

The [exact source-test receipt](data/pose_interaction_binding_source_2026-11-07.json)
records **190 passing cases**: 44 new binding protocol-double controls and 146
existing coordinate/argument/model/result regressions. Both public entry points,
nonmonotonic integer maps, pm/fs caller policy, physical tolerance, producer/
score preservation, accessor detachment and adverse inputs pass. Real MolSysMT
operations are forbidden by the worker; no Vina module is imported. This proves
consumer logic, not actual provider/native-system or installed-artifact receiving.

The initial collection fails because a synthetic boolean fixture is rejected by
Pint before it reaches the binding. The next attempt passes 184 cases but fails
when another synthetic fixture performs in-place floating conversion into an
integer array before the translated-carrier refusal. Both failures are retained;
neither is reported as a provider defect or hidden by a skip. Corrected fixtures
pass the complete selection in `source-tests-04` with no resource interruption.

The owned process is terminal after 2.762 wall seconds, sampled peak group RSS
128,102,400 bytes, under the registered one-CPU/worker, nice10, 1 GiB RSS/2 GiB
address-space and 45 CPU/60 wall-second limits. The monitored 8 GiB reserve is
preserved. These are source-test resource observations, not API throughput or
scientific performance measurements. Task sources, raw logs, JUnit, exact
collected reports and all attempts remain under
`.molsyssuite/e4-pose-binding-20261107` with #50 custody, review 2026-11-14.
The shared guard proposal remains MolSysSuite #173; frozen guard functions are
reused by hash rather than modifying the historical producer.

The first collection failure also reproduces known
[Pytest Receptor #46](https://github.com/uibcdf/pytest-receptor/issues/46): the
local 1.2.0 compact header says `1 of 146 executed` although the component
worker records zero completed cases and no test-phase reports. Exit 2 and the
`COLLECTION_ERROR` verdict remain correct; this is count/phase fidelity, not a
false PASS. Keep the actual pytest events, JUnit and process status authoritative.
The owner receives this consumer evidence; no tool fix or dependency change is
included here. Reassess the workaround after a provider fix and actual consumer
qualification of the chosen published tool.
