# BindingSite elementary geometry declaration profile

Owner: BindingMT #111. Admission: 2026-11-13 before implementation.
Status: implemented and source-received B1/B2 static geometry profile.

## Public scope and local decisions

Add `BindingSite.from_sphere(source=..., center=..., radius=..., frame=...)` and
`from_box(source=..., center=..., lengths=..., frame=..., axes=None)`. Retain
name, declared structure/state scope, optional extensions and immutable evidence/
definition operations. Molecular resolution, atom inclusion and domain placement
keep their C1/C2 gates; this increment implements no application stub or molecular
coordinate capture. Geometry belongs to the site, not to a second trajectory.

Require finite explicit length quantities: center shape `(3,)`, radius positive
scalar and full box edge lengths positive shape `(3,)`. Writer normalization is
canonical nm through the existing shared length boundary and PyUnitWizard.
Use sealed QuantityRecord fields `bindingmt.site.geometry.center`, `.radius`
and `.lengths`; readers handshake field/unit/dimensionality and shape rather
than infer current units. The ordinary `geometry` property returns detached
quantities in nm using the caller's active quantity form.

Frame is an explicit descriptor with nonempty `id`,
`coordinate_policy="cartesian"` and `pbc=False`. It is a caller-declared Cartesian
single-image association, not proof that a target shares the frame/source.
No PBC wrapping, assembly generation, alignment or transform is performed.
An unspecified molecular-structure scope means a frame-defined declaration,
not applicability/evaluation over every conformation. Admit at most one selected
source-structure occurrence for a saved geometry. Evidence retains its separate
scope. A geometry series/ensemble needs another profile.

Boxes preserve orientation. Default axes are the identity; optional axes are
three right-handed orthonormal local basis vectors expressed as rows in the
declared frame. Accept only fully known real numeric 3x3 arrays/lists/tuples,
without unitful inputs or arbitrary object coercion. Validate orthonormality and
determinant +1 with zero relative and 1e-6 absolute dimensionless tolerance,
preserving the supplied values without repair. Seal axes as a dimensionless
QuantityRecord with field `bindingmt.site.geometry.box_axes` and owned kind
`urn:bindingmt:site:box-axes`. This is an orientation declaration, not an angular
quantity or a molecular transform. An oriented box is not silently converted to
an axis-aligned BoxRegion.

## Experimental wire and capabilities

Geometry emits **BindingSite 0.3**, admitting exactly one sphere/box view named
`geometry`, role `declared_geometry`. Existing 0.1 residue/criterion and 0.2
atom/group factories/records stay unchanged and readable. Old readers must
refuse 0.3. No silent migration or proposed shared `@1` freeze occurs; the
package/source tag remains 0.1.0.

Inspection reports declared geometry and frame separately from molecular
membership, which remains not supplied. Molecular resolution/placement stay
unperformed, realization coverage not requested and binding support unknown.
The geometry property is None for nongeometric profiles. Derivations retain
the original format, geometry, exact claim references and observations.

## Checks and limits

Exercise equivalent explicit units, nm/pm-fs and unyt policy preservation,
signed centers, positive extents, shape/dtype/dimension/field/quantity-seal
refusals, immutable values/axes, orientation, frame/PBC, single-source occurrence,
old-version reading/refusal and actual public save/read/revision. Cold reading
must use no molecular/optional engine operation or new originating credit.
Frozen original records/producers remain intact; new compatibility inputs have
exact installed-test support hashes. No docking/native build/prefix change or
held evaluator restart is commissioned.

