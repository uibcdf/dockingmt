# Public Viewer archive receiving — 2026-11-04

Owners: [DockingMT #47](https://github.com/uibcdf/dockingmt/issues/47),
[#60](https://github.com/uibcdf/dockingmt/issues/60) and qualification
[#30](https://github.com/uibcdf/dockingmt/issues/30). Provider disposition:
[MolSysViewer #294](https://github.com/uibcdf/molsysviewer/issues/294).

**The exact public Viewer 0.24.0 build 1 is incompatible with the qualified
DockingMT addon profile.** Static addon/callback symbols do not establish the
required behavior. Keep the successful private-source receiving and its
scientific pins unchanged. No runtime, dependency minimum or release is changed.

## Exact installed composition

The public file is `molsysviewer-0.24.0-py_1.tar.bz2`, SHA-256
`e31dfb114ab2e49f22b372992d0201455b91849f2631d0165b802069e13abeaa`.
The [archive receipt](data/public_viewer/archive_2026-11-04.json) identifies the
main-channel URL and dependencies. Build 0 is a different staging-only file.
The embedded build-time wheel URL is not used as installed-artifact provenance.

A normal offline Conda clone with `--copy` creates an independent prefix.
File-inode checks precede any replacement. Only in that new receiver, the
private Viewer is uninstalled and the exact public file is installed normally,
with dependencies held fixed. This bounded artifact test is not a fresh public
solve. Conda cloning initially restores its registered ArgDigest over the
controlled pip overlay; the first payload preflight refuses before pytest.
Normal removal/reinstallation of the unchanged controlled ArgDigest wheel in
the new receiver restores the intended composition. The failed preflight is
retained separately; no provider defect is inferred from that setup correction.

| Component | Received identity |
| --- | --- |
| Python / platform | 3.14.8 / Linux x86_64 |
| DockingMT private wheel | `0.0.0+225.g50d8e33`, producer `50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9`, SHA-256 `5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98` |
| MolSysMT controlled wheel | `0.23.0+361.gde7ffad2a`, SHA-256 `4a8e58f40627ff468fab99301674429fba66362f549a31fb4cc747d9cf19a0ba` |
| ArgDigest controlled wheel | `0.15.0+5.g3d1ec53`, SHA-256 `1cb379478b1abea9d91c06fc6fa5dffa24ede35a24fb1a2d8657c9b13ed55f0c` |
| Unchanged support | PyUnitWizard 0.29.0, SMonitor 0.22.0, DepDigest 0.15.1 |
| Source-free test/data harness | `1c343924b4a144058685796783d72c174b032651` |
| Installed runner SDK | `738fe8dd731abb99dac421b0bb2acc8564110180` |

## Executed selection and isolated observations

The [installed receipt](data/public_viewer/installed_selection_2026-11-04.json)
records seven unchanged viewer/player/presentation/saved-audit test files,
executed outside source with the shared importlib runner, `--receptor=llm` and
cleared pytest `pythonpath`. Both production namespaces are absent from the
harness. The addon entry point loads the installed consumer. All **4,145**
payloads verify before and after: 63 consumer files, 629 public Viewer
site-package files, 3,415 molecular-provider files and 38 ArgDigest files.
All 1,244 loaded scientific modules remain receiver-owned. Dependency closure
passes before and after; matching metadata alone does not make the APIs compatible.

The actual result is **119 passed, 7 failed, 36 errors, zero skips**, exit 1,
in 6.18 s, with two warnings. The warnings are preimported SMonitor assertion
rewriting and a recursion diagnostic during SMonitor exception emission.
The initialization cascade prevents many cases from reaching their assertions;
these are not 43 independently established provider defects.

Fresh-process [diagnostic probes](data/public_viewer/provider_probes_2026-11-04.json)
isolate the useful findings:

- A public `view.shapes.add_sphere(...)` returns `Shape`, whose `info()` is
  absent. The addon uses the later qualified public handle API to read owned
  domain visibility. This relates to Viewer #217's source delivery.
- After explicit Pandas/MolSysMT initialization, a real provider demo selects
  three frames. `view.player.go_to_structure(2)` changes index to 2 but delivers
  no `on_frame_change` callback. This is the public-file boundary of Viewer
  #291; its later source delivery remains qualified separately.
- Creating that demo after Viewer-first lazy molecular initialization instead
  produces recursive addon-loading diagnostics and an eventual NumPy import
  error. The suite reports partially initialized Pandas and absent `msm.get`.
  Pandas-only import and explicit MolSysMT initialization pass in fresh
  processes. This remains owner triage of the controlled combination, not proof
  of a standalone Pandas/NumPy defect. Import-order changes are diagnostic only.

The provider issue contains the minimal shape and three-frame callback
reproductions. No local polling, private observer, copied handle API or molecular
substitute is added. Generic viewer behavior belongs in MolSysViewer; molecular
operations remain MolSysMT-owned.

## Notebook, preservation and continuation

The registered saved-case notebook stops **before kernel launch or preparation**
after failed receiving. Its unexecuted companion draft is retired. No maps,
searches, energy, optimization or RMSD are attempted in the guarded selection;
the probes use a provider demo without preparation or engine work. The earlier
successful five-cell private-Viewer notebook and all original records remain
unchanged. All **45,015 files/symlinks** in the original qualified receiver
verify unchanged against the pre-operation inventory.

The [manifest](data/public_viewer/manifest_2026-11-04.json) hashes the new
path-free records and full public Viewer payload inventory. Raw logs, the failed
preflight, independent receiver and private diagnostic drivers remain under
#47/#60/#50 custody, review **2026-11-11**. Tests/probes have finished; no kernel,
server or watcher is started. Original prefixes, shared caches and sibling
worktrees are preserved.

The [prior checkpoint CI receipt](data/public_viewer/prior_ci_2026-11-04.json)
recovers all four completed successful runs for exact head `8dbcab39`: CI
`41755973401`, DOM `41755973066`, policy `41755973544` and publication governance
`41755973005`. These do not qualify the incompatible public Viewer composition
or another source head.

Local closeout passes Ruff lint/format, generated report indexes, manifest
hashes, JSON privacy, local receipt links, frozen earlier manifest checks and
20 reporting/distribution controls. The first administrative test invocation
omits the explicit immutable SDK selector and stops its setup (one reporting
test passes, 19 distribution setups error); the corrected selector passes all
20 controls. This setup correction does not alter the failed public receiving.

Next receive an owner-selected additive public Viewer artifact covering the
handle/player contracts and triage the initialization boundary under #294.
Repeat this bounded installed gate before the saved-case kernel. Separately
receive a MolSysMT artifact exposing the reader/graph APIs under its #334;
neither provider's frozen initial release is expanded by this request. Then
qualify the real public combination, numerical minima and installed-helper
profile before choosing a staged DockingMT candidate. Preserve published bytes
and tags. Browser controls/comm/canvas and visible C4/C6 remain deferred.
