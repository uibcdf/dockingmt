---
summary: Complete and qualify the existing MolSysViewer saved-result explorer.
issue: uibcdf/dockingmt#60
status: partial
opened: 2026-11-03
closed:
severity: medium
verification: measured
area: [viewer, results]
guard: tests/test_viewer_player_receiving.py
normative:
blocked_by: []
supersedes: []
---

# Saved-result addon explorer

## Public artifact boundary — 2026-11-04

[Public Viewer 0.24.0 build-1 receiving](../validation/public_viewer_receiving.md)
fails independently of the successful development-source checkpoint below.
Payloads/origins/closure pass, but actual addon selection reports 119 passes,
7 failures and 36 errors. Fresh public-provider probes confirm missing handle
readback and synchronous frame callbacks; initialization errors are retained for
triage. MolSysViewer #294 owns the additive public-file handoff. No downstream
substitute, changed source pin or numerical minimum is introduced. The saved-case
notebook stops before kernel launch/preparation. This proposal remains partial
for live frontend observation, which this public-artifact test does not replace.

## Public player notification receiving — 2026-11-03

[Current receiving](../validation/player_notifications_receiving.md) adopts
MolSysViewer `78ede79e`, delivered for #291, while keeping molecular-provider
pins and DockingMT runtime unchanged. Thirteen actual player/widget guards
cover immediate Python navigation/playback notifications, duplicate suppression,
lifecycle and failure boundaries. The old provider fails informatively; the new
selection passes 98 tests. Explicit readback remains covered independently.

The complete source-free installed suite passes **1,449 tests**, zero skips,
in 848.90 s, with all consumer/provider payloads and loaded origins verified.
It reuses the original SPDX consumer wheel from `50d8e33` and a distinct
qualification harness `1c34392`. The new five-cell real-kernel 3PTB companion
also passes immediate navigation assertions, preserving original science and
33 original files; its kernel is shut down. The provider blocker is removed.

This proposal remains **partial** for real frontend comm/controls/canvas and
visual C6 acceptance. No maintainer interaction is required now. Public
dependency minima and artifact/platform admission remain #30/#47. Historical
entries below retain their original provider and artifact identities.

## Shipped JavaScript exercised in a DOM — 2026-11-03

[The DOM checkpoint](../validation/addon_dom.md) adds 21 passing JavaScript
cases and six backend/module contract cases. The complete local Python selection
passes 78 cases without skips. Exact production `_esm` modules execute in isolated
jsdom contexts; panel actions, display meaning, updates and subscription cleanup
are checked. Production runtime and the original wheel/notebooks remain unchanged.
The sandbox launch failure and 20-pass/one-expectation-failure run are retained
before the corrected 21-pass result; no provider defect is inferred.

A separate `Addon DOM` workflow keeps the original scientific jobs/source pins
unchanged. Its one new reviewed workflow brings the inventory to ten routes,
with four scientific contexts preserved. MolSysSuite #161 owns review of a
reusable optional starter pattern. This remains DOM/model-double evidence:
real comm transport, provider callback delivery, rendered pixels and C6 remain
unaccepted. No maintainer interaction or public release is required now.

## Private installed-addon checkpoint — 2026-11-03

[Installed receiving](../validation/addon_installed_receiving.md) qualifies the
private wheel produced at `376679c`, including its actual addon discovery,
installed resources, **1,430 passing installed tests** without skips and five-cell real-kernel
3PTB companion. Only installation/origin/provenance checks differ from the frozen
source notebook; all later scientific/widget cells are identical. The receiver
is independent, dependency closure passes and task kernels are shut down.

The maintainer review remains deferred. No browser/canvas acceptance, C6, public
package or other platform follows. #291 remains provider-owned, and this proposal
stays partial. The original source/kernel evidence below is not relabelled.

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

At first-slice source `1c96052`, the selection of presentation, existing
addon/reference, score and reporting tests passes **104 cases**, zero skips,
on routine Python 3.14.7
(11.89 s; 26 existing legacy-H5MSM warnings). It includes 28 presentation cases
and real provider-built frame coordinates for scientific ranks `[7, None, 1]`.
Ruff lint/format, generated indexes, whitespace checks and Explorer ESM syntax
validation pass. Exact-head hosted CI is tracked separately on the issue.
The initial new-test
run had 26 passes and two failures caused by calling the wrong PyUnitWizard
policy-inspection API in the test. The corrected test uses the documented
`puw.configure.report()`. No provider defect is inferred.

### Panel state and owned visuals — second slice

Mounted widgets now refresh together after completed DockingMT actions, including
Python adapter calls and context actions. Each widget publishes its own
`explorer` or `domain` subrecord through public `set_state`, retaining the
supported direct messages. Initial/reopened panels read current public state.
Subscriptions use `on_frame_change` / `off_frame_change`; unmount/close detaches
only that widget. Widget references in the per-view runtime are weak.

