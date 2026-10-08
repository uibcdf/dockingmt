---
summary: Preserve caller tracing in the developer result-export benchmark.
issue: uibcdf/dockingmt#48
status: resolved
opened: 2026-10-08
closed: 2026-10-08
severity: low
verification: reproduced
area: [tooling, governance]
guard: devtools/tests/test_result_export_resources.py
normative:
blocked_by: []
supersedes: []
---

# Result-export tracing ownership

## What

At source `8da5bbcede2101c3f4b0e058cd5b0711a8522cc9`, the optional memory
sample in `devtools/benchmark_result_export.py` unconditionally stops tracemalloc.
If the caller already started tracing, successful sampling and an export error
both stop a resource the helper does not own. Its existing finally correctly
releases tracing started by the helper; that behavior is retained.

## How

Python 3.14.7 `-S` children import the actual stdlib-only tool and supply an
inert result implementing snapshot/length/iteration. No molecular package,
engine or synthetic scientific record is imported or computed. Two caller-owned
success/failure guards fail before repair; three owned-tracing/no-memory controls
already pass. All five pass after ownership-aware start/stop handling.

## Why

Surrounding diagnostics may retain an active tracer. The developer helper must
not terminate that caller resource. This is resource custody under
uibcdf/molsyssuite#104, independent of docking correctness or benchmark budgets.

## What was refuted

There is no leak of tracing started by the helper: its finally already handles
success and failure. No framework, new tracing API or permanent scratch is needed.
Peak measurement, timing formulas, payload fields and comparison contracts remain
unchanged; only tracing ownership changes.

## Scope and exclusions

Local developer benchmark and resource regression module only. No runtime API,
dependency, SDK/policy pin, guide, engine operation or public artifact change.
The actual scientific profiler, qualification scripts and full suites are not
executed by these guards.

## Acceptance criteria and verification

Five real-tool guards verify caller tracing survives return/error, owned tracing
ends on return/error, and the no-memory path preserves the caller. The two
observed failures become passing regressions; the three passing controls remain
green. The registered guard therefore protects the actual mechanism and is
statically addressable. Each child and managed fixture is disposed.

Selected administrative checks run with scientific conftest disabled. Exact
manual policy/publication gates verify source controls after the authorized
conditional internal skip; they do not execute these regressions remotely or
clear full-suite debt. The five guards are executed locally on the committed
code. Diego/Liliana and existing nightly/manual recovery retain full-suite
evidence under uibcdf/dockingmt#30 and uibcdf/molsyssuite#104.
