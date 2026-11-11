---
summary: E3's full historical PDBQT checksum conflates artifact identity with current-producer compatibility.
issue: uibcdf/bindingmt#88
status: resolved
opened: 2026-11-08
closed: 2026-11-09
severity: medium
verification: reproduced
area: [scientific-validation, provenance]
guard:
normative: devguide/validation/e3_source_control_receiving_2026-11-08.md
blocked_by: []
supersedes: []
---

# E3 source-replay artifact identity

## Delivered criterion; full receiving incomplete — 2026-11-08

The [prospectively amended selection](../validation/e3_source_control_receiving_2026-11-08.md)
passes exact current-control/treatment equality while authenticating the distinct
historical input. Strict full39 and prepared25 maps, stereo and rigid/H controls
also pass in the normal prefix. The old historical-checksum FAIL is preserved.
The new whole normal selection then fails at the third H5 write because the
provider's documented 0.5 codec rejects nonempty mechanics. Both reads and final
live checks are unreached; pm/fs is unattempted. The 156-member primary and
nine-member independent-reader archives authenticate this bounded outcome.

Keep this report partial until the amended complete normal/pm-fs selections
qualify. [MolSysMT #256](https://github.com/uibcdf/molsysmt/issues/256) owns the
lossless native mechanics persistence question; do not relax or remove that gate.
The criterion has been corrected in the prescription; this is not complete E3
or full unit-policy acceptance. No runtime/helper/data declaration changes.

## What

The first editable #645 receiving selection passes both explicit H-policy
operations and the strict full39 correspondence, then fails a comparison of a
new PDBQT export against a complete historical file checksum. The old and current
producers differ. The failure remains a failure; pm/fs was not attempted.

## How

The historical source SHA-256 is
`ae0e9d3beb4d14363ea6edb1bff591c56d53b02295082bae8c281d9284d84b9e`;
the current normal-profile export is
`49f054d3fa258bcf965619d7edb4f154949512aa74a3d57a0876da19af8ee9e0`.
Four provenance comments name the actual new MolSysMT version. Three ATOM Y
fields differ by 0.001 angstrom at the written precision. The historical
preparation used pm/fs; the new failed cell used the normal profile. A causal
explanation for the coordinate rounding difference is unestablished.

Prospectively register an independent source preparation with the same current
composition, unit policy, source authority, state, charge/type methods and rigid
preparation recipe, without H normalization. Require the normalized treatment's
complete PDBQT bytes to match this control. Retain the historical file verbatim
as a distinct authenticated artifact. Preserve the old failed selection and
every other chemical, geometry, correspondence, persistence and custody gate.

## Why

A historical full-file checksum authenticates its artifact. Requiring a new
honestly versioned export to have that checksum conflates provenance identity
with a controlled compatibility question. Stripping comments, falsifying version
stamps or silently tolerating coordinate differences would not correct it.

## What was refuted

The difference is not confined to comments. No provider writer defect, changed
chemistry or common receptor frame has been established. No downstream parser,
normalizer, atom matcher, coordinate restoration from diagnostic JSON or relaxed
scientific tolerance is justified.

## Scope and exclusions

This is a correction to the registered qualification criterion, owned by
BindingMT. Runtime and provider algorithms do not change. Full E3, MolSysMT #604,
legacy pose/frame admission, docking, public artifacts and visible acceptance
retain their separate gates.

## Acceptance criteria

The normative amended prescription must distinguish current paired-control
compatibility from historical artifact authentication, retain failed evidence
and require complete normal and pm/fs selections with all other original gates.
Seal and independently read the exact producers, records and outcomes. Update
#79 and current checkpoints, then archive this policy correction with its outcome.

## Bounded resolution — 2026-11-09

The complete suffix-03 [public-0.6 receiving](../validation/e3_h5msm06_reference_receiving_2026-11-09.md)
passes normal/pm-fs and independent 261-member/nine-member reading. Every original
scientific assertion remains; the final observer preserves literal strings and
detects five actual altered-copy losses, including unchanged-dtype F/farad.
All historical failures and weaker initial seals remain immutable. This resolves
the local criterion/observer concern for these exact inputs and editable sources;
full E3 and installed/public/hosted acceptance remain separate. Relevant local
and fresh committed-source documentation/resource checks accompany publication.
