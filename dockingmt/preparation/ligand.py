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


class PreparedLigand:
    """A prepared ligand/docking partner molecular state ready for docking.

    Preserves source atom identities, assigned atom types, partial charges,
    rotatable-bond degrees of freedom, and coordinates, and can render
    backend-specific representations such as PDBQT.

    Parameters
    ----------
    state_id : str
        Identifier of this prepared ligand state.
    atom_names : list[str]
        Names of the retained ligand atoms.
    group_name : str
        Residue/ligand name (e.g. 'BNZ').
    coordinates : Any
        Cartesian coordinates as a PyUnitWizard length quantity of shape (N, 3).
    atom_types : list[str]
        Assigned AutoDock atom types.
    charges : list[float]
        Assigned partial atomic charges.
    torsion_dof : int, default 0
        Number of active torsional degrees of freedom. Only 0 is currently supported.
    metadata : dict[str, Any] | None, optional
        Arbitrary preparation metadata.
    """

    def __init__(
        self,
        state_id: str,
        atom_names: list[str],
        group_name: str,
        coordinates: Any,
        atom_types: list[str],
        charges: list[float],
        torsion_dof: int = 0,
        group_names: list[str] | None = None,
        group_ids: list[int] | None = None,
        metadata: dict[str, Any] | None = None,
        source_molsys: Any = None,
    ):
        self.state_id = state_id
        self.atom_names = list(atom_names)
        self.group_name = str(group_name)
        self.coordinates = coordinates
        self.atom_types = list(atom_types)
        self.charges = [float(c) for c in charges]
        if (
            isinstance(torsion_dof, bool)
            or not isinstance(torsion_dof, int)
            or torsion_dof != 0
        ):
            raise ArgumentError(
                arg_name='torsion_dof',
                reason=(
                    'DockingMT currently writes only rigid ligand PDBQT (TORSDOF 0). '
                    'Active torsions require a ROOT/BRANCH tree; see dockingmt#6.'
                ),
            )
        self.torsion_dof = torsion_dof
        self.group_names = (
            list(group_names)
            if group_names is not None
            else [self.group_name] * len(self.atom_names)
        )
        self.group_ids = (
            list(group_ids) if group_ids is not None else [1] * len(self.atom_names)
        )
        self.metadata = dict(metadata) if metadata is not None else {}
        self.source_molsys = source_molsys

    @property
    def n_atoms(self) -> int:
        """Number of atoms in the prepared ligand."""
        return len(self.atom_names)

    def to_pdbqt(self) -> str:
        """Generate a PDBQT formatted string for docking engines."""
        if self.torsion_dof != 0:
            raise ArgumentError(
                arg_name='torsion_dof',
                reason='A nonzero TORSDOF requires a ROOT/BRANCH tree (dockingmt#6).',
            )
        coords_ang = puw.get_value(puw.convert(self.coordinates, to_unit='angstrom'))
        lines = ['ROOT']
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
            line = (
                f'ATOM  {i + 1:5d}  {name:<3s} {gname:3s} A{gid:4d}    '
                f'{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00    {q:6.3f} {atype:<2s}'
            )
            lines.append(line)
        lines.append('ENDROOT')
        lines.append(f'TORSDOF {self.torsion_dof}')
        return '\n'.join(lines) + '\n'

    def to_dict(self) -> dict[str, Any]:
        """Serialize prepared ligand to a versioned dictionary."""
        return {
            'schema_version': '1.0',
            'state_id': self.state_id,
            'n_atoms': self.n_atoms,
            'atom_names': self.atom_names,
            'group_name': self.group_name,
            'group_names': self.group_names,
            'group_ids': self.group_ids,
            'atom_types': self.atom_types,
            'charges': self.charges,
            'torsion_dof': self.torsion_dof,
            'metadata': self.metadata,
        }

    def to_molecular_system(self) -> Any:
        """Convert the prepared ligand into a MolSysMT molecular system."""
        if self.source_molsys is not None:
            import molsysmt as msm

            molsys = msm.copy(self.source_molsys)
            if msm.get(molsys, element='system', n_atoms=True) != self.n_atoms:
                raise ArgumentError(
                    arg_name='source_molsys',
                    reason='Prepared ligand atom count differs from its molecular source.',
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
        return (
            f'PreparedLigand(state_id={self.state_id!r}, n_atoms={self.n_atoms}, '
            f'torsion_dof={self.torsion_dof})'
        )


def prepare_ligand(
    molecular_system: Any,
    selection: str = "molecule_type=='small molecule'",
    state_id: str | None = None,
    torsion_dof: int | None = None,
) -> PreparedLigand:
    """Prepare a small molecule ligand for docking calculations.

    Extracts the selected ligand atoms using MolSysMT, assigns AutoDock atom types,
    and returns an inspectable PreparedLigand.

    Parameters
    ----------
    molecular_system : Any
        Molecular system in any format supported by MolSysMT.
    selection : str, default "molecule_type=='small molecule'"
        Selection query identifying ligand atoms.
    state_id : str | None, optional
        Unique identifier for the prepared ligand state.
    torsion_dof : int | None, optional
        Active torsion count. Only 0 or None (rigid ligand) is currently supported.

    Returns
    -------
    PreparedLigand
        The prepared ligand state.
    """
    import molsysmt as msm

    extracted = select_one_structure(molecular_system, selection)
    n_atoms = msm.get(extracted, element='system', n_atoms=True)

    atom_names, group_names, group_ids, elements = atom_metadata(extracted, 'LIG')
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
    coords = msm.get(extracted, element='atom', coordinates=True)[0]

    primary_group = str(group_names[0]) if len(group_names) > 0 else 'LIG'

    retained_names: list[str] = []
    retained_gnames: list[str] = []
    retained_gids: list[int] = []
    retained_types: list[str] = []
    retained_charges: list[float] = []
    retained_indices: list[int] = []
    merged_hydrogen_charges: dict[int, float] = {}
    omitted_hydrogen_indices: list[int] = []

    for i, (aname, element) in enumerate(zip(atom_names, elements)):
        aname_str = str(aname).strip()
        gname_str = (
            str(group_names[i]).strip() if i < len(group_names) else primary_group
        )
        gid_val = int(group_ids[i]) if i < len(group_ids) else 1
        if element.upper() == 'H':
            neighbors = bonded_atoms[i] if bonded_atoms is not None else []
            heavy_neighbors = [
                int(j) for j in neighbors if elements[int(j)].upper() != 'H'
            ]
            if len(heavy_neighbors) != 1:
                raise ArgumentError(
                    arg_name='molecular_system',
                    reason='A ligand hydrogen needs exactly one explicit heavy-atom bond for Vina preparation.',
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
            atype = 'N'
        elif element.upper() == 'S':
            atype = 'SA'
        elif element.upper() in ('F', 'CL', 'BR', 'I'):
            atype = element.capitalize()
        elif element.upper() == 'P':
            atype = 'P'
        elif element.upper() == 'C':
            if (aromaticity is not None and aromaticity[i]) or (
                aromaticity is None and gname_str in ('BNZ', 'BENZENE')
            ):
                atype = 'A'
            else:
                atype = 'C'
        else:
            raise ArgumentError(
                arg_name='molecular_system',
                reason=f'No temporary Vina atom-type rule exists for element {element!r}.',
            )

        retained_names.append(aname_str)
        retained_gnames.append(gname_str)
        retained_gids.append(gid_val)
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

    resolved_id = state_id if state_id is not None else f'ligand_state_{primary_group}'
    resolved_torsions = torsion_dof if torsion_dof is not None else 0

    return PreparedLigand(
        state_id=resolved_id,
        atom_names=retained_names,
        group_name=primary_group,
        coordinates=retained_coords,
        atom_types=retained_types,
        charges=retained_charges,
        torsion_dof=resolved_torsions,
        group_names=retained_gnames,
        group_ids=retained_gids,
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
            else 'element_group_heuristic',
            'torsion_policy': 'rigid_only',
            'hydrogen_policy': 'retain_polar_merge_nonpolar',
            'omitted_hydrogen_indices': omitted_hydrogen_indices,
            'atom_map_status': 'identity'
            if len(retained_indices) == n_atoms
            else 'hydrogen_subset_mapped',
            'merged_hydrogen_charges': bool(merged_hydrogen_charges),
            'source_chemistry': chemistry_evidence(extracted),
        },
        source_molsys=msm.extract(extracted, selection=retained_indices),
    )
