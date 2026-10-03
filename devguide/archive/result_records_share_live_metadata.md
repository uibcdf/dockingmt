---
summary: Isolate serialized docking results from live metadata and provenance
issue: uibcdf/dockingmt#25
status: resolved
opened: 2026-10-02
closed: 2026-10-03
severity: medium
verification: measured
area: [results, serialization, provenance]
guard: tests/test_result_contracts.py::test_result_export_is_independent_snapshot
normative:
blocked_by: []
supersedes: []
---

# Result records share live metadata

## What

Exported pose and result dictionaries retained references to live metadata,
problem information, protocol information, and provenance. Editing a nested
exported field could therefore modify the original result. Reconstructed objects
likewise shared nested fields with the supplied dictionary.

## How

Changing `record['provenance']['backend']['version']` after `result.to_dict()`
changed the original result's backend provenance. Editing nested pose metadata
after `DockingPose.from_dict(record)` changed the reconstructed pose.

The fix copies structured data at both serialization boundaries. Pose and result
exports are independent snapshots; reconstruction is independent of its input
record. Coordinates retain their existing quantity-to-list representation and
the schema stays at version `1.0`.

## Measured evidence (2026-10-02)

Before both result-model fixes, 29 of 36 new contract cases failed. After the
fixes, all 43 focused cases in `tests/test_result_contracts.py` and
`tests/test_results.py` passed in 4.90 seconds. Snapshot guards cover nested
metadata, scores, coordinate lists, problem/protocol information, and provenance,
including mutation in both directions and a strict JSON round trip.

Full `pytest --receptor=llm` passed all 233 tests in 42.48 seconds on Python
3.13.14, compared with the preceding 197-test baseline. The same twelve provider
warnings remain. Ruff checks, format checks (70 Python files), generated report
indexes, and whitespace checks pass. These checks use editable sibling sources;
they do not establish published-dependency compatibility or a hosted CI result.

## Why

Result records support inspection and replay. An exported record must retain the
recorded provenance when either the live result or the record is edited later.
Loading a record must not create an implicit shared mutable provenance object.

## What was refuted

A shallow dictionary copy leaves nested references shared. A JSON encode/decode
copy would unnecessarily restrict structured Python metadata. No new storage
framework or schema migration is required to establish boundary independence.

## Scope and exclusions

Only dictionary export and reconstruction ownership are changed. Constructor
ownership of arbitrary caller metadata remains outside this issue. This does not
manipulate molecular systems, change molecular reconstruction, introduce storage
formats, or require MolSysMT or MolSysViewer changes or coordination.

The guarded implementation is committed with this record. The issue remains
partial pending hosted qualification; local validation and publication do not
establish compatibility with CI's pinned dependency set.

## Acceptance criteria

- Export independent pose and result records, including nested mutable fields.
- Reconstruct objects independently of the supplied records in both directions.
- Preserve schema version `1.0` and existing JSON round-trip behavior.
- Keep result-only operations independent of molecular and viewer operations.
- Record hosted qualification before closing the issue.

## Hosted resolution (2026-10-03)

[CI run 37107875583](https://github.com/uibcdf/dockingmt/actions/runs/37107875583)
qualified commit `ff64d84239dbadd030ac1ba5f82eb0a60b5517b4`. All four Linux
lanes (Python 3.11, 3.12, 3.13 and 3.14) passed the ordinary installed-package
import and metadata gate and all 414 tests, without skips. The test named in
`guard` remains the durable regression check. This closes the hosted software
qualification requirement; it does not establish public dependency admission or
scientific preparation validity. Historical local-only statements above describe
the evidence available when originally recorded.
