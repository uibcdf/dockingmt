---
summary: Result pose collections admit malformed empty axes and unordered live inputs.
issue: uibcdf/dockingmt#87
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [core, arguments, serialization, provenance]
guard: tests/test_result_record_admission.py
normative:
blocked_by: []
supersedes: []
---

# Result pose collection admission

## Delivered correction and source qualification — 2026-11-08

The saved-result reader now requires a list/tuple pose axis and validates each
member as a mapping before copying or coordinate construction. Invalid members
raise DMT-E002 naming `poses` with their zero-based `pose_index`; nested version
failures retain their existing schema diagnostic and before-copy priority.
Malformed empty objects/text/sets can no longer appear to be legitimate empty
results. Omitted legacy axes and actual empty lists/tuples remain supported.

The live ArgDigest boundary now refuses Set inputs before iteration. Ordered
lists/tuples/generators retain order, borrowed pose identity and single source
consumption. Saved records preserve order, multiplicity, scores/IDs/metadata and
detached copies, including nested outcome reading. No sorting, deduplication,
schema change or molecular inference is introduced. Resource exceptions retain
their original identity.

The 47 new cases expose **31 failures / 16 passes** on the original source.
That complete selection remains FAIL. The final affected source selection
passes **383 cases per policy**, normal and pm/fs with J/mol, zero failures/
errors/skips. It includes previous coordinate/protocol/box/schema and argument
guards. These are two executions of the same software-case population. The six
watched molecular entry points and optional engine imports remain uncalled;
per-profile pytest caches/report state are task-owned.

The [75-member primary evidence](../validation/data/result_collection_admission_2026-11-08/manifest.json)
has SHA-256 `4dbd6ca79d1e50146b91af49e2a75c7ae4acbd26730e6afb57e644e0a5dc6662`,
139,095 stored bytes. Original diagnosis/red/green snapshots, registry attempts,
raw JUnit, policies and source/resource identities remain. The
[17-member reader/publication companion](../validation/data/result_collection_admission_reader_2026-11-08/manifest.json)
has SHA-256 `32d52779eae0fe6e487eae6e5942665760266355d7c9d579def47be69269b89a`,
21,313 stored bytes. Independent stdlib reading authenticates every stored/
decoded member, original failure counts, final JUnit, source and policy/resource
facts and registry identity comparison without rerunning those operations.

Probe/red/green durations are 1.330/4.410/4.923 s. Final-green sampled peak
group RSS is 103,493,632 bytes, minimum available 56,338,014,208 bytes. CPU 0,
nice 10, one worker, monitored 13 GiB reserve and 1 GiB group-RSS/2 GiB address-
space/45 s CPU/60 s wall bounds cover descendants. Every group is terminal with
no resource interruption; red's FAIL is functional. Preserve
`.molsyssuite/result-collection-admission-20261108` under #50/review 2026-11-14.

Final local checks cover source/evidence/index/Ruff/resource/reporting contracts;
actual committed export separately checks resource/index/publication and
qualified blob identity. Exact receipts remain in the task. This is focused
source qualification, not new installed/public/scientific acceptance. #19 and
the full #73 objective remain partial; #28 exact-head hosted evidence remains
missing under the authorized `[skip ci]` route. Provider artifact/clustering/
generation, canvas and native-build holds remain. No dependency/helper/data/pin,
scientific input, build/install, molecular/native-engine or CI change occurs.

## Fresh public registry observation and limits

The sandboxed probe's DNS failure is retained as an unavailable observation,
not artifact absence. A separately registered read with authorized network
access completes in 0.925 s under the same resource controls. The 183,573-byte
response has SHA-256
`088fc593476ce62bdf4101d2413986b9a2c3bd4c417202477e427cbd9e80734c`.
All 107 basename/version/SHA-256/size/upload-time identities equal the retained
prior inventory; no new advertised file is observed. Both raw/current and
prior records are independently authenticated. This is dated public metadata,
not package payload qualification, proof about private artifacts, or a complete
dependency closure. The provider artifact request and held construction remain.

## What

At source d5fe700b2bfe1eea9ee15f2de0f6fae0cb50b459, explicit malformed empty
mapping/text/set pose axes can be read as zero-pose results. Null axes leak
TypeError; invalid members name the root data argument. Live constructors also
accept unordered sets for the positional pose axis. Nine record and three live
controls retain these observations and valid/legacy positive controls.

## How

Require a stored list/tuple axis and mapping members before copying/conversion.
Keep nested version admission and its before-copy priority. Exclude Set inputs
from the live ArgDigest boundary without restricting ordered iterables/generators.
Use DMT-E002 naming poses and the invalid member position. Preserve order,
multiplicity, scores/IDs/metadata, detachment and resource failures.

## Why

An invalid record must not look like a genuinely empty result. Positional axes
must preserve declared input order. This continues #19's component-owned public
record review; the full functional/scientific/public objective remains #73.

## What was refuted

Do not repair mappings, sort or deduplicate input to produce a valid axis.
Omitted legacy poses and legitimate empty lists/tuples remain supported.
A sandboxed registry lookup failed DNS; the separate bounded network-enabled
lookup succeeds with the same 107 advertised identities. Neither substitutes
for actual compatible artifact receiving.

## Scope and exclusions

Only pose-collection argument/record admission and inherited outcome reading.
No schema/output, molecular/native algorithm, backend, provider/helper/data pin,
build/install or CI change. Historical failures and native/canvas holds remain.

## Acceptance criteria

Prove old failures, then qualify malformed axes/members before iteration/copy,
nested schema priority, valid/legacy tuple/list records, ordered live generators,
order/multiplicity, detached results and resource exceptions under both policies.
Retain raw evidence, archive this report and synchronize its owning issue after
local/committed-export checks. Installed/public/scientific evidence stays separate.
