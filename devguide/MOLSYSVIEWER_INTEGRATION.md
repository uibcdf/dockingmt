# MolSysViewer Integration

## Goal

Docking should be explorable as a scientific result, not merely exported as coordinates.

DockingMT should eventually ship a dedicated MolSysViewer addon capable of understanding
`DockingResult` and `DockingPose`.

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

## Docking Explorer — DESIGNED FOR

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

MolSysViewer owns interactive presentation.

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
