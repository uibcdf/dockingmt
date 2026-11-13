# Native Cartesian contacts: first N0/C admission

Owner: BindingMT #112; molecular owner: MolSysMT #734; shared coordination:
MolSysSuite #195. Admission recorded 2026-11-12 before implementation.
Status: **first Cartesian native source profile implemented and received; broader/installed adoption pending**.

## Selected public and scientific profile

`calculate_interface_contacts(molecular_system, *, participants, cutoff,
structure_index, source_id, atom_map=None, source_structure_index=None,
max_dense_pairs=65536)` returns an immutable `BindingInterface`.
`participants` has exactly two names mapped to MolSysMT selections. The cutoff
is an explicit finite nonnegative length, without an implicit scientific default.
`structure_index` selects one existing Cartesian structure. Coordinates must be
finite, unwrapped in the intended common frame and stable during the call.
Identity, topology/state association and participant interpretation must also
remain stable while the borrowed input is used.
Admit the intended chemical state, present H representation and no inter-side
covalent link as caller preconditions; geometric contacts do not prove those facts.
The source is an existing native MolSys, not an automatically prepared input.

Definition `bindingmt.cartesian_atomic_contacts@1`: unique cross-participant atom
pairs whose MolSysMT distance is <= cutoff, including equality, with no added
tolerance. PBC, alignment, completion, radius overlap and chemical recognition
are outside this profile. Distinct/empty/unresolved participant requests refuse;
nonempty participants with zero contacts yield completed evaluated-empty results.

## Molecular operations and ownership

Only public MolSysMT operations inspect forms/counts/coordinates/state/groups,
resolve selections, normalize declared maps and calculate geometry. BindingMT
contains no selection parser, molecular representation, matching operation or
contact/distance search kernel. Source baseline inspected:
`ff25f120243319ca9515009b4971e24a2eb0dc22`; restricted owner contract received at
`04bf56131fd0cea94359e1f0f9307d0f0e36b3cb` under #734.

Use `msm.select` for exact ordered endpoint axes and `msm.get` for selected
coordinates, actual atom-group correspondence, structure count/state association.
Call `msm.structure.get_contacts(..., pairs=False, output_type='pairs',
output_indices='atom', pbc=False, use_gpu=False, cell_list=False,
parallel=False, num_threads=1)` and `msm.structure.get_distances` on the same
explicit axes/structure with Cartesian product and CPU-one settings. Keep owner
exceptions as failures; never translate missing proof or a failed child to zero.
No optional TopoMT/PISA or engine is required for the native calculation.

## Axes, records and footprints

`source_id` names the caller-admitted source axis, without authenticating it.
By default it is the input MolSys atom axis and chosen structure. An optional
owner `atom_map` is validated/normalized by `msm.compose_atom_maps` and must map
all selected local atoms bijectively to known original-source atoms. With a
map, supply the corresponding original `source_structure_index` explicitly.
These declared maps transport correspondence; they do not prove foreign assets
share a molecular identity. No generated atom acquires an original identity.

Pairs retain requested endpoint order, exact source/local labels and all atomic
witnesses. Owner atom-group indices support unique ordered group-pair reduction;
counts name unique atomic pairs or unique group pairs, not independent support.
Group indices name the input MolSys group axis; no original-source group map is
invented. Missing group membership yields partial coverage and an unavailable
complete group count, while geometric contacts remain useful.
Each side's contact footprint has ascending source indices and position-aligned
local indices, exact calculation/parent/context/criterion and every contributing
pair. Positive and evaluated-empty footprints have their own safe public save/read.
They are not continuous patches, binding sites or affinity estimates.

The declaration-only 0.1 record remains readable. Native calculation records
use experimental 0.2, whose required calculation semantics an older reader must
refuse. Known cutoff/distance fields use PyUnitWizard QuantityRecord with exact
field and [L] handshakes. Reads preserve original evidence and historical checks,
perform no molecular/asset lookup, restore no active policy and earn no new
originating calculation credit. Copy/read retain identity; reinterpretation keeps
original calculation associations. Context applicability after edits needs a new
calculation; saved evidence is history, not an active match.

