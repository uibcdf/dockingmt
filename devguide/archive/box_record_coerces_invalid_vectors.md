---
summary: Saved box vectors bypass scalar admission through float coercion.
issue: uibcdf/dockingmt#85
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [core, arguments, serialization, units]
guard: tests/test_box_record_admission.py
normative:
blocked_by: []
supersedes: []
---

# Saved box vector admission

## Delivered correction and source qualification — 2026-11-08

The saved-box reader now admits complete value/unit mappings and three real
numeric scalars before converting them to float. Booleans, text, complex arrays,
wrong shapes and arbitrary float-only objects no longer acquire the meaning of
declared geometry. Invalid scalar/field/unit construction identifies `center`
or `lengths` through DMT-E002 and retains the provider cause where applicable.
MemoryError propagates with its original identity. PyUnitWizard still owns units;
existing BoxRegion admission still owns finite values, positive lengths and
derivation binding. No general geometry or quantity codec is added.

All 78 new cases run against the old reader: **38 fail and 40 pass**. The raw
JUnit retains each failure; the old log also retains two ComplexWarnings from
discarding array imaginary components. That complete selection remains FAIL.
The final complete source selection passes **234 cases per policy**, normal and
pm/fs with J/mol, no failures/errors/skips. It includes all new cases plus the
existing search-domain, schema and protocol #84 regressions. These are two
executions of the same case population. Valid/legacy records, integer/float
arrays, three length units, names, detached data, invalid derivation refusal
and caller policy are checked. Live molecular selection-derived domain workflows,
installed/public files and broader scientific acceptance are not rerun or claimed.

The [52-member primary evidence](../validation/data/box_record_admission_2026-11-08/manifest.json)
has SHA-256 `f115c01e500a2dbb898834978f662e10f14c181ac788f5ba231458ad592260f2`,
94,230 stored bytes. It retains original diagnosis, complete red/green source
and test snapshots, raw JUnit/policies/resources and bounded artifact triage.
The [17-member reader/publication companion](../validation/data/box_record_admission_reader_2026-11-08/manifest.json)
has SHA-256 `fd5e7f1245c3cc9428a6f2c2db0daa7bcd4473b009b964e9465b2f34ebca152e`,
21,916 stored bytes. Independent stdlib reading authenticates those stored/
decoded records, all original failure counts, final JUnit and policy/resource
facts without rerunning the source selection.

Probe/red/green durations are 0.818/5.955/10.567 s. Final-green sampled peak
group RSS is 101,928,960 bytes, minimum available 54,070,542,336 bytes. CPU 0,
nice 10, one worker, a monitored 13 GiB available reserve and 1 GiB group-RSS/
2 GiB address-space/45 s CPU/60 s wall bounds cover descendants. All groups are
terminal without resource interruption. Preserve
`.molsyssuite/box-record-admission-20261108` under #50/review 2026-11-14.

Publication uses final source/evidence/index/Ruff/resource/reporting checks and
an actual committed export for resource/index/publication contracts; exact
receipts remain in the task. No dependency, helper/data or scientific-input
change, build/install, native search or remote CI. #28's exact-head hosted
evidence remains missing under the authorized `[skip ci]` route. #19 and the
full Core/Extended/scientific/public/stabilization objective #73 stay partial.

## Bounded existing-artifact discovery

Public metadata covers the latest three releases, ten general runs, fifteen
manual runs and thirty PR runs at inspection; overlapping entries are not
independent observations or an exhaustive history. The three release headers
have no attached assets. Candidate Rust-wheel run 41839338780 at `fbb09782` and
public-ArgDigest run 42259461880 at `bd40d705` both use complete Rust tree
`32cfb07b9c26ae9ad3ed379c1b76fab85669cf67`; read-only immutable Git source checks
exclude them for the earlier three-correction target's required tree
`fb25b2eac60b6e706c712e788119b3dad94329fe`. No binary is downloaded/qualified and
no job/log interpretation or workflow dispatch follows. This is bounded source/
metadata triage, not proof that all private or historical artifacts are absent.
Compatibility with #645's later source remains separately unassessed. The
existing provider artifact request and held #642 construction remain unchanged.

## What

At source `8e6a8fd58165f5fa6adfd98787b146da8ef64318`,
`BoxRegion.from_dict` coerces center/length vectors to float before inspecting
their scalar types. Boolean and numeric-text elements become physical geometry;
Python complex values leak uncoded TypeError. Eight record-only observations
confirm both fields while preserving caller dictionaries.

## How

Admit each component-owned value/unit field and its exact three real values
before numerical conversion. Keep units in PyUnitWizard and shape/positive-
length/derivation semantics in BoxRegion. Local diagnostics identify the field
and preserve provider causes; resource errors propagate. Do not introduce a
general quantity codec, geometry algorithm or molecular fallback.

## Why

Saved search-domain geometry must describe its supplied numeric data. This
continues the #19 record-boundary review and complements pose #63/protocol #84.
The complete Core/Extended/scientific/public objective remains #73.

## What was refuted

This is not a provider unit parser or molecular geometry defect. An invalid
serialized scalar must be refused before its original type disappears.
Bounded artifact discovery also identifies two older provider-native source
contexts with the incompatible Rust tree; it receives no replacement binary.

## Scope and exclusions

Only saved BoxRegion vector admission and its focused source guards. No output
schema, engine default, molecular operation, source/provider/helper/data pin,
installation, public package or remote CI changes. Held native construction and
all old scientific failures remain.

## Acceptance criteria

Reject Boolean/text/complex/nonfinite/wrong-shaped vectors and malformed fields
with DMT-E002, preserve valid/legacy records, unit conversion, caller arrays and
active policy, and retain existing derivation refusal. Demonstrate old failures
then run complete affected offline selections under both unit policies. Retain
all raw JUnit/source/resource evidence, archive this record and synchronize #85
after final local and committed-export checks; #19 and #73 remain partial.
