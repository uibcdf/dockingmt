"""Small, inspectable MolSysMT reads shared by the Vina preparation adapters."""

from typing import Any

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError


def autodock_element(atom_type: str) -> str:
    """Decode only the element identity carried by a known AutoDock atom type."""
    elements = {
        'A': 'C',
        'C': 'C',
        'N': 'N',
        'NA': 'N',
        'O': 'O',
        'OA': 'O',
        'S': 'S',
        'SA': 'S',
        'HD': 'H',
        'P': 'P',
        'F': 'F',
        'Cl': 'Cl',
        'Br': 'Br',
        'I': 'I',
    }
    if atom_type not in elements:
        raise ArgumentError(
            arg_name='atom_types',
            reason=f'Cannot recover an element from AutoDock type {atom_type!r}.',
        )
    return elements[atom_type]


def select_one_structure(molecular_system: Any, selection: Any) -> Any:
    """Prepare one chosen chemical state and structure from a molecular input."""
    molsys = msm.convert(molecular_system, to_form='molsysmt.MolSys')
    n_structures = msm.get(molsys, element='system', n_structures=True)
    if n_structures != 1:
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Preparation requires exactly one selected structure.',
        )
    indices = msm.select(
        molsys, selection=selection, structure_indices=0, chemical_state='structure'
    )
    if not indices:
        raise ArgumentError(
            arg_name='selection',
            reason=f"Selection '{selection}' did not match any atoms.",
        )
    return msm.extract(molsys, selection=sorted(int(index) for index in indices))


def atom_metadata(
    molsys: Any, fallback_group: str
) -> tuple[list[str], list[str], list[int], list[str]]:
    """Read atom identity without assuming that the source has residue groups."""
    n_atoms = int(msm.get(molsys, element='system', n_atoms=True))
    if not msm.has_attribute(molsys, 'atom_type'):
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Atomic elements are required to prepare a Vina input.',
        )
    elements = [
        str(x).strip()
        for x in msm.get(
            molsys,
            element='atom',
            atom_type=True,
            chemical_state='structure',
            structure_indices=0,
        )
    ]
    if msm.has_attribute(molsys, 'atom_name'):
        names = [str(x).strip() for x in msm.get(molsys, element='atom', name=True)]
    else:
        names = [f'{element}{index + 1}' for index, element in enumerate(elements)]
    # Temporary consumer guard for uibcdf/molsysmt#233: group-free systems
    # currently raise a raw IndexError when group_name is queried directly.
    if msm.has_attribute(molsys, 'group_name'):
        group_names = [
            str(x).strip() for x in msm.get(molsys, element='atom', group_name=True)
        ]
    else:
        group_names = [fallback_group] * n_atoms
    if msm.has_attribute(molsys, 'group_id'):
        group_ids = [int(x) for x in msm.get(molsys, element='atom', group_id=True)]
    else:
        group_ids = [1] * n_atoms
    return names, group_names, group_ids, elements


def source_partial_charges(molsys: Any, n_atoms: int) -> list[float] | None:
    """Return only a complete finite atomic charge array; never infer zero charges."""
    if not msm.has_attribute(molsys, 'partial_charge'):
        return None
    values = msm.get(molsys, element='atom', partial_charge=True)
    if puw.is_quantity(values):
        values = puw.get_value(values, to_unit='elementary_charge')
    charges = np.asarray(values, dtype=float)
    if charges.shape != (n_atoms,) or not np.isfinite(charges).all():
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Atomic partial charges must be complete and finite.',
        )
    return charges.tolist()


def source_aromaticity(molsys: Any, n_atoms: int) -> list[bool] | None:
    if not msm.has_attribute(
        molsys, 'atom_is_aromatic', chemical_state='structure', structure_indices=0
    ):
        return None
    values = msm.get(
        molsys,
        element='atom',
        atom_is_aromatic=True,
        chemical_state='structure',
        structure_indices=0,
    )
    if len(values) != n_atoms:
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Atomic aromaticity must have one value per atom.',
        )
    return [bool(x) for x in values]


def chemistry_evidence(molsys: Any) -> dict[str, Any]:
    """Record available structural facts without treating them as readiness."""
    completeness = msm.get(
        molsys,
        connectivity_completeness=True,
        chemical_state='structure',
        structure_indices=0,
    )
    return {
        'connectivity_completeness': list(completeness)
        if completeness is not None
        else None,
        'bond_order_available': msm.has_attribute(
            molsys,
            'bond_order',
            chemical_state='structure',
            structure_indices=0,
        ),
    }
