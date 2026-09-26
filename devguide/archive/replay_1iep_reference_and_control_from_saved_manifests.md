---
summary: Replay 1IEP reference and control from saved manifests
issue: uibcdf/dockingmt#16
status: resolved
opened: 2026-09-26
closed: 2026-09-26
verification: measured
area: [validation, provenance]
guard: tests/test_1iep_replay.py
normative:
blocked_by: []
supersedes: []
---

# Replay 1IEP reference and control from saved manifests

## What

The public 1IEP validator records complete DockingMT results and captured Vina
PDBQT inputs for its reference and displaced-box runs. The original ligand SDF
and the source-to-PDBQT atom map live only in the report. There is no separate
process that reconstructs both runs from durable records and compares them.

## How

Capture the pinned SDF bytes, hash, source atom map, and source revision in both
result manifests. A replay command should verify those records and the PDBQT
payloads before docking, stage captured PDBQT bytes in a temporary directory,
reconstruct the recorded DockingProblems, and invoke the recorded Vina protocol.
Compare source identity, exact backend inputs, boxes, protocol, software
versions, pose count and identity, scores, pose coordinates, source-referenced
RMSD, and the control's near-native classification. State numeric tolerances.

## Why

This checks reproducibility after the original Python objects and input paths
are unavailable. It exercises DockingMT's result/provenance model with a
flexible ligand and a methodological negative control. The case-specific 1IEP
map remains temporary; general molecular correspondence belongs to MolSysMT
`uibcdf/molsysmt#223` and `#226`.

## What was refuted

Running the recorder twice while the source files remain in place does not
prove that the saved manifests contain everything needed for replay. A digest
without retained bytes does not reconstruct a missing source.

## Scope and exclusions

DockingMT owns this audit of its protocol, Vina adapter, results and provenance.
The externally prepared chemistry remains unassessed. The replay does not infer
general PDBQT chemistry or a graph mapping for another ligand.

## Acceptance criteria

- Both manifests contain authenticated SDF and PDBQT source bytes and one
  verified atom map.
- Replay succeeds in a new process without the original input paths.
- Source, protocol, box, pose and metric comparisons pass on a clean recorded
  revision under declared tolerances.
- Corrupt captured input, mismatched maps or changed protocol fail before or
  during replay with an actionable diagnostic.
- An addressable test protects the preflight and comparison mechanisms.

## Resolution

Both manifests now retain authenticated source SDF and Vina PDBQT bytes, a
verified source atom map, and the DockingMT source revision. The replay checks
their fixed identities, reconstructs both problems from temporary PDBQT files,
reruns the recorded protocol, and compares every pose under the declared score
and RMSD tolerances. A separate-process replay passed after all three original
input paths were temporarily unavailable. It returned one reference pose and
three control poses with zero measured score, coordinate, and source-RMSD
drift; the near-native counts remained one and zero, respectively. Altered SDF
or PDBQT bytes, one-sided and two-sided false maps, and a changed protocol were
rejected before docking. The public case and its limits are documented in
`devguide/validation/1iep_external_pdbqt.md`.
