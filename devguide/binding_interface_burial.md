# Native SASA and interface burial: first N2 admission

Owner: BindingMT #112. Molecular tools: MolSysMT #734. Shared receiving: #195.
Recorded 2026-11-12 before implementation. Status: **bounded N2 source profile implemented and received; broader/installed adoption pending**.

## Public and scientific contract

`calculate_interface_burial(molecular_system, *, participants, structure_index,
source_id, probe_radius, n_sphere_points, hydrogen_policy, atom_map=None,
source_structure_index=None, max_surface_evaluations=20000000)` returns immutable
`BindingInterface`. Two nonempty unique disjoint selections name participants.
The input is a native MolSys with one explicitly chosen whole Cartesian structure,
chemistry/state/H representation admitted by the caller and stable for the call.
`hydrogen_policy='as_supplied'` is the only first policy; no H is added/removed.
No inter-side covalent links or implicitly cut required participant chemistry are
admitted. Radii are the native bundled element-vdW model, not force-field/ProtOr
radii; unknown/nonpositive/nonfinite selected radii refuse before SASA.

Probe length and sampling density are explicit choices, without application
scientific defaults. PBC/alignment/relaxation/preparation and additional environment
atoms remain unsupported. No contact result is needed. The environment is exactly
the selected A union B; reporting selection never silently removes occluders.

For identical supplied coordinates, element/radius/H model and sample directions,
calculate three independent owner-extracted contexts: A, B and A union B. Invoke
`msm.physchem.get_sasa` on each, engine MolSysMT, all atoms, local structure 0,
pbc=False, use_gpu=False, use_cell_list=False, parallel=False, num_threads=1.
BindingMT composes both atomic losses, side sums, total and explicit mean-side area:

```text
L_A = SASA_A(A) - SASA_A(A union B)
L_B = SASA_B(B) - SASA_B(A union B)
total = sum(L_A) + sum(L_B)
mean_side = total / 2
```

Never double one side or substitute MolSysMT's tabulated residue descriptors.
No surface, neighbor or sampling kernel/radius table is implemented locally.
Atom-to-group contributions use actual owner group correspondence and retain
atomic witnesses; missing group identities preserve partial coverage, not zero.

## Context and quantity proof

All form/selection/state/coordinate/atom-type/group/radius inspection, extraction
and map normalization use public MolSysMT operations. Native extraction retains
sorted source atoms and source structure s becomes local 0. Record those actual
operation maps; optional upstream maps retain the same explicit original-axis
preconditions as the contact profile. Reject unmapped/generated identities when
that requested original-source projection cannot be established.

Use `msm.compare` for admitted molecular comparisons, require the requested keys,
and retain exact selected-coordinate fingerprints plus actual type/state/radius
checks for source/subsystem and isolated/combined baselines. This verifies model-
relevant transport, not chemical validity or authentication of foreign assets.
Other chemical interpretation remains caller-admitted; no generic molecular
observer or chemistry repair is introduced. Check the original input again after
all children and preserve earlier results on failure or later edits.

Experimental result format 0.3 carries one composed surface-result reference,
independent of whether its burial is zero. Such a result is not a positive
interface finding. 0.1 declaration/0.2 contact records remain readable. Store
probe/radii as sealed length records and areas/signed losses as sealed area
records; receivers require exact field, unit nm/nm**2 and [L]/[L]**2. Reads invoke
no scientific operation, asset lookup or active context reassessment. Positive-
area membership/footprints are not selected by this profile.

## Numerical and resource limits

Raw losses remain signed. Classify negative values as within binary64 roundoff
or inconsistent using an explicit relative bound of 32 epsilons against the
isolated atom area, with zero absolute bound. Preserve every raw value/status;
never clamp. A result with an inconsistent negative is numerically unusable for
burial while its completed child observations remain inspectable. This bound is
not a sampling-error estimate, physical uncertainty or membership criterion.

Independent two-sphere controls use analytically specified radii/geometry and a
predeclared eight-maximum-sphere-patches error budget per side at each density.
Check multiple densities/rotations without asserting monotonic convergence or
exact rotation invariance. Molecular-radius resources and Fibonacci sampler code
retain owning version/content fingerprints and reached implementation/method
attribution. The native implementation is Shrake-Rupley, not execution of another
reference program. Primary method DOI: 10.1016/0022-2836(73)90011-9.

Admit `(n_A**2+n_B**2+(n_A+n_B)**2)*n_sphere_points` <= the explicit work budget
before extraction/SASA. Record sphere/input/result estimates separately; this is
not reserved RAM, elapsed-time prediction or total RSS. The first route is serial
brute-force CPU, without hidden cell/GPU fallback. Task cells use CPU-one/nice 10,
native/build workers one, 13 GiB available reserve, 512 MiB owned-group cap.
No shared-prefix installation/native rebuild or held scientific-suite restart.

## Required receiving

Tiny authored systems exercise analytic isolated/paired C and C/H spheres,
separation/containment, unequal side losses, atomic/group sums, unrelated occluders,
reordering/source structure maps, same-source/radius/geometry preservation,
missing radii, invalid/work-budget refusal, actual required-child failures and
raw negative-status controls. Test normal/pm-fs and alternate user quantity form,
public save/read in an independent process with molecular calls forbidden and
optional scientific providers absent. Retain original failed attempts and exact
source/native/software identities. Report concrete owner defects in MolSysMT;
no downstream molecular workaround is authorized. #112/#30/#195 and T/H/P scopes
remain separate from this bounded source increment.

