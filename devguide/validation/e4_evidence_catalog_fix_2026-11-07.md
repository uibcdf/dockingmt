# Receiving the provider evidence-catalog correction — 2026-11-07

Owner: [DockingMT #80](../pending_proposals/receive_docking_interaction_analysis.md).
Provider: [MolSysMT #642](https://github.com/uibcdf/molsysmt/issues/642).
Registered before execution; outcome at registration: **unexecuted**.

## Exact source and artifact boundary

The provider closed #642 with published correction
`4d8af6c34cb6b3f9e22833771b246d8767ef85e9`. Its source tests and real-carrier
checks do not receive DockingMT's actual installed client. Preserve both old
failed consumer attempts and every existing archive. This increment must not
discard unused labels, normalize catalogs or patch an installed provider module.

Use the unchanged DockingMT source `2ef82d2`, private wheel
`0.0.0+310.g2ef82d2`, SHA-256
`6db76835f4f3f9c41d06a163cb3a4fbc9e780597bfd89d2fc6a75d29cff31133`.
Build the complete provider wheel from the exact published correction in a
separate sparse Git checkout containing every runtime package and build input.
The local MolSysMT checkout remains clean at `9e1f1b1`, 111 commits behind its
freshly fetched main; Viewer local checkout/qualified overlay remain unchanged.
New provider Rust sources differ from the old binary, so borrowing that binary
cannot qualify the correction. No provider pin or routine environment changes.

One offline candidate-build attempt uses the installed Rust/Cargo1.99.1 and
setuptools-rust toolchain, a private copy of the cached Cargo registry/target
files and the explicit `SETUPTOOLS_RUST_CARGO_PROFILE=dev`. Preserve exact build
commands, source hashes, cache provenance, wheel RECORD/installed hashes and
new native binary identity. This private development-profile artifact carries
no release, performance, platform, public-channel or dependency-closure claim.
No dependency solve or network acquisition is allowed during that build. Do not
alter source/build configuration to force success; keep any failure/interruption.

Replace the old MolSysMT packages/addon/dist-info in a new task-local provider
prefix; retain every other transported provider byte. Reuse the verified
consumer/Viewer prefixes read-only. Verify loaded Python/native origins and
the routine Conda metadata before/after, without editable/source fallback.

## Finite scientific receiving

Only after a complete candidate build/install receipt passes, run one fresh
normal-policy cell, then one fresh pm/fs cell on identical frozen workers,
candidate and publication SDK `95f693be`. The complete normal selection must
pass before pm/fs. Use the immutable original retained carrier/result/association
from scientific producer `5952053`, exact input hashes from the prior archives.
Also read the immutable already-written failing carrier and compare its complete
typed analyses with its original pre-write diagnostic payload. No molecule is
reconstructed from an inspection dictionary or query page.

For each policy: read the original positive 3238-atom/one-frame carrier; retain
original native/typed witnesses and complete five-pose result. Publicly invalidate
`hbonds` at frame0, copy/reassociate the full carrier, bind the selected original
pose through the actual installed DockingMT API and receive detached accessors,
queries/pages and one full H5MSM write/readback. Require complete typed equality,
including the retained `baker_hubbard_hbond_geometry` catalog and original codes,
zero evaluated hbonds frames/occurrences and unchanged evaluated hydrophobic2.
Verify topology, chemistry, mechanics absence, frame/state/atom maps, coordinates,
units, method/producer metadata and original input/source/result nonmutation.
Original unaffected hbonds remain evaluated with three observations; four other
original poses remain unevaluated. No new docking/control pose is created.

Per-policy direct caps: original/immutable-failure/new-roundtrip H5 reads3,
H5 writes1, invalidation1, carrier derivation1, accepted binding1, detached
carrier accessor1, complete analysis accessor4, public analysis queries2/pages2,
native snapshots6 and typed exports32. Provider nested caps: convert128, copy40,
get640, has_attribute256, H5 reads3/writes1, invalidation1, analysis copy128,
remap16 and typed exports128. All extraction/merge/append/set, preparation,
H/charge/type assignment, detectors, distances/RMSD/energy/scoring/search,
alignment/coordinate transformations and View/browser/kernel creation are
forbidden. No persistence equality or numerical tolerance may be relaxed.

## Resources, custody and closeout

Run every build/scientific cell serially at CPU0/nice10/one native/build worker,
with 8 GiB available-RAM reserve, 1 GiB owned-group RSS, 2 GiB address space,
45 CPU seconds and 60 wall seconds. Reuse the frozen shared-request #173 guard
functions SHA-256
`3663659769ae4cddabd4edc8e351558fe900b568f195496ffd0a07e6f0c65c2d`.
Apply limits to heavy descendants; preserve terminal groups and interruptions.
Do not automatically restart heavy work after a headroom stop. A partial build,
process exit or passing provider tests alone cannot accept installed receiving.

Task `.molsyssuite/e4-evidence-fix-20261107` retains worktree, Cargo copies,
wheel/prefixes, source/tool/input/candidate identities, all logs and failures
under #50 custody, review 2026-11-14. Original migration files stay untouched.
Seal the completed records and receive them with an independent standard-library
reader. Update #80 and the maintained checkpoints with exact outcomes and limits.
No manual CI; #28 hosted exact-head evidence stays missing under `[skip ci]`.
Actual canvas #52/#60 remains held. Broader E4, E3 #604, Core/E5, independent
scientific reproduction, public/minor/platform delivery and full #73 remain open.

## Candidate interruption and registered retry

`candidate-01` reaches the 60 s wall limit during native wheel construction;
no candidate receipt or completed wheel is accepted and scientific cells do not
start. The group terminates with no live owned descendant, elapsed 60.235 s,
sampled peak group RSS 533,749,760 bytes and minimum available RAM 60,525,551,616
bytes. This is a wall-resource interruption, not a headroom stop or provider
scientific failure. Original provider/shared-prefix bytes remain untouched.

Register one fresh complete build/validation/install attempt, `candidate-02`,
with the same source, dev profile, offline boundary, resources and equality
requirements. Reuse only the first attempt's private exact-source checkout and
private Cargo copies/incremental objects instead of copying the same cache again.
Verify source identity before and after; choose a fresh wheel output directory,
retain the original logs/outcome and add verbose build logging. Private cache
reuse is not candidate acceptance; the complete wheel RECORD/source/native/
installed-byte checks and nonmutation receipts must still finish. Do not start
another retry automatically if this registered retry is also interrupted.

## Separate native-construction budget after cache-path diagnosis

`candidate-02` is also interrupted at the 60 s wall bound, elapsed60.205 s,
peak group RSS794,234,880 bytes, available-RAM minimum60,447,477,760 bytes,
terminal with no owned descendants. Its verbose native log explicitly reports
`Dirty ...: the path to the source changed`: the relocated private registry
requires dependency recompilation. No completed wheel, installed candidate or
molecular call is accepted. Both construction interruptions remain nonpassing.

The initial one-minute construction assumption is inadequate for an exact native
provider artifact. This is an agent-selected task budget, not a normative
repository time limit or a scientific acceptance tolerance. Before another run,
register `candidate-03` as a separate complete native construction with at most
600 wall seconds/300 CPU seconds per process, while retaining CPU0/nice10, one
Cargo/native/build worker, 8 GiB available-RAM reserve, 1 GiB group RSS and 2 GiB
address space. Reuse only private verified source/cache objects. Keep this
construction/resource population separate from every scientific case and preserve
all earlier failed receipts. No source, native feature, build profile, dependency,
RECORD assertion, equality check or scientific limit is changed. Scientific
normal/pm-fs remain 45 CPU/60 wall seconds with their original finite call caps.

This reviewed construction registration supersedes the automatic-retry stop:
it is a new explicit response to observed cache-path recompilation, not a silent
restart of the same one-minute attempt. If it hits a headroom or group-memory
stop, do not restart. Complete local evidence/custody and request an owner-built
exact artifact instead. A completed construction alone still proves no client
receiving, public compatibility, canvas or whole E4.

## Final construction disposition

`candidate-03` is interrupted at the owned-group RSS bound while compiling
`faer 0.24.4`: elapsed 202.384 s, sampled peak group RSS 1,075,798,016 bytes,
minimum available RAM 60,510,699,520 bytes. The 1 GiB guard detects that sampled
crossing and terminates only the owned group. Every group is terminal; no
owned descendant remains. No further build is started after this memory stop.

No complete provider wheel, installed provider prefix, candidate receipt,
scientific receiving, molecular import/detector or new source/provider adoption
is established. Prepared `run_fix.py`/`fix_worker.py` are unexecuted proposed
harnesses, not qualified code or ready permission to resume. All three attempt
registrations/frozen workers/raw logs/resources remain immutable observations.
The historical positive-source failures stay failed, and the earlier eight
installed View cells retain their old qualified provider/artifact scope.

Post-stop byte custody verifies that the unchanged consumer75/provider3794/
Viewer641-file prefixes still match their prior exact receipt, every copied
tracked provider source byte remains exact and its sparse checkout is clean
at 4d8af6c. Routine Conda metadata matches the prior verified candidate. No older
native binary is relabelled as this changed Rust source, and no module is patched.

**Next for #80:** request a complete owner-built artifact for the exact published
source and native payload, with digest/build/platform/metadata identity, or an
explicit provider-supported acquisition route. Keep this construction held;
new inputs need fresh admission before any native client receiving. Provider
#642 remains correctly source-resolved; a local construction interruption is
not a reopened provider scientific defect. Public availability/closure and
runtime/platform/minor acceptance remain separately unproven.

**Independent next work:** [E5 #83](../archive/qualify_independent_installed_reproduction.md)
owes a source-free installed reconstruction of the retained 1IEP representative
workflow. Inspect existing records/support/replay first; register every native
call before execution. Browser/comm/canvas stays held and the complete goal
remains active. No manual CI or shared-environment/provider-pin change occurs.

## Immutable construction custody

The [44-member construction archive](data/e4_evidence_catalog_build_2026-11-07/manifest.json)
is SHA-256 `f2af7ec1e07cde5883ebd64a973a0ad7367a5ed8c810686008ff17263ed81e25`,
592,331 stored/1,691,192 decoded bytes. It freezes every construction attempt,
raw commands/logs, resource classifications, source/cache provenance, unexecuted
prepared receiving harnesses and final byte-custody summary. The
[19-member administrative-reader companion](data/e4_evidence_catalog_build_reader_2026-11-07/manifest.json)
is `187dd4042d270f8471932e1fc93fab3532e2ef88c01c18a7acd049989ff67164`,
31,186 stored/84,901 decoded bytes. The detached standard-library reader verifies
all 44 primary stored/decoded records and the exact three interruption classes
in 0.103 s, with no scientific imports or molecular operations. Passing byte
custody does not accept any interrupted construction or unexecuted client case.

Applicable local checks cover lint/format, indexes, declared dependency routes,
shared resource/publication contracts, exact evidence, links and fresh base/
overlay exports. Fresh actual-committed export checks remain separately required;
task-local final/committed/published receipts retain exact qualified blobs and
final identities. No runtime/helper/fixture SHA declaration changes or scientific
reruns are part of this administrative closeout.
