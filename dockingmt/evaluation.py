"""Explicit, single-case redocking evaluation using MolSysMT geometry."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from copy import deepcopy
from math import isfinite
from numbers import Integral
from typing import Any

import numpy as np
import pyunitwizard as puw
import smonitor
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.results import (
    DockingPose,
    DockingResult,
    _atom_key,
    _molecular_atom_keys,
)


def _json_copy(value, argument):
    """Require finite JSON without coercing keys, arrays or arbitrary objects."""
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ArgumentError(arg_name=argument, reason='JSON keys must be strings.')
        return {key: _json_copy(item, argument) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_copy(item, argument) for item in value]
    if value is None or type(value) in (str, bool, int):
        return value
    if type(value) is float and isfinite(value):
        return value
    raise ArgumentError(arg_name=argument, reason='Supply finite JSON values.')


def _coordinates_record(coordinates, argument):
    values = np.asarray(puw.get_value(coordinates, to_unit='angstrom'))
    if not np.isrealobj(values):
        raise ArgumentError(
            arg_name=argument, reason='Coordinates must be real lengths.'
        )
    values = np.asarray(values, dtype=float)
    if values.ndim == 3 and values.shape[0] == 1:
        values = values[0]
    if (
        values.ndim != 2
        or values.shape[1:] != (3,)
        or not len(values)
        or not np.isfinite(values).all()
    ):
        raise ArgumentError(
            arg_name=argument, reason='Use one nonempty finite coordinate structure.'
        )
    return {'value': values.tolist(), 'unit': 'angstrom'}


def _digest(record):
    return hashlib.sha256(
        json.dumps(
            record, sort_keys=True, separators=(',', ':'), allow_nan=False
        ).encode()
    ).hexdigest()


@smonitor.signal(tags=['api', 'analysis', 'redocking'])
@arg_digest(config='dockingmt._argdigest')
def evaluate_redocking(
    result: DockingResult,
    reference: Any,
    *,
    rmsd_cutoff: Any,
    top_n: tuple[int, ...] = (1, 5),
    selection: Any = 'all',
    reference_info: Mapping | None = None,
) -> dict[str, Any]:
    """Evaluate one result against one reference in a shared receptor frame.

    ``rmsd_cutoff`` is a finite non-negative scalar length with explicit units.
    Recovery means positional RMSD <= cutoff. Top-N uses the first N positions
    in the existing result order, retaining declared ranks separately. No
    alignment, symmetry correction, score ranking or chemistry validation occurs.

    Molecular or DockingPose references require verified source atom keys.
    Coordinate quantities explicitly choose caller-declared positional matching.
    All poses must cover one common atom population and compatible known states.
    ``selection`` applies to molecular references, following ``get_rmsds``; it
    does not filter pose atoms. Arrays/pose references require selection='all'.

    Return a detached finite JSON report in angstrom, with reference coordinate
    evidence, pose geometry hashes, identities, explicit policy and compact input/
    preparation/protocol/ranking context. Caller ``reference_info`` is a recorded
    declaration, not authenticated provenance. Empty results have no best pose.
    Provider failures propagate. Vina and MolSysViewer are not needed to evaluate.
    """
    import molsysmt as msm

    positional = puw.is_quantity(reference)
    pose_reference = isinstance(reference, DockingPose)
    if positional or pose_reference:
        if not isinstance(selection, str) or selection != 'all':
            raise ArgumentError(
                arg_name='selection',
                reason="Coordinate/pose references require selection='all'.",
            )
        reference_coordinates = reference if positional else reference.coordinates
        reference_keys = (
            None if positional else deepcopy(reference._verified_atom_keys())
        )
        resolved_reference = reference
        reference_selection = None
    else:
        resolved_reference = (
            reference.to_molecular_system()
            if hasattr(reference, 'to_molecular_system')
            else msm.convert(reference, to_form='molsysmt.MolSys')
        )
        if msm.get(resolved_reference, n_structures=True) != 1:
            raise ArgumentError(
                arg_name='reference', reason='Use exactly one reference structure.'
            )
        reference_coordinates = msm.get(resolved_reference, coordinates=True)
        reference_keys = _molecular_atom_keys(resolved_reference)
        reference_selection = [
            int(index) for index in msm.select(resolved_reference, selection=selection)
        ]

    reference_record = {
        'kind': 'coordinates'
        if positional
        else ('pose' if pose_reference else 'molecular_system'),
        'coordinates': _coordinates_record(reference_coordinates, 'reference'),
        'atom_keys': reference_keys,
        'selected_atom_indices': reference_selection,
        'declared_info': _json_copy(reference_info or {}, 'reference_info'),
    }
    if pose_reference:
        reference_record['pose_id'] = reference.pose_id
        reference_record['partner_state_id'] = reference.partner_state_id
        reference_record['receptor_state_id'] = reference.receptor_state_id
    reference_record['snapshot_sha256'] = _digest(reference_record)

    poses = result.poses
    rows = []
    populations = []
    for index, pose in enumerate(poses):
        if not isinstance(pose, DockingPose):
            raise ArgumentError(
                arg_name='result', reason='Every result entry must be a DockingPose.'
            )
        coordinates = _coordinates_record(pose.coordinates, 'result')
        keys = None
        if not positional or 'source_atom_keys' in pose.metadata:
            keys = deepcopy(pose._verified_atom_keys())
            populations.append(
                tuple(_atom_key(key) for key in keys)
                if positional
                else frozenset(_atom_key(key) for key in keys)
            )
        if positional and len(coordinates['value']) != len(
            reference_record['coordinates']['value']
        ):
            raise ArgumentError(
                arg_name='reference',
                reason='Coordinate reference and poses must have the same atom count.',
            )
        if pose.rank is not None and (
            isinstance(pose.rank, bool)
            or not isinstance(pose.rank, Integral)
            or pose.rank < 1
        ):
            raise ArgumentError(
                arg_name='result',
                reason='Declared ranks must be positive integers or None.',
            )
        for field in ('pose_id', 'partner_state_id', 'receptor_state_id'):
            value = getattr(pose, field)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ArgumentError(
                    arg_name='result',
                    reason=f'{field} must be a nonempty string or None.',
                )
        rows.append(
            {
                'position': index + 1,
                'pose_id': pose.pose_id,
                'rank': int(pose.rank) if pose.rank is not None else None,
                'partner_state_id': pose.partner_state_id,
                'receptor_state_id': pose.receptor_state_id,
                'n_atoms': pose.n_atoms,
                'atom_keys': keys,
                'coordinates_sha256': _digest(coordinates),
                'scores': deepcopy(pose.scores),
                'score_definitions': pose.score_definitions,
            }
        )
    if populations and any(
        population != populations[0] for population in populations[1:]
    ):
        raise ArgumentError(
            arg_name='result',
            reason='Compare a common mapped atom population in every pose.',
        )
    for field in ('partner_state_id', 'receptor_state_id'):
        known = {
            getattr(pose, field) for pose in poses if getattr(pose, field) is not None
        }
        if pose_reference and getattr(reference, field) is not None:
            known.add(getattr(reference, field))
        if len(known) > 1:
            raise ArgumentError(
                arg_name='result', reason=f'Conflicting known {field} declarations.'
            )

    cutoff = float(puw.get_value(rmsd_cutoff, to_unit='angstrom'))
    measurements = result.get_rmsds(reference=resolved_reference, selection=selection)
    if len(measurements) != len(rows):
        raise ArgumentError(
            arg_name='result',
            reason='The RMSD provider must return one value per pose.',
        )
    for row, measurement in zip(rows, measurements):
        values = np.asarray(puw.get_value(measurement, to_unit='angstrom'))
        if (
            values.shape != ()
            or not np.issubdtype(values.dtype, np.number)
            or not np.isrealobj(values)
            or not np.isfinite(values)
            or values < 0
        ):
            raise ArgumentError(
                arg_name='result',
                reason='Each RMSD must be a finite non-negative scalar length.',
            )
        row['rmsd'] = float(values)
        row['recovered'] = bool(values <= cutoff)
    closest = min(rows, key=lambda row: row['rmsd']) if rows else None
    provenance = result.provenance
    from dockingmt._version import __version__

    report = {
        'schema_version': '1.0',
        'evaluation_type': 'redocking',
        'criterion': {
            'metric': 'positional_rmsd',
            'unit': 'angstrom',
            'cutoff': cutoff,
            'comparison': '<=',
            'alignment': 'none',
            'symmetry_correction': 'none',
            'coordinate_frame': 'caller_declared_shared_receptor_frame',
            'atom_scope': 'retained_pose_atoms',
            'atom_correspondence': 'caller_declared_positional'
            if positional
            else 'verified_source_atom_keys',
            'top_n_basis': 'result_order',
        },
        'reference': reference_record,
        'poses': rows,
        'n_poses': len(rows),
        'first_pose': deepcopy(rows[0]) if rows else None,
        'closest_pose': deepcopy(closest),
        'top_n': [
            {
                'requested': n,
                'considered': min(n, len(rows)),
                'recovered': any(row['recovered'] for row in rows[:n]),
            }
            for n in top_n
        ],
        'context': {
            'problem_info': {
                key: value
                for key, value in result.problem_info.items()
                if key not in ('receptor', 'partner')
            },
            'protocol_info': result.protocol_info,
            'backend': provenance.get('backend'),
            'backend_version': provenance.get('backend_version'),
            'preparation': provenance.get('preparation'),
            'ranking_history': result.ranking_history,
            'input_artifacts': {
                role: {
                    field: value
                    for field, value in artifact.items()
                    if field in ('sha256', 'size_bytes', 'format')
                }
                for role, artifact in provenance.get('backend_artifacts', {}).items()
            },
        },
        'evaluator': {
            'dockingmt_version': __version__,
            'molsysmt_version': msm.__version__,
            'rmsd_function': 'molsysmt.structure.get_rmsd',
        },
    }
    return _json_copy(report, 'result')
