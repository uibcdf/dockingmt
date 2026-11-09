"""Associate existing provider analyses with one explicitly selected docking pose."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError, signal
from dockingmt.core.results import (
    DockingPose,
    DockingResult,
    _atom_key,
    _coordinate_values,
    _molecular_atom_keys,
)


class PoseInteractions:
    """A detached association between a result, one pose and its analysed carrier.

    ``pose_index`` is a zero-based collection position, independent of scientific
    rank or pose ID. ``pose_atom_indices[i]`` identifies pose atom i on the carrier
    axis. The carrier must contain one structure and existing named full analyses.
    No atom matching, molecular preparation, detection or frame replication occurs.

    State IDs and ``assume_aligned=True`` are caller declarations. The operation
    checks the mapped pose's ordered atom labels/elements and physical coordinates;
    it does not validate chemical equivalence, the rest of the receptor geometry,
    analysis authenticity or biological meaning. Supply an already admitted carrier.

    Result, analysis and carrier accessors return independent objects. The
    association dictionary is inspection evidence, not a molecular persistence
    codec. Use MolSysMT's supported persistence for the complete carrier/analyses.
    """

    @arg_digest(
        config='dockingmt._argdigest',
        native_constructor='dockingmt.interactions.PoseInteractions.__init__',
    )
    def __init__(
        self,
        result: DockingResult,
        molecular_system: Any,
        *,
        pose_index: int,
        pose_atom_indices: Any,
        partner_state_id: str,
        receptor_state_id: str,
        assume_aligned: bool = False,
        coordinate_tolerance: Any = None,
    ):
        if not assume_aligned:
            raise ArgumentError(
                arg_name='assume_aligned',
                reason='Declare the admitted carrier in the original receptor frame.',
            )
        if pose_index >= len(result):
            raise ArgumentError(
                arg_name='pose_index', reason='Select an existing collection position.'
            )
        record = result.to_dict()
        pose = result[pose_index]
        expected_keys = pose._verified_atom_keys()
        for argument, value in (
            ('partner_state_id', partner_state_id),
            ('receptor_state_id', receptor_state_id),
        ):
            if value is None or value != getattr(pose, argument):
                raise ArgumentError(
                    arg_name=argument,
                    reason='Declare the known state ID recorded by the selected pose.',
                )
        if len(pose_atom_indices) != pose.n_atoms:
            raise ArgumentError(
                arg_name='pose_atom_indices',
                reason='Supply exactly one carrier atom index per pose atom.',
            )

        import molsysmt as msm

        carrier = msm.copy(msm.convert(molecular_system, to_form='molsysmt.MolSys'))
        n_atoms = msm.get(carrier, element='system', n_atoms=True)
        if n_atoms is None:
            raise ArgumentError(
                arg_name='molecular_system',
                reason='Supply a carrier with a known atom count.',
            )
        n_atoms = int(n_atoms)
        n_structures = msm.get(carrier, element='system', n_structures=True)
        if n_structures is None:
            raise ArgumentError(
                arg_name='molecular_system',
                reason='Supply a carrier with a known coordinate structure count.',
            )
        n_structures = int(n_structures)
        if n_structures != 1:
            raise ArgumentError(
                arg_name='molecular_system',
                reason='Supply the admitted one-structure carrier; no frames are projected.',
            )
        if any(index >= n_atoms for index in pose_atom_indices):
            raise ArgumentError(
                arg_name='pose_atom_indices', reason='An index is outside the carrier.'
            )
        actual_keys = _molecular_atom_keys(carrier, atom_indices=pose_atom_indices)
        if [_atom_key(key) for key in actual_keys] != [
            _atom_key(key) for key in expected_keys
        ]:
            raise ArgumentError(
                arg_name='pose_atom_indices',
                reason='Ordered carrier atom identities differ from the pose map.',
            )
        coordinates = msm.get(carrier, element='atom', coordinates=True)
        if coordinates is None:
            raise ArgumentError(
                arg_name='molecular_system',
                reason='Supply coordinates for the admitted one-structure carrier.',
            )
        values = puw.get_value(coordinates, to_unit='angstrom')
        if np.shape(values) != (1, n_atoms, 3):
            raise ArgumentError(
                arg_name='molecular_system',
                reason='Carrier coordinate axes are invalid.',
            )
        mapped = puw.quantity(
            _coordinate_values(values[0, list(pose_atom_indices), :]), 'angstrom'
        )
        tolerance = float(puw.get_value(coordinate_tolerance, to_unit='angstrom'))
        if not puw.are_close(mapped, pose.coordinates, rtol=0, atol=tolerance):
            raise ArgumentError(
                arg_name='molecular_system',
                reason='Mapped carrier coordinates differ from the selected pose.',
            )

        # The public MolSysMT accessor owns full-result and carrier-axis admission.
        analyses = carrier.interactions
        if not analyses:
            raise ArgumentError(
                arg_name='molecular_system', reason='Supply existing named analyses.'
            )
        self._result_record = record
        self._carrier = carrier
        self._pose_index = pose_index
        self._analysis_names = tuple(analyses)
        self._association = {
            'pose_index': pose_index,
            'original_pose_count': len(result),
            'pose_id': pose.pose_id,
            'partner_state_id': partner_state_id,
            'receptor_state_id': receptor_state_id,
            'pose_atom_indices': list(pose_atom_indices),
            'structure_index': 0,
            'carrier_n_atoms': n_atoms,
            'carrier_n_structures': n_structures,
            'assume_aligned': True,
            'coordinate_check_scope': 'mapped pose atoms only',
            'coordinate_tolerance': {'value': tolerance, 'unit': 'angstrom'},
            'relative_tolerance': 0,
            'analysis_names': list(analyses),
            'analysis_evaluated': {
                name: bool(0 in analysis.evaluated_structure_indices)
                for name, analysis in analyses.items()
            },
            'other_pose_evaluation': 'not established by this association',
            'chemical_equivalence_validated': False,
            'analysis_producer_authenticated': False,
        }

    @property
    def pose_index(self) -> int:
        """Zero-based position in the complete original result."""
        return self._pose_index

    @property
    def result(self) -> DockingResult:
        """Restore a detached complete result through its existing public codec."""
        return DockingResult.from_dict(self._result_record)

    @property
    def pose(self) -> DockingPose:
        """Restore only the selected pose, preserving its original identity/rank."""
        return DockingPose.from_dict(self._result_record['poses'][self._pose_index])

    @property
    def association(self) -> dict[str, Any]:
        """Detached association declarations and mapped-coordinate check evidence."""
        return deepcopy(self._association)

    @property
    def analysis_names(self) -> tuple[str, ...]:
        """Original provider analysis names, including evaluated-empty analyses."""
        return self._analysis_names

    @arg_digest(config='dockingmt._argdigest')
    def get_analysis(self, name: str) -> Any:
        """Return a provider-owned copy for its public filtering/interchange APIs."""
        if name not in self._analysis_names:
            raise ArgumentError(
                arg_name='name', reason='Choose a stored name from analysis_names.'
            )
        return self._carrier.interactions[name].copy()

    def to_molecular_system(self) -> Any:
        """Return the complete detached carrier, retaining all named analyses."""
        import molsysmt as msm

        return msm.copy(self._carrier)


@signal(tags=['api', 'interactions', 'association'])
def bind_interactions(
    result: DockingResult,
    molecular_system: Any,
    *,
    pose_index: int,
    pose_atom_indices: Any,
    partner_state_id: str,
    receptor_state_id: str,
    assume_aligned: bool = False,
    coordinate_tolerance: Any = None,
) -> PoseInteractions:
    """Bind existing analyses to one pose without modifying the original result.

    See :class:`PoseInteractions` for declarations, checks, ownership and limits.
    Its constructor performs the ArgDigest value contract once; this convenience
    function delegates without repeating digestion or copying molecular state.
    """
    return PoseInteractions(
        result,
        molecular_system,
        pose_index=pose_index,
        pose_atom_indices=pose_atom_indices,
        partner_state_id=partner_state_id,
        receptor_state_id=receptor_state_id,
        assume_aligned=assume_aligned,
        coordinate_tolerance=coordinate_tolerance,
    )
