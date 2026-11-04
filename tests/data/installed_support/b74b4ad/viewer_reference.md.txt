# Docking poses and reference frames

`dockingmt.view(result, reference=reference, view=existing_view)` replaces the
displayed docking complex. Reusing a viewer therefore does not accumulate
duplicate receptors and poses. A result's structures correspond to pose ranks:
frame 0 is rank 1. Reconstruction still requires checked source atom identity.
The receptor and each reconstructed pose must contain exactly one structure;
select the receptor conformation through MolSysMT before rendering a result.

The independently usable public operation
`molsysviewer_dockingmt.build_docking_reference_system(reference, n_poses)`
prepares a detached reference through public MolSysMT conversion, copy and
extraction:

- One static structure is explicitly repeated to the pose count.
- Exactly N reference structures are copied in their existing order, comparing
  reference frame k with pose frame k.
- Other counts and non-positive/non-integer pose counts raise `ValueError`.

No alignment, interpolation, inferred atom correspondence or chemical
preparation is performed. Source coordinates, units and declared structure
attributes remain owned by MolSysMT; input systems are not mutated. Repetition
preserves the static reference's declarations, including time when present.
It does not invent a time axis to match arbitrary trajectories.

The reference count is checked before replacing the scene. Provider load and
initial-player failures propagate, retaining the original exception. No render
success event or completed result state is published on failure. Multiple
provider calls are not a transaction: if reference addition or player movement
fails after replacement, the scene may be partially changed. Correct the input
and reload explicitly; the runtime retains the last completed result.

## Provider contract and temporary compatibility

The reference is loaded with `mode='add'` and
`structure_pairing='by_index'` when that parameter is explicitly present in the
public `view.load` signature. Arbitrary `**kwargs` does not advertise support.
There is no catch-and-retry on `TypeError` or other provider errors.
The unchanged CI-pinned legacy viewer receives its existing load signature.

This bounded compatibility branch is tracked by
[DockingMT #37](https://github.com/uibcdf/dockingmt/issues/37) and
[MolSysViewer #151](https://github.com/uibcdf/molsysviewer/issues/151).
DockingMT maintainers will review it by 2026-11-03 and remove it when published
explicit pairing support is qualified across the supported provider profiles.
The provider owns time/cell compatibility and loading behavior. No minimum
published version or committed delivery of the candidate is asserted here.
The consumer handoff requests an inspectable public signature and exact
committed/published migration identity. No sibling source files were changed.

## Measured integration — 2026-10-03

The editable `molsyssuite@uibcdf_3.14` environment uses Python 3.14.7 and Vina
1.2.7. The full suite passes **706 tests without skips in 133.23 s**, using
MolSysMT `c19a47ada0c2279029abfa296cf915560610ad9a` and MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889`, the unchanged Python 3.14 CI pins.
`tests/test_viewer_reference.py` adds 22 cases covering counts, source ownership,
time/box and non-default pm/fs units, explicit/legacy signatures, original
loading/player failures, reload and frame correspondence. Existing addon and
native 181L redocking controls remain included.

The same 32 focused cases pass in **30.16 s** against an isolated snapshot of
the in-progress MolSysViewer tree, retaining the pinned MolSysMT provider.
Its HEAD is `924da3a32111d8994639e8a72cb901ebeb8f870a` with uncommitted changes.
[Source evidence](data/viewer_reference/candidate_source.json) records the
633-file Python source inventory digest and individual boundary file hashes.
This is candidate integration evidence, not released viewer qualification.

The [executed notebook](viewer_reference.ipynb) uses real seeded Vina poses
from 181L with explicitly provisional preparation. Four code cells check
public reference preparation, molecular coordinate correspondence, player
movement, repeated result loading and rejection before scene mutation. Its
saved outputs use the CI-pinned viewer. Candidate execution is recorded
separately in [the notebook receipt](data/viewer_reference/candidate_notebook.json).
Neither execution certifies browser graphics or docking accuracy.

The legacy viewer emits `RegionWithoutOwnVisualWarning` when visibility is
toggled on the reference region without its own representation. These tests
verify the DockingMT command/runtime boundary; they do not claim that legacy
visibility changes browser graphics. The candidate supports masking such
regions through the whole representation. This distinction is handed off in
MolSysViewer #151 rather than bypassing its representation policy here.
Provider H5MSM deprecation, pandas future and structural-attribute-drop warnings
also remain visible; molecular field completeness is not inferred from a
successful display. The full stable run reports 57 warnings, the candidate
focused run 27.

Reproduce the test boundary with:

```bash
python -m pytest tests/test_viewer_reference.py tests/test_viewer_addon.py \
    tests/test_redocking.py --receptor=llm
```

Set `PYTHONPATH` to the qualified provider archives for exact-source evidence.
The notebook records actual import origins and the original 181L SHA-256. Its
kernel is the shared Conda environment, not the launching shell's Python.
