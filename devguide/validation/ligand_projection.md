# Native ligand projection in production — 2026-10-24

Owner: [DockingMT #49](https://github.com/uibcdf/dockingmt/issues/49), related to
#5/#33 and [MolSysMT #223](https://github.com/uibcdf/molsysmt/issues/223).
`prepare_ligand` now calls public `msm.build.merge_nonpolar_hydrogens` instead
of determining H parents and aggregating their charges in a local loop.
Receptor preparation, PDBQT writing and pose parsing retain their separate work.

## Actual delegation and prepared state

After the existing explicit H/charge/type stages and input checks, the provider
receives the selected native ligand with `typing_scheme='autodock4',
selection='all', chemical_state='structure', structure_indices=0,
return_report=True`. It owns H-label eligibility, parent validation, charge
transfer, retained graph/coordinates, virtual-H updates, native domain handling
and derived assignment binding. Failures propagate without another projection
or an implicit repair/model calculation in DockingMT.

DockingMT consumes the returned axes for presentation and existing stage/source/
prepared/written accounting. Explicit docking cuts and ROOT/branch orientation
still use the complete selected source through public topology tools. Legacy
charge audit/remarks continue to describe the original assignment plus transfer
accounting; they do not perform the molecular transform.

`PreparedLigand.source_molsys` now holds the actual independent provider-reduced
system, with aggregate charges and updated virtual-H inventory. Reconstruction
copies this system publicly. Previously it held an extracted retained graph with
unaggregated source charges, even while `prepared.charges` held aggregate values.
This native-return behavior changes intentionally; the original caller's system
and scientific records remain untouched.

Metadata adds the detached public `molecular_projection` report and
`projected_partial_charge_assignment` / `projected_atom_type_assignment` reports.
The original `partial_charge_assignment` / `atom_type_assignment` remain in their
existing compatibility fields. The actual native assignments are derived and nest
the original producer/calculation; no parameter calculation is credited again.
Native projection indices refer to the selected post-stage source, not positions
in the original experimental file before H creation. Existing stage maps retain
that earlier distinction. The consumer's `omitted_hydrogen_indices` are merged
source H; native report `omitted_source_atom_indices` denotes outside-selection
atoms and is a different scope.

## Explicit compatibility boundary

The public operation requires one complete prepared chemical state, finite
charges, valid named AutoDock4 types, and known virtual explicit-H / zero implicit-H
counts on merged parents. Indexed H and successful named parameter assignment do
not alone establish that stored inventory. Raw native SDF admission can preserve
unknown counts. Such input now rejects before Vina, even with provisional opt-in;
DockingMT does not assume missing counts are zero or invoke an unrequested stage.

Use public `msm.physchem.get_hydrogen_inventory` to inspect the source. Supply a
prepared/declared state through MolSysMT. Its fixed-state H builder materializes a
known inventory; it also rejects unresolved stored counts and is not a general
remedy for unknown inventory. The precise native-SDF preparation/declaration route
is [handed to the provider](https://github.com/uibcdf/molsysmt/issues/223#issuecomment-6388367762)
with the raw input and executed refusals. No consumer inventory normalizer, state
pruner or fallback is introduced.

Positive methanol controls explicitly declare their finite six-indexed-atom CH4O
hypothesis, zero virtual H and disabled implicit H through public setters before
parameterization. The H-complete 5X72 charge-export control declares its inventory
as a fixture hypothesis too. These declarations are test data, not a reusable
routine deciding arbitrary molecules' inventory. Raw SDF/H-stage refusal and new
unassessed-inventory negative controls remain. Immutable fixture files are not
edited. Receptor behavior is unchanged in this slice.

## Guard and scientific limits

[Seven new guards](../../tests/test_ligand_projection_consumption.py) exercise the
actual public call, default/nondefault units, independent methanol atom-resolved
charges, virtual-H counts, original/derived reports, detached metadata and source
immutability. No unrequested H/charge/type model is allowed. A provider refusal
propagates as the same exception, and unresolved inventory rejects before engine
construction under both provisional policies. A receptor control bounds the slice.

The initial pre-change guards report three failures / one pass (the provider was
never called). The first migration selection reports 122 passed / 24 failed,
all on missing stored inventory. Declared positive inputs then yield 145 passed /
one fixture-conversion failure; the corrected focused selection passes eight
cases in 5.04 seconds. These exploratory failures remain separate from passing
qualification, and do not establish a provider calculation defect.

A full local source run executes 1,194 cases: **1,188 passed / six failed**,
813.49 seconds, 230 retained warnings. All six are positive ownership controls
still using undeclared raw methanol. They now share the explicit finite fixture;
its corrected ownership/projection/native-export selection passes **22 cases**,
11.31 seconds. The unchanged 1,188 results retain their scope; the initial full
run is not relabelled green. Exact-head hosted gates remain required after the
unskipped push and their terminal outcomes are recorded in #49. Source and ordinary
installed candidate receiving remain separate evidence.

The [versioned evidence](data/ligand_projection_2026-10-24/manifest.json) retains
reports, original diagnostics, input/source/runtime hashes and original ordinary
wheel comparisons. The provider remains the normally built/installed
`128a0bbb94e6804f5663e58a45313c77de1cc30d`, with ArgDigest/Viewer pins unchanged.
Read-only inspection of later provider main finds the two projection implementation
files unchanged; that inspection is not a runtime qualification of later main.
The shared routine environment and prior scientific receivers are not modified.

## Four reference wire comparisons

The original ordinary DockingMT wheel at
`173319a71b17b70bc6d13ecc68eb413edfd08640` is preserved. Its four preparations
were repeated at the same provider and agree with their retained snapshots.
All four candidate preparations retain atom records, coordinates, written charges,
ROOT/BRANCH/TORSDOF, written/retained axes and complete torsion selection reports.
Three complete PDBQT byte streams match. The 1S63 stream changes only its
`REMARK DOCKINGMT_PARTIAL_CHARGES` total, from
`-4.5102810375396984e-17` to `-1.734723475976807e-17` elementary charge, reflecting
the provider's floating-point aggregation order. No value is renormalized or
rounded to manufacture equality; atom records and the tree remain exact. Both
payload identities are retained, and old producer/archive bytes are not rewritten.
These are representation/software controls, not chemical or affinity admission.

## Remaining work and recovery

Next, consume the native PDBQT writer with its completed export map in the supported
prepared producer, preserving explicit serial/name/group presentation, tree policy,
precision and attribution. Then consume the qualified known-source reader for that
bound wire profile. No completed map is manufactured from the legacy writer's
metadata. Receptor projection, general native permutations (#369), wider preparation
acceptance and public file/pair qualification remain separate under #49/#33/#5 and
#30/#47. HTML/C6 review remains deferred. No public package or Release is published.

Task resources are retained under #50 for review by 2026-10-31. A new task-owned
ordinary receiver inherits the original dependency runtime read-only (review by
2026-10-27) and installs the authenticated provider wheel plus the candidate
DockingMT wheel into its own prefix. Old receivers/wheels and sibling human work
remain unchanged. Review dates are not automatic deletion. A single diagnostic
sample during the slow full run showed active public native fixture construction;
it is diagnostic evidence, not a performance comparison or a passing gate.
