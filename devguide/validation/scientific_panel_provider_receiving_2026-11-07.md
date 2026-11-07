# Scientific-panel occupancy and CCD-reference receiving — 2026-11-07

Owner: [DockingMT #33](../pending_proposals/validate_native_molsysmt_formats.md),
with [#49](../pending_proposals/retire_general_molecular_operations.md) retaining
molecular ownership. Starting source: `9977317bfdbff60ee783043c5445f5b3e9719920`.
Status: **bounded read-only receiving passes; panel admission remains partial**.
No runtime, public API, helper or scientific-fixture declaration changes occur.
This increment improves evidence for the provider integration; it measures no
speed gain or interface usability.

## Delivered boundary

Two complete serial cells, normal and pm/fs/coulomb, receive public MolSysMT
CIF primary occupancy and coordinate-free neutral CCD references for MK1/BTN.
Strict explicit-label maps and read-only template assessments pass against both
original PDB and CIF observations of 1HSG/1STP. Eight intentional typed refusals,
source coordinate/readiness nonmutation, input/prefix preservation and caller
unit restoration pass. A fresh stdlib reader verifies the sealed records.

This receives the bounded consumer uses of source-resolved
[MolSysMT #556](https://github.com/uibcdf/molsysmt/issues/556) and
[#557](https://github.com/uibcdf/molsysmt/issues/557). It does not choose bound
protonation, apply a template, prepare a receptor or admit a docking case.
Both original candidates and the proposed 24-search matrix remain unadmitted.
Previous E5 1IEP reconstruction remains received under
[#83](../archive/qualify_independent_installed_reproduction.md); it is not a new
independent molecular case or authorization for another E5 campaign.

## Exact composition and private artifact route

The original qualified provider `9e1f1b1ad8bf09446374ab6f04ca7208e2717936`
lacks both new public #557 modules. #556 is source-fixed at
`06c065d335c7e42af141e9d85ee8e7e65a08e279`; the selected complete Python source
is the #557 closeout `faab727ca5b5c9078e2f2e505971fc0ea1cf1a8d`.
A bounded central workspace refresh preserves source/main worktrees, fetched
state, the original migration and all existing prefixes.

Public [Conda registry metadata](https://api.anaconda.org/package/uibcdf/molsysmt)
is acquired once under 25-second/16-MiB bounds. The 107-file inventory does not
establish a newly covering public artifact. The actual old main 0.23.0 and
staging-only 1.0.0 files retain their earlier
[public-readiness disposition](public_candidate_readiness.md); the API summary
latest-version field is stale. No solver, public install, environment update or
remote workflow is run.

Complete Rust tree `32cfb07b9c26ae9ad3ed379c1b76fab85669cf67`, build-system
requirements, setuptools-rust declaration and ABI3 options are identical at
9e1f1b1 and faab727c. Standard unmodified setuptools `build_py` assembles the
whole isolated faab worktree; its declared build output receives the unchanged
qualified native extension. Standard `bdist_wheel --skip-build` produces the
complete private wheel without compiler entry, build-class patch, individual
module replacement or forged metadata/RECORD. Source/resource/member hashes and
native equivalence are retained. The version comes from upstream versioningit.

| Identity | Exact receipt |
| --- | --- |
| Private provider wheel | `molsysmt-0.23.0+520.gfaab727ca-cp311-abi3-linux_x86_64.whl`, 223,631,482 bytes |
| Wheel SHA-256 | `c603fbde78a58fcec43d6d0fb8a6b27dabcbef706c19c35b4f5033c8a8dae9c6` |
| Reused native SHA-256 | `2a79b9a83b0fe0b00a54c9b80f04bf6c9ace2b3473c53269edbfe29904f8930b`, 101,188,064 bytes |
| Installed candidate manifest SHA-256 | `c7061d409bf59f8598027588f7dd8589edea16c36a58812436fad0c2adb5e76a` |
| Consumer | unchanged `2ef82d25e34266d1b504464dc238e8863a9dade0`, wheel `6db76835f4f3f9c41d06a163cb3a4fbc9e780597bfd89d2fc6a75d29cff31133` |
| Viewer context | unchanged `78ede79e`; no Viewer is constructed |

The native binary retains its original 9e1f1b1 source/qualification context;
no new compilation or compiler-source receipt is claimed. Receiving is private
Linux/Python 3.14.10 only. #642 source `4d8af6c` has different Rust tree
`fb25b2eac60b6e706c712e788119b3dad94329fe`: this reuse is forbidden there.
Its owned-memory build interruption and artifact request retain their hold.

Whole-wheel admission installs into a fresh prefix with no dependencies,
bytecode or shared-environment writes: 3,793 files, including 313 retained support
files and excluding all 3,481 old provider/addon/distribution files. Actual
module/native origins and both new public tools verify. Prefixes, old native
artifact and routine Conda metadata remain unchanged, including the previously
observed plantuml entry. This is no whole-environment or public-provider release.

## Inputs and prospective selection

The original [panel design](scientific_panel_design_2026-11-04.md),
[source admission](scientific_panel_admission_2026-11-04.md),
[environment observations](scientific_panel_environment_2026-11-04.md) and
[terminal diagnostic](scientific_panel_terminal_probe_2026-11-04.md) retain their
original producers and limits. All four original PDB/CIF raw SHA-256 identities
verify through their existing archive; they are not duplicated here.

Two unchanged provider fixtures are retained once from exact faab source
`tests/physchem/data/chemical_templates/`: MK1.cif SHA-256
`c1d46b02c24a3f7e6c089762a365c094078d9a00aee824131d75768d2805141a`,
BTN.cif `9fff069dc9e0387d49c3ef62cab0867a10dae56274931a779fb87f377b9c11ea`.
They are local CCD reference definitions, not new online acquisitions or bound
state decisions. The ledger's embedded EST fixture manifest is historical
context only; MK1/BTN attribution is their actual source paths/bytes/reports.

Before molecular calls, the input ledger, candidate, resource policy and exact
finite selection are frozen. A complete normal PASS precedes the identical
worker/candidate/input pm/fs cell. Each calls public MolSysMT only:

| Direct call kind | Registered and observed per cell |
| --- | ---: |
| Original source conversions | 4 |
| Coordinate getters, explicit angstrom extraction | 8 |
| Primary occupancy getters | 4 |
| Ligand selections | 4 |
| Chemical-readiness reports | 10 |
| Reference constructors, positive / missing source | 2 / 2 |
| Explicit name maps, positive / repeated-query refusal | 4 / 2 |
| Read-only template assessments | 4 |

Nested observed counts are convert 4, get 28, get_form 592, select 34,
has_attribute 8, copy 0, within registered 64/1024/2048/256/256/64 caps.
PDB reading declares `get_missing_bonds=False`; CIF retains its existing named
reader policy. Asymmetric units supply source/ligand observations only; the
original dimer/tetramer receptor requirement is not changed.

Reference construction explicitly selects `ccd_canonical_descriptor`,
`stored_counts`, stored descriptor program `CACTVS`, and `max_matches=4096`.
RDKit 2026.09.2 actually interprets the descriptor; CACTVS is not executed.
The reference contains no coordinates. Unique-name/element correspondence is
not a generic chemical equivalence claim. Assessment uses reference state and
`require_same_graph`; compatible/conflict/unassessed were all allowed outcomes,
without application or repair. Missing local files refuse with
`ChemicalReferenceLookupError`, repeated map queries with `ArgumentError`.
Network and engine/compiler entry are denied during both scientific cells.

## Observations and failure accounting

| Candidate | Reference heavy / stored H | Source atoms / occupancy | PDB and CIF reference assessments, both policies |
| --- | --- | --- | --- |
| 1HSG / MK1 | 45 / 47 | 1,686; all occupancy 1 | compatible |
| 1STP / BTN | 16 / 16 | 1,001; 930 ones, 71 nonunit, minimum 0.42 | compatible |

No H is generated. Occupancy stays on each native source axis; only declared
distributions are compared between formats. No positional PDB-to-CIF map or
copied occupancy array is invented. Coordinates/readiness are exactly preserved
within each cell. Across policies, all observed report/map/occupancy fields
match; explicit angstrom coordinate witnesses differ descriptively by at most
1.4210854715202004e-14 for 1HSG and 7.105427357601002e-15 for 1STP.
These are reader arithmetic observations, not a retrospective pass tolerance or
new molecular measurement. Serialized witness field/unit/axes are declared in
the primary manifest; the reader explicitly selects that field and unit.

| Cell | Outcome | Wall seconds | Sampled group RSS bytes |
| --- | --- | ---: | ---: |
| Public artifact inventory | PASS | 0.854 | 26,324,992 |
| Whole private wheel assembly | PASS | 12.091 | 291,610,624 |
| Initial in-process-pip admission | FAIL | 8.790 | 277,508,096 |
| Fresh subprocess-pip admission | PASS | 10.448 | 250,896,384 |
| Normal reference-only receiving | PASS | 7.781 | 333,586,432 |
| pm/fs/coulomb reference-only receiving | PASS | 7.672 | 333,520,896 |
| Detached stdlib record reader | PASS | 0.408 | 65,884,160 |

The first admission fails its final unit-policy restoration assertion after
unsupported in-process pip use. Its installed files remain unchanged; the
prospective correction separates pip into its own process and uses a fresh
prefix, retaining all authority assertions. No provider/PyUnitWizard defect is
inferred from that task misuse. The failed attempt stays failed. An initial
worktree target-path error was corrected with Git's worktree move before build;
the isolated source is retained under this task and sibling main is unchanged.
All original warnings, logs, frozen prescriptions and producer scripts survive.
Intentional negative-control ERROR lines are retained and not test failures.

All cells use logical CPU 0, nice 10, one worker, 8 GiB available reserve,
1 GiB owned group RSS, 2 GiB address space, CPU 45 / wall 60 seconds. Every group
is terminal; no resource interruption or automatic heavy restart occurs.
All new native searches, template applications, terminal/H reconstructions,
energies, RMSDs, detectors, views and admitted docking cases are **zero**.

## Sealed records, checks and next action

[Primary manifest](data/panel_provider_receiving_2026-11-07/manifest.json):
126 members, 3,433,272 stored bytes, SHA-256
`0c5c9e8fe95f115f4ab37b627afc96a5e28706cfba9b5285ac31f6a8998663d1`.
[Reader companion](data/panel_provider_reader_2026-11-07/manifest.json):
20 members, SHA-256
`607af29018ecbd408f89ebbcd044294474fef4d99d95dbe4a3de143f49380b85`.
The fresh isolated stdlib reader authenticates stored/decoded bytes, linked
original inputs, candidate/worker identities, exact call counts, both complete
cells and all eight refusals without scientific imports. It does not replace a
new molecular calculation. Scripts are inert compressed text in the archive.
The molecular campaign is terminal; its controller rejects additional calls.

Applicable final checks cover indexes, lint/format, dependency routes,
publication contract, exact archives, links, source/prefix custody and shared
installed-test resources, including a fresh committed export. Exact receipts
remain task-local; publication records the actual commit and executed outcomes.
No full pytest or hosted CI result is invented from documentation checks;
unchanged runtime/helpers retain their previous qualification identities.

**Next:** record evidence-backed ligand/catalytic state, water/other-ligand,
terminal/truncation and full-assembly decisions for each original candidate.
Receive public terminal-completion correspondence/history under
[MolSysMT #558](https://github.com/uibcdf/molsysmt/issues/558) before using generated
receptor atoms. `add_terminal_atoms` requires caller coordinates and is not an
alternative geometry generator. Register any next application/preparation/search
selection only after these actual prerequisites pass. No local CCD parser,
matcher, reconstruction map, OXT placer or chemistry fallback is authorized.

#33/#49 stay partial; full #73 remains active and unproven. E3 #604 and actual
canvas scheduling holds persist; #642 native construction is not restarted.
#30/#47 public/platform/minor delivery and #28 missing hosted evidence remain
separate. No manual CI or release follows. Complete task resources, source
worktree, private wheel/native files, prefixes and caches remain under #50,
review 2026-11-14, until custody review and covering owner-built artifact receiving.
Original migration material stays untouched.