## Resource and attribution contract

The selected owner route is explicitly dense; pair output retains a Boolean map.
Refuse a Cartesian product larger than `max_dense_pairs` before numeric calls.
The default admits 65,536 candidate pairs, estimating arrays plus boxed/JSON
composition conservatively at 1,024 bytes per candidate, plus coordinate/map
inputs. This is an application admission bound, not reserved RAM or process RSS.
Higher budgets/larger sources need caller resource admission and separate measured
receiving. No hidden CSR/dense fallback, GPU or all-core dispatch is allowed.

Record actual child operations/options, molecular/package source versions,
CPU/backend, candidate count, estimated payload and source/state/maps. Raw owner
arrays gain no fabricated foreign analysis/run ID. BindingMT owns its composed
calculation identity. Generic Cartesian cutoff/distance has no new reference
program or chemical method credit; preserve actual MolSysMT implementation credit
and distinguish numerical execution from saving/reuse. Optional Ackredit events
retain their owner semantics when reached; no unused integration is introduced.

## Receiving and completion

Freeze a tiny authored MolSys with independently specified inside/on/outside-cutoff
pairs; exercise reordered axes, exchanged sides, zero, invalid requests,
nonidentity owner permutation maps, original structure 2/local 0, group witnesses,
normal/pm-fs sealed quantities and malformed/tampered/dimension refusals. Spy on
actual owner calls and forbid any optional provider/engine. Public result and
positive/empty footprint save/read must succeed in a fresh process that forbids
molecular calls. Preserve originals and required-child/resource failures.

Run serially, CPU-one/nice 10, native workers one; reserve 13 GiB available RAM
and monitor owned descendants. No native rebuild/shared-prefix repair or held
full scientific selection is authorized by this profile. Record actual source,
loaded ABI SHA-256, environment and all attempts before calling receiving complete.

## Delivered public workflow

```python
import bindingmt as bmt

result = bmt.calculate_interface_contacts(
    system,  # an admitted native MolSys, stable for this call
    participants={'A': 'chain_index==0', 'B': 'chain_index==1'},
    cutoff='0.5 nm', structure_index=0, source_id='my-admitted-source',
)
print(result.summary())
result.save('contacts.json')
footprint = result.project_footprint(participant='A')
footprint.save('A-contact-footprint.json')
restored = bmt.BindingInterface.read('contacts.json', experimental=True)
restored_footprint = bmt.ContactFootprint.read('A-contact-footprint.json', experimental=True)
```

The example cutoff is a caller choice, not a scientific default. The native
result's summary exposes actual atomic/group counts, cutoff criterion, selected
checks and limits. `contact_calculation` exposes detached expert records. The
footprint retains canonical source members/aligned local members, all witnesses,
original calculation and exact parent; it can be independently read/copied/saved.
The first 0.2 record admits exactly one native contact analysis; ambiguous multiple
native analyses refuse. Data-only 0.1 records retain their original behavior.
Common I/O now lives in private `interface_records` and is shared by both actual
record types; molecular representations and generic inspection stay in MolSysMT.

## Numerical verification versus membership

Contact membership is exclusively the inclusive predicate executed by MolSysMT.
No extra tolerance is supplied to that calculation and no local search/filter
kernel is introduced. The separately returned distance can acquire binary64 unit-
conversion roundoff: unyt pm/fs receiving observes `1.0000000000000002 nm` for
an owner contact at the nominal 1-nm boundary. Preserve that raw value.

