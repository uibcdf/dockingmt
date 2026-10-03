---
summary: Score prepared fixed conformations independently of docking and preserve prior evaluations.
issue: uibcdf/dockingmt#34
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: medium
verification: measured
area: [core, engines, validation]
guard: tests/test_scoring.py
normative:
blocked_by: []
supersedes: []
---

# Fixed-pose scoring

## What

Provide public `score(problem, protocol=None, backend=None, pose=None,
score_name='score')` returning a `DockingPose`, and additive
`DockingPose.with_scores(scores, score_definitions=None)`.

## How

Use Vina/Vinardo's native `score()` on already prepared inputs. Preserve the
eight documented score components, empirical units, submitted-input hashes,
preparation assessment and evaluation history. Read input geometry through
public MolSysMT APIs. A prior pose must match submitted coordinates and known
state identifiers before attaching new scores. Validate names and descriptors
before execution and return a detached pose without changing the caller's data.

## Why

MVP E1 and issue #28 require scores to be independent of pose generation.
Provider improvements #221–#224 remain with MolSysMT's owners; this operation
can consume current prepared inputs without those changes or MolSysViewer.

## What was refuted

Importing Meeko, adding a new general scoring framework, silently replacing
scores, treating `Vina.energies()` and `Vina.score()` columns as identical,
or using optimization to implement fixed-conformation scoring.

## Scope and exclusions

One prepared ligand and rigid receptor, Vina/Vinardo. No automatic preparation,
AD4, flexible receptor, coordinate optimization, chemical qualification or
implicit ranking. Search-only VinaProtocol settings are explicitly recorded
as unused. A supplied pose must already correspond to the prepared ligand;
this operation does not rebuild a ligand from a pose.

## Acceptance criteria

Public behavior tests cover independent score attachment, native component
mapping, fixed coordinates, known state/geometry checks, failed-input cleanup,
non-default unit policy, optional dependency absence and serialization. An
executed notebook demonstrates a prepared control and additive rescoring.

## 2026-10-03 completion evidence

Implemented the two public operations and optional backend boundary, sharing
backend resolution and exact-input staging with docking. Prior geometry/state
and score meaning are checked before native setup. Vina/Vinardo's eight native
components, explicit units, preparation assessment and detached evaluation
history survive JSON pose roundtrips. No optimizer or search API is called.

The full local gate passes 595 tests without skips in 123.85 seconds on Python
3.14.7, Vina 1.2.7 and editable DockingMT in `molsyssuite@uibcdf_3.14`. The 31 new
behavior cases include native engine comparisons, flexible original 1IEP input,
exact byte snapshots, default provisional rejection, non-default quantity policy,
legacy adapter compatibility and cleanup on geometry/native/output failures.
The existing 27 provider warnings are unchanged. Ruff lint/format, report indexes
and diff checks pass. All four notebook code cells execute successfully with the
explicit Conda kernel and their retained outputs contain no errors.

The [contract](../validation/fixed_pose_scoring.md),
[notebook](../validation/fixed_pose_scoring.ipynb) and DMT-033 record the accepted
bounds. Qualification uses the unchanged CI provider/viewer source pins, preserving
live sibling worktrees. This resolves the bounded prepared-input scoring operation,
not chemical qualification, generic rescoring result audits, future methods or
issue #28's remaining architecture/scientific workload review.
