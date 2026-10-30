---
summary: Receive independent ChemicalStates storage and graph tools from MolSysMT.
issue: uibcdf/dockingmt#56
status: partial
opened: 2026-10-28
closed:
verification: measured
area: [integration, preparation, validation]
guard: tests/test_torsion_policy_consumption.py::test_qualification_probe_compares_assigned_and_reference_connectivity
normative: devguide/chemical_domain_receiving.md
blocked_by: [uibcdf/molsysmt#255]
supersedes: []
---

# Receiving the chemical-domain cutover

What — Torsion preparation and symmetry consume the four moved graph tools from
`msm.chemical_states`; state fixtures use the independent chemical owner.

How — The [receiving contract](../chemical_domain_receiving.md) identifies source
pins, current audit tools, historical producers and qualification boundaries.
Controlled CI inputs select MolSysMT 9fb77c358 and compatible Viewer ca7ebea60.
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
