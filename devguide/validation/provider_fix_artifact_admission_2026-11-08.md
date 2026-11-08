# Shared provider-correction artifact admission — 2026-11-08

Owners: [DockingMT #33](../pending_proposals/validate_native_molsysmt_formats.md),
[#49](../pending_proposals/retire_general_molecular_operations.md) and
[#80](../pending_proposals/receive_docking_interaction_analysis.md).
Starting source: `acce58e3dc0ff17673f091b42765fb65257b8977`.
Status: **focused rebuilt-editable receiving passes; original whole workflows and public artifact qualification remain unreceived**.

## Rebuilt editable provider receiving — 2026-11-08

After the maintainer reported completing the editable reinstall, the routine
environment actually imports MolSysMT `0.23.0+687.g2325038e8` from clean
`../molsysmt` at `2325038e8c68157f5c730693ffbb8535f0b45540`, and DockingMT from
this editable checkout. The loaded `_rust.abi3.so` is 101,190,496 bytes, SHA-256
`5715bda28be19820e96c2b81e4734bf75e1a9f05dd660d9c7e2817bc6bcd79d3`;
it differs from the earlier unchanged binary. Imports retain the application's
pm/fs/coulomb policy. `python -m pip check` passes. This records observed runtime
identities after the maintainer's build, not an independently audited build log
or a public package qualification.

The focused MolSysMT selection passes **115 cases**, zero failures/errors/skips:
complete evidence-catalog persistence across four routes, invalid formal-charge
diagnostics/nonmutation, explicit indexed-H normalization with typed history,
component-type comparison flags, direct rotated-cell native kernels and changing-
cell unwrap. The original provider guards include normal/nondefault unit
profiles. Eight existing DockingMT modules pass **383 cases once**, zero
failures/errors/skips, for result/pose/protocol/box/schema/argument boundaries.
No assertion, selected guard or source module is modified. The
[11-member archive](data/editable_provider_receiving_2026-11-08/manifest.json)
retains exact selections/input hashes, producer and guard sources, actual import
origins, dependency output, raw JUnit, receptor logs and terminal resource outcomes.

All four checks run serially on CPU 0/nice 10/one worker with native/build workers
limited to one, a monitored 13 GiB available reserve, 1 GiB group RSS, 2 GiB
address space and CPU 45 s/wall 60 s per group. Import: 2.657 s/124,518,400 bytes;
dependency check: 1.536 s/43,196,416 bytes; provider guards: 16.677 s/225,312,768
bytes; consumer guards: 6.548 s/129,110,016 bytes sampled peak group RSS. Minimum
available RAM across them is 56,385,351,680 bytes. Every owned group is terminal;
no resource interruption occurs. The maintainer's compilation resources were
not measured by these subsequent checks. No new build, install, molecular dataset,
search or remote CI is launched here; keep the task under #50/review 2026-11-14.

The refreshed development composition can now receive the original complete
#33/#49/#79/#80 workflows. Preserve their historical failures until each complete
selection succeeds; these synthetic regressions are not independent scientific
cases or a replacement for those workflows. #604 clustering, #558 maps/history,
actual canvas and full public/minor/platform acceptance remain separate. No
separate owner-built artifact is required to continue routine development.

## Maintainer-directed editable development route — 2026-11-08

The maintainer corrected the operational resumption route: the participating
components are developed together from editable local checkouts. A separate
owner-built or published package is not required to receive ordinary Python
source updates. The earlier artifact request remains an optional acquisition
route and a historical observation, rather than a prerequisite for routine work.

`git pull --ff-only origin main` advanced clean `../molsysmt` from
`9e1f1b1ad8bf09446374ab6f04ca7208e2717936` to
`2325038e8c68157f5c730693ffbb8535f0b45540`, receiving 174 commits. The checkout
is clean and matches fetched `origin/main`. Existing routine Python 3.14.10
distribution metadata declares this checkout editable; module resolution selects
`../molsysmt/molsysmt/__init__.py`. This is source/installation-origin inspection,
not a successful import, affected runtime test or completed client workflow.

The native extension is unchanged: `_rust.abi3.so`, 101,188,064 bytes, SHA-256
`2a79b9a83b0fe0b00a54c9b80f04bf6c9ace2b3473c53269edbfe29904f8930b`.
The new source retains Rust tree `fb25b2eac60b6e706c712e788119b3dad94329fe`,
whereas the old context has `32cfb07b9c26ae9ad3ed379c1b76fab85669cf67`.
`rust/src/mic.rs` and `rust/src/pbc.rs` changed. Editable Python updates do not
recompile native code. Next inspect the affected native signatures and determine
the required local development rebuild under conservative resource limits before
affected receiving. The previous #642 interruption remains preserved; this pull
does not automatically restart it or establish complete native compatibility.

No dependency installation, source pin change, scientific calculation, public
package receiving or CI dispatch occurs. Original failures and private artifacts
below are unchanged. #604 clustering, #558 maps/history, caller-policy controls
and full public/minor/platform delivery retain their separate scope. The
untracked migration directory is preserved. Resume through the
[updated development handoff](../MACHINE_HANDOFF.md#maintainer-directed-editable-provider-refresh--2026-11-08).

## One coherent source target for three receiving needs

The previous [reference checkpoint](scientific_panel_receptor_models_2026-11-08.md)
retains all original failed selections. Fresh provider notices identify
[formal-charge correction #644](https://github.com/uibcdf/molsysmt/issues/644)
at `64f8c955ac8b93198f4926642d4f3d257a1d0c27` and
[comparison correction #646](https://github.com/uibcdf/molsysmt/issues/646)
at `ad67e0e915ba23d90cb9d6331c063c342852d67a`.
The latter source commit is independently present on GitHub. Its owner reports
220 source cases and fourteen fast gates; #644 reports 474 cases/fourteen gates.
Those are provider source observations, not this client's installed receiving.

A bounded private Git-object fetch verifies that `ad67e0e` contains both
`64f8c955` and the earlier evidence-catalog correction
`4d8af6c34cb6b3f9e22833771b246d8767ef85e9` (#642). One whole compatible provider
artifact could therefore serve all three separately owned client workflows.
Their original scientific and adverse controls remain unchanged; no acceptance
is pooled across them.

| Source context | Complete Rust tree |
| --- | --- |
| Old qualified native 9e1f1b1 and Python faab727ca | `32cfb07b9c26ae9ad3ed379c1b76fab85669cf67` |
| #642 source 4d8af6c, #644 source 64f8c955, #646 source ad67e0e | `fb25b2eac60b6e706c712e788119b3dad94329fe` |

The three correction contexts also retain identical source-declared
`build-system`, `tool.setuptools-rust` and `tool.distutils` sections. These are
source/build-input comparisons, not compiler/platform/profile or native-binary
qualification. A provider-qualified native from the #642 context could be
considered for whole-source assembly only with its exact artifact and build
provenance; no such native artifact is received here. The old 32cf native remains
ineligible for this full target under the declared candidate contract.

The preserved local MolSysMT checkout stays clean at 9e1f1b1. Inspection uses a
separate bare object store inside this task, with shared read-only old objects;
no existing checkout, installed module, pin or compiled binary is replaced.
The provider's later resolved report is available on current main, separately
from the original fix commit. Its initially absent archived path at the fix
commit does not imply that the independently verified code commit is missing.

## Advertised package observation

One bounded public request reads
[the MolSysMT registry metadata](https://api.anaconda.org/package/uibcdf/molsysmt):
183,573 bytes and 107 advertised files. Every basename/version/SHA-256/size/upload-
time tuple equals the earlier receiving inventory. There are no newly advertised
files in this observation. The summary `latest_version=0.12.0` is stale relative
to the file list and is not used as an availability decision.

Linux main 0.23.0 and staging 1.0.0 retain their original advertised identities;
the newest advertised files are dated 2026-10-08 and omit exact source Git
revisions. They are not newly qualified for this target. This metadata comparison
does not inspect or install package payloads, prove the absence of private files,
or establish a dependency closure/public release/platform qualification.

## Receiving boundary and next action

Request a complete owner-built wheel/Conda artifact covering ad67e0e, or an
explicit provider-supported composition with matching qualified native inputs.
Retain source revision, artifact SHA-256, version, platform/ABI, build profile,
native identity and dependency provenance. Keep native 4d8/ad67 source equality
separate from a claim that any particular binary was built from it.

No candidate wheel/prefix is produced by this inspection. Do not transplant
selected Python modules, reuse the mismatching old native, silently backport a
different provider tree or restart #642's interrupted construction. The
[original native-build interruption](e4_evidence_catalog_fix_2026-11-07.md)
remains held; its cache/source/artifacts and all old failures are preserved.
Refresh actual routine composition before future molecular receiving because
the shared environment changed after the previous diagnostic.

When a complete candidate is independently admitted, separately register and
execute the original complete reference selections and evidence-catalog
receiving under their existing controls. #558 generation correspondence/history,
#645 stored-H policy, #604 clustering, environment/canvas and public/minor gates
remain distinct. The complete Core/Extended/scientific/public/stabilization
objective #73 stays active and unproven.

## Actual resource and custody outcome

The inspection uses CPU 0, nice 10, one worker, a 13 GiB available reserve,
1 GiB group-RSS/2 GiB address-space/CPU 45 s/wall 60 s bounds. One 20 s/16 MiB HTTP request
and bounded Git subprocesses perform no scientific imports, molecular calls,
native compilation, package installation or remote CI. It completes in 11.183 s,
sampled peak group RSS 630,546,432 bytes, minimum available 59,787,382,784 bytes,
no resource interruption and a terminal owned group. The measured Git-object
peak exceeds the initial 256 MiB estimate but remains below the declared cap;
future similar inspections must use that actual observation.

Keep `.molsyssuite/provider-fix-artifacts-20261108`, including its approximately
464 MiB bare object store, under #50/review 2026-11-14. The store depends on the
preserved original provider object database; do not purge it independently.
The [primary manifest](data/provider_fix_artifact_admission_2026-11-08/manifest.json)
retains 19 compressed metadata/source/producer/resource records, 57,183 stored
bytes, SHA-256 `e3df5faaff6336e5b43f756c70ac0b2f8cbb92b7fac49afcfa6e0b1613dadc16`.
An independent stdlib reader authenticates their stored/decoded identities,
retained source Git blobs, recorded ancestry results, registry comparison and
terminal resource outcome. It passes in 0.103 s, sampled peak group RSS
4,202,496 bytes, without reexecuting ancestry or receiving an artifact.

The [reader/publication manifest](data/provider_fix_artifact_admission_reader_2026-11-08/manifest.json)
retains 17 records, 21,115 stored bytes, SHA-256
`9e08153e3f69a417ddbeed2bd12d54273ca8ff2feabff2d5f269a4a845561f02`.
Publication checks cover indexes, Ruff, formatting, shared resource and Conda
contracts, declared dependency routes, whitespace, exact records and maintained
links. The actual committed export separately checks resource/index/publication
contracts and qualified blob identities. The SDK is immutable
`95f693be10c9205ab9b912cb53453710a207bf45`; task-local receipts retain exact
check outcomes. Shared routine metadata is observed separately, without claiming
an unchanged or newly qualified scientific dependency closure.

This is documentation/record qualification only. Runtime, installed helpers and
historical scientific inputs stay unchanged; no molecular pytest rerun applies.
Exact-head hosted evidence remains missing under #28 and the maintainer's
`[skip ci]` route. These records do not establish provider/scientific/package
acceptance.
