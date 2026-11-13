# H-R2: characterization evidence alongside a native hypothesis

Owner: BindingMT #112; provider feedback remains PyUnitWizard #156 and
PharmacophoreMT #202. Admission: 2026-11-12 before implementation.
Status: bounded H-R2 native source workflow implemented and received; broader consumer/public adoption pending.

## Selected workflow and boundaries

Extend the useful native ionic I0/H0/I1 route with
`BindingInterface.with_characterizations(molecular_system, *, characterizations,
participant, query_ref=None)`. The input is an immutable native ionic characterization, optionally
already associated with exact saved PharmacophoreMT hypotheses. The caller supplies
the unchanged full MolSys and a nonempty named mapping of actual native contact
and/or surface/burial BindingInterface results. The named target has the same
label/source atoms in those results and constitutes one whole side of the ionic
binary grouping. The other side represents the same combined counterpart atoms.
This initial identity-axis Cartesian profile implements no label remapping,
partial composite-side projection or chemical-state transfer.

BindingMT composes participant-level evidence and exact atomic contributor
references; it does not reinterpret evidence as feature recognition, site membership,
query importance or affinity. The complete original records retain their own
criteria, radii/probe/H policy, output/occluder populations, coverage, units,
original provenance and numerical status. Ionic full-source context may include D
while the contact/burial environment is explicitly A+B+C; these meanings remain
separate. The composition infers no universal normalization or statistical support.

All molecular checks use existing public MolSysMT operations. Reuse the admitted
ionic source recheck and each calculation's actual geometry snapshot order,
frame/state/source labels and original local/source axes. For surfaces also verify
current public element-vdW radii against the saved model. A usable surface profile
is required; inconsistent negative losses refuse this annotation route while the
original result remains inspectable. No detection, SASA/contact recalculation,
chemical repair, matching, native artifact lookup or scientific-provider fallback
is introduced by annotation. The caller still admits unchanged complete topology
and original analysis identity; snapshots are not foreign-source authentication.
Recheck the borrowed source after composing; no atomic concurrent-edit guarantee.

## Result, persistence and semantics

Return a new immutable BindingInterface with an immediate parent and explicit
reason. Original question, analyses and hypothesis/site references stay intact.
The optional namespaced extension `bindingmt.interface_characterizations`,
definition `bindingmt.native_characterization_annotation@1`, stores the complete
native core records plus their exact identities/digests, target participant,
per-atom contact-witness or atomic-loss-position references and historical checked
source facts. No atom is dropped for zero area/contact membership. Group coverage
remains as declared by the originating calculation. This is participant evidence;
no continuous patch, new functional site or guessed per-feature area is produced.

Core format 0.4 retains its version: this is an explicitly optional namespaced
annotation, without a changed native observation definition. Current readers
validate the known extension and embedded native records offline; older readers
may preserve it opaquely and gain no interpretation/assurance from that preservation.
Reads never restore a current check or consult a molecular/native asset. Copies
retain identity; later reinterpretation keeps original annotation provenance.
An already annotated record refuses replacement/stacked annotation in this finite
route; make a new annotation from its unannotated parent instead. Historical
records and original external/native files remain intact on failure.

The operation accepts no native hypothesis handle and imports no PharmacophoreMT.
Thus it changes no essential flag, weight, geometry/direction, tolerance, exclusion,
score, model metadata, saved hypothesis bytes or evaluator policy. The link already
in I1 retains its exact native asset and construction context. The optional `query_ref` can retain an exact caller-declared saved hypothesis
URI/SHA-256 when a curated query does not qualify the stricter observed-construction
linker; such declarations are labelled
caller evidence and do not gain native-construction authority. There is no new
curation/linking API in H-R2.

## Receiving and completion

Use the unchanged frozen cb6af716 four-ion source and actual public native ionic,
contact and SASA/burial operations. Preserve precise criterion/contributor and
unit fields through emitted I2 save/read, copy and reinterpretation. Check known
zero evidence, changed source/frame/state/maps/participants, failed required child,
malformed/tampered annotation and already-annotated input refusals.

