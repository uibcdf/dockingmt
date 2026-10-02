---
summary: Reject invalid named scores before ranking docking poses
issue: uibcdf/dockingmt#24
status: partial
opened: 2026-10-02
closed:
severity: medium
verification: measured
area: [results, ranking, arguments]
guard: tests/test_result_contracts.py::test_ranking_rechecks_scores_after_rescoring_edits
normative:
blocked_by: []
supersedes: []
---

# Invalid scores can corrupt pose ranking

## What

A pose with a `NaN` score could appear first after `rank_by('vina')`. Non-numeric
scores could also be sorted lexicographically, and truthy non-boolean values of
`ascending` silently chose a ranking direction. This made the reported top pose
depend on invalid data or an unintended policy.

## How

The reproduction ranked an input sequence with scores `NaN` and `-8`; the
invalid pose remained first. The fix validates nonempty string score names and
finite real values when constructing a pose, normalizing supported numeric
scalars to Python floats. Ranking revalidates the selected score because the
public score mapping can be edited during rescoring. Export also validates
scores so later edits cannot silently produce an invalid score record.

`rank_by` uses ArgDigest for its score name, boolean direction, and closed
argument admission. Invalid score diagnostics expose the score name and pose
index when ranking. Both directions preserve ties, state identities, and the
original pose order and ranks; the returned result records its ranking policy.

## Measured evidence (2026-10-02)

Before both result-model fixes, 29 of 36 new contract cases failed. After the
fixes, all 43 focused cases in `tests/test_result_contracts.py` and
`tests/test_results.py` passed in 4.90 seconds. NumPy scalar scores survive a
strict JSON round trip. Guards forbid molecular operations and viewer imports
during ranking, export, and reconstruction.

Full `pytest --receptor=llm` passed all 233 tests in 42.48 seconds on Python
3.13.14, compared with the preceding 197-test baseline. The same twelve provider
warnings remain. Ruff checks, format checks (70 Python files), generated report
indexes, and whitespace checks pass. These checks use editable sibling sources;
they do not establish published-dependency compatibility or a hosted CI result.

## Why

Ranking is an explicit scientific decision. Invalid scores must not acquire a
rank, and a supplied direction must represent an unambiguous boolean policy.
Serializable numeric scores also allow downstream inspection without a custom
JSON encoder for NumPy scalars.

## What was refuted

Filtering invalid poses silently would change result membership. Treating strings
as numbers would hide input errors. Inferring score units or selecting a score
automatically would introduce scientific policy outside this bounded correction.

## Scope and exclusions

Only named score validation, ranking arguments, and their diagnostics are changed.
Molecular coordinates and provider responsibilities are unchanged. This does not
add scoring functions, score units, clustering, or molecular operations, and
requires no MolSysMT or MolSysViewer changes or coordination.

The guarded implementation is committed with this record. The issue remains
partial pending hosted qualification; local validation and publication do not
establish compatibility with CI's pinned dependency set.

## Acceptance criteria

- Reject nonfinite, boolean, and non-numeric named scores with local diagnostics.
- Reject empty score names, ambiguous ranking directions, and unknown keywords.
- Revalidate edited scores without changing the source result on failure.
- Preserve stable ties, pose identity, and explicit ranking provenance.
- Record hosted qualification before closing the issue.
