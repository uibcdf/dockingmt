# Pause checkpoint — 2026-10-20

**Paused at the user's request before visualization.** Start here when resuming.
The three authorized steps are complete: reconstruct the installed environment,
consume delivered MolSysMT input/symmetry tools, and execute the human workflow
through evaluation and result recovery. No viewer scene or browser rendering was
executed. The next action is a discussion with the maintainer, not another search.

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), with human
workflow coordination in [#33](https://github.com/uibcdf/dockingmt/issues/33).
This checkpoint changes documentation and retained evidence only.

## Read these first

1. This handoff and the [current roadmap](../ROADMAP.md#current-execution-checkpoint--2026-10-20).
2. The executed [human notebook](human_3ptb_workflow_2026-10-20.ipynb), especially its
   final pre-visualization stop, and the [workflow contract](symmetry_redocking.md#executed-installed-workflow--2026-10-20).
3. The [qualification manifest](data/human_3ptb/qualification_2026-10-20.json),
   [source CI receipt](data/human_3ptb/terminal_2026-10-20.json) and
   [terminal owning-issue report](https://github.com/uibcdf/dockingmt/issues/49#issuecomment-6298468447).
4. For scene planning, the existing [MolSysViewer integration design](../MOLSYSVIEWER_INTEGRATION.md),
   [viewer/reference contract](viewer_reference.md) and Core gates in [MVP](../MVP.md).
   These are starting contracts, not evidence that the present human scene passed.

## What completed

- A fresh isolated Python 3.14 provider environment and ordinary wheel receiver
  were created outside the source checkout. Installed import origins, all 60
  required package files, wheel identity and dependency closure were verified.
  The selected installed contracts pass **277 tests, zero skips/deselections**.
- Compressed PDB input goes through public MolSysMT APIs. Optional symmetry
  evaluation also delegates graph correspondence and geometry to MolSysMT. The
  default positional RMSD, result order, ranking and summary criterion are intact;
  the corrected measurement has its own report. Neither route fits or aligns poses.
- The human notebook used the original compressed 3PTB source, explicit audited
  receptor/benzamidinium preparation and a preregistered rigid/native-box seed-7
  search. **Exactly one new native search returned five poses.** Its parameters,
  submitted bytes and native result are preserved.
- The initial notebook correctly refused incomplete stereochemistry metadata.
  A subsequent complete execution restored that same native result and explicitly
  declared `atom_stereochemistry='unspecified'` on a detached chemical context via
  MolSysMT. It performed no additional search. These are two recorded executions,
  not one uninterrupted green run or a generic downstream stereochemistry repair.
- All **24 historical rows / 167 poses** were received without repeating their
  searches. Original positional RMSD agrees within `1e-10 angstrom`; energy
  vectors and containment agree. Optional symmetry is recorded separately.
  Original failures, archives and producers remain unchanged.
- Exact-head source CI at `4695041ea8923bdf6180d5a86d66ebe015af1789`
  passed **1,145 tests with zero skips on each Python 3.11–3.14**, quality,
  distribution governance, suite policy and actual coverage upload. This source
  receipt is separate from the bounded installed selection and scientific validity.

## Producers and retained evidence

| Boundary | Identity / evidence |
| --- | --- |
| Implementation and original wheel producer | `1decee504b112cfd92026c52dcbe22449de30f4f` |
| Executed notebook, final regression and qualified source head | `4695041ea8923bdf6180d5a86d66ebe015af1789` |
| Ordinary wheel | `dockingmt-0.0.0+180.g1decee5-py3-none-any.whl`, 123,838 bytes |
| Wheel SHA-256 | `24cfe209935b9bcdef371590427dc74818f23eece6711171346c72402c02ba4e` |
| MolSysMT | `c35252d89a28a8faff11e0014bda91312167f549` |
| ArgDigest | `3d1ec53c374098016452abab74706e9d80df5462` |
| MolSysViewer | `a61b75bc994e3ad674c3e7eafe53bb6b2a989c5f` |
| Installed-test SDK | `738fe8dd731abb99dac421b0bb2acc8564110180` |
| Native MolSysMT extension SHA-256 | `feb001379201b92690eadf04fd0be6b710cdfe50bad240feba26cf666e19b41b` |

The versioned [data directory](data/human_3ptb/) contains the original fresh
[native result](data/human_3ptb/native_result_2026-10-20.json.gz),
[admission](data/human_3ptb/admission_2026-10-20.json.gz),
[evaluation](data/human_3ptb/evaluation_2026-10-20.json.gz),
[historical receiving](data/human_3ptb/saved_receiving_2026-10-20.json.gz),
environment, installed origins, kernel/cell receipts and qualification manifest.
The separately added terminal receipt records completed source CI; it does not
rewrite the earlier qualification manifest or relabel the wheel producer.
The closing documentation commit receives normal CI, reported in the owning issue.

Local closeout checks pass: 29 administrative contracts, report-index regeneration
and verification, Ruff lint/format, 69 local links in the changed Markdown files,
all 16 original qualification-manifest members, unchanged original wheel digest
and exact copies of the two newly retained receipts. All seven synchronized guides
match their current remote canonical bytes. Receiving `pip check` still passes.
No scientific code, dependency, input or notebook execution changes in this handoff;
the earlier scoped scientific evidence retains its producer and limits.

## Where to resume

1. **Discuss and agree the first visual question and acceptance criteria.** The
   suggested minimal scene shows receptor, reference ligand, one rank-1 pose under
   its named ranking criterion and the actual search domain. Preserve the shared
   coordinate frame, units, source identities and visible object labels. The
   maintainer has not yet accepted this scene or chosen among pose comparison and
   rigid/flexible comparison alternatives.
2. After agreement, inspect the existing DockingMT/Viewer public tools against
   that concrete scene. Molecular selection, copying, conversion or other general
   system manipulation belongs to MolSysMT; viewer behavior belongs to MolSysViewer.
   Keep docking decisions and orchestration in DockingMT. Propose missing reusable
   operations as issues in their providers, linked from the consumer evidence.
3. Restore the saved result for the agreed visualization; a new docking search is
   not required. Validate observable scene behavior and provenance before deciding
   C6. Review all Core gates before claiming whole-Core completion, then choose the
   next scientific workflow using `../moli-vertical-pilots` as local inspiration.
   Do not publish private pilot content.

There is no known technical blocker to planning that bounded scene. C6 and
whole-Core acceptance remain open. No new implementation or scene design is
authorized by this pause checkpoint itself.

## Recovery and temporary resources

Task owner [#50](https://github.com/uibcdf/dockingmt/issues/50) retains
`/tmp/dockingmt-human-20261020`; review by **2026-10-27**, with no automatic cleanup.
See the [actual resource disposition](data/human_3ptb/resource_closeout_2026-10-20.json).

- `environment/bin/python`: normally installed pinned providers and native engine.
- `receiving/bin/python`: ordinary original wheel, inheriting task dependencies.
- `wheels/`, `sdk/`, `sources/`, `harness/`: artifact, frozen SDK, detached provider
  sources and source-free receiving harness.
- `human-output/`: initial admission and original native result;
  `human-recovered-output/`: completed receiving/evaluation output.
- Initial failed and completed notebooks, execution scripts, original installed
  logs and complete CI bundles retain diagnostic and producer evidence locally.

Before reuse, check that both prefixes and the original wheel still exist, verify
the wheel digest, actual module origins, `pip check` and recorded provider/native
identities. Work outside the checkout without an editable production overlay.
The notebook documents `DOCKINGMT_HUMAN_DATA_ROOT`, a new never-overwritten
`DOCKINGMT_HUMAN_OUTPUT`, `DOCKINGMT_EXPECTED_PREFIX` and explicit
`DOCKINGMT_HUMAN_RESTORE_FROM` for restoring the original result without a search.

If temporary resources disappeared or drifted, use the committed environment and
identity receipts to qualify a new receiver. A rebuilt wheel is a new producer;
never assign it the old artifact's digest or evidence. The previous 2026-10-13
prefixes were already absent at reconstruction; their historical receipts remain
valid records of their original scope. No task-owned kernel or scientific process
needs to remain active. Shared environments and sibling worktrees are preserved.

## Open work retains its owner

- [MolSysMT #390](https://github.com/uibcdf/molsysmt/issues/390): reusable
  stereochemistry handoff from chemical templates; the bounded explicit context
  declaration does not resolve the provider proposal.
- [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49): remaining molecular
  projection/export maps, native pose/permutation and selected connectivity needs
  stay provider-owned. Delivered gzip and symmetry support do not close all of #49.
- [#30](https://github.com/uibcdf/dockingmt/issues/30) and
  [#47](https://github.com/uibcdf/dockingmt/issues/47): public artifact/channel/pair
  admission, complete installed qualification and untested platform/browser scope.
  This controlled wheel is not a public release.
- Chemical/scoring hypotheses and broad biological performance still require
  informative scientific validation. Green CI does not establish those claims.
- Shared environment closure and source acquisition remain
  [MolSysSuite #82](https://github.com/uibcdf/molsyssuite/issues/82) and
  [#31](https://github.com/uibcdf/molsyssuite/issues/31); do not alter the shared
  routine environment to repair this task's isolated runtime.

These broader issues do not require implementation before the scene-planning
discussion. No owning issue is closed by this handoff.
