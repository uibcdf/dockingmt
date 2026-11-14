# BindingSite finite molecular contract receiving

Owner: [BindingMT #111](https://github.com/uibcdf/bindingmt/issues/111).
Review/receiving: 2026-11-14. Status: finite owner facts received in the client
development process; public `resolve_region` and C1/M2 remain pending.

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

## Review starting point

At the initial read-only review the development source was MolSysMT
`ff25f120243319ca9515009b4971e24a2eb0dc22`, with historical on-disk native
SHA-256 `2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`.
It differs from the owner's recorded source/native combination. A digest
difference alone is not a demonstrated incompatibility; do not claim owner-pair
qualification or require a rebuild merely from that difference.

The planned next step was a bounded official worktree inspection, an authorized
clean fast-forward source update and a small receiving of the offered operations.
The executed result below supersedes that next action. No native rebuild/install
was inferred from the digest difference. Provider review alone did not deliver
`resolve_region` or establish public/client application adoption.

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

## Actual client receiving after fast-forward — 2026-11-14

Official six-member status inspection preserved every sibling worktree and
fetched advance. The authorized clean MolSysMT `main` was fast-forwarded from
ff25f120 to **27ba3d4c8d63a6a40a2d77f0190309ff15f4deef**, exactly the reviewed
owner source. Its worktree stays clean, and pyproject/root/test instructions are
unchanged across the source update; the synchronized common guide is received
through the published owner changes. Other runtime providers stay at the prior
recorded source commits. The native file remains unchanged at SHA-256
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`.
No source build, installation, native replacement or environment repair occurred.
A separate fresh-process origin probe verifies that the actual imported extension
and mapped shared object are that exact checkout file/hash. This binds runtime
origin, not builder/source authenticity or the whole native ABI.

Two complete owner-authored modules pass in the actual BindingMT development
process, with package import origins and before/after source/native bytes checked:

- **18 membership/map/state cases**, including explicit entry order, group
  expansion, source-sorted extraction, nonidentity atom directions, group
  relationships, `[2,0,2]` occurrence/state tables, H5MSM readback under nm/ps and
  pm/fs, unknown/empty/missing/contradictory/generated-member controls. Exact
  published guard Git blob: `991f943b2f17d0cfab2dc53cc4ba542117ad636b`.
- **18 #750 selection-bounds cases**, covering native and H5MSM inputs, negative/
  out-of-range structures, numeric/all/expression selection and valid repeated
  structure scope with preserved numeric atom order. Exact published guard Git
  blob: `58e2018284a7139472e8904f0112a1b4b67bcb6d`.

These exact copied assertions run without editing the provider or its tests.
The owner modules are distinct bounded controls, not two independent full suites
or proof of BindingMT's unimplemented projection. Their success with the existing
native file establishes only the operations exercised; it does not authenticate
its build/source origin or certify every native ABI/package/platform combination.
The differing reference native digest therefore did not require a new binary for
this measured profile.

The same **500 complete BindingMT software controls pass per policy**, normal
and pm/fs, after the provider update: 463 resource/helper/serialization/offline-
domain plus 37 argument/bootstrap cases. This is a new receiving population on
the updated source, not a rewrite or sum of #116's original-source evidence.
The old 498-case native-problem interruption and earlier evaluator hold are
preserved, neither retried nor replaced by these small profiles.

All cells are serial, CPU 0/nice 10/one native worker, with a monitored 13 GiB
available reserve, 512 MiB group RSS stop threshold, 2 GiB address space and
45 CPU/120 wall seconds. The new profile's observed group peak is below 301 MiB;
all owned groups terminate without a resource interruption. Temporary H5MSM
outputs are small authored transport controls, retained under task custody.
Original scientific fixtures/producers and earlier native artifacts are intact.
No original optional engine, new model, GPU, docking/search or scientific campaign
is run. The source tag 0.1.0 and package publication state are unchanged.

Private receipts live in `.molsyssuite/site-molecular-owner-746-20261114/`:
preflight, official status/disposition, before/after source pull and native hashes,
exact copied guards, actual import origins, per-cell source snapshots/XML/resource
outcomes and final documentation/committed-export/publication readback. The six
applicable documentation/resource checks run after final edits in the workspace
and fresh committed export; the export is retired. #50 reviews this task on
2026-11-21. No original held selection is automatically restarted.

## Next implementation boundary

The finite P0m dependency is ready for the admitted operations. Implement the
real public C1 native atom/group region projection and its detached versioned
result through the existing owner operations. Retain the original source as the
caller's explicit asset association and consistent-input precondition; a separate
derived target needs checked atom maps and explicit structure-occurrence/group
correspondence, never an inferred identity map. Group expansion policy, effective
state and source/local indices must remain explicit. Default complete coverage
refuses missing members; an admitted partial result preserves omissions and its
weaker guarantee. No generated member inherits original evidence/confidence.

Qualify the actual BindingMT callable, independent expected outputs and saved
projection before claiming C1. Current-finding/placement guarantees, public C2/M2,
foreign conversions, broader source/native/installed/platform/final-pair receiving,
shared agreements and actual consumer adoption retain their separate gates.
No public `resolve_region` stub or local molecular algorithm is added by this
receiving increment.
