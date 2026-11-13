# BindingInterface: first declaration and persistence profile

Owner: [BindingMT #112](https://github.com/uibcdf/bindingmt/issues/112).
Delivered source profile: **P0a/D1/D2, experimental data-only 0.1**, 2026-11-12.
This is the implementation admission for the first slice of
[work-plan revision 4](binding_interface_implementation_plan.md). The scientific
information model remains revision 2; later numerical/owner profiles retain their
own admission. The experimental record version is not the package/tag version.

The subsequent [native contact profile](binding_interface_contacts.md) adds the
separate calculation entry point, experimental 0.2 result and independent
footprints. The original data-only 0.1 contract/evidence below remains preserved.

## Public workflow

```python
import bindingmt as bmt

interface = bmt.characterize_interface(
    question={'kind': 'association'},
    participants={'A': {'source_id': 'source-a'}, 'B': {'source_id': 'source-b'}},
    grouping=(('A',), ('B',)),
)
print(interface.summary())
interface.save('interface.json')  # exclusive creation
restored = bmt.BindingInterface.read('interface.json', experimental=True)
assert restored.record_id == interface.record_id
```

This declares a question with no supplied analysis, unknown support and no
molecular correspondence check. Core installation dependencies remain required.
Molecular selections, coordinates, provider objects and numerical calculation
are outside this profile. Use exact declared references, not live MolSys handles.

A caller can preserve analysis-level evidence separately from individual finding
references. Construction validates declarations; it verifies no originating owner.

```python
interface = bmt.characterize_interface(
    question={'kind': 'association'},
    participants={'A': {'source_id': 'source-a'}, 'B': {'source_id': 'source-b'}},
    grouping=(('A',), ('B',)),
    analyses={'declared': {
        'owner': 'example.owner',
        'reference': {'run_id': 'run-1', 'analysis_id': 'analysis-1'},
        'outcome': 'completed',
        'finding_refs': [],
    }},
)
assert interface.summary()['analyses']['declared']['finding_count'] == 0
```

## P0a decisions closed for this slice

| Boundary | Admitted contract |
| --- | --- |
| Entry/result | Root exports `characterize_interface` and immutable `BindingInterface`; implementation in `bindingmt/core/interface.py`. |
| Question | Required mapping with `kind='association'`, optional nonempty `description`; unknown core fields refuse. |
| Participants/grouping | At least two named nonempty reference mappings; at least two ordered nonempty groups using each local name exactly once. Public grouping accepts lists/tuples; records use lists. Membership/chemistry is not resolved. |
| Contexts/site references | Optional named nonempty context mappings and list of exact nonempty site-reference mappings. These are caller declarations, without molecular authentication or required BindingSite runtime. |
| Claim | `claim_status='declared'` by default; explicit `inferred` describes the caller's claim and earns no scientific support. |
| Analyses | Optional mapping, default no analyses. Required owner/reference/outcome/finding_refs; authority is always `caller_declared`. Typed owner recovery/verification is deferred to its adapter. |
| Assurance | Only `preserved_evidence`. Default context policy is `None`; explicit `require_match` remains visible but not applicable. Molecular correspondence is `not_required`, current assessment `not_performed`, asset access `not_checked`. Stronger assurances refuse. |
| Identity | Fresh declaration/revision gets a UUID identity. Copy/read retain it. Each analysis retains its original question/participants/grouping/contexts, including after reinterpretation. |
| Format | Required `format='bindingmt.binding_interface'`, `format_version='0.1'`, `experimental=True`, explicit receiver opt-in and exact known core fields. No missing-version/legacy admission. |
| Integrity | SHA-256 of canonical finite JSON excluding `content_sha256`; checked on admission and refreshed by revision. Identifies declared content, not authenticity, molecular identity or independence. |
| Unknown data | Optional namespaced `extensions` preserve finite JSON without interpretation/import. Unknown core/required semantics refuse. No known physical observable field is admitted yet; future lengths/areas require the shared sealed-quantity contract and field/dimension handshake. |
| Revision | `revise(question=..., reason=...)` changes the interpretation only; one immediate parent ID/reason, no embedded ancestry. Existing analysis claims stay unchanged. Changed grouping/remapping/numerical results require later profiles. |

## Analysis outcomes and original associations

`outcome` is `unknown`, `completed` or `failed`. Completed evidence requires an
explicit `finding_refs` list, including `[]` for completed zero. Unknown/failed
require `finding_refs=None`; failure additionally requires a nonempty `failure.stage`.
No supplied analysis is a separate summary state. Positive/empty/failure labels
remain caller-declared even after a successful round trip.

Optional `criterion`, `coverage`, `context_refs`, `asset_refs`, `historical_checks`,
`failure` and namespaced `extensions` retain original evidence. `context_refs`
name contexts in that analysis's `original_claim`, not a future interpretation.
Historical matches retain their scope and never become an active match on read.
The API supplies `original_claim` at declaration when absent; incoming saved
records require it explicitly. Foreign reference payloads retain their original
vocabulary under caller authority and are not decoded by a generic registry.

## Ownership, persistence and refusal

`question`, `participants`, `grouping`, `analyses`, `summary()` and `to_dict()`
return detached snapshots. The result stores immutable JSON; `copy()` is faithful.
`from_dict(record, experimental=True)` validates the exact core/digest and detaches.
`save(path)` exclusively creates UTF-8 JSON and never overwrites an existing file.
A failed owned write removes the new path only while its inode is still ours;
cleanup failure preserves the original error. Crash durability is not promised.
`read(path, experimental=True)` reads only the specified JSON, rejects duplicate
object keys, and performs no external-asset lookup, dynamic owner import, molecular
operation or restoration of application unit settings. Native filesystem/resource
exceptions propagate; they are not analysis outcomes. Invalid JSON propagates its
JSON parsing error; invalid known declarations use catalog `ArgumentError`.

The existing finite-JSON helper moved unchanged from `evaluation.py` to private
`serialization.json_copy`; evaluation retains its `_json_copy` import identity
for existing consumers. ArgDigest owns argument admission and SMonitor the local
structured diagnostics; no competing validator/unit/provenance framework is added.

## Executed evidence and limits

Task custody: `.molsyssuite/interface-data-core-112-20261112/`, #50 review
2026-11-14. Source guards: [test_binding_interface.py](../tests/test_binding_interface.py),
plus existing result-record/outcome admission controls. The final selection has
**158 passing cases per policy**, normal and pm/fs, with no skips or warnings.
This includes **50 new interface cases** and **three fresh-process unit-bootstrap cases**. Six actual public records are emitted
(no analysis, unknown, completed zero, nonempty, failed and revised), then read in
a fresh process under pm/fs with molecular operations forbidden, optional owners
absent and application policy preserved. Check resources/receipts retain actual
attempts separately from final qualification. Final Ruff/format/index/proposal/
resource/Conda checks also run on the workspace and fresh committed source.

Broader exploratory selections remain failed, not relabelled as this passing
selection. Four pre-existing backend cases initially lacked `unyt`; after the maintainer
installed it, the complete core-helper selection passes in both policies.
Two existing summary controls fail: frozen producer vocabulary and exact pm/fs
floating equality; [#113](pending_bugs/redocking_summary_receiving_controls.md)
records reproduction on unchanged `630f6d6`, original inputs and separate ownership.
Final failure controls also exercise write, flush/allocation and close errors,
preserving the exact original exception and protecting existing files. The first
46-case pass retained 36 constructor-repr diagnostic warnings; disabling
the generated dataclass repr fixed the uninitialized-object observation. A private
pm/fs harness also initially compared dynamic loaded-library inventories as policy;
the corrected harness compares actual policy fields. All attempts remain retained.

The inspected MolSysMT `_pyunitwizard.py` at `ff25f120` and MolSysViewer at
`0dcdd6ce` declare the same guarded suite standards as BindingMT. The received
PyUnitWizard guide (SHA-256
`2bebdab26b9f5ac70bafd35bc48522e1a07535953e2a1b8939e0a3feb6d5b860`)
and MolSysMT additionally guard cache setup when Pint is already loaded; BindingMT
now follows that pattern. Fresh-process controls cover existing Pint without
standards and application-selected Pint/unyt pm/fs, with explicit conversions
and preserved policy. Future physical fields will use `ensure_quantity` and
`QuantityRecord` with receiver field/dimension checks, as in MolSysMT's storage;
this first data profile introduces no competing unit codec.

The independent unyt ndarray fast-track witness is handed to
[PyUnitWizard #155](https://github.com/uibcdf/pyunitwizard/issues/155): a requested
nm fast track leaves `1000 pm` unchanged, whereas public explicit conversion
returns `1 nm`. BindingMT adds no converter workaround and the first data profile
uses no fast-track quantity calculation. Defer that optimization's unyt receiving
to the owner correction. Fresh bootstrap tests exercise explicit provider conversions
with an eight-binary64-epsilon relative bound, not exact floating equality; the
original broader fast-track/roundoff test attempts remain retained.

Read-only legacy Python 3.14.10 imports and `pip check` pass for these bounded
offline controls. New-environment migration/#82 pause remains separate; no prefix
installation/rebuild or whole scientific selection resumes. Cells use one CPU,
nice 10, native/build workers one, 13 GiB available reserve, 512 MiB owned-group
RSS cap and continuous monitoring. This is source software evidence, without a
new installed package, hosted CI, provider/native scientific or platform claim.

## Next increment

The contact portion of N0/C and the first N1 source route are now delivered under
the contact-profile contract. Next close N2 surface acceptance independently. T0/T1 and H/P inputs/receiving remain
pending under their recorded owners. #111 stays independent. No tag/release or
closure of #112 is implied by this first source delivery.
