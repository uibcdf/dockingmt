# E1 finite native rescoring — 2026-11-06

Owner: [BindingMT #78](https://github.com/uibcdf/bindingmt/issues/78).
Status at prescription: **prospective**. This follows the
[complete-pose receiving and comparison matrix](e1_comparison_admission_2026-11-06.md).
The [notebook](e1_native_rescoring.ipynb) qualifies the selected backend and
executes a finite new fixed-score population. It does not repeat preparation,
search, optimization, historical scoring or interaction detection.

## Selected runtime and artifact gate

Use routine Python 3.14.10 with the current editable BindingMT/MolSysMT
composition. A task-local Conda artifact overlay supplies Vina 1.2.7
`py314ha160325_0`, SHA-256
`9a337ada583bf92635f34211c7c3dc47249b0bd85b912432a53b46f4e795d824`,
and libboost 1.86.0 `hd24cca6_5`, SHA-256
`a17ae9fd2af96eac7c29072b3e345ec3c2af42f18e33102633ab4440c1168ef7`.
Both come from official conda-forge artifacts, selected through publisher
metadata and verified before offline installation. Vina's required Boost range
excludes the routine prefix's Boost 1.90; never substitute that library by a
symlink. Supporting library versions are checked against the borrowed
runtime metadata. Actual loaded paths/hashes are retained; Boost must come from
the overlay. Other libraries are not individually matched to their package
manifests, so no full native dependency-closure claim follows.

This is an explicitly borrowed development composition, not a standalone Conda
environment, clean whole-environment closure or installed/public package gate.
The manager installs only those two selected artifacts into an owned prefix;
its cache also remains task-local. The shared environment remains untouched.
Preserve the manager's warning about unavailable optional environment-list
registration; do not seek permission to write that unrelated user registry.

Before any score call, verify installed Vina payload hashes against the Conda
path records, module/extension origins, distribution and module version 1.2.7,
Python ABI, native library mappings and library hashes. Add only the overlay's
site-packages to this disposable process. Native loader paths name the overlay
and borrowed routine prefix explicitly. Instantiate two unconfigured Vina
objects, one per method, with CPU 1 and seed 7. These two constructor/info probes
compute no maps or energies. Require actual default weights to match the
previous contract, and installed Python signatures to retain `no_refine=False`,
spacing 0.375 angstrom and `force_even_voxels=False`.

Constructor/signature inspection is distinct from observing an effective native
grid. The ten public score histories retain engine-reported weights/spacing;
they do not expose full native grid bounds, voxel state or a new measurement of
`no_refine`. Bind those defaults to the actual installed Python bytes and record
the limit. Matching a version label does not prove native source/build identity
or independent energy accuracy.

## Exact inputs and execution population

Verify every entry of the frozen complete-pose manifest, including compressed
and decoded identities. Stage its original provided receptor and the five
normal-policy `bindingmt.pdbqt` exports unchanged. Match each ligand hash to its
prospective scoring contract and retain its source/preparation associations.
No chemical/mechanical model is reconstructed from inspection sidecars.

Use one common box with center `[-1.759111,14.461,16.915778] angstrom` and size
`[24,24,24] angstrom`. Each new pose has the received common partner-state
declaration and its own pose ID; a case-local receptor label binds the fixed
provided bytes, without claiming complete receptor chemistry. Historical state
labels, scores, ranks, producers and the old box remain separate associations.

Read written ligand coordinates through public MolSysMT conversion with
explicit tree discard solely for that projection. Create a score-free
`DockingPose` in written order with no rank. For each pose, invoke public
`dmt.score` once with Vina and once with Vinardo, attaching the second result to
the first. The protocol has CPU 1, seed 7, captured backend inputs and timings;
it requests no new active cuts. The existing flexible tree is already in the
submitted bytes. Five poses × two methods gives **ten attempted evaluations**,
eighty new values and two histories per fully completed pose.

All ten calls run under one explicit nondefault pm/fs/coulomb/kJ-per-mol caller
policy. Inputs/backend boundaries retain their actual angstrom and kcal/mol
units. This is one native population, not duplicated native unit-policy runs;
the source inputs already passed their two-policy construction receiving.

## Checks and failure policy

Save each returned record before further assertions. Require eight new finite
components and one additional history per call, no mutation of the previous
pose or earlier scores, exact identity/coordinate preservation, unchanged inputs
and caller unit policy. Check actual method/version, weights, grid spacing,
box, requested/applied CPU/seed and unused search parameters against the contract.
Verify captured receptor/ligand bytes against the registered original files.
Retain native numbers unchanged, including zero and unexpected finite values.

The reference declaration must retain `native_current_conformation`, its actual
component name and the reported native value. Do not require references to be
zero/equal across poses, reconstruct a different total or manufacture a shared
reference. Require consistent standalone audits and exact finite-JSON pose
roundtrips; retain every intermediate eight-score and final sixteen-score record.

Create a five-pose scoring collection without invented docking provenance.
Its audit may be incomplete for missing collection-stage evidence, with no
inconsistencies. Public `rank_by` must reject both described totals because
actual partner contexts differ. Preserve that collection and both diagnostics;
do not erase input hashes, alter descriptors or introduce an ordering policy.
Present any numeric observation table in source pose order, with methods and
components separate, explicit kcal/mol units and no historical-energy pooling.

Direct caps: two qualification constructors/info probes; ten score attempts;
five direct conversions and coordinate gets; ten standalone audits/roundtrips;
one collection audit and two expected ranking refusals. Adapter/provider internals
are not counter-instrumented. Track attempted, returned and checked evaluations
separately in an append-only journal, including failures and partial outputs.
An unexpected backend, field, audit or context result stops later calls. Any
correction requires a separate registered attempt; no successful subset is
spliced across attempts.

## Resource and retention boundary

Register exact notebook/cell/input/artifact/prescription identities before a
fresh isolated process executes its four plain Python cells. Use one allowed
logical CPU, nice 10 and one native/build worker. Admit and monitor an **8 GiB
available-RAM reserve**, **1 GiB task RSS**, **2 GiB address space**, **60 CPU
seconds** and **90 seconds wall time**. Stop only owned work on resource threats,
preserve interruptions/signals and do not automatically restart interrupted
heavy work. Save package/native fingerprints before and after execution.

Retain inputs, individual evaluations/histories, captures, audits, parameters,
timings, warnings, qualification/installation diagnostics and all partial
attempts under #78/#50; custody review **2026-11-13**. This receives source-level
fixed-scoring integration and provenance only. No historical prepared-H identity,
affinity accuracy, common-reference ranking, complete E1, public distribution,
full supported-platform/minor matrix or E4 restart follows.

## Executed development/native receiving

Attempt 01 completes the four registered plain Python cells in **29.86 s**.
The [registration](data/e1_native_rescoring_2026-11-06/registration.json) binds
notebook SHA-256
`7b8e335de453b0f4ad11ca88305fbab99c3da804f87657f0c849375bca5ba626`;
the [frozen prescription](data/e1_native_rescoring_2026-11-06/registered_prescription.md)
predates execution. This is a disposable Python process, not qualification of
a Jupyter frontend/kernel session.

The [backend qualification](data/e1_native_rescoring_2026-11-06/backend_qualification.json.gz)
verifies all **103 installed artifact paths**, actual Vina Python/extension
origins, distribution/module version, ABI and required metadata bounds. Both
loaded Boost libraries are the private **1.86.0** filesystem/thread libraries,
with actual paths/hashes retained alongside 51 initially mapped native libraries.
Two constructor/info probes match the expected method weights and inspected
Python defaults. The final native-library inventory retains later provider
loads. These are artifact/integration observations, not independent kernel
accuracy or complete source/build correspondence.

The exact [artifact identities](data/e1_native_rescoring_2026-11-06/acquisition/selected_artifacts.json)
and [installation outcome](data/e1_native_rescoring_2026-11-06/acquisition/install-outcome.json)
remain separate. Offline installation succeeds in 1.44 s, with unchanged
borrowed Conda metadata and no Vina installed into the shared prefix. Its
[optional environment-list warning](data/e1_native_rescoring_2026-11-06/acquisition/install-stderr.log)
is preserved; that unavailable registry write is unnecessary for this explicit
prefix. No shared library is replaced and no source build runs.

| Receiving | Complete-attempt outcome |
| --- | --- |
| Native population | Ten public score attempts, ten returns and ten checked evaluations; five poses, Vina and Vinardo, eighty new finite empirical values. |
| Captures and parameters | Actual submitted receptor/ligand bytes, hashes, weights, 24-angstrom requested box, reported 0.375-angstrom spacing, CPU 1 and seed 7 agree with the registered contract. Search-only parameters remain unused. |
| Records | Ten consistent standalone audits and ten exact finite-JSON roundtrips; earlier pose objects/scores and all input bytes remain unchanged. Five final poses retain sixteen scores and two histories each. |
| Reference | Each evaluation retains its own `native_current_conformation` record and reported eighth component. No offset, reconstructed total or shared-reference declaration is added. |
| Collection | The saved scoring collection audit is incomplete for absent collection-stage provenance, with no inconsistent checks. No docking stage is invented. |
| Ranking | Both public ranking attempts reject the distinct described partner contexts. The collection is unchanged; no numerical ordering is performed. |
| Units/resources | One nondefault pm/fs/coulomb/kJ-per-mol caller policy with explicit backend angstrom/kcal-per-mol fields; caller policy restored. One CPU, nice 10, one native/build worker, sampled peak RSS **517.69 MiB**, minimum available RAM **47.57 GiB**. No resource interruption or termination signal. |

The following observations stay in source pose order. Each table concerns only
its named method, in **kcal/mol**; these columns are not a pooled affinity scale,
an admitted ranking, or reproduced historical docking scores. All eighty values
and the complete per-evaluation records remain in the
[observation record](data/e1_native_rescoring_2026-11-06/observations.json).

| Source position | Vina total | Vina `lig_inter` | Vina reported reference |
| --- | ---: | ---: | ---: |
| 1 | -6.067 | -6.422 | -0.043 |
| 2 | -5.912 | -6.258 | -0.043 |
| 3 | -3.878 | -4.105 | -0.043 |
| 4 | -3.786 | -4.007 | -0.043 |
| 5 | -3.313 | -3.507 | -0.043 |

| Source position | Vinardo total | Vinardo `lig_inter` | Vinardo reported reference |
| --- | ---: | ---: | ---: |
| 1 | -5.613 | -5.941 | -0.088 |
| 2 | -5.363 | -5.676 | -0.088 |
| 3 | -3.036 | -3.214 | -0.088 |
| 4 | -3.171 | -3.357 | -0.088 |
| 5 | -2.811 | -2.975 | -0.088 |

Equal three-decimal reference observations within each method do not establish
one shared unrounded energy reference. The original preparation, rigid tree,
box, native producers and reference conventions remain different historical
conditions. No historical score is modified or used as an expected new value.

The [receipt](data/e1_native_rescoring_2026-11-06/receipt.json.gz) retains counts,
native fingerprints and claim boundaries. The
[manifest](data/e1_native_rescoring_2026-11-06/manifest.json) binds all intermediate
eight-score/final sixteen-score poses, audits, collection, ranking diagnostics,
capture associations, timings and resource records. Gzip is transport only;
verify compressed and decoded identities before restoring an original filename.
Original complete-pose inputs remain in their existing custody and in native
captures; no duplicate staged-input archive is published here.

Runtime is Python 3.14.10, editable BindingMT `0.0.0+295.g2fda623`, MolSysMT
`0.23.0+513.g9e1f1b1ad`, ArgDigest `0.17.1+3.g0712641`, PyUnitWizard
`0.29.1+6.gf82b618`, NumPy `2.5.4`, DepDigest `0.15.2+2.g032d345` and
SMonitor `0.22.1+1.gc1b6ce2`, with the selected Vina 1.2.7 artifact. This differs
from the historical Python-3.12 installed producer; no old producer is relabelled.
The next E1 boundary is an explicit study-level comparison/ordering contract
with conservative refusal evidence, followed by appropriate installed workflow
qualification. These native observations alone do not close #78 or accept E1.
