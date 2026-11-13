"""Binding-domain composition of public MolSysMT Cartesian contacts and distances."""

import hashlib
from numbers import Integral
from uuid import uuid4

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest

from bindingmt._private.interface_contacts import (
    CUTOFF_FIELD,
    DEFINITION,
    DISTANCE_VERIFICATION_RTOL,
    DISTANCES_FIELD,
    distance_statuses,
    length_record,
)
from bindingmt._private.interface_records import _digest, _require
from bindingmt._private.smonitor import ArgumentError, signal
from bindingmt.core.interface import BindingInterface, characterize_interface


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


@signal(tags=['api', 'interface', 'contacts'])
@arg_digest(config='bindingmt._argdigest')
def calculate_interface_contacts(
    molecular_system,
    *,
    participants,
    cutoff,
    structure_index,
    source_id,
    atom_map=None,
    source_structure_index=None,
    max_dense_pairs=65536,
):
    """Calculate a bounded binary contact profile using MolSysMT's public tools.

    Supply two named MolSysMT selections on one native MolSys and an explicit
    length cutoff. Coordinates must be unwrapped in the intended common frame
    and remain stable throughout the call. Intended identity/chemical state and
    absence of inter-side covalent bonds are caller preconditions. No preparation,
    alignment, PBC reconstruction or chemical recognition occurs.
    """
    import molsysmt as msm

    from bindingmt import __version__

    frame = _integer(structure_index, 'structure_index')
    budget = _integer(max_dense_pairs, 'max_dense_pairs')
    _require(budget > 0, 'max_dense_pairs', 'Admit a positive candidate-pair budget.')
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
    try:
        threshold = puw.ensure_quantity(
            cutoff, dimensionality={'[L]': 1}, to_unit='nm', standardized=False
        )
    except (MemoryError, OSError):
        raise
    except Exception as error:
        raise ArgumentError(
            arg_name='cutoff',
            reason='Supply a finite nonnegative scalar length with units.',
        ) from error
    limit = np.asarray(puw.get_value(threshold, to_unit='nm'))
    _require(
        limit.shape == () and np.isrealobj(limit) and np.isfinite(limit) and limit >= 0,
        'cutoff',
        'Supply one finite nonnegative length.',
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
    candidates = len(axes[0]) * len(axes[1])
    _require(
        candidates <= budget,
        'max_dense_pairs',
        'The Cartesian product exceeds the admitted dense profile; no numerical call was started.',
    )
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
    selected = axes[0] + axes[1]
    geometry = _geometry_digest(msm, molecular_system, selected, frame)
    common = dict(
        selection=axes[0],
        selection_2=axes[1],
        structure_indices=[frame],
        pairs=False,
        center_of_atoms=False,
        center_of_atoms_2=False,
        pbc=False,
        use_gpu=False,
        parallel=False,
        num_threads=1,
    )
    # Membership and distances are owned operations. No local search/filter kernel.
    pairs = msm.structure.get_contacts(
        molecular_system,
        threshold=threshold,
        output_type='pairs',
        output_indices='atom',
        cell_list=False,
        **common,
    )
    distances = msm.structure.get_distances(molecular_system, **common)
    _require(
        _geometry_digest(msm, molecular_system, selected, frame) == geometry,
        'molecular_system',
        'Geometry changed during the admitted operation; no result is published.',
    )
    matrix = np.asarray(puw.get_value(distances, to_unit='nm'))
    _require(
        matrix.shape == (1, len(axes[0]), len(axes[1])) and len(pairs) == 1,
        'molecular_system',
        'The owner delivered unexpected contact/distance axes.',
    )
    local_pairs = [[int(a), int(b)] for a, b in pairs[0]]
    positions = [{atom: i for i, atom in enumerate(axis)} for axis in axes]
    maps = [dict(zip(local, source)) for local, source in zip(axes, source_axes)]
    group_maps = [dict(zip(local, group)) for local, group in zip(axes, group_axes)]
    lengths = []
    originals = []
    group_pairs = {}
    for index, (a, b) in enumerate(local_pairs):
        _require(
            a in positions[0] and b in positions[1],
            'molecular_system',
            'Owner contact labels are outside the requested endpoints.',
        )
        lengths.append(float(matrix[0, positions[0][a], positions[1][b]]))
        originals.append([maps[0][a], maps[1][b]])
        groups = (group_maps[0][a], group_maps[1][b])
        if None not in groups:
            group_pairs.setdefault(groups, []).append(index)
    analysis_id = str(uuid4())
    context = {
        'source_id': source_id,
        'structure_index': frame,
        'source_structure_index': source_frame,
        'structure_chemical_state_index': state_index,
        'coordinate_policy': 'cartesian',
        'pbc': False,
        'group_axis': 'input_molsys.group_index',
        'geometry_sha256_nm_float64': geometry,
        'caller_preconditions': [
            'intended source/state and hydrogen representation',
            'stable input identity, topology/state association and whole Cartesian geometry during the call',
            'no inter-participant covalent link',
        ],
        'performed_checks': [
            'owner selection/count/group/state queries',
            'bounded unique disjoint endpoints',
            'finite selected coordinates',
            'geometry snapshots unchanged before/after',
        ],
    }
    calculation = {
        'definition': DEFINITION,
        'analysis_id': analysis_id,
        'context': context,
        'participants': {
            name: {
                'local_atom_indices': axes[i],
                'source_atom_indices': source_axes[i],
                'group_indices': group_axes[i],
            }
            for i, name in enumerate(names)
        },
        'cutoff': length_record(threshold, CUTOFF_FIELD),
        'distances': length_record(
            puw.quantity(np.asarray(lengths, dtype=float), 'nm'), DISTANCES_FIELD
        ),
        'distance_consistency': {
            'relative_bound': DISTANCE_VERIFICATION_RTOL,
            'status': distance_statuses(lengths, float(limit)),
            'changes_contact_membership': False,
        },
        'local_pairs': local_pairs,
        'source_pairs': originals,
        'group_pairs': [list(p) for p in group_pairs],
        'group_contributors': list(group_pairs.values()),
        'group_coverage': 'complete'
        if all(g is not None for axis in group_axes for g in axis)
        else 'partial',
        'calls': [
            {
                'operation': 'molsysmt.structure.get_contacts',
                'options': {
                    **common,
                    'threshold_record': length_record(threshold, CUTOFF_FIELD),
                    'output_type': 'pairs',
                    'output_indices': 'atom',
                    'cell_list': False,
                },
            },
            {'operation': 'molsysmt.structure.get_distances', 'options': common},
        ],
        'producer': {
            'bindingmt_version': __version__,
            'molsysmt_version': msm.__version__,
            'molsysmt_module': 'molsysmt',
        },
        'resources': {
            'candidate_pairs': candidates,
            'max_dense_pairs': budget,
            'estimated_payload_bytes': candidates * 1024 + len(selected) * 64,
            'route': 'explicit_dense_cartesian_cpu_one',
            'is_ram_reservation': False,
        },
        'attribution': {
            'implementation': 'MolSysMT public contact/distance operations',
            'method': 'Cartesian Euclidean distance cutoff',
            'optional_provider_execution': False,
        },
    }
    declared = characterize_interface(
        question={'kind': 'association'},
        participants={
            name: {'source_id': source_id, 'source_atom_indices': source_axes[i]}
            for i, name in enumerate(names)
        },
        grouping=[[name] for name in names],
        contexts={'calculation': context},
    )
    record = declared.to_dict()
    record['format_version'] = '0.2'
    record['analyses'] = {
        'contacts': {
            'owner': 'bindingmt',
            'reference': {'analysis_id': analysis_id},
            'authority': 'bindingmt_calculated',
            'outcome': 'completed',
            'finding_refs': [
                {'analysis_id': analysis_id, 'contact_index': i}
                for i in range(len(local_pairs))
            ],
            'original_claim': {
                k: record[k]
                for k in ('question', 'participants', 'grouping', 'contexts')
            },
            'context_refs': ['calculation'],
            'criterion': {'definition': DEFINITION},
            'calculation': calculation,
        }
    }
    record['content_sha256'] = _digest(record)
    return BindingInterface(record, experimental=True)
