# Saved 3PTB human scene

Owner: [DockingMT #52](https://github.com/uibcdf/dockingmt/issues/52).
The maintainer accepted the first scene on 2026-10-23, following the
[pre-visualization pause](pause_handoff_2026-10-20.md).

The [notebook](human_3ptb_scene_2026-10-23.ipynb) composes existing public tools:
restore the original result, reproduce its audited explicit preparation, verify
submitted hashes, call `dockingmt.view`, give disjoint molecular regions explicit
representations, exercise Python visibility/frame commands and export through
`view.export.html`. MolSysMT owns all molecular operations and MolSysViewer owns
loading, representations and HTML/runtime export. There is no new molecular
implementation, rendering engine or production API in DockingMT.

## Executed evidence — 2026-10-23

All five code cells complete through the ordinary installed wheel. The notebook
checks all five frames / 2,033 loaded atoms, five identity fields per molecular
region, original coordinates within `1e-12 angstrom`, the actual twelve box edges,
Python reference/box visibility commands, frame 5 → 1 navigation, nondefault pm/fs
units and original result/input immutability. Search and scoring entry points are
forbidden throughout this execution. There are **zero new searches or scores**.

The separate source-free installed selection passes **41 viewer/reference and
molecular-delegation tests, zero skips**, 25.26 seconds, with 29 retained legacy
H5MSM warnings. The 29 administrative contracts pass separately. These checks
establish their stated Python/installed boundaries, not browser graphics.

The [manifest](data/3ptb_scene/manifest_2026-10-23.json),
[runtime receipt](data/3ptb_scene/receipt_2026-10-23.json),
[compressed self-contained HTML](data/3ptb_scene/scene_2026-10-23.html.gz),
[scene state](data/3ptb_scene/scene_state_2026-10-23.json.gz) and
[compact installed report](data/3ptb_scene/installed_tests_2026-10-23.txt.gz) retain
exact bytes/digests, execution scope and limits. Decompress the HTML archive before
opening it; the manifest records both stored and original digests. The original
uncompressed artifact is also retained at
`/tmp/dockingmt-3ptb-scene-20261023/output/scene.html` (7,758,464 bytes, SHA-256
`25fb6eb625f96c721f3b0b4d14ab19ef1884b5d8a166272cae2e225d3b537439`).

The first exploratory call used an incorrect export method name, and the initial
notebook attempt compared a tuple with a list in its strict map assertion. These
construction diagnostics are preserved locally and summarized in the manifest;
neither is a provider defect or a passing execution. The completed notebook uses
the documented public APIs and retains the full coordinate/identity assertions.

## Accepted question and scene

Can the saved docking pose be inspected against the observed reference and actual
search domain, in the original receptor frame, without manual molecular file
conversion or new search?

| Object | Declared scope | Representation |
| --- | --- | --- |
| Receptor | Existing dry prepared 3PTB hypothesis; 2,011 atoms | Grey cartoon |
| Selected pose | 13 actual submitted atoms, rank 1 initially | Blue ball-and-stick |
| Reference | Nine original observed ligand heavy atoms | Pink ball-and-stick |
| Search domain | Actual native box, 20 × 20 × 20 angstrom | Blue 12-edge wireframe |

The complete saved population of five poses remains as five frames. Rank 1 means
the lowest named `vina` score in that original population: **-6.422 kcal/mol**.
It is not a ranking by reference RMSD. No alignment, centering, new charge/state
assignment, omitted-H reconstruction or docking/biological accuracy claim follows
from the display. Camera movement is a presentation operation, not a coordinate
transformation of the molecular systems.

The reference and poses have different atom populations. MolSysMT validates the
pose/source identity; the notebook checks their declared separate loaded maps
and original coordinate slices. It does not invent a thirteen-atom reference.
Composition warnings about discarded preparation/mechanics or structural fields
remain visible. The scene is not a replacement preparation archive.

## Reproduce with the retained installed receiver

The ordinary wheel remains the original producer
`1decee504b112cfd92026c52dcbe22449de30f4f`, SHA-256
`24cfe209935b9bcdef371590427dc74818f23eece6711171346c72402c02ba4e`.
MolSysMT `c35252d89a28a8faff11e0014bda91312167f549`, MolSysViewer
`a61b75bc994e3ad674c3e7eafe53bb6b2a989c5f` and ArgDigest
`3d1ec53c374098016452abab74706e9d80df5462` retain the checkpoint composition.
They are normally installed task providers, not editable sibling overlays.

Use the recorded kernel with the ordinary receiver outside the source checkout.
Set these environment variables before starting the kernel:

```bash
export DOCKINGMT_SCENE_DATA_ROOT=/tmp/dockingmt-3ptb-scene-20261023/harness
export DOCKINGMT_EXPECTED_PREFIX=/tmp/dockingmt-human-20261020/receiving
export DOCKINGMT_SCENE_OUTPUT=/tmp/dockingmt-3ptb-scene-20261023/my-new-output
```

The data root contains the committed case recipes/data but neither production
namespace. The output directory must not already exist. The notebook authenticates
both original input and saved result, forbids search/scoring, and verifies loaded
DockingMT/addon module origins. If temporary resources disappeared, reconstruct and
qualify a new receiver using the [pause recovery instructions](pause_handoff_2026-10-20.md#recovery-and-temporary-resources);
do not relabel a rebuilt wheel as the old artifact.

## Browser acceptance remains separate

Python construction, state changes and HTML export cannot certify rendered pixels,
clipping, controls or camera framing. This session's UI inventory has no enabled
browser; attempting the integrated browser reports `Browser is not available: iab`.
Do not replace that missing observation with a screenshot claim or accept C6.

Open the generated self-contained `scene.html` in a WebGL-capable browser. If a
served page is needed, use the provider's existing preview tool:

```bash
/tmp/dockingmt-human-20261020/receiving/bin/python -m molsysviewer.preview \
    /tmp/dockingmt-3ptb-scene-20261023/output
```

Check receptor, pose, reference and box are simultaneously visible, the title
identifies rank/score/units, and pose/reference can be compared while rotating and
zooming the camera. In the live notebook check reference/box hide/show and frame
5 → 1 navigation, returning to rank 1. Python addon callbacks are not asserted to
run in a static HTML page. Retain a real browser observation and any failures in
#52 before deciding [C6](../MVP.md#gate-c6--basic-molsysviewer-integration).
Whole-Core acceptance still requires all other gates and credible scientific
validation; no public package or release is created by this work.

## Provider deliveries and deferred work

The closeout also synchronizes published SMonitor/ArgDigest/PyUnitWizard guide
copies through the official MolSysSuite tool. The [exact guide receipt](data/3ptb_scene/guides_2026-10-23.json)
records canonical commits/blobs/digests for all seven guides. This is documentation
delivery under #19, not a runtime upgrade or optional-feature activation; the
selected wheel/provider identities above are unchanged.

[MolSysMT #390](https://github.com/uibcdf/molsysmt/issues/390) is now resolved by
`3d5fea534`, preserving explicit template stereo declarations with conflicts and
strict correspondence admission. That delivery is not part of this unchanged
installed scene composition. The earlier notebook and explicit bounded declaration
retain their original identity; future adoption needs its own consumer checks.

The newer native copy delivery tracked by
[DockingMT #51](https://github.com/uibcdf/dockingmt/issues/51) is also separate.
This scene continues to call existing public independent-copy operations; it
does not migrate molecular storage or claim qualification of that newer provider.

Task-owned `/tmp/dockingmt-3ptb-scene-20261023` retains scene artifacts, notebooks,
logs and a source-free harness under [#50](https://github.com/uibcdf/dockingmt/issues/50).
Review by **2026-10-30**, with no automatic deletion. Keep the dependent original
receiver/environment/artifact while needed; their existing review date remains
2026-10-27. Shared environments and sibling worktrees are preserved.
