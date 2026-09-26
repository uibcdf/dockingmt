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
from dockingmt.preparation._temporary_torsions import TorsionTree, build_torsion_tree


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
        Number of active torsional degrees of freedom. A nonzero value requires
        a verified rigid-fragment tree built by ``prepare_ligand``.
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
        _torsion_tree: TorsionTree | None = None,
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
            or torsion_dof < 0
            or torsion_dof != (len(_torsion_tree.active_bonds) if _torsion_tree else 0)
        ):
            raise ArgumentError(
                arg_name='torsion_dof',
                reason=(
                    'A nonzero TORSDOF requires a matching ROOT/BRANCH tree; '
                    'use prepare_ligand(active_torsion_bonds=...).'
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
        self._torsion_tree = _torsion_tree

    @property
    def n_atoms(self) -> int:
        """Number of atoms in the prepared ligand."""
        return len(self.atom_names)

    @property
    def pdbqt_atom_indices(self) -> list[int]:
        """Prepared-atom indices in the exact order written to PDBQT."""
        return (
            list(self._torsion_tree.atom_order)
            if self._torsion_tree is not None
            else list(range(self.n_atoms))
        )

    def to_pdbqt(self) -> str:
        """Generate a PDBQT formatted string for docking engines."""
        if self.torsion_dof != (
            len(self._torsion_tree.active_bonds) if self._torsion_tree else 0
        ):
            raise ArgumentError(
                arg_name='torsion_dof',
                reason='A nonzero TORSDOF requires a ROOT/BRANCH tree (dockingmt#6).',
            )
        coords_ang = puw.get_value(puw.convert(self.coordinates, to_unit='angstrom'))
        serials = {
            atom: serial for serial, atom in enumerate(self.pdbqt_atom_indices, 1)
        }

        def write_atom(atom: int) -> str:
            x, y, z = coords_ang[atom]
            name = self.atom_names[atom]
            if not 1 <= len(name) <= 4:
                raise ArgumentError(
                    arg_name='atom_names',
                    reason='PDBQT atom names must contain one to four characters.',
                )
            name_field = f' {name:<3s}' if len(name) <= 3 else name
            return (
                f'ATOM  {serials[atom]:5d} {name_field} '
                f'{self.group_names[atom]:3s} A{self.group_ids[atom]:4d}    '
                f'{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00    '
                f'{self.charges[atom]:6.3f} {self.atom_types[atom]:<2s}'
            )

        lines = ['ROOT']
        root_atoms = (
            self._torsion_tree.root_atoms
            if self._torsion_tree is not None
            else range(self.n_atoms)
        )
        lines.extend(write_atom(atom) for atom in root_atoms)
        lines.append('ENDROOT')

        def write_branches(branches: tuple) -> None:
            for branch in branches:
                parent_serial = serials[branch.parent_atom]
                child_serial = serials[branch.child_atom]
                lines.append(f'BRANCH {parent_serial:3d} {child_serial:3d}')
                lines.extend(write_atom(atom) for atom in branch.atoms)
                write_branches(branch.children)
                lines.append(f'ENDBRANCH {parent_serial:3d} {child_serial:3d}')

        if self._torsion_tree is not None:
            write_branches(self._torsion_tree.branches)
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
            'pdbqt_atom_indices': self.pdbqt_atom_indices,
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
    active_torsion_bonds: list[tuple[int, int]] | None = None,
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
        Legacy rigid-only assertion. A nonzero count without selected bonds is rejected.
    active_torsion_bonds : list[tuple[int, int]] | None, optional
        Explicit active bonds as pairs of selected-ligand atom indices before
        nonpolar hydrogen projection. None or an empty list keeps the ligand rigid.

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
    requested_bonds = active_torsion_bonds if active_torsion_bonds is not None else []
    torsion_tree = (
        build_torsion_tree(extracted, retained_indices, requested_bonds, elements)
        if requested_bonds
        else None
    )
    resolved_torsions = len(torsion_tree.active_bonds) if torsion_tree else 0
    if torsion_dof is not None and torsion_dof != resolved_torsions:
        raise ArgumentError(
            arg_name='torsion_dof',
            reason='TORSDOF must match the selected ROOT/BRANCH tree; specify active_torsion_bonds.',
        )

    return PreparedLigand(
        state_id=resolved_id,
        atom_names=retained_names,
        group_name=primary_group,
        coordinates=retained_coords,
        atom_types=retained_types,
        charges=retained_charges,
        torsion_dof=resolved_torsions,
        _torsion_tree=torsion_tree,
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
            'torsion_policy': 'explicit_selected_bonds'
            if torsion_tree
            else 'rigid_only',
            'active_torsion_bonds': [list(pair) for pair in torsion_tree.active_bonds]
            if torsion_tree
            else [],
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
