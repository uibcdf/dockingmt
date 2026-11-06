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

With an admitted result and its explicit molecular inputs, the existing public
entry is:

```python
import dockingmt as dmt

viewer = dmt.view(
    result,
    receptor=receptor,
    partner=partner,
    reference=reference,
    search_domain=domain,
)
```

`dmt.show` is an alias. This is an API composition example, not an instruction to
launch the deferred visual review. A detached saved result does not restore its
molecular inputs; use the declared [workflow prerequisites](human_workflow_review.md)
and [saved-result addon contract](pending_proposals/qualify_saved_result_addon.md).

## Docking Explorer — current bounded iteration

The existing Explorer and Search Domain panels are the first interface. Pose
selection uses collection/frame index, displayed separately from optional
scientific rank and identity. Named scores retain their existing descriptors
and units; absent meaning is explicit. Mounting and navigation perform no
implicit RMSD calculation. Live Jupyter control/canvas qualification remains
pending; successful Python widget tests do not establish visible behavior.

Mounted panels refresh after docking adapter/context actions and subscribe to
public frame callbacks with per-widget teardown. They publish separate state
records in the addon namespace and offer explicit Refresh for public scene
readback. MolSysViewer #291 has delivered synchronous notifications for public
Python player navigation. [Controlled source/private receiving](validation/player_notifications_receiving.md)
at Viewer `78ede79e2e345593db5bfe80d246d3f6c70bd005` verifies immediate addon
panel state after those calls; it is no longer a missing source capability.
The [reviewed public Viewer 0.24.0 build 1](validation/public_viewer_receiving.md)
does not provide that qualified handle/callback behavior. Its public-artifact
disposition remains MolSysViewer #294 and DockingMT #30/#47; do not infer a
compatible public pair or new minimum from source/private success.

Search-domain handles, rather than tag names alone, determine
cleanup ownership. Missing visuals are prerequisites; provider failures remain
errors. Clear/disable releases the docking binding and its owned shape outputs,
leaving molecular scene data with the Viewer.

Python state, DOM controls, kernel execution and actual rendered canvas remain
distinct evidence. Live controls/comm/pixels and C4/C6 acceptance are still
pending under #52/#60 and the maintainer's scheduling decision.

## Structured interactions — partial receiving

[E4/#80](pending_proposals/receive_docking_interaction_analysis.md) now receives
one bounded provider-only 3PTB workflow: normal/pm-fs profiles, typed/H5MSM
persistence, filtering, original-pose association and independent saved readers
pass at producer `5952053`. The [interaction guide](validation/installed_3ptb_interactions.md)
preserves original files, failed attempts, named definitions and scientific limits.
This is not whole E4 or visual acceptance.

Admission into the addon remains work. The analysis model includes five H added
by MolSysMT beyond the original thirteen-atom docking pose. Its atom/structure
indices must not be treated as the existing scene's indices merely because
labels or counts appear compatible. Use supported MolSysMT correspondence,
projection and query operations and MolSysViewer's generic interaction contracts;
report uncovered reusable needs in those providers. Preserve evaluated-empty
versus unevaluated data, method/units/producers and the original result. Loading,
navigation or showing an existing analysis must not silently prepare molecules
or recalculate interactions.

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

DockingMT owns docking-specific result, score/ranking and analysis-association
semantics. General molecular detection, characterization, geometry, identity,
editing and serialization must remain in MolSysMT; missing reusable tools are
requested there. Topographic, pharmacophore and elastic-network models retain
TopoMT, PharmacophoreMT and ElastNetMT ownership.

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
