# Retained ligand connectivity through MolSysMT

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), with active
ligand torsions under #6/#17 and native formats under #33. This 2026-10-23 slice
removes one molecular implementation from DockingMT's flexible preparation path.
The broader issues remain partial.

## Public contract and behavior

`build_torsion_tree` calls:

```python
blocks = msm.topology.get_covalent_blocks(
    source_molsys,
    selection=retained_indices,
    chemical_state='structure',
    structure_indices=0,
)
```

The already checked nonempty retained inventory must yield exactly one block.
Disconnected retained atoms still reject with the existing DockingMT diagnostic.
An omitted atom cannot connect selected atoms. Source indices are passed directly;
nonmonotonic retained order remains available for ROOT tie-breaking and branch
orientation. There is no molecular copy, local graph traversal, reference-state
fallback or caught provider exception in this check.

MolSysMT owns connectivity, chemical eligibility and rigid fragments. DockingMT
retains explicit cuts, recorded docking exceptions, ROOT and tree orientation.
The classifier still requires complete assigned-state chemistry before this
connectivity check; the provider's generic stored-bond graph is not itself a
chemical-completeness certificate. Default rigid preparation is unchanged.

## Delivered provider and retained composition

[MolSysMT #348](https://github.com/uibcdf/molsysmt/issues/348) delivered explicit
state/structure scope in `43e8ba8d3f6cbce87d6ed10beb23fd9a80f4cdd8`. Git ancestry
verifies it is already in the selected
`128a0bbb94e6804f5663e58a45313c77de1cc30d`; no dependency pin, public floor or
provider implementation changes here. The normally built installed provider
wheel/native identities remain those of the
[preceding receiving](provider_receiving_2026-10-23.md).

The previous local traversal's removal condition is fulfilled and its
2027-01-06 exception retired. Earlier notebooks, graph counterexamples and
scientific archives retain their original code/source identities. No historical
run is regenerated to adopt this implementation.

## Guard and selected source evidence

[The durable consumer guard](../../tests/test_rigid_fragment_consumption.py)
checks actual public delegation with the original molecular object, retained
source indices and explicit state/structure scope. Four explicit graph controls
cover reference/assigned disagreement in both directions, an omitted connector
and a connected selected component of a disconnected complete graph. They verify
source state tables, coordinate quantities, structure associations and caller
indices remain intact. A controlled provider refusal propagates as the identical
exception, without returning a local fallback result.

Before the production change, the enhanced module reports **15 passed, three
failed**, 8.53 seconds: two missing public calls and one swallowed-by-nonuse
provider refusal. The existing local algorithm passed the four graph outcomes;
this migration addresses ownership and failure propagation, not a newly asserted
numerical defect.

After replacing the traversal, **75 selected source tests pass without skips**,
56.55 seconds, 24 retained structural-attribute warnings. The selection includes
this module, torsion-policy consumption, flexible ligands, the pinned Vina torsion
matrix and native formats. It retains real Vina parser/execution controls,
nondefault quantity policy, four reference ligands, explicit ester/nitrile choices,
identity/permutation/fragment checks and unsupported chemistry/format refusals.
This is software/preparation compatibility evidence, not affinity or general
chemical-state validation.

Scientific tests use the preceding qualified Python 3.14.8/MolSysMT receiver,
with this checkout on the source path. Routine lint/administrative tools retain
the standard contributor environment; neither it nor original scientific
receivers are modified. Installed candidate receiving and exact-head four-minor
CI are separate gates whose results are recorded in the owning issue after the
candidate commit. Local type checking has no configured runner in this repository.

[Versioned evidence](data/retained_connectivity_2026-10-23/manifest.json) retains
the before/after compact source reports, commands, source hashes and resource
ownership. Ordinary installed before/after preparation snapshots compare the four
current named-preparation outputs separately from the older provisional baseline;
terminal identities and outcomes are handed off through #49.

## Remaining scope and recovery

Task resources belong to #50; review by 2026-10-30. A new receiver inherits the
retained original dependency runtime read-only and installs the authenticated
provider wheel plus the new ordinary DockingMT candidate wheel into its own prefix.
Its base runtime retains the 2026-10-27 review date and must remain while dependent
receivers/scenes need it. No automatic deletion is authorized. The initial unused
prefix selected the routine base; it was replaced before qualification with the
retained scientific base to avoid inheriting unrelated dependency conflicts.

The suite-status refresh preserves behind sibling clones and the human TopoMT
version-file edit; no sibling worktree is merged or edited. Provider-owned
projection/charge transfer and source/export maps (#223), native atom permutation
(#369) and broader serialization/pose acceptance remain under #49/#33. Source,
ordinary installed receiving and public installed-file/pair admission are separate.
HTML review/C6 remain deferred, and no public package or Release is published.
