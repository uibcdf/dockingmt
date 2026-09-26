from __future__ import annotations

from typing import Any, Iterator

import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.problem import DockingProblem


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


def _atom_key(record: dict[str, str | None]) -> tuple[str | None, ...]:
    return tuple(
        record.get(field)
        for field in ('atom_id', 'atom_name', 'element', 'group_id', 'group_name')
    )


def _molecular_atom_keys(molsys: Any) -> list[dict[str, str | None]]:
    """Read ordered MolSysMT atom identities for a DockingMT pose map."""
    import molsysmt as msm

    required = ('atom_id', 'atom_type')
    if any(not msm.has_attribute(molsys, attribute) for attribute in required):
        raise ArgumentError(
            arg_name='partner',
            reason='A pose atom map requires source atom IDs and elements.',
        )
    atom_ids = msm.get(molsys, element='atom', atom_id=True)
    n_atoms = int(msm.get(molsys, element='system', n_atoms=True))
    atom_names = (
        msm.get(molsys, element='atom', name=True)
        if msm.has_attribute(molsys, 'atom_name')
        else [None] * n_atoms
    )
    elements = msm.get(
        molsys,
        element='atom',
        atom_type=True,
        chemical_state='structure',
        structure_indices=0,
    )
    group_ids = (
        msm.get(molsys, element='atom', group_id=True)
        if msm.has_attribute(molsys, 'group_id')
        else [None] * n_atoms
    )
    # MolSysMT currently raises IndexError for group-free group_name queries (#233).
    group_names = (
        msm.get(molsys, element='atom', group_name=True)
        if msm.has_attribute(molsys, 'group_name')
        else [None] * n_atoms
    )
    columns = (atom_ids, atom_names, elements, group_ids, group_names)
    if any(len(column) != n_atoms for column in columns):
        raise ArgumentError(
            arg_name='partner', reason='Source atom identity arrays are incomplete.'
        )
    if any(
        value is None or not str(value).strip()
        for column in (atom_ids, elements)
        for value in column
    ):
        raise ArgumentError(
            arg_name='partner',
            reason='Source atom IDs and elements must be set.',
        )
    records = [
        {
            'atom_id': str(atom_ids[i]),
            'atom_name': str(atom_names[i]) if atom_names[i] is not None else None,
            'element': str(elements[i]),
            'group_id': str(group_ids[i]) if group_ids[i] is not None else None,
            'group_name': str(group_names[i]) if group_names[i] is not None else None,
        }
        for i in range(n_atoms)
    ]
    if len({_atom_key(record) for record in records}) != n_atoms:
        raise ArgumentError(
            arg_name='partner', reason='Source atom identities are not unique.'
        )
    return records


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
            Molecular references require the pose's verified source atom map.
            Coordinate arrays are compared positionally by explicit caller choice.
        selection : str, default 'all'
            Selection expression if reference is a MolSysMT system. Extra reference
            hydrogens may be omitted from the mapped comparison.

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
            keys = self._verified_atom_keys()
            reference_keys = reference._verified_atom_keys()
            reference_lookup = {
                _atom_key(record): index for index, record in enumerate(reference_keys)
            }
            if set(reference_lookup) != {_atom_key(record) for record in keys}:
                raise ArgumentError(
                    arg_name='reference',
                    reason='Pose atom identities differ from reference pose identities.',
                )
            reference_coordinates = puw.get_value(reference._coordinates)[
                [reference_lookup[_atom_key(record)] for record in keys]
            ]
            ref_sys = puw.quantity(
                np.expand_dims(reference_coordinates, axis=0),
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
            keys = self._verified_atom_keys()
            reference_molsys = msm.convert(reference, to_form='molsysmt.MolSys')
            if msm.get(reference_molsys, element='system', n_structures=True) != 1:
                raise ArgumentError(
                    arg_name='reference',
                    reason='Molecular RMSD requires one reference structure.',
                )
            reference_keys = _molecular_atom_keys(reference_molsys)
            selected = msm.select(reference_molsys, selection=selection)
            selected_keys = [reference_keys[int(index)] for index in selected]
            reference_lookup = {
                _atom_key(record): int(index)
                for index, record in zip(selected, selected_keys)
            }
            pose_keys = {_atom_key(record) for record in keys}
            if not pose_keys.issubset(reference_lookup) or any(
                record['element'] != 'H'
                for record in selected_keys
                if _atom_key(record) not in pose_keys
            ):
                raise ArgumentError(
                    arg_name='reference',
                    reason=(
                        'Reference atoms do not match the verified pose map; '
                        'only omitted hydrogens may remain in the reference.'
                    ),
                )
            reference_coordinates = msm.get(
                reference_molsys, element='atom', coordinates=True
            )
            values = puw.get_value(reference_coordinates)[
                0, [reference_lookup[_atom_key(record)] for record in keys], :
            ]
            ref_sys = puw.quantity(
                np.expand_dims(values, axis=0),
                puw.get_unit(reference_coordinates),
            )

        res = msm.structure.get_rmsd(
            coords,
            reference_molecular_system=ref_sys,
            selection='all',
        )
        return res[0]

    def _verified_atom_keys(self) -> list[dict[str, str | None]]:
        keys = self.metadata.get('source_atom_keys')
        if (
            self.metadata.get('pose_atom_order') != 'verified_pdbqt_order'
            or not isinstance(keys, list)
            or len(keys) != self.n_atoms
            or any(not isinstance(record, dict) for record in keys)
            or any(
                any(
                    not isinstance(record.get(field), str) or not record[field]
                    for field in ('atom_id', 'element')
                )
                or any(
                    record.get(field) is not None and not isinstance(record[field], str)
                    for field in ('atom_name', 'group_id', 'group_name')
                )
                for record in keys
            )
            or len({_atom_key(record) for record in keys}) != len(keys)
        ):
            raise ArgumentError(
                arg_name='pose',
                reason='Molecular reconstruction and RMSD require a verified source atom map.',
            )
        return keys

    def to_molecular_system(self, partner: Any) -> Any:
        """Convert this pose into a MolSysMT molecular system using partner topology.

        Parameters
        ----------
        partner : Any
            The source partner/ligand molecular system or PreparedLigand. Its ordered
            atom identities must match the verified pose map. Omitted hydrogens
            remain absent from the returned molecular system.

        Returns
        -------
        Any
            MolSysMT MolSys instance with this pose's coordinates.
        """
        import molsysmt as msm

        expected_keys = self._verified_atom_keys()
        base_sys: Any
        if hasattr(partner, 'to_molecular_system'):
            base_sys = partner.to_molecular_system()
        else:
            base_sys = msm.convert(partner, to_form='molsysmt.MolSys')
        molsys = msm.copy(base_sys)
        partner_n_atoms = msm.get(molsys, element='system', n_atoms=True)
        selected = self.metadata.get('selected_atom_indices')
        expected_n_atoms = self.metadata.get('selected_partner_n_atoms')
        if selected is not None:
            if (
                expected_n_atoms != partner_n_atoms
                or not isinstance(selected, list)
                or len(selected) != self.n_atoms
                or len(set(selected)) != len(selected)
                or any(
                    not isinstance(i, int) or i < 0 or i >= partner_n_atoms
                    for i in selected
                )
            ):
                raise ArgumentError(
                    arg_name='partner',
                    reason='The pose-to-partner atom indices are invalid.',
                )
            molsys = msm.extract(molsys, selection=selected)
            partner_n_atoms = msm.get(molsys, element='system', n_atoms=True)
        if partner_n_atoms != self.n_atoms:
            raise ArgumentError(
                arg_name='partner',
                reason=(
                    f'Pose has {self.n_atoms} atoms but partner has {partner_n_atoms}; '
                    'a verified pose-to-partner atom map is required.'
                ),
            )
        molecular_keys = _molecular_atom_keys(molsys)
        pose_index_by_key = {
            _atom_key(record): index for index, record in enumerate(expected_keys)
        }
        if {_atom_key(record) for record in molecular_keys} != set(pose_index_by_key):
            raise ArgumentError(
                arg_name='partner',
                reason='Partner atom identities differ from the verified pose map.',
            )
        molecular_order = [
            pose_index_by_key[_atom_key(record)] for record in molecular_keys
        ]
        coords_3d = puw.quantity(
            np.expand_dims(puw.get_value(self._coordinates)[molecular_order], axis=0),
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

    def reconstruct_problem(
        self, receptor: Any = None, partner: Any = None
    ) -> DockingProblem:
        """Recover the recorded problem, verifying available source fingerprints.

        File-backed inputs can be loaded from the manifest alone. Molecular
        objects that were not serialized must be supplied explicitly.
        """
        if not self.problem_info:
            raise ArgumentError(
                arg_name='problem_info',
                reason='The result has no recorded docking problem to reconstruct.',
            )
        problem = DockingProblem.from_dict(
            self.problem_info, receptor=receptor, partner=partner
        )
        self.problem = problem
        return problem

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
