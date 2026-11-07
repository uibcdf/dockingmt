# Viewing an admitted pose interaction binding

Owner: [DockingMT #80](../pending_proposals/receive_docking_interaction_analysis.md).
Registered source increment before execution, starting at `d71fd6b`.
Implementation and qualification were unproven at registration. The route is
now implemented with passing source/DOM qualification below and separately
[received on its exact installed candidate](e4_pose_interaction_view_installed_2026-11-07.md)
normal/pm-fs. Actual comm/canvas, public delivery and whole E4 remain unproven.

## Public route

```python
# binding already identifies the original pose and its admitted full carrier.
viewer = dmt.view(binding)
query = viewer.interactions.query('hbonds', structure_indices=[0])
```

The existing binding operation supplies `PoseInteractions`. Opening it retains
the complete original result in `viewer.addons.dockingmt.result`; it does not
make a one-pose replacement result. Original position, pose ID and scientific
rank stay distinct. Python/context navigation rejects positions without loaded
geometry before asking the player to move. The ordinary result renderer remains
the route for a reconstructed multi-pose trajectory.

Provider interaction visuals are created for each stored name and only local
frame 0. The Explorer shows current evaluated/unevaluated/unavailable states and
occurrence counts from public provider metadata. Counts are observations, not
affinity or proof of biological absence. Filtering, typed analysis access and
molecular persistence remain provider APIs. The addon summary/export carries
the original association inspection snapshot and compact live display metadata,
not a replacement complete molecular/analysis codec or authenticated producer.
Replacing the loaded system disables this geometry association, even if the
new system has matching counts. The original result remains available for
inspection. Cleanup failure retains handles for explicit retry; unrelated
Search Domain inspection does not depend on interaction metadata succeeding.

## Concrete workflow and ownership

The existing result renderer builds one structure per original pose from
receptor/partner sources. The admitted saved interaction carrier has one
structure, possibly another atom/H representation, and no correspondence to
that multi-pose scene. Never substitute it into that scene or replicate its
observations over four unevaluated poses.

Provide the explicit `dmt.view(binding)` route for a `PoseInteractions` produced
by the existing public binding operation. Load its complete detached carrier
through public MolSysViewer replacement loading, preserving all named analyses.
Create provider-owned interaction visuals with public `view.interactions.add`;
MolSysViewer owns rendering, geometry, filtering and current-frame projection.
No detector, matcher, preparation, geometry edit or analysis codec is introduced.

Keep the complete original `binding.result` in the addon, including every
original pose/score/rank/provenance. Scene frame 0 maps only to
`binding.pose_index`, even when that is collection member 3 or later. Explorer,
frame callbacks, summary/export and Python/context actions must agree on this
mapping. The complete pose table remains visible; unavailable geometries have
an explicit reason and disabled navigation. No other original pose becomes
evaluated. This bounded route does not replace the wider product requirements
for multi-pose interaction exploration.

The binding already selects a pose and complete carrier. Conflicting result,
problem, receptor, partner or reference inputs and a nondefault `pose_rank` are
refused before view creation/mutation. The ordinary result/problem/domain routes
retain their current behavior. An explicit search-domain visual may coexist
because it changes no molecular axes. Forwarded provider `skip_digestion` must
not bypass owned options. The default rank argument is not used to reselect the
bound pose; original scientific rank remains independent of position.

Read live analysis metadata from public MolSysViewer APIs, preserving evaluated-
empty versus unevaluated coverage in the panel. Keep the public loaded-system
handle as the scene association: replacing/adding/editing the system invalidates
this association when the handle changes. Do not trust matching counts, a label,
or an unrelated frame event. Direct mutation of the public inspect-only
`view.molsys` handle is outside MolSysViewer's documented editing contract.
Failed provider operations propagate; several calls are not a transaction.

Owned cleanup during clear/disable/re-render removes only interaction visuals whose
current public registry identity matches the retained handle. Scientific named
analyses and foreign visuals survive clear/disable. Explicit replacement loading
retains the provider's whole-scene replacement semantics. Preserve cleanup handles on a deletion
failure. Publish completed result/binding state only after required provider
calls succeed, while retaining ownership of partially created visuals for cleanup.

## Source qualification registered before running

Use protocol doubles for complete carriers, provider load/analysis/layer APIs
and controlled failures. Construct synthetic binding records explicitly; they
are not native molecular or installed-artifact qualification. Test a nonfirst
bound collection member, full result preservation, frame callbacks/readback,
source detachment, live coverage, replaced scenes, unavailable navigation,
conflicting inputs, missing capabilities, provider errors and visual ownership/
cleanup failures. Keep ordinary view/result/presentation/state regressions.

Run the new module plus applicable interaction-binding, view-argument,
presentation/state and frontend-protocol modules with the routine Python 3.14
interpreter and `pytest --receptor=llm`. Record the exact collected selection,
native pytest completion/JUnit/artifacts and actual exit status; known Pytest
Receptor #46 compact counting cannot replace native events. Forbid real
molecular operations and Vina import in this source selection. Preserve every
failed attempt; an exit without complete receipts is not a pass.

Run scientific/source qualification serially on CPU0/nice10, one native/build
worker, with 8 GiB available-RAM reserve, 1 GiB group RSS, 2 GiB address space,
45 CPU seconds and 60 wall seconds. Reuse the frozen guard functions SHA-256
`3663659769ae4cddabd4edc8e351558fe900b568f195496ffd0a07e6f0c65c2d`,
MolSysSuite #173. Stop owned work on a resource interruption; preserve it and
do not automatically restart after a headroom stop.

Extend the existing exact-ESM DOM tests for unavailable geometry, the nonfirst
bound index, safe literal coverage text and action suppression. Run the locked
existing Node/jsdom composition with one worker/CPU and bounded resources; no
browser/comm/canvas, server or kernel is started. Source doubles and jsdom do
not qualify actual installed provider behavior, rendered pixels or whole E4.

Raw code/attempts stay under `.molsyssuite/e4-addon-binding-20261107`, #50
custody, review 2026-11-14. Original migration inputs remain untouched/untracked.
No helper/fixture producer or runtime dependency pin changes are authorized by
this increment. Update maintained checkpoints and relevant resource declarations
after final edits; check the fresh actual committed export. Use `[skip ci]`,
no automatic manual hosted CI; missing exact-head evidence remains #28.

## Remaining gates

Receive a new exact installed candidate on the original admitted carriers,
normal/pm-fs, before claiming this new route's provider compatibility. Preserve
the original five-pose result and explicit one-frame association in that
qualification. Positive-source invalidation persistence stays failed under
MolSysMT #642 until separately received. Actual canvas #52/#60, other-carrier
projection, broader E4, E3/MolSysMT #604, independent science/reproduction,
public delivery and the complete #73 objective remain separate.

## Source-selection correction and frontend tool admission

`source-tests-01` collects 182 cases: 181 pass and one existing real-MolSysViewer
receiving case is stopped by the deliberately forbidden molecular-operation
guard. That case, `tests/test_viewer_state.py::test_public_resolved_widgets_keep_separate_reactive_state_and_owned_cleanup`,
loads an actual molecular fixture; it is not a source protocol test. No actual
molecular operation executes. The attempt remains failed (4.706 s, 202,485,760
bytes sampled group RSS), without resource interruption. Register its explicit
deselection from the complete repeated source selection; its real provider gate
remains outstanding for actual installed receiving. No production assertion or
scientific refusal is weakened and no skipped result becomes a pass.

The routine environment contains Node 24.22.1/npm 11.19.1, while the existing
locked DOM harness declares Node 26. Reuse its previously qualified Node 26.3.1
through a task-owned Linux x64 official archive, verified against that exact
release's official SHA-256 list. Do not change Conda or relax the declared engine.
Install the existing lockfile locally with lifecycle scripts/audit/funding checks
disabled. Run one Node worker, CPU0/nice10, 8 GiB available reserve, 512 MiB group
RSS, a 256 MiB V8 heap, 45 CPU seconds and 90 wall seconds. Use a 16 GiB virtual
address limit for V8's reservations; it does not expand the RSS allowance.
Download/extraction uses the same finite process policy. Preserve exact commands,
source/archive digests, versions, raw failures and completion receipts. Neither
tool acquisition nor DOM execution modifies the routine scientific environment.

## Executed source and DOM outcomes

The final complete source selection, `source-tests-05`, passes **186 cases**,
zero skips/failures: 28 new view controls, seven frontend protocol checks and
151 interaction/view/presentation/argument regressions. Its native pytest event
reports and JUnit agree. It takes 4.299 s with 201,863,168 bytes sampled owned-
group RSS, no forbidden real molecular call/Vina import and no resource
interruption. Earlier complete passes (181/184/186 cases) keep their original
source hashes and scope; the initial accidental native-case selection remains
failed. The one explicitly deselected real-provider receiving test remains an
outstanding native gate, not an accepted skipped test.

The locked Node 26.3.1/npm 11.16.0/jsdom 30.1.3 composition passes **23 exact-ESM
DOM cases**, including two new interaction-view controls. The runner tests the
literal served modules, not rewritten JavaScript. Actual native TAP records
23 passes, zero failures/cancellations/skips/todos. It takes 2.689 s with
314,146,816 bytes sampled group RSS under the separately registered V8 limits.
The original normal-state examples remain unchanged; a fifth binding example
is compared to fresh production Python panel state. Literal text, unavailable
row/input/button actions, live coverage changes and clearing back to ordinary
result state pass. No real browser, comm transport or pixels are observed.

The task-isolated official Node archive is SHA-256
`55647180e4ae58ffeaa3294e89aa4abda7c371dfbd64b44cbdb022980177aae0`,
verified against its retained official release list. The executed binary is
`0b52710a27133a3baf45f0d1f10689ab874f50e5821d8e611486d17e20bcacdd`.
Bootstrap/locked dependency installation pass in 7.890/2.970 s. Conda's existing
Node 24.22.1 and scientific environment are unchanged. The private dependency
tree/tool prefix remain under task custody for subsequent checks.

The [qualification receipt](data/pose_interaction_view_source_2026-11-07.json)
is SHA-256 `9c69f2468b35da2e26a83004809a6f47139d8d62f9ed12d3240b59f5550c217f`.
The [178-member immutable archive](data/e4_pose_interaction_view_source_2026-11-07/manifest.json)
is `9fbdb4081342dc80e117ff731837acc7be8a91edf690c157325a4e5173c4a04a`,
348,736 stored/1,484,121 decoded bytes. It preserves all five source attempts,
deduplicated byte-exact frozen source objects, native logs/JUnit/events, all
frontend phases, exact tool/source identities and terminal resource receipts.
The publishing commit binds tested runtime/test/ESM bytes; the recorded
`d71fd6b` is the implementation base, not a claim that it already contained this
new route. Administrative sealing passes without molecular imports/replay.

The runtime resource inventory adds only the new adapter module's required
installed path. The 30 helper/564 historical fixture SHA declarations are
unchanged; the new qualification records are not installed-test inputs. No
provider pin, original scientific input or existing immutable archive changes.
All owned groups are terminal, with no resource interruption in this increment.

**Installed follow-through:** source `2ef82d2` now has separately
[passing exact-candidate receiving](e4_pose_interaction_view_installed_2026-11-07.md),
eight real-provider cells normal/pm-fs and independent reading of 342 sealed
members. The previously excluded native test passes in each policy. This does
not rewrite the initial failed source attempt or convert the source-only receipt
to native evidence. Runtime/test/ESM bytes and original producers remain unchanged.

**Next:** review remaining #80/#60 acceptance criteria against this one-carrier
route. Preserve the maintainer's actual canvas/comm scheduling hold. #642 has
owner triage, no received correction; positive-source persistence remains failed.
#28 exact-head hosted evidence is missing under `[skip ci]` without manual CI.
Other-carrier projection, broader Core/E4/E5, independent scientific reproduction,
public/minor/platform delivery and full #73 remain open.
