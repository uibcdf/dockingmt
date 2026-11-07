# E1 public reconstruction and additive rescoring — 2026-11-06

Owner: [DockingMT #78](https://github.com/uibcdf/dockingmt/issues/78).
Status at prescription: **prospective**. This receives the first missing
boundary in the [public-workflow review](e1_public_workflow_review_2026-11-06.md):
existing docking result → public reconstruction → explicit repreparation →
additive scoring and saved original/new result evidence.

## New population and existing authority

The historical result lacks a recoverable complete prepared authority; the newer
fixed-score collection lacks verified source maps. Neither is silently upgraded.
Create one explicitly new, bounded docking population from the already received
complete eighteen-atom model of pose 1. This is continuity/integration receiving,
not historical reproduction, pose recovery or affinity validation.

Use complete-pose manifest SHA-256
`45b3665ba09b6979aa1bcdf1bea0ac3e8102f081fefbfc51348c55bc71405df3`.
Its `normal/pose_1/full18_chemical_only.h5msm.gz` has compressed SHA-256
`bc81efd6a6d6de00141fb03473970a28f356c54bf95eefdf769fd972229bc468`.
Verify all manifest stored/decoded identities before loading. The file contains
previously received chemical/structural data and local H coordinates: **no new H
generation** runs. It has no complete MM payload. Calculate fresh named
Gasteiger–Marsili charges and AutoDock4 chemical-environment types through public
preparation options, without restoring inspection sidecars or old assignments.

The selected cut joins `C3` and `C1`. Resolve that explicit unique atom-name
selection through MolSysMT on each actual input axis, then request its pair in
`prepare_ligand`. Reuse the complete-pose contract's provided receptor and box:
center `[-1.759111,14.461,16.915778] angstrom`, size `[24,24,24] angstrom`.
The fixed receptor remains unassessed. The ligand is the declared new
benzamidinium model, with a separate experiment/producer association.

## Preparation gate before native work

Prepare full18 once, retaining its complete prepared13 native source, named
assignments, conservation evidence and nonidentity written traversal. Call its
public `to_molecular_system`, then `prepare_ligand` with only state/cut and no
H/charge/type options. This second preparation must consume the projected
mechanical attribution without recalculation.

Before any search require thirteen atoms, one cut, unchanged chemistry, charges,
types, coordinates and tree meaning, and source nonmutation. Receive a supplied-
identity graph witness for full18 and another for the prepared13 gate. Coordinate
and charge conservation use explicit nm/e expectations with absolute tolerance
`1e-12 nm` and `1e-12 e`. Keep the documented scoring PDBQT geometry tolerance
separate. Read exports through public MolSysMT to check rounded fields and tree
meaning. Derived reports, lineage, REMARK and hashes may change legitimately;
do not require byte/document identity between different preparation producers.
Retain all original/new reports. Unexpected chemistry, mechanics, axis or tree
stops the population before search; do not repair it or weaken admission.

## One finite new docking result

Register one public `dock` call: Vina 1.2.7, CPU 1, seed 7, exhaustiveness 1,
requested poses 2, explicit 3 kcal/mol retrieval range, input capture and timings.
Protocol cuts stay empty because the supplied prepared source carries its tree.
Save the full result before checking it. Retain all returned poses, their four
original scores, actual ranks/IDs, verified source maps, native output/captures,
settings and backend ranking history. Require a consistent source audit and at
least two returned poses for this multi-pose profile. Fewer poses are a preserved
incomplete population, not permission to change seed/box/effort or repeat.

The requested count is not guaranteed or an independent-complex denominator.
Native search/optimization belong to this explicit docking call; no additional
refinement or interaction detector runs.

## Portable public composition

The maintained `examples/rescore_existing_poses.ipynb` receives public objects:
the original result/prepared source, receptor, domain, explicit torsion selections
and a fresh output directory. Its cells contain no developer/SDK imports, frozen
data roots or qualification counters. MolSysMT resolves cut selections on each
reconstructed axis. No private tree, molecular matcher, PDBQT coordinate writer
or inferred permutation is implemented in client code.

For every original pose call `pose.to_molecular_system(source)`, then
`prepare_ligand` without H/charge/type recalculation, preserving state and selected
cut. `score(..., pose=original)` adds `vina_fixed`, then `score(..., pose=first)`
adds `vinardo_fixed`. Save every returned record before later work; retain a
progress/failure journal and stop on name collisions. For two poses this gives
four successful fixed-score evaluations and thirty-two added scalar components:
four original plus sixteen new values per pose. Preserve the original docking
reference convention separately from each fixed-score reference.

Combine new pose records with the original collection's actual problem/protocol/
provenance using public record/constructor operations. Save before auditing.
Require unchanged original scores/ranks/coordinates/states/ranking history,
consistent per-evaluation/combined audits and finite JSON roundtrips. Add no
collection stage or ranking decision.

Qualification stays outside the user cells. Inspect actual axes, mechanical
values/attribution, geometry and full graph witnesses on reconstructions and
preparations. Supplied identity maps are allowed only after ordered IDs/names
confirm the axis. Another axis stops this finite profile rather than being
guessed. Selection transports the declared cut independently of assumed order.

After positives, use two detached controls: changed partner-state declaration
and a pose paired with the other pose's prepared geometry. First confirm the
two geometries differ beyond scoring tolerance. If not, the control is not
received; do not invent a displacement. Both score names must be fresh and both
calls must refuse for the expected state/geometry reason before native scoring,
preserving inputs. Two new-component `rank_by` requests must retain exact-context
refusals. Existing source ranks/history keep their original meaning; no positive
comparison policy or new public comparison API is claimed.

## Runtime, counters and failure policy

Reuse the exact private DockingMT/support wheels, borrowed MolSysMT snapshot and
Vina/Boost overlay of the [installed receiving](e1_installed_receiving_2026-11-06.md).
Check 3,824 private paths and 103 engine paths before/after, actual module/native
origins/versions and unchanged routine Conda metadata. Retain the generated
PyUnitWizard module's received initializer binding. This is the same private
installed-consumer scope, not a rebuilt provider or public/environment closure.

For two poses direct caps are preparations×4 (source, gate, two reconstructions),
public pose reconstruction×2, docking attempt×1, scoring attempts×6 (four returns,
two expected pre-native refusals), supplied-map witnesses×6, charge audits×4 and
new-component ranking refusals×2. Track attempted/returned/checked separately;
these caps do not count all provider/native internals. A fresh JSON process
checks saved source/updated records, captures, scores/ranks/histories and
detachment without engine, molecular, preparation or ordering operations.

Hash receiving/user notebooks and cells, prescription, immutable inputs,
composition and harness before execution. Run serially on CPU 0, nice 10, one
native/build worker. Monitor an 8 GiB available-RAM reserve, 1 GiB owned-group
RSS, 2 GiB address space, 60 CPU seconds and 90 wall seconds per process. Stop
only owned work on a threatened bound; preserve interruptions and never restart
heavy work automatically. Save every returned record before later assertions,
stop unexpected outcomes and never splice successful subsets across attempts.

Retain original/new records, chemistry/mechanics/axis evidence, registration,
progress/diagnostics, partial failures and resources under #78/#50; custody review
**2026-11-13**. The positive user-comparison boundary, historical prepared13
identity, accuracy, public matrix, whole E1/E5 and separate E4 hold remain.

## Preserved preparation stop and registered copy correction

Attempt 01 stops in 6.27 s during its first preparation attempt:
`ModuleNotFoundError: No module named 'molsysmt.build'`. The case-local provider
copy had excluded every directory named `build`, including MolSysMT's legitimate
Python runtime package. This is an error in the private snapshot preparer, not a
demonstrated provider/API defect. One full18 chemical self-witness completes;
no preparation returns, charge computation, search or fixed-score call occurs.
There is no resource interruption or termination signal.

Before attempt 02, create a separate private target for this receiving. Preserve
the earlier 3,824-file target and its qualification unchanged. Copy its exact
wheels/metadata and provider files, then add every missing file under the actual
provider package roots, excluding only Python/Git caches rather than runtime
names such as `build`. Compare existing files against their sources and never
silently replace a mismatch. Keep the original native extension and its actual
identity; no provider wheel or compilation is fabricated.

The correction receipt retains old preparation identities, the full new target
and source inventories, exclusions and scope. Hash it and the corrected harness
before repeating the complete selection. Scientific criteria, portable notebook,
native artifact and operation budgets stay unchanged. Do not splice the first
attempt's witness into the complete second attempt. Final custody includes both
outcomes and the precise remaining private-composition limitations.

The corrected target contains **3,866 files**, including the missing 42 runtime
files of `molsysmt/build/`; its provider source inventory contains 3,481 entries.
The original 3,824-file target and both original preparation receipts remain
unchanged. Correction SHA-256:
`96b164638d132327e4e514b7160fd7e92bd5b4e4fe322026ae47dffdb77db364`.

## Returned population and separate singleton receiving

Attempt 02 completes both preparations, two charge audits and the two supplied-
map gate witnesses, then executes its single registered search. Vina returns
**one** pose from the requested two. The complete result is saved before the
minimum-population assertion stops the run. This two-pose receiving remains
**incomplete**; no seed/box/effort change or repeat search follows.

The actual result JSON SHA-256 is
`cd0e7e20a64034a5b1462f2c42810a83a0b247a4d1af56c237ceca13719fe55c`.
It contains four original scores, rank 1, verified keys and an actual backend
ranking history. Its submitted ligand hash is
`dc4e89dc86bd02012b6e14ed1432fc470c1366ba2f66345fe27dc818ce2b873b`.
There are no fixed-score returns in attempt 02. The process stops in 9.30 s,
sampled group peak 573.90 MiB, without resource interruption or signal.

Register a **new existing-single-pose continuity population**, attempt 03,
consuming that exact result, rather than redefining the failed two-pose test.
Its [receiving notebook](e1_single_pose_receiving.ipynb) reproduces the source
preparation through fresh public charge/type assignment on the same full18
authority. Before reconstruction or scoring, require exact original submitted
PDBQT hash, captured-input integrity and agreement of IDs, names, coordinates,
charges, types, state and traversal with the saved source-preparation inspection.
Inspection sidecars are comparisons only; no mechanical values or reports are
restored from them. The freshly received thirteen-atom graph digest must agree
with the original gate witness within the same correspondence schema.

Run the **same portable public notebook** on this actual one-pose result. Preserve
its four scores/rank/history and add two named evaluations/sixteen components.
The new direct caps are preparations×2 (source reproduction, pose preparation),
pose reconstruction×1, searches×0, score attempts×3 (two returns, one changed-state
refusal), supplied-map witnesses×4 and charge audits×2. The extra initial
thirteen-atom witness authenticates the reproduced authority before user work.
The [new fresh JSON reader](e1_single_pose_reader.ipynb) receives the singleton
under both reader policies, retaining the existing audit/roundtrip/detachment
caps. Both new notebooks and the changed registration/harness are frozen first;
the original N2 notebook rules and frozen attempts are preserved.

The swapped-geometry control is **not received/not attempted** without a second
pose. No singleton `rank_by` rejection is expected or claimed: a one-member
collection can satisfy that API's comparison condition. The positive user
comparison policy and multi-pose continuity remain pending. This new population
adds no search and cannot retroactively turn attempt 02 into a two-pose pass.
