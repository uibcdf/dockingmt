# E1 complete-pose construction and comparison admission — 2026-11-06

Owner: [BindingMT #78](https://github.com/uibcdf/bindingmt/issues/78).
This case-specific prescription follows [prepared-authority receiving](e1_prepared_authority_2026-11-06.md).
The [notebook](e1_complete_pose_receiving.ipynb) constructs a new five-pose
population and stages comparison evidence. Status at prescription: **prospective**.
It performs no native scoring, search, optimization or numerical ordering.

## Complete-pose recipe

Use the frozen new declared nine-heavy-atom authority, not the legacy snapshot.
The five heavy-coordinate sets and their historical pose/score associations
are already received in the [authority evidence](data/e1_declared_authority_2026-11-06/normal/observations.json).
Verify input digests and the actual coordinate unit before any molecular work.
For each set, independently copy the authority and set all nine coordinates
through MolSysMT. Materialize all nine missing H on that pose with public
fixed-state RDKit, `pH=None`, strict preservation, and no optimization. All H
coordinates are newly generated local geometry; no historical H is matched or
copied. Do not transplant only nine coordinates into an existing thirteen-atom
model, and do not leave old H coordinates attached to a changed heavy pose.

Assign Gasteiger–Marsili charges and AutoDock4 chemical-environment types once
to each new eighteen-atom model. Prepare one flexible thirteen-atom view with
the explicit source-axis cut `(0,6)`. Preserve the actual H-generation,
reduction, named-assignment and export reports. Independently receive each
eighteen- and thirteen-atom graph against the first newly prepared graph of
its own representation through one supplied identity candidate and
`max_matches=1`. Those witnesses concern the new recipe, not historical H identity.
Check full-precision charge/type equivalence separately from chemical witnesses.

Run all five variants serially under nm/ps/e and pm/fs/coulomb policies:
**ten** H expansions, ten charge assignments, ten typings and ten preparations.
The unit repetitions are not independent molecular complexes. Keep original
pose IDs/scores as historical associations and give every new pose its own
producer/input identities. The explicit flexible tree differs from the original
rigid input; this is a new scoring population, not an exact historical replay.

For every variant, keep independent public-native and BindingMT PDBQT bytes,
actual native export map/hash, composed source9 lineage and written tree.
Check native/BindingMT fields through MolSysMT, then read the native export with
its complete chemical source and its own map. Expect thirty positive witnesses:
ten full18, ten prepared13 and ten mapped-read13. The pose reader does not
transfer MolecularMechanics. H5MSM files explicitly contain only chemical and
structural domains; full-precision values/reports remain inspection evidence.
No complete MM persistence/replay contract is introduced.

Coordinate conservation uses `rtol=0, atol=1e-12 nm`, PDBQT per-component
rounding `0.0000500001 nm`; charge equivalence uses `1e-12 e`, named total +1
within `1e-6 e`, and reduction uses its actual provider conservation tolerance.
Written per-atom error is bounded by `0.000500001 e`, with the writer's separate
sum-rounding bound. Check original labels/IDs/elements and coordinates, missing
H counts, generated parent maps, and all retained source snapshots. Require
exact corresponding PDBQT bytes between unit policies and distinct hashes for
the five normal-policy complete poses. The earlier negative export/charge
controls are not rerun by this population.

## Fixed receptor and prospective backend contract

Stage the exact original captured receptor PDBQT from the frozen human 3PTB
result; verify SHA-256
`edeff77e6222c5c5ab1aa6be2354efc323c0ffe8a7884366069ee0addbf7b970`.
This supplied receptor has partial PDBQT chemistry and unassessed preparation.
Using the same bytes establishes a fixed software-model input, not complete
receptor chemical identity or physical validity. Preserve its original producer
and state declaration separately. Do not repair or regenerate the receptor.

Attempt 01 used the captured backend box: center
`[-1.759111,14.461,16.915778] angstrom`, size `[20,20,20] angstrom`.
The separately registered corrected population uses the same center and one
common requested size `[24,24,24] angstrom`, as the amendment below specifies.
Future native admission must verify all submitted ligand atoms lie inside that domain;
this receiving checks its staged coordinates conservatively against the bounds.
The staged contract has separate Vina and Vinardo evaluations, CPU 1 and seed 7.
Expected Vina 1.2.7 factory weights, spacing `0.375 angstrom`,
`force_even_voxels=False` and `no_refine=False` come from inspected source.
They are prospective expectations, not observations from an executed backend.
Before scoring, bind the actual installed Python/native artifact identities,
version, engine-reported weights/grid and submitted input captures. A changed
version/default is a new admission question, not an implicit fallback.

## Comparison matrix

| Pair/question | Admission and required evidence |
| --- | --- |
| New poses, same method and component | Eligible for a separately registered component study only after the complete recipe, graphs, mechanics, torsion/tree, fixed receptor/frame, box, weights, grid/refinement policy and actual backend artifacts all pass. Preparation is still unassessed physically. |
| `lig_inter` within one native method | A possible future receptor-interaction comparison. It does not use the unbound reference subtraction, but still requires the full common-model evidence above. No preferred direction or new ranking descriptor is inferred here. |
| Fixed-score totals with current-conformation references | Retain every native component and reference observation. They answer the fixed-score convention, not a common-unbound-energy or docking-order question. No shared reference is invented from equal rounded values. |
| Historical docking versus new fixed scoring | Keep separate: historical H/producer, rigid/flexible tree and energy-reference conventions differ. No pooled total, difference presented as reproduced historical score, or recovery claim. |
| Vina versus Vinardo | Separate methods, weights and scales. No pooled numeric ordering or cross-method subtraction. |
| Unknown graph, mechanics, state, receptor, units or backend setting | Unassessed/pending; a matching label or isolated numeric value does not supply missing evidence. Explicit contradictions refuse that comparison. |
| Current public `rank_by` on new per-pose fixed scores | Expected refusal for different actual partner hashes in described contexts. Keep those hashes/descriptors and all histories. Do not remove fields, relabel contexts, synthesize legacy records or weaken the existing API. |

The [Python API](https://github.com/forlilab/AutoDock-Vina/blob/v1.2.7/build/python/vina/vina.py#L407)
rounds returned values to three decimals and calls native `score()` when no
unbound value is supplied. The [native fixed-score route](https://github.com/forlilab/AutoDock-Vina/blob/v1.2.7/src/lib/vina.cpp#L690)
computes the current system's intramolecular reference; search uses the best
searched pose's reference. The [intramolecular implementation](https://github.com/forlilab/AutoDock-Vina/blob/v1.2.7/src/lib/model.cpp#L856)
and source identities are retained by the inspection receipt. These are source
findings, not a new native experiment. Component interpretation is bounded to
the inspected version and rigid-receptor setup.

The existing descriptor context includes each actual partner SHA-256, receptor
SHA-256, box, weights, grid spacing and preparation assessment. `rank_by` requires
identical descriptors and state labels. A separate study-level comparison
contract remains needed for ordering distinct submitted conformations. This
prescription selects no new public API and manufactures no new energy values.

## Resources, failure and custody

Register exact notebook/helper/input/prescription identities before running
four plain Python cells in a fresh isolated process. The helper cell is reused
from the exact previously received preparation notebook; its code and file
hashes are explicit, without modifying package globals or a provider source.
Direct-call caps: convert 180, get 850, copy 20, set 40, H expansion 10, charges
10, types 10, preparation 10, H inventory 24, correspondence 30, map composition
10, pose reading 10 and tree reading 20. Unused inherited wrappers have cap 0.
These count only selected direct calls, not methods or provider internals.

One allowed logical CPU, nice 10, one native/build worker. Admit and monitor an
8 GiB available-RAM reserve, 1 GiB task RSS, 2 GiB address space, 60 CPU seconds
and 90 seconds wall time. Stop only owned work on resource threats; preserve
interruptions and do not automatically retry. Unexpected molecular/field/
domain refusals stop the remaining selection, preserve partial outputs and
require a separately registered correction. Keep both completed and failed
denominators under #78/#50, with custody review on **2026-11-13**. E4 remains
on its existing hold. This is development receiving, not installed/public
qualification, scoring admission already executed, or complete E1 acceptance.

## Common-box amendment before attempt 02

Attempt 01, notebook SHA-256
`8310b33ea8d2033e477fd7bb517e3f8a45ef9a168caf1307c184ab4a280fd400`,
stops at the fifth normal-policy pose's all-ligand-atom requested-domain check.
All five H/charge/type/preparation stages have executed; four poses complete
mapped reading and association capture. Fourteen witnesses pass, but no whole
unit profile completes. The original prescription, code, partial molecular
outputs, counts and failure remain separate. This 12.69-second attempt has no
resource interruption and runs no Vina operation.

The additional [source inspection](data/e1_complete_pose_2026-11-06/source_inspection_grid.json)
shows that Vina's [grid check](https://github.com/forlilab/AutoDock-Vina/blob/v1.2.7/src/lib/cache.cpp#L168)
uses effective voxel bounds and omits H; its
[header](https://github.com/forlilab/AutoDock-Vina/blob/v1.2.7/src/lib/cache.h)
declares a `0.0001 angstrom` margin. Requested and effective bounds differ after
upward voxel rounding. The failed conservative local test is therefore not a
newly executed native grid refusal. Retain that distinction and the source
identities; no backend behavior is measured by reading its source.

For the new complete-pose population, retain the stricter requested-domain
check on all thirteen ligand atoms and declare one common 24-angstrom box for
all poses and both unit policies. Preserve the original 20-angstrom box and
record both margins per pose. This is an explicit prospective study-domain
change, not a claim of equivalent historical scoring. Every future evaluation
must carry the actual new domain in its own context; do not rewrite historical
records or descriptors. Register the changed notebook and prescription, then
repeat the complete population from a fresh process with the original inputs,
chemistry, H placement and torsion policy. No attempt-01 observation is spliced
into attempt 02. Native effective-grid receiving remains future work.

## Executed complete-pose receiving

Attempt 02 completes all four registered cells in **20.53 s**, in a fresh
isolated Python process. Its [registration](data/e1_complete_pose_2026-11-06/registration.json)
binds notebook SHA-256
`b1ef3b1549f0e860356ba2bba6ebde701eed313916c9e6c87ee7d0f6ab99e665`;
the [frozen prescription](data/e1_complete_pose_2026-11-06/registered_prescription.md)
includes the common-box amendment before execution. This does not receive a
Jupyter frontend/kernel session or an installed/public artifact.

| Receiving | Actual complete-attempt outcome |
| --- | --- |
| Population | Five received heavy-coordinate sets, ten new complete preparations across two unit policies, one declared chemical state. |
| H and mechanics | Ten fixed-state local H expansions 9→18, ten named charge assignments, ten named typings, ten flexible reductions 18→13; four polar H retained and five nonpolar H merged per model. |
| Chemical checks | Thirty supplied-map witnesses: ten full18, ten prepared13 and ten mapped-read13. Four are first-reference self checks; counts are not independent molecular cases. |
| Prepared representation | Charges/types agree across new poses within the prescribed scope; the single active cut, nonidentity written order, source9 lineage, actual payload hashes and rounding checks pass. |
| Policies and custody | Corresponding native and BindingMT PDBQT bytes are identical between policies; explicit-unit full-precision comparisons and checked source snapshots pass. Historical scores and input bytes remain unchanged. |
| Domain | Minimum all-ligand-atom margin in the common 24-angstrom requested box is `1.0161559903577775 angstrom`. Pose 5's margin in the original requested box is `-0.9838440096422225 angstrom`. These are checked coordinate margins, not measured Vina grid acceptance. |
| Resources | One CPU, nice 10, one native/build worker; sampled peak RSS **315.55 MiB**, minimum available RAM **47.18 GiB**, no resource interruption. |

The [receipt](data/e1_complete_pose_2026-11-06/receipt.json.gz) retains the actual
editable Python/provider composition and loaded Rust binary identity; its
source/build correspondence stays unassessed. Direct calls are convert 156,
get 830, copy 10, set 30, H expansion 10, charges 10, typing 10, preparation 10,
inventories 22, correspondences 30, map composition 10, pose reading 10 and tree
reading 20. No registered cap is exceeded. No Vina import or energy call occurs.

The [manifest](data/e1_complete_pose_2026-11-06/manifest.json) binds molecular
reports/values, chemical-only H5MSM files, actual PDBQT exports/maps, exact
provided-receptor bytes, source inspection, registered code, diagnostics and
resource outcomes. Gzip is transport only; verify both compressed and decoded
identities before restoring an original filename. The identical decompressed
authority9 remains in original custody rather than being republished here.

The [attempt ledger](data/e1_complete_pose_2026-11-06/attempts.json) preserves the
failed population separately. Across both attempts, fifteen H expansions,
fifteen assignments of each kind, fifteen preparations and forty-four witness
calls actually execute. The failed run supplies no completed unit profile and
is not pooled with the separately repeated complete population. Its first four
complete associations and fifth model's partial receiving remain inspectable.

The [prospective scoring contract](data/e1_complete_pose_2026-11-06/prospective_scoring_contract.json)
now names the fixed provided receptor, five actual normal-policy ligand hashes,
one common 24-angstrom requested box, separate Vina/Vinardo methods and explicit
expected settings. Effective native parameters, references, score components
and backend artifact qualification remain unexecuted. A numerical ordering of
the new inputs is not admitted by the current strict `rank_by` route. The next
work is to register the finite native experiment against these exact complete
inputs and actual backend artifacts, preserving that ranking limitation and
all historical observations. Full E1 and the separate E4 hold remain unchanged.
