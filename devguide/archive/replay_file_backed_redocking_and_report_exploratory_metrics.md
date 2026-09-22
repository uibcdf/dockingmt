---
summary: Replay file-backed redocking and report exploratory metrics
issue: uibcdf/dockingmt#10
status: resolved
opened: 2026-09-22
closed: 2026-09-22
verification: measured
area: [redocking, validation, provenance]
guard: tests/test_redocking_replay.py::test_file_backed_181l_manifest_replays_without_original_objects
normative:
blocked_by: []
supersedes: []
---

# Replay file-backed redocking and report exploratory metrics

## What

Demonstrate that one file-backed 181L redocking result can be saved as JSON,
loaded without the original Python objects, and rerun with its recorded problem
and Vina protocol. Produce a reviewable per-pose regression report.

## How

Reconnect a deserialized DockingResult to its serialized DockingProblem on
request, then use the existing VinaProtocol deserializer. Compare source and
PDBQT fingerprints, atom correspondence, scores, and mapped RMSDs with stated
replay tolerances. Report near-native rank, all pose RMSDs and named scores,
failure mode, and relevant provenance.

## Why

Gate C2 requires reconstruction from recorded configuration. The current 181L
test checks a provisional top-pose RMSD but does not reconstruct and rerun a
saved manifest or report per-pose outcomes.

## What is measured and what is assumed

**Inspected:** DockingResult.from_dict retains poses and dictionaries but drops
its in-memory DockingProblem; the constituent problem and protocol have
deserializers. The 181L file-backed source can be fingerprinted.
**Assumed:** Fixed seed and one CPU will produce results comparable within
modest score and RMSD tolerances; measure this before fixing those values.

## What was refuted

A single passing top-pose RMSD does not establish replayability or scientific
validity of provisional ligand/receptor chemistry.

## Scope and exclusions

One conventional rigid, file-backed case. Charge/typing validation remains
dockingmt#5. General multi-backend replay and a broad benchmark suite await
concrete accepted workflows.

## Acceptance criteria

- A JSON round trip can reconstruct the file-backed 181L problem and recorded
  protocol and run Vina again without retaining the original molecular objects.
- Replay checks source and submitted-PDBQT hashes and compares pose identity,
  scores and RMSDs using documented tolerances; changed files fail clearly.
- A report command provides per-pose metrics, near-native rank, failure mode,
  metric definition and provenance while labeling the chemistry exploratory.

## Dependencies and risks

Related local work: uibcdf/dockingmt#4, uibcdf/dockingmt#5.
Provider limitation uibcdf/molsysmt#234 prevents assuming in-memory molecular
objects can be serialized to H5MSM without losing partial charges.

## Resolution

`DockingResult.reconstruct_problem()` now reconnects a serialized result to
its file-backed problem. Reconstruction verifies recorded source fingerprints
and molecular selections before replay. The 181L command records a complete
result manifest, replays its recorded protocol, and reports the problem, input
and PDBQT hashes, code revision, per-pose scores and mapped RMSDs, near-native
rank and failure mode. It checks pose identity and uses explicit score and RMSD
replay tolerances. The selected pytest guard exercises the file-backed JSON
round trip and replay without retaining the original molecular objects; other
tests reject changed source content and altered recorded selections.

The [measured 181L baseline](../validation/181l_redocking_exploratory.md)
records four returned poses, a near-native rank of 1 at 2.5 Å, and zero replay
score and RMSD differences on a clean source revision. This remains
exploratory because preparation is still provisional under issue #5.
