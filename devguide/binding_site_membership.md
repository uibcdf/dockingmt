# BindingSite source-index membership profile

Owner: BindingMT #111. Admission: 2026-11-13 before implementation.
Status: atom/group declarations source-received; finite C1 offer reviewed, client molecular receiving pending.

## Ordinary declaration and scope

The [first data core](binding_site_data_core.md) preserves coordinate-free residue
annotations and definitions. This increment adds `BindingSite.from_atoms` and
`from_groups`, receiving `atom_indices` and `group_indices` respectively, plus the
same explicit source/name/structure/state/extension options. No MolSys is queried
by these factories. The source owner/id/revision and its atom/group index space
are caller declarations, not proof of current molecular correspondence.

Accept an ordered list, tuple or one-dimensional NumPy integer array. Preserve
order, normalize genuine integer scalars to portable Python integers and reject
bools, floats, negative/duplicate values, selection strings, unordered sets and
multidimensional arrays. Empty is a declared empty population, not a successful
negative finding. A group index is not a residue ID or sequence position; group
membership does not perform an implicit atom expansion. Bounds require the
actual source and belong to C1.

The admitted view role is `declared_members`. The payload records element
`atom`/`group`, explicit `source_atom_index`/`source_group_index`, ordered source
indices and `resolution.state="declared"`. Inspection reports that declared
membership separately from unresolved residue annotations and missing membership.
Molecular resolution remains not performed, realization coverage not requested
and binding support unknown. Independent versus selected structure/state scope
and repeated occurrence references retain the existing meanings.

## Explicit experimental version admission

New atom/group declarations emit experimental BindingSite **0.2**. They admit one
explicit molecular-membership view. Existing residue/criterion factories still
emit **0.1** and actual original 0.1 files remain unchanged/readable. Never inject
0.2 membership into 0.1, silently migrate old files or claim old-reader support.
The actual previous reader must refuse 0.2. Both formats remain separate from
the unchanged package/source tag 0.1.0 and unfrozen proposed shared `@1`.

Evidence/definition derivations keep the original format/profile. They preserve
the exact original claim/observation associations, and new citations retain their
explicit interpretation authority. Copy/read keep identity; exclusive save and
optional-extension behavior reuse the admitted lifecycle. JSON object order
cannot determine source-index order or element identity.

Freeze actual prior 0.1 API outputs with original hashes, record/content IDs,
source checkpoint and producer metadata. New compatibility fixtures get exact
installed-test support declarations. No original fixture or producer is rewritten.

## C1 owner agreement before molecular resolution

