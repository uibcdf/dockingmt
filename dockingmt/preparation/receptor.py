from __future__ import annotations

from typing import Any

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._export import render_pdbqt
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
from dockingmt.preparation._typing import type_projection
from dockingmt.preparation.charges import _charge_projection


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
        Assigned partial atomic charges in elementary charge.
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
        """Render the declared receptor view through MolSysMT's native writer."""
        return render_pdbqt(self, ligand=False)

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
        """Convert through MolSysMT, restoring full-precision prepared values.

        Without a source, only PDBQT's partial chemistry is available. No absent
        bonds, aromaticity or chemical assignments are inferred by DockingMT.
        """
        import molsysmt as msm

        if self.source_molsys is not None:
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

        molsys = msm.convert('pdbqt_text:' + self.to_pdbqt(), to_form='molsysmt.MolSys')
        msm.set(
            molsys,
            coordinates=puw.quantity(
                np.expand_dims(puw.get_value(self.coordinates), axis=0),
                puw.get_unit(self.coordinates),
            ),
            partial_charge=puw.quantity(self.charges, 'elementary_charge'),
        )
        return molsys

    def __repr__(self) -> str:
        return f'PreparedReceptor(state_id={self.state_id!r}, n_atoms={self.n_atoms})'


@arg_digest(config='dockingmt._argdigest')
def prepare_receptor(
    molecular_system: Any,
    selection: str = "molecule_type=='protein'",
    state_id: str | None = None,
    *,
    charge_options: dict[str, Any] | None = None,
    typing_options: dict[str, Any] | None = None,
) -> PreparedReceptor:
    """Prepare a conventional protein receptor for docking calculations.

    Extracts the selected protein component using MolSysMT, consumes named
    AutoDock atom types, and delegates typed-H reduction and charge transfer
    to MolSysMT. The native source carries the actual aggregate charges and
    virtual-H inventory; original and derived assignments remain distinct.
    Merged parents require known virtual-H counts and zero implicit H.
    Unknown counts are not inferred or repaired, and no model is chosen implicitly.

    Parameters
    ----------
    molecular_system : Any
        Molecular system in any format supported by MolSysMT (PDB, MolSys, file, etc.).
    selection : str, default "molecule_type=='protein'"
        Selection query identifying receptor atoms.
    state_id : str | None, optional
        Unique identifier for the prepared state. If None, an automatic ID is assigned.
    charge_options : mapping or None, optional
        Opt-in public MolSysMT charge assignment with an explicit named method,
        before requested typing. Complete finite source charges or this explicit
        calculation are required. Supplied zeros remain valid; no model is chosen
        automatically and no receptor repair or hydrogen stage is performed.
    typing_options : mapping or None, optional
        Opt-in public MolSysMT typing on the selected complete graph. Require
        typing_scheme='autodock4' and an explicit method. Valid preassigned native
        types are consumed without calculation. Chemistry and H must already be
        supplied; charges may come from the explicit preceding charge stage.
        No receptor repair or parameter model is selected automatically.
        Without valid named types or explicit options, preparation raises an error.

    Returns
    -------
    PreparedReceptor
        The prepared receptor state with preserved atom identities and PDBQT rendering.
    """
    import molsysmt as msm

    _, charge_options, typing_options = stage_options(
        None, charge_options, typing_options
    )
    extracted = select_one_structure(molecular_system, selection)
    extracted, workflow = run_stages(extracted, None, charge_options, typing_options)
    n_atoms = msm.get(extracted, element='system', n_atoms=True)

    atom_names, group_names, group_ids, _ = atom_metadata(extracted, 'REC')
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
    retained_names = [str(atom_names[i]) for i in retained_indices]
    retained_gnames = [str(group_names[i]) for i in retained_indices]
    retained_gids = [int(group_ids[i]) for i in retained_indices]
    retained_types = list(msm.get(reduced, element='atom', atom_ff_type=True))
    retained_charges = source_partial_charges(reduced, len(retained_indices))
    retained_coords = msm.get(reduced, element='atom', coordinates=True)[0]

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
            'charge_source': 'source_partial_charge',
            'atom_type_source': 'molsysmt_named_autodock4',
            'atom_type_assignment': typing_assignment,
            'atom_type_projection': type_projection(
                typing_assignment, retained_indices, retained_types
            ),
            **(
                {
                    'preparation_workflow': finish_stage_maps(
                        workflow, projection, list(range(len(retained_indices)))
                    )
                }
                if workflow is not None
                else {}
            ),
            'merged_hydrogen_charges': bool(charge_transfers),
            'hydrogen_policy': 'retain_polar_merge_nonpolar',
            'omitted_hydrogen_indices': omitted_hydrogen_indices,
            'partial_charge_assignment': assignment,
            'molecular_projection': projection,
            'projected_partial_charge_assignment': detached_provider_report(
                reduced.molecular_mechanics.partial_charge_assignment
            ),
            'projected_atom_type_assignment': detached_provider_report(
                reduced.molecular_mechanics.atom_type_assignment
            ),
            'charge_projection': _charge_projection(
                assignment,
                charges,
                retained_indices,
                charge_transfers,
                retained_charges,
            ),
            'source_chemistry': chemistry_evidence(
                extracted, include_residue_coverage=True
            ),
        },
        source_molsys=reduced,
    )
