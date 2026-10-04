# Public redocking collection summary

`dockingmt.summarize_redocking(evaluations, *, failures=None)` summarizes a
small caller-selected collection of saved `evaluate_redocking` schema 1.0
reports. It uses saved observations, with no molecular operation, engine run,
ranking change or viewer access.

```python
summary = dockingmt.summarize_redocking(
    {'case-a': report_a, 'case-b': report_b},
    failures={
        'case-c': {
            'stage': 'docking',
            'error': failed_outcome.error,
            'context': {'source_index': failed_outcome.index},
        }
    },
)
```

Case IDs are explicit nonempty strings, unique within each input mapping and
disjoint between evaluated and failed cases. Preserve IDs when building mappings;
Python cannot recover entries overwritten before this call. Cases retain mapping
order, evaluated cases first and failures second. This does not reconstruct an
interleaved execution order. `DockingOutcome.index` is a position, not a molecular
or case identity. The caller associates it with a case and evaluates successful
outcomes separately.

## Compatible recorded policies

Every evaluated case must use the same exact finite JSON declarations for:

- positional RMSD criterion, angstrom unit, cutoff, <= comparison, no alignment
  or symmetry correction, retained-atom scope, correspondence and receptor frame;
- ordered top-N requests and current-result-order interpretation;
- evaluator identity and versions;
- backend/version, complete protocol and complete preparation records.

The gate compares canonical JSON, preserving value types and literal unit
declarations. It does not normalize unknown schemes or convert another report
unit into angstrom. Even an internally agreeing nanometer report is rejected:
schema 1.0 declares cutoff and pose RMSD in angstrom. A non-default application
unit policy cannot alter those saved measurements.

Reference coordinates, selected inputs, search domains, atom counts, molecular
state IDs and full case ranking histories remain case-specific. No scores or
global poses are ranked or pooled. The named metric is current-result-order
recovery; it does not certify identical physical score contexts or biological
comparability. Equality of unknown backend/preparation declarations still means
unknown. Caller reference information and recorded state IDs are declarations,
not authenticated molecular evidence.

The complete preparation/protocol equality rule is deliberately conservative.
It includes seeds, flags, units, preparation modes, state IDs and any stored
metadata. Distinct automatically prepared systems may therefore require separate
calls even if a caller regards their preparation as similar. Do not remove their
evidence to force pooling. This initial profile fits homogeneous prepared-input
controls; relaxing it requires a named comparison policy and concrete evidence.

Inconsistent/unsupported input raises `ArgumentError`; it is never silently
skipped or converted to an execution failure. Admission checks schema, finite
JSON, reference unit/shape/snapshot digest, pose positions/counts/identities,
finite nonnegative RMSD, literal recovery, first/closest summaries including tie
order, and top-N requests/considered counts/recovery. This is bounded record
consistency: the operation cannot recompute geometry from pose hashes, authenticate
source chemistry or establish that a declared receptor frame is physically shared.
Retain the original saved results, reports and input artifacts for deeper audits.

## Counts and denominators

Each successful evaluation counts once, regardless of its returned pose count.
An empty docking result is an evaluated nonrecovery. A declared failure has
unknown recovery; it is separate from evaluated nonrecovery.

| Field | Meaning |
| --- | --- |
| `n_submitted` | Caller-supplied evaluated cases plus declared failures |
| `n_evaluated` / `n_failed` | Separate completed evaluations and failures |
| `n_empty_results` | Evaluated cases with no pose |
| `evaluation_coverage` | Evaluated / submitted; null for an empty collection |
| top-N `n_recovered` | Evaluated cases with a recovered pose in the first N positions |
| top-N `n_not_recovered` | Evaluated cases without one, including empty results |
| top-N `n_unknown` | Declared failures |
| top-N `fraction_of_evaluated` | Recovered / evaluated |
| top-N `fraction_of_submitted` | Observed recovered / submitted |

The latter fraction includes failures in its denominator but does not label them
nonrecovered: their recovery remains unknown. For every top-N entry, recovered +
not recovered + unknown equals submitted. `considered` counts and actual pose
counts stay in the case records; requesting N greater than available poses does
not invent missing poses.

Empty/all-failure collections have `policy=None` and no top-N entries: there is
no observed evaluation policy to infer. An empty collection has null coverage;
an all-failure collection has zero coverage. These are observations in the
selected submissions, not certified dataset success rates, independent samples,
confidence intervals, predictive accuracy or a chemical preparation qualification.

## Detached evidence and reproducibility

Summary schema 1.0, type `redocking_collection`, retains the exact common policy,
counts and compact case records. Evaluated cases retain first/closest pose IDs,
declared ranks/states, atom counts and RMSD, their top-N observations, compact
case input/ranking context, reference declarations/snapshot hash,
and a SHA-256 of the complete original evaluation. No full pose population or
reference coordinate arrays are duplicated. Common backend, protocol and
preparation declarations are retained once in `policy`, rather than in every
case's context. Failed cases preserve stage, typed
error and optional context. The typed summary uses the existing public
`DockingOutcome` admission; no exception object/traceback is stored.

Original evaluation digests use UTF-8 JSON with sorted keys, separators `(',',
':')` and `allow_nan=False`. They cover the recorded report, not authenticated
science. Inputs, output sections and later summaries have detached JSON ownership.
Keep original reports separately; the compact summary cannot reconstruct them.

The [executed notebook](redocking_summary.ipynb), [raw receipt](data/redocking_summary/summary.json)
and [`qualify()` helper](../../devtools/qualify_redocking_summary.py) read the
unchanged native reports from [#38](https://github.com/uibcdf/dockingmt/issues/38).
Their source hash, source size, implementation/helper hashes, checkout HEAD,
Python and current summarizer version are recorded. Historical evaluator/provider
versions and native observations remain in the input reports and common policies.
This is an offline consumer qualification, not fresh Vina execution.

181L provisional preparation stays in a separate cohort. The external 1IEP and
displaced-domain controls retain unassessed preparation: one case meets the
declared 2.5 Å criterion and one does not. Their fractions are 1/2 for evaluated
and submitted cases. Adding a clearly labelled **declared failure fixture** keeps
evaluated recovery at 1/2, gives submitted recovery 1/3 and coverage 2/3. That
fixture is not a newly observed runtime failure. All-failure and empty collection
controls infer no recovery policy. The collection is a positive/negative software
control pair, not a biological benchmark or a representative dataset.

[DockingMT #39](https://github.com/uibcdf/dockingmt/issues/39) owns this block.
Publication organization remains separate in #29; future molecular symmetry
remains provider-owned in MolSysMT #310. No sibling source or dependency pins
change for aggregation.

## Local qualification — 2026-10-04

All **837 tests pass without skips in 210.09 s**, including 87 new summary
controls; the same 96 existing/provider warnings remain visible. Ruff
lint/format (109 Python files), generated report indexes, reporting guard and
diff checks pass. `pip check` exits 0. Local source qualification uses editable
`molsyssuite@uibcdf_3.14` (Python 3.14.7) and unchanged MolSysMT
`c19a47ada0c2279029abfa296cf915560610ad9a` / MolSysViewer
`ec4c71e574d798b7c8675b7e7e983da878ce9889` pins. All three notebook code cells
execute with the requested interpreter. This does not qualify published
dependencies, another platform or a scientifically prepared screening dataset.
