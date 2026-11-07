# E1 declared-source preparation receiving — 2026-11-06

Owner: [DockingMT #78](https://github.com/uibcdf/dockingmt/issues/78).
Status at prescription: **prospective**. The
[notebook](e1_prepared_authority.ipynb) receives preparation of the
[new declared authority](e1_declared_authority_2026-11-06.md). It uses the selected
editable development composition, not public or ordinary-installed artifacts.

## Inputs and declared population

Verify the normal-policy source H5MSM compressed SHA-256
`b518b813738fe5e9e5d72817858359d0320e321ce425fcf04af0354a10d16575`
and decoded SHA-256
`fd01a684d624e8abaa19ee6d16d62ab0b84927c3abd74d5bbd5dcc3881c712b7`.
Decompression is transport; loading uses public MolSysMT conversion.

Run two serial unit policies: nm/ps/elementary charge and pm/fs/coulomb. For each,
materialize nine stored H once with fixed chemical state, explicit RDKit,
`pH=None`, strict attribute preservation and no optimization. Keep the complete
hydrogen report, generated IDs, parent pairs and original-coordinate checks.
Generate one named Gasteiger–Marsili charge assignment and one named AutoDock4
chemical-environment typing on the resulting eighteen-atom system. These are
new calculations from the newly declared source, not restored historical values.

Prepare two arms from the same typed eighteen-atom model, without repeating the
H/charge/type stages: rigid, and flexible with the explicit source-axis cut
`(0, 6)`. Both have the same declared chemical-state label. Receive the actual
provider reduction reports: five nonpolar H merged into their parents, four
polar H retained, thirteen atoms, conserved total charge +1 within `1e-6 e`.
Also check the stricter conservation tolerance reported by the provider.
Charge-audit consistency does not establish physical validity; public preparation
assessment remains unassessed. Generated H have local geometry, without
environmental optimization or experimental coordinate attribution.

## Projection, maps and controls

The finite rigid tree contains all thirteen atoms in source order. The finite
flexible tree declares root atoms 6–12, child atoms 0–5, branch `(6, 0)`, and one
torsional degree of freedom. Check this declaration against the actual public
prepared traversal and provider writer. This is a specified case, not a local
graph-rooting/remapping implementation.

Keep independent public-native and DockingMT PDBQT exports. Only the actual
native export receives its public atom map; its hash must not be reassigned to
DockingMT text with different remarks. Interpret both through MolSysMT and
compare written coordinates, labels, elements, charges, types and torsion trees.
Keep the parsed trees before explicitly discarding them for native conversion.
Check coordinate rounding within `0.0000500001 nm` per component and charge
rounding within `0.000500001 e` per atom. The rounded charge sum has a separate
thirteen-atom bound of `0.0065 e`; do not impose the unrounded `1e-6 e` tolerance.
Compose the actual H-generation, reduction and export maps through the public
provider. Four retained generated H must have no fabricated pre-generation index.

Read each native export through public `read_poses`, bound to its actual map
and complete thirteen-atom chemical source. Receive chemical graph witnesses
and rounded coordinates on the source axis. The pose reader explicitly does
not transfer MolecularMechanics. Do not reattach or recalculate assignments to
make it appear otherwise. The flexible export supplies the nonidentity written
axis. No historical H map is attempted, and historical heavy-coordinate poses
are not transplanted into a new thirteen-atom model leaving H stale.

Per policy, expect five supplied-map chemical witnesses: two chemical-only
H5MSM roundtrips, two mapped PDBQT readings, and rigid/flexible chemical equality.
Every identity call has one supplied complete candidate and `max_matches=1`.
Four adverse exports per policy must refuse missing charges, missing types,
an old tree after atom-axis permutation, and nonfinite geometry. A separate
per-policy edited-prepared-charge audit must be inconsistent. Use detached
copies; preserve full diagnostics. An unexpected result stops the population.

## Persistence and nonmutation

H5MSM 0.5 and MolSysDict 0.2 do not persist nonempty MolecularMechanics. Compose
explicit chemical-only systems from public topology/chemical-state/structure
domains, preserve frame/state association, and label every saved H5MSM accordingly.
Keep full-precision coordinate/charge quantity records, types, prepared metadata,
both named assignment reports, original reduction/generation/export/read maps,
and native mechanics inspection separately. Native `MM.to_dict()` omits named
assignment reports; retain them explicitly. These inspection records are not a
new codec or a qualified complete mechanical-model replay route.

Check before/after snapshots of source9, expanded18, charged18, typed18 and each
native13 for the listed chemical payload, mechanics values/reports, coordinates,
IDs/names/elements and frame/state link. Check caller unit-policy restoration
and exact cross-policy PDBQT bytes. These checks enumerate their scope rather
than certifying every possible native field.

## Execution budget and custody

Register exact notebook/cell/input identities and this prospective prescription
before executing plain Python cells in a fresh isolated process. One allowed
logical CPU, nice 10, one native/build worker; available-RAM reserve **8 GiB**,
task RSS **1 GiB**, address space **2 GiB**, CPU **60 s**, wall **90 s**. Admit RAM
before launch and monitor it every 0.1 s. Stop only owned work on resource
threats, preserve interruptions and do not automatically retry them.

Direct-call caps are convert 80, get 340, copy 12, set 16, permutation 2,
H expansion 2, charge assignment 2, typing 2, preparation 4, H inventory 8,
correspondence 10, map composition 4, pose reading 4 and tree reading 8. Counters
cover selected direct calls, not constructors, methods, provider internals or
other aliases. Keep all cell events, partial outputs, diagnostics and resource
records. A correction requires a distinct registration/code identity. Custody
review under #78/#50: **2026-11-13**.

This population has one newly declared chemical state and two unit repetitions.
It admits no historical prepared13 identity, historical H correspondence, energy
comparison, native Vina execution, public artifact, full E1 acceptance or E4
restart. Comparison/reference admission and representative rescoring remain
separate next work.

## Amendment before attempt 02

Attempt 01, notebook SHA-256
`ec709fd82e05d45922f2929cf3410d38142cfe52325582270ad8cd140063e1cb`,
completed the normal profile and stopped during the pm/fs rigid arm. Its exact
array-equality assertion compared native13 coordinates against retained typed18
coordinates after public unit conversions; 21 of 39 components differed, with
maximum absolute difference `2.220446049250313e-16 nm`. The attempt's exception,
counts, completed profile, partial outputs and original prescription remain
separate evidence. It was an assertion failure, not a resource interruption.

The corrected attempt uses `rtol=0, atol=1e-12 nm` for that conservation check.
This is numerical tolerance for public unit conversions, not a geometry-quality
or experimental-equivalence criterion. Original molecular inputs and preparation
choices are unchanged. Reregister the corrected notebook and repeat both unit
policies and all controls from a fresh process; do not splice attempt-01 results
into the new population. Both attempts retain their actual scientific-call counts.

## Executed development receiving

Attempt 02 completes all four registered plain Python cells in **9.55 s**.
Its [registration](data/e1_prepared_authority_2026-11-06/registration.json) binds
notebook SHA-256
`31993b57ad1377ba7605dd17d5e769686289ea7c183be8d57a8350294c1d5972`.
The [frozen prescription](data/e1_prepared_authority_2026-11-06/registered_prescription.md)
includes the amendment before execution. This is cell execution in a fresh
isolated Python process, not a received Jupyter frontend/kernel session.

| Receiving | Outcome in the complete attempt |
| --- | --- |
| H expansion and named assignments | Two expansions 9→18, two Gasteiger–Marsili assignments and two AutoDock4 chemical-environment assignments; one of each per unit policy. No original atom coordinate, label or element changes within the checked scope. |
| Prepared arms | Four successful 18→13 preparations; each merges five nonpolar H, retains four polar H, and preserves the provider's charge-conservation tolerance. Rigid TORSDOF 0 and flexible TORSDOF 1. |
| Full-precision and written charge | Each prepared total is `1.0000000000000004 e`; its PDBQT total is `1.0010000000000001 e`. The rounding difference is within the `0.0065 e` bound, independently of the full-precision tolerance. |
| Molecular witnesses | Ten positive supplied-map witnesses: four chemical-only H5MSM roundtrips, four mapped PDBQT readings and two rigid/flexible comparisons. Each uses one supplied candidate. |
| Written axes | Rigid order 0–12; flexible order `[6,7,8,9,10,11,12,0,1,2,3,4,5]`. Actual public map hashes bind only their own native export bytes. |
| Generation lineage | Composed maps retain four generated polar H with source9 index `-1`. They receive no historical H identity or invented pre-generation coordinates. |
| Adverse receiving | Eight expected export refusals and two inconsistent edited-prepared-charge audits. All checked reference snapshots remain unchanged after the adverse operations. |
| Unit policies | Full-precision typed18 coordinates/charges agree within `1e-12` in explicit nm/e units; types agree exactly. All corresponding native and DockingMT PDBQT files are byte-identical between policies; caller policy is restored. |
| Resources | One CPU, nice 10, one native/build worker, sampled peak RSS **311.63 MiB**, minimum available RAM **48.41 GiB**; no resource interruption. |

The [receipt](data/e1_prepared_authority_2026-11-06/receipt.json.gz) records the actual
development composition and original loaded native-module identity. Direct
counts are convert 72, get 314, copy 6, set 12, permutation 2, H expansion 2,
charges 2, typing 2, preparation 4, inventories 8, correspondences 10, map
composition 4, pose reading 4 and tree reading 8. All remain within registered
caps. The Rust binary's source/build correspondence stays unassessed.

The [manifest](data/e1_prepared_authority_2026-11-06/manifest.json) binds original
reports, values, chemical-only H5MSM files, PDBQT bytes/maps, diagnostics,
resources and both attempts' code/prescriptions. Gzip is transport only: verify
compressed and decoded identities before restoring the original filename.
The [attempt ledger](data/e1_prepared_authority_2026-11-06/attempts.json) preserves
attempt 01's 12.75-second assertion failure, one completed policy and partial
pm/fs outputs. Across both attempts the actual direct work includes four H
expansions, four charge assignments, four typings and seven preparations;
those repetitions are not additional independent chemical cases or a pooled
success population.

The new authority now has bounded prepared-state and flexible/nonidentity export
receiving. MolecularMechanics remains available in the running native objects
and in separate inspection evidence, without a qualified complete persistent
replay contract. Pose reading retains complete source chemistry and the listed
rounded fields; it does not carry mechanical assignments into the read model.
No energy call ran. Next define comparison/reference admission and the policy
for constructing each future complete thirteen-atom pose before registering
rescoring. The historical prepared13 identity, strict `rank_by` context rules,
original input hashes and local E4 hold remain intact.
