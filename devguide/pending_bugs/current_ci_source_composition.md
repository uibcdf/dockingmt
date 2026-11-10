---
summary: Current source CI declarations differ from the received development composition.
issue: uibcdf/dockingmt#100
status: partial
opened: 2026-11-09
closed:
severity: medium
verification: reproduced
area: [ci, dependencies, provenance]
guard: devtools/tests/test_ci_source_composition.py
normative: devguide/validation/ci_source_alignment_2026-11-09.md
blocked_by: [uibcdf/molsyssuite#178]
supersedes: []
---

# Current versus frozen source contexts

## What

The original ordinary CI revisions and current editable receiving select distinct
ArgDigest/MT/Viewer source generations. Original E4 and fixed0.1.0 candidate
receivers retain their independent source identities. New MT metadata declares
Jinja2 and stronger bootstrap floors absent from the original current environment.

## How

Follow [the prospective selection](../validation/ci_source_alignment_2026-11-09.md).
Align current declarations with exact already received sources, preserve frozen
contexts through separate source IDs, use shared context preflight and verify
source/declaration bindings with adverse guards and actual routine3.14 provenance.

## Why

CI must select a reviewed reproducible context. A local source PASS is not proof
of another source generation, solver closure, native build or hosted execution.

## What was refuted

No provider regression or new public dependency floor is established. No sibling
fix/build, new installer or generic source-workflow abstraction is required.

## Scope and acceptance

Receive the bounded configuration delivery and preserve old failures/contexts.
Keep hosted/native/public/platform qualification explicitly owned under the
broader existing issues; this correction cannot close their missing evidence.

## Delivered configuration; receiving limits

The new source/bootstrap/frozen-context declarations pass 101 administrative tests
and 26 subtests after the generated report index is refreshed. The original 13
adverse failures/one pass and one index-only failure are retained. Actual old
source-context receiving fails at the original revision mismatch; after alignment,
actual routine3.14 receiving remains refused by the SDK's documented HTTPS-only
origin profile because the installed development clones use SSH remotes.
MolSysSuite #178 owns an existing supported route or reviewed profile extension.
No source/native compatibility test runs after that refusal, and no Git remote,
shared metadata, verifier code or configuration is rewritten to fabricate a pass.
Keep this issue partial until its applicable source-context/hosted evidence is
actually supplied. Independent private consumer-wheel receiving remains its own
profile and does not clear this restriction. Broader #21/#28/#30/#47 stay open.
