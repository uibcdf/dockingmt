---
summary: Complete and qualify the existing MolSysViewer saved-result explorer.
issue: uibcdf/dockingmt#60
status: partial
opened: 2026-11-03
closed:
severity: medium
verification: measured
area: [viewer, results]
guard: tests/test_viewer_presentation.py
normative:
blocked_by: []
supersedes: []
---

# Saved-result addon explorer

## What

Complete the existing `molsysviewer_dockingmt` workspace as a faithful explorer
of saved results, then qualify its actual controls in live Jupyter. The human
accepted this bounded plan after comparing the MolSysMT, ElastNetMT,
PharmacophoreMT and TopoMT addons. Source references and the complete acceptance
criteria are retained in [#60](https://github.com/uibcdf/dockingmt/issues/60).

## How

The first implementation separates collection/frame index, one-based display
position, optional scientific rank and optional pose identity. The panel sends
zero-based indices; the existing Python `set_active_pose(view, rank)` argument
and `runtime.active_pose_rank` retain their legacy one-based position meaning.
The new read-only `runtime.active_pose_index` exposes that mapping explicitly.
No result order or scientific rank is changed.

Explorer rows, selected-pose summaries and the addon export use the same detached
presentation records. Each score carries its name, scalar value, declared unit
and existing scientific descriptor. Undescribed scores remain unknown, including
scores named `vina`. The workbench distinguishes top-pose scores from the
selected pose; the compatibility scalar `top_score` contains only a real Vina
value, including zero, or `None`. Other metrics are available in `top_scores`.

Mounting, refreshing and navigating no longer compute RMSD. No recorded
comparison is currently bound to this presentation, so the panel states that
RMSD is unavailable. The public scientific evaluation API remains available
separately. A later comparison action needs explicit correspondence, reference,
frame, policy and unit attribution, with molecular operations in MolSysMT.

The final source selection of presentation, existing addon/reference, score and
reporting tests passes **104 cases**, zero skips, on routine Python 3.14.7
(11.89 s; 26 existing legacy-H5MSM warnings). It includes 28 presentation cases
and real provider-built frame coordinates for scientific ranks `[7, None, 1]`.
Ruff lint/format, generated indexes, whitespace checks and Explorer ESM syntax
validation pass. Exact-head hosted CI is tracked separately on the issue.
The initial new-test
run had 26 passes and two failures caused by calling the wrong PyUnitWizard
policy-inspection API in the test. The corrected test uses the documented
`puw.configure.report()`. No provider defect is inferred.

## Why

The old table selected rows by scientific rank while the player selected frames
by collection position. Missing ranks were fabricated from position. The old
workbench also replaced a legitimate Vina zero through boolean fallback, and
arbitrary score values were labelled kcal/mol. The current guards exercise those
failure mechanisms, score-definition detachment, non-default pm/fs/kJ/mol policy,
invalid selections, provider refusal and independent view state.

## What was refuted

A new renderer or workspace scaffold is unnecessary: DockingMT already ships
the addon entry point, workspace, widgets and adapters. Other scientific addons
provide architectural examples, not new dependencies. Widget action tests and
JavaScript syntax validation establish no live frontend/canvas acceptance.
Captured backend files and detached results do not establish complete molecular
inputs. No molecular reconstruction belongs in the presentation layer.

## Scope and exclusions

All runtime changes are in the DockingMT-owned addon. MolSysViewer owns the
generic host, lifecycle, transport and rendering; MolSysMT owns molecular
conversion, selection, correspondence and coordinate work. No provider pins,
package metadata, scientific algorithms, result schemas, historical receipts,
preparation, energy calculations or searches are changed.

The shared development environment retains unrelated dependency-closure
conflicts; this source test selection is not an ordinary-installed artifact
qualification. CI uses the unchanged controlled provider composition. No new
wheel, release, platform admission or visual acceptance follows.

## Acceptance criteria

The first data-fidelity slice is implemented. Keep this proposal partial until:

- Panel state coherently reflects public Python/context actions and actual
  player changes across navigation and remounts. Inspect the supported host
  notifications before implementation; provider gaps get owning issues.
- Missing molecular inputs and unsupported/provider-failed actions have explicit
  prerequisites and diagnostics. Teardown affects only owned visuals.
- A live Jupyter workflow exercises table/navigation/reference/domain controls
  and observes the corresponding 3D scene using explicit molecular inputs and
  the retained public five-pose 3PTB case, in its original coordinate frame.
- The receipt records exact runtime/artifact identities and observed limits.
  Standalone HTML, Qt and popup-specific qualification remain distinct.

The historical scene review remains deferred under #52. Public delivery stays
#30/#47, and molecular recovery/reader limits stay with #4/#49/#33 and their
provider issues. Do not reinterpret these as addon blockers or accepted gates.
