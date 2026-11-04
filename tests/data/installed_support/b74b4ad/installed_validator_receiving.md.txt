# Installed import-root validator receiving — 2026-11-04

Owner: [DockingMT #47](https://github.com/uibcdf/dockingmt/issues/47);
qualification coordination: [#30](https://github.com/uibcdf/dockingmt/issues/30).
Shared operation: [MolSysSuite #110](https://github.com/uibcdf/molsyssuite/issues/110).

The shared verifier from `95f693be10c9205ab9b912cb53453710a207bf45`
passes bounded receiving against the retained actual private DockingMT wheel.
It infers both `dockingmt` and `molsysviewer_dockingmt` from the existing resource
inventory, clears inherited pytest source paths and rejects loaded source
modules or contaminated package search paths. No local replacement is added.

This prepares the installed-validator profile independently of public dependency
availability. The installed workflow remains pinned to `2d320484...`; source
SDK `738fe8dd...`, scientific pins, resources, full-suite declaration and all
candidate/platform gates remain unchanged. This is not the staged Conda file,
complete public closure, source-helper migration or a whole installed matrix.

## Bound identities and source-free execution

The consumer remains wheel `0.0.0+225.g50d8e33`, producer
`50d8e33f4ccb3354a8d27aea9fa9010c1b13e9a9`, SHA-256
`5a923951f5e1bec31f41329b7e62fc9a398286bfba10b6951e984c87b0676c98`.
Linux x86_64 / Python 3.14.8 uses the original controlled molecular composition:
MolSysMT `0.23.0+361.gde7ffad2a`, Viewer `0.24.0+260.g78ede79e` and
ArgDigest `0.15.0+5.g3d1ec53`. Nothing is installed or rebuilt. These are private
provider versions, distinct from the [failed public Viewer file](public_viewer_receiving.md).

An exact provider `git archive` exports only `devtools`; all 82 exported Git
blob identities verify before imports. The [source receipt](data/installed_validator/sdk_source_2026-11-04.json)
binds that commit, export digest and every file hash. The provider's sibling
worktree is not imported. The original source-free test/data checkout remains
`1c343924b4a144058685796783d72c174b032651`; all seven selected test files equal
current source. Both production namespaces are absent from that harness.

Every case starts a fresh actual receiver interpreter with `-I -B`, outside
the repository, with only the exact SDK and source-free harness added for test
operations. `sys.prefix` is real, the primary import is actually installed,
PEP 610 matches the original wheel digest, and all 63 consumer payloads verify
before and after each case. The shared operation receives the actual reviewed
resource inventory, not a substitute single-root descriptor. Its optional-addon
check remains lazy; initial addon absence is recorded before each control.

## Executed controls

The [case receipt](data/installed_validator/cases_2026-11-04.json) distinguishes
passing tests from expected provider refusals:

| Fresh-process case | Observed outcome |
| --- | --- |
| Source path inherited from pytest configuration and explicitly repeated in arguments | The shared runner's final override clears both. One test loads the actual installed addon and verifies its origin/version; pass, zero skips. |
| Actual source addon loaded before pytest | Shared `ContractError` rejects its origin at session start. |
| Installed addon with a source directory appended to its package search path | Shared `ContractError` rejects the contaminated `__path__` even though `__file__` remains installed. |
| Actual source addon imported by the test itself | Shared post-test `ContractError` rejects the loaded descendant; a successful test call alone cannot clear provenance. |
| Explicit import-roots list omits the addon present in required payload | Shared `ContractError` refuses the descriptor before pytest. |
| Seven existing addon/player/presentation/saved-result test files | **162 passed**, zero failures/errors/skips, 14.59 s; all 58 loaded core/addon modules are receiver-owned. |

All six receiving processes exit zero because each negative case requires its
specific provider refusal. Those four refusals are not four passing scientific
tests. Preloaded contamination produces pytest internal-error diagnostics before
the outer shared check raises the expected `ContractError`; raw logs retain
those diagnostics. No unsupported outcome is normalized into success.

The 162-test selection retains 43 warnings: 42 legacy H5MSM warnings and one
preimported SMonitor assertion-rewrite warning. The one-test source-path control
retains that same preimport warning separately. Engine/map/energy/optimization
and RMSD entry points are guarded in all cases, with zero attempts. There is no
preparation, new scientific kernel, search, geometry measurement or browser work.
Provider demos and molecular scene operations in the existing addon tests remain
delegated to MolSysMT/Viewer; no general molecular routine is introduced here.

## Preservation, CI and continuation

All 45,015 original receiver files/symlinks verify unchanged against the retained
pre-operation inventory, and dependency closure still passes. The prior public
Viewer manifest and scientific records stay unchanged. The [manifest](data/installed_validator/manifest_2026-11-04.json)
hashes the new path-free records. Task-only SDK export, probes and raw logs remain
under #47/#50 custody, review **2026-11-11**. All receiving processes finish;
no kernel/server/watcher is started. Original archives, shared environments and
sibling worktrees are preserved.

Local closeout passes Ruff lint/format, generated report indexes, the reporting
protocol test, current/frozen manifest hashes, JSON privacy and local receipt
links. No real release plan exists. These administrative checks do not extend
the focused installed selection to a full scientific or public-candidate gate.

The [source CI receipt](data/installed_validator/source_ci_2026-11-04.json)
recovers exact head `2d7b410e3a8bf74a833554a4f55a01defd65f0e2`: CI
`41839976367` completes successfully with all seven jobs, including four Python
lanes. DOM `41839976417`, policy `41839976847` and publication governance
`41839976787` also pass. This resolves the preceding pending source observation;
it does not qualify another validator composition, public file or new head.

Next review actual staged-candidate/helper needs and the whole installed suite
before adopting this installed-workflow pin. The current focused evidence does
not cover source-dependent support migration or every test. Public Viewer
#294 and MolSysMT #334 retain the additive-artifact handoffs; repeat public
receiving against their exact covering files before the saved-case kernel and
public combination/minima/candidate gates. Keep the failed public receiving
visible and preserve each provider's frozen initial release scope. C4/C6 visual
observation remains deferred.