Portable distance verification has a distinct explicit relative bound of eight
binary64 epsilons (zero absolute bound), with per-contact `consistent` or
`within_conversion_roundoff` status and `changes_contact_membership=False`.
Values outside that bound refuse. This is neither a changed geometric cutoff nor
physical uncertainty. Known fields use QuantityRecord and explicit nm/[L]/Pint
receiver handshakes without altering the application's unit policy. Tests retain
exact owner membership at/just below the cutoff and reject resealed wrong-field,
time-dimension and out-of-bound distance payloads.

## Executed source evidence and limits

Task receipts: `.molsyssuite/interface-native-contacts-112-20261112/`, #50 custody
review 2026-11-14. The final selected source gate has **187 passing cases per
unit policy**, normal and pm/fs, including **29 new contact cases**, plus the
original declaration/record/argument/bootstrap controls. Authored 32-atom/three-
structure geometry has independently expected pairs `[[8,10],[2,30]]`, distances
`[1,0.5] nm`, source footprints `[2,8]`/`[10,30]` and group witnesses `[0,1]`. A separate four-group control proves that reordered
atom endpoints retain the actual distinct group axis and pair witnesses.
Actual owner extraction/permutation gives aligned local footprints `[1,0]`/`[3,2]`
and original structure 2/local 0. Exchanged sides, empty requests versus evaluated
zero, missing group membership, required-child allocation failure and source edits
have their own observed controls. Existing failures under #113 remain separate.

Six actual native result/positive-empty footprint records are read in another
process under pm/fs with public molecular operations forbidden and TopoMT/PISA/
Vina unavailable. Required core imports may load MolSysMT's native module; import
is not a numerical operation. The initial harness incorrectly forbade that import
and is retained as a failed attempt. The initial reader consistency failure,
NumPy-scalar JSON correction, two unsupported nullable-setter fixture attempts and
corrected independent witness/harness attempts remain preserved, not relabelled.

Actual local molecular source is `ff25f120243319ca9515009b4971e24a2eb0dc22`;
loaded Linux native SHA-256 is
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`.
This is the historical local native file, distinct from the owner handoff's
`4ffb82e4` reference. Its builder/source identity is not newly authenticated.
The controls establish bounded operation compatibility for these actual bytes,
not a new build, broad ABI/native-source qualification or provider acceptance.
Reported package versions accompany the task's exact source/file/native snapshots;
they do not replace source identity in an editable installation.

Cells remain CPU-one/nice 10, native workers one, 13 GiB available reserve,
512 MiB owned-group cap; source/provider identities are checked around final
receiving. No resource interruption or shared-prefix change is implied by a test
pass. Applicable final Ruff/format/index/proposal/resource/Conda checks run in the
workspace and a fresh committed export. No new installed/public package, hosted
matrix, native rebuild, large-system performance or whole scientific gate is claimed.

## Provider feedback and next work

[MolSysMT #739](https://github.com/uibcdf/molsysmt/issues/739) records the independent
public group-setter dtype defect: selected `group_index=[None]` succeeds on a fresh
native column, then fails after an ordinary full integer assignment. Current
owner source was checked for the same setter body. No local molecular-editing
workaround is added. The missing-group test instead constructs a native MolSys
with an initially unknown inventory through the provider's constructor.

N2 is next: close the surface-specific radius/H/environment/probe/sampling and
numerical contracts, then compose the actual MolSysMT SASA operations. T0/T1,
H/P inputs/adoption, #111 and #30/#195 keep their own gates. This bounded native
source profile closes neither #112 nor consumer-wide/public acceptance.

The source/Conda/live test manifests now require PyUnitWizard >=0.29.3, the
reviewed public sealed-quantity/cutoff/origin baseline also pinned by the 0.1.0
source context. Its `record.py` at source `c81916e` exposes the exact field/unit/
dimension/form handshake used here; the current native tests use cc51c8e. This
is a selected compatibility floor, not a claim that QuantityRecord originated in
0.29.3. Original E4 0.29.0 manifests/receipts remain at their original producer
commits; the live bootstrap adjustment does not rerun or relabel that science.
No dependency is installed or shared-prefix metadata rewritten by this increment.
