---
summary: Review Python support-library and developer-tool adoption
issue: uibcdf/dockingmt#19
status: partial
opened: 2026-09-27
closed:
verification: measured
area: [governance, tooling, arguments, diagnostics, dependencies, units]
guard: tests/test_argument_contracts.py
normative:
blocked_by: []
supersedes: []
---

# Review Python ecosystem policy adoption

## What

Review support-library and developer-tool adoption independently under
`uibcdf/molsyssuite#56`. Declaring a dependency is not evidence of runtime adoption.

## How

### Initial adoption audit (2026-09-27)

The earlier audit inspected `9c5d56a4288af1e2dedd4c99f3a9bf7987592f6c` on
`origin/main` under `uibcdf/molsyssuite#56`. Support-library and developer-tool
adoption were partial: three of the four declared support libraries had runtime
paths, while `_argdigest.py` had no package call sites. CI run `36310576692`
passed all four jobs, and suite policy run `36310577050` passed. Published GH
Run Receptor `1.0.0` inspected both runs. The maintained test command already
selected `--receptor=ci`, but `devtools/conda-envs/test_env.yaml` and the test
extra left `pytest-receptor` unpinned. An exact published receptor pin and a new
hosted run confirming the installed version remain outstanding. Green CI did
not establish either that exact tool version or public argument coverage.

### Runtime implementation (2026-10-02)

The first implementation block covers `dock`, `VinaBackend.dock`, `VinaProtocol.__init__`,
`prepare_ligand`, and `prepare_receptor`: closed argument admission, meaningful
value validation, explicit energy units, stable catalog diagnostics, and lazy
optional Vina/viewer dependency checks. Molecular forms and selection interpretation
remain owned by MolSysMT; DockingMT validates docking options and absent inputs.

## Why

The initial ArgDigest configuration pointed to a nonexistent package. Protocol
integer parameters accepted booleans or truncated fractional values. Bare energy
values implicitly meant kcal/mol, and nonfinite quantities were accepted. Local
SMonitor entries lacked stable codes, and warning constructors could not rebuild
from their rendered message. MolSysViewer had a dependency decorator without a
matching declaration.

## Measured evidence (2026-10-02)

- Baseline: 103 tests passed. After the runtime block: `pytest --receptor=llm`
  passed all 151 tests in 45.41 seconds on Python 3.13.14. The same 12 provider
  warnings remain (11 deprecated H5MSM 0.4 reads and one occupancy drop).
- `ruff check .`, `ruff format --check .`, and
  `python devtools/devguide_index.py --check` passed.
- `tests/test_argument_contracts.py` covers rejected coercion, unknown names,
  energy units/shape/finiteness, round trips, and rejection before molecular or
  backend operations. Existing preparation, Vina, redocking, and replay guards
  continue to pass.
- `tests/test_support_contracts.py` covers all five catalog codes across five
  profiles, diagnostic reconstruction/pickle/copy, structured warning emission
  with Python filters, and missing Vina/viewer dependencies.
- An isolated process loaded CI's pinned ArgDigest source
  `4fdbf19d386bbf476455d35c9988bf00624873e1` and passed a bounded probe of explicit
  unit conversion, protocol round trips, invalid integer/energy values, and
  unknown argument admission. This is not a hosted three-version CI result.
- Full local tests use editable sibling checkouts. They do not establish
  compatibility with the published dependency set. The local test runner needed
  permission to open the socket used by the installed `pytest-rerunfailures`
  plugin; no repository test-runner configuration was changed.

## What was refuted

Replacing MolSysMT's molecular-form or selection contracts with DockingMT's own
recognition rules would duplicate provider responsibilities. Support-library
runtime evidence alone cannot close the independent developer-tool review.

## Independent search-domain block (2026-10-02)

Continue Gate C0/C3 while MolSysMT preparation work proceeds separately. The
explicit `BoxRegion` constructor and `contains` now use ArgDigest. Geometric
inputs use PyUnitWizard's quantity boundary and reject nonfinite or non-real
values. Supplying both `lengths` and `size` is rejected instead of silently
choosing one. Padding must be a finite nonnegative scalar length.

