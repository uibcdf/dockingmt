---
summary: Attribute per-pose scoring histories correctly inside saved result audits.
issue: uibcdf/bindingmt#76
status: resolved
opened: 2026-11-05
closed: 2026-11-05
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
BindingMT's record semantics; molecular inspection/reconstruction stays MolSysMT.

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

## Resolution and executed evidence — 2026-11-05

Implementation `d4aac964732bf6bdb1637f5297ccf95f3d3a272d` shares the existing
private history checker. The [separate receiving receipt](../validation/data/scored_result_audit_2026-11-05/receiving.json)
binds source, installed bytes, unchanged original inputs and canonical reports.
Source Python 3.14 passes 130 record tests, excluding one native execution case.
The private installed Linux Python 3.12.16 reader passes 83 tests; all 63 new
runtime files match its wheel before/after, and 62 non-generated files match
committed source. The generated version has its own digest. Original docking
and standalone-pose report contents remain equal to the retained baseline.

The guard's 19 cases address ignored malformed/future histories, false stage
attribution, actual contradictions/duplicates, missing evidence, producer overlap,
original-docking preservation, strict ranking contexts and detached reports.
Missing collection provenance stays incomplete; the two-evaluation collection
has zero invented contradictions. The appended-stage case is synthetic record
mutation only. It is not a new native evaluation or a molecular identity check.
Installed receiving blocks optional native/viewer imports and molecular/native/
viewer operations, with zero attempts; original base consumer bytes/metadata
remain intact and pip check passes. This narrowed selection consumes no staged
helper namespace; the declared full installed suite/support gate is unchanged.

An initial full export stopped at local disk quota before building or creating
an environment. Only its owned partial archive was retired. A minimal package/
test/data export and borrowing installation supplied the separate installed
receipt. The wheel truthfully uses the configured `0.0.0+unknown` fallback in
this Git-free private context; it is not the fixed 0.1.0 artifact. One retained
pytest assertion-rewrite warning concerns preimported SMonitor. No native
execution or new scientific campaign occurs. Hosted broad regression remains
tracked separately in #28; this focused defect resolution does not qualify
another source, dependency closure, public platform or whole Extended E1.
