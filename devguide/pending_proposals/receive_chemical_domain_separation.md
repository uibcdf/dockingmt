---
summary: Receive independent ChemicalStates storage and graph tools from MolSysMT.
issue: uibcdf/bindingmt#56
status: partial
opened: 2026-10-28
closed:
verification: measured
area: [integration, preparation, validation]
guard: tests/test_chemical_domain_receiving.py
normative: devguide/chemical_domain_receiving.md
blocked_by: []
supersedes: []
---

# Receiving the chemical-domain cutover

What — Torsion preparation and symmetry consume the four moved graph tools from
`msm.chemical_states`; state fixtures use the independent chemical owner.

How — The [receiving contract](../chemical_domain_receiving.md) identifies source
pins, current audit tools, historical producers and qualification boundaries.
Current controlled CI inputs select MolSysMT de7ffad2a and compatible Viewer
ca7ebea60. The original draft receipts below retain provider 9fb77c358.
The test bootstrap requires DepDigest >=0.15.1, the provider's actual floor.
Workflow byte changes are limited to those two source pins; reviewed input
hashes are updated only after checking that exact delta.

Why — Unmodified 51b2232 against the new provider produces 27 failures / 7 passes
in the original 34-case probe. Four production graph calls and test fixture/audit
accesses still use the removed facade. There is no demonstrated new docking
criterion or numerical disagreement in that diagnostic scope.

## Executed evidence and limits

The initial scratch runtime/test/snapshot proposal passes 24 flexibility/symmetry
cases (exit 0). The completed state-fixture migration passes 116 focused cases
(exit 0, 47.41 seconds). A new state-scope guard first reproduces the obsolete
capability-failure assertion, then compares assigned and reference graphs through
the current provider. Full-suite evidence is recorded below when completed.
Python 3.14.7/Pandas 2.3.3, shared source environment and existing native backend;
this is not an installed-package or four-minor source certificate. Warnings are
retained, including nullable/legacy/projection diagnostics. Historical producer
records are preserved; they are not reclassified as current cutover evidence.

## Owner acceptance before completion

- Review/adopt the PR and run its exact controlled source CI; preserve all guards.
- Complete any broader current consumer receiving discovered by the full suite.
- Requalify historical producer workflows separately with new output identities.
- Qualify the actual installed/public provider pair and justify its real public
  minimum before consumer publication; do not invent an unavailable version.
- Record the adopted consumer/provider commits and settle #56 with its evidence.

Diego requested owner-reviewed PRs after the scratch handoff. No main merge,
package build, publication or modification of the original checkout is included.


## Expanded source probe and corrections — 2026-10-30

The full development selection (run 156) returned **1,339 passed / 25 failed /
4 errors**, exit 1, 443.37 seconds. It is retained as failed evidence. Three
qualification modules expose helpers used by active 3PTB/5X72 tests; their graph
calls also need the new namespace. Two runtime readers expanded the now-scalar
connectivity property into characters, incorrectly selecting a legacy pose path.
Preparation now wraps the scalar once in its established evidence list; Vina
staging compares the scalar directly after the single-state guard.

The corrective selection (run 160) passes **73/73**, exit 0, 102.72 seconds.
All 29 failed/error node identities from run 156 are explicitly present and
passed. Existing refusal, map, later-pose and numerical guards are unchanged.
This is corrective coverage, not a fresh all-suite or exact installed certificate;
the final PR CI must execute the complete suite before owner integration.

Reused current helpers are migrated without changing historical proof constants,
source-fingerprint paths or dated JSON. The separate state-scope receiving guard
protects the supported state comparison. No old producer result is relabeled.
The PR remains a draft for owner review, complete exact-source CI and delivery
acceptance; #56 stays open.

## Owner review of the requested checkpoint — 2026-11-02

The latest #56 handoff requests actual receiving of MolSysMT
`de7ffad2aef18ff3bccd184133dc69e081cb506e`. The four production graph callers,
scalar connectivity consumers, active helper routes and fixtures were reviewed.
Remaining old topology graph access is confined to the explicitly historical
`qualify_torsion_policy` producer; current guards use its separately named state
scope probe. Historical constants and all frozen evidence retain their identity.

The existing 103-case selection and the additional 13-case consumer guard pass
on Python 3.14.7/Pandas 2.3.3 with a newly built provider wheel. The shared base
has unrelated dependency conflicts; these passes do not establish clean installed
closure. The offline clean-environment attempt cannot resolve DepDigest >=0.15.1
from its cache; a separately recorded online attempt follows the declared channels.
Source/full/installed/hosted outcomes and provider matrix remain separate evidence.
The issue remains partial until its owner acceptance conditions are settled.

## Adopted source and retained qualification boundaries — 2026-11-02

PR #59 source `79740b4ce373c8d98da6f1c9f5633456381f73fa` is reviewed and adopted.
The [receiving contract](../chemical_domain_receiving.md#source-adoption-and-executed-owner-qualification--2026-11-02)
records 1,381 passing source tests, both exact-source four-minor CI runs and the
private ordinary-built consumer/provider artifacts. Full initial installed
receiving has 1,376 passes / five harness-context failures. The corrected 131-case
selection includes all five failed identities and passes without skips; the first
run is not relabelled as clean. Test/helper bytes, scientific inputs, artifact and
dependencies are preserved. Separate administrative checks pass 29 cases after
replacing an incomplete historical SDK copy with the same clean immutable SDK.
All 389 frozen evidence files retain their bytes.

This source-adoption slice is complete. Keep this broader issue partial for the
provider's final qualification and real installed/public/platform/minimum scope;
no public coordinate is invented from development version `0.23.0+361.gde7ffad2a`.
Final main-head CI is recorded on #56. Temporary resources belong to #56/#50,
review 2026-11-09, with no automatic deletion. Scientific profile acceptance and
historical requalification remain separately scoped.

## Main-source location and complete installed receiving — 2026-11-03

Provider #255 is resolved and its main integration is `00abb958fb93649131d5ce5fe5e12e90cf4900e9`.
Git-object comparison confirms unchanged package, Rust, test and build inputs
relative to `de7ffad2a`. The source dependency/CI route selects that exact main
checkpoint; neither an unavailable package minimum nor a different scientific
implementation is inferred. Existing private wheels retain their original
versions, producers and digests. The corrected context re-executes the complete
installed selection as a new result; full receiving and final exact-head CI
outcomes are recorded on #56, preserving both earlier attempts.

The resolved provider implementation is no longer a blocking prerequisite.
This broader record remains partial for actual public package/platform/minimum
admission coordinated with #30/#47. See the
[maintained main receiving contract](../chemical_domain_receiving.md#main-source-receiving-and-complete-installed-gate--2026-11-03).
No publication or visible workflow acceptance occurs here.
