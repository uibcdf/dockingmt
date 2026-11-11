# Public player notification receiving

Owner: [BindingMT #60](https://github.com/uibcdf/bindingmt/issues/60).
Provider: [MolSysViewer #291](https://github.com/uibcdf/molsysviewer/issues/291).
This receiving adds consumer guards and controlled source pins. BindingMT runtime
and molecular routines are unchanged. Browser transport, controls, pixels and C6
remain pending; no maintainer interaction is required now.

## Provider and consumer identities — 2026-11-03

The selected Viewer source is
`78ede79e2e345593db5bfe80d246d3f6c70bd005`, replacing `ca7ebea6` in both
scientific CI workflows and the dependency inventory. MolSysMT stays at main
`00abb958fb93649131d5ce5fe5e12e90cf4900e9`; the retained molecular wheel's actual
producer is `de7ffad2aef18ff3bccd184133dc69e081cb506e`, with identical relevant
source/build objects. ArgDigest stays `3d1ec53c374098016452abab74706e9d80df5462`.
No molecular-provider upgrade or downstream callback replacement is needed.

The new private Viewer wheel is `molsysviewer-0.24.0+260.g78ede79e-py3-none-any.whl`,
SHA-256 `3d31a4d9edb7ed0e72fadcd81b3952196795218f55776478a7625b79e47e9e2a`.
All 635 payload members match that source/build output. An ordinary, independent
Conda receiver installs this archive and the retained scientific wheels normally.
OpenMM retains the previously recorded public CPython-wheel acquisition variant.
Dependency closure passes; original receivers and sibling worktrees are preserved.

BindingMT reuses the private SPDX wheel from producer
`50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9`, version `0.0.0+225.g50d8e33`,
SHA-256 `5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`.
Its 62 nongenerated runtime files equal the receiving source; the generated
version retains its original artifact identity. The test/data harness is the
separate qualification commit `1c343924b4a144058685796783d72c174b032651`.
The retained BindingMT artifact is not rebuilt or relabelled. The new Viewer
wheel is private; no archive is uploaded or promoted by this receiving.

## Informative regression and actual widgets

The new [consumer guard](../../tests/test_viewer_player_receiving.py) uses a real
public Viewer demo/frame selection, addon discovery, public widget resolver,
actual panels and their unchanged state publication. Its presentation records
deliberately contain ranks `[7, None, 1]`, missing identity and Vina zero; they
are controlled presentation data, not a molecular-geometry experiment.

Against the preserved old Viewer installation, the first navigation case fails:
`player.index` becomes 2 while the addon remains at 0. The failure is retained
separately from passing receiving. With the delivered provider, **98 selected
tests pass**, zero skips, in 14.10 s with 43 warnings (42 legacy-H5MSM and one
preimport/assertion-rewrite warning). Thirteen new cases exercise direct seek,
first/last, stepping/wrap, duplicate suppression, play/pause state, real widget
unmount/remount/close, failed seeks and independent views. Both panels receive
notifications without Refresh; stored result meaning is preserved.

This focused run combines the current harness with installed provider bytes;
the source-free full installed gate below establishes complete import provenance.
The existing fake-host readback guard remains deliberately non-notifying, so
explicit Refresh compatibility remains covered. No polling, private observer,
molecular implementation or generic Viewer replacement is introduced.

## Source-free installed gate

The complete installed suite passes **1,449 tests**, zero failures/errors/skips,
in **848.90 s** on Linux x86_64 / Python 3.14.8. Its scientific namespaces are
absent from the sparse harness; execution starts outside source and uses the
immutable SDK's importlib runner. All 63 consumer files, all provider payloads
and all loaded core/addon/provider origins are checked before and after tests;
the harness stays clean and final dependency closure passes.

The [installed receipt](data/addon_player/installed_suite_2026-11-03.json)
retains 342 warnings in eight groups, including legacy H5MSM, structural-field
loss, PDB bond-inference diagnostics and preimported SMonitor assertion rewriting.
The [manifest](data/addon_player/manifest_2026-11-03.json) binds regression,
environment, original consumer/new provider archive inventories and notebook
receipts to their hashes. This is private-wheel Linux/Python 3.14 qualification;
other interpreters/platforms and public archives remain separate. Exact-head
hosted observations and their recovery route are recorded on #60/#47.

The declared dependency preflight passes ten routes/four contexts. An initial
invocation without `--declared-only` is rejected because installed qualification
requires an explicit context; it executes no qualification. The corrected
declared-only run passes. The routine administrative selection passes 34 tests.
Ruff lint/format and report indexes retain their own gates.

## Real-kernel saved-case replay

The new [3PTB companion](addon_3ptb_player_receiving_2026-11-03.ipynb) preserves the
preceding notebook's molecular reconstruction and scene cells byte-for-byte.
Installation/provenance checks bind the retained consumer, new Viewer archive
and distinct harness. Widget assertions now require immediate state after direct
Python navigation before Refresh, plus suppression of a repeated seek. Explicit
Refresh remains checked. Historical notebooks and receipts are unchanged.

All five code cells complete in a real task-owned IPC kernel, which is shut down
after execution. The [kernel receipt](data/addon_player/kernel_receipt_2026-11-03.json)
and [execution record](data/addon_player/notebook_execution_2026-11-03.json) retain
five poses/frames, 2,033 atoms, the original coordinate frame and identity checks,
`1e-12 angstrom` tolerance, 33 unchanged original files, detached result and
nondefault-unit checks. Recreating inputs explicitly makes one receptor and two
ligand preparations through the existing MolSysMT admission recipe. Current
writer bytes stay separate from the original submitted bytes. Guarded map,
energy, optimization, search and RMSD entry points have zero notebook calls.

The nine known scene-composition warnings remain explicit: structural
occupancy/B-factor loss, chemical assignment/type/charge loss and mechanical
assignment loss. The display is not a molecular archive.

## Meaning and remaining work

The delivered event reports accepted Python authority state synchronously; it
does not certify a browser round trip or GPU completion. Frame indices refer to
the loaded trajectory, not source-frame indices or scientific ranks. #291's
provider delivery and this consumer receiving are separate from public API
minima and published package compatibility.

Keep #60 partial until live frontend controls/comm/canvas and the deferred visual
criteria are observed. #52 retains the original scene review. Public dependency
coordinates, candidate/platform admission and release planning stay #30/#47;
partial/reference molecular reading remains MolSysMT #521. No new scientific
profile, public release or C6 acceptance follows.

Task-owned receiver, archives, harness, logs and kernel tools remain under
#60/#50 custody, review **2026-11-10**. No server or watcher is needed; the kernel
is closed and the full test process has completed. The independent Viewer build
checkout is retired after archive verification; its archive and receipts remain.
Original evidence, sibling clones and shared environments are protected.