The finite owner disposition is now [reviewed for C1](binding_site_molecular_contract_receiving.md), following
[MolSysMT #746](https://github.com/uibcdf/molsysmt/issues/746).
C1 needs its own public molecular facts/checks/preconditions. Existing #734 covers
the restricted contact/SASA profile; it does not by itself certify site resolution.
Inspection of public `select`, `get`, `extract`, `permute_atoms` and
`compose_atom_maps` supplies candidate operations, not new executed agreement.

The finite review concerns native MolSys source/index/state facts, explicit
group-to-atom expansion, original-to-target maps and structure 2 becoming local 0,
missing/contradictory correspondence and generated/omitted members. Map-range or
ID/count agreement is not common-origin authentication. No implicit reference-state
or multi-structure default, geometry calculation, new molecular matcher/serializer
or universal mutation receipt is commissioned.

First settle the actual callable/fact table and its caller preconditions; then
implement `resolve_region` with complete coverage by default and a separately
admitted explicit partial profile. Current-finding guarantees remain unsupported
unless their own prerequisites are received. Source declarations alone cannot
upgrade the requested guarantee. This declaration increment ships no resolution
stub or fake successful projection.

## Public example

```python
import bindingmt as bmt

site = bmt.BindingSite.from_atoms(
    source={"owner": "caller", "id": "source-A", "revision": "r1"},
    atom_indices=[5, 1, 3],
    structure_indices=[2, 0, 2],
)
groups = bmt.BindingSite.from_groups(
    source={"owner": "caller", "id": "source-A", "revision": "r1"},
    group_indices=[2, 0],
)
assert site.views[0]["payload"]["source_indices"] == [5, 1, 3]
assert groups.inspect()["membership"]["index_space"] == "source_group_index"
assert site.inspect()["molecular_resolution"] == "not_performed"
site.save("members.binding-site.json")
restored = bmt.BindingSite.read("members.binding-site.json", experimental=True)
assert restored.to_dict() == site.to_dict()
```

This constructs source declarations. It does not assert that atom 5 exists,
expand groups into atoms, choose a target-local frame or evaluate a binding site.
The NumPy-array route requires one dimension and integer dtype, including for an
empty array. Lists/tuples may contain genuine NumPy integer scalars; floats,
bools, object arrays and masked unknown indices do not become integers implicitly.

## Executed bounded source receiving — 2026-11-13

`tests/test_site_membership.py` supplies **64 passing controls**. The complete
site/index-membership/interface-data/core-helper/serialization/argument/bootstrap
selection reports **321 passes per policy**, normal and pm/fs. It covers ordered
atom/group declarations, empty populations, NumPy normalization/detachment,
invalid/duplicate/coercible indices, source-vs-local index space, explicit roles,
unchanged old observations through revisions, required-version refusals and
actual frozen old 0.1 reading/copy/JSON sorting. Source bounds are deliberately
not fabricated from labels or counts.

The five new frozen compatibility support files under
`tests/data/site_membership_compat/bb3dbfc/` have exact SHA-256 declarations in
`devtools/conda-build/resources.toml`. They retain three original API-emitted 0.1
records, their original producers/claim associations and the real production base
4e41913 separately from the subsequently qualified source bb3dbfc. No original
scientific fixture/helper or producer is regenerated or overwritten.

An actual public workflow emits seven new 0.2 records, copies the three original
0.1 records unchanged and writes ten separate sorted derivatives. A fresh
unyt/pm-fs reader restores all 20 with molecular queries/conversion/selection/
contacts/SASA and optional owners blocked. Ordered source axes, `[2,0,2]` source
references and `[0,1,2]` occurrences, old observation/claim references, empty versus
missing membership and unknown support survive. Files/caller policy remain
unchanged and originating uses stay zero. The actual bb3dbfc reader independently
refuses atom and group 0.2 outputs before molecular work; its temporary source
export is retired. These are data controls, not new molecular calculations or
consumer adoption.

Participating development sources remain MolSysMT ff25f120, PyUnitWizard cc51c8e,
ArgDigest 7be790b, SMonitor 4a4cd1e and DepDigest 5e93eaf, with legacy Python
3.14.10. Every final cell binds runtime/test/support-input/resource hashes,
provider heads/runtime bytes and native-file SHA-256 before/after. Historical
native-file SHA-256 remains
`2dbcf13d148cb3ae13a5908707fcdd61c75a2de5027e50c566ce07de81bdb038`,
with unauthenticated builder/source identity; this receiving qualifies no new
native molecular operation. Fetched upstream changes remain unmerged. Optional
provider work and the interrupted evaluator under #30 remain untouched.

Serial cells use CPU0/nice10/one worker, monitored 13-GiB available reserve,
512-MiB group RSS and bounded CPU/wall time. No prefix reinstall, native build,
held-suite restart, hosted CI, tag or installed/public/platform pass accompanies
this increment. Six applicable checks cover Ruff/format, indexes, documentation/
quantity/references, shared noarch resources and Conda contract on final workspace
and fresh committed source. Shared SDK source is
95f693be10c9205ab9b912cb53453710a207bf45. The authorized `[skip ci]` push supplies
no hosted evidence.

Raw attempts, exact source/provider/native/support-input snapshots, old-reader,
public workflows, owner request/readback and resource/export/publication receipts
retain #50 custody in `.molsyssuite/site-membership-111-20261113/`, review
2026-11-14. #111 stays open. Next receive the finite MolSysMT #746 disposition and
bind C1 to actual owner calls/facts/preconditions. Geometry and C2/T/H/P remain
separate profiles; missing owner acceptance does not block independent B1 work.
PeptideMT #60 still awaits the separate interface P package.

## Finite owner disposition reviewed — 2026-11-14

[The reviewed offer](binding_site_molecular_contract_receiving.md) supplies the
requested public group/map/occurrence/state facts and #750 bounds correction.
The provider request is resolved. Actual client source/native receiving and
public C1 implementation remain pending; the original 321-case declaration
population above is unchanged and is not molecular qualification.
