# Molecular preparation requires supplied partial charges

## Compatibility change — 2026-10-10

[DockingMT #5](https://github.com/uibcdf/dockingmt/issues/5) and
[#49](https://github.com/uibcdf/dockingmt/issues/49) own removal of fabricated
zero charges from molecular preparation. Both `prepare_ligand` and
`prepare_receptor` now require complete finite atomic partial charges after
requested provider stages. Missing values raise an actionable `ArgumentError`.
There is no default model or zero substitution. Molecular charge assignment
remains the public MolSysMT operation delivered under
[#221](https://github.com/uibcdf/molsysmt/issues/221).

Both preparators accept `charge_options` with an explicit `method` and its
required parameters. The ligand retains optional fixed-state H addition before
charge assignment; the receptor performs no H addition or repair. Requested
charge assignment precedes requested named typing. Options and input systems
remain detached, and provider failures propagate without fallback.

```python
prepared = dmt.prepare_receptor(
    receptor_with_declared_chemistry_and_indexed_hydrogens,
    selection='all',
    charge_options={'method': chosen_method, **chosen_charge_parameters},
    typing_options={'typing_scheme': 'autodock4', 'method': chosen_typing_method},
)
```

Alternatively, explicitly call `msm.build.assign_partial_charges` and
`msm.build.assign_autodock_atom_types` before preparation. Automatic
`dock(problem)` requires preassigned systems; the execution protocol chooses no
molecular model. `allow_provisional_preparation=True` cannot bypass absent
charges, including when valid named types are already present. Missing types
retain their separate actionable error when both requirements are absent.

## Supplied values and attribution

The policy requires values, not a nonzero sum or a compulsory new named charge
calculation. Explicit supplied zeros remain valid. Complete legacy supplied
numeric charges without a named calculation report remain **unassessed** and
unattributed; DockingMT does not invent a report. Numeric native values are in
elementary charge; quantity inputs use explicit conversion to that unit.

Valid named assignments keep method, parameters, versions, references and
source correspondence. A calculation requested after selected-input extraction
has assigned status; a manual calculation before extraction may have projected
status. Preserve those different valid histories rather than normalizing them
to make records equal. Existing source-binding and finite-value checks remain.

Hydrogen transfer, total-charge conservation, existing maps, exact prepared values
and PDBQT rounding retain their existing contracts. They remain temporary consumer
routes pending the provider-owned transform in
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223); this change adds no
charge model, molecular projection or replacement serializer. An unassessed
assessment does not establish chemical or scoring validity.

Historical manually constructed or deserialized preparations may still declare
`zero_placeholder` or heuristic types. Their assessment and Vina opt-in guards
remain readable and executable. Current preparation never creates new placeholder
objects. External PDBQT remains unassessed. Do not rewrite original scientific
receipts, producers or archived bytes to fit the new policy.

## Executed controls and qualification

[test_required_partial_charges.py](../../tests/test_required_partial_charges.py)
covers both roles: missing-charge rejection without unrequested molecular work,
input immutability, actionable errors, automatic Vina before engine construction
with provisional opt-in on/off, supplied zeros under pm/coulomb policy,
explicit charge-then-type delegation and mapping, provider failure propagation,
nonfinite provider values and invalid receptor options before conversion.

Typing-only fixtures declare their synthetic charge inputs explicitly. Flexible
ligand and original torsion-reference controls request the named Gasteiger method
through MolSysMT. Template workflows explicitly request charges after template/H
work. Original source/reference hashes, cuts, fragments, atom correspondence and
scientific archives remain fixed. None of these fixture choices is a default
charge model or scientific acceptance for other inputs.

The grouped-receptor fixture now assigns charges on `MolSysBuilder.build()`'s
output, as that builder explicitly excludes MolecularMechanics. This respects
its contract instead of copying molecular domains downstream. The non-default
template fixture explicitly declares coulomb as it now performs charge work.
[MolSysMT #381](https://github.com/uibcdf/molsysmt/issues/381) records the narrower
observed limitation when native charge assignment runs under a policy containing
only pm/fs: its internal standardized quantity raises `NoStandardsError`.
The native fixed-unit contract versus this policy prerequisite needs provider
clarification; DockingMT neither overrides caller policy nor catches the error.

Use the unchanged CI provider source
`739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac`, retained native binary and qualified
ArgDigest/Viewer sources on Python 3.14 for local checks. No dependency, metadata,
shared environment or sibling implementation is changed. Local source composition
and normal installed/complete-source hosted checkpoints are distinct evidence.
The final affected local selection passes **169 tests without skips in
124.28 s**, with 74 retained provider warnings, including the 19 new required-charge
controls. Distribution/reporting checks pass **24 tests in 2.97 s**. Ruff lint
and format (154 files), generated indexes, current synchronized-guide checks,
changed-document local links, original scientific digests and diff checks pass.
Earlier failing fixture probes are diagnostic only: the final controls preserve
assigned/projected report histories and exercise nonfinite getter values without
bypassing public native setters.

A complete source run is in progress at the publication checkpoint. Normal
unskipped exact-head CI must execute all four required Python minors, ordinary
installation, isolated installed-package checks and complete source suites;
terminal results will be linked on #5/#49. These local results alone do not qualify
that matrix or public/scientific admission. Keep both issues partial: general
projection/export and chemical/scoring acceptance remain separate work.
