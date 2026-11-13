"""Binding-domain composition of public MolSysMT Cartesian contacts and distances."""

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
from bindingmt._private.interface_context import (
    _geometry_digest,
    _integer,
    admit_axes,
    source_metadata,
)
from bindingmt._private.interface_records import _digest, _require
from bindingmt._private.smonitor import ArgumentError, signal
from bindingmt.core.interface import BindingInterface, characterize_interface


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
    names, axes, n_atoms = admit_axes(
        msm, molecular_system, participants, frame, source_id
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
    candidates = len(axes[0]) * len(axes[1])
    _require(
        candidates <= budget,
        'max_dense_pairs',
        'The Cartesian product exceeds the admitted dense profile; no numerical call was started.',
    )
    source_axes, group_axes, state_index, source_frame = source_metadata(
        msm, molecular_system, axes, frame, n_atoms, atom_map, source_structure_index
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