Manual **Refresh**, workbench summaries and addon exports read `player.index`,
owned shape metadata and reference-region visibility from public APIs. A datum
being supplied is distinct from its visual being available. Missing visuals
disable their controls with an explicit prerequisite; provider query/action
failures remain errors. Domain state declares angstrom and angstrom**3, and the
frontend refuses other display-unit records rather than interpreting them silently.

Search-domain rendering records actual returned handles, validates geometry
before replacement and refuses caller-owned tag collisions. Clear/disable
deletes only still-owned handles, including renamed/custom-tag shapes; reused
tags are preserved. Failed deletion retains outstanding handles for retry.
Cleanup releases the result/reference/domain binding while leaving molecular
scene data in the Viewer. Loading a new result requires receptor/partner inputs
before any scene loading and does not inherit an omitted reference or old domain.
Scene loading remains a series of public provider calls, not a transaction.

The headless integration guard uses the public widget resolver and the same addon
classes to check their reactive namespace, selection,
domain visibility and cleanup. This is Python contract evidence, not an observed
frontend/canvas session.

The addon specification reports `dockingmt.__version__` instead of the former
hardcoded `0.1.0`; the existing contract test checks that identity.

The final routine selection passes **148 tests**, zero skips, in 16.77 s with
28 legacy-H5MSM warnings. It includes source fidelity, 20 new state/ownership
cases, real reference/reload guards and the administrative distribution controls.
A separate **51-case** addon/state/reference selection passes in 12.44 s with
the ordinary-installed qualified provider composition (28 legacy warnings).
That selection imports this source addon with the retained providers; it does
not qualify a new ordinary-installed DockingMT artifact. Ruff lint/format,
both panel ESM syntax checks, whitespace and generated indexes pass. Exact-head
hosted results remain separately recorded on #60.

### Original provider and distribution follow-up — historical

The original ordinary-installed Viewer probe at qualified `ca7ebea6` loads two
frames and registers a public callback. After Python `go_to_structure(1)`, the
index is 1 and the callback list remains empty. Current Viewer main `d72f93f7`
retains that implementation by inspection. The request for consistent public
Python-navigation notifications is
[MolSysViewer #291](https://github.com/uibcdf/molsysviewer/issues/291).
At that checkpoint, immediate notification after unrelated Python player calls
awaits the provider. The later
[notification receiving](../validation/player_notifications_receiving.md) at
`78ede79e` delivers and qualifies that behavior, including the real-kernel
companion and private installed suite. Preserve the original failed probe as
historical evidence; #291 is not a remaining implementation prerequisite.
There is no polling, player replacement or private-field observer. Unrelated
direct visibility edits are still read on mount/Refresh.

The first implementation head `1c96052` has a failing distribution job in
[CI 41689015547](https://github.com/uibcdf/dockingmt/actions/runs/41689015547/job/126102325478):
23 controls pass and the full-inventory guard detects the omitted
`_presentation.py`. Its earlier 104-case selection did not cover that gate.
The declared resource inventory now includes that module, `_scene.py` and
`panels/_base.py`. The unchanged administrative guards pass 24 cases with the
accepted immutable SDK; current source/CI receipts are recorded separately on
#60/#47. No old artifact or qualification is relabelled.

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
qualification. CI uses the unchanged controlled provider composition. That source
slice built no new wheel and established no release, platform admission or visual
acceptance. The later private-wheel qualification is recorded separately above.

## Acceptance criteria

The [new notebook](../validation/addon_3ptb_workflow.md) completes all five code
cells in a real kernel, checking actual saved-case coordinates/identity and
resolved Python widgets without a maintainer interaction. Its new receipts
retain the failed assertion attempt and successful correction separately. Each
attempt explicitly recreates the declared inputs; no new searches or energy
calculations occur. The result stays detached and all 33 monitored original
files are unchanged. Current export bytes differ and are not substituted into
the original execution. The kernel is shut down after capture; no browser is
connected. Actual frontend observation and the maintainer review remain deferred.

Data fidelity, addon-origin synchronization, explicit readback and ownership
guards are implemented. Immediate Python player notifications from MolSysViewer
#291 are also received at the qualified `78ede79e` source; that source/private
artifact evidence does not qualify a different public package. Keep this proposal
partial until:

- A live Jupyter workflow exercises table/navigation/reference/domain controls
  and observes the corresponding 3D scene using explicit molecular inputs and
  the retained public five-pose 3PTB case, in its original coordinate frame.
- The receipt records exact runtime/artifact identities and observed limits.
  Standalone HTML, Qt and popup-specific qualification remain distinct.

The historical scene review remains deferred under #52. Public delivery stays
#30/#47, and molecular recovery/reader limits stay with #4/#49/#33 and their
provider issues. Do not reinterpret these as addon blockers or accepted gates.