`from_points` previously rejected single-point, linear, or planar point sets
even when padding was positive: `from_bounds` rejected equal corners before
padding could expand them. Ordered equal corners now work when padding yields
strictly positive final dimensions; inverted bounds and zero-volume final boxes
remain invalid. This corrects the existing documented point-based workflow.

The block changes only local search-domain geometry and argument validation.
MolSysMT coordinate retrieval in `from_selection` is untouched. The pure geometry
guards are in `tests/test_search_domain_contracts.py`, including a test that
forbids MolSysMT `get`, `select`, and `convert` during explicit construction,
serialization, containment, and backend-unit export. Class factories retain
Python's closed signature admission and share the geometric value validators;
they are not claimed to have complete ArgDigest constructor coverage.

Validation after this block: all 185 tests passed in 47.70 seconds on Python
3.13.14, including 34 new geometric regression cases. The same 12 provider
warnings remain. Ruff checks, format checks (68 Python files), generated indexes,
and whitespace checks pass. The isolated probe using CI's pinned ArgDigest
revision also passed for padded point construction, round trips, containment,
nonfinite dimensions, and unknown keyword rejection. This remains local evidence,
not a new hosted CI or published-dependency qualification.

## Capability-validator boundary (2026-10-02)

`DockingBackend.validate_capabilities` now also uses ArgDigest and rejects absent
or mistyped protocols with local diagnostics. Its structured mismatch includes
all requested, supported, and missing capabilities. The associated execution
ordering defect and unsupported AD4 declaration are tracked independently in
[DockingMT #23](https://github.com/uibcdf/dockingmt/issues/23), with evidence in
[`vina_adapter_advertises_unsupported_ad4_scoring.md`](../pending_bugs/vina_adapter_advertises_unsupported_ad4_scoring.md).
After this block, all 197 tests and the local quality gates passed. This does not
complete the outstanding developer-tool or provider qualification review.

## Result-ranking boundary (2026-10-02)

`DockingResult.rank_by` now uses ArgDigest to validate the named score and require
an explicit boolean direction, including unknown-keyword rejection. Named score
validation and independent serialization boundaries are tracked separately in
[DockingMT #24](https://github.com/uibcdf/dockingmt/issues/24) and
[DockingMT #25](https://github.com/uibcdf/dockingmt/issues/25). The bounded guards
are in `tests/test_result_contracts.py`; these operations request no molecular
or viewer operations. Pose/result constructors and serialization methods are
not claimed to have complete ArgDigest coverage by this block.

After this block, all 233 tests passed in 42.48 seconds, including 36 new
result-model contract cases; the same twelve provider warnings remain. Local
quality gates also pass. This extends runtime evidence without closing the
developer-tool or published-dependency review.

## Publication validation (2026-10-02)

Before publication, the implementation was rebased onto `origin/main` at
`12f06dc`, preserving the initial adoption audit and the independent CI/governance
work. Full `pytest --receptor=llm` then passed all 237 tests in 70.59 seconds on
Python 3.13.14, including four CI-backlog tests supplied by those remote changes.
The same twelve provider warnings remain. Ruff checks, format checks (72 Python
files), generated indexes, and whitespace checks pass. The implementation is
committed with this record; hosted compatibility remains separately qualified.

## Scope and exclusions

This block does not change chemistry, molecular selections, provisional-preparation
policy, torsion perception, scoring, or engine selection. `view(**kwargs)` delegates
viewer options to MolSysViewer; its open keyword interface is not declared fully
digested. Prepared-object constructors and complete ArgDigest coverage for
search-domain class factories remain separately reviewed boundaries. The CI dependency fallback and exact published developer-tool pins
remain outstanding, as do central adoption-inventory updates. Do not close #19
or claim suite-wide adoption from this block.

## Acceptance criteria

- Representative invalid public calls fail before preparation or backend execution.
- Physical energy inputs carry explicit units; default and serialized protocols
  retain the same resolved 3 kcal/mol cutoff.
- Diagnostics have catalog codes, typed occurrence data, and rebuildable messages.
- Missing optional dependencies fail lazily with actionable diagnostics.
- Record measured local validation separately from hosted compatibility evidence.
- Pin the reviewed published receptor version and record an exact-commit hosted
  run confirming that version with unchanged test selection.
- Complete the remaining public-boundary and developer-tool review before closing.
