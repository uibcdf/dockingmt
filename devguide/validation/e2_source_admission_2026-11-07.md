# E2 source-only admission prescription — 2026-11-07

Owner: [DockingMT #81](https://github.com/uibcdf/dockingmt/issues/81), with
chemistry/provider scope in #33/#49 and resource custody in #50. Status at
registration: **prospective**. Custody review: **2026-11-14**.

Receive the current chemical interpretation of both source candidates from the
[collection admission](e2_ligand_collection_admission_2026-11-07.md), before
preparation or native docking. This is one source-admission population with two
declared stereochemical entities. It does not receive the subsequent collection
execution, cross-ligand prioritization, biological activity or all E2.

## Immutable candidates and intended interpretation

Use the [candidate inventory](data/e2_ligand_collection_candidate_2026-11-07.json),
SHA-256 `898b26fa60561bb99f823d2dd0c27216cc5771ac7dceacdb103760fed2e22284`.
Verify its bytes and all seven listed source/context files before molecular
loading. Load only P59H and P69H SDFs. Preserve raw files, SD properties, source
license and upstream producer; the context receptor/crystal files are not new
chemical input authorities for these ligand models.

The expected fixture populations are 39 atoms, 42 bonds and 15 indexed H per
source. Preserve their supplied starting conformations. The historical control
is R for P59 and S for P69 at source index 7; require actual current provider
interpretation on the received axis, never inserted labels or a local matcher.
All source/state IDs are caller declarations, not chemical certificates.

For each source, explicitly call public `msm.convert` to native MolSys with
`stereo_engine='rdkit', discard_properties=True`, then native to `rdkit.Mol`
and back to native MolSys. Retain the original native and newly interpreted
authority separately. The actual provider's supported SDF wedge/3D interpretation
belongs to this recipe. No additional caller-side coordinate-based stereo
inference, atom addition, geometry generation, optimization or assignment occurs.

Use public readiness reports on both native representations. Receive explicit
CIP reports on the two new authorities with one selected structure, its associated
chemical state, engine `rdkit` and `from_coordinates=False`. Retain each field's
coverage and every unassessed check. RDKit can make previously unknown H or
aromatic declarations explicit; do not claim retrospective full-graph identity
or readiness of the partial original from the new authority's witness.

Require complete supplied-axis graph self-witnesses on the two newly interpreted
authorities through `msm.chemical_states.get_atom_correspondences`. The fixture's
predeclared identity axis must be checked with current public IDs/elements and
unchanged physical coordinates, tolerance `1e-12 angstrom`. This verifies the
declared conversion axis; it is not a general matching algorithm. Full new graph
coverage, actual R/S labels, populations, geometry and source nonmutation must
all be received for both candidates.

## Operations, records and acceptance

The unexecuted [source-receiving notebook](e2_ligand_source_receiving.ipynb) is frozen
with its cell hashes before
launch. Direct operation caps for the complete selection are:

| Operation | Cap |
| --- | ---: |
| SDF to native source conversions | 2 |
| Native source to RDKit conversions | 2 |
| RDKit to new native authority conversions | 2 |
| Readiness reports, original/new | 4 |
| Explicit CIP reports on new authorities | 2 |
| Supplied-axis new-authority self-witnesses | 2 |
| Preparation, H generation, charges, atom typing, searches, scoring, comparison execution | 0 |

These are direct orchestration caps. Snapshot format conversions, getters and
provider-internal SDF/stereo interpretation are not independently new cases or
separately attributed top-level transformations. The existing unshipped
`dmt_test_support.qualify_chemical_templates` inspection helper remains declared
through the shared installed-test support mechanism; its source/hash is frozen.
Do not introduce a molecular codec or restore MM from inspection records.

Run once under an explicit pm/fs/coulomb caller policy, with all boundary values
converted to declared physical units. Require policy preservation inside the
context and restoration afterwards. No second-policy repetition of molecular
work is registered. Save actual returned objects' inspections and provider reports
before qualification assertions; retain partial returns, exceptions, attempted
and not-attempted cases in a two-candidate ledger. A failure stops the complete
selection without substitution, silent repair, automatic retry or a passing subset.

The output is a finite source/interpretation manifest, raw inputs, original/new
native inspections, readiness and CIP reports, actual provider graph evidence,
axis/coordinate checks, nonmutation, operation/resource receipts and admit/refuse
dispositions. Inspections are evidence, not restoration inputs. Later preparation
will reproduce the same public source recipe and compare its actual fields;
no H5/MSM or MM persistence is claimed by this phase.

After a passing molecular receiving, a fresh standard-library process checks the
sealed records, original hashes, populations, source/state associations, reported
units, counters and detached finite JSON. It performs zero molecular operations.
This reader receives saved declarations; it does not independently revalidate
chemistry or authenticate a historical producer.

## Exact runtime and resource policy

Reuse the privately installed consumer from source
`a7422dfb9f8c3b1c8ede3d852e202dc33e4beefe`, wheel SHA-256
`93d76f898575fb64b39520f33ceded25708270c8042c2a53c9a451acd834bcdd`,
the existing 3,867-file target and identified borrowed MolSysMT snapshot
`9e1f1b1ad8bf09446374ab6f04ca7208e2717936` and support wheels. Freeze actual
RDKit/provider/module/native identities and verify complete private payload and
routine environment metadata before/after. This phase neither needs nor imports
Vina and does not install/rebuild providers or claim public dependency closure.

Register exact notebook/cell, prescription, candidate inventory, source/artifact,
support and harness identities before execution. Both molecular receiving and
the later independent reader run serially on CPU 0, nice 10, one native/build
worker including descendants, monitored 8 GiB available-RAM reserve, 1 GiB owned
group RSS, 2 GiB address space, 60 CPU seconds and 90 wall seconds per process.
Check headroom before launch and monitor it throughout; stop only owned work on
a threatened limit. Preserve interruptions and do not automatically restart.

Retain original warnings and every failure. A successful source phase still
requires separately registered preparation, native collection/control execution,
study comparison and whole installed/persistence receiving before E2 acceptance.
The current E4/live-visual holds, broader science and public-delivery owners are
unchanged. This prescription selects no native protocol, energy, package or release.


## Received source population — 2026-11-07

`source-01` passes for both declared candidates in the privately installed
composition. P59 is received as R and P69 as S on the preserved source axis.
Each original/interpreted model has 39 atoms, 42 bonds and 15 indexed H. Native
IDs/elements and physical coordinates survive the explicit conversion recipe
within 1e-12 angstrom, and all original/new live-source inspections remain
unchanged. Complete provider graph self-witnesses describe the new authorities;
no full equivalence of the initially partial native representations is claimed.

All direct caps are met exactly: six source/bridge conversions, four readiness
reports, two explicit CIP reports and two self-witnesses. Observed aliases retain
36 convert calls, 90 getters, twelve snapshots and four CIP calls (including the
source interpreter's two internal requests). These are not additional ligands
or independent experiments. Zero preparation, H generation, charge/type
assignment, energy, search or H5 persistence occurs. Vina is not imported.
The pm/fs/coulomb caller policy and its restoration pass, with complete private
payload/origin, routine-metadata and shared-support checks before/after.

Both initial SDF-to-native reports are lossy for the explicitly permitted SD
property blocks; exact raw files preserve those properties. The native/RDKit/
native reports are equivalent within their non-exhaustive audited chemical
scope. They do not establish universal chemical equivalence. In both cases,
aromatic atom/bond declarations and virtual/implicit-H fields change from
missing to present. Integer `bond_order` changes from present to partial after
aromatic interpretation; the received `covalent_multiplicity` and complete
provider graph carry the chosen aromatic representation. This partial field is
retained, not replaced with invented integer orders. Valence, protonation,
missing-H inventory, stereogenicity, conformer quality, parameterization and
experimental validity remain unassessed as reported.

The fresh `reader-01` receives all 57 sealed phase members with no scientific
imports. Exact raw hashes, source/state bindings, R/S labels, original/intermediate/
new-authority coordinates and explicit units, all direct counts, recorded graph
witnesses and readiness coverage transitions agree. No molecular operation or
energy is recomputed by the reader.

| Process | Outcome | Wall seconds | Sampled peak group RSS |
| --- | --- | --- | --- |
| `source-01` | PASS, both source interpretations | 21.63 | 331.55 MiB |
| `reader-01` | PASS, standard-library persistence receiving | 0.31 | 26.48 MiB |

Neither process has a resource interruption or termination signal. Source logs
contain no warnings; conversion-report losses remain explicit. These times
include imports, payload hashing and qualification, not a throughput benchmark.

The [original archive](data/e2_source_admission_2026-11-07/manifest.json)
contains 80 files, 971,125 stored bytes, plus its manifest. Manifest SHA-256:
`a5a60b65715b466bd04dc5e2bdb41a73489fdf9a13254552870628d387221b8d`.
Its original/decoded identities preserve inputs, code cells, registrations,
provider reports and source/reader receipts. Consumer source stays `a7422df`;
qualification base is `250db02`, with the actual notebook hash
`621144004826510370b13f6c5cc9bd7ea52ee4ec444888ec32381eb10ae7a6af`.
The prospective candidate inventory preserves its original pending counts; this
receiving owns the observed two admitted authorities. Inspection JSON is never
an MM or molecular restoration input.

Next register preparation receiving: reproduce these two authorities from the
same sources, compare actual fields to this admitted record, then explicitly
assign the named charges/types and prepare the declared rigid representations.
Keep complete source/projection/H accounting, actual bytes, source nonmutation
and all failures. Preparation and the later three-item native collection are
still unexecuted. Whole E2 remains partial, with its scientific/public/visual
boundaries unchanged. Private receipts and scripts stay task-owned under
`.molsyssuite/e2-source-admission-20261107` and the borrowed prior targets until
#50's custody review on 2026-11-14.


Applicable final local checks cover the unexecuted notebook's AST/cell identity,
Ruff lint/format, report indexes and maintained links, all archive stored/decoded
hashes, declared dependency/publication contracts and shared package resources
on the worktree and fresh source exports. Runtime code and fixture declarations
are unchanged, so prior software/distribution guards retain their own applicable
scope; they are not rerun as new molecular evidence. Exact-head hosted CI remains
missing under #28 and the maintainer's `[skip ci]` instruction, with no manual
remote dispatch. Fresh committed-source resource/index/publication checks follow
publication preparation without repeating scientific work.


The initial staged diff check identifies upstream trailing spaces in the copied
SDF property headings. Their original bytes/hashes are retained. The root
`.gitattributes` applies the existing fixture `whitespace=-blank-at-eol` rule
only to this archive's SDF source copies; source-code whitespace checks remain
in force. This is an archival attribute correction, not changed molecular data,
a new scientific attempt or a repeated interpretation.

## Subsequent preparation checkpoint — 2026-11-07

The later [named rigid preparation receiving](e2_preparation_receiving_2026-11-07.md)
reproduces these original source/authority observations before two fresh named
charge/type assignments and preparations. Both preparations and their separate
saved reader pass; original source records and this archive remain unchanged.
The resulting 25-atom representations retain R/S and fifteen represented H
through provider projection and exact export maps. The current next action is
native collection/control and study-policy registration under #81. Earlier
source-phase statements that preparation is unexecuted describe that original
population; they are not the maintained work queue.
