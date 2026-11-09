---
summary: The installed resource inventory omits the already-shipped interaction module.
issue: uibcdf/dockingmt#93
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [distribution, resources]
guard: devtools/tests/test_distribution_contract.py::TestDistributionContract::test_complete_core_addon_and_generated_version_inventory
normative:
blocked_by: []
supersedes: []
---

# Shipped interaction module missing from the resource inventory

## What

The real private wheel from producer `6310a97b7a900f31d37f84a476bc355a899282de`
contains 66 runtime files, while its resource descriptor lists 65. The sole extra
is the tracked public `dockingmt/interactions.py`; no module is missing from the
wheel. The private installed-record gate fails before installation. Wheel version
`0.0.0+339.g6310a97`, SHA-256
`13169bd91cc90a16bd3b8f60329856ee2cb1921a0dd69ebb598230f543e6fa92`.

## How

Reuse the existing complete-coverage distribution guard before/after adding the
missing path. Run the whole original distribution-control module. Preserve the
original wheel and failed qualification, then inspect the same bytes using the
corrected separately identified descriptor; retain original runtime/test producer
identity and all initial failures. Do not rebuild or relabel the artifact.

## Why

The declared complete payload and installed checks must cover the public binding
API already delivered by the wheel. A required-path preflight checks listed paths;
this component's existing exact-coverage guard separately protects omissions.

## What was refuted

No setuptools packaging failure, missing runtime module, shared-tool defect,
new test or new scientific operation is established. The existing guard suffices.
Metadata Python constraint ordering is semantically normalized during inspection;
this changes no supported interpreter range.

## Scope and exclusions

Add one required path; preserve all runtime code/tests, 594 helper/data inputs,
workflow/source pins, public version/installation claims and provider holds.
The original private wheel may receive this corrected qualification descriptor
without becoming a Conda/public artifact or a wheel from the later commit.

## Acceptance criteria

Original guard fails with this exact missing path; the corrected descriptor and
complete distribution controls pass. Current private installed receiving uses
unchanged wheel/source/test bytes, shared SDK and explicit original producer/
qualification separation. Update checkpoints, indexes and GitHub; qualify final
resource/publication checks and a fresh committed export. Owners #47/#30/#73;
private custody #50/review 2026-11-14. No remote CI, shared installation or provider
refresh/build; keep the #256/#558 and actual-canvas holds.


## Resolution and receiving — 2026-11-08

One required path is added; all runtime/tests, other descriptor fields and 594
helper/data declarations remain unchanged. The existing named guard has its
original one-failure receipt; complete distribution controls pass 19 tests/five
subtests. No new test, source packaging workaround or shared-tool change is needed.

[Complete private installed-record receiving](../validation/record_wheel_editable_2026-11-08.md)
then passes both original 990-case profiles normal/pm-fs, four import refusals,
66-file/RECORD/source/metadata/license/provenance and ordinary pip checks. The same
original wheel is preserved, with its producer distinct from this qualification.
A zero-test usage failure and initial 65-path assertion failure remain. Independent
193-member primary/nine-member reader receiving verifies native reporting and
all outcomes without replay. The later committed checkpoint records final local
and fresh-export gates in #47/#93; no source/test assertion is changed.

This resolves the declaration defect, not #47/#30's public/Conda/full-installed/
platform qualification or #73's complete goal. Private custody and original
#256/#558/canvas holds remain as the linked receiving record describes.
