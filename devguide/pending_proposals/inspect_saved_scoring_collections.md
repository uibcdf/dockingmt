---
summary: Inspect saved scoring collections through an explicit ordinary-installed example mode.
issue: uibcdf/dockingmt#77
status: active
opened: 2026-11-05
closed:
verification: asserted
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
