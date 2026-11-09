# E3 saved-pose comparison and clustering

Owner: [DockingMT #79](https://github.com/uibcdf/dockingmt/issues/79).
Prospective registration: 2026-11-09, issue comment 6746958468; source
`ae0db98560f66ac6be7a933fb053f6e1e9917d99`, editable MolSysMT
`efbe67e1c6042078144bce1db24aa80bb565dbd2`, unchanged native SHA-256
`5715bda28be19820e96c2b81e4734bf75e1a9f05dd660d9c7e2817bc6bcd79d3`.

## Population and prerequisites

Use the original three P59 poses, positions 0/1/2, ranks 1/2/3, from the
[E2 native archive](e2_native_collection_2026-11-07.md). Authenticate all 193
members against manifest SHA-256
`4535ecab26c9fbe4d80bf50fabb48ec3a74ae067979f4e970f5523f703c98e46`.
Original P59 decoded record SHA-256
`c71b4789274f008130ecf512095246e310a18d3856344986f25d174abcde8a0e`;
P69 control `9cdbb66fc60517abd73533d2b4094191057b3b292ebe38396df7d7cc5eb7f8f3`.
Require state `e2-5x72-p59` and receptor state
`e2-5x72-protein-only-provided`; refuse P69 before molecular work.
Preserve original coordinates, scores, histories, rank and producer identities.
Three poses from one original run are not independent molecular cases.

The complete suffix-03 [reference prerequisite](e3_h5msm06_reference_receiving_2026-11-09.md)
passes normal/pm-fs with the corrected text-aware mechanical observer and five
altered-copy refusals. Independent 261-member receiving passes, with zero actual
quantity objects in the mechanical domain (unit-like text remains text).
Primary manifest `ae734a2ecc51a61defbb29a584527ce0acc72df80bb995a23dd8e4faa24d4eda`;
nine-member reader `f60c0dd34f1e8d8da0ed199fa7b685f3a3cbf8f1743eac6df775640612630935`.
Use the same fixed normal-03 source25/reference25/heavy24 H5 files in both new
profiles, not separately regenerated references.

## Frame and identity admission

Pin `tests/data/vina_torsions/5x72.pdb`, provided receptor PDBQT and box by
SHA-256 in the frozen plan. Their provenance is the unchanged upstream Vina
example at commit `3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`; retain the fixture README.
Read PDB with `get_missing_bonds=False`; do not assign chemistry to that PDB.
Select P59 A201. Identity order is only a candidate for this fixed pair:
require all 24 per-position elements equal and every Cartesian component within
**0.002 angstrom** of heavy24, plus public positional RMSD under that bound.
No inferred atom map, relabeling, superposition or alternate selection on failure.
Retained reference25 heavy coordinates stay within the original **1e-12 angstrom**.

Public exact-name correspondence matches four unique MET A1 anchors C/O/CA/CB
between original PDB and provided receptor. Require the same component and RMSD
bound and a finite nonplanar public dihedral. This admits only these pinned axes;
it neither validates receptor chemistry/preparation nor implements general frame
recognition. A public 1 nm translation must fail the same component criterion,
with original source unchanged. No centering, rotation, reflection or PBC imaging.

## Measurements and preservation

Reconstruct all three poses through `DockingPose.to_molecular_system` using the
same-axis source25 template. Concatenate with public strict-attribute policy.
Two fresh strict public chemical witnesses admit heavy24 within full fixed25
context: self and independent reference. No graph/H/state/stereo relaxation.
Call public symmetry-corrected and positional pairwise RMSD, independent
symmetry-corrected reference RMSD, complete-linkage primary clustering and
single-linkage sensitivity clustering. Cutoff **2 angstrom**, inclusive `<=`,
medoid representatives, original member order/tie rules. No score-selected member,
local RMSD/matrix/linkage implementation or new native search.

Serialize actual physical output fields with PyUnitWizard QuantityRecord and
explicit length handshakes; preserve provider maps/winners/provenance, array
dtypes/shapes and attribution. New analysis stays separate from original records.
Check source topology/structures/states/mechanics/reports, caller policy, configuration,
support retirement and exact source/import/native custody at completion.
Existing complete analytic/adverse geometry receiving (18 pairwise, 23 clustering,
22 typed refusals per policy) remains applicable only after verifying unchanged
relevant geometry/cutoff/test/native hashes; retain those comparisons in the task.

## Limits and execution

Private task `.molsyssuite/e3-pose-study-20261109`, owners #79/#50, review 2026-11-14.
Direct maxima per profile: three H5 reads, two PDB/PDBQT conversions, three
selections, 16 public getters, four frame RMSD, one name correspondence, one
dihedral, one translation, three pose reconstructions, one concatenation, two
chemical witnesses, two pairwise, one reference RMSD and two cluster calls.
Metadata/copy calls inside supported tools are recorded by their public boundary;
no H/charge/type assignment, search, detector, View or hidden source regeneration.

Run normal then pm/fs serially, identical frozen code/inputs. CPU 0, nice 10,
one native/build worker, monitored **13 GiB available-memory reserve**, 1 GiB
group RSS, 2 GiB address space, 45 CPU/60 wall seconds. Expected RSS below 512 MiB;
check actual headroom before each cell. No Slurm allocation; original bounded
inconclusive applicability probe retained. Stop on headroom loss; no automatic
restart or increased limits. Preserve every failure and unreached operation.
Compare final physical matrices/reference vectors across policies at **1e-12 nm**,
cluster membership/representatives exactly; canonical matrix byte digests may
honestly differ across float unit roundtrips. Receive records independently without
molecular replay before bounded E3 acceptance. Full scientific accuracy, broader
panel, actual canvas, installed/public/platform and hosted qualification remain
separate. No remote CI or shared installation is authorized by this selection.

One task-setup path typo is preserved before scientific-child creation; E2
hash authentication had completed but no molecular calls occurred. Its corrected
archive name does not change any scientific input, producer or assertion.

## First selection and call correction

Normal-01 fails after three H5 reads, two conversions, two selections and two
getters: our second atom-type request omitted `element="atom"`, leaving the
public getter at its system default. This is consumer invocation misuse, not a
provider defect. Preserve the failed process, logs and unreached operations.
Explicitly name the atom element in both element-inventory requests and execute
a fresh whole suffix-02 selection. Inputs, gates, counts and resource limits
are unchanged; no automatic resource-interruption restart is involved.

Normal-02 passes all physical frame/anchor/nonplanarity/translated-refusal
checks, then fails while serializing the public selection: it is a Python list,
not an array with `.tolist()`. Preserve the whole failed outcome. Replace only
three selection-list serialization/admission expressions with `list(...)`; no
index contents/order or scientific assertion changes. Fresh suffix-03 repeats
the complete selection with the same caps and limits before final receiving.

## Completed bounded receiving

Both final complete suffix-03 selections pass: normal **18.824 s**, peak
**251,191,296 B** sampled group RSS; pm/fs **19.044 s**, **250,859,520 B**.
Available memory stays above 60.65 GB; no interruption, no remaining owned process.
Both reach every scientific direct cap, with nine of16 allowed getters. All
physical frame checks, the nonplanar anchors and both negative controls pass.
Three reconstructed poses retain original state/order/rank/scores; strict
self/reference witnesses each contain two heavy24/full25 maps. Source snapshots,
mechanics/reports, caller/configuration/support and exact runtime custody pass.

Symmetry-corrected pairwise distances are approximately **8.6905,5.6365,7.6976 Å**
for pairs (0,1),(0,2),(1,2). Both complete and single linkage at 2 Å return
**three singleton groups**, original positions0/1/2 and their own medoids. This
is not evidence that the ligand has three independent binding populations.
The independent-reference distances are approximately **9.9181,5.2610,6.9923 Å**
in original order. No accuracy threshold or affinity conclusion is accepted;
the original first scoring rank is not selected as a geometric representative.

The immutable [256-member primary](data/e3_saved_pose_study_2026-11-09/manifest.json)
SHA-256 `0454c57f03f06d6860d6d9b34b28d3fb543efeaf53c4c2024250cac882e852f0`
contains 3,635,176 stored/29,326,507 decoded bytes. The
[nine-member independent reader](data/e3_saved_pose_study_reader_2026-11-09/manifest.json)
SHA-256 `a37a12ef79ea5b783956efbc26e8e82560cfb8227dcae20e94c355e20732a25a`
receives every member, both complete profiles, actual failures and frozen inputs.
It verifies **34 physical fields**, refuses four invalid quantity handshakes and
compares all reported physical arrays across policies within 1e-12 nm without
molecular replay. Membership/representatives agree exactly. Each clustering
matrix digest is independently authenticated using its shape and canonical nm
float64 bytes: normal `4bca2d0693d48a1cfd945ae7221fede537654c44d4836c8cea0afb27ef9007f9`,
pm/fs `7f603d22f129d54f27a47bdeed09a90bd0fa06db5dfdca361e7406ed39b80aed`.
Their honest byte difference does not change the admitted physical result.
Before reader execution, source review corrected its initial draft's omitted
shape prefix in this digest check. The sealed draft remains in primary producer
records; the actual corrected executed reader/hash is frozen in the companion.
No scientific record or original matrix digest is rewritten.

This receives **#79's bounded existing-P59 workflow**, alongside the unchanged
complete analytic/adverse geometry receiving and final public-0.6 reference
prerequisite. No new DockingMT runtime/helper/test or provider algorithm is
needed: consumer selection/provenance orchestrates supported public tools.
Preserve both failed whole normal selections, the setup failure, all old E3
failures, initial weaker reference seals and distinct original producers.

Remaining complete-product work includes #558's panel generation maps/history,
actual browser/comm/canvas observation under #52/#60, full exact public/installed
platform/dependency closure under #30/#47 and required hosted evidence #28/#21.
Provider #256's stable/default and broader receiving gates are its owner's scope.
The old interrupted native build remains historical; editable #642 was already
received at `c238513a1e76715a56abffb6528ba31bf913e226` and is not a current
codec blocker. The prior private wheel remains qualified only with its original
provider composition, not retroactively with the new provider source.

## Publication qualification

Seven final local checks pass: Ruff lint/format, generated report indexes,
shared installed-support resources, publication contract, diff whitespace and
exact stored/decoded authentication of all six new archives (802 members).
Runtime, addon, helpers, tests and devtools remain byte-unchanged. A fresh export
of the actual committed source must repeat the five relevant documentation/
resource gates and all six exact archives before push. Hosted CI is deliberately
unexecuted under the maintainer's incremental `[skip ci]` route; #28/#21 retain
that missing evidence. This is not a package release or full-suite claim.
