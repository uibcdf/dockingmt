---
summary: Add displaced-search-domain control to 1IEP validation
issue: uibcdf/dockingmt#15
status: resolved
opened: 2026-09-26
closed: 2026-09-26
verification: measured
area: [validation, search_domain]
guard: tests/test_1iep_search_control.py
normative:
blocked_by: []
supersedes: []
---

# Add displaced-search-domain control to 1IEP validation

## What

The public 1IEP case verifies one search box containing the native ligand. It
does not show how the same backend and inputs behave when the search domain is
deliberately wrong.

## How

Keep the pinned receptor, ligand, source map, seed, and Vina parameters fixed.
Shift only the box center by 30 Å along x, confirm that every native ligand
atom lies outside the new box, and store a separate complete DockingMT result
manifest. Report the control poses, scores, and source-referenced RMSDs beside
the original run. Use the stated 2.5 Å cutoff to flag near-native poses.

The source-linked control returned three poses with scores -4.106, -4.074, and
-4.064 kcal/mol and heavy-atom positional RMSDs 25.364, 22.894, and 22.483 Å.
The reference run returned one pose at -13.286 kcal/mol and 0.897 Å. Both runs
used the pinned PDBQT bytes, seed 42, one CPU, and Vina 1.2.7.

## Why

This is a methodological negative control for the search domain. A score can
exist even when the native site was excluded. It is not a biological inactive
ligand control and does not measure selectivity or affinity.

## What was refuted

The presence of returned poses is not proof that the chosen search region was
appropriate. A valid Vina score cannot substitute for source-referenced pose
geometry.

## Scope and exclusions

DockingMT owns search-domain projection, protocol execution, pose normalization,
and provenance. The pinned, externally prepared PDBQT chemistry remains
unassessed; MolSysMT preparation capabilities are not duplicated here.

## Acceptance criteria

- The control excludes every mapped native ligand atom by geometry.
- Both runs submit the same pinned PDBQT bytes and differ only in search box.
- The control has a separate reconstructable result manifest and pose metrics.
- No control pose falls within 2.5 Å of the native reference in the recorded run.
- A durable test fails if the control box overlaps the reference.

## Resolution

The validator now checks that the original box contains every source atom and
that the 30 Å displaced box contains none. It runs both domains with identical
pinned PDBQT inputs and protocol settings, writes separate complete result
manifests, and reports each pose's score and source-referenced RMSD. The control
returned three poses, all at least 22.483 Å from the native reference and thus
outside the declared 2.5 Å near-native threshold. Its scores remained finite,
showing why a score must be read alongside the search-domain and pose geometry.
`tests/test_1iep_search_control.py` guards the displaced-box geometry and the
overlap rejection.
