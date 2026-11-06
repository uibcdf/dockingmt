---
summary: Attribute per-pose scoring histories correctly inside saved result audits.
issue: uibcdf/dockingmt#76
status: active
opened: 2026-11-05
closed:
severity: medium
verification: measured
area: [results, scoring, provenance]
guard: tests/test_scored_result_audit.py
normative:
blocked_by: []
supersedes: []
---

# Audit scoring stages inside saved collections

## What

At `289b7b7`, the unchanged native docking result audits as consistent even after
a detached copy receives unsupported per-pose scoring-history schema `99`.
The valid saved two-evaluation pose audits as consistent alone but, wrapped
unchanged by the public `DockingResult` constructor, produces 16 erroneous
`score_stage` contradictions. No molecular/native operation is required.

## How

Share the existing scoring-history crosschecks between pose and result audits.
Use pose-relative paths in collections, retain original result-level docking
provenance, and route additional score names to their recorded evaluations.
Conflicting original-docking/scoring ownership remains inconsistent. Absent
history for a scoring descriptor or absent collection provenance stays incomplete.
Preserve ordinary docking-only and standalone reports and strict ranking policy.

## Why

The concrete E1 workflow following #75 stores and inspects a collection carrying
named evaluations. Ignoring known histories misses contradictory evidence;
checking them as original docking stages invents contradictions. Ownership is
DockingMT's record semantics; molecular inspection/reconstruction stays MolSysMT.

## What was refuted

No new stage framework, molecular fingerprint/parser, score computation,
comparison-context override or altered ranking admission is required. Recorded
agreement does not prove coordinate/PDBQT correspondence or chemical validity.

## Scope and exclusions

Schema-1.0 record crosschecks only. Original scientific fixtures/producers and
the fixed private 0.1.0 candidate `905abc9` remain unchanged. This correction has
its own source and consuming evidence. No provider issue/change, new scientific
campaign, heavy local suite, release or visible acceptance.

## Acceptance criteria

Retain baseline reports; correctly audit valid, missing, malformed, future,
duplicate and contradictory histories within a collection. Preserve original
docking checks, input immutability, detached deterministic JSON reports and
unknown evidence. Targeted source/installed controls forbid molecular/native/
viewer work and preserve ranking comparability. Hosted CI supplies broader
supported-minor regression; report any pending gates explicitly.