Run actual before/after evaluation and public native hypothesis save/read for the
observed primary/alternative, explicit keep-policy, absent essential site at weight
zero and independent exclusion cases. Expected decisions/fit remain independently
specified (1/matched, 0/not_matched, 0.5/not_matched and positive fit1/rejected).
Check the actual flags, geometry, metadata and original file bytes, not just a
summary label. Annotation is stored in BindingMT, never by editing PHMT native files.
Owner-only curated queries retain their own original native persistence and are
not promoted through the I1 observed-construction linker merely to run this check.

Cold core reading forbids molecular calls and optional scientific providers;
explicit owner-native readback/evaluation has its own scoped provider requirements.
Pint normal and pm/fs qualification includes the matching operation's angle
standard; unyt native construction remains pending #156. Core read under unyt
remains an independent no-recognition case. Scientific cells stay serial CPU0,
nice10, native workers one, monitored 13-GiB available reserve and 512-MiB owned
RSS cap; no shared-prefix change, native rebuild or held-suite restart. Preserve
all attempts and exact source/provider/native and frozen input identities. T0/T1
remains deferred optional interoperability; H-R1/P/#111/#30/#195 keep their owners.

## Delivered workflow

```python
from bindingmt import BindingInterface

# linked is an admitted native ionic BindingInterface, optionally with its
# exact original saved PharmacophoreMT hypothesis/site references.
annotated = linked.with_characterizations(
    system,
    characterizations={'contacts': contacts, 'burial': burial},
    participant='C',
)
print(annotated.summary()['characterizations'])
contacts_record = annotated.characterizations['contacts']['record']
annotated.save('I2.json')
restored = BindingInterface.read('I2.json', experimental=True)
```

`contacts` and `burial` are actual results from the existing public calculation
entry points, using explicit cutoff, probe and sampling. The target is C and the
counterpart is A+B in this admitted example. Labels/source axes align explicitly;
no atom/source matching is inferred. `query_ref={'uri': ..., 'sha256': ...}` can
add a caller-owned reference for a separately curated native hypothesis. That
reference stays caller-declared and is not opened, reconstructed or granted new
native-construction/context authority. The existing stricter I1 linker is unchanged.

`characterizations` returns detached evidence with full original records and
exact definition/identity/digest, including per-target-atom contact witness indices
or atomic-loss positions. Original area/distance quantities stay sealed. The
positive authored example has two geometric contacts involving C but only one
ionic occurrence per labelled analysis; their different criteria remain intact.
Zero contact evidence keeps C's atomic membership with an empty witness list.
Both side losses and the total/mean area conventions remain in the saved surface
result, without becoming a membership threshold or query weight.

The source operation checks current source, original input group/state mapping,
model radii and actual selected-coordinate fingerprint before/after composition,
through public MolSysMT queries/shared admission. Saved annotation checks are
historical. Copy/read preserve identity, while reinterpretation makes a new record
and keeps original annotation/source links. Inconsistent burial, changed source,
nonidentity maps, different frame/participants/labels, malformed annotation and
repeated replacement refuse. Existing data and native query assets remain intact.

## Executed source receiving — 2026-11-12

The new module supplies **33 passing H-R2 controls**. The complete affected source
selection reports **304 passed and 1 strict xfailed per unit policy**, normal Pint
and pm/fs with the matching operation's explicit angular standard. The sole xfail
is the already reported native unyt charge conversion in PyUnitWizard #156; it
is neither a new failure nor a qualified native backend. Annotation under unyt also remains affected by the source
recognition gap; no workaround is introduced. Core reading under
unyt/pm-fs is separately exercised without recognition or optional scientific tools.

Seven independently specified before/after query decision cases cover primary
and alternative sources, explicit keep policy, absent essential weight-zero and
exclusion veto. A further authored optional directed query constraint retains its
actual `[1,0,0]` direction, flags, radius and a 12-degree matching tolerance through
native readback and evidence annotation. Those authored constraints are software/
consistency controls, not additional ionic detector observations. Real owner-native
query files are byte-identical before/after annotation and read/write, and query
fit/decisions remain equal to independent expectations. No curation authority is
inferred from the optional reference.

Adverse source/group/frame/map/context, required-child and tamper controls pass.
The deliberately injected inconsistent SASA child is a named software adversity
control, not measured physical negative burial. The first fixture attempts
retain the incorrect record-exception expectation and direct structure append
with stale unrelated analyses; the corrected frame fixture clears analyses only
on its independently copied geometric input. A later test-only missing import
attempt is also preserved. No owner defect or source correction is invented for
these local fixture errors.

