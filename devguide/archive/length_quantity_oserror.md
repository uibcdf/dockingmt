---
summary: Shared length admission masks an original OS/resource error as invalid input.
issue: uibcdf/bindingmt#115
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: reproduced
area: [units, resources, public-api]
guard: tests/test_site_geometry.py::test_length_resource_exception_preserves_original_identity
normative:
blocked_by: []
supersedes: []
---

# OS/resource exceptions in shared length admission

An authored probe on e1e6a337dbf487d1b2e36809cc72ea46a7639f60 patches
`pyunitwizard.ensure_quantity` to raise an explicit OSError(12), then constructs
a valid BoxRegion. `_ensure_length_quantity` wraps it as ArgumentError with the
same OSError as cause. It should propagate the original resource exception,
as already done for MemoryError, without classifying an infrastructure failure
as malformed scientific input. The new #111 geometry factories reuse this
boundary; no competing quantity parser should be introduced.

Evidence: `.molsyssuite/site-geometry-111-20261113/resource-probe-01/`, including
the original type/cause receipt and bounded terminal outcome. This is controlled
error-path injection, not actual memory pressure or a PyUnitWizard defect.
Fix the narrow catch, preserve original exception identity and qualify existing
BoxRegion plus new site geometry under normal and pm/fs policies. Input/value/
dimension errors retain their existing owning diagnostics. #30's earlier
evaluator interruption, original fixtures and shared prefix remain untouched.
Custody owner #50 reviews raw receipts on 2026-11-14.

## Resolution and additional receiving

Both `_ensure_length_quantity` and the saved-box `_box_vector_from_record`
now re-raise `(MemoryError, OSError)` before their invalid-input branch.
An additional authored saved-reader probe reproduced the same wrapping with
`pyunitwizard.quantity`; its original source bytes/context and receipt are kept
under `resource-reader-probe-01`. Neither injection is real resource pressure.

The primary guard checks original exception identity for BoxRegion and the new
sphere/box factories with MemoryError, OSError and PermissionError. The additional
`tests/test_box_record_admission.py::test_box_reader_preserves_quantity_construction_os_failure`
checks the actual saved-box reader with OSError and its PermissionError subclass;
the preceding memory guard remains unchanged. Invalid dimensions/values retain
their owning input diagnoses. No scientific quantity, threshold or producer is
rewritten by this correction.

The complete affected selection passes **473 cases per normal/pm-fs policy**,
including 72 new geometry cases and two new saved-reader OS-error cases. This
extends the final core population to 436, plus 37 argument/bootstrap controls;
earlier successful 434-core/71-focused attempts precede the final selection.
See [the geometry profile](../binding_site_geometry.md) for exact source closure,
public/cold/old-reader evidence, bounds and unchanged resource holds. All new
attempts terminate within their limits without a resource interruption.
Exact final source, selected reports, workspace/fresh committed-export gates and
public issue synchronization retain #50 custody under the task path above.
Closure follows publication of the committed fix; missing hosted/installed/public
platform evidence stays separate under #30.
