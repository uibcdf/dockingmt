# Native prepared-writer consumption — 2026-10-28

Owner: [BindingMT #49](https://github.com/uibcdf/bindingmt/issues/49), with
[#33](https://github.com/uibcdf/bindingmt/issues/33). This follows
[presentation receiving](pdbqt_presentation_receiving.md) at `fe9a48b` and consumes
the already qualified MolSysMT `e395e52646dab2ecb480d3d67aa7254be99b8524`.
ArgDigest/Viewer pins, source acquisition and public dependency metadata stay
unchanged. Provider API delivery and this production adoption are separate facts.

## Actual production calls

Both `PreparedLigand.to_pdbqt` and `PreparedReceptor.to_pdbqt` now call the public
MolSysMT native text converter. Their former ATOM formatting and ROOT/BRANCH
serialization loops are removed. The private consumer adapter declares the
existing output labels/serials, optional structural fields, caller attribution
and explicit docking ROOT/cut policy; MolSysMT constructs, validates and writes
the molecular representation. A returned completed export map checks that actual
written order agrees with the prepared object's declared axis. No completed map
is modified, and the engine does not yet consume that map.

For a source-backed preparation, identical native values are exported directly
through the read-only provider. This does not require copying unrelated caller
resources. Changed coordinates/charges/types require public `msm.copy` and
`msm.set` on an independent view; their actual source is never modified. Identical
native charges/types retain original/derived assignment reports. Manual replacement
uses public setters, which own attribution invalidation; it neither calculates a
model nor retains a false native claim. Existing consumer charge/type guards
still reject changes accompanied by stale named consumer evidence.

For a source-free object, `molsysmt.native.MolSys(n_atoms=...)` and public setters
receive the object's available coordinates, charges and labels. Public
`msm.element.atom.get_atom_type_from_atom_ff_type(..., typing_scheme='autodock4')`
decodes chemical elements from supplied AutoDock labels. No absent bond/order,
H inventory, scientific hierarchy or experimental identity is inferred. The
existing public `to_molecular_system` route can then read the provider-rendered
PDBQT and apply public inverse permutation/full-precision setters. Its writer
does not call it, so there is no writer/reader bootstrap cycle.

The old `autodock_element` dictionary is also removed. Its existing private
adapter, used by engine/reference checks, calls the same public decoder.
Classification, general molecular construction and format work remain reusable
provider operations; there is no consumer serializer or fallback.

## Compatibility and explicit limits

The existing prepared-name width diagnostic and torsion-count guard remain.
Output atom fields, group labels, chain A, occupancy 1.00/B factor 0.00,
three-decimal charges/coordinates, ROOT choices and BindingMT REMARKs are retained
for the covered profile. Native short-name alignment/branch whitespace and native
provenance REMARKs change whole-payload bytes. A rigid receptor also gets the
provider's terminal END record. Historical payloads, captured hashes and producer
receipts keep their original bytes; they are never regenerated to look current.

There is one deliberately exposed provider restriction. A known complete graph
with disconnected selected atoms cannot currently be declared as one rigid ligand
ROOT: native fragment validation rejects it. The existing acetamide C/N selection
still retains parent labels and projected attribution; ligand rendering refuses,
while rigid receptor format succeeds. The old local writer emitted this case.
The parent-label test continues to assert attribution, and a new end-to-end guard
requires the native refusal before Vina is constructed. No topology knowledge is
erased, branch invented or output patched to make it pass. The existing
[MolSysMT #214 profile question](https://github.com/uibcdf/molsysmt/issues/214#issuecomment-6478224407)
owns any future reusable extension. See [BMT-041](../DECISIONS.md#bmt-041--consume-native-prepared-pdbqt-writing-and-its-explicit-profile).

Source-free partial representations do not claim complete connectivity. They
remain writable under the provider's partial-data contract, with their known
precision, labels and explicit tree. This is not chemical-preparation admission.

## Checks and evidence

[Production delegation guards](../../tests/test_prepared_writer_delegation.py)
cover both roles, source-free rigid/nested trees, alternate units, source identity
and immutability, unchanged derived attribution, manual-value invalidation,
provider error propagation, the decoder call and the actual written-order map.
Existing reconstruction, named chemistry, native reader/export and real Vina
controls remain in the selection. The receptor four-character-name guard now
locates its ATOM record explicitly, preserving all column/engine assertions
instead of assuming it is the last line before native END.

Four independently captured before/after preparations (generated methanol,
flexible generated pentanol, charge-only ligand and charge-only receptor) preserve
all meaningful atom fields, full prepared charges, source/written maps, tree
records and original BindingMT attribution. Whole-byte hashes differ as declared.
The compact [evidence manifest](data/prepared_writer_2026-10-28/manifest.json)
retains comparisons, guard reports and source/provider identity. Full source,
ordinary-installed and exact-head hosted gates have separate receipts under #49;
overlapping selections are not summed.

Initial diagnostics remain distinct: an incorrect consumer root class spelling
failed before using the supported `molsysmt.native.MolSys` namespace; the first
181-case selection exposed the complete-graph restriction; a new negative fixture
initially omitted explicit charges and was corrected through public assignment.
Two superseded full runs were terminated and do not qualify anything. Final
passing selections and required exact-head gates retain their own results.

### Full-suite correction

Initial implementation `19637d74aa10acb7fd985234951aa02fe1ea1428` exposes eight
additional failures in its completed 1,261-case local suite. Four show unnecessary
copying during read-only export when a caller attaches a resource that correctly
refuses independent copying. The corrected unchanged-data path calls the native
read-only writer directly. Explicit molecular edits still require a provider copy
and propagate that same resource refusal; both paths are guarded.

Four failures come from a preparation-only partition spy remaining active during
native export's separate validation on the reduced atom axis. Its monkeypatch
scope now ends with preparation. All original full-H classification/partition,
retained identity, reference-tree and geometry assertions remain; the actual
writer validates the reduced graph without that test instrumentation. These
diagnostics and the initial wheel/producer remain historical, not a full passing
checkpoint. Final source/installed/exact-head results use the corrected source.
The [correction evidence](data/prepared_writer_correction_2026-10-28/manifest.json)
retains that unsuccessful full run and the corrected **212-case** source selection
(145.02 s, zero skips). Sixteen new guards are included in the overlapping
selection. The corrected implementation needs its own new ordinary artifact;
the initial `19637d7` wheel is preserved and does not qualify the changed runtime.

The new helper is included in the declared core/addon package inventory. A new
ordinary consumer wheel must be built from the actual implementation producer,
authenticated and tested without checkout import shadows; the old `fe8ad13` wheel
remains immutable historical evidence and cannot qualify this changed runtime.
Task-owned receiver/build/verification resources are retained under #49/#50 for
review **2026-11-04**, with no automatic disposal or shared-environment mutation.

## Next boundary

The production pose parser remains. Next request/retain the prepared writer's
actual source view, final payload and completed export map in the engine operation,
then adopt public known-source pose reading for those exact bytes. Do not export a
second live view and assume it has the same binding, or rebind a map to old bytes.
Existing numeric-array coherence checks stay engine-specific. #49/#33/#5 remain
partial; biological preparation/affinity, public delivery #30/#47 and explicitly
deferred HTML/C6 #52 retain their own acceptance. No package/Release is published.


## Caller-unit native comparison correction — 2026-11-09

[BindingMT#103](https://github.com/uibcdf/bindingmt/issues/103) and its
[receiving record](installed_small_fixtures_2026-11-09.md) extend the original
readonly contract to preparation/export unit cross-products. Canonical native
sources are read through public `Structures.get_coordinates()` (owned nm data)
and converted once to the actual prepared representation for exact comparison.
This avoids a round trip through the export caller's display unit. It does not
change process-global unit policy, use approximate tolerance, mutate the source
or suppress explicit-edit copies/resource failures. The existing generic
nonnative route retains its original behavior. Source receiving covers both
prepared roles, one-ULP edits and original MemoryError identity; actual new-wheel
receiving retains its separate gate. Historical outcomes above are unchanged.


The new real private wheel frombba53f6 now receives the correction:64 affected
cases and 20 new regression cases pass separately under both caller unit policies.
The original wheel's failed outcome and explicit provider warnings remain;
public/full scientific/platform acceptance is not inferred.


## Independent native materialization — 2026-11-09

[Reconstruction receiving](installed_reconstruction_2026-11-09.md) isolates #104:
reapplying unchanged prepared coordinates during native materialization can
change canonical bits. Both materializers retain mandatory provider copying and
reuse the export comparison to omit only unchanged coordinate assignment.
Actual edits still use the public setter; source-free parser/permutation and
generic-source behavior stay unchanged. The complete source52/20 selections pass
both policies; real new-wheel receiving remains separate. No general molecular
algorithm, approximate tolerance or provider-private read is introduced.


The actual aeae47d private wheel now passes both complete52-case and20-case
selections on the original provider cohort. Subsequent MolSysMT0c6f9c7 receiving
passes complete52/20/64-case installed selections normal/pm-fs and six original
owner controls. #675 removes index-only diagnostics without filters; #677 aligns
the catalog with the original22-atom input. Native/build/data bytes,606 support
records and other providers remain unchanged. Original failed/interrupted cells
and complete/public/platform/source-context gates retain their separate scope.
