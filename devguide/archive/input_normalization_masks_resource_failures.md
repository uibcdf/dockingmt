---
summary: Public input normalization masks native memory failures as invalid arguments.
issue: uibcdf/dockingmt#92
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: reproduced
area: [core, diagnostics, resources]
guard: tests/test_input_resource_errors.py
normative:
blocked_by: []
supersedes: []
---

# Native resource failures at public input boundaries

## What

Seven broad handlers in source `b195cf3ba27032ead16dd52086ea7e3631e18890`
translate provider MemoryError into ArgumentError: molecular input normalization,
box length normalization, energy/cutoff/unit/tolerance digesters and empirical
score units. This misclassifies a resource interruption as invalid user data.
Existing saved-record handlers already preserve resource failures explicitly.

## How

Use synthetic provider/quantity failures through public constructor, redocking,
box, protocol, evaluation, interaction-binding, backend-unit and score APIs.
Never exhaust memory or execute molecular operations to reproduce the boundary.
Preserve the exact MemoryError object, unchanged process-control exceptions,
ordinary field-local DMT-E002 diagnostics and provider cause, and valid input
selection/state/source behavior. Add only explicit resource passthrough before
ordinary exception translation; no new exception framework or retry policy.

## Why

Callers must distinguish resource exhaustion from invalid arguments and stop or
manage their own work appropriately. A diagnostic wrapper must not defeat that
choice. This is local exception ownership, not a demonstrated sibling defect.

## What was refuted

No provider change, molecule preparation, actual allocation failure, optional
engine or wider scientific rerun is needed. Unit/selection/state meaning and
provider ownership stay unchanged. Test doubles are software controls only.

## Scope and exclusions

Seven existing handlers in four files, with public source guards under normal
and pm/fs policies. No signature, schema, defaults, dependency/helper/data pin,
build/install, provider refresh, remote CI, scientific or canvas admission.
Respect the original #256 wait and #558 panel maps/history requirement.

## Acceptance criteria

Retain the original failing controls, pass complete affected source selections
under both unit policies, preserve ordinary diagnostics/native exception identity,
stop at injected failure, and verify unchanged non-handler AST and existing test
assertions. Update checkpoints/indexes and receive final resource/publication
checks, including a fresh committed export. #19/#73 remain partial; hosted
exact-head evidence stays under #28 and private custody under #50.

## Delivered source correction and exact receiving — 2026-11-08

Execution base: `b195cf3ba27032ead16dd52086ea7e3631e18890`, with frozen final
source/test bytes. The fix adds **seven explicit MemoryError passthrough branches**
in four existing modules, fourteen source lines in total. Molecular normalization,
box quantities, energy/cutoff/backend-unit/tolerance digesters and empirical score
units now preserve the original resource exception. Unit/shape/state/selection
checks, ordinary field diagnostics, original causes and valid behavior remain.
Independent AST receiving removes only those seven new bare-raise handlers and
obtains the exact original executable AST; no signature or scientific rule changes.

[The guard](../../tests/test_input_resource_errors.py) contains 139 public API
cases: three molecular entry routes at nine provider boundaries, four exception
families, three valid selection/state/source controls, and seven quantity-boundary
variants across those same exception families. A MemoryError/KeyboardInterrupt/
SystemExit object must propagate unchanged, and a ValueError must retain the
existing field-local DMT-E002 and exact cause. Call traces stop at the injected
boundary. No test exhausts RAM, invokes a molecular provider operation or executes
an optional engine. These are software controls, not scientific populations.

The corrected original 139-case selection remains **34 failures/105 passes**.
A complete old-runtime selection with the final test/tool bytes has **34 failures/
515 passes out of 549**, confirming the same defect population while retaining all
existing controls. Final complete affected source selections pass **549 normal,
then 549 pm/fs**, zero failures/errors/skips/deselections. They include complete
model/helper/schema/protocol/box/score/argument/interaction-binding modules.
Every original test assertion remains; no failing parameter is removed.

