---
summary: E3 reference readback omits explicit mechanical parameters and assignment evidence.
issue: uibcdf/dockingmt#96
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: inspected
area: [scientific-validation, evidence, persistence]
guard:
normative: devguide/validation/e3_h5msm06_reference_receiving_2026-11-09.md
blocked_by: []
supersedes: []
---

# E3 reference mechanical evidence

## What

The original reference worker compares schema-3 chemical-template snapshots.
That helper observes topology, structures, chemical states and associations,
not MolecularMechanics, its typed atom table or charge/type assignment reports.
Its historical default-0.5 attempt correctly fails; no earlier complete E3
reference pass is accepted or retroactively changed.

## How

Retain the original helper and assertions. Add task-specific observations of
public mechanical parameters/table/report values, dtype/shape/index/columns,
original units through PyUnitWizard records, and producer metadata. Compare
both readbacks and all final source states. Require actual nonempty prepared25
reports and detect four isolated corruptions on public mechanical copies.
Observe each new file's 0.6 root version without implementing a molecular codec.

## Why

Successful old-domain equality would not prove preservation of the exact domain
whose absence blocked E3. The new gate must detect real loss, not merely produce
the expected observation shape.

## What was refuted

This is consumer qualification coverage, not a demonstrated provider defect.
No helper/runtime/schema/source-fixture modification or new molecular algorithm
is needed. Historical inputs and producers stay exact.

## Scope and acceptance

Follow the preregistered [reference selection](../validation/e3_h5msm06_reference_receiving_2026-11-09.md).
Keep all original science/custody checks and four writes/two reads; add only
four mechanical copies/four header observations. Preserve the zero-operation
setup failure. Complete normal/pm-fs, independent receiving and final local/
fresh committed-source checks are required. Full E3, installed/public/scientific
scope and #256's final provider freeze remain separate.

## Bounded resolution — 2026-11-09

The complete suffix-03 [public-0.6 receiving](../validation/e3_h5msm06_reference_receiving_2026-11-09.md)
passes normal/pm-fs and independent 261-member/nine-member reading. Every original
scientific assertion remains; the final observer preserves literal strings and
detects five actual altered-copy losses, including unchanged-dtype F/farad.
All historical failures and weaker initial seals remain immutable. This resolves
the local criterion/observer concern for these exact inputs and editable sources;
full E3 and installed/public/hosted acceptance remain separate. Relevant local
and fresh committed-source documentation/resource checks accompany publication.
