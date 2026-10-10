# Native prepared PDBQT export: adoption boundary

## Decision — 2026-10-10

The public MolSysMT serializer can write explicit prepared charges, AutoDock
labels, coordinates and a declared ROOT/BRANCH tree. This checkpoint qualifies
that supported route independently of the molecular transform still requested in
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223). It does not replace
the production writers or add a consumer projection, molecular snapshot builder,
tree remapper or fallback. [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49)
remains partial; [#5](https://github.com/uibcdf/dockingmt/issues/5) retains charge
policy and scientific preparation acceptance.

The complete migration needs a provider-produced molecular projection whose
native values agree with its result map. The current retained `source_molsys`
is an extraction of the original selected system. Its charges exclude the
charges of omitted H. Serializing that object directly would therefore lose
the transferred values while producing valid-looking PDBQT. Replacing the
writer by a call on the original full source instead retains every H. Neither
route implements the present prepared representation.

## Executed consumer controls

[test_native_prepared_export_contract.py](../../tests/test_native_prepared_export_contract.py)
contains five controls against the actual public writer and Vina 1.2.7:

- Named Gasteiger methanol, for both preparation roles and angstrom/pm inputs:
  six explicit source atoms versus three retained atoms (C, OA, HD), source
  charges and reports unchanged, charge recipients and prepared values checked
  independently. The native full-source writer retains all three nonpolar H.
- The prepared methanol charges are approximately `0.19000057917`,
  `-0.39963024356`, `0.20962966439` e. Supplying those explicit values to a
  detached native copy writes `0.190`, `-0.400`, `0.210` e. Actual fixed columns
  retain atom IDs, types and positions within 0.000501 angstrom, including under
  a pm/coulomb application policy. Real Vina ligand/receptor admission succeeds.
- A known six-carbon flexible axis writes prepared order `[2,3,4,5,1,0]`,
  serials 1–6, `BRANCH 1 5`, matching `ENDBRANCH`, and `TORSDOF 1` through the
  provider's explicit tree schema. This is a declared fixture, not an algorithm
  discovering correspondence or permuting a molecular object.

Public `msm.set(..., partial_charge=...)` correctly clears the native charge
calculation assignment. The resulting payload must not claim a new Gasteiger
calculation. Production adoption must retain the original calculation report
and describe its derived transform separately, as existing DockingMT remarks
already do. A serializer's projected typing report alone does not describe
hydrogen charge aggregation.

The RDKit source has no groups. Native output preserves blank group/chain fields
and still parses in Vina. DockingMT's prepared object declares `LIG/1`; adopting
the writer must explicitly carry those presentation fields or document a
compatibility change. This is a consumer representation decision, not a native
writer defect. Whitespace, charge field padding, END and native remarks also
differ from historical consumer bytes. Parsing and numerical agreement do not
authorize rewriting original scientific producer files or archives.

## Evidence and limits

The five final controls pass without skips in **8.20 s** on Python 3.14.7, using
the unchanged CI-pinned MolSysMT source
`739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac`, the retained native binary, qualified
ArgDigest/Viewer source composition and Vina 1.2.7. Initial fixture diagnostics
were corrected for MolSysMT's plain native charge arrays and object dtype; those
failed attempts are not qualifying evidence. No provider defect follows from
those test errors.

The surrounding native format, named charge/type, flexible-ligand and reporting
selection passes **119 tests without skips in 93.77 s**, with 47 retained provider
warnings. The subsequent five-case run also executes the added explicit total
charge and donor/recipient assertions; 119 distinct contracts are covered.
Ruff lint/format, generated report indexes, current component-guide/contributor
routes, changed-document local links, unchanged synchronized-guide snapshots,
original scientific digests and diff checks pass. The normal unskipped hosted
checkpoint will supply exact published-head installation and complete source
suite evidence on the owning issues; these local results do not replace it.

Read-only inspection of upstream MolSysMT
`889b3b4fe0ddac4a24105b49a58d3321e8708045` still finds the writer's explicit
no-merging/no-aggregation contract and the pending #223 proposal. That newer
source is not runtime-qualified here. Shared checkouts remain unchanged; their
behind states and the separate untracked 5X72 scientific work are preserved.

This is serialization/adoption evidence, not chemical validity, new scores,
search success, public dependency closure or installed-artifact admission.
Source-free reconstruction, arbitrary permutation and mechanical persistence
remain owned by MolSysMT #226/#369/#256. The existing retained-graph exception
remains #348. No sibling implementation is added in DockingMT.

## Provider handoff and next adoption

The executed evidence is handed to
[MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223) and
[#214](https://github.com/uibcdf/molsysmt/issues/214), linked from DockingMT #49.
The provider owns implementation and priority. Request the existing proposal's
native projected system plus retained/omitted/merged source maps and recipients,
pre-rounding conserved charges, valid named type binding, original versus derived
attribution, unchanged source and an explicit output axis. Keep declared docking
cuts, ROOT orientation and presentation compatibility in DockingMT.

After that operation is delivered, qualify its actual result through the native
serializer for rigid receptors, rigid and nested flexible ligands, four-character
names, missing/nonfinite fields, original maps, charge rounding, non-default
units and source-free legacy compatibility. Remove the corresponding consumer
projection and writers only for covered routes. Original archived bytes and
their producer identities remain fixed. Existing compatibility limits are owned
by #49/#33, reviewed by DockingMT contributors by 2027-01-06.
