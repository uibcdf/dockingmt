# Resource failures in fixed-pose geometry — 2026-11-10

Owner: [BindingMT #107](https://github.com/uibcdf/bindingmt/issues/107), with
#73/#47 qualification and #50 custody. Source base a0c184f. Status: corrected and qualified in source.

The old installed helper diagnostic raises controlled MemoryError, OS ENOMEM
and ValueError through a fake provider facade. All three become ArgumentError;
the original resource objects remain causes. Its helper bytes match the source
base. Preserve that original observation separately from public red/green
receiving. No real allocation failure or molecular/native work is induced.

Add 16 public `score` controls across conversion, coordinate/name/element reading
and four error families: MemoryError, OS ENOMEM, ValueError and OS ENOSPC. Check
exact exception/cause/field, stopping before the next provider/native operation,
original input/protocol and owned staging-file retirement. The real engine is
unavailable to these controls; explicit software availability/construction seams
are intentional and never native execution. Expected original red result:
eight allocation failures incorrectly translated, eight ordinary controls pass.

Then add only MemoryError and OS ENOMEM passthrough before the existing geometry
argument translator. No string matching, generic OSError passthrough, new schema,
scientific definition, dependency or provider change. Run complete unchanged
original 139 input-resource cases plus 16 new guards (155) and all 48 pose-audit
cases, 203 total per normal/pm-fs policy, without exclusions or changed assertions.
The two actual native score calls per complete profile retain the original tiny
four/two-record inputs, 10-angstrom box, seed 17 and CPU 1. Existing bounded provider
geometry projection performs two conversions/six reads only in the fresh-score
node; all injected-error and remaining audit cases perform no actual molecular
or native calculation. Preserve generated labels separately from exact source
Git/overlay identity and observe real core origins before/after pytest.

Reuse the retained original Vina 1.2.7/103-file prefix and same six-provider
source/native cohort. Check all 788 frozen source/support inputs before/after;
606 support sources/declarations stay exact. No install, native build or source
refresh. Do not infer new artifact receiving from the old comparison wheel.

Each scientific cell remains serial CPU 0/nice 10/one worker, 13 GiB available-RAM
reserve, 1 GiB group RSS, 2 GiB address space, 60/65 CPU seconds and 180 wall seconds.
Estimate 768 MiB for complete profiles including the child process, 256 MiB for red;
the prior audit peak is below 493 MiB. Check reserve before launch, monitor owned
descendants during execution and retain every interruption. No automatic
headroom restart. No Slurm allocation; earlier applicability remains inconclusive.

Retain original diagnostic, source overlays/red/green/native observations and
independent readers under `.molsyssuite/scoring-geometry-resources-20261110`,
owners #107/#50, review 2026-11-14. Preserve earlier native/receiver/SDK custody and
human migration backup. Public/platform/hosted/interactive, SSH #100/#178 and
original provider-panel requirements remain separate; no remote CI is launched.


## Public regression and correction received

The public guard reproduces exactly eight original failures: MemoryError and
OS ENOMEM are translated at each of the four reads. All eight ordinary ValueError/
OS ENOSPC controls already pass. No actual molecular/native calculation or memory
exhaustion occurs in those controls. The original helper diagnostic remains an
observation of the old installed aeae47d module, not public/source fixed receiving.

The correction adds only an errno import, an explicit MemoryError passthrough
and OS ENOMEM passthrough before the existing ArgumentError translator. Public
signatures, scientific declarations, geometry tolerance, native parameters and
ordinary cause/field/code remain unchanged. Every new guard verifies exact error
identity/cause, expected provider-call prefix, no native construction, cleanup of
owned staging paths and unchanged caller problem/protocol snapshots.

| Attempt | Cases | Failures | Pytest exit | Actual native scores | Outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| red-01 | 16 | 8 | 1 | 0 | Expected original resource failures, eight ordinary controls pass |
| complete-normal-01 | 203 | 0 | 0 | 2 | Complete corrected source PASS |
| complete-pm-fs-01 | 203 | 0 | 0 | 2 | Same complete worker/source PASS |

Both complete profiles have zero errors, skips or warnings and no deselections.
They preserve 139 original input-resource and 48 original pose-audit cases plus 16
new controls. Their four actual score calls retain the original Vina/Vinardo
inputs/CPU/seed; fresh eight/sixteen-score histories and their internal audit pass.
Only the fresh native node performs the original bounded two-conversion/six-read
geometry projection. Injected-error controls use a private facade and fake engine
availability/construction, with zero actual provider/native operations. Original
process-control, unit policy and no-optional-provider child controls remain intact.

Normal/pm-fs wall 14.139/12.694s and measured child CPU 14.039/12.616s; source native
peak 517033984 B (below 494 MiB). Available memory remains at least 55361290240 B in
these profiles, with no resource interruption or surviving owned group. The
failed red is an ordinary expected test failure, not a resource interruption.
All 788 source/support/data hashes and 606 support declarations are checked;
no scientific fixture/provider/build/shared installation changes.

## Independent retained evidence

The [primary manifest](data/scoring_geometry_resource_errors_2026-11-10/manifest.json)
seals 119 members, 2267804 stored/7357063 decoded bytes, SHA256
`d2e171deee52e7d93c10827c217f81ee58fc582c12f5503123ea073a5ac499fb`.
The [reader companion](data/scoring_geometry_resource_errors_reader_2026-11-10/manifest.json)
seals 14 members, 19131 stored/49068 decoded bytes, SHA256
`a1b039b3ce855ba847a93265c889469f425c1114bedc1ac7e8d45c404e065b3e`.
Independent reading authenticates all compressed/decoded bytes, six qualified
source files, source-origin receipts, public red/green parameter populations,
old installed diagnostic and original/final source hashes. It checks actual
native inputs/vectors/extension maps, fresh public score/audit records and exact
provider-read witnesses without replay.

AST comparison recovers the exact original executable module after removing only
the errno import and two new passthrough clauses. All original test-module AST
nodes remain; the additions are four standard-library imports and one 16-case
parametrized guard. Red/green input dictionaries differ only in `_vina_scoring.py`;
both complete green workers and all frozen input hashes are identical. Three
native JUnit/Receptor sessions cross-check through verified private Receptor 1.2.2
without scientific imports. No failed population or unavailable evidence is hidden.

Core source origins are recorded before/after pytest. Actual generated package
label remains `0.0.0+297.g3b1853a`; source base a0c184f plus the exact overlay and
final committed-byte receiving identify execution, not that old label. No source
context verifier, remote or package metadata is rewritten. This does not establish
shared SSH source-context admission or a new installed consumer artifact.

#107 resolves in source. Next build/receive a genuine private consumer wheel
covering #106/#107 with the unchanged provider/native cohort, then run its new
resource guards and original native regressions through the shared installed
runner. A Python wheel build is separate from held native rebuilds; register its
own resource limits before execution. Preserve the old aeae47d file/observations.
Full #30/#47/#73, public Conda/closure/eight OS-minor cells, hosted/interactive,
SSH #100/MolSysSuite #178 and original panel/provider holds retain their owners.

## Local closeout

Run Ruff lint/format, report indexes, final shared resource validation,
release-contract structure, whitespace and archive/qualified-byte checks. Retain
applicable administrative evidence and repeat source/archive/resource checks on
a fresh actual committed export before push. Skipped CI is missing hosted
evidence; no manual remote workflow is dispatched automatically.


Final source closeout passes Ruff lint/format, indexes, shared resource/release
contracts, whitespace and archive/qualified-byte checks. The import-blocked
administrative suite passes 29 cases and 5 subtests, zero errors/skips/warnings
(native JUnit 34 including subtests). Final committed-export receiving remains
required before push; retain its exact commit receipt. MolSysMT #521/#558 and
MolSysSuite #178 remain open on the final 2026-11-10 review; no provider intake is
claimed from issue status alone.
