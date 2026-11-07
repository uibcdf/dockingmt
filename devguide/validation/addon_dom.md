# Addon JavaScript DOM checkpoint

Owner: [DockingMT #60](https://github.com/uibcdf/dockingmt/issues/60).
The accepted next slice executes the shipped Explorer/Search Domain JavaScript
without requiring maintainer interaction. It adds test coverage and a test-only
CI job; production core/addon code is byte-identical to baseline `9f8b787`.
The preceding private wheel and frozen notebook/receipts are unchanged.

The subsequent [interaction-view source increment](pose_interaction_view.md)
now passes 23 exact-ESM DOM cases, including two interaction-view additions and
seven current backend/frontend contract cases. It changes product code and has
its own receipt/source hashes; it does not rewrite the original 21-case
checkpoint below or qualify installed provider/comm/canvas behavior.

## Executed scope — 2026-11-03

**21 JavaScript tests pass**, zero failures/skips, using Node 26.3.1, npm 11.16.0
and locked jsdom 30.1.3. The runner reads the literal `_ESM` declarations with
Python 3.14.7's standard-library AST, then evaluates their exact ES modules in
separate jsdom VM contexts. It does not rewrite exports, duplicate the panel
implementation or import scientific packages for JavaScript extraction.

The tests exercise real DOM click/change handlers and assert actual outgoing
action messages, collection index versus display position/scientific rank,
missing identity/rank, zero and unknown score meaning, declared score units and
descriptors, empty/error/cleared states, invalid positions, both state delivery
paths, reference/domain prerequisites, render/hide/show actions, rejected display
units, literal text, independent instances, remount and subscription cleanup.
Cleanup preserves unrelated model subscribers. DOM handler exceptions fail tests;
each window closes even when module evaluation/rendering fails.

The model double supplies only attributes, change/custom events and JSON message
capture. Subsequent-state mutations represent supplied host states; they do not
simulate or verify real provider callbacks or a Python/JS round trip.

Six Python contract cases bind the four JSON examples to fresh production panel
states and the extracted modules to actual widget `_esm` values. Together with
existing presentation/state and administrative controls, the final selection
passes **78 Python tests**, zero skips, in 6.69 s, with one legacy-H5MSM warning.
The full prior 1,430-case installed result is retained as its original evidence;
it is not relabelled as a full run of these new tests.

The [receipt](data/addon_dom/checkpoint_2026-11-03.json) records executed file
hashes, versions, results, attempts and limits. Raw logs remain private.

## Corrections and diagnostics

The first Node launch fails before case execution because the local sandbox
reports `spawnSync python EPERM`. A permitted execution outside that restriction
runs all cases. Its first full run has 20 passes and one test expectation failure:
the assertion expects the abbreviation `kJ/mol`, but the actual Python protocol
declares the canonical string `kilojoule / mole`. The final assertion requires
the exact supplied unit while retaining the numeric expectation and descriptor
checks. All 21 cases then pass. No production or provider fix is inferred.

Node emits its documented experimental VM-module warning. The flag belongs only
to this development runner. jsdom supplies DOM behavior without layout/rendering;
no real browser, pixels, camera/clipping, widget comm transport, maintainer review
or C6 is accepted. No server, kernel or watcher is launched.

## CI, ownership and reproduction

Use the [local commands and harness contract](../../devtools/frontend/README.md).
The private npm package/lockfile adds only third-party test dependencies; none
enter Python metadata, Conda runtime requirements or the distribution payload.
The component graph covers registered members, so these third-party tools add
no registered-member edge. Existing scientific workflows and source pins retain
their exact bytes. The complete declared workflow inventory now has ten routes
and the same four scientific contexts; administrative guards/preflight pass.

`Addon DOM` runs on push, pull request and manual dispatch with explicit tool
setup, a locked install without lifecycle scripts and the direct failing-test
command. This local addition covers a measured gap: Python CI does not execute
the panel JavaScript. A reusable optional starter pattern is proposed in
[MolSysSuite #161](https://github.com/uibcdf/molsyssuite/issues/161); replace the
local gate when a qualified shared route preserves these assertions. Hosted
exact-head results are recorded on #60 after publication, separately from local
success. The future real release plan must explicitly review this new product
gate under #47; no release example, staged archive or release is changed here.

The task-only npm cache is removed after verification, without cleanup errors.
Private logs/operational records and the ignored dependency tree remain useful
for subsequent addon tests under #60/#50, review **2026-11-10**. Original
scientific receivers, shared environments and unrelated work remain protected.

## Next

Receive supported Python player notifications from MolSysViewer #291 when
delivered. Observe the live comm/control/canvas path using the saved 3PTB
notebook when a browser session is available; no maintainer action is required
now. MolSysMT #521 retains partial/reference molecular reading. Public artifact,
dependency-minimum and platform admission stay #30/#47. This is addon testing,
with no new molecular implementation, scientific hypothesis or computation.