## Delivered ordinary and expert workflow

```python
import bindingmt as bmt

result = bmt.calculate_interface_burial(
    system,  # an admitted native MolSys, stable throughout the call
    participants={'A': 'chain_index==0', 'B': 'chain_index==1'},
    structure_index=0, source_id='my-admitted-source',
    probe_radius='0.14 nm', n_sphere_points=960,
    hydrogen_policy='as_supplied',
)
print(result.burial_areas)  # quantities: sides, total, mean_side
print(result.summary()['native_surface'])
result.save('burial.json')
restored = bmt.BindingInterface.read('burial.json', experimental=True)
evidence = restored.surface_calculation  # detached typed areas, axes and provenance
```

The probe/density in the example are caller choices, not defaults or universally
converged settings. `burial_areas` returns signed quantities in nm**2 using the
application's active quantity form without altering its policy. `surface_calculation`
retains raw isolated/combined areas, signed atomic/side losses, actual group-axis
witnesses and coverage, projections, operation options, model resource hashes and
attribution. Group membership names the input MolSys group axis, not a fabricated
original-source group map. Missing groups retain partial coverage and all atoms.
A successful surface analysis has one surface-result reference even for zero area;
`result_count=1` is not a positive interface finding. `contact_calculation` is None,
contact projections refuse and no area-membership/footprint threshold is inferred.
Inconsistent negative losses retain completed child observations but set
`burial_usable=False`; consumers must inspect that status before using burial.
Copy/read preserve identity and reinterpretation preserves original scope.
The first 0.3 profile admits one surface analysis; automatic contact/surface
bundling is not implemented. Data 0.1 and contact 0.2 records remain readable.

## Exact source receiving and limits — 2026-11-12

Focused source selection (serial, `--receptor=llm`) passes **238 cases per policy**,
normal and pm/fs: **51 burial controls**, 29 contact controls and the existing
158 declaration/result/outcome/core/bootstrap controls. The 18 independent
spherical-cap cases cover C/C and unequal C/H radii, densities 240/960/3840 and
three rotations. The fixed analytic radius anchors are C 0.170 nm and H 0.110 nm,
with explicit 0.140-nm probe. Sampling tolerances follow the declared patch budget,
not a fit to observed errors or physical uncertainty. Other tests exercise exact
separated zero/containment, group witnesses, reversed sides, reordered/source
structure maps, unknown radii, before-execution refusal and real required-child
failures. Two deliberately injected negative observations are **software adversity
controls**, not physical/sampling evidence. The first failed test attempts
(missing local atom-query level and a wrongly addressed tamper fixture field)
remain preserved; neither was a provider defect or resource interruption.

Actual public positive and zero results pass save/read in a fresh process under
unyt/pm-fs with molecular inspection/calculation forbidden and optional providers
unavailable. Reads leave source files and policy unchanged. Applicable final
Ruff/format/report-index/proposal/shared-resource/Conda checks run in the workspace
and a fresh committed export. No frozen scientific helper/input changed; existing
installed-support declarations retain their exact original SHA-256 values.

The molecular checkout is clean `ff25f120243319ca9515009b4971e24a2eb0dc22`.
Actual loaded `_rust.abi3.so` SHA-256 is
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`.
Its historical builder/source identity remains unauthenticated; it is not the
different owner-reference SHA `4ffb82e4`. Other clean editable providers are
PyUnitWizard `cc51c8e`, ArgDigest `7be790b`, SMonitor `4a4cd1e`, DepDigest `5e93eaf`.
Package versions in results complement these exact receiving identities. This
source pass establishes only the actual bounded operations/bytes tested; no
new native rebuild, installed/public artifact, full Python/platform matrix,
large-source performance, arbitrary chemistry or complete scientific gate is claimed.

Exact source/test hashes before/after each final cell, imported environment and
native identities, raw test reports, actual serialized records/fresh reader,
resource outcomes and final workspace/export receipts retain #50 custody under
`.molsyssuite/interface-sasa-burial-112-20261112/`, review 2026-11-14.
Cells use one CPU/nice 10, native workers one and a monitored 13-GiB available
reserve; the estimate/budget is not a reservation. Original shared-prefix/full-suite
holds, original producer records and the 0.1.0 source tag remain unchanged.

No missing public MolSysMT operation was found in this admitted composition.
The earlier independent nullable group-setter defect remains owned by
[MolSysMT #739](https://github.com/uibcdf/molsysmt/issues/739); no downstream
molecular-editing workaround is added. Any newly discovered provider limitation
must be reported with consumer evidence in MolSysMT, cross-linked to #112.

Next execute the separately admitted T0/T1 PISA intake/persistence/refusal branch;
receive exact H/P inputs and record shared native-contract disposition under
MolSysSuite #195. Those obligations, #111 and #30 keep their own owners/evidence.
This finite N2 source milestone leaves #112 open and implements no environment-
aware, energetic, ensemble or predictive profile.
