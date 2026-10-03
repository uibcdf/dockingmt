# Native MolSysMT format consumption: initial prepared-input profile

Issue [#33](https://github.com/uibcdf/dockingmt/issues/33) owns consumer acceptance
of experimental MolSysMT SDF/PDBQT support. The first accepted slice consumes
**already prepared PDBQT**, retaining its supplied atom inventory, charges, labels
and declared torsion tree. It does not qualify or assign chemical preparation.
The [executed notebook](native_molsysmt_formats.ipynb) exercises native round trips
and a real 1IEP docking run using explicit MolSysMT strings.

## Source and executed paths

Provider implementation: `eb0549b50689b2af5d8fbedb2687fb5746d43de6`, including the
preceding SDF/CIP work at `f70bb3314`. Inspected local source:
`bbeeb72cf4da1c7e287abf0452b420922fcbc537` (later documentation), with no tracked
provider code modifications. Runtime MolSysMT reports the stale editable-build
version `0.22.4+118.g03b318549.dirty`; that string alone is not source identity.
The refreshed suite inventory is preserved; no sibling worktree is changed.
CI and full-matrix workflows now pin the implementation commit for all four
Python lanes. Existing ArgDigest/viewer routes and the source-install fallback
remain governed by the current dependency variation and molsyssuite#31.

The [nine pinned source files](../../tests/data/vina_torsions/README.md) are
unmodified published Vina inputs at
`3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`. Tests validate their checksums before
PDBQT qualification. These preparations are comparison inputs, not independent
chemical ground truth.

| Input | Public native path exercised | Initial outcome |
| --- | --- | --- |
| 1IEP ligand PDBQT | file → explicit string → MolSys → explicit string → Vina parser | 40 atoms, seven declared branches; assignments and fragment membership preserved. |
| 1S63 ligand PDBQT | Same | 30 atoms, six branches; reference-only H retained. |
| 5X72 P59/P69 ligand PDBQT | Same, independently for each | 25 atoms and two branches each; prepared inventory preserved. |
| 1IEP rigid receptor PDBQT | file → string → MolSys → file → Vina receptor parser | 2,702 atoms; no ligand tree invented. |
| 5X72 P59/P69 SDF | explicit RDKit stereo interpretation → MolSys → V3000 SDF → MolSys | 39 atoms, 42 bonds, 15 explicit H; atom 7 remains R/S respectively. |
| Original 1IEP SDF | Public native reader with explicit stereo/property options | Rejected: nonzero valence field on atom 32. |
| Original 1S63 SDF | Same | Rejected: counts line has no explicit CTAB version. |

The two SDF profile limitations are reported with exact inputs and reproductions
in [MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215#issuecomment-5967782707).
Fixtures are not edited to make conversion pass. The existing RDKit source bridge
remains for these inputs; no silent new fallback is added.

## Supported use

```python
import molsysmt as msm
from molsysmt.form.file_pdbqt import get_torsion_tree

source = "prepared_ligand.pdbqt"
tree = get_torsion_tree(source)
native, report = msm.convert(source, to_form="molsysmt.MolSys",
                            discard_torsion_tree=True, return_report=True)
payload = msm.convert(native, to_form="string:pdbqt_text",
                      typing_scheme="autodock4", torsion_tree=tree)
# payload can be supplied directly as DockingProblem.partner.
```

DockingMT accepts the explicit `pdbqt_text:` form for receptor and partner and
removes its prefix before external Vina input. File/string identity bridges retain
original bytes; native reserialization intentionally drops source remarks/record
kinds and may reorder atoms. Native output is compared using retained serial IDs,
not equal counts or positional guessing. Known losses remain in conversion
reports. Omitting a saved tree requests rigid-receptor layout, not a ROOT-only
ligand. Tree order must match the native atom-ID axis.

Every present prepared H is retained. BRANCH edges are partial connectivity,
not a complete chemical graph. A source TORSDOF remains independent of branch
count. Charges/labels are supplied MolecularMechanics values; chemical elements
remain a separate attribute. Neither `typing_scheme='autodock4'` nor successful
Vina parsing certifies chemical assignments.

SDF ingestion of the supported stereo cases explicitly uses
`stereo_engine='rdkit', discard_properties=True`. The stereo provider and authorized
property loss are consumer choices. These native systems still need supported
chemical preparation before automatic docking. #5's default rejection and
provisional opt-in remain in force.

## Checks and boundaries

`tests/test_native_molsysmt_formats.py` supplies 16 cases: five prepared PDBQT
round trips/parser checks, pm/fs unit-policy serialization, two SDF stereo round
trips, two current unsupported SDF dialect controls, malformed/unsupported PDBQT,
stale-tree rejection before destination mutation, explicit-fragment equivalence
and actual DockingMT explicit-string docking. File/native inputs are unchanged.
Coordinate round-trip tolerances are 1e-10 angstrom for the already rounded PDBQT
inputs and 1e-4 angstrom for SDF output. The curated 5X72 SDF/PDBQT correspondence
uses unique same-element coordinates within 0.002 angstrom; this matches existing
reference-case policy and is not a general atom-mapping algorithm.

The public `msm.topology.get_rigid_fragments` explicit cuts reproduce the current
bridge's projected 5X72 fragment partition. This is initial equivalence evidence;
it does not qualify automatic rotatable-bond perception or the complete matrix.
The 1S63 added H and aryl–nitrile branch require separate mapping/policy evidence.

| Temporary operation | Removal condition / owner |
| --- | --- |
| SDF/RDKit reference bridge | MolSysMT #215 admits original 1IEP/1S63 chemistry and identity without unreported normalization. |
| Input/pose PDBQT atom parsing | MolSysMT #214/#226 covers both the actual prepared input profile and Vina MODEL pose outputs with verified atom correspondence. Current single-record support does not cover pose ensembles. |
| `_temporary_torsions` fragment/chemical checks | #224 passes the complete consumer projection/malformed matrix; docking root orientation and selected cuts remain DockingMT decisions (#6/#17). |
| Prepared ligand/receptor PDBQT writers and typing heuristics | #214 serialization plus the independently reviewed charge/type/hydrogen/projection profile meet the existing consumer contracts and atom/charge maps. Serialization alone cannot remove #5's protection. |

Minimum chemical-profile review remains open: fixed selected states/readiness
(#217), receptor coverage (#218), explicit templates (#298), fixed-state H addition
(#300), named charges (#221), chemical AutoDock typing (#222), hydrogen/charge
projection (#223), and chemical torsion eligibility (#224), all provider-owned.
Atom additions/omissions must have explicit maps; a later merging profile must
check charge aggregation. No support or scientific completion is inferred merely
from these issue references. #33 therefore remains partial.
