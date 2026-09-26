# DockingMT

*The molecular docking layer of MolSysSuite*

[![MolSysSuite: Scientific Component](https://img.shields.io/badge/MolSysSuite-scientific%20component-0b7285?labelColor=24292f)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/repository_badges.md#scientific-component)
[![MolSysSuite policy](https://github.com/uibcdf/dockingmt/actions/workflows/molsyssuite-policy.yml/badge.svg?branch=main)](https://github.com/uibcdf/dockingmt/actions/workflows/molsyssuite-policy.yml)
[![Python 3.11 | 3.12 | 3.13](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://github.com/uibcdf/molsyssuite/blob/main/devguide/python_policy.md)
[![License](https://img.shields.io/github/license/uibcdf/dockingmt)](https://github.com/uibcdf/dockingmt/blob/main/LICENSE)

DockingMT is a native scientific component of **MolSysSuite**, designed to provide a
reproducible, inspectable, and backend-independent framework for molecular docking.

Its long-term direction evolves *from box-based docking to molecular-landscape-aware docking*,
integrating conformational, topographic, flexibility, and pharmacophoric landscapes
provided by MolSysMT, TopoMT, ElastNetMT, and PharmacophoreMT.

AutoDock Vina is the initial reference engine for canonical protein–small-molecule docking
and redocking validation.

## Molecular input

`DockingProblem` accepts molecular inputs that MolSysMT can convert to
`molsysmt.MolSys`. Select the receptor and partner independently, even when both
come from the same complex:

```python
import molsysmt as msm
import pyunitwizard as puw
from dockingmt import BoxRegion, DockingProblem

complex_path = msm.systems['T4 lysozyme L99A']['181l.pdb']
domain = BoxRegion.from_selection(
    complex_path,
    selection="group_name=='BNZ'",
    padding=puw.quantity(8.0, 'angstrom'),
)
problem = DockingProblem(
    receptor=complex_path,
    partner=complex_path,
    search_domain=domain,
    receptor_selection="molecule_type=='protein'",
    partner_selection="group_name=='BNZ'",
)

receptor = problem.receptor_molsys
ligand = problem.partner_molsys
source_ligand_indices = problem.partner_atom_indices
```

For redocking from one experimental complex, `DockingProblem.for_redocking(...)`
uses the same ligand selection and structure to define the box and the docking
partner. It selects structure 0 when the complex has one structure; when the
complex has multiple structures, pass `structure_index` explicitly. The same
index is used for the receptor, ligand and box.
`problem.to_dict()['molecular_inputs']` includes the resolved chemical state and
MolSysMT conversion report for each molecular input.
File-backed inputs also carry a SHA-256 fingerprint; reconstruction refuses a
file whose contents have changed. In-memory inputs still require the original
objects for reconstruction while [MolSysMT H5MSM charge preservation](https://github.com/uibcdf/molsysmt/issues/234)
is unresolved.

For `DockingProblem(...)`, inputs with multiple structures require
`receptor_structure_index` and `partner_structure_index` as applicable. The Vina
adapter prepares selected MolSys inputs when `dock(problem)` is called.
Preparation preserves atomic partial charges and aromaticity when the source
provides them; otherwise it records placeholder charges. AutoDock atom types
currently use a heuristic in both cases. Vina rejects these provisional
preparations by default, including `PreparedLigand`
and `PreparedReceptor` objects produced by DockingMT. To run an exploratory
calculation while [issue #5](https://github.com/uibcdf/dockingmt/issues/5)
remains open, pass `VinaProtocol(allow_provisional_preparation=True)`. The choice
and the preparation assessment are recorded in result provenance. Externally
provided PDBQT inputs are accepted with an `unassessed` chemistry assessment.
A controlled removal of nonpolar hydrogens
retains an explicit source atom map, and Vina's PDBQT output order is checked
before poses are returned. Molecular pose reconstruction and RMSD verify source
atom identities even when a flexible PDBQT tree changes their record order;
omitted hydrogens remain absent from reconstructed poses.
Raw PDBQT inputs without a molecular source map can still produce scores and
coordinates, but cannot be reconstructed as molecular poses or compared by
molecular RMSD. Explicit coordinate-array RMSD is positional. Other atom losses
require a verified map. Preparation chemistry remains provisional under
[issue #5](https://github.com/uibcdf/dockingmt/issues/5).
Ligands remain rigid by default (`TORSDOF 0`). For a molecular ligand with an
explicit graph and bond orders, select active torsions by pairs of atom indices
in the selected ligand before nonpolar hydrogen removal:

```python
from dockingmt import VinaProtocol

protocol = VinaProtocol(
    active_torsion_bonds=[(1, 2)],
    allow_provisional_preparation=True,
)
```

The same selection can be passed to `prepare_ligand(...)` when preparing a
ligand explicitly. DockingMT checks that selected bonds are single, outside
rings and amide C–N bonds, and have nonterminal heavy-atom sides; invalid or
unavailable graph information fails clearly. The temporary rigid-fragment
calculation is tracked by [MolSysMT #224](https://github.com/uibcdf/molsysmt/issues/224)
and will be removed when MolSysMT provides the verified operation. Explicit
torsions do not validate the still provisional charges and atom types.
Result provenance records the hydrogen and torsion policies, preparation
assessment, and SHA-256 digests of the PDBQT bytes submitted to Vina. Remaining
preparation-decision provenance is tracked in
[issue #4](https://github.com/uibcdf/dockingmt/issues/4).
Set `VinaProtocol(capture_backend_inputs=True)` to also retain the exact receptor
and ligand PDBQT bytes as base64 in the serialized result's `backend_artifacts`.
This increases manifest size and supports independent inspection of the backend
inputs; it does not validate their chemistry. File inputs are staged from the
captured bytes before Vina reads them, so the recorded digest identifies the
submitted content.

For the file-backed 181L regression case, save a result manifest and replay it
in a separate command:

```bash
python devtools/redocking_181l.py record --manifest /tmp/181l-manifest.json
python devtools/redocking_181l.py replay --manifest /tmp/181l-manifest.json --report /tmp/181l-report.json
```

The report lists each pose's source-mapped RMSD and named scores, near-native
rank at the declared 2.5 Å cutoff, failure mode, source and PDBQT fingerprints,
code revision, and replay differences. The manifest retains both PDBQT inputs;
replay validates their digests and checks that the new run submits identical
bytes. Its assessment is **exploratory** while
the chemical preparation in [issue #5](https://github.com/uibcdf/dockingmt/issues/5)
remains provisional. Use the reported metrics for regression, not as a validated
docking-performance claim. The measured case is documented in the
[181L regression baseline](devguide/validation/181l_redocking_exploratory.md).

An additional [1IEP external PDBQT check](devguide/validation/1iep_external_pdbqt.md)
uses the official AutoDock Vina prepared receptor and flexible ligand to audit
the Vina adapter. It retains the submitted PDBQT bytes, verifies pose atom
identity, and records the exact search box sent to Vina. DockingMT's molecular
preparation remains under [issue #5](https://github.com/uibcdf/dockingmt/issues/5).
The [1IEP native preparation audit](devguide/validation/1iep_preparation_audit.md)
also verifies seven explicitly selected torsions and records the remaining
charge and atom-type differences.

## Governance and Design Authority

* [`MOLSYSSUITE_GUIDE.md`](MOLSYSSUITE_GUIDE.md) routes suite-wide policies and cross-component issues to `uibcdf/molsyssuite`.
* [`AGENTS.md`](AGENTS.md) specifies developer and AI agent instructions.
* [`devguide/`](devguide/) contains the frozen architectural and scientific seed (`devguide v0.1`).

## Development

Routine development uses Python 3.13; the supported user range is Python 3.11 to 3.13.

```bash
# Run local gates before committing
ruff check .
ruff format --check .
pytest --receptor=llm
python devtools/devguide_index.py --check
```
