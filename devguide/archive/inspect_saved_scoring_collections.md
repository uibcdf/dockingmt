---
summary: Inspect saved scoring collections through an explicit ordinary-installed example mode.
issue: uibcdf/dockingmt#77
status: resolved
opened: 2026-11-05
closed: 2026-11-06
verification: measured
area: [examples, scoring, provenance]
guard:
normative: devguide/validation/result_audit.md
blocked_by: []
supersedes: []
---

# Inspect saved scoring collections

## What

Extend the #75 public example with explicit `--record-kind result` after #76's
collection-history correction. Preserve its default pose interface/output.

## How

Delegate to public result/pose audits, detached model readers and captured-input
integrity checks. Show stored pose order, score meaning, evaluation producers
and original docking provenance separately; preserve unknown evidence. Qualify
the exact example outside source with the unchanged #76 private reader wheel.

## Why

This is the next concrete E1 reading workflow under #73: a saved collection
must be inspectable without executing a backend or reconstructing molecules.

## What was refuted

No new runtime API, input-kind inference, ranking, comparison-context override,
molecular helper or scientific campaign is needed. A collection with absent
global provenance remains incomplete; evaluation history cannot replace it.

## Scope and exclusions

Read-only JSON interpretation/tutorial receiving. Molecular work stays MolSysMT-
owned. Provider changes, live observation, public delivery and fixed candidate
`905abc9` retain their existing identity/deferrals. Preserve #75/#76 receipts.

## Acceptance criteria

Compare old/new default pose output with the same ordinary-installed reader.
Receive saved native docking, the retained two-evaluation collection and missing
capture controls. Refuse changed score, future history, wrong independent digest,
source overlay and explicit record-kind mismatch. Preserve all original inputs,
scores, evaluations, ordering and producers; forbid external work. Record exact
example/input/wheel identities, resource bounds and all diagnostic outcomes.


## Completion — 2026-11-06

Example implementation `b87eb08` is qualified by the
[separate receipt](../validation/data/scoring_collection_inspection/receiving_2026-11-06.json)
and [usage guide](../validation/installed_scoring_inspection.md#explicit-collection-mode--2026-11-06).
Thirteen invocations include seven successful reads and six expected refusals.
Previous/revised default examples emit equal summaries with the same reader
and input. Native/scored/empty and missing/unknown-evidence collections retain
their declared scope; changed score/history, wrong digest, record-kind mismatch
and source overlay refuse. All input files and 63 reader runtime files remain
intact, with zero guarded operations or optional provider loads. The base consumer
is preserved and pip check passes. No new molecular result is computed.

The borrowing installation consumes the unchanged #76 private development wheel;
it is not a fresh/public dependency closure or qualification of fixed candidate
`905abc9`. Public APIs retain scientific admission and diagnostic ownership;
this unshipped example adds Argparse selection and JSON presentation. Original
#75/#76 receipts remain frozen. Lightweight local and final committed-source
governance apply before handoff; broad hosted receiving remains #28. Owned
borrowing/copy scratch is retired after handoff; unique evidence is retained under
#77/#50 for review on 2026-11-12. No watcher or heavy retry is scheduled, and
other-repository and visual deferrals remain.
