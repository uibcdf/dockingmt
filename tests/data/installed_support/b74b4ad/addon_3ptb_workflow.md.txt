# Saved-case addon workflow in a real Jupyter kernel

The later [private installed-wheel checkpoint](addon_installed_receiving.md)
executes a separate companion profile in an independent receiver. This page and
its linked original notebook/receipts retain the earlier source execution below.

Owner: [BindingMT #60](https://github.com/uibcdf/bindingmt/issues/60).
The maintainer cannot perform an interactive review at this checkpoint. The
[new notebook](addon_3ptb_workflow_2026-11-03.ipynb) is prepared for that later
review and has been executed through a real kernel without a browser.

## Executed scope — 2026-11-03

All **five code cells** complete using BindingMT source `a667dc1` and the retained
ordinary-installed provider composition from
[ChemicalStates receiving](../chemical_domain_receiving.md). The notebook checks
actual module origins before molecular work. This is source-addon/kernel evidence,
not a newly built or ordinary-installed BindingMT artifact.

The public scene has five frames and 2,033 atoms: 2,011 receptor atoms, 13 pose
atoms and nine observed reference atoms. All frame coordinates, five identity
fields per role and the twelve search-box edges match their explicit inputs.
The saved result, its producer attribution and all **33** monitored original
files are unchanged. Coordinate assertions retain `1e-12 angstrom` tolerance.

The real public addon resolver creates Explorer and Search Domain widgets.
Their Python action path verifies pose selection, named scores/descriptors,
shared reactive state, reference/domain visibility, unmount/remount, explicit
Refresh after an external player call, independent views and owned cleanup.
Non-default pm/fs/kJ/mol policy preserves coordinates and stored score meaning.
The notebook ends at position 1 with reference/domain visible and requests the
Docking Explorer workspace through the public Viewer API.

The [kernel receipt](data/addon_3ptb/kernel_receipt_2026-11-03.json) and
[manifest](data/addon_3ptb/manifest_2026-11-03.json) retain versions, source-file
hashes, exact original-result/source identities, notebook/receipt digests,
attempt history and all observed diagnostic categories. They contain no personal
paths. The executed notebook and task kernel tooling remain private task resources.

## Explicit input recreation, not a recovered molecular snapshot

The #58 verifier recovers the original five-pose record with `problem is None`.
The original scene receiver is absent from its historical location; no replacement
is presented as that original artifact. Instead this new notebook explicitly
replays `devtools.qualify_3ptb_admission.admit`, the existing registered molecular
hypothesis, through public MolSysMT and BindingMT tools.

Each attempt calls receptor preparation once and ligand preparation twice
(the existing rigid/flexible admission recipe). Only the saved rigid/native
result is displayed. Prepared coordinates, state labels, names/groups, atom
types, charges and original source axes match the retained admission. Reference
coordinates and actual domain geometry also match. No routine in this notebook
reconstructs molecules from captured PDBQT or infers missing chemistry.

Current native exports differ in bytes for all three prepared roles; both the
old submitted hashes and the new export hashes are recorded. The original
execution remains bound to its original bytes. No new search, maps, energy
evaluation, optimization or RMSD is performed; guarded entry points fail if
invoked. This does not establish a new redocking result, experimental state
validity, affinity accuracy or a general preparation archive.

Nine provider warnings remain recorded: three report loss of occupancy/B-factor
fields, five report loss of partial-charge/type assignment metadata during scene
composition, and one reports loss of `atoms_ff`. These declared concatenation
losses make the composed display unsuitable as a replacement molecular/mechanics
archive. Explicit scientific inputs and the original result remain separate.

## Attempts and kernel ownership

Attempt 1 stops in the second code cell because a notebook assertion compares the
three-field geometry projection with a backend record that additionally declares
`rounding_decimals`. Input-coordinate/type/charge checks had passed. Attempt 2
compares center/size/unit and separately requires the recorded six-decimal policy;
the coordinate tolerance and molecular expectations are unchanged. Both attempts
are retained, with three preparation calls each and zero new searches. This is
an orchestration correction, not a provider defect or a passing first attempt.

Jupyter tools were installed in a task-only directory with existing compatible
scientific dependencies retained in their original prefix. The successful
kernel uses local IPC, a task-only kernel specification and task-only caches.
There is no web server, persistent user kernel registration or running kernel
left by the automated execution. Shared environments and sibling worktrees are
unchanged. Resources belong to #60/#50, review **2026-11-10**, without automatic
deletion of retained evidence.

## Reproduce when convenient

Use a Python 3.14 kernel with this checkout as the BindingMT source and a compatible
controlled scientific prefix. The kernel needs the Jupyter tooling recorded in
the receipt; these tools are development/execution dependencies, not new package
runtime requirements. Set the following before starting the kernel:

```bash
export BINDINGMT_NOTEBOOK_ROOT="$PWD"
export BINDINGMT_EXPECTED_PROVIDER_PREFIX=/path/to/qualified/scientific/prefix
export BINDINGMT_ADDON_OUTPUT=/path/to/a/new/output/directory
```

Open `devguide/validation/addon_3ptb_workflow_2026-11-03.ipynb` from the checkout
and select that kernel. Its output directory must not exist. Running all cells
explicitly recreates the declared inputs but does not search or score again.
The source and provider origin assertions refuse accidental sibling overlays.

Headless execution can use the standard `nbclient.NotebookClient` with the chosen
kernel and checkout as its working directory. Keep the executed copy separate
from the committed notebook, retain failures and shut down the task kernel in
`finally`. The committed notebook has no stored widget outputs; opening a saved
executed file alone does not restore its Python backend. A live user-run kernel
keeps the displayed view available after the final cell.

## Deferred observation

The current UI inventory contains **no connected browser**. Kernel execution and
Python widget actions verify no rendered pixels, camera framing, clipping or
actual frontend button/row behavior. `browser_controls_verified`,
`rendered_pixels_verified` and `C6_accepted` remain false in the receipt.
No action from the maintainer is required now.

When an appropriate browser session is available, verify that all four objects
are visible, click pose rows and navigate 5 → 1, compare the selected score/rank
with the scene, toggle reference/domain, reopen panels and rotate/zoom the camera.
Record the actual observation or owning provider failure in #60. Immediate
notification after unrelated Python player calls still awaits
[MolSysViewer #291](https://github.com/uibcdf/molsysviewer/issues/291); Refresh is
the explicit bounded route meanwhile. The historical HTML observation remains
deferred under #52. Public package/platform admission remains #30/#47.
