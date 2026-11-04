---
summary: Report all-returned pose recovery independently of requested top-N.
issue: uibcdf/dockingmt#61
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: measured
area: [analysis, validation, aggregation]
guard: tests/test_redocking_summary.py::test_any_returned_recovery_can_occur_beyond_every_requested_top_n
normative:
blocked_by: []
supersedes: []
---

# Explicit any-returned recovery in saved redocking summaries

## What

The accepted audit/panel workflow needs recovery anywhere in the returned set
distinguished from first/top-N recovery. A near-reference pose can appear beyond
the largest requested N. Existing per-case closest-pose data supports the metric,
but the public collection summary does not expose its aggregate directly.

## How

Add `any_returned` to the schema-1.0 collection output, using only validated saved
closest-pose recovery. Share the existing evaluated/submitted denominator arithmetic
with top-N, preserving all previous arguments, compatibility and top-N values.
Empty evaluated results are nonrecovery; failures remain unknown. With no evaluated
reports, the field is null and no comparison policy is inferred.

## Why

This makes audit E6/Q2's returned-set versus ordering distinction available through
the existing public API. It does not require molecular inspection, geometry,
re-ranking, seed-pooling policy or a campaign abstraction. The 5X72 evidence is
motivation, not a new calculation or evidence that one physical cause is known.

## What was refuted

Top-5 is not any-returned recovery when more poses exist. Failed cases are not
observed nonrecovery, and no evaluated policy exists in an all-failure collection.
No molecular provider gap is filled in DockingMT.

## Scope and exclusions

Additive output field only; exact cohort compatibility and finite saved-report
admission remain unchanged. Old summaries retain their original bytes/producers;
an absent historical field is not a false recovery observation. The new field
describes returned poses, not every internal Vina sample or predictive accuracy.

## Acceptance criteria

Controls cover recovery beyond every requested N, positive/negative/empty/failure
denominators, null-policy cases, detachment, fresh offline reading and unchanged
compatibility. Relevant summary/evaluation tests and administrative gates pass.
The public contract and DMT-038 document the additive field and scientific limits.

## Initial source evidence

Before implementation, six selected checks fail with the missing `any_returned`
key, including null-policy and evaluated-empty controls. This is feature absence,
not a claim that prior top-N summaries were numerically wrong. The implementation
introduces no molecular/backend call and preserves earlier qualification scope.

## Resolution and source validation — 2026-11-04

The current source returns the additive aggregate with unchanged arguments,
exact policy admission and original top-N output. Two new independent scenarios
exercise a recovered sixth pose beyond top-5 and mixed positive/negative/empty/
failure denominators. Existing null-policy/empty, detachment, incompatible
declarations and fresh offline reader controls cover the extension as well.

The selected summary/evaluation gate passes **135 tests**, no failures/skips,
81.27 s, in the routine editable Python 3.14 environment. It retains 39
LegacyH5MSMWarning and one StructuralAttributeDropWarning. The source extension
does not qualify a new installed/public artifact or molecular/scientific model.
No original record, provider pin, dependency or installed receiver is changed.

[The public contract](../validation/redocking_summary.md), DMT-038 and README
describe the additive schema-1.0 field and historical-absence semantics. Core
status now names its original scientific/installed baseline separately from this
source change. Administrative/committed-export checks and exact-source hosted
recovery belong to the issue closeout. This completes #61's bounded API extension;
the panel's molecular/provider/state/environment work remains under #33/#49.
