---
summary: Pair docking reference frames explicitly and expose viewer failures.
issue: uibcdf/dockingmt#37
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: medium
verification: measured
area: [viewer, validation]
guard: tests/test_viewer_reference.py
normative:
blocked_by: []
supersedes: []
---

# Pose and reference loading

## What

Reference loading failures are suppressed, pre-existing trajectories are repeated,
and repeated result rendering adds duplicate complexes. The emerging provider
contract requires explicit pairing when composing trajectories.

## How

Prepare references through public MolSysMT operations, require one receptor frame,
replace the docking complex, pair reference frames by index when the public
MolSysViewer signature exposes that contract, and propagate loading/player errors.
Prevalidate references before scene mutation; do not promise multi-call rollback.

## Why

The existing redocking control can appear to succeed while its reference is absent.
Incorrect frame counts prevent meaningful pose/reference comparison.

## What was refuted

Do not catch TypeError and retry without pairing or interpret **kwargs as advertised
support. Do not duplicate molecular manipulation in DockingMT or migrate CI to an
uncommitted provider tree.

## Scope and exclusions

DockingMT adapter changes only. Provider handoff: uibcdf/molsysviewer#151.
The legacy signature branch is temporary until published pairing support is
qualified across supported profiles; review by 2026-11-03, owner DockingMT maintainers.
No browser rendering certification, chemistry change or provider source edits.

## Acceptance criteria

Public reference preparation, frame switching and reload behavior, observable
errors, existing native redocking, an executed notebook, and local gates pass.

## Measured outcome — 2026-10-03

The public addon operation `build_docking_reference_system` delegates copying
and static repetition to MolSysMT. The adapter replaces the molecular scene,
requires single-structure receptor/reconstructed poses and passes explicit
by-index pairing when advertised in the public viewer signature. Reference
and initial-player exceptions retain their original identity; failures produce
no render success event and do not publish a completed result.

The guard covers the original suppression and trajectory-multiplication
mechanisms, legacy/explicit/kwargs signatures, prevalidated reference counts,
source independence, declared time/box, pm/fs policy, reload and coordinate
correspondence with a real viewer. All 706 tests pass without skips in 133.23 s
against the unchanged Python 3.14 CI provider pins. The 32 focused integration
cases pass in 30.16 s against a frozen uncommitted viewer candidate. All four
notebook cells execute with each profile. See
[`validation/viewer_reference.md`](../validation/viewer_reference.md) for exact
source identities, digests, warnings and the evidence boundaries.

Provider handoff:
[MolSysViewer #151](https://github.com/uibcdf/molsysviewer/issues/151#issuecomment-5973771913).
No provider code or CI pin changed. MolSysMT's existing public extraction
already supports the required repetition, so no missing molecular-operation
issue was needed. Published viewer delivery and browser rendering remain
separate qualification tasks; the legacy visibility warning is retained.
