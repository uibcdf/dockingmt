---
summary: Reject unsupported AD4 scoring before Vina execution
issue: uibcdf/dockingmt#23
status: resolved
opened: 2026-10-02
closed: 2026-10-03
severity: medium
verification: measured
area: [vina, capabilities]
guard: tests/test_backend_contracts.py::test_ad4_rejected_before_problem_hooks_preparation_or_provider
normative: devguide/ENGINES.md
blocked_by: []
supersedes: []
---

# Vina adapter advertises unsupported AD4 scoring

## What

`VinaBackend` declared `scoring_ad4` and accepted the required capability while
always invoking the Vina-map calculation path. DockingMT has no external map
input or `load_maps` execution path. The local capability check therefore
promised a scoring mode that the adapter could not execute.

## How

Before the fix, `VinaBackend().validate_capabilities(VinaProtocol(scoring='ad4'))`
succeeded. An isolated process with AutoDock Vina 1.2.7 rejected
`Vina(sf_name='ad4').compute_vina_maps(...)` with `RuntimeError`, reporting that
Vina affinity maps cannot be computed using AD4. This is also explicit in the
[versioned upstream implementation](https://github.com/ccsb-scripps/AutoDock-Vina/blob/v1.2.7/src/lib/vina.cpp#L292-L299).

The bounded local fix removes `scoring_ad4` from the adapter's capabilities.
AD4 protocol intent remains serializable but fails execution through
`CapabilityMismatchError` (`DMT-E003`) before problem hooks, input preparation,
temporary input staging, or provider imports. A non-Vina protocol is rejected
before calling its validation hook. Capability diagnostics expose the protocol
name and sorted requested, supported, and missing capability sets.

## Measured validation (2026-10-02)

- Before the fix, nine of eleven new contract tests failed, exposing false AD4
  acceptance, execution of an incompatible protocol hook, invalid-protocol
  `AttributeError`s, and missing structured capability data.
- The eleven contract tests now pass without warnings. Their guards forbid
  problem validation, box projection, preparation, input staging, native Vina
  imports, and MolSysMT form/get/select/extract/convert operations during rejection.
- The existing native PDBQT execution test now covers both Vina and Vinardo,
  checks the named score and serialized scoring choice, and continues to verify
  input fingerprints and pose identity.
- Full `pytest --receptor=llm`: 197 passed in 42.79 seconds on Python 3.13.14,
  compared with the preceding 185-test baseline. The same twelve provider
  warnings remain; no new diagnostic warnings were introduced.
- `ruff check .`, `ruff format --check .` (69 Python files),
  `python devtools/devguide_index.py --check`, and whitespace checks passed.
- These are local checks against editable sibling sources and installed Vina
  1.2.7. No hosted matrix result or scientific preparation qualification is claimed.

## Why

Upstream engine capabilities and DockingMT adapter capabilities are different
contracts. Clients need an accurate execution decision before potentially
expensive preparation or a provider failure. This fulfills the existing Core
MVP capability gate rather than introducing a new scoring workflow.

## What was refuted

Installing Vina cannot provide the missing adapter map-input path. Silently
substituting Vina scoring for requested AD4 would change scientific intent.
Removing AD4 from protocol serialization would also discard otherwise valid
intent; the execution boundary owns the unsupported-capability decision.

## Scope and exclusions

Only DockingMT's capability declaration, rejection order, and diagnostics are
changed. MolSysMT and MolSysViewer are not modified or coordinated. This does
not generate, load, or validate external AD4 maps; qualify molecular preparation;
or add new engines. Existing Vina/Vinardo software execution is guarded using
prepared PDBQT fixtures, without a new docking-performance claim.

The guarded implementation is committed with this record. The issue remains
partial pending hosted qualification; local validation and publication do not
establish compatibility with CI's pinned dependency set.

## Acceptance criteria

- AD4 execution fails through the local capability error before problem handling
  or provider invocation, including the top-level `dock` route.
- Invalid protocol inputs fail clearly, and rejected protocol hooks are not run.
- Supported Vina/Vinardo requests still execute and preserve named scores.
- Protocol intent and serialized parameters remain inspectable.
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
