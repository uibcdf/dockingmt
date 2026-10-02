---
summary: Reject unsupported constraints and guidance before Vina execution
issue: uibcdf/dockingmt#26
status: open
opened: 2026-10-02
closed:
severity: high
verification: reproduced
area: [protocols, capabilities, vina]
guard:
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
