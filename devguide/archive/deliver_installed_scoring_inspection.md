---
summary: Inspect saved named-scoring evidence through an ordinary-installed public API example.
issue: uibcdf/dockingmt#75
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [examples, scoring, provenance]
guard: tests/test_pose_audit.py
normative:
blocked_by: []
supersedes: []
---

# Installed saved-scoring inspection for Extended E1

## What

Provide a standalone public-API example for a user holding a saved scoring pose
with multiple named evaluations. The existing source notebook requires the
repository/development environment. This slice supplies ordinary-installed
reading from an arbitrary directory, following #73's concrete E1 review.

## How

Use standard file/JSON IO with a caller-supplied independent SHA-256, then delegate
schema, record consistency, detached reading/roundtrip and captured-input checks
to `audit_pose`, `DockingPose` and `verify_captured_inputs`. Display scores and
original evaluation producers separately from the installed reader. Missing
evidence stays incomplete and contradictions refuse. Qualify the exact example
with the retained native software control, detached adverse profiles and a
deliberate source-overlay refusal,
using the existing private receiver without installing/upgrading it.

## Why

Saved rescoring evidence should be inspectable without a source checkout,
recomputing scores or implicitly converting a pose into a molecular system.
This is a practical next E1 workflow and exposes its provenance/interpretation
limits before a multi-pose rescoring study is designed.

## What was refuted

No new runtime reader/IO framework, scoring API, molecular operation or ranking
policy is required. Equal score units do not establish cross-method/pose
comparability. Do not strip input hashes or change descriptors to force ranking.
The historical control's producer is a dirty development version; a later
ordinary-installed reader must not relabel it as its own clean producer.

## Scope and exclusions

Reading/tutorial evidence only. Preserve #31/#34/#35, their fixtures and original
producers. No new preparation, native evaluation, docking, reconstruction,
RMSD, chemical assessment or viewer work. General molecular operations remain
MolSysMT-owned. Remote #74 qualification, public Conda delivery and visible
acceptance remain separate; this does not accept whole E1 or 1.0.0.

## Acceptance criteria

The exact standalone example must pass original/missing-capture receiving and
refuse wrong external identity/changed score evidence outside the clone with
ordinary-installed origins. Preserve file bytes, all 16 original scores, two
evaluation records, states/rank, assessment and producers; retain missingness.
Record actual reader/artifact identity, guarded external-call attempts, output
and input/example hashes, failures and relevant lightweight checks. The existing
pose-audit guard protects the delegated API; receiving qualifies the example.

## Completion — 2026-11-05

The [standalone example](../../examples/inspect_saved_scoring.py),
[installed guide](../validation/installed_scoring_inspection.md) and
[exact receiving receipt](../validation/data/scoring_inspection/receiving_2026-11-05.json)
deliver this bounded workflow. Five final isolated profiles pass their expected
outcomes: original consistent, missing capture incomplete, changed score/wrong
external hash/source-overlay reader refused. The private ordinary 0.1.0 reader
and all 63 payload files remain unchanged. All 16 original score values, labels,
two histories and historical dirty producer declarations survive. No guarded
molecular/native/render operation or optional-provider load occurs.

The initial private launcher's output-name collision and subsequent pre-child
missing-copy error remain explicitly invalidated diagnostics. Separate receipt
names and controller postchecks verify every final input after execution; no
original fixture or qualified environment was overwritten. The exact formatted
example hash is bound in the receipt. Local Ruff/index/reporting and final
workspace/committed-export controls remain required for publication handoff.
No new native tests or scientific campaign is needed for this reading-only change.

This resolves the installed inspection example, not whole E1 or cross-pose
rescoring/ranking admission. Those retain #73's declared workflow/comparison
boundaries and MolSysMT molecular ownership. Public/visual and #74 source-event
work remain separate. Small copies/unique diagnostics are held under #75/#50,
review 2026-11-12; no reader/controller/kernel/watcher remains running.