### Preserved initial failures and test-only dependency receiving

The first red selection records 37 failures/102 passes: 34 resource failures and
three test mistakes that request a nonexistent public chemical-state-ID property.
The corrected assertions read the same state ID from the supported public problem
record; the three cases then pass. Preserve both attempts and their meaning.
Import sorting changes no test assertion. The first expanded final-runtime
selection has 545 passes/four failures because declared test extra `unyt` is absent
from the routine environment; these are ModuleNotFoundError, not new runtime defects.

A native pip dry-run resolver against the unchanged routine environment identifies
only published `unyt 3.2.0`, `sympy 1.14.0` and `mpmath 1.3.0`. Exact public wheel
URLs/digests, downloads and a 1,714-file SHA-256 inventory authenticate a **separate
private test-only prefix**. No shared Conda installation is modified, no molecular
provider is overlaid and no source distribution is built. Final source children
verify the prefix before use and every imported support module afterwards.
Native published Receptor 1.2.2 retains its separately authenticated 15-file prefix;
the routine environment's editable Receptor metadata remains 1.2.0. Neither tool
prefix establishes public molecular dependency closure or installed delivery.

The complete old-runtime baseline and both final profiles use identical test/tool
bytes and this exact unit-support prefix. The old runtime still fails the same
34 controls; all four unyt cases pass. Thus installing test support is not credited
with fixing resource propagation, and the initial dependency failure stays retained.
No shared-environment installation or actual out-of-memory event occurred in
these tests.

### Immutable records, resources and limits

The [164-member primary manifest](../validation/data/input_resource_errors_2026-11-08/manifest.json)
is SHA-256
`f706008a18f436c45a94a4e90b70bed309ef97826f872f175beb659cb5e22410`.
It retains all original/corrected failures, old/full/final source snapshots,
producers, native events/JUnit/logs, support resolution/wheel receipts and resource
outcomes. The [nine-member independent-reader companion](../validation/data/input_resource_errors_reader_2026-11-08/manifest.json)
is SHA-256
`ce7005b7c9992bfc9df2e9580cfb8e24ca68d9b39949a87d679e862f9eb8aac6`.
Stored/decoded byte receiving, Receptor/JUnit/count agreement, all 34 original
failures, test/source identity and the exact seven-handler AST delta pass without
replaying tests or importing molecular/unit-support packages.

Final full cells take 7.061/16.871 s, sampled group peaks
192,086,016/192,090,112 RSS bytes. Minimum available memory remains above 59 GB
across the test attempts. Test support preparation takes 3.442 s, sampled peak
80,281,600 RSS bytes. Every owned group is terminal without resource interruption.
CPU 0/nice 10/one worker, monitored 13 GiB available reserve, 1 GiB group RSS,
2 GiB address space and CPU 45/wall 60 second bounds apply to descendants.
Availability is not a reservation; no Slurm allocation or native build is started.

Retain `.molsyssuite/problem-memory-20261108`, its original wheels/private prefix
and receipts under #92/#19/#50, review **2026-11-14**. Original migration files,
provider checkouts, shared environment and the earlier interrupted native build
remain protected. The 594 helper/data declarations and original scientific inputs
are unchanged. All seven local checks pass: Ruff, formatting, report indexes,
shared resources, publication contract, diff and exact source/archive receiving.
A fresh committed-source export must also pass its six corresponding checks
before the authorized `[skip ci]` push; exact committed receipts are reported
in #92. No remote CI is dispatched, and
current-head hosted evidence remains missing under #28.

This closes the bounded source defect only. #19's wider adoption/public closure,
#73's complete Core/Extended/scientific/installed/public outcome and #52/#60 canvas
acceptance remain partial. Continue independent accepted work while respecting
the maintainer's #256 wait, E3's original lossless-reference gate and #558 panel
maps/history. No provider pull/build, synthetic substitute or repeated completed
scientific population follows from this source correction.
