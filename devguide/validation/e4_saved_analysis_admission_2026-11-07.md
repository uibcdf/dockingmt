# Saved E4 analysis: prospective consumer admission

Owner: [DockingMT #80](../pending_proposals/receive_docking_interaction_analysis.md).
Subsequent receiving: [the separate saved-carrier selection](e4_saved_carrier_receiving_2026-11-07.md)
now passes normal/pm-fs and independent saved-record reading. The same-carrier
baseline is received; general projection and the consumer/addon API remain open.

This is a **source-reviewed recipe**, with a selected prospective saved-carrier
receiving below, not an executed workflow. It adds no API. The original heavy
local selection remains suspended and live-viewer acceptance remains deferred.
The resumed development objective permits a distinct, lightweight receiving
after its registration is sealed; no additional human confirmation is required
by the resource rule. Do not replay preparation/detectors or dispatch manual CI
automatically.

## Fixed evidence and provider sources

The [hosted success receipt](data/interaction_hosted_success_2026-11-06.json)
records producer `5952053328aac6f737e22906e984c0f9eb938dd7`, one selected original
pose (`pose_1`, position 1 of five), twelve detector calls across normal/pm-fs,
and independent saved readers. The profiles repeat the same case under two unit
policies. Earlier failed/interrupted attempts remain unchanged; the
[executed guide](installed_3ptb_interactions.md) retains its bounded claims.

| Component | Qualified source in that receipt | Separately inspected development sources; compatibility not received here |
| --- | --- | --- |
| MolSysMT | `00abb958fb93649131d5ce5fe5e12e90cf4900e9` | Local checkout `9e1f1b1ad8bf09446374ab6f04ca7208e2717936`; cached `origin/main` `82bfa1c82f1d48035679fa4630e81a2506b67bd6`. |
| MolSysViewer | `78ede79e2e345593db5bfe80d246d3f6c70bd005` | Local checkout/cached `origin/main` `1187fc187247aa2d20d01791856a541d50562bcb`. |

These are read-only local Git observations without a new fetch or pin change.
Signature inspection does not qualify a different artifact or the new composition.

The prospective baseline uses the existing private consumer payload (3867 files,
DockingMT source `a7422dfb9f8c3b1c8ede3d852e202dc33e4beefe`, MolSysMT source
`9e1f1b1ad8bf09446374ab6f04ca7208e2717936`) plus a new task-owned transport
overlay of the existing private Viewer wheel from `78ede79e` (641 files, wheel
SHA-256 `3d31a4d9edb7ed0e72fadcd81b3952196795218f55776478a7625b79e47e9e2a`).
Its original wheel receipt is
[preserved separately](data/addon_player/viewer_wheel_2026-11-03.json).
This is a new private composition to receive, not the original hosted runtime
or a public installation claim. No environment installation, provider checkout
update, dependency solve or wheel rebuild belongs to this selection.

Reuse the original [five-pose result](data/human_3ptb/native_result_2026-10-20.json.gz)
and the normal/pm-fs `association.json.gz` and eight H5MSM files under
[the preserved hosted directory](data/3ptb_interactions_hosted_5952053/).
Verify **stored and decompressed** bytes/hashes using the success receipt's
`selected_original_exports`; gzip is byte transport, not a molecular codec.
The result's stored SHA-256 is
`4b1f51cdeb135fd6785a181f6bb09a0d0f631ec3d9de7c169c88703748924249`.
The normal `retained_pose.h5msm` original SHA-256 is
`02f463d0e1f65794250ac39069d219fbeb12de13744e3661251b984fb6c417fe`;
the other profile/files retain their own recorded identities.

The association binds original states, scores, coordinate-record hash, thirteen
atom keys and the original-to-materialized-ligand correspondence. Its merged
ligand indices are `3220..3237`: the analysed carrier has **receptor_h3220 plus
ligand18**, one structure. Thirteen ligand atoms came from docking; five nonpolar
H have provider-generated local geometry. The **2011-atom prepared receptor**
in the preparation receipt is a different population. A scene built from that
prepared receptor and ligand13 would contain 2024 atoms; the saved analysed
carrier contains 3238. Inspect the actual destination rather than assuming this
example describes every scene. Original docking scores/states do not establish
energies for the expanded carrier; model suitability remains `unassessed`.

## Public recipe reviewed at the qualified pins

1. Verify inputs first and retain them read-only. In the separately registered
   receiving, load the complete carrier with
   `msm.convert(filename, to_form='molsysmt.MolSys')`; its named analyses are
   `hbonds` and `hydrophobic`. An independent layer read is
   `msm.h5msm.read_layers(filename, layers=['interactions'],
   analysis_names=['hbonds', 'hydrophobic'])`. A layer read alone cannot prove
   identity/geometry against another system. The old hosted reader already
   receives persistence; this increment receives a new consumer composition.
2. First use that **same complete saved carrier** as the baseline consumer input.
   `view.load(carrier, mode='replace')` is the source-inspected scene route, not
   received canvas evidence. Check its ordered molecular/state/H and frame/box
   axes, coordinates and complete named analyses before/after. Verify the retained
   thirteen ligand atoms physically against the original pose through the recorded
   correspondence and public provider getters; generate no replacement H.
3. For another docking scene, fix its actual axes and obtain an admitted
   provider-supported relationship to the saved carrier **before attachment**.
   Public `analysis.remap(atom_indices=..., structure_indices=...)` extracts or
   reorders a complete result and composes source maps. `msm.extract(...)` can
   extract the carrier and attached analyses together. Neither supplies missing
   correspondence to an independently reconstructed scene. No map is invented here.
4. After those checks, independent attachment can use
   `view.interactions.attach(full_result, name=..., assume_aligned=True)` or
   `view.interactions.load(filename, analysis_name=..., name=...,
   assume_aligned=True, atom_indices=..., structure_indices=...)`.
   The flag **declares**, rather than authenticates, matching atom/structure order,
   geometry and boxes. Loading extracts/reorders source axes; it does not embed a
   subsystem in a larger target or replace scene coordinates. Preserve existing
   names; conflicts must not overwrite them implicitly.
5. Retain complete provider persistence and associate it with the original
   result/pose using the existing receipt. Provider queries/pages support
   inspection/filtering; `Interactions.to_dict()`/`to_page()` are not complete
   codecs. Choose any future addon entry point from the received composition;
   this recipe adds no analysis field, binding class or automatic renderer.

Immutable source contracts inspected:
[conversion](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/basic/convert.py),
[layer reads](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/h5msm.py),
[query/remap](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/molsysmt/interactions/result.py),
[carrier extraction controls](https://github.com/uibcdf/molsysmt/blob/00abb958fb93649131d5ce5fe5e12e90cf4900e9/tests/native/test_molsys_interactions.py),
and [Viewer attach/load](https://github.com/uibcdf/molsysviewer/blob/78ede79e2e345593db5bfe80d246d3f6c70bd005/molsysviewer/interactions.py).

## Selected prospective baseline

The new [registration](e4_saved_carrier_receiving_2026-11-07.md) and
[notebook](e4_saved_carrier_receiving.ipynb) will seal the exact sources, scripts,
inputs, operation caps and guard/worker before calculation. Process **normal**,
then **pm_fs**, serially. Each profile reads its two saved complete carriers:
`retained_pose.h5msm` and `translated_geometry_control.h5msm`. Each destination
is the **same saved 3238-atom, one-frame carrier** being received, without a new
cross-carrier map. The original receipt's thirteen-atom correspondence remains
input evidence, not a newly invented witness. No 2024-atom scene, alternative
carrier, five-pose replication or addon API is admitted by this baseline.

Each process has one logical CPU (CPU0 affinity as fixed by the receiving guard),
`nice10`, one native worker, RSS at most 1 GiB, address space at most 2 GiB,
CPU time at most 45 seconds and wall time at most 60 seconds. Monitor an 8 GiB
task reserve; stop only owned work if a bound is threatened, retain partial
records and do not retry automatically. Headless provider/Viewer loading,
projection, persistence and queries **are molecular consumer operations** and
must be counted. Preparation, H addition, charge/type assignment, detectors,
native work, RMSD and alignment all have zero budgets. No manual CI, browser/
canvas observation or environment installation is part of the receiving.

This new selection does not restart the interrupted preparation/detector
selection or consume its unverified six-call reserve. Its authority comes from
the resumed objective and its concrete registered scope, not a new machine or
available headroom. The common rule in [AGENTS.md](../../AGENTS.md) prohibits
automatic **heavy** restarts and requires bounded, monitored local execution;
it does not create a separate human approval gate for every new saved-file read.

## General projection admission and stop conditions

The selected population is one original pose, its retained analysis, the saved
translated control, and normal/pm-fs repetitions. Analytic files remain original
controls, not extra docking poses. Original 3/2 retained and 0/0 translated
observations are **baseline** evidence, not promised projected counts. Preserve
definitions, measurements/units, participant roles, source maps, evaluation
scopes/coverage, assumptions and producer versions.

- Distinguish a complete result from a query view. `remap` refuses queries; named
  carrier attachment requires complete compatible analyses. A query/page must
  not be promoted to complete persistence or silently replace the original.
- A relation survives remapping only if **every atom of every participant** is
  retained. Record lost relations/occurrences and changed evaluation populations
  alongside retained ones. Dropped H/receptor atoms can remove observations;
  this is neither biological absence nor a new evaluation of the subset.
- Preserve evaluated-empty separately from unevaluated, absent and unsupported.
  The other four original poses are unevaluated. Repeating structure index 0
  duplicates occurrences; never use it to fill those different poses. Appended
  frames need explicit compatible carrier/order evidence, preserving old
  coverage without inventing evaluation for new frames.
- Receive provider refusals for missing alignment declaration, query-as-full,
  duplicate/out-of-range atom axes and name conflicts. Consumer preflight must
  stop for unknown/wrong target-map or frame relationships before attachment;
  accepting the flag is not an identity control. Report unsupported composition
  to its provider without local matching, coordinate editing or retry fallback.
- Compare normal and pm/fs physically through PyUnitWizard, using explicit units
  and a preregistered tolerance. Preserve caller policy, original files and
  detached before/after result, carrier, analysis and scene records on success
  and failure. Compare full analyses through provider typed persistence, not
  count equality. No full persistence is reconstructed from inspection JSON.
- Register **zero** preparation, H addition, charge/type assignment, detection,
  search, scoring, optimisation and alignment calls. Count provider reads,
  extraction/remap/query, scene loads and attachments separately. The baseline's
  resource profile is fixed above; broader rendering remains separate. A fresh
  independent reader verifies sealed records without molecular replay; numerical
  evidence and consumer-association evidence remain distinct.

**The separately sealed baseline now passes receiving.** Its actual scope,
ledger, sources/artifacts, failures and independent reader are linked above.
This recipe retains the original source-reviewed route. Preserve the original
heavy interruption, unknown counters and
diagnostics without relabelling them as a passing saved-carrier receiving.

**Projection to another carrier remains unready.** That later selection must
fix its destination and admit the receptor/ligand/frame correspondence, supported
projection/attachment calls and expected participant losses/coverage; the
same-carrier baseline supplies none of those missing maps automatically. Register
that distinct scope before running it. Headless association/persistence, usable
addon admission and deferred #52/#60 canvas acceptance remain separate outcomes.
Neither this recipe nor the prospective baseline accepts whole E4, public
delivery, affinity or biological validity.