The actual public workflow emits three I2 core records (observed linked, curated
reference and known-zero), two owner-native queries and a complete H5MSM source.
Cold readers independently inspect the three records/five embedded native records
with PharmacophoreMT/TopoMT/Vina unavailable, then explicitly exercise native owner
readers with molecular detection/recognition/queries forbidden. Files, units,
constraints and provenance remain intact, and saved reading captures zero new
originating uses. The source never needs PISA.

Participating runtime source: MolSysMT ff25f120, PharmacophoreMT c2ad4e6,
PyUnitWizard cc51c8e, ArgDigest 7be790b, SMonitor 4a4cd1e and DepDigest 5e93eaf.
Historical version strings remain separate from Git/content identities. Loaded
MolSysMT `_rust.abi3.so` SHA-256 is
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`;
its original builder/source identity remains unauthenticated. Frozen cb6af716
inputs and all installed-test-support hashes retain their original producer and
bytes; this increment changes no fixture/helper/resource declarations.

Concurrent PharmacophoreMT work modified only unrelated owner tests/devguide
files during one otherwise passing attempt. Its whole-worktree guard failed and
that attempt is preserved, not counted as final qualification. Final cells bind
all participating runtime Python file hashes plus Git heads and actual native
bytes before/after, and preserve separately measured dirty tests/docs without
editing them. Other unexpected provider changes refuse the guard. This is a
scoped source custody rule for this receiving, not an exemption from component
full-suite/admission requirements or permission to overwrite sibling work.

Exact BindingMT/runtime/test/provider snapshots, raw outcomes, concurrent-work
receipts, original failed attempts, actual saved workflow/readers, resource and
final workspace/fresh committed-export checks retain #50 custody in
`.molsyssuite/interface-characterization-annotation-112-20261112/`, review
2026-11-14. Scientific cells use one logical CPU/nice10/native worker, a monitored
13-GiB available reserve and 512-MiB owned-group RSS cap. No resource interruption,
shared-prefix edit, native rebuild or held scientific-suite restart is part of
this increment. Hosted/installed/public/platform and broad chemical/mapping
qualification remain separate.

## Next owner actions

H-R2 is source-received for the selected participant-level native contact/surface
annotation. Regional H-R1 is conditional on its separate accepted workflow.
The subsequent [BindingMT #114 correction](archive/interface_json_object_order.md)
separately qualifies sorted/reversed objects and new ionic order records; see the
compatibility checkpoint below. Receive remaining exact PeptideMT P inputs and
execute their admitted public controls; record shared/consumer disposition under MolSysSuite #195 rather than
claiming adoption from these local results. PyUnitWizard #156 and PharmacophoreMT
#202 remain with their owners. PISA T0/T1 stays deferred optional interoperability;
#111, #30 and complete #112 acceptance retain their separate gates.

After source receiving, PharmacophoreMT committed its previously preserved test/
documentation work as 878864e. Its full diff from tested c2ad4e6 changes only tests/
devguide, with identical runtime Python bytes. Both identities and their complete
measured diff are retained; no runtime or imported version metadata was replaced.

## JSON ordering and historical compatibility — 2026-11-13

The [#114 resolution](archive/interface_json_object_order.md) extends the original
own-writer receiving above to sorted/reversed JSON objects. New ionic collections
use experimental record 0.5 with explicit `context.analysis_names`. Actual old
0.4 I0/I1/I2 remain unchanged/readable; a saved construction supplies known order,
while bare I0 reports `interaction_analysis_order is None`. New construction from
unknown-order history must supply explicit `analysis_names`; that new choice is
attributed to the caller rather than the old producer. Known order cannot be
overridden. The actual old decoder refuses new 0.5 records before molecular work.
The package's 0.1.0 source tag is unchanged.

Contact/surface orientation and nested annotations use original ordered operation
axes. The new 30-control module plus complete directly affected source modules
report 229 passes/1 strict PyUnitWizard #156 xfail per policy, normal and pm/fs
with radians. Actual core/native cold readers inspect 13 sorted records under
unyt/pm-fs without recognition; original witnesses, lists, maps, quantities,
producers, historical checks and native query files remain intact. See #114 for
the selected population, exact source/native/fixture/resource identities and
remaining qualification limits. The older counts/producers above remain the
original receiving populations, not silently rewritten evidence.
