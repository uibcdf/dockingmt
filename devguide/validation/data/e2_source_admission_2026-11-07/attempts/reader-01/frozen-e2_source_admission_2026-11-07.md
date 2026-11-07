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
