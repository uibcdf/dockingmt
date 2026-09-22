from __future__ import annotations

from typing import Any

import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._molsys import (
    atom_metadata,
    autodock_element,
    chemistry_evidence,
    select_one_structure,
    source_aromaticity,
    source_partial_charges,
)


class PreparedReceptor:
    """A prepared receptor molecular state ready for docking.

    Preserves source atom identities, assigned atom types, charges, and coordinates,
    and can render backend-specific representations such as PDBQT.

    Parameters
    ----------
    state_id : str
        Identifier of this prepared receptor state.
    atom_names : list[str]
        Names of the retained receptor atoms.
    group_names : list[str]
        Residue/group names of the retained receptor atoms.
    group_ids : list[int]
        Residue sequence numbers.
    coordinates : Any
        Cartesian coordinates as a PyUnitWizard length quantity of shape (N, 3).
    atom_types : list[str]
        Assigned AutoDock / force-field atom types.
    charges : list[float]
        Assigned partial atomic charges.
    metadata : dict[str, Any] | None, optional
        Arbitrary preparation metadata (e.g. pH, protonation method, source info).
    """

    def __init__(
        self,
        state_id: str,
        atom_names: list[str],
        group_names: list[str],
        group_ids: list[int],
        coordinates: Any,
        atom_types: list[str],
        charges: list[float],
        metadata: dict[str, Any] | None = None,
        source_molsys: Any = None,
    ):
        self.state_id = state_id
        self.atom_names = list(atom_names)
        self.group_names = list(group_names)
        self.group_ids = list(group_ids)
        self.coordinates = coordinates
        self.atom_types = list(atom_types)
        self.charges = [float(c) for c in charges]
        self.metadata = dict(metadata) if metadata is not None else {}
        self.source_molsys = source_molsys

    @property
    def n_atoms(self) -> int:
        """Number of atoms in the prepared receptor."""
        return len(self.atom_names)

    def to_pdbqt(self) -> str:
        """Generate a PDBQT formatted string for docking engines."""
        coords_ang = puw.get_value(puw.convert(self.coordinates, to_unit='angstrom'))
        lines = []
        for i, (name, gname, gid, (x, y, z), atype, q) in enumerate(
            zip(
                self.atom_names,
                self.group_names,
                self.group_ids,
                coords_ang,
                self.atom_types,
                self.charges,
            )
        ):
            # Standard PDBQT ATOM record format
            line = (
                f'ATOM  {i + 1:5d} {name:<4s} {gname:3s} A{gid:4d}    '
                f'{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00    {q:6.3f} {atype:<2s}'
            )
            lines.append(line)
        return '\n'.join(lines) + '\n'

    def to_dict(self) -> dict[str, Any]:
        """Serialize prepared receptor to a versioned dictionary."""
        return {
            'schema_version': '1.0',
            'state_id': self.state_id,
            'n_atoms': self.n_atoms,
            'atom_names': self.atom_names,
            'group_names': self.group_names,
            'group_ids': self.group_ids,
            'atom_types': self.atom_types,
            'charges': self.charges,
            'metadata': self.metadata,
        }

    def to_molecular_system(self) -> Any:
        """Convert the prepared receptor into a MolSysMT molecular system."""
        if self.source_molsys is not None:
            import molsysmt as msm

            molsys = msm.copy(self.source_molsys)
            if msm.get(molsys, element='system', n_atoms=True) != self.n_atoms:
                raise ArgumentError(
                    arg_name='source_molsys',
                    reason='Prepared receptor atom count differs from its molecular source.',
                )
            coords = puw.quantity(
                np.expand_dims(puw.get_value(self.coordinates), axis=0),
                puw.get_unit(self.coordinates),
            )
            msm.set(molsys, element='atom', coordinates=coords)
            return molsys

        from .._private.conversion import pdb_text_to_molsys

        coords_ang = puw.get_value(puw.convert(self.coordinates, to_unit='angstrom'))
        seen_per_res: dict[tuple[str, int], set[str]] = {}
        lines = []
        for i, (name, gname, gid, (x, y, z), atom_type) in enumerate(
            zip(
                self.atom_names,
                self.group_names,
                self.group_ids,
                coords_ang,
                self.atom_types,
            )
        ):
            res_key = (gname, gid)
            if res_key not in seen_per_res:
                seen_per_res[res_key] = set()
            aname = name
            c = 1
            while aname in seen_per_res[res_key]:
                aname = f'{name[:2]}{c}'
                c += 1
            seen_per_res[res_key].add(aname)

            lines.append(
                f'ATOM  {i + 1:5d} {aname:<4s} {gname[:3]:3s} A{gid:4d}    '
                f'{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00          {autodock_element(atom_type):>2s}'
            )
        lines.append('END\n')
        pdb_text = '\n'.join(lines)
        return pdb_text_to_molsys(pdb_text)

    def __repr__(self) -> str:
        return f'PreparedReceptor(state_id={self.state_id!r}, n_atoms={self.n_atoms})'


