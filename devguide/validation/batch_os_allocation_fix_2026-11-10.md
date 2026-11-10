# Recorded-batch OS allocation errors — 2026-11-10

Owner: [DockingMT #106](https://github.com/uibcdf/dockingmt/issues/106),
functional/resource owners #73/#50. Source base 85d91c1. Status: corrected and qualified in source; no new installed artifact.

The original ordinary installed aeae47d diagnostic raises pre-created errors,
not a real allocation failure. MemoryError propagates as the same object after
first/bad; OSError(errno.ENOMEM) records failure and visits third. ENOENT records
and continues as intended. Preserve that observation and original wheel; it is
not receiving of the source correction.

Add two policy cases for OS allocation failure, preserving exact exception
identity, first outcome, unconsumed next item and caller-owned source. Add two
recording controls for ordinary ENOENT/ENOSPC errors. Receive an expected failing
record-policy case before changing runtime code, then correct only ENOMEM
classification. No string matching, generic OSError passthrough, schema or
dependency change is admitted.

Run the entire updated 45-case batch module normal then pm/fs, with all 41 original
cases and assertions retained. Native work remains ten tiny searches per policy,
the same four/two-record PDBQT, seed 123, CPU 1, exhaustiveness 1 and 10-angstrom box.
Use the unchanged retained engine and six-provider cohort. Source origins and
overlay hashes are explicit; no new wheel/install/public artifact is claimed.

Each cell is serial CPU 0/nice 10/one worker, 13 GiB available-RAM reserve, 1 GiB group
RSS, 2 GiB address space, 60/65 CPU seconds and 180 wall seconds. Expected native
peak 768 MiB, red control 256 MiB; prior whole-module peak is below 452 MiB. The
registered monitor checks RAM before launch and during execution, supervises
owned descendants and preserves every interruption. No automatic headroom
restart or native build. Slurm has no allocation; earlier applicability check
was inconclusive. Retain original programs, overlays, outcomes and original
diagnostic under `.molsyssuite/batch-os-allocation-fix-20261110`, owners #106/#50,
review 2026-11-14. Original runtime artifacts and scientific fixtures stay intact.

Full/public/platform/hosted/interactive and SSH-source-context gates retain their
separate scope. No remote CI, shared environment or provider changes are needed.


## Correction and complete source receiving

`dock_many` now propagates the same `OSError` object for errno.ENOMEM under
both policies. All other ordinary item errors keep their prior recording rule;
MemoryError and process-control handling remain unchanged. The two new allocation
cases preserve the first outcome, stop before the third source item and leave the
borrowed source available to its caller. The two ordinary I/O controls retain
recording and continuation for ENOENT/ENOSPC.

| Attempt | Tests | Failures | Pytest exit | Actual native searches | Outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| red-01 | 0 | 0 | 4 | 0 | Source-relative selector admission error; not a regression result |
| red-02 | 1 | 1 | 1 | 0 | Expected original DID NOT RAISE failure |
| batch-normal-01 | 45 | 0 | 0 | 10 | Complete corrected source PASS |
| batch-pm-fs-01 | 45 | 0 | 0 | 10 | Same exact worker/source pair PASS |

Both complete source profiles have zero errors, skips or warnings and preserve
all 41 original declarations/bodies/assertions plus four new cases. Native calls
remain unchanged; prior positive result-equivalence and missing-file recovery
checks pass. The source driver checks explicit source import before pytest and
all 372 frozen runtime/test/helper inputs before/after. All 606 support sources
also match their unchanged declarations between policies and after the pair;
this is source validation, not installed support staging/retirement.

Actual source package label is `0.0.0+297.g3b1853a` in this development interpreter.
It is a retained generated label, not the execution source identity. Source base
`85d91c1d98bbac83988e5d9274b36753a5fc29eb` plus the exact frozen overlay, and the
final commit's qualified-byte check, identify the executed implementation. Do not
infer its source from that old label or from the aeae47d comparison wheel. No
version metadata, installation or original result producer is rewritten.

Native source peak group RSS is 468860928 B (below 448 MiB), normal/pm-fs wall time
14.621/29.137 seconds and measured child CPU 14.483/14.596 seconds. Each original
source case uses one CPU and its original fixed inputs. Available memory stays
above 59162869760 B in the passing pair. All owned groups terminate; there is no
resource interruption or native-build/shared-environment change.

## Independent evidence and explicit metadata limit

The [primary manifest](data/batch_os_allocation_fix_2026-11-10/manifest.json)
seals 257 members, 2808473 stored / 9298899 decoded bytes, SHA256
`42415a24d7ae876d66d0b5c296c1242dd4d0cc2ce5a763877390c82dd0e0f3ab`.
The [reader companion](data/batch_os_allocation_fix_reader_2026-11-10/manifest.json)
seals 20 members, 26018 stored / 64386 decoded bytes, SHA256
`b78caf987102033026a7ca81c6d3c3ec3753383f0e5376ff7178d4166c2daf13`.
Both preserve the original ordinary-installed diagnostic and its actual outcome,
source admission/regression failures, exact overlays, original test ASTs, native
maps/input/output identities and actual JSON exports. Old installed errors remain
observations of old bytes, never reclassified as corrected-wheel receiving.

The first independent reader fails on an empty serialized `source_origins`
dictionary. The driver did execute its explicit core-source import assertion,
but a recorder replacement left the later origin field empty. This unavailable
post-execution metadata is retained explicitly; no replacement field or recovery
claim is manufactured. The corrected reader authenticates the executed import
assertion, source hashes and all original receipts while marking post-execution
serialized origin availability false. This source receiving does not establish
shared SSH source-context admission or a new ordinary installed prefix.

The reader also proves every old top-level test AST node is retained and the
only additions are the errno import and two parametrized tests. The red/green
source-input dictionaries differ only in batch.py; both complete green workers
and frozen source dictionaries are byte-identical. Four JUnit/Receptor streams
cross-check through verified private Receptor 1.2.2 without scientific imports or
molecular/native replay. Failed reader/admission attempts remain archived.

#106 resolves in source. Next register complete original pose-audit receiving,
including its fresh-native scoring node. Receive #106 in a genuine future
consumer artifact under #47; the old aeae47d installation remains unchanged and
is not certified for this fix. Full #30/#47/#73, public/platform/hosted/interactive,
SSH #100/MolSysSuite #178 and scientific-panel/provider holds retain their owners.


## Local closeout checks

Ruff lint/format, report indexes, final shared support-resource validation,
release-contract structure, whitespace and archive/qualified-source checks pass.
The separate import-blocked administrative selection passes 29 cases and 5
subtests with zero errors/skips/warnings (native JUnit 34 including subtests).
Before push, repeat source/archive/resource checks on a fresh actual committed
export and retain its exact commit receipt. Neither these local checks nor
`[skip ci]` replace missing hosted/public-delivery evidence.
