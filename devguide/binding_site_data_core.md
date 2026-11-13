# First BindingSite declaration and persistence profile

Owner: BindingMT #111. Admission: 2026-11-13, before implementation.
Status: first coordinate-free B1/B2 source profile implemented; broader #111 work pending.

## Selected local decisions

Start with coordinate-free source-addressed residue annotations and unevaluated
definitions. The [reviewed plan](binding_site_implementation_plan.md) explicitly
permits one complete declaration/persistence slice before the other factories.
Atom/group membership, geometry, molecular resolution, domain placement and
TopoMT/PharmacophoreMT/PeptideMT receiving keep their own gates. No MolSys is
queried, copied or serialized by this first profile.

- `BindingSite.from_residues(source=..., address_space="author_residue",
  residues=..., name=None, role="annotated_members", structure_indices=None,
  chemical_state_indices=None, extensions=None)` declares addresses, not molecular
  atom/group indices. Source requires a nonempty owner/id; revision may be unknown.
  Entries have chain/id and optional insertion code. Preserve string residue IDs,
  explicit empty chains/codes and unknown `None` distinctly. Do not parse integers
  or infer a sequence. Ordered entries must be unique. Empty is a declared empty
  annotation, not a completed negative calculation.
- `BindingSite.from_definition(source=..., claim=..., criterion=..., name=None,
  structure_indices=None, chemical_state_indices=None, extensions=None)` records
  a hypothesis/criterion without manufacturing an empty membership view. The
  criterion is finite declared data with a named kind; it is not executed.
- Structure-independent definition, view and evidence scope is distinct from
  explicitly selected source structures. Preserve `[2,0,2]` and occurrence
  positions `[0,1,2]`; optional state indices align one-to-one and may be unknown.
  These are caller declarations, not verified MolSys positions or evaluated
  realizations. Evidence has its own structure/state scope; no ensemble result,
  independent repetition, prevalence or thermodynamic weight is inferred.
- Public `definition`, `views`, `context`, `evidence` and `inspect()` return
  detached information. Manual support remains unknown. `inspect()` reports
  not-supplied, declared-empty and unresolved membership separately, with no
  implicit molecular applicability or optional asset lookup.
- `with_definition(claim=..., criterion=..., reason=..., evidence_refs=())`
  creates a new immutable declaration. Existing evidence keeps its original
  exact claim reference; a new definition cites none by default. Explicit
  `evidence_refs` is a new interpretation, not another observation or support
  upgrade. This initial operation retains source/view/structural scope.
- `with_evidence(key=..., source=..., observation=..., attribution=...,
  structure_indices=None, chemical_state_indices=None)` adds one attributed
  source annotation and cites it explicitly. Its original claim reference names
  the exact preceding record/definition, avoiding a self-referential digest.
  Revisions preserve that reference and the observation unchanged. No generic
  confidence/evidence aggregation or owner finding adapter is implemented.

## Identity and experimental wire decision

Use explicit `format="bindingmt.binding_site"`, `format_version="0.1"` and
`experimental=true`, separate from the existing package/source tag 0.1.0.
The proposed `@1` remains unfrozen. Typed `from_dict` / `read` require
`experimental=True`; factory calls produce this documented experimental profile.
Choose `read` consistently with the existing interface/footprint lifecycle; no
unimplemented load/resolve/application aliases are exported.

`record_id` identifies one immutable declaration; `site_id` exposes the same
declaration identity in this first profile. It is not a persistent physical-site
tracking ID. Copy/read preserve identity. Definition/evidence additions allocate
new identities and record an immediate parent content reference, reason and
derivation kind. `definition_ref` is the exact record ID/content SHA-256/definition
key, rather than the latest declaration with a label. Digests address finite JSON
content; they do not authenticate chemistry, source ownership or site equivalence.

The closed envelope validates source, ordered views, definition/evidence scopes,
original claim references, parent, producer, experimental version and digest.
Unknown required core fields/representations refuse. Namespaced extensions are
explicitly optional (`required: false`, opaque finite `payload`); required
unknown extension semantics refuse. No callable, object deserialization or asset
resolution is permitted. No physical quantity is admitted by this coordinate-free
profile; later geometry must use the shared PyUnitWizard sealed quantity contract.

Reuse the existing local record lifecycle: exclusive save, detached finite JSON,
duplicate-key refusal and identity-preserving copy/read. ArgDigest owns public
argument dispatch and SMonitor owns diagnostics. Unsupported address/role or
required capabilities and malformed records remain distinguishable. No native
molecular, contact or surface implementation is duplicated.

## Required receiving and remaining work

Exercise real public construction/save/read/revision, ordered/empty/unknown
addresses, independent versus selected/repeated structure scope, evidence scope,
old-claim association after revision, explicit new citation, detached ownership,
finite/required/version/digest refusals, optional extensions and safe existing-file
lifecycle. Run the complete selected declaration controls under normal and pm/fs
policies, and cold read under unyt/pm-fs with molecular/optional owner work blocked.
Keep current caller unit policy and original producer/evidence identity.

Resource checking and CPU-one/nice10/one-worker supervision apply. The previous
additional evaluator interruption stays under #30; this data-only profile does
not restart that work. Source-only receiving is separate from installed/public/
hosted/platform and consumer adoption. #111 stays open for remaining B1 factories,
C1/C2 and the admitted T/H/P workflows. PeptideMT #60 is still awaiting the
separate interface P inputs; it is not evidence of this site's consumer adoption.

