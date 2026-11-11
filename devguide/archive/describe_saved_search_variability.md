---
summary: Describe seed and effort variability in frozen search results
issue: uibcdf/bindingmt#67
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [science, analysis, reporting]
guard: tests/test_saved_search_variability.py
normative:
blocked_by: []
supersedes: []
---

# Saved-search seed and effort analysis

## What

Extend the existing scientific overview with a retrospective descriptive analysis
of seed/effort variability and returned-pose ordering. The overview already
reports first/any-returned recovery and RMSD ranges; this work adds resolution
by recorded seed/effort and cumulative recovery over collection positions.
This is the next proposed BindingMT-only task. Other components' issues remain
deferred at the maintainer's request.

## Declared inputs and analysis units

Use the three exact archives already bound by
[`build_summary.py`](../validation/data/evidence_synthesis_2026-11-04/build_summary.py):

- Original `3ptb_search/audit_2026-10-10.json.gz` and its distinct
  `3ptb_search/evaluation_2026-10-10.json.gz` saved-evaluation receiver. These
  represent one set of 24 searches, not 48 independent observations.
- `5x72_root_order/audit_2026-10-09.json.gz`, retaining 24 searches in its own
  declared ROOT-order challenge.

The [issue prescription](https://github.com/uibcdf/bindingmt/issues/67) records
their exact SHA-256 values before the new summary calculation. Preserve original
producer/input identities and the source/receiver distinction; archive bytes and
historical reports remain unchanged.

Keep eight arms separate: 3PTB rigid/flexible × native/negative, and 5X72 P59/P69
× native/first-fixed ROOT. Each arm contains seeds 7/42/2026 at effort 1/8.
Retain the 3PTB 2 Å/nine-heavy-atom and 5X72 2.5 Å/24-heavy-atom criteria,
original frame, no alignment and no symmetry correction.

## Questions and planned outputs

1. Tabulate each run's seed, effort, requested/returned poses, first/closest saved
   RMSDs, recovery and first recovered collection position. Preserve declared
   scientific ranks separately from positions.
2. Describe cumulative observed top-N recovery within each arm and effort, with
   explicit evaluated-run denominators and actual considered-pose counts. N
   beyond the returned count uses the available set; it invents no missing pose.
3. Compare effort 1/8 at the same recorded seed/arm using the saved outcomes.
   They are separate seeded searches, not assumed nested trajectories. Preserve
   all protocol differences; do not remove declarations to force the existing
   conservative public summary gate to pool them.

Produce a dated methods/results document, a small case-specific reproducer,
machine-readable derived records and standalone figures linked from the existing
overview. Register this analysis as retrospective, not as a new preregistered
docking experiment. Three seeds describe within-case variation; this work makes
no statistical-significance or general predictive-accuracy claim.

## Validation and ownership

Validate hashes, source/receiver association, complete expected seed/effort cells,
literal units/criteria, run/pose counts and recorded recovery. Report missing or
inconsistent information explicitly. Preserve the original 3PTB reporting failures
and later successful receiving as different stages. A reporting failure is not
an observed docking nonrecovery.

Read saved records only. Molecular operations, RMSD measurement, search/scoring,
preparation, atom matching and reranking are outside this work. No public API,
provider capability, package release or visible C4/C6 acceptance is introduced.
The existing BMT-044 evidence policy governs publication; #33 retains broader
scientific-profile acceptance.

## Acceptance

Deliver the declared outputs and a check mode verifying exact inputs and derived
records, with meaningful controls for denominators and position/rank distinction.
Keep original populations/producers separate and make reproduction steps explicit.
At prescription checkpoint d1435ff, the new numerical analysis had not been run.

## Resolution — 2026-11-05

The [dated methods/results](../validation/saved_search_variability_2026-11-05.md)
deliver the retrospective analysis, 48-run table, machine-readable records,
cumulative top-N and 24 within-seed effort comparisons, with standalone PNG/SVG
figures. The reader authenticates all three frozen archives, retains eight arms
and their separate 167/99 pose populations, and preserves original reporting
failures and later receiving. No new molecular or native operation is executed.

Twenty controls verify denominators, complete cells, source/receiver joins,
criteria, input integrity, invalid observations and position/rank independence.
The check-mode subprocess blocks molecular and plotting imports. Original
producers remain distinct from this analysis. P59's effort-8 recovered poses
first appear at position four for all three seeds in each ROOT arm while all
first poses fail; no general recovery/affinity claim follows. #33's broader
scientific acceptance, provider/public qualification and visible C4/C6 remain
separate. Other components' issues remain deferred.
