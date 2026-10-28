# Native prepared-writer consumption — 2026-10-28

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), with
[#33](https://github.com/uibcdf/dockingmt/issues/33). This follows
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

For a source-backed preparation, public `msm.copy` and `msm.set` supply its current
coordinates without changing the source. Identical native charges/types retain
their actual original/derived assignment reports. Explicitly manual replacement
uses public setters, which own attribution invalidation; it does not calculate a
model or retain a false native charge/type claim. Existing consumer charge/type
guards still reject changes accompanied by stale named consumer evidence.

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
three-decimal charges/coordinates, ROOT choices and DockingMT REMARKs are retained
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
owns any future reusable extension. See [DMT-041](../DECISIONS.md#dmt-041--consume-native-prepared-pdbqt-writing-and-its-explicit-profile).

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
records and original DockingMT attribution. Whole-byte hashes differ as declared.
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