The reused length helper and saved-box reader now preserve original OS/resource
exception identity under [BindingMT #115](archive/length_quantity_oserror.md),
while retaining malformed physical-input diagnostics. Both authored probes
observed the former ArgumentError wrapping. This is a local reusable-boundary
correction, not a provider defect or actual system memory-pressure event.

The finite [MolSysMT #746 offer is reviewed](binding_site_molecular_contract_receiving.md);
the finite owner facts are now client-received; actual public C1 projection remains pending.
Offline physical declaration alone supplies no placed-geometry/current-finding
assurance. C2 must preserve derivation and verify the actual consumed problem
input before its public application can be received. Shared/consumer/installed/
public/platform/hosted evidence remains separate from this source increment.

## Ordinary and expert use

```python
import bindingmt as bmt

source = {'owner': 'local.study', 'id': 'system-A', 'revision': '1'}
frame = {'id': 'source-cartesian-frame', 'coordinate_policy': 'cartesian', 'pbc': False}
site = bmt.BindingSite.from_sphere(
    source=source, center='[-1, 2, 3] nm', radius='5 angstrom', frame=frame,
    structure_indices=[2],
)
geometry = site.geometry  # Detached quantities, explicit frame and geometry kind.
print(site.describe())
record = site.to_dict()
restored = bmt.BindingSite.from_dict(record, experimental=True)
assert restored.record_id == site.record_id
```

`from_box` takes `lengths='[2, 4, 6] nm'` instead of radius. Its optional `axes`
preserves orientation; inspect the row-basis convention in `geometry`. File IO
uses the existing exclusive `site.save(path)` and
`BindingSite.read(path, experimental=True)`. None of these declarations computes
atom inclusion or proves that source structure 2 has the declared frame.

## Actual receiving — 2026-11-13

On BindingMT base `e1e6a337dbf487d1b2e36809cc72ea46a7639f60` plus this
increment, **473 complete selected cases pass per policy**, normal and pm/fs:
436 core/record/helper cases and 37 argument/bootstrap cases. The selection
includes **72 new geometry controls and two new saved-box OS-error controls**;
78 existing box-admission cases were newly included, not newly authored. Final
cells are `final-core-normal-02`, `final-core-pm-fs-01` and the two
`final-arguments-*-01` cells. Earlier 71/434-pass attempts precede the final
selection and are preserved separately.

A real public workflow saves five new geometry records and reuses three actual
old records; sorted derivatives bring the total to **16 files**. A fresh
unyt/pm-fs reader preserves physical quantities, orientation, exact original
claim references and old 0.1/0.2 identities. It performs zero molecular calls,
optional engine imports or originating uses, preserves policy and leaves inputs
unchanged. The actual archived e1e6a33 decoder refuses both new sphere/box 0.3
files before molecular work. Its temporary export is retired; the existing
generated version module is separately hashed metadata context, not a new build.

Five compatibility inputs under `tests/data/site_geometry_compat/e1e6a33/` retain
original 0.2 bytes, producer identities, production-base versus qualified-source
identities and exact installed-test support hashes. Earlier scientific fixtures
and measurements are unchanged. The existing PyUnitWizard floor >=0.29.3 covers
the consumed public field/kind handshake; no new provider floor is inferred from
the development checkout.

Executed source closure: MolSysMT `ff25f120243319ca9515009b4971e24a2eb0dc22`,
PyUnitWizard `cc51c8e600f78f108bc563edd3221bd8788ead86`, ArgDigest
`7be790b7334e16715fceebbfa8a2b400edf768bb`, SMonitor
`4a4cd1e415ea57e50c22925c36c2e727772fb3ab` and DepDigest
`5e93eaff314fe7cddf4eee89842977023b3a8b00`. Each selected cell retains before/after
runtime/test/support/resource hashes. The historical MolSysMT binary's on-disk
SHA-256 is `2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`;
its build/source provenance remains unauthenticated. No new native operation is
qualified here, and concurrent PharmacophoreMT work is not imported.

All cells run serially on CPU 0 at nice 10, one native worker, 512 MiB group RSS
cap, 2 GiB address space, 45 CPU seconds/120 wall seconds and a monitored 13 GiB
available-memory reserve. Peak selected-test RSS is below 270 MiB; no resource
interruption occurs. #30's earlier evaluator hold remains untouched. Exact raw
attempts, source hashes, gates, frozen inputs and publication/committed-export
receipts retain #50 custody in `.molsyssuite/site-geometry-111-20261113/`, review
2026-11-14. Applicable workspace and fresh committed-export checks cover Ruff,
formatting, report indexes, documentation links/sketches, shared resources and
the Conda contract; exact public commit/readback is recorded in #111/#30. This
is source-profile evidence, not hosted CI, installed/public delivery, platform
qualification or executed consumer adoption.

M1's admitted static/single-view data profiles are now source-received: six
factories, detached inspection, immutable revision and versioned persistence.
Broader multi-view/ensemble operations and C1/C2/T/H/P/shared acceptance remain
pending. Next receive #746's finite owner disposition and settle the admitted
C2 offline derivation/assurance profile separately from molecular placement.

## Subsequent internal C2 checkpoint — 2026-11-13

The [offline domain-geometry increment](binding_site_domain_geometry.md) now
implements the separate geometric substep, retaining this profile's exact site/
claim/quantity references in a locally versioned recipe. Backend export remains
unavailable while placement is unassessed; no public application stub is added.
Its distinct 557-case-per-policy receiving and saved/old-reader controls do not
rewrite the original 473-case population above or complete C1/public C2/M2.

## Molecular-offer review and resource correction — 2026-11-14

[The finite owner offer](binding_site_molecular_contract_receiving.md) is reviewed;
[normalization #116](archive/molecular_input_os_resource_error.md) is source-corrected
with its own 500-case software receiving and explicit broader native resource
interruption. These do not change the original geometry populations, supply
molecular placement or complete public C2/M2. Next qualify the actual client
source/native profile and implement its real region result.
