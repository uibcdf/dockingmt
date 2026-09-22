from __future__ import annotations

from typing import Any, Iterator

import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError


def _ensure_coordinates_quantity(coords: Any) -> Any:
    """Validate that coords is an (N, 3) physical quantity with length units."""
    if not puw.is_quantity(coords):
        raise ArgumentError(
            arg_name='coordinates',
            reason="'coordinates' must be a physical quantity with length units (e.g. using PyUnitWizard).",
        )
    if not puw.are_compatible(coords, 'nm'):
        unit_str = str(puw.get_unit(coords))
        raise ArgumentError(
            arg_name='coordinates',
            reason=f"'coordinates' has unit '{unit_str}', which is not compatible with length.",
        )
    raw = np.asarray(puw.get_value(coords), dtype=float)
    if raw.ndim != 2 or raw.shape[1] != 3:
        raise ArgumentError(
            arg_name='coordinates',
            reason=f"'coordinates' must have shape (N, 3), got shape {raw.shape}.",
        )
    unit = puw.get_unit(coords)
    return puw.quantity(raw, unit)


class DockingPose:
    """A candidate bound configuration tied to molecular state and provenance.

    Parameters
    ----------
    coordinates : Any
        Atomic coordinates of shape (N, 3) as a PyUnitWizard length quantity.
    scores : dict[str, float], optional
        Named scores produced by scoring functions or backends (e.g. {'vina': -7.5}).
    rank : int, optional
        1-indexed ranking assigned by an explicit ranking policy.
    pose_id : str, optional
        Unique identifier for the pose.
    partner_state_id : str, optional
        Identifier linking this pose to its specific ligand/partner molecular state.
    receptor_state_id : str, optional
        Identifier linking this pose to its receptor conformation/state.
    metadata : dict[str, Any], optional
        Arbitrary structured annotations (e.g. interaction flags, clusters).
    """

    def __init__(
        self,
        coordinates: Any,
        scores: dict[str, float] | None = None,
        rank: int | None = None,
        pose_id: str | None = None,
        partner_state_id: str | None = None,
        receptor_state_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ):
        self._coordinates = puw.convert(
            _ensure_coordinates_quantity(coordinates), to_unit='nm'
        )
        self.scores: dict[str, float] = dict(scores) if scores is not None else {}
        self.rank = rank
        self.pose_id = pose_id
        self.partner_state_id = partner_state_id
        self.receptor_state_id = receptor_state_id
        self.metadata: dict[str, Any] = dict(metadata) if metadata is not None else {}

    @property
    def coordinates(self) -> Any:
        """Atomic coordinates (N, 3) in nanometers."""
        return self._coordinates

    @property
    def n_atoms(self) -> int:
        """Number of atoms in the pose."""
        return int(puw.get_value(self._coordinates).shape[0])

    def to_dict(self) -> dict[str, Any]:
        """Serialize pose to a machine-readable dictionary."""
        return {
            'schema_version': '1.0',
            'pose_id': self.pose_id,
            'rank': self.rank,
            'partner_state_id': self.partner_state_id,
            'receptor_state_id': self.receptor_state_id,
            'scores': self.scores,
            'metadata': self.metadata,
            'coordinates': {
                'value': puw.get_value(self._coordinates).tolist(),
                'unit': str(puw.get_unit(self._coordinates)),
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DockingPose:
        """Reconstruct DockingPose from a serialized dictionary."""
        c_info = data['coordinates']
        coords = puw.quantity(np.asarray(c_info['value'], dtype=float), c_info['unit'])
        return cls(
            coordinates=coords,
            scores=data.get('scores'),
            rank=data.get('rank'),
            pose_id=data.get('pose_id'),
            partner_state_id=data.get('partner_state_id'),
            receptor_state_id=data.get('receptor_state_id'),
            metadata=data.get('metadata'),
        )

    def get_rmsd(self, reference: Any, selection: str = 'all') -> Any:
        """Compute the RMSD of this pose against a reference structure or pose.

        Parameters
        ----------
        reference : Any
            A reference DockingPose, coordinate quantity array, or MolSysMT system.
        selection : str, default 'all'
            Selection expression if reference is a MolSysMT system.

        Returns
        -------
        Any
            RMSD as a PyUnitWizard length quantity.
        """
        import molsysmt as msm

        coords = puw.quantity(
            np.expand_dims(puw.get_value(self._coordinates), axis=0),
            puw.get_unit(self._coordinates),
        )

        ref_sys: Any
        if isinstance(reference, DockingPose):
            ref_sys = puw.quantity(
                np.expand_dims(puw.get_value(reference._coordinates), axis=0),
                puw.get_unit(reference._coordinates),
            )
        elif puw.is_quantity(reference):
            ref_val = np.asarray(puw.get_value(reference))
            if ref_val.ndim == 2:
                ref_sys = puw.quantity(
                    np.expand_dims(ref_val, axis=0), puw.get_unit(reference)
                )
            else:
                ref_sys = reference
        else:
            ref_sys = reference

        res = msm.structure.get_rmsd(
            coords,
            reference_molecular_system=ref_sys,
            selection=selection,
        )
        return res[0]

    def to_molecular_system(self, partner: Any) -> Any:
        """Convert this pose into a MolSysMT molecular system using partner topology.

        Parameters
        ----------
        partner : Any
            The partner/ligand molecular system or PreparedLigand providing atom names/topology.

        Returns
        -------
        Any
            MolSysMT MolSys instance with this pose's coordinates.
        """
        import molsysmt as msm

        base_sys: Any
        if hasattr(partner, 'to_molecular_system'):
            base_sys = partner.to_molecular_system()
        else:
            base_sys = msm.convert(partner, to_form='molsysmt.MolSys')
        molsys = msm.copy(base_sys)
        partner_n_atoms = msm.get(molsys, element='system', n_atoms=True)
        if partner_n_atoms != self.n_atoms:
            selected = self.metadata.get('selected_atom_indices')
            expected_n_atoms = self.metadata.get('selected_partner_n_atoms')
            if (
                self.metadata.get('pose_atom_order') == 'verified_pdbqt_order'
                and expected_n_atoms == partner_n_atoms
                and isinstance(selected, list)
                and len(selected) == self.n_atoms
                and len(set(selected)) == len(selected)
                and all(
                    isinstance(i, int) and 0 <= i < partner_n_atoms for i in selected
                )
            ):
                molsys = msm.extract(molsys, selection=selected)
                partner_n_atoms = self.n_atoms
        if partner_n_atoms != self.n_atoms:
            raise ArgumentError(
                arg_name='partner',
                reason=(
                    f'Pose has {self.n_atoms} atoms but partner has {partner_n_atoms}; '
                    'a verified pose-to-partner atom map is required.'
                ),
            )
        coords_3d = puw.quantity(
            np.expand_dims(puw.get_value(self._coordinates), axis=0),
            puw.get_unit(self._coordinates),
        )
        msm.set(molsys, element='atom', coordinates=coords_3d)
        return molsys

    def __repr__(self) -> str:
        rank_str = f', rank={self.rank}' if self.rank is not None else ''
        scores_str = f', scores={self.scores}' if self.scores else ''
        return f'DockingPose(n_atoms={self.n_atoms}{rank_str}{scores_str})'


class DockingResult:
    """Structured scientific output of a docking run or protocol execution.

    Parameters
    ----------
    poses : list[DockingPose]
        Collection of candidate docking poses.
    problem_info : dict[str, Any], optional
        Contextual info on the problem (receptor, partner, domain references).
    protocol_info : dict[str, Any], optional
        Resolved protocol choices, parameters and defaults.
    provenance : dict[str, Any], optional
        Execution metadata (backend, versions, random seeds, environment).
    problem : Any, optional
        Original DockingProblem instance if available in-memory.
    """

    def __init__(
        self,
        poses: list[DockingPose],
        problem_info: dict[str, Any] | None = None,
        protocol_info: dict[str, Any] | None = None,
        provenance: dict[str, Any] | None = None,
        problem: Any = None,
    ):
        self._poses = list(poses)
        self.problem_info: dict[str, Any] = (
            dict(problem_info) if problem_info is not None else {}
        )
        self.protocol_info: dict[str, Any] = (
            dict(protocol_info) if protocol_info is not None else {}
        )
        self.provenance: dict[str, Any] = (
            dict(provenance) if provenance is not None else {}
        )
        self.problem = problem

    def __len__(self) -> int:
        return len(self._poses)

    def __getitem__(self, index: int) -> DockingPose:
        return self._poses[index]

    def __iter__(self) -> Iterator[DockingPose]:
        return iter(self._poses)

    @property
    def poses(self) -> list[DockingPose]:
        """List of all docking poses."""
        return list(self._poses)

    @property
    def top_pose(self) -> DockingPose | None:
        """The top-ranked pose (rank 1), or the first pose if unranked."""
        if not self._poses:
            return None
        ranked = [p for p in self._poses if p.rank == 1]
        return ranked[0] if ranked else self._poses[0]

    def rank_by(self, score_name: str, ascending: bool = True) -> DockingResult:
        """Produce a new DockingResult with poses ranked according to a named score.

        Parameters
        ----------
        score_name : str
            The key in pose.scores to rank by (e.g. 'vina').
        ascending : bool, default True
            If True, lower scores receive top rank (standard for binding affinities/energies).
            If False, higher scores receive top rank.
        """
        for i, pose in enumerate(self._poses):
            if score_name not in pose.scores:
                raise ArgumentError(
                    arg_name='score_name',
                    reason=f"Pose at index {i} does not have score '{score_name}'. Available: {list(pose.scores.keys())}",
                )

        sorted_poses = sorted(
            self._poses,
            key=lambda p: p.scores[score_name],
            reverse=not ascending,
        )

        new_poses: list[DockingPose] = []
        for rank_idx, pose in enumerate(sorted_poses, start=1):
            new_pose = DockingPose(
                coordinates=pose.coordinates,
                scores=pose.scores,
                rank=rank_idx,
                pose_id=pose.pose_id,
                partner_state_id=pose.partner_state_id,
                receptor_state_id=pose.receptor_state_id,
                metadata=pose.metadata,
            )
            new_poses.append(new_pose)

        new_provenance = dict(self.provenance)
        new_provenance['ranking_policy'] = {
            'score_name': score_name,
            'ascending': ascending,
        }

        return DockingResult(
            poses=new_poses,
            problem_info=self.problem_info,
            protocol_info=self.protocol_info,
            provenance=new_provenance,
            problem=self.problem,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize DockingResult to a versioned machine-readable dictionary."""
        return {
            'schema_version': '1.0',
            'problem_info': self.problem_info,
            'protocol_info': self.protocol_info,
            'provenance': self.provenance,
            'poses': [p.to_dict() for p in self._poses],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DockingResult:
        """Reconstruct DockingResult from a serialized dictionary."""
        poses = [DockingPose.from_dict(p) for p in data.get('poses', [])]
        return cls(
            poses=poses,
            problem_info=data.get('problem_info'),
            protocol_info=data.get('protocol_info'),
            provenance=data.get('provenance'),
        )

    def get_rmsds(self, reference: Any, selection: str = 'all') -> list[Any]:
        """Compute the RMSD of each pose in this result against a reference structure.

        Parameters
        ----------
        reference : Any
            Reference pose, coordinate array, or MolSysMT system.
        selection : str, default 'all'
            Selection expression if reference is a MolSysMT system.

        Returns
        -------
        list[Any]
            List of RMSD length quantities for each pose.
        """
        return [
            pose.get_rmsd(reference=reference, selection=selection)
            for pose in self._poses
        ]

    def __repr__(self) -> str:
        return f'DockingResult(n_poses={len(self._poses)})'
