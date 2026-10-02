---
summary: Reject unsupported constraints and guidance before Vina execution
issue: uibcdf/dockingmt#26
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: high
verification: measured
area: [protocols, capabilities, vina]
guard: tests/test_backend_contracts.py::test_vina_rejects_unsupported_intent_before_hooks_or_execution
normative: devguide/DESIGN_PRINCIPLES.md
blocked_by: []
supersedes: []
---

# Vina ignores constraints and search guidance

## What

`DockingProblem` accepts scientific constraints and search guidance, but the
current Vina path neither implements nor rejects nonempty values. Requested
intent is retained in result problem information without an execution disposition.

## How

At `181000a4fd63b40d750fd739414fb651f5631fbc`, construct a problem from
`MINIMAL_REC_PDBQT` and `MINIMAL_LIG_PDBQT` in `tests/test_engines.py` with a
10 Å box centered at the origin. Supply:

```python
constraints = {'required_contact': 'UNSUPPORTED_SENTINEL'}
search_guidance = {'pharmacophore': 'UNSUPPORTED_SENTINEL'}
protocol = VinaProtocol(exhaustiveness=1, n_poses=1, seed=123, cpu=1)
```

`protocol.validate_problem(problem)` succeeds. Installed Vina 1.2.7 returns
one pose, with coordinates and scores identical to an otherwise identical
unconstrained control. The requested contact remains in
`result.problem_info['constraints']`; no constraint-handling field is present in
run provenance. Source inspection confirms that the adapter never consumes
either scientific intent field. The probe forbids MolSysMT `get`, `select`,
`extract`, `convert`, `copy`, and `set`; the raw PDBQT route needs none of them.

## Guarded correction (2026-10-02)

The Vina protocol and backend share a private admission check. Nonempty list or
dictionary requests fail through `CapabilityMismatchError` (`DMT-E003`), exposing
the unsupported fields, offending argument, protocol, and engine. Invalid
containers fail through `ArgumentError` (`DMT-E002`). The backend checks before
the protocol validation hook, so overriding that hook cannot silently enable
unsupported intent. Empty lists/dictionaries and default unconstrained requests
remain valid. Other backends are not given a universal empty-intent restriction.

The ten dispatch guards cover each field separately, lists and dictionaries,
both fields together, and direct/top-level execution. They forbid protocol
validation hooks, box projection, preparation, staging, input resolution, native
Vina import, and molecular operations. Additional cases cover direct protocol
validation, malformed containers, empty intent with Vina/Vinardo, and an
overridden protocol hook. No constraint or guidance implementation was added.

## Measured validation (2026-10-02)

Before the fixes for #26 and #27, the selected contract modules had 86 failures
and 30 passing cases. After the initial correction, 131 focused cases passed in
12.66 seconds, including existing Vina/Vinardo native execution. Two additional
nested-schema guards were then added for #27.

Full `pytest --receptor=llm`: 344 passed in 48.96 seconds on Python 3.13.14,
versus the preceding 237-test baseline. The same twelve provider warnings remain.
Ruff, format checks (74 Python files), generated indexes, and whitespace checks
pass. These are local checks using editable support sources; they do not establish
hosted or published-dependency compatibility. Existing preparation remains
provisional under #5. Resolution here covers the guarded admission defect only.

## Why

Constraint enforcement, post-filtering, and search guidance have different
scientific meanings. Silently executing the unconstrained problem can produce
a plausible result for the wrong question. This directly undermines future
PharmacophoreMT and guided-search integration.

## What was refuted

Keeping the request in a manifest does not mean it was implemented. Equal output
alone is not proof of ignored guidance; the missing source consumption and the
absence of an execution disposition establish the current unsupported route.

## Scope and exclusions

Reject unsupported nonempty intent before domain projection, preparation, staging,
and engine execution. This does not implement constraints, pharmacophore parsing,
guidance algorithms, or a generic protocol framework. No MolSysMT or MolSysViewer
change or coordination is needed. The broader architecture review is
[DockingMT #28](https://github.com/uibcdf/dockingmt/issues/28).

## Acceptance criteria

- Direct and top-level Vina execution reject unsupported nonempty intent clearly.
- Structured diagnostics identify the unsupported scientific field.
- Rejection occurs before preparation, projection, staging, and native execution.
- Existing unconstrained Vina/Vinardo execution remains valid.
- A future supported route must declare enforcement or guidance handling explicitly.
- Add a durable rejection guard and record validation before closing.