## Ordinary public workflow

```python
import bindingmt as bmt

site = bmt.BindingSite.from_residues(
    source={"owner": "caller", "id": "target-A", "revision": "r1"},
    address_space="author_residue",
    residues=[{"chain": "A", "id": "012", "insertion_code": ""}],
    structure_indices=[2, 0, 2],
)
annotated = site.with_evidence(
    key="annotation-7",
    source={"owner": "curator", "id": "annotation-7", "revision": "v1"},
    observation={"reported_members": "membership"},
    attribution={"producer": "original-curator", "version": "1"},
    structure_indices=[0],
)
revised = annotated.with_definition(
    claim="Retain as an annotation-only hypothesis",
    criterion=annotated.definition["criterion"],
    reason="Explicit interpretation change",
)
assert revised.evidence == annotated.evidence
assert revised.definition["evidence_refs"] == []
assert annotated.evidence[0]["original_claim_ref"] == site.definition_ref
revised.save("site.binding-site.json")
restored = bmt.BindingSite.read("site.binding-site.json", experimental=True)
assert restored.to_dict() == revised.to_dict()
```

This is an unresolved annotation workflow, not molecular selection or a binding
prediction. Residue `"012"` remains that source address. Unknown chain/insertion
information (`None`) is distinct from explicitly empty strings. The first API
normalizes omitted source revision/insertion availability to explicit `None`;
these canonical fields are required on typed wire read, without silent migration.
A revised claim can explicitly cite prior keys through `evidence_refs`; those
observations keep their old original-claim references and gain no new support.
Additional criterion/observation data are finite declarations, not executed
physical fields, owner methods or newly admitted geometry.

## Executed bounded source receiving — 2026-11-13

The new module provides **59 passing controls**. Complete site, interface data,
core-helper, serialization, argument and unit-bootstrap modules report
**257 passes per policy**, normal and pm/fs. They exercise actual public emission,
old-observation association through successive revisions, explicit new citations,
unknown/empty/source-address distinctions, selected/repeated structure/state
references, contradictory states, detached ownership, opt-in/version/digest/
required-semantics refusals, optional extensions, JSON object normalization and
exclusive file lifecycle. Physical molecular facts are not authenticated by
those declared source/structure indices.

A separate public workflow emits six original records and their sorted JSON
derivatives: initial annotation, attributed annotation, revised claim, explicit
new citation, empty annotation and criterion-only declaration. A fresh unyt/pm-fs
reader recovers all 12 with molecular queries/selection/conversion/contact/SASA
and optional tools unavailable. The old claim reference, unchanged observations,
occurrences `[2,0,2]`/`[0,1,2]`, separate evidence scope and unknown support survive.
Files, caller unit policy and producer data stay unchanged, with zero new
originating uses. All emitted records are new authored software controls; the
review specimens and original scientific fixtures/producers are untouched.

Participating development sources: MolSysMT ff25f120, PyUnitWizard cc51c8e,
ArgDigest 7be790b, SMonitor 4a4cd1e and DepDigest 5e93eaf; Python 3.14.10 through
the unchanged legacy development interpreter. Each final cell binds runtime/test
hashes, provider heads/runtime bytes and native-file bytes before/after. The
historical MolSysMT native file SHA-256 remains
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`;
its builder/source identity is unauthenticated. This profile qualifies no new
molecular/native calculation or provider API. Fetched upstream advances stay
unmerged; concurrent optional-provider work is not used or overwritten.

Cells run serially on CPU0/nice10 with one native worker, a monitored 13-GiB
available reserve and 512-MiB group RSS cap. Source-only development qualification
is not installed/public/platform, shared schema agreement or consumer adoption.
No prefix install, native build, held-suite restart, hosted CI or tag accompanies
this increment. The unrelated prior evaluator interruption remains under #30.

Exact attempts, public input snapshots, source/provider/native/resource receipts,
emitted records, cold reader and workspace/fresh committed-source checks retain
#50 custody under `.molsyssuite/site-data-core-111-20261113/`, review 2026-11-14.
Applicable gates are Ruff/format, indexes, documentation/quantity/reference checks,
shared noarch resources and Conda release contract. The shared SDK source remains
95f693be10c9205ab9b912cb53453710a207bf45; skipped remote CI supplies no hosted pass.

## Next owner step

This completes the first admitted B1/B2 profile, not all of B1/B2 or milestone M1.
Next admit coordinate-free atom/group membership and settle C1's concrete public
MolSysMT selection/map/structure/state checks and caller preconditions. Reuse the
restricted public facts already received under #734 where applicable; no universal
receipt or observer is a new prerequisite. Molecular resolution/application,
physical geometry and T/H/P adapters keep their own implemented/received/adopted
gates. #111 stays open, and #112/PeptideMT #60 retain their independent work.


## Subsequent source-index profile — 2026-11-13

[Atom/group declarations](binding_site_membership.md) now have their own admitted
experimental 0.2 views. This article's original residue/criterion 0.1 factories,
producer identities, 257-case population and cold-read outputs retain their exact
original scope. Actual old 0.1 files are frozen unchanged for compatibility; the
new receiving independently reports 321 cases per policy. C1's concrete owner
review is requested in MolSysMT #746, with no molecular projection claimed yet.
