# Selection-domain construction provenance — 2026-10-28

Owner: [#55](https://github.com/uibcdf/dockingmt/issues/55), identified by the
[nonvisual Core audit](core_mvp_audit_2026-10-28.md) under #28/#4.
This closes the construction-record part of C4. Its visible observation and C6
remain deferred under #52; broader scientific/profile acceptance stays #4/#5/#33.
The qualified MolSysMT pin `e395e52646dab2ecb480d3d67aa7254be99b8524`, other
provider pins, geometry definitions and original scientific producers are unchanged.

## Public behavior and compatibility

`BoxRegion.from_selection` now records its executed construction recipe.
`box.derivation` returns an independent JSON-compatible copy. `to_dict` includes
that optional record; `from_dict` validates/restores it without rereading a source.
Explicit `BoxRegion`, `from_points`, `from_bounds` and legacy geometry-only
records have `derivation is None` and retain their previous serialized keys.
The enclosing box schema stays `1.0`; the nested schema is independently named
`dockingmt.box_derivation@1`.

```python
box = dockingmt.BoxRegion.from_selection(
    source, selection=[2, 3], structure_indices=1,
    padding=pyunitwizard.quantity(2, 'angstrom'))
recipe = box.derivation
saved = box.to_dict()
restored = dockingmt.BoxRegion.from_dict(saved)
```

The recipe retains provider form and source atom count, existing input-byte
fingerprint where available, requested selection and actual resolved atom indices,
requested structure axis, chosen position, chemical selection context and optional
provider-reported state association. Native/composed objects have an explicitly
absent file/literal fingerprint; no molecular identity hash or snapshot is invented.
Padding and the resulting full-precision physical box are stored in canonical nm.
`None` padding remains distinct from an explicitly supplied zero quantity.

`chemical_state` is a new optional forwarding argument, default `reference`,
preserving the previous selection context. MolSysMT owns its interpretation.
The existing multiple-frame behavior remains **first returned structure**:
`structure_indices=[1, 0]` is retained as requested, with `structure_position=0`.
No frame sorting, chemical-state inference or molecular-index resolver is added.

## Actual ownership and original redocking axes

Public `msm.select/get/has_attribute/get_form` resolve the molecular input, atom
axis, coordinates and available state association. Provider failures propagate.
The existing input-boundary byte-fingerprint helper is reused for file/literal
integrity; it does not parse molecular content. The box extent/padding remain
DockingMT's pre-existing search-domain policy over returned coordinates.

`DockingProblem.for_redocking` reuses its existing public native normalization and
selected-frame/state handling. It constructs the same geometric box from those
actual selected points, then records `method='redocking_partner_bounds'` with the
original source form/fingerprint, partner selection, original atom indices and
selected frame/state. It does not present a reindexed temporary selection as the
original source. File fingerprints and selected axes are checked across factory
construction before returning the problem.

Direct construction uses `method='selection_bounds'`. Optional state association
is recorded only from the provider; absent data stays absent. Direct legacy H5MSM
file selection does not acquire a consumer chemical-state workaround. The initial
54-pass/one-failure regression correctly exposed that `chemical_state='structure'`
requires native context for that route; the factory correction uses its already
existing native normalization. The unrelated optional original-index query gap is
reported in [MolSysMT #523](https://github.com/uibcdf/molsysmt/issues/523); the recipe
needs no local replacement for that getter.

## Binding, mutability and backend projection

The validated descriptor is detached from caller arrays, native objects and
returned records. Its canonical geometry must match the current box exactly.
Editing a derived box's coordinate buffer cannot silently preserve old attribution:
serialization and backend projection raise an actionable `ArgumentError`. Construct
a new selection-derived box for a new recipe, or a new explicit geometric box when
no derivation is claimed. File changes during construction also reject.

Validation covers schema/method, required fields, source/atom axes, typed frame/
state records, optional byte fingerprints, finite nonnegative padding and box
binding. This is declared construction history, not authentication of arbitrarily
forged source fields or recovery of an original molecular system. Later caller
source edits do not mutate the stored historical recipe or silently recompute its
box; native source-file identity remains explicitly unavailable when absent.

The existing `to_backend_box` numerical record is unchanged. The problem/result
`search_domain` carries the recipe alongside the operation's actual rounded
`backend_box`, units and engine context. Restoration preserves it. A fake-engine
boundary control verifies the exact submitted center/size and normalized result
without launching a new native search. Existing Vina/scoring contracts remain in
the wider selection; no registered human search or historical population is rerun.

## Checks and separate artifact evidence

[The new module](../../tests/test_domain_derivation.py) has **22 cases**, covering
nm/pm policies, original and repeated frame requests, native/file/literal sources,
redocking axes, absent padding, source immutability, independent records, malformed
bindings, caller geometry/file changes, provider refusals, legacy records and
problem/result/backend serialization. The current source selection passes **188
cases**, 66.07 s, 40 warnings, zero skips; it includes those controls. An earlier
186-case selection and the 22-case module have their own overlapping receipts.
[Source evidence](data/domain_derivation_2026-10-28/manifest.json) records code hashes
and diagnostics. Ordinary installed and exact-head hosted checks are separate
receipts on #55; previous wheels never qualify changed runtime code by relabelling.

Quota-interrupted receiver/test attempts are retained privately as unsuccessful
attempts. Recovery removes one verified unused ignored task compilation cache and
owned pytest fallback files, preserves exact provider wheel/native hashes, and
normally reinstalls the same provider wheel in the task's own receiver. Source
checks are repeated after recovery. No sibling source, shared environment, original
scientific evidence or qualification artifact is edited or disposed.

Task resources `/tmp/dockingmt-domain-provenance-20261028` remain owned by #55/#50,
review **2026-11-04**, no automatic deletion. No public package or GitHub Release
is published. The earlier audit's pending hosted verification is separately closed
by [its terminal recovery](https://github.com/uibcdf/dockingmt/issues/28#issuecomment-6485389513);
that older run does not qualify this new implementation.
