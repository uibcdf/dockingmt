# BindingSite finite molecular contract receiving

Owner: [BindingMT #111](https://github.com/uibcdf/bindingmt/issues/111).
Review: 2026-11-14. Status: owner disposition reviewed and selected for C1;
actual client source/native receiving and `resolve_region` remain pending.

## Delivered owner offer

[MolSysMT #746's response](https://github.com/uibcdf/molsysmt/issues/746#issuecomment-6871608700)
closes its finite review. The published source is
`27ba3d4c8d63a6a40a2d77f0190309ff15f4deef`, with contract/controls
`f9f384412c209089dc591c9e484b1ab985cebe70` and selection correction
`6deed142d222605a8f1b1f6baee634523372b243`.
Read the [normative owner contract](https://github.com/uibcdf/molsysmt/blob/27ba3d4c8d63a6a40a2d77f0190309ff15f4deef/devguide/native_binding_site_membership_contract.md),
[meaningful 18-case guard](https://github.com/uibcdf/molsysmt/blob/27ba3d4c8d63a6a40a2d77f0190309ff15f4deef/tests/basic/test_binding_site_membership_handoff.py)
and [exact receiving receipt](https://github.com/uibcdf/molsysmt/blob/27ba3d4c8d63a6a40a2d77f0190309ff15f4deef/devtools/data/binding_membership_receiving_746_750_20261113.json).
The owner reports 356 selected cases and an overlapping final 18-case module;
do not add them as independent full suites or call them BindingMT adoption.
The reference native SHA-256 is
`4ffb82e4250a1862fff17dbe7725fb8f0770d613ffef2648370389a66983d345`.

[MolSysMT #750](https://github.com/uibcdf/molsysmt/issues/750) repairs invalid
structure-index admission for numeric and `all` selections, reusing the existing
public validator before every branch. Its original 12-failure/six-pass regression
remains preserved. The owner review is complete; this is no longer a pending
request for an unspecified provider capability.

## Mapping the offer to C1

| Requirement | Received public fact | BindingMT implementation/qualification obligation |
| --- | --- | --- |
| Native axes | Public native/get cardinalities and atom/group relationships; explicit numeric selection bounds/order | Admit the actual native domains and declared source/target axes; do not turn counts or labels into origin/revision authentication. |
| Ordered group expansion | One atom list per requested group, in request order | Preserve entry-aligned outputs. A source-ordered selection expression or mask is not an ordered group-expansion receipt. |
| Known extraction | Atoms are sorted unique source indices; groups follow first surviving atom occurrence | Retain maps from that known operation. There is no general extraction map report; never invent one or infer group identity from duplicated labels. |
| Permutation/composition | Public complete atom directions and checked composable atom maps, with omissions/generated members | Use the owner validator/composition; retain declared adjacent-asset association. Validate forward indices before lookup so -1 cannot mean Python's last atom. |
| Group correspondence | Aligned surviving source/output atom parents support groups in the known operation | Empty groups and unrelated assets need explicit correspondence. Unknown parentage must not certify complete expansion or a negative finding. |
| Repeated structures | `[2,0,2]` preserves three occurrences and associated states; source 2 maps to target 0 and 2 | Retain an occurrence table/relation, including inverse `[[1], [], [0,2]]`. Do not force this into a one-to-one atom map or infer sampling/evidence weights. |
| Effective chemistry | Explicit associated-state queries and state-sensitive selection; mixed/missing required associations refuse | Forward the admitted state/occurrence and preserve source/local distinctions. No reference-state fallback or inferred chemical identity. |
| Missing/partial/generated | Checked maps expose absent and generated members | Default to complete coverage/refusal. A separately admitted partial profile retains omissions and weaker guarantee. Generated atoms can join explicit current-group expansion without inheriting original atom identity/evidence/confidence. |
| Persistence | Owner H5MSM readback covers the admitted molecular axes/states/coordinates | BindingMT retains its own site/result/sidecar references and qualifies actual public projection/replay. No arbitrary sidecar persistence or BindingSite native domain is supplied automatically. |

This covers the finite P0m molecular-fact request. The first client implementation
can use existing public operations; no new molecular kernel, matcher, parser,
serializer, universal snapshot/observer or whole-suite adoption gate is needed.
The caller still declares asset association and a consistent check/use context.
Missing proof, observed contradiction, unknown/empty membership, incomplete
coverage and unsupported profiles keep their separate meanings. The owner offer
does not establish a current finding or stronger C2 placement guarantee.

## Client state and next admission

At this review the development source is still MolSysMT
`ff25f120243319ca9515009b4971e24a2eb0dc22`, with historical on-disk native
SHA-256 `2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`.
It differs from the owner's recorded source/native combination. A digest
difference alone is not a demonstrated incompatibility; do not claim owner-pair
qualification or require a rebuild merely from that difference.

Next inspect the participating worktrees through official MolSysSuite tooling,
advance the authorized clean development checkout with a fast-forward update,
retain its exact source/native identities and execute a small bounded receiving
of the offered operations. Do not rebuild/install/copy native files automatically.
Then implement and qualify the actual public C1 result against independent
entry/map/state/coverage expectations. No `resolve_region` stub is shipped by
this review, and P0m review completion is not C1/M2 or consumer adoption.

[BindingMT #116](archive/molecular_input_os_resource_error.md) separately corrects
native-input ENOMEM translation. Its 500-case-per-policy software receiving uses
the original source closure above; the broader 498-case molecular selection was
RSS-interrupted and is not automatically restarted for #746. Current/future
C1 receiving must have its own small profile and resource registration.

Exact public comment, contract/guard/report/receipt bytes and Git blob hashes
are retained as private source evidence under
`.molsyssuite/molecular-input-enomem-116-20261114/provider-offer/`. These are
read-only owner inputs, not regenerated scientific observations or shipped test
fixtures. Raw attempts and this review keep #50 custody, review 2026-11-21;
earlier evidence remains preserved with its existing review status.
