# Inspect saved scoring evidence with an installed reader

Owners: [DockingMT #75](https://github.com/uibcdf/dockingmt/issues/75) and
[#77](https://github.com/uibcdf/dockingmt/issues/77), bounded follow-ups to the
Extended E1 review under #73. The standalone
[example](../../examples/inspect_saved_scoring.py) reads a caller-supplied
DockingPose JSON file by default, or a DockingResult collection with an explicit
record-kind choice. It uses existing public APIs. Copy it and your input to any
directory with a compatible ordinary-installed DockingMT environment available.

```bash
python inspect_saved_scoring.py saved_pose.json --sha256 INDEPENDENT_EXPECTED_SHA256
python inspect_saved_scoring.py saved_result.json --record-kind result --sha256 INDEPENDENT_EXPECTED_SHA256
```

Obtain the expected digest from your trusted source. The example matches the
file bytes before interpreting JSON. Computing a new expected digest from an
untrusted replacement does not authenticate its history. The reader must have
matching module/distribution version and origin; editable/source-overlaid
readers are refused. This is a reader check, not a complete dependency audit.

The worked input is the existing
[two-evaluation software control](data/audit/minimal_scored_pose.json), with
independently retained SHA-256:

```text
970f516aadc19d6e5df8b5f7e930a7c8b7c239ab603f4e9f6d74769beb095723
```

Its receptor and ligand deliberately overlap. The two Vina/Vinardo evaluations
and all 16 native score components already exist; this example never recalculates
them. Preparation remains unassessed, and its state labels are control
declarations rather than independently verified chemical identities. It is not
a binding-prediction example. The original [pose audit](pose_audit.md) and
[scoring contract](fixed_pose_scoring.md) retain their original evidence.

## Reading and interpretation

The example calls `audit_pose`, reads with `DockingPose.from_dict`, checks an
independent canonical roundtrip and uses `verify_captured_inputs` when both
captured inputs are present. It emits a compact JSON summary containing:

- The current reader identity, independent file digest and aggregate audit.
- Pose/state labels and rank, retaining unknown values.
- Every named score with its recorded method, component, kind, unit and advisory
  direction. Missing descriptors stay unknown; no units are guessed or values
  compared across methods.
- Each evaluation's original DockingMT/MolSysMT/backend version labels,
  captured-input integrity/byte counts and recorded preparation assessments.

Full contexts and captured bytes stay in the unchanged input rather than being
copied into the summary. Contradictions cause a nonzero exit and list their
bounded audit paths/reasons. Missing evidence remains `incomplete` and unavailable;
the example does not fabricate it. Ordinary schema/quantity refusals retain the
public SMonitor diagnostic code when the reader raises `CatalogException`.
No private exception type is imported.

The historical producer label is **`0.0.0+101.gbe39d74.dirty`**, with MolSysMT
`0.22.4+24.g42b487869` and Vina `1.2.7`. The new reader is a separate identity.
A dirty version string is not an authenticated exact source/build record; the
example does not recover or certify the historical software bytes.

Record consistency and captured-byte integrity do not establish molecular
coordinate correspondence, chemical validity, score correctness, comparability
or binding affinity. Molecular inspection, conversion and reconstruction remain
MolSysMT-owned and are not invoked. No preparation, native scoring, docking,
optimization, RMSD, ranking or viewer operation runs.

## Executed private installed receiving — 2026-11-05

The [receiving receipt](data/scoring_inspection/receiving_2026-11-05.json) binds
the exact formatted example, original/derived inputs and final outputs. Five
serial, isolated Python profiles run outside the clone with one logical CPU,
low priority, single native-library threads and monitored RAM headroom:

| Profile | Actual result |
| --- | --- |
| Original saved control | Audit consistent; 16 scores, both evaluation producers, labels/rank, canonical roundtrip and both captures preserved/verified. |
| First evaluation's partner capture removed on a detached copy | Audit incomplete; that capture unavailable and the second evaluation still verified; original scores and histories retained. |
| Current `vina` value changed while its historical evaluation stays unchanged | Exit 1; audit reports `claims_disagree`. |
| Wrong independently expected file hash | Exit 1 before JSON interpretation. |
| Deliberately source-overlaid reader in an isolated negative child | Exit 1; the ordinary-installation boundary refuses it. |

The positive reader uses retained Python **3.12.16**, ordinary private DockingMT
**0.1.0**, wheel SHA-256
`fbe3591068d9633ae0066ab3dcd593508f7fc31d86eefad01975fd4e4bb71752`.
It reuses the qualified [private minor composition](data/source_0_1_0_2026-11-05/source_minor_matrix.json)
without an install, upgrade or new environment. All 63 consumer payloads and
loaded core/support/provider origins verify before/after; the negative overlay
is explicitly separate from those positive origin claims. The qualified
consumer's 63 payload files and original input remain intact. This is not a public
installation recipe or a new full-suite qualification; public delivery stays
#30/#47.

Validation permits the required MolSysMT bootstrap import, then guards its
molecular operations and DockingMT preparation/execution/reconstruction/render
calls, plus optional engine/Viewer/RDKit/OpenMM loads. No guarded work is
attempted. The exact example runs without a source/data harness or SDK import;
only the explicit input file is copied. All final input digests are independently
checked after the controller exits. No process, kernel, server or watcher stays
active.

An initial private launcher used a receipt filename that overwrote its own input
copy after the within-example checks. A subsequent launch stopped before a
child because that copy had been archived. The original repository fixture and
qualified prefix were untouched. Distinct receipt filenames and independent
postchecks correct the launcher; the five final profiles above use the final
example bytes. Earlier attempts remain diagnostic history and are not counted
as additional scientific cases or a product defect.

## Explicit collection mode — 2026-11-06

`--record-kind result` selects `audit_result` and the `DockingResult` reader.
The default remains `pose`; there is no record-kind inference. The selected
kind requires its identifying payload key before model reading, so a pose
cannot silently become an empty result. Saved collections carrying per-pose
scoring histories require the [#76 corrected reader](result_audit.md#collection-scoring-history-receiving--2026-11-05).
The fixed private 0.1.0 candidate predates that correction.

The collection summary adds stored pose order/indices, original ranks, recorded
ranking policy/history, and original docking-producer/capture information.
Each pose retains the existing score/evaluation summary. Missing collection
provenance is not filled from an evaluation: unknown producer values remain
`null`, missing captures stay unavailable, and the audit lists incomplete
paths/reasons. Missing score descriptors leave units/methods unknown. No ranking
is executed and no comparison context is changed. Full original contexts,
ranking observations and captured bytes remain in the input.

The [separate #77 receipt](data/scoring_collection_inspection/receiving_2026-11-06.json)
binds exact example revision `b87eb08` and the unchanged #76 private reader
wheel SHA-256 `6f61287017cc0c545e1b80c2997ef3b89361201fde92dbc2eed4005770dc41f3`,
actual version `0.0.0+unknown`, Python 3.12.16. A small borrowing installation
uses the retained qualified dependency base; it is not a newly solved/public
closure. All 63 reader runtime payloads remain equal to that wheel before/after.
The original 0.1.0 base consumer and #75/#76 receipts retain their identities.

| Receiving invocation | Observed result |
| --- | --- |
| Previous and revised default pose examples, same reader/input | Both exit 0 and emit equal JSON summaries. |
| Original two-pose native docking result | Consistent; stored order/ranks, original producer, ranking history/order and capture integrity retained. |
| Collection constructed from the original two-evaluation pose | Incomplete for absent collection provenance; all 16 scores/two original evaluation producers retained. |
| First evaluation capture removed on a detached copy | Incomplete; first capture unavailable, second verified. |
| Docking score descriptors removed on a detached copy | Incomplete; score units/methods remain unknown. |
| Empty result | Incomplete, zero poses; no invented producer or ranking. |
| Changed current score; future scoring-history schema | Each exits 1 with audit contradictions. |
| Wrong independent digest; either explicit record-kind mismatch | Each exits 1 before model interpretation. |
| Deliberate source overlay in a separate fresh child | Exits 1 through the ordinary-installation refusal. |

These are 13 invocations including the previous-example comparator: seven
successful reads and six expected refusals, not 13 molecular cases or a pytest
suite. Exact standalone example runs are sequential outside source, without a
test/data harness or SDK import; the deliberate overlay is isolated separately.
Required MolSysMT bootstrap is permitted, while molecular/preparation/native/
reconstruction/ranking/viewer operations and optional native/viewer imports are
guarded. Zero such attempts occur. Parent postchecks verify every input after
execution. Local work uses one logical CPU, low priority, single native threads
and monitored RAM reserve; the receiving finishes without resource interruption.

The two-evaluation collection is built through the public `DockingResult`
constructor from the unchanged saved pose. Other variants are detached record
mutation controls; their byte hashes and derivations are recorded in the receipt.
No new molecular result, evaluation or identity is produced. The example uses
Argparse for its CLI and delegates scientific record/quantity admission and
diagnostics to the existing public APIs; it adds no runtime dependency or helper.

## Remaining E1 boundary and custody

This delivers installed saved-scoring inspection, not whole-E1 acceptance.
The existing score/attachment/ranking APIs and their original native/software
evidence remain separate. A representative multi-pose rescoring/ranking study
still needs its declared preparation/comparison context and execution scope.
Different submitted pose bytes can yield different descriptor hashes; do not
strip hashes or edit descriptors to force ranking admission. General molecular
identity or pose-to-prepared-input needs belong to MolSysMT, with provider work
still deferred. No new molecular campaign is registered or executed here.

The new #77 borrowing environment and disposable example/input copies are retired
after handoff. Unique receipts, launcher and diagnostics remain for review on
2026-11-12; no local controller, test, kernel, server or watcher remains active.
The reused #76 wheel and qualified base retain their original custody.

Earlier small input/example copies, raw diagnostics and receipts belong to #75/#50,
review **2026-11-12**. Retain unique evidence through handoff and retire disposable
copies at that review. Preserve original records, private wheels/receivers and
shared environments. Scientific/public/visual acceptance and #74 remain distinct.
