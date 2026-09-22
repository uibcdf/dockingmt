from __future__ import annotations

from typing import Any

import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError


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
        Number of active torsional degrees of freedom (rotatable bonds).
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
    ):
        self.state_id = state_id
        self.atom_names = list(atom_names)
        self.group_name = str(group_name)
        self.coordinates = coordinates
        self.atom_types = list(atom_types)
        self.charges = [float(c) for c in charges]
        self.torsion_dof = int(torsion_dof)
        self.group_names = (
            list(group_names)
            if group_names is not None
            else [self.group_name] * len(self.atom_names)
        )
        self.group_ids = (
            list(group_ids) if group_ids is not None else [1] * len(self.atom_names)
        )
        self.metadata = dict(metadata) if metadata is not None else {}

    @property
    def n_atoms(self) -> int:
        """Number of atoms in the prepared ligand."""
        return len(self.atom_names)

    def to_pdbqt(self) -> str:
        """Generate a PDBQT formatted string for docking engines."""
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
        from .._private.conversion import pdb_text_to_molsys

        coords_ang = puw.get_value(puw.convert(self.coordinates, to_unit='angstrom'))
        seen_per_res: dict[tuple[str, int], set[str]] = {}
        lines = []
        for i, (name, gname, gid, (x, y, z)) in enumerate(
            zip(self.atom_names, self.group_names, self.group_ids, coords_ang)
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
                f'{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00           C'
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
        Explicit number of rotatable bonds. If None, defaults to 0 for rigid ligands.

    Returns
    -------
    PreparedLigand
        The prepared ligand state.
    """
    import molsysmt as msm

    molsys = msm.convert(molecular_system, to_form='molsysmt.MolSys')
    extracted = msm.extract(molsys, selection=selection)

    n_atoms = msm.get(extracted, element='system', n_atoms=True)
    if n_atoms == 0:
        raise ArgumentError(
            arg_name='selection',
            reason=f"Selection '{selection}' did not match any atoms in the ligand system.",
        )

    atom_names = msm.get(extracted, element='atom', name=True)
    group_names = msm.get(extracted, element='atom', group_name=True)
    try:
        group_ids = msm.get(extracted, element='atom', group_id=True)
    except Exception:
        group_ids = [1] * len(atom_names)
    coords = msm.get(extracted, element='atom', coordinates=True)[0]

    primary_group = str(group_names[0]) if len(group_names) > 0 else 'LIG'

    retained_names: list[str] = []
    retained_gnames: list[str] = []
    retained_gids: list[int] = []
    retained_types: list[str] = []
    retained_charges: list[float] = []
    retained_indices: list[int] = []

    for i, aname in enumerate(atom_names):
        aname_str = str(aname).strip()
        gname_str = (
            str(group_names[i]).strip() if i < len(group_names) else primary_group
        )
        gid_val = int(group_ids[i]) if i < len(group_ids) else 1
        # Drop non-polar hydrogens if Vina united-atom convention, or keep
        if aname_str.startswith('H') and not aname_str.startswith('HD'):
            continue

        atype = 'C'
        if aname_str.startswith('O'):
            atype = 'OA'
        elif aname_str.startswith('N'):
            atype = 'N'
        elif aname_str.startswith('S'):
            atype = 'SA'
        elif (
            aname_str.startswith('F')
            or aname_str.startswith('Cl')
            or aname_str.startswith('Br')
            or aname_str.startswith('I')
        ):
            atype = aname_str[:2]
        elif aname_str.startswith('C'):
            # Check aromaticity: Benzene or aromatic ring carbons
            if gname_str in ('BNZ', 'BENZENE') or 'aromatic' in aname_str.lower():
                atype = 'A'
            else:
                atype = 'C'

        retained_names.append(aname_str)
        retained_gnames.append(gname_str)
        retained_gids.append(gid_val)
        retained_types.append(atype)
        retained_charges.append(0.0)
        retained_indices.append(i)

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
        },
    )
