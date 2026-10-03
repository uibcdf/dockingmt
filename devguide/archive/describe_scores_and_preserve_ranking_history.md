---
summary: Describe score semantics and preserve ranking history
issue: uibcdf/dockingmt#31
status: resolved
opened: 2026-10-03
closed: 2026-10-03
verification: measured
area: [results, scoring, serialization]
guard: tests/test_score_semantics.py
normative:
blocked_by: []
supersedes: []
---

# Score semantics and ranking history

## What

Attach method/version, interpretation, conventional unit, preferred direction and
comparison context to the scores of the current Vina/Vinardo route. Preserve the
evidence for successive explicit rankings of saved results. Follow-up to #28.

## How

Use the existing pose metadata and result provenance extension points. Validate
descriptors at construction, export and ranking. Retain original numeric values,
schema 1.0 and fully undescribed legacy results. Record only scalar observations
and order indices in history, with independently owned structured metadata.

## Why

Finite numbers and names alone do not establish scientific comparability. The
previous implementation replaced the latest ranking policy without preserving its
predecessor. Stable pose/state identity and detached evidence permit independent
inspection without a live molecular system or engine.

## What was refuted

An empirical docking score in conventional energy-like units is not a measured
physical energy. Matching descriptors are a necessary admission condition, not
scientific calibration or proof that different protocols can be compared.
No automatic direction change or invented descriptor for legacy values is justified.

## Scope and exclusions

This block describes existing scores and ranking only. No rescoring engine,
physical-energy score API, campaign, cache, molecular operation or sibling change
is included. #29 still owns the future publication platform decision.

## Acceptance criteria

- Validate explicit descriptors and reject mixed/incompatible described rankings.
- Keep legacy records readable and explicitly rankable.
- Preserve successive rankings, stable ties, score values, state/pose identity and inputs.
- Retain executed offline example and ordinary gate evidence.

## Resolution

`DockingPose.score_definitions` validates and detaches descriptors supplied through
the new constructor argument or existing metadata extension point. Vina/Vinardo
attach conventional empirical semantics and actual input/settings evidence to
their unchanged score numbers. Ranking checks declared comparison contexts and
state identities, preserves explicit direction/tie order, and appends independent
scalar evidence. Native order and legacy policy-only evidence remain distinct.
The outer schema and latest-policy access remain compatible.

The guard `tests/test_score_semantics.py` protects this boundary through actual
constructor/export/ranking/reader operations, incompatible collections and nested
mutation probes. The extended native execution test in `tests/test_engines.py`
checks both Vina and Vinardo against submitted input hashes and actual provider
versions. It retains the previous profiling output-equality assertions.

The [contract](../validation/score_semantics.md),
[executed notebook](../validation/ranking_history.ipynb) and
[saved synthetic fixture](../validation/data/ranking/synthetic_result.json)
provide reproducible offline evidence. All five notebook cells execute, its schema
validates and no cell reports an error. The fixture is explicitly invented software
data; it does not replace the Core scientific preparation/redocking gates.

Coordinate buffers retain the existing sharing contract. Ranked structured metadata,
result context and history are independently copied; the history stores no coordinates.
This introduces bounded work proportional to retained metadata and ranking observations,
not a runtime speedup claim or a cache. A legacy export smoke retains exactly the
previous small-mapped benchmark's payload hash.

Final local gates: `pytest --receptor=llm` passes 413 tests in 52.77 seconds, with
the same twelve provider warnings (eleven legacy H5MSM warnings and one occupancy
attribute-drop warning). Ruff lint and format checks, current report indexes and
`git diff --check` pass. The five-cell notebook validates and executes successfully.
