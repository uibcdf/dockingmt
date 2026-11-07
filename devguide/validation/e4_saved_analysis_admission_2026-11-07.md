# Saved E4 analysis: prospective consumer admission

Owner: [DockingMT #80](../pending_proposals/receive_docking_interaction_analysis.md).
This is a **source-reviewed recipe and future admission prescription**, not an
executed workflow or permission to run one. It adds no API. The local E4
computational hold and deferred live-viewer acceptance remain active; do not
replay preparation/detectors or dispatch manual CI automatically.

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

1. Verify inputs first and retain them read-only. In a separately authorised
   future receiving, load the complete carrier with
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

## Required receiving and stop conditions

The future population is one original pose, its retained analysis, the saved
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
  extraction/remap/query, scene loads and attachments separately. Loading or
  rendering needs its own resource/hold decision even without detectors. A fresh
  independent reader verifies sealed records without molecular replay; numerical
  evidence and consumer-association evidence remain distinct.

**Not ready for execution.** Before launch, #80 must fix the exact destination
carrier and admissible atom/structure relationship, resolve the missing
full-receptor-to-scene correspondence, select supported projection/attachment
calls and expected loss/coverage controls, and seal the script/notebook, sources
and artifact manifest. The registration must specify finite call caps, one
CPU/native worker, wall/CPU/RSS/address-space limits, live RAM reserve,
failure/custody paths and no automatic retry. The maintainer must review the
local E4 hold explicitly and choose the execution venue; this prescription does
not lift it or authorise CI. Headless association/persistence, usable addon
admission and #52/#60 canvas acceptance remain separate outcomes. This proposed
increment accepts neither whole E4 nor public delivery, affinity or biological
validity.
