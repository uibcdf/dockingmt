---
summary: Interaction binding leaks scalar/form errors for absent carrier domains.
issue: uibcdf/bindingmt#89
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [arguments, analysis, diagnostics]
guard: tests/test_interaction_binding.py::test_missing_carrier_domains_have_a_local_argument_diagnostic
normative:
blocked_by: []
supersedes: []
---

# Interaction binding and partial carrier diagnostics

## Delivered source correction — 2026-11-08

Both public routes now check absent successful atom/frame count returns before
integer coercion, and absent coordinates before unit extraction. The existing
catalog BMT-E002 identifies `molecular_system` and its missing domain. Actual
provider exceptions remain untouched; no domain, geometry, frame or analysis
is invented. Existing valid/adverse binding, coverage and detachment remain.

The final complete binding/view selection passes **78 cases per caller policy**,
normal and pm/fs, zero failures/errors/skips/deselections. Native JUnit and
Pytest Receptor agree. Real molecular operations, optional engines, provider
View construction and native searches are guarded and remain zero. The guard
exercises each missing domain through both public routes; existing valid,
unit, source-preservation, detachment and provider-error cases also pass.

The original six-failure selection remains FAIL: four TypeError and two low-level
quantity-form errors. An earlier preformat complete normal PASS remains separate.
The initial format check requests two test-only wraps; the formatter preserves
the complete test AST, including all original regression assertions. Final
normal/pm-fs use identical runtime/test bytes. Root-wide Ruff also finds I001
in the untracked private migration script; that bundle remains untouched.
Final Ruff check/format explicitly exclude its directory and pass (255 formatted
source files). Initial quality failures are retained as console observations;
complete raw final gate logs are retained separately.

The [60-member primary archive](../validation/data/interaction_carrier_admission_2026-11-08/manifest.json),
SHA-256 `0f9f3c78dab5c7e1d591195425c9fe0d50558129bf9ff7047910afc3a859d4f6`,
contains 143,364 stored / 933,978 decoded bytes: original/final inputs, workers,
registrations, logs, complete receptor streams, JUnit, policies and resources,
at execution base `1ffff2ea`. The independent reader uses the provider's supported
`read_artifact`, checks native JUnit and source/AST agreement, and reruns no tests
or molecular work. Its [nine-member companion](../validation/data/interaction_carrier_admission_reader_2026-11-08/manifest.json)
is SHA-256 `9e853eca5c622c32e6d34850dd0240835d4c86279c89b95ddd5e8df2ef292f9f`
(12,470 stored / 37,694 decoded bytes), retaining reader/controller/guard,
registration, logs, receipt and resource outcome.

Final normal/pm-fs cells take 3.374/3.474 s, peak sampled group RSS
154,394,624/154,587,136 bytes and minimum available RAM
60,113,821,696/60,292,354,048 bytes. Red takes 1.634 s / 82,370,560 bytes;
preformat PASS takes 3.371 s / 154,636,288 bytes. All owned groups terminate
without resource interruption under CPU 0/nice 10/one native worker, monitored
13 GiB reserve, 1 GiB group RSS, 2 GiB address space and 45 CPU/60 wall seconds.
Retain `.molsyssuite/interaction-carrier-admission-20261108` under #50, review
2026-11-14. No installation/build, molecular replay, browser/kernel or remote CI.

This closes the local source diagnostic only; full E4/scientific/installed/
canvas, E3's MolSysMT #659/#256 holds and complete #73 remain unaccepted.
Final publication gates cover Ruff, formatting, indexes, resources, publication,
whitespace and source/archive scope, with applicable checks and archive
authentication on a fresh committed export. The unchanged 30-helper/564-data
declaration remains authoritative. Exact-head hosted evidence stays pending
under #28; skipped CI is not a pass.

## What

The local one-frame association requires known carrier atom/structure counts
and coordinates. Successful provider queries returning `None` instead reach
`int(None)` or PyUnitWizard quantity extraction. Both public routes leak low-level
errors rather than identifying the incompatible `molecular_system` argument.

## How

Six new cases use the existing explicitly synthetic provider fixture, covering
three missing returns through `bind_interactions` and `PoseInteractions`.
The original `1ffff2ea` runtime fails all six: four TypeError and two provider
NotImplementedFormError, zero errors/skips in the pytest summary. This red
population remains FAIL. No real molecular operation, engine or canvas executes.

Check missing successful returns before scalar coercion or physical extraction.
Use the existing BMT-E002 catalog exception with `arg_name='molecular_system'`
and an actionable domain explanation. Keep actual provider exceptions unchanged.

## Why

Partial molecular representations are valid provider inputs, but cannot establish
this association's atom/frame/coordinate contract. Users need an admission error
at the binding boundary, without a misleading unit-form or Python scalar error.

## What was refuted

No faulty molecular detector, coordinate generation, provider format conversion
or PyUnitWizard behavior is established. This is a BindingMT consumer check;
there is no justification for a provider workaround or broad exception wrapper.

## Scope and exclusions

Do not repair or invent domains, maps, chemistry, frames or analyses. Keep known
zero/multiple frames refused, ordinary provider failures propagated, original
result/carrier unchanged, accessors detached and evaluation coverage distinct.
This source correction does not accept molecular/installed/public profiles,
actual canvas or the full E3/E4/Core/Extended objective.

## Acceptance criteria

The guard must fail on the original runtime and pass on the correction through
both public routes. Complete affected binding/view source cases must pass under
normal and pm/fs caller policies, including existing valid/negative/detachment/
provider-error controls. Run Ruff and applicable document/resource gates,
retain exact failures and final evidence, update current checkpoints, archive
this record and synchronize the owning issues.
