"""Binding profile admission through public MolSysMT queries and maps."""

import hashlib
from numbers import Integral

import numpy as np
import pyunitwizard as puw

from bindingmt._private.interface_records import _require


def _integer(value, name):
    _require(
        isinstance(value, Integral) and not isinstance(value, bool) and value >= 0,
        name,
        'Use an explicit nonnegative integer.',
    )
    return int(value)


def _geometry_digest(msm, source, selected, frame):
    coordinates = msm.get(
        source,
        element='atom',
        selection=selected,
        structure_indices=[frame],
        coordinates=True,
    )
    _require(
        coordinates is not None,
        'molecular_system',
        'Selected coordinates are unavailable.',
    )
    values = np.asarray(puw.get_value(coordinates, to_unit='nm'), dtype=np.float64)
    _require(
        values.shape == (1, len(selected), 3) and np.isfinite(values).all(),
        'molecular_system',
        'The selected Cartesian structure must have finite coordinates.',
    )
    return hashlib.sha256(values.astype('<f8', copy=False).tobytes()).hexdigest()


def admit_axes(msm, molecular_system, participants, frame, source_id):
    _require(
        isinstance(source_id, str) and bool(source_id.strip()),
        'source_id',
        'Name the admitted original source axis.',
    )
    _require(
        len(participants) == 2
        and all(isinstance(k, str) and k.strip() for k in participants),
        'participants',
        'Supply exactly two named MolSysMT selections.',
    )
    _require(
        msm.get_form(molecular_system) == 'molsysmt.MolSys',
        'molecular_system',
        'Supply an existing native MolSys.',
    )
    n_atoms, n_structures = msm.get(molecular_system, n_atoms=True, n_structures=True)
    _require(
        isinstance(n_structures, Integral) and frame < n_structures,
        'structure_index',
        'Select an existing structure.',
    )
    names = list(participants)
    axes = [
        list(map(int, msm.select(molecular_system, selection=participants[name])))
        for name in names
    ]
    for indices in axes:
        _require(
            indices
            and len(set(indices)) == len(indices)
            and min(indices) >= 0
            and max(indices) < n_atoms,
            'participants',
            'Each resolved endpoint must be nonempty, unique and in range.',
        )
    _require(
        not set(axes[0]) & set(axes[1]),
        'participants',
        'Resolved endpoints must be disjoint.',
    )
    return names, axes, n_atoms


def source_metadata(
    msm, molecular_system, axes, frame, n_atoms, atom_map, source_structure_index
):
    if atom_map is not None:
        mapping = msm.compose_atom_maps([atom_map])
        _require(
            mapping['n_output_atoms'] == n_atoms,
            'atom_map',
            'The owner map output axis must match the input MolSys.',
        )
        source_frame = _integer(source_structure_index, 'source_structure_index')
        source_axes = [
            [int(mapping['output_to_source_atom_indices'][i]) for i in axis]
            for axis in axes
        ]
        _require(
            all(min(axis) >= 0 for axis in source_axes),
            'atom_map',
            'Generated/unmapped members have no original-source identity.',
        )
    else:
        source_frame = (
            frame
            if source_structure_index is None
            else _integer(source_structure_index, 'source_structure_index')
        )
        _require(
            source_frame == frame,
            'source_structure_index',
            'A different source frame requires an explicit owner atom map.',
        )
        source_axes = [axis.copy() for axis in axes]
    flattened = source_axes[0] + source_axes[1]
    _require(
        len(set(flattened)) == len(flattened),
        'atom_map',
        'The selected source correspondence must be bijective.',
    )
    group_axes = []
    for axis in axes:
        values = msm.get(
            molecular_system, element='atom', selection=axis, group_index=True
        )
        group_axes.append(
            [
                None
                if v is None or v is np.ma.masked or not isinstance(v, Integral)
                else int(v)
                for v in values
            ]
        )
    state = msm.get(
        molecular_system, structure_indices=[frame], structure_chemical_state_index=True
    )
    state_index = (
        None
        if state is None or len(state) == 0 or not isinstance(state[0], Integral)
        else int(state[0])
    )
    return source_axes, group_axes, state_index, source_frame
