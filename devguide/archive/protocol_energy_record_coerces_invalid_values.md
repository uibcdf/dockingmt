---
summary: Saved protocol energy magnitudes bypass scalar admission through float coercion.
issue: uibcdf/dockingmt#84
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [core, arguments, serialization, units]
guard: tests/test_protocol.py
normative:
blocked_by: []
supersedes: []
---

# Protocol energy record admission

## Delivered correction and qualification — 2026-11-08

`VinaProtocol.from_dict` now admits a parameter mapping and a real numeric
scalar in the saved energy value/unit mapping before constructing its quantity.
Booleans, text, vectors, complex values and arbitrary `__float__` objects cannot
become accepted energy magnitudes. PyUnitWizard retains unit parsing/conversion;
the existing constructor retains energy dimensionality, finite and nonnegative
checks. Invalid unit construction carries DMT-E002/`energy_range` and its
provider cause; invalid parameter containers name `parameters`. A resource
MemoryError propagates with its original identity.

Generated numeric records, integer/float NumPy scalars, kcal/mol and kJ/mol,
supported unit-bearing strings and legacy omitted defaults remain readable.
Incomplete saved mappings reject explicitly. Caller records and the chosen
default form/parser/standard units survive both success and refusal. No schema,
quantity codec, engine setting or molecular operation changes.

The original source diagnostic observes True→1 and False→0 in seven read-only
pairs. With the new initial guards, the old reader has **18 failures / 15 passes
out of 33 cases**. That complete selection remains FAIL. After correction, the
first affected source selection passes 152 cases under each policy. Four final
guards add incomplete mappings and resource-failure identity; the complete
final selection passes **156 cases per policy**, normal and pm/fs with J/mol,
zero failures/errors/skips. These are two executions of the same case population,
not 312 independent tests. The 37 new protocol-reader cases supplement the
existing protocol/argument/schema tests. The public molecular entry points
`get`, `select`, `extract`, `convert`, `copy` and `set`, plus optional engine
imports, are blocked in the harness; no watched call is attempted.

The [67-member primary evidence](../validation/data/protocol_energy_record_2026-11-08/manifest.json)
has SHA-256 `67ba1078d3a29bc531f0e57dce26095ae1f04f5511ee2fce06c77b53199775de`,
87,970 stored bytes. It retains original diagnosis, complete red/first-green/
final-green records, exact runtime/test producers, raw JUnit and caller policies.
The [17-member reader/publication companion](../validation/data/protocol_energy_record_reader_2026-11-08/manifest.json)
has SHA-256 `d9d42bf640b612a21c447e847a72afa547b16aba849aa6a564176ac48a7c1ce5`,
20,935 stored bytes. Independent stdlib reading authenticates all decoded/stored
members, source identities, 18 original failures, final JUnit cases, policies
and terminal resources without rerunning the tests.

Original probe/red/final-green durations are 0.819/2.155/3.798 s; final-green
sampled peak group RSS is 101,306,368 bytes, minimum available 58,434,666,496.
One CPU 0/nice 10/worker 1, monitored 13 GiB reserve, 1 GiB group-RSS/2 GiB
address-space/45 s CPU/60 s wall bounds apply to descendants. Every group is
terminal, no resource interruption; red's FAIL is a functional outcome.
Keep `.molsyssuite/protocol-record-energy-20261108` under #50/review 2026-11-14.

Publication checks authenticate exact source/evidence, indexes, Ruff, shared
resources, declared dependency routes and maintained links; an actual committed
export separately checks resource/index/publication contracts. Exact receipts
remain in the task. This is focused source qualification, not new installed
wheel, full-suite, public/platform or scientific acceptance. #28 retains missing
exact-head hosted evidence under the maintainer's `[skip ci]` route; #19 and
the full #73 objective remain partial. MolSysMT artifact/clustering/canvas and
the native-build hold retain their owners. No helper/data or provider pin changes.

## What

At source `a870142ef1d8ab936e4adbbfb04a59763307fe66`,
`VinaProtocol.from_dict` converts the legacy value/unit record's magnitude with
`float()` before quantity admission. True becomes 1 kcal/mol and False becomes
0; vectors/complex values leak uncoded TypeError. This can silently change the
meaning of a saved protocol. The seven-pair diagnostic preserves the caller's
record and runs no molecular/backend work.

## How

Admit the component-owned saved numeric scalar without Boolean/text/vector/
complex coercion. Keep physical units and conversion in PyUnitWizard and the
existing constructor's finite/nonnegative/energy checks. Invalid parameter
containers and quantity construction need DMT-E002 with the failing field and
provider cause where applicable. Preserve valid and legacy defaults, supplied
quantity/string inputs and caller policy. Do not introduce a new record codec.

## Why

Record reconstruction must preserve the protocol's declared meaning rather than
turn an invalid JSON Boolean into a legitimate energy threshold. #19 owns the
broader public argument review; Core C5/#73 retains complete workflow acceptance.

## What was refuted

PyUnitWizard legitimately parses numeric text when explicitly supplied with
units; that public constructor behavior is separate from a stored numeric
field. Its refusal to construct a Boolean quantity is not a provider defect.
No old molecular failure, native build hold or public artifact is changed.

## Scope and exclusions

Only VinaProtocol saved-record admission and its focused regression evidence.
No schema/version, engine/default CPU/search/chemical model, provider pin,
helper/data, public package or CI route changes.

## Acceptance criteria

Reject invalid saved scalars and parameter containers with actionable local
diagnostics; retain valid scalar/unit conversion and legacy defaults without
mutating input or caller unit policy. Demonstrate old failures and pass the
affected offline protocol/argument/schema selection under both declared unit
policies. Preserve original diagnosis and all attempts. Archive after the
durable regressions and publication checks pass; keep missing hosted evidence
owned by #28 and the full objective open.
