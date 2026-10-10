---
summary: Retire remaining consumer implementations of general molecular operations
issue: uibcdf/dockingmt#49
status: partial
opened: 2026-10-10
closed:
verification: measured
area: [molsysmt, preparation, viewer, architecture]
guard: tests/test_molecular_delegation.py
normative:
blocked_by: []
supersedes: []
---

# General molecular operations belong to their provider

## What

The [owning review](https://github.com/uibcdf/dockingmt/issues/49) distinguishes
actual MolSysMT delegation from remaining consumer duplicates. The maintainer
requires general molecular operations to be proposed and implemented in MolSysMT;
pharmacophoric operations belong to PharmacophoreMT. DockingMT selects and
interprets docking workflows and consumes these tools.

## How

The first migration removes manual coordinate concatenation from
`build_docking_complex_system`. Every pose frame is composed with public
`msm.merge([receptor, ligand_frame])`; public `msm.append_structures` collects the
frames. Static-receptor pairing, pose order and the requirement for a verified
source ligand remain DockingMT decisions. No local molecular merger or new
dependency is introduced.

The three new guards exercise distinct ligand placements with the static receptor,
input immutability, default and pm/fs unit policies, actual public delegation for
every frame, and propagation of a later provider composition failure. Existing
viewer/result contracts exercise real pose reconstruction and viewer navigation.
These are molecular consumer contracts, not docking-quality measurements.

Executed provider remains `5bd893c85fe8d211663b2b1f865f5f1d2c382a90`, with the existing
qualified ArgDigest and Viewer sources. No provider upgrade, environment change,
native rebuild or sibling worktree edit is part of this migration.

Local selected validation: 40 viewer, molecular-delegation and result tests pass
in 26.04 s, with 37 existing provider warnings. The reporting check passes
separately (four cases including three repeated new guards, 6.23 s): **41 distinct
selected tests**, no skips. Ruff lint/format, generated indexes, all seven
registered guide copies, contributor routing and document links pass. Required
four-minor hosted CI is a separate exact-commit checkpoint.

## Why

The previous path merged the first frame publicly but assembled later frames with
NumPy concatenation, a copied topology and coordinate replacement. Calling the
provider for every frame makes it responsible for molecular composition and
attribute handling; its failures propagate instead of being bypassed.

## Remaining work and bounded migration

- **Available typing:** MolSysMT already owns named AutoDock classification. Retire
  the legacy consumer heuristics through an explicit compatibility decision under
  [#5](https://github.com/uibcdf/dockingmt/issues/5), preserving safe rejection and
  named-method choices.
- **Projection:** retained/omitted H, charge aggregation and derived atom maps
  belong to [molsysmt#223](https://github.com/uibcdf/molsysmt/issues/223). Its public
  operation must perform the transform, not merely describe a consumer transform.
- **Serialization:** public native PDBQT output is available under
  [molsysmt#214](https://github.com/uibcdf/molsysmt/issues/214). Its formatting differs
  from the legacy consumer output. Qualify the complete charge/type/tree/map
  profile, explicitly retain old producer bytes and decide representation
  compatibility before replacing writers. Do not rewrite historical archives.
- **Poses and flexible source-free reconstruction:** provider MODEL-aware reading
  and export/source maps belong to
  [molsysmt#226](https://github.com/uibcdf/molsysmt/issues/226) and #223. Keep the
  prepared atom axis explicit; provider extraction does not supply an arbitrary
  atom reorder. Do not add a consumer reordering or molecular parsing algorithm.
- **Connectivity:** the existing retained-graph traversal remains the bounded
  exception under [molsysmt#348](https://github.com/uibcdf/molsysmt/issues/348), with
  its existing review date 2027-01-06.
- **Source-free conversion:** replacing PDB reconstruction with native PDBQT
  conversion can retain molecular types/charges and restore full coordinate and
  charge precision through public setters. That adds mechanics to the native
  representation, exposing the old pinned provider's merge defect in
  [molsysmt#352](https://github.com/uibcdf/molsysmt/issues/352). The provider fix is
  delivered but its compatible consumer adoption still needs qualification.
  Do not silently discard mechanics or implement a downstream merger to bypass
  this requirement. The conversion draft is not integrated in this first slice.

The remaining historical conversion/writer/heuristic routes are tracked here and
in [#33](https://github.com/uibcdf/dockingmt/issues/33); they are not architectural
acceptance. Responsible role: DockingMT contributors. Review by 2027-01-06.
Removal requires a qualified supported provider operation covering the existing
units, inventories, correspondence, source immutability and explicit preparation
attribution. They must not be generalized while adoption is pending.

## What was refuted

Successful current tests do not prove that all molecular operations are delegated.
Source inspection of a newer provider does not qualify its runtime, installed
artifacts or scientific compatibility. MOLI's platform architecture does not
transfer provider implementation ownership to DockingMT. Independent finite
checks of provider geometry in developer controls are not a replacement geometry
API. No current missing pharmacophoric capability was established, so no
speculative PharmacophoreMT implementation or issue is introduced.

## Scope and exclusions

Keep #49 partial. This slice does not close #5/#33 or the provider proposals.
No new scores, searches, optimizations, public release or artifact admission.
The previously completed, unintegrated seven-point scientific producer and raw
archive remain unchanged and separate from this migration's validation.

## Acceptance criteria

Delegate each reviewed general operation through a supported provider contract,
or retain a current bounded owner-linked exception and removal condition. Verify
actual calls and user-visible identity, units, failure and provenance behavior.
Preserve docking decisions, original scientific inputs/producer bytes, and human
work in sibling checkouts. Provider maintainers own their delivery decisions.
