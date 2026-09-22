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
partner. `problem.to_dict()['molecular_inputs']` includes the resolved chemical
state and MolSysMT conversion report for each molecular input.
File-backed inputs also carry a SHA-256 fingerprint; reconstruction refuses a
file whose contents have changed. In-memory inputs still require the original
objects for reconstruction while [MolSysMT H5MSM charge preservation](https://github.com/uibcdf/molsysmt/issues/234)
is unresolved.

An input with multiple structures requires a `receptor_structure_index` or
`partner_structure_index`. The Vina adapter prepares selected MolSys inputs when
`dock(problem)` is called. Preparation preserves atomic partial charges and
aromaticity when the source provides them; otherwise it records placeholder
charges. AutoDock atom types currently use a heuristic in both cases. Vina
rejects these provisional preparations by default, including `PreparedLigand`
and `PreparedReceptor` objects produced by DockingMT. To run an exploratory
calculation while [issue #5](https://github.com/uibcdf/dockingmt/issues/5)
remains open, pass `VinaProtocol(allow_provisional_preparation=True)`. The choice
and the preparation assessment are recorded in result provenance. Externally
provided PDBQT inputs are accepted with an `unassessed` chemistry assessment.
A controlled removal of nonpolar hydrogens
retains an explicit source atom map, and Vina's PDBQT output order is checked
before poses are returned. Molecular pose reconstruction and RMSD verify ordered
source atom identities; omitted hydrogens remain absent from reconstructed poses.
Raw PDBQT inputs without a molecular source map can still produce scores and
coordinates, but cannot be reconstructed as molecular poses or compared by
molecular RMSD. Explicit coordinate-array RMSD is positional. Other atom losses
require a verified map. Preparation chemistry remains provisional under
[issue #5](https://github.com/uibcdf/dockingmt/issues/5).
DockingMT's current ligand writer supports rigid ligands only (`TORSDOF 0`);
requesting active torsions raises an error until a valid PDBQT torsion tree is
available under [issue #6](https://github.com/uibcdf/dockingmt/issues/6).
Result provenance records the hydrogen and torsion policies, preparation
assessment, and SHA-256 digests of the PDBQT bytes submitted to Vina. Remaining
preparation-decision provenance is tracked in
[issue #4](https://github.com/uibcdf/dockingmt/issues/4).

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
