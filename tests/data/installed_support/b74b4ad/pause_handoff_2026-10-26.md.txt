# Pause checkpoint — 2026-10-26

The maintainer paused work after closing the native receptor qualification's
pending CI. Resume from this checkpoint and the [current roadmap](../ROADMAP.md),
then consult [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49).
The earlier [2026-10-20 handoff](pause_handoff_2026-10-20.md) retains the preceding
scientific workflows, original producers and scene recovery.

## Completed and verified

The current qualified source checkpoint is
`ae5940432b8672abf8efb96eb0e659151272e8c5`. Its
[terminal receipt](https://github.com/uibcdf/dockingmt/issues/49#issuecomment-6425206189)
closes the formerly pending CI verification:

- [CI 40149390711](https://github.com/uibcdf/dockingmt/actions/runs/40149390711):
  **1,231 tests passed per Python 3.11–3.14**, zero test skips, all seven jobs.
- Ordinary sibling/consumer installation, installed namespace/context checks,
  dependency closure and the actual exact-head Codecov upload execute successfully.
- [Policy 40149390941](https://github.com/uibcdf/dockingmt/actions/runs/40149390941)
  and [publication governance 40149390974](https://github.com/uibcdf/dockingmt/actions/runs/40149390974)
  succeed at the same source.
- The overlapping native writer/reader/projection/map selections pass **58 source
  cases** (96.44 s) and **58 ordinary-installed cases** (87.98 s), zero skips.
  The new three-case protein module is included, not added to those totals.

Actual molecular operations now delegated to MolSysMT include retained
connectivity, H projection/charge transfer in both roles, flexible source-free
permutation/reconstruction, viewer frame composition and preparation atom-map
composition. The actual provider-reduced native systems retain prepared aggregate
charges and original/derived assignment evidence.

[Ligand native export receiving](native_ligand_export_receiving.md) covers rigid,
one-cut and nested trees. [Receptor native receiving](native_receptor_export_receiving.md)
covers the real 181L system: 2,603 pre-typing atoms → 1,615 written atoms, with
988 H merged. Preserved native IDs allow direct preparation/export composition.
A consecutively renumbered copy correctly refuses the original ID-label chain.
This is representation/software evidence; biological protonation, affinity and
whole-Core scientific acceptance remain separate.

## Runtime and immutable artifacts

The qualified runtime remains MolSysMT
`3502232d802ee2927f6b6f5d19f0ae045777ecb5`, compatible ArgDigest
`3d1ec53c374098016452abab74706e9d80df5462` and MolSysViewer
`a61b75bc994e3ad674c3e7eafe53bb6b2a989c5f`.
Read-only inspection of newer MolSysMT
`c7fb92a6227777810e85e95980701ab0a143a6c8` finds the three writer-route files
unchanged; that revision is not runtime-adopted.

The ordinary installed consumer wheel retains its original producer
`fe8ad1351b8661b43957132236715115d495d795`:
`dockingmt-0.0.0+196.gfe8ad13-py3-none-any.whl`, 122,993 bytes, SHA-256
`962ce548821ee37a7b2cf986280de720ad39c989059da2dc3daa2c95c7ade05e`.
All 57 package/addon code files, wheel bytes and installed origins were reverified
on 2026-10-26. The later qualification and this pause change tests/documentation
only; they do not relabel or rebuild that artifact.

Original scientific archives, scene/notebooks and producer identities are retained.
The original 181L legacy PDBQT still has SHA-256
`c372bbb4a83414cc82ddbc2263424dfe18b20df8ae6d5362f978c0d445a82ccc`.
No historical search is repeated for this checkpoint.

## Decision and next work at resume

1. Read the latest state of
   [MolSysMT #214](https://github.com/uibcdf/molsysmt/issues/214). The requested
   presentation/caller-remark extension remains undelivered at this pause.
   Its contract must distinguish molecular IDs from output serials and bind
   the completed export map to the final actual bytes.
2. Decide whether to prepare a provider-owned contribution through a PR linked
   to that existing issue, or wait and choose independent DockingMT work from
   the accepted pilot/issue backlog. That priority question was not answered
   before the pause. No provider contribution has been started.
3. Keep the current production presentation until a provider route is received
   or a native-presentation compatibility change is explicitly accepted. Such
   a change has not been accepted. General molecular builders, serializers,
   label repairs and map rebinding belong to MolSysMT, not a new consumer fallback.
4. After receiving the supported writer contract, retire the covered production
   writer and adopt the known-source pose reader against its actual map/payload.
   Retain source-free and original-producer compatibility in the accepted scope.

The production writers/pose parser remain unchanged. #49/#33/#5 stay partial;
their broader work is not closed by the successful CI checkpoint.

HTML/browser review and C6 remain deferred under #52. No public package or Release
is published. Public file/pair/platform admission remains #30/#47; future publication
still requires the release-specific MolSysSuite notice and the maintainer's
package/Release availability announcement.

## Resources and recovery

Resources remain owned by [#50](https://github.com/uibcdf/dockingmt/issues/50):

| Location | Retained purpose | Review |
| --- | --- | --- |
| `/tmp/dockingmt-native-writer-20261024` | Protein probes, source-free harness, full CI bundles, original pending and final receipts | 2026-10-31 |
| `/tmp/dockingmt-continuation-20261026` | Final verifier, handoffs, source/artifact rechecks and suite inventory | 2026-10-31 |
| `/tmp/dockingmt-stage-maps-20261024` | Unchanged ordinary receiver, wheel, provider evidence and stable GH Run Receptor 1.3.0 | 2026-10-31 |
| `/tmp/dockingmt-human-20261020/environment` | Inherited dependency base under its existing ownership | 2026-10-27 |

Review dates are not automatic deletion. Preserve older artifacts and human/shared
environments. The latest read-only suite inventory preserves all sibling work and
behind states, the TopoMT version edit and OpenCASTP's two local commits ahead.
No sibling source or environment was modified.

If a temporary resource is unavailable on resume, recover the committed compact
evidence and owning issue receipts first. Use verified GH Run Receptor 1.3.0 to
inspect/capture the existing run rather than rerunning scientific producers.
The final verifier accepts GitHub's whole-job log archives; the earlier
step-member-layout assertion is retained as a verifier diagnostic, not a CI failure.

This pause commit changes developer documentation only. Its applicable gates are
report indexes, local links, synchronized-guide identity and reporting/governance
checks. Retain the completed scientific evidence at its original source/artifact
identities; no new scientific or public-artifact qualification is claimed for prose.
The pause's documentation commit uses a scoped CI skip, with those manual gates
recorded at its exact head in #49. This does not waive runtime, external-PR,
admission or publication gates. Revalidate affected code, inputs, environment or
scope when they change.