def prepare_receptor(
    molecular_system: Any,
    selection: str = "molecule_type=='protein'",
    state_id: str | None = None,
) -> PreparedReceptor:
    """Prepare a conventional protein receptor for docking calculations.

    Extracts the selected protein component using MolSysMT, assigns standard
    AutoDock atom types (C, A, OA, N, NA, SA, HD), merges non-polar hydrogens,
    and returns an inspectable PreparedReceptor.

    Parameters
    ----------
    molecular_system : Any
        Molecular system in any format supported by MolSysMT (PDB, MolSys, file, etc.).
    selection : str, default "molecule_type=='protein'"
        Selection query identifying receptor atoms.
    state_id : str | None, optional
        Unique identifier for the prepared state. If None, an automatic ID is assigned.

    Returns
    -------
    PreparedReceptor
        The prepared receptor state with preserved atom identities and PDBQT rendering.
    """
    import molsysmt as msm

    # Convert to MolSys for robust element extraction
    extracted = select_one_structure(molecular_system, selection)
    n_atoms = msm.get(extracted, element='system', n_atoms=True)

    atom_names, group_names, group_ids, elements = atom_metadata(extracted, 'REC')
    charges = source_partial_charges(extracted, n_atoms)
    aromaticity = source_aromaticity(extracted, n_atoms)
    bonded_atoms = (
        msm.get(
            extracted,
            element='atom',
            bonded_atoms=True,
            get_missing_bonds=False,
            chemical_state='structure',
            structure_indices=0,
        )
        if msm.has_attribute(extracted, 'bonded_atoms')
        else None
    )
    coords = msm.get(extracted, element='atom', coordinates=True)[0]  # shape (N, 3)

    aromatic_residues = {'PHE', 'TYR', 'TRP', 'HIS'}
    aromatic_ring_atoms = {
        'PHE': {'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'},
        'TYR': {'CG', 'CD1', 'CD2', 'CE1', 'CE2', 'CZ'},
        'TRP': {'CG', 'CD1', 'CD2', 'CE2', 'CE3', 'CZ2', 'CZ3', 'CH2'},
        'HIS': {'CG', 'CD2', 'CE1'},
    }

    retained_names: list[str] = []
    retained_gnames: list[str] = []
    retained_gids: list[int] = []
    retained_types: list[str] = []
    retained_charges: list[float] = []
    retained_indices: list[int] = []
    merged_hydrogen_charges: dict[int, float] = {}
    omitted_hydrogen_indices: list[int] = []

    for i, (aname, gname, gid, element) in enumerate(
        zip(atom_names, group_names, group_ids, elements)
    ):
        # Skip non-polar hydrogens (standard Vina united-atom convention for rigid receptor)
        if element.upper() == 'H':
            neighbors = bonded_atoms[i] if bonded_atoms is not None else []
            heavy_neighbors = [
                int(j) for j in neighbors if elements[int(j)].upper() != 'H'
            ]
            if len(heavy_neighbors) != 1:
                raise ArgumentError(
                    arg_name='molecular_system',
                    reason='A receptor hydrogen needs exactly one explicit heavy-atom bond for Vina preparation.',
                )
            attached = heavy_neighbors[0]
            if elements[attached].upper() not in ('N', 'O', 'S'):
                if charges is not None:
                    merged_hydrogen_charges[attached] = (
                        merged_hydrogen_charges.get(attached, 0.0) + charges[i]
                    )
                omitted_hydrogen_indices.append(i)
                continue

        atype = 'C'
        if element.upper() == 'H':
            atype = 'HD'
        elif element.upper() == 'O':
            atype = 'OA'
        elif element.upper() == 'N':
            if gname in ('HIS', 'TRP') and aname in ('ND1', 'NE2', 'NE1'):
                atype = 'NA'
            else:
                atype = 'N'
        elif element.upper() == 'S':
            atype = 'SA'
        elif element.upper() == 'C':
            if (aromaticity is not None and aromaticity[i]) or (
                aromaticity is None
                and gname in aromatic_residues
                and aname in aromatic_ring_atoms.get(gname, set())
            ):
                atype = 'A'
            else:
                atype = 'C'
        elif element.upper() == 'P':
            atype = 'P'
        elif element.upper() in ('F', 'CL', 'BR', 'I'):
            atype = element.capitalize()
        else:
            raise ArgumentError(
                arg_name='molecular_system',
                reason=f'No temporary Vina atom-type rule exists for element {element!r}.',
            )

        retained_names.append(str(aname))
        retained_gnames.append(str(gname))
        retained_gids.append(int(gid))
        retained_types.append(atype)
        retained_charges.append(charges[i] if charges is not None else 0.0)
        retained_indices.append(i)

    if charges is not None:
        for atom_index, hydrogen_charge in merged_hydrogen_charges.items():
            retained_charges[retained_indices.index(atom_index)] += hydrogen_charge

    retained_coords = puw.quantity(
        puw.get_value(coords)[retained_indices],
        puw.get_unit(coords),
    )

    resolved_id = state_id if state_id is not None else 'receptor_state_0'

    return PreparedReceptor(
        state_id=resolved_id,
        atom_names=retained_names,
        group_names=retained_gnames,
        group_ids=retained_gids,
        coordinates=retained_coords,
        atom_types=retained_types,
        charges=retained_charges,
        metadata={
            'selection': selection,
            'source_n_atoms': int(n_atoms),
            'retained_n_atoms': len(retained_names),
            'retained_atom_indices': retained_indices,
            'charge_source': 'source_partial_charge'
            if charges is not None
            else 'zero_placeholder',
            'atom_type_source': 'element_aromaticity_heuristic'
            if aromaticity is not None
            else 'element_residue_heuristic',
            'merged_hydrogen_charges': bool(merged_hydrogen_charges),
            'hydrogen_policy': 'retain_polar_merge_nonpolar',
            'omitted_hydrogen_indices': omitted_hydrogen_indices,
            'source_chemistry': chemistry_evidence(extracted),
        },
        source_molsys=msm.extract(extracted, selection=retained_indices),
    )
