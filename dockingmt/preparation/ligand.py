from __future__ import annotations

from typing import Any

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._molsys import (
    atom_metadata,
    chemistry_evidence,
    detached_provider_report,
    select_one_structure,
    source_atom_types,
    source_charge_assignment,
    source_partial_charges,
)
from dockingmt.preparation._stages import finish_stage_maps, run_stages, stage_options
from dockingmt.preparation._temporary_torsions import TorsionTree, build_torsion_tree
from dockingmt.preparation._typing import type_projection, type_remark
from dockingmt.preparation.charges import _charge_projection, _charge_remark


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
        Assigned partial atomic charges in elementary charge.
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

        lines = _charge_remark(self) + type_remark(self) + ['ROOT']
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
        """Convert through MolSysMT, restoring full-precision prepared values.

        A source-free representation carries only PDBQT's partial chemistry;
        conversion does not recover absent bonds or assign a chemical model.
        MolSysMT applies the declared inverse traversal for a flexible ligand,
        transporting all available native domains onto the prepared atom axis.
        """
        import molsysmt as msm

        if self.source_molsys is None:
            molsys = msm.convert(
                'pdbqt_text:' + self.to_pdbqt(),
                to_form='molsysmt.MolSys',
                discard_torsion_tree=True,
            )
            if self._torsion_tree is not None:
                molsys = msm.permute_atoms(
                    molsys,
                    atom_indices=np.argsort(self.pdbqt_atom_indices).tolist(),
                )
            msm.set(
                molsys,
                coordinates=puw.quantity(
                    np.expand_dims(puw.get_value(self.coordinates), axis=0),
                    puw.get_unit(self.coordinates),
                ),
                partial_charge=puw.quantity(self.charges, 'elementary_charge'),
            )
            return molsys

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

    def __repr__(self) -> str:
        return (
            f'PreparedLigand(state_id={self.state_id!r}, n_atoms={self.n_atoms}, '
            f'torsion_dof={self.torsion_dof})'
        )


