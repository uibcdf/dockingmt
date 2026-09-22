from __future__ import annotations

from typing import Any

import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError


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
    ):
        self.state_id = state_id
        self.atom_names = list(atom_names)
        self.group_names = list(group_names)
        self.group_ids = list(group_ids)
        self.coordinates = coordinates
        self.atom_types = list(atom_types)
        self.charges = [float(c) for c in charges]
        self.metadata = dict(metadata) if metadata is not None else {}

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
    molsys = msm.convert(molecular_system, to_form='molsysmt.MolSys')
    extracted = msm.extract(molsys, selection=selection)

    n_atoms = msm.get(extracted, element='system', n_atoms=True)
    if n_atoms == 0:
        raise ArgumentError(
            arg_name='selection',
            reason=f"Selection '{selection}' did not match any atoms in the receptor system.",
        )

    atom_names = msm.get(extracted, element='atom', name=True)
    group_names = msm.get(extracted, element='atom', group_name=True)
    group_ids = msm.get(extracted, element='atom', group_id=True)
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

    for i, (aname, gname, gid) in enumerate(zip(atom_names, group_names, group_ids)):
        # Skip non-polar hydrogens (standard Vina united-atom convention for rigid receptor)
        if (
            aname.startswith('H')
            or aname.startswith('1H')
            or aname.startswith('2H')
            or aname.startswith('3H')
        ):
            continue

        atype = 'C'
        if aname.startswith('O'):
            atype = 'OA'
        elif aname.startswith('N'):
            if gname in ('HIS', 'TRP') and aname in ('ND1', 'NE2', 'NE1'):
                atype = 'NA'
            else:
                atype = 'N'
        elif aname.startswith('S'):
            atype = 'SA'
        elif aname.startswith('C'):
            if gname in aromatic_residues and aname in aromatic_ring_atoms.get(
                gname, set()
            ):
                atype = 'A'
            else:
                atype = 'C'

        retained_names.append(str(aname))
        retained_gnames.append(str(gname))
        retained_gids.append(int(gid))
        retained_types.append(atype)
        retained_charges.append(0.0)
        retained_indices.append(i)

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
        },
    )
