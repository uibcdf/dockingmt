---
summary: Decide how to collect and publish validation strategies and benchmarks
issue: uibcdf/bindingmt#29
status: resolved
opened: 2026-10-02
closed: 2026-11-04
verification: inspected
area: [validation, benchmarks, documentation]
guard:
normative: devguide/validation/evidence_publication_policy.md
blocked_by: []
supersedes: []
---

# Decide validation and benchmark publication

## Resolution — 2026-11-04

[BMT-044](../DECISIONS.md#bmt-044--publish-evidence-through-a-staged-repository-first-route)
selects a staged repository-first route: the maintained scientific overview and
original records remain in Git, with a root README entry. There is no main
documentation site/build in the inspected checkout; rendered user documentation
is the next presentation destination when a concrete site or reader need exists.
A separate site remains conditional on a measured navigation/scale requirement.

The [evidence publication policy](../validation/evidence_publication_policy.md)
inventories readers/material, compares all three routes, and defines original
versus derived sources, minimum evidence, interpretation, responsibilities,
corrections, rerun triggers, retention and conditions for an immutable external
store. The [existing reproducible overview](../validation/scientific_evidence_overview_2026-11-04.md)
supplies the first reader presentation without copying archives or remeasuring
geometry. Directory instructions carry the accepted contributor action.

All decision acceptance criteria below are satisfied by those maintained sources
and navigation. This resolves the organization/publication decision; no website,
scheduled campaign, storage migration, release or scientific qualification is
claimed. Molecular provider issues, #30/#47 public delivery and visible C4/C6
remain separate. Original opening specification below is retained as history.

## What

Choose how BindingMT should collect, document, maintain and publish validation
strategies and benchmark evidence. The user requested a future decision between
a documentation section, a dedicated website, or another appropriate collection
and publication route. No platform has been selected.

## How

Inventory the existing cases in `devguide/validation/` and their intended readers.
Compare a **Validation and benchmarks** section in the main documentation, a
dedicated site, and a staged or hybrid route. Evaluate discoverability,
reproducibility, historical versions, build/hosting complexity and maintenance.

Define how strategies, reference cases, scripts/tests, notebooks, raw reports and
published summaries relate. Specify the minimum evidence and maintenance
lifecycle: dataset/input identity, method/backend, versions, preparation choices,
units/metrics/tolerances, hardware/resources, repeated measurements, limitations
and failure cases. Decide where large artifacts would live when Git becomes
unsuitable, and how notebooks and pages reuse the same maintained source data.

## Why

The work in [#28](https://github.com/uibcdf/bindingmt/issues/28) already retains an
[executed profiling notebook](../validation/workflow_profiling.ipynb),
[measurement definitions](../validation/workflow_profiling.md) and
[raw reports](../validation/data/workflow_profiling/). Other existing cases cover
181L redocking, external 1IEP inputs and preparation audits. These provide concrete
material for a publication decision, but preservation alone does not establish a
reader-facing collection or its maintenance lifecycle.

Scientific correctness/accuracy, software regression, integration qualification
and runtime/memory benchmarking need clear interpretation. Provisional chemistry,
passing CI and performance observations must retain their actual evidence level.
Related coverage work in [#22](https://github.com/uibcdf/bindingmt/issues/22)
concerns a distinct software metric.

## What was refuted

No publication alternative has been ruled out. A separate website is an option,
not an accepted requirement. This proposal does not replace existing scientific
gates or imply that the current exploratory cases are scientifically qualified.

## Scope and exclusions

This is a BindingMT decision, with no immediate website, publishing pipeline or
benchmark service implementation. Existing evidence and molecular ownership are
preserved. No sibling changes or coordination are required. A future shared suite
rule or reusable publishing tool would need its own MolSysSuite proposal.

## Acceptance criteria

- Inventory current material and its readers.
- Compare routes; choose one with rationale and a concrete reconsideration trigger.
- Define evidence organization, reproducibility, historical provenance,
  interpretation, rerun cadence and maintenance responsibilities.
- Preserve one maintained source of evidence and separate scientific validation,
  performance measurements and software checks.
- Record the decision in `DECISIONS.md` and track bounded implementation follow-ups.
  Building a complete website is not required to close the decision issue.