@arg_digest(config='dockingmt._argdigest')
def prepare_ligand(
    molecular_system: Any,
    selection: str = "molecule_type=='small molecule'",
    state_id: str | None = None,
    torsion_dof: int | None = None,
    active_torsion_bonds: list[tuple[int, int]] | None = None,
    *,
    hydrogen_options: dict[str, Any] | None = None,
    charge_options: dict[str, Any] | None = None,
    typing_options: dict[str, Any] | None = None,
) -> PreparedLigand:
    """Prepare a small molecule ligand for docking calculations.

    Extracts the selected ligand atoms using MolSysMT, consumes named AutoDock types,
    and delegates typed-H reduction and charge transfer to MolSysMT. The retained
    native system carries the actual prepared charges and derived assignment;
    original attribution and provider maps remain in preparation metadata.
    Merged parents require a declared virtual-H inventory and zero implicit H.
    Unknown counts are not inferred or repaired; supply an explicitly prepared
    chemical state. No hydrogen, charge or typing model is selected implicitly.

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
        MolSysMT classifies the complete graph. Explicit ester/thioester and
        triple-adjacent cuts retain recorded docking exceptions; restricted C-N
        links, ring, nonsingle, H and terminal bonds are rejected.
    hydrogen_options : mapping or None, optional
        Opt-in public MolSysMT hydrogen-builder arguments. Require explicit
        mode='fixed_chemical_state', pH=None and engine. Attribute policy defaults
        to strict; explicitly choose intersection to allow reported attribute loss.
    charge_options : mapping or None, optional
        Opt-in public MolSysMT charge-builder arguments, including an explicit
        named method. Charge assignment follows hydrogen addition when requested.
        No default model, state repair or engine fallback is selected.
        Complete finite source charges or this explicit calculation are required;
        absent charges raise an error. Supplied zero values remain valid inputs.
    typing_options : mapping or None, optional
        Opt-in public MolSysMT type assignment after requested H/charge stages.
        Require typing_scheme='autodock4' and an explicit method. Valid named
        assignments already present on the input are consumed without calculation.
        Without valid named types or explicit options, preparation raises an error;
        no heuristic or automatic typing model is selected.

    Returns
    -------
    PreparedLigand
        The prepared ligand state.
    """
    import molsysmt as msm

    hydrogen_options, charge_options, typing_options = stage_options(
        hydrogen_options, charge_options, typing_options
    )
    extracted = select_one_structure(molecular_system, selection)
    extracted, workflow = run_stages(
        extracted, hydrogen_options, charge_options, typing_options
    )
    n_atoms = msm.get(extracted, element='system', n_atoms=True)

    atom_names, group_names, group_ids, elements = atom_metadata(extracted, 'LIG')
    _, typing_assignment = source_atom_types(extracted, n_atoms)
    charges = source_partial_charges(extracted, n_atoms)
    assignment = source_charge_assignment(extracted)
    projected = msm.build.merge_nonpolar_hydrogens(
        extracted,
        typing_scheme='autodock4',
        selection='all',
        chemical_state='structure',
        structure_indices=0,
        return_report=True,
    )
    reduced = projected['molecular_system']
    projection = detached_provider_report(projected['report'])
    retained_indices = projection['output_to_source_atom_indices']
    charge_transfers = projection['merged_source_atom_pairs']
    omitted_hydrogen_indices = [pair[0] for pair in charge_transfers]
    # Preserve the existing docking presentation on the provider's retained axis.
    # Molecular selection, H inventory and charge aggregation belong to MolSysMT.
    retained_names = [str(atom_names[i]).strip() for i in retained_indices]
    retained_gnames = [str(group_names[i]).strip() for i in retained_indices]
    retained_gids = [int(group_ids[i]) for i in retained_indices]
    retained_types = list(msm.get(reduced, element='atom', atom_ff_type=True))
    retained_charges = source_partial_charges(reduced, len(retained_indices))
    retained_coords = msm.get(reduced, element='atom', coordinates=True)[0]
    primary_group = str(group_names[0])

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
            'charge_source': 'source_partial_charge',
            'atom_type_source': 'molsysmt_named_autodock4',
            'atom_type_assignment': typing_assignment,
            'atom_type_projection': type_projection(
                typing_assignment,
                retained_indices,
                retained_types,
                torsion_tree.atom_order if torsion_tree else None,
            ),
            'torsion_policy': 'explicit_selected_bonds'
            if torsion_tree
            else 'rigid_only',
            'active_torsion_bonds': [list(pair) for pair in torsion_tree.active_bonds]
            if torsion_tree
            else [],
            **(
                {'torsion_selection': torsion_tree.selection_report}
                if torsion_tree
                else {}
            ),
            'hydrogen_policy': 'retain_polar_merge_nonpolar',
            'omitted_hydrogen_indices': omitted_hydrogen_indices,
            'atom_map_status': 'identity'
            if len(retained_indices) == n_atoms
            else 'hydrogen_subset_mapped',
            'merged_hydrogen_charges': bool(charge_transfers),
            'molecular_projection': projection,
            'projected_partial_charge_assignment': detached_provider_report(
                reduced.molecular_mechanics.partial_charge_assignment
            ),
            'projected_atom_type_assignment': detached_provider_report(
                reduced.molecular_mechanics.atom_type_assignment
            ),
            'partial_charge_assignment': assignment,
            **(
                {
                    'preparation_workflow': finish_stage_maps(
                        workflow,
                        retained_indices,
                        list(torsion_tree.atom_order)
                        if torsion_tree
                        else list(range(len(retained_indices))),
                    )
                }
                if workflow is not None
                else {}
            ),
            'charge_projection': _charge_projection(
                assignment,
                charges,
                retained_indices,
                charge_transfers,
                retained_charges,
            ),
            'source_chemistry': chemistry_evidence(extracted),
        },
        source_molsys=reduced,
    )
