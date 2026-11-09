# Native resource failures in offline audits

Owner: [DockingMT #95](https://github.com/uibcdf/dockingmt/issues/95).
Execution base: `7271667b35f8d95a5c5097a8ee604a45376b97e7`, with frozen
source/test changes. This is software qualification over existing saved records,
not a new molecular observation, installed artifact or scientific calculation.

## Correction and consumer guard

Three broad ordinary-error translators converted MemoryError to ValueError,
which the report validator classified as inconsistent saved input. The source
correction adds **three explicit MemoryError passthrough handlers**, six lines
in `core/audit.py` and `core/pose_audit.py`: length parsing/conversion, saved
scoring-protocol restoration and fixed reference-energy conversion. Removing
only those handlers recovers the exact original executable AST. No signature,
schema, validation rule, quantity conversion, exception class or default changes.

The [60-case public guard](../../tests/test_audit_resource_errors.py) exercises
15 applicable route/boundary combinations with MemoryError, KeyboardInterrupt,
SystemExit and ordinary ValueError. Nine combinations cover three unit-provider
operations across standalone, docking and scored-collection audits; two cover
protocol reconstruction; four cover reference quantity construction/conversion.
Each control verifies the clean report, injects one failure, checks exact native
exception identity or the original inconsistent-value report, and verifies the
unchanged input and recovered identical clean report after the injection ends.
No actual memory exhaustion is used. Native interruptions are not converted to
local catalog failures; ordinary malformed-value reports retain their meaning.

Original source receiving records **15 failures/45 passes**, all failures being
MemoryError that did not propagate. The final complete affected selection passes
**464 normal, then 464 pm/fs**, zero failures/errors/skips. Both profiles retain
one explicit deselection of the existing real-native scoring test, whose source
and assertions remain unchanged. That case is outside this offline source slice;
it is not marked passing. Complete selected modules are:

```text
tests/test_audit_resource_errors.py
tests/test_result_audit.py
tests/test_pose_audit.py
tests/test_scored_result_audit.py
tests/test_scoring_reference.py
tests/test_audit_coordinate_records.py
tests/test_audit_pose_identity_records.py
tests/test_result_record_admission.py
tests/test_pose_record_admission.py
tests/test_public_exceptions.py
```

The exact filter is
`-k 'not test_fresh_native_scoring_and_rescoring_produce_auditable_evidence'`.
All original test assertions, legacy report digests, ordinary field diagnostics,
record bytes/units/ranking semantics and the new guard remain unchanged between
red/final source snapshots. Existing reference-energy controls use detached
synthetic declarations over the legacy fixture; neither those declarations nor
the injected failures become new producer evidence for the original observations.

## Composition and independent receiving

Tests run with routine Python **3.14.10** and authenticated published Pytest
Receptor **1.2.2** in the existing private reporting prefix. Existing private
unyt 3.2.0/SymPy 1.14.0/mpmath 1.3.0 test support remains separately verified;
the shared Conda/editable environment is unchanged. The editable distribution
version label remains separate from actual source/hash/import attribution.
Both final runs retain two assertion-rewrite warnings from the already imported
reporting plugin; native JUnit, Receptor and process exit status agree.

Real molecular get/select/extract/convert/copy/set and viewer construction are
guarded, as are actual Vina/RDKit/OpenMM imports. None occurs. Caller unit
form/parser/standard units are preserved under normal and pm/fs policy. The
same two historical JSON fixtures, all existing tests and the full **594-input**
helper/data declaration retain exact hashes. Runtime inventory remains **67**
paths; this correction adds no runtime member, dependency or installed support.

| Frozen evidence | Members | Manifest SHA-256 |
| --- | --- | --- |
| [Primary](data/audit_resource_errors_2026-11-09/manifest.json) | 102 | `fca556fe4ef4ecc777f7f74c3ad3683d740db1a1b9a80a96db418b5f0d304982` |
| [Independent reader](data/audit_resource_errors_reader_2026-11-09/manifest.json) | 9 | `e75d9bad49db15a4e2f93f31553cdeafd98bf24cbb9f741d63e79b6443c8ce76` |

The reader verifies all source/test/fixture/tool hashes, red/final native and
Receptor counts, policy/resource outcomes, exact selection and the unchanged
native-test exclusion. It confirms only the three bare-raise handlers change
AST; every other frozen runtime/test/descriptor/fixture input remains exact.
It imports no DockingMT or molecular package and replays no test or calculation.

## Resources, final checks and limits

All cells use CPU 0, nice 10 and one native/build worker, with a monitored
**13 GiB available-memory reserve**, 1 GiB group RSS/2 GiB address space and
45 CPU/60 wall-second limits. Final cells take **13.501/13.602 seconds**, sampled
peaks below 140 MB RSS. All owned groups terminate without resource interruption
or live descendants. Sealing/independent reading uses the same bounded policy.

Final local qualification covers Ruff/format, indexes, shared resource and
publication contracts, whitespace, exact source scope and independent archive
receiving. A fresh committed-source export repeats applicable source/document/
resource/publication checks and verifies exact committed archive members.
Direct publication uses `[skip ci]`; no remote CI is dispatched. Required hosted
checks remain unreceived under #28, rather than passing by omission.

This closes #95's local source defect and strengthens Core C5. #19/#28/#73 stay
partial for their wider scopes; no new installed/public/platform/full scientific
or actual browser/comm/canvas acceptance follows. Earlier wheels keep their
original producers and qualifications and do not certify this later correction.
Respect the maintainer's #256 wait, #558 generation-map/history requirement and
the interrupted native-build hold. Advance independent accepted work or receive
the original owner handoff without substituting a different reference gate.

Retain `.molsyssuite/audit-memory-20261109` under #95/#19/#28/#50, review
2026-11-14. Preserve all original failures, private reporting/unit support,
previous installed receivers/wheels, migration directory, shared environment
and historical interrupted build. Committed records can be read without replay;
executable repetition needs the exact declared test tools and resource policy.
