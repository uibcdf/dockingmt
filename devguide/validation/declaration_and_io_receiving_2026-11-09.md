# Declaration ownership and file-I/O receiving

Owners: [#97](https://github.com/uibcdf/bindingmt/issues/97),
[#98](https://github.com/uibcdf/bindingmt/issues/98), broader #19/#28/#73.
Prospective registration 2026-11-09; baseline
`9b077fabf41e19ffdfb945bc7aa3fb6c53265e0f`.

## Accepted concrete boundaries

Retaining a prepared-input/problem declaration must not allow later editing of
that exported observation to change the live scientific input. Source inspection
finds live list/metadata aliases in both preparation exports and the problem
export/reader. This complements #25's earlier pose/result isolation. Detach those
existing Python record boundaries, preserving exact fields/schema/values, rich
metadata types/cycles/aliases within each snapshot and subtype behavior. Keep
explicit live receptor/partner sources borrowed and outside serialized/copied
payloads. Ordinary constructor borrowing stays unchanged. No chemistry validator,
molecular codec, generic model framework or JSON encoder is introduced.

Separately, an already identified regular file whose open/read fails must not
fall through to hashing its path as literal molecular text. Propagate the exact
original I/O exception, preserving MemoryError/process-control semantics, stream
chunking and successful hashes. Existing literal/nonfile detection stays within
its original scope; ambiguous failed stat/typed Path behavior is not expanded.
No retry, polling or input-format inference follows.

## Prospective receiving

Freeze/run the complete two new guard modules on the old implementation first;
retain failing cases and positive controls without relabeling them. Apply the
smallest consumer-owned changes, then run both complete affected selections in
fresh normal and pm/fs processes with identical test/code inputs. The final union
is the two new modules plus whole serialization, model/prepared-view argument,
input-resource, batch/outcome and result-record modules named in registration.
Only offline public operations and explicit provider stand-ins are admitted.
Real molecular conversion/geometry/search, Viewer construction and optional engine
imports are actively blocked. Source/file errors use tiny task-owned PDBQT bytes;
one 1 MiB+1 byte case verifies the existing chunk boundary, not a benchmark.

Preserve caller policies, schema-before-payload admission, exact source/module/
helper/tool bytes, original inputs and scientific producers. Verify executed
Pytest Receptor 1.2.2/JUnit agreement and complete outcomes independently without
replaying tests. The existing verified private test-only unit/reporting prefixes
are reused; no shared install or build. No new installed/public/platform/canvas/
hosted acceptance is inferred. Prior wheels retain their original byte identity.

Private task `.molsyssuite/plan-push-20261109`, owners #97/#98/#50, review
2026-11-14. Serial CPU0/nice10, native/build workers1; check available RAM before
each cell and monitor **13 GiB available reserve**, 1 GiB group RSS, 2 GiB address
space, 45 CPU/60 wall seconds. Expected RSS below256MiB. Slurm binaries exist,
no allocation; original bounded inconclusive applicability observation retained.
Do not automatically restart after headroom loss or increase limits to force a
pass. Preserve all failed/interrupted attempts and unreached gates. Final shared
resource/documentation checks repeat on fresh actual committed source; use
`[skip ci]`, with #28/#21 hosted evidence explicitly missing.

## Preserved old guard and collection amendment

The old runtime fails **61 of77** new cases (16 positive controls pass), with
no errors/skips. The first corrected-runtime affected selection fails collection
before test execution: batch tests import fixed PDBQT constants from the engine
test module, which eagerly imports a Vina-owning scientific helper. #99 owns
that local test boundary. Move only that helper import into its two actual
scientific users; retain all constants/helper/scientific assertions verbatim.
Explicitly deselect the existing two-parameter native batch comparison and
one native missing-file recovery case from this offline selection. They remain
mandatory in their original scientific/hosted scope; no native pass is claimed.
Fresh whole suffix-02 normal/pm-fs will receive the declared offline selection.

The initial harness unnecessarily pre-imports Pytest Receptor before pytest,
producing two assertion-rewrite warnings in the preserved red record. Let
pytest load its declared plugin normally in final cells; do not suppress warnings
or change the tests to disguise them. This is harness use, not a receptor defect.

## Reader-ownership refinement before final admission

The first complete corrected profiles and their independent receiving pass
518 cases per policy. Pre-publication review identifies a compatibility concern:
copying the entire problem input record also copies ignored extension payloads
and serialized receptor/partner payloads explicitly replaced by live arguments.
Those objects are not consumed by restoration. Three focused controls reproduce
this first correction's failure (fresh red-02: three failures/77 passes).

Retain that intermediate implementation, both 518-case profiles and their initial
122-member/13-member receiving. Narrow reader copying to one detached bundle of
only consumed constraints/guidance/metadata and both requested selections,
preserving aliases within that bundle. Explicit live arguments and unused
payloads stay untouched. All export, file-I/O, source, schema, fixture, native
exclusion and resource gates remain. Execute a fresh complete suffix-03
normal/pm-fs selection including those three compatibility guards before final
source acceptance; no headroom restart or scientific rerun is involved.

## Final source receiving and limits

Both final complete suffix-03 selections pass **521 tests**, with zero failures,
errors, skips or warnings and **three explicit unchanged native deselections**
each. Normal takes 5.322 s with 212,000,768 B sampled peak group RSS; pm/fs
10.640 s with 211,435,520 B. Minimum available memory stays above 60.4 GB. Every
owned group terminates without interruption; no actual molecular/provider
operation, engine import/execution, new scientific sample or shared install occurs.
The elapsed difference is an observation on a shared host, not a performance claim.

The final [200-member primary](data/declaration_io_final_v2_2026-11-09/manifest.json)
SHA-256 `2a8256eac8078a74a3fc9725fcb87cd75de3861d2a2af931bb583a2e25aaa554`
(1,667,253 stored/8,952,099 decoded bytes) and
[16-member independent reader](data/declaration_io_final_v2_reader_2026-11-09/manifest.json)
`f46a6c99f13a4c19a16117aa49445c06f617e471b62c47b5a7e3494605c176f4`
receive original 61-failure controls, the collection error, intermediate 518-case
profiles, the three-failure ownership refinement and final 521-case profiles.
Independent reading checks every stored/decoded/frozen digest, native JUnit and
complete published Receptor event integrity/counts, caller's active form/parser/
units and actual resource outcomes without replay. Provider fast-track alias
registration changes from empty to populated during normal import; it is recorded
and is not confused with a changed caller unit policy.

Executable AST changes are confined to five runtime functions: both preparation
exports, problem export/reader and the original file-fingerprint helper. Export
changes unwrap mechanically to the exact old dictionaries. The reader detaches
only consumed declarations; no ignored or explicitly replaced source payload is
copied. Engine-test AST is identical after removing only the relocated typing
imports, including all original scientific assertions and both literal fixtures.
All 594 shared helper/data inputs and 67 runtime paths remain unchanged in count;
no dependency floor, installation route, release candidate or hosted pin changes.

Retain the initial 121-member seal (`ae27a54f7ff1b9da4bc33a2f7e427f96438384cc1428e7f609e2bd1f79096735`),
initial 122-member receiving (`3a224885afefbe31412d90b145057e940058175513614b36b9fa4b63c49e4768`)
and 13-member companion (`44ce2d052cc51fb98312fe11f976af5da29e04d1b053c68c53d421c0111d5a9a`).
The first reused manifest envelope had an old E3-specific schema name; the next
seal corrects that task envelope and retains the previous controller before independent reading. These are
intermediate declarations, not acceptance of the final narrower reader. A local
sealing-controller indentation error is preserved with its source, before worker/
archive creation and with zero test/molecular replay. No historical scientific
input/result or prior immutable evidence is changed or reclassified.

This resolves #97/#98/#99 in their bounded source scope and strengthens CoreC1/C5.
The existing private wheel retains its original behavior/producer; these fixes
are not retroactively installed/public-qualified. #19/#28/#73, full scientific/
platform/canvas and required hosted #28/#21 evidence remain partial. The separate
[public inventory refresh](public_candidate_readiness.md#availability-refresh--2026-11-09)
finds no covering public MT/Viewer bytes. Next inspect the exact current hosted
source composition against received development APIs before a new CI checkpoint;
no provider build or CI is automatically launched. Panel #558 and actual canvas
#52/#60 retain their original holds.

## Publication checks

Seven final local gates pass: Ruff lint/format, generated reporting indexes,
shared support/resources, publication contract, whitespace and all five retained
archives/472 stored+decoded members plus exact final qualified source/test inputs.
A fresh export of the actual committed source must repeat the five applicable
quality/documentation/resource gates and archive/input authentication before push.
Full pytest/native/installed/platform/hosted matrices are not replaced by these
checks; #28/#21 remote evidence remains explicitly unexecuted under `[skip ci]`.
