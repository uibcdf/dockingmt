---
summary: Diagnose saved P59 total-score preference versus positional recovery.
issue: uibcdf/dockingmt#69
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [science, analysis, reporting]
guard: tests/test_p59_score_diagnostic.py
normative:
blocked_by: []
supersedes: []
---

# Saved P59 score and RMSD diagnostic

## What

Follow #67's returned-set/first-pose recovery gap with a retrospective
description of saved total scores and saved positional RMSD. The
[issue prescription](https://github.com/uibcdf/dockingmt/issues/69) precedes
the new score-pairing calculations. Original experiments remain historical;
other components' issues remain deferred.

## Inputs and analysis units

Authenticate the original ROOT-order archive SHA-256
`2129d7eed2b73bcf90737b2a6c722e3b8e9269abeba0ca3b1444df51f046634e`
and unchanged #67 summary SHA-256
`0d88030650a768c14e9940b2c58dd21c16465550518cedd5f64c557e3e7369fc`.
The latter's producer module hash is
`91ef4d7a591ff0d9904d5d26be93e9b1bad6116bbeba004325ea3974664064a5`,
published at `9b8677d82f37af3b916950516e0a888e378f55d9`.
Keep original archive/producer identities distinct from this analysis.

The archive has 24 runs. Select only P59's twelve runs and fifty poses:
native/first-fixed ROOT × seeds 7/42/2026 × exhaustiveness 1/8. Keep both
arms and all twelve cells, including runs without recovery. P69 and 3PTB
rows remain outside this diagnostic; seeds/poses are not independent complexes.
Join through the #67 result digests, run keys and original pose identities,
validating the projection against the original archive before using its RMSD.

## Prescribed questions and outputs

1. Compare actual saved list order with the recorded ascending `vina` policy.
   Retain positions, ranks, ties and any discordance without reranking or
   discarding a discordant run.
2. Report the first pose, earliest closest-RMSD pose, earliest recovered pose
   and lowest score among recovered poses, with relevant tied positions.
3. Compute every pose's total-score difference from first and the corresponding
   closest/recovered comparisons within each run. Preserve missing recovered
   contrasts explicitly. Positive differences mean less preferred scores.
4. Deliver twelve-run/fifty-pose tables, machine-readable records and separate
   per-run score–RMSD panels, with seed/effort and requested/returned counts.

Use saved `vina` empirical total docking scores only: literal
`kilocalorie / mole`, method `AutoDock Vina/vina` 1.2.7, lower preferred
direction, complete definitions/contexts and original ranking history.
Do not reconstruct a total from component terms. Preserve the original RMSD
criterion: 24 experimental heavy atoms, original shared frame, no alignment
or symmetry correction, inclusive cutoff 2.5 Å. No unit conversion is required.

## Interpretation and limits

Ascending saved scores plus positive recovered-pose differences would support
a finite mismatch between recorded score preference and this RMSD criterion.
This does not establish a general scoring defect or its chemical cause. Keep
ties and contrary cases; nonrecovering runs supply no recovered-pose contrast.
Existing preparation remains unassessed. Do not pool arms, correlate all poses,
test significance, infer affinity, invent a score/model, or rerank results.

The reader performs scalar record arithmetic only. Molecular inspection,
geometry, atom correspondence, scoring, search and preparation remain outside
this work and in their owning providers. Original archives and #67 outputs
remain unchanged; no runtime API, public package or live C4/C6 is qualified.

## Acceptance

Deliver dated methods/results linked from the overview, a case-specific
standard-library reader/check mode and bounded standalone figures. Validate
hashes, joins, units/definitions/context, counts, ranks/positions, ties and
missing observations with meaningful controls. Check mode recomputes numerical
and text outputs and verifies figure hashes without importing molecular or
plotting tools. Declare exact unshipped helper/data inputs through shared
installed-test support. Follow DMT-044 publication and report/resource custody.

At prescription checkpoint 414ff0e, the new numerical diagnostic had not run.

## Resolution — 2026-11-05

The [dated diagnostic](../validation/p59_score_diagnostic_2026-11-05.md) delivers
twelve-run/fifty-pose tables, a unit-labelled CSV, full machine-readable
provenance/contexts, within-run score contrasts and standalone PNG/SVG panels.
Both original inputs and all #67 outputs remain unchanged. The reader uses
saved scalar observations and performs no molecular or native operation.

All twelve saved lists follow the recorded ascending `vina` total-score policy,
with unique first-position score minima. In recovering effort-8 cases, recovered
scores are +0.472/+0.523/+0.480 kcal/mol above first in native ROOT and
+0.512/+0.511/+0.510 in first-fixed ROOT (seeds 7/42/2026). The first-fixed
seed-42 effort-1 recovery has a +0.535 contrast. Nonrecovering runs have explicit
unavailable recovered contrasts; ranks, ties and original ordering remain.
This supports a finite mismatch with the declared RMSD criterion without
establishing its chemical cause or a general scoring defect.

Twenty-nine new guards plus twenty #67 controls pass through shared support
outside the owner tree; another 24 administrative controls pass. Guarded cases
include altered definitions/units/contexts, mismatched joins, finite values,
rank/position/tie distinctions, retained discordance and missing contrasts.
Fresh check mode blocks molecular and plotting imports. Figures were inspected.
The helper/six outputs have exact shared support declarations, with no runtime
payload change. Hosted exact-head observation remains #28; provider/public
qualification and live C4/C6 remain separate and deferred as applicable.
