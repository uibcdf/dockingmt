# MolSysViewer Integration

## Goal

Docking should be explorable as a scientific result, not merely exported as coordinates.

DockingMT ships `molsysviewer_dockingmt`, a dedicated MolSysViewer addon that
understands `DockingResult` and `DockingPose`. Its bounded interactive
qualification is tracked in [#60](https://github.com/uibcdf/dockingmt/issues/60)
and the [current proposal](pending_proposals/qualify_saved_result_addon.md).

Following the MolSysViewer ownership model, the addon belongs to the DockingMT repository
and package distribution. MolSysViewer provides the host API; DockingMT owns the docking
integration.

## Core MVP visualization

Display together:

- receptor;
- search domain;
- selected ligand pose;
- optionally native/reference ligand;
- pose rank and named scores.

A natural high-level interaction is:

```python
view.show(result)
```

or an equivalent explicit DockingMT addon API.

## Docking Explorer — current bounded iteration

The existing Explorer and Search Domain panels are the first interface. Pose
selection uses collection/frame index, displayed separately from optional
scientific rank and identity. Named scores retain their existing descriptors
and units; absent meaning is explicit. Mounting and navigation perform no
implicit RMSD calculation. Live Jupyter control/canvas qualification remains
pending; successful Python widget tests do not establish visible behavior.

## Richer Docking Explorer — DESIGNED FOR

A richer viewer could provide:

```text
Pose   Rank   Vina score   Other scores
----------------------------------------
1      1      ...
2      2      ...
3      3      ...
```

Selecting a pose should update the scene.

Potential layers:

- pocket/topographic surface;
- search domain;
- search guidance;
- constraints;
- ligand pose(s);
- molecular/preparation state information;
- hydrogen bonds;
- contacts;
- interacting residues;
- pharmacophore matches;
- flexibility field;
- pose clusters;
- receptor states.

A particularly expressive future scene could combine:

```text
pocket geometry
+
pharmacophore guidance
+
flexibility field
+
pose
```

## Separation of responsibilities

DockingMT owns docking scientific data and analysis.

DockingMT owns the docking-specific interaction in its addon. MolSysViewer owns
generic presentation, rendering, panel hosting and transport. General molecular
operations remain MolSysMT-owned.

Do not place essential scientific information only inside viewer state.

## Future MolSys-AI interaction

Structured result/viewer integration can later support requests such as:

```text
Show the three best poses interacting with Asp25.
Compare the top two pose clusters.
Show only poses satisfying this pharmacophore.
Display the pocket and residues contacting pose 4.
Show how this pose changes across receptor states.
```

This should emerge from structured DockingMT data, not from parsing rendered scenes.
