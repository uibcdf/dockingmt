# Private installed-wheel addon receiving

Owners: [BindingMT #47](https://github.com/uibcdf/bindingmt/issues/47) and
[#60](https://github.com/uibcdf/bindingmt/issues/60). This checkpoint qualifies
one private Linux x86_64 / Python 3.14.8 installation. Public distribution,
platform admission, browser observation and C6 remain separate gates.

## Exact candidate

The private wheel is `bindingmt-0.0.0+222.g376679c-py3-none-any.whl`, built once
from committed producer `376679c2fe77298eda7a80edd311335c2cfa205b`.
Its SHA-256 is
`aa5626e1ee7073a2df32fdce75cf10c132eeedffc807aa71a5421d1a55a9391e`.
All 63 required payload files are present; 62 match source bytes and the
generated version file matches the wheel version. Python bounds are compared
as specifier sets, preserving `>=3.11,<3.15` regardless of metadata ordering.
No artifact is rebuilt, retagged, uploaded or promoted by receiving.

The [receiving manifest](data/addon_installed/manifest_2026-11-03.json) binds the
[archive inventory](data/addon_installed/wheel_2026-11-03.json),
[environment inventory](data/addon_installed/environment_2026-11-03.json),
[installed-suite receipt](data/addon_installed/installed_suite_2026-11-03.json)
and [kernel receipt](data/addon_installed/kernel_receipt_2026-11-03.json)
to their content hashes. Raw logs, original wheels and executed widget outputs
remain task-owned evidence; these public records are sanitized summaries.

A new independent Conda prefix provides support/scientific dependencies through
the ordinary UIBCDF/conda-forge route. The unchanged controlled ArgDigest,
MolSysMT and MolSysViewer wheels are then installed normally alongside this
BindingMT wheel. OpenMM 8.6.1 comes from its public CPython 3.14 wheel, without
the Conda CUDA dependency chain. This is an explicitly recorded acquisition
variant, not a claim that every dependency byte equals the earlier receiver.
`pip check` reports no broken requirements. The original receiver is preserved.

PEP 610 records bind the installed consumer to the exact archive digest and
refuse editable installation. The `molsysviewer.addons` entry point loads
`molsysviewer_bindingmt`; its addon version equals the wheel version. The public
Viewer resolver creates and mounts the real Explorer widget. All 63 installed
consumer files and every non-metadata payload member of the three provider
wheels match their original archives.

## Full installed test gate

The test/data context is a separate sparse Git checkout of the exact producer,
with neither production package present. Execution starts outside all source
checkouts using the receiver interpreter in isolated mode. Only this source-free
harness and the immutable SDK are added for tests and developer operations.
The shared `installed_noarch.run_tests` operation uses importlib mode and
`-o pythonpath=` with the complete `tests/` selection and `--receptor=llm`.
Additional pre/post checks cover core, addon and loaded provider origins, plus
all installed consumer hashes; the SDK's single primary-root check alone is
not used to establish addon provenance.

The full suite passes **1,430 tests**, zero failures/errors/skips, in **903.38 s**.
All loaded core/addon/provider modules remain prefix-owned and all 63 consumer
files are unchanged after tests. Dependency closure still passes afterward.
The receipt retains 328 warnings in eight groups, including legacy H5MSM,
declared structural-field losses, PDB bond-inference diagnostics and a preimported
`smonitor` assertion-rewrite warning. This does not qualify public dependency
coordinates, other interpreters/platforms or an actual Conda release archive.

The exact producer's hosted run `41699697539` separately verifies quality,
distribution governance and Linux/Python 3.14 (**1,430 passed**, 522.33 s,
334 warnings). The other three Python jobs are queued/in progress in the
retained observation, so the whole run is not claimed successful.
Policy `41699698013` and publication-governance
`41699697902` complete successfully at that same producer. Inspect remaining jobs
on #47/#60; their pending state does not become installed-wheel evidence.

## Real-kernel installed workflow

The [installed companion notebook](addon_3ptb_installed_workflow_2026-11-03.ipynb)
changes only the introductory profile and installation/origin/provenance checks
of the [source notebook](addon_3ptb_workflow_2026-11-03.ipynb).
Every later scientific/widget cell is byte-identical. The source notebook and
its original receipts remain frozen. The companion requires the exact candidate
version, digest and source-free data checkout, and verifies installed core,
addon and provider origins before molecular work.

All five cells complete through a real task-owned IPC kernel. Five frames and
2,033 atoms match the explicit original inputs, with coordinate tolerance
`1e-12 angstrom`. The original result remains detached, and all 33 monitored
original files are unchanged. Real Python widget actions, score/identity
presentation, explicit external-player Refresh, remount, reference/domain
visibility, independent views, owned cleanup and non-default units pass.

Input recreation explicitly replays the existing admission recipe: one receptor
and two ligand preparation calls. New native writer hashes stay separate from
the historical submitted bytes. Guarded search/map/energy/optimization/RMSD
entry points have zero calls. These zero counts describe the notebook, not the
complete unit suite. Nine composition warnings retain the same three categories
as source execution; the display is not a molecular/mechanics archive.

Two startup failures are retained: missing task-tool Tornado, then a missing
IPC runtime directory. Neither attempt executes a notebook cell or prepares
inputs. The third attempt completes after task-only setup corrections; no
scientific assertions or packages are changed. All task kernels are shut down.
The executed notebook and raw logs remain private; committed receipts contain
no personal paths or unrestricted logs.

For a later run, retain the exact wheel and provider archives identified by the
manifest, use the recorded receiver composition and prepare a separate test/data
checkout of the producer without either production package. Set
`BINDINGMT_NOTEBOOK_ROOT` to that harness,
`BINDINGMT_EXPECTED_PROVIDER_PREFIX` to the receiver and
`BINDINGMT_ADDON_OUTPUT` to a new directory. Start the recorded kernel with
task-only Jupyter tooling and that harness on its import path and as its working
directory. The companion's
first cell refuses a source overlay, editable candidate, wrong archive/version
or wrong data-checkout revision. Headless execution needs an existing task-only
IPC runtime directory and explicit kernel shutdown in `finally`.

## Resource and remaining-work checkpoint

Initial receiver setup stopped when the temporary filesystem could not complete
installation. A proposed hardlink clone was rejected by automatic review before
execution because writes could affect the original environment. The successful
route creates a genuinely independent prefix on separate storage. No hardlink
clone was executed. Retained wheel, receiver, setup attempts, source-free harness
and execution tools belong to #47/#60/#50, review **2026-11-10**, with no automatic
deletion of original evidence or shared environments.

Setuptools also reports deprecated license-table/classifier metadata during the
build. The packaging cleanup is tracked on #47 for a future candidate; this
qualification does not rewrite or rebuild the retained archive.

There is no connected browser. Actual frontend controls, camera/clipping and
rendered pixels remain unobserved; C6 is unaccepted and maintainer interaction
is deferred. MolSysViewer #291 still owns immediate notifications for unrelated
Python player calls; Refresh remains the explicit route. MolSysMT #521 owns
partial/reference molecular reading. No downstream molecular routine or generic
Viewer replacement is introduced here.

Next: receive delivered provider changes against this bounded workflow, perform
the browser checklist when a session is available, and complete actual public
artifact/dependency/platform admission under #30/#47 before any release. No
human interaction is required for the current headless checkpoint.
