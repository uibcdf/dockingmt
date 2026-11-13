"""Binding-domain burial composition of three public MolSysMT SASA contexts."""

import hashlib
from importlib.resources import files
from numbers import Integral
from uuid import uuid4

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest

from bindingmt._private.interface_burial import (
    DEFINITION,
    PROBE_FIELD,
    RADII_FIELD,
    VERIFICATION_RTOL,
    area_record,
    group_contributions,
    loss_statuses,
)
from bindingmt._private.interface_contacts import length_record
from bindingmt._private.interface_context import (
    _geometry_digest,
    _integer,
    admit_axes,
    source_metadata,
)
from bindingmt._private.interface_records import _digest, _require
from bindingmt._private.smonitor import ArgumentError, signal
from bindingmt.core.interface import BindingInterface, characterize_interface


def _radii(msm, source, axis):
    quantity = msm.physchem.get_atomic_radius(source, selection=axis, definition='vdw')
    values = np.asarray(puw.get_value(quantity, to_unit='nm'), dtype=float)
    _require(
        values.shape == (len(axis),)
        and np.isfinite(values).all()
        and (values > 0).all(),
        'molecular_system',
        'The element-vdW model requires positive finite atomic radii.',
    )
    return values


def _state(msm, source, frame):
    values = msm.get(
        source, structure_indices=[frame], structure_chemical_state_index=True
    )
    return (
        None
        if values is None or not len(values) or not isinstance(values[0], Integral)
        else int(values[0])
    )


@signal(tags=['api', 'interface', 'burial'])
@arg_digest(config='bindingmt._argdigest')
def calculate_interface_burial(
    molecular_system,
    *,
    participants,
    structure_index,
    source_id,
    probe_radius,
    n_sphere_points,
    hydrogen_policy,
    atom_map=None,
    source_structure_index=None,
    max_surface_evaluations=20000000,
):
    """Compose fixed-geometry, supplied-H, element-vdW SASA losses on two sides.

    Supply a native MolSys with caller-admitted identity, chemical state and whole
    Cartesian coordinates, stable throughout the call. No inter-side covalent
    links/cut required chemistry are admitted. Explicit probe and sampling choices
    define this model; it predicts neither affinity nor chemical correctness.
    Required MolSysMT child failures propagate without publishing a partial zero.
    """
    import molsysmt as msm

    from bindingmt import __version__

    frame = _integer(structure_index, 'structure_index')
    names, axes, n_atoms = admit_axes(
        msm, molecular_system, participants, frame, source_id
    )
    axes = [
        sorted(axis) for axis in axes
    ]  # public extract's documented input-axis order
    union = sorted(axes[0] + axes[1])
    _require(
        hydrogen_policy == 'as_supplied',
        'hydrogen_policy',
        'Explicitly admit the supplied H inventory with as_supplied.',
    )
    try:
        probe = puw.ensure_quantity(
            probe_radius, dimensionality={'[L]': 1}, to_unit='nm', standardized=False
        )
    except (MemoryError, OSError):
        raise
    except Exception as error:
        raise ArgumentError(
            arg_name='probe_radius', reason='Supply a scalar nonnegative length.'
        ) from error
    limit = np.asarray(puw.get_value(probe, to_unit='nm'))
    _require(
        limit.shape == () and np.isrealobj(limit) and np.isfinite(limit) and limit >= 0,
        'probe_radius',
        'Supply one finite nonnegative length.',
    )
    work = sum(len(axis) ** 2 for axis in [*axes, union]) * n_sphere_points
    _require(
        work <= max_surface_evaluations,
        'max_surface_evaluations',
        'The brute-force work bound exceeds admission; no extraction/SASA was started.',
    )
    source_axes, group_axes, state, source_frame = source_metadata(
        msm, molecular_system, axes, frame, n_atoms, atom_map, source_structure_index
    )
    geometry = _geometry_digest(msm, molecular_system, union, frame)
    radii = _radii(msm, molecular_system, union)
    types = list(
        msm.get(molecular_system, element='atom', selection=union, atom_type=True)
    )
    options = dict(
        element='atom',
        selection='all',
        structure_indices=[0],
        engine='MolSysMT',
        pbc=False,
        use_gpu=False,
        use_cell_list=False,
        parallel=False,
        num_threads=1,
        n_sphere_points=n_sphere_points,
        probe_radius=probe,
    )
    results, calls, projections = [], [], []
    positions = {atom: i for i, atom in enumerate(union)}
    for axis in [*axes, union]:
        subset = msm.extract(
            molecular_system, selection=axis, structure_indices=[frame]
        )
        comparison = msm.compare(
            molecular_system,
            subset,
            selection=axis,
            structure_indices=[frame],
            structure_indices_2=[0],
            atom_type=True,
            coordinates=True,
            include_none=True,
            output_type='dictionary',
        )
        coordinate_sha = _geometry_digest(msm, molecular_system, axis, frame)
        indices = [positions[i] for i in axis]
        _require(
            comparison == {'atom_type': True, 'coordinates': True}
            and _geometry_digest(msm, subset, list(range(len(axis))), 0)
            == coordinate_sha
            and _state(msm, subset, 0) == state
            and list(msm.get(subset, element='atom', atom_type=True))
            == [types[i] for i in indices]
            and np.array_equal(
                _radii(msm, subset, list(range(len(axis)))), radii[indices]
            ),
            'molecular_system',
            'Owner extraction did not preserve the admitted surface model.',
        )
        projections.append(
            {
                'input_atom_indices': axis,
                'input_structure_index': frame,
                'local_structure_index': 0,
                'chemical_state_index': state,
                'geometry_sha256_nm_float64': coordinate_sha,
                'owner_comparison': comparison,
                'transport_verified': True,
            }
        )
        quantity = msm.physchem.get_sasa(subset, **options)
        areas = np.asarray(puw.get_value(quantity, to_unit='nm**2'), dtype=float)
        _require(
            areas.shape == (1, len(axis))
            and np.isfinite(areas).all()
            and (areas >= 0).all(),
            'molecular_system',
            'The owner returned unavailable/nonphysical SASA axes.',
        )
        _require(
            _geometry_digest(msm, subset, list(range(len(axis))), 0) == coordinate_sha,
            'molecular_system',
            'A required child changed its input geometry.',
        )
        results.append(areas[0])
        calls.append(
            {
                'operation': 'molsysmt.physchem.get_sasa',
                'input_atom_indices': axis,
                'options': {
                    **{k: v for k, v in options.items() if k != 'probe_radius'},
                    'probe_radius_record': length_record(probe, PROBE_FIELD),
                },
            }
        )
    _require(
        _geometry_digest(msm, molecular_system, union, frame) == geometry
        and np.array_equal(_radii(msm, molecular_system, union), radii)
        and list(
            msm.get(molecular_system, element='atom', selection=union, atom_type=True)
        )
        == types
        and source_metadata(
            msm,
            molecular_system,
            axes,
            frame,
            n_atoms,
            atom_map,
            source_structure_index,
        )
        == (source_axes, group_axes, state, source_frame),
        'molecular_system',
        'The source changed during calculation; no result is published.',
    )
    members, statuses, sums = {}, {}, []
    for i, name in enumerate(names):
        indices = [positions[j] for j in axes[i]]
        isolated, combined = results[i], results[2][indices]
        losses = isolated - combined
        sums.append(float(np.sum(losses)))
        statuses[name] = loss_statuses(isolated, losses)
        members[name] = {
            'local_atom_indices': axes[i],
            'source_atom_indices': source_axes[i],
            'group_indices': group_axes[i],
            'radii': length_record(puw.quantity(radii[indices], 'nm'), RADII_FIELD),
            'isolated_area': area_record(isolated),
            'combined_area': area_record(combined),
            'atomic_loss': area_record(losses),
            'side_loss': area_record(sums[-1]),
            'group_contributions': group_contributions(group_axes[i], losses),
            'group_coverage': 'partial' if None in group_axes[i] else 'complete',
        }
    context = {
        'source_id': source_id,
        'structure_index': frame,
        'source_structure_index': source_frame,
        'structure_chemical_state_index': state,
        'coordinate_policy': 'cartesian',
        'pbc': False,
        'group_axis': 'input_molsys.group_index',
        'environment': 'selected_A_union_B',
        'geometry_sha256_nm_float64': geometry,
        'projections': projections,
        'caller_preconditions': [
            'intended identity/state and supplied H inventory',
            'stable input identity/topology/state and whole Cartesian geometry',
            'no inter-side covalent links or cut required participant chemistry',
        ],
        'performed_checks': [
            'public owner selection/count/group/state queries',
            'unique disjoint endpoints and bounded work',
            'positive element-vdW radii',
            'owner comparison and exact coordinate/type/radius/state transport',
            'original source snapshots unchanged before/after',
        ],
    }
    analysis_id = str(uuid4())
    calculation = {
        'definition': DEFINITION,
        'analysis_id': analysis_id,
        'context': context,
        'participants': members,
        'probe_radius': length_record(probe, PROBE_FIELD),
        'n_sphere_points': n_sphere_points,
        'hydrogen_policy': hydrogen_policy,
        'totals': {
            'total': area_record(sum(sums)),
            'mean_side': area_record(sum(sums) / 2),
        },
        'numerical': {
            'relative_bound': VERIFICATION_RTOL,
            'absolute_bound_nm2': 0.0,
            'atomic_loss_status': statuses,
            'burial_usable': all(
                'inconsistent_negative' not in s for s in statuses.values()
            ),
            'clamped': False,
        },
        'calls': calls,
        'producer': {
            'bindingmt_version': __version__,
            'molsysmt_version': msm.__version__,
        },
        'resources': {
            'surface_evaluations_bound': work,
            'max_surface_evaluations': max_surface_evaluations,
            'estimated_sphere_buffer_bytes': n_sphere_points * 3 * 8,
            'estimated_composition_bytes': len(union) * 4096,
            'route': 'explicit_bruteforce_cartesian_cpu_one',
            'is_ram_reservation': False,
        },
        'model_resources': {
            path: hashlib.sha256(
                files('molsysmt').joinpath(path).read_bytes()
            ).hexdigest()
            for path in ('physchem/atoms/radius.py', 'lib/structure/sphere_points.py')
        },
        'attribution': {
            'implementation': 'MolSysMT native Shrake-Rupley SASA',
            'method_doi': '10.1016/0022-2836(73)90011-9',
            'radius_model': 'bundled element-vdW',
            'optional_provider_execution': False,
            'reference_program_execution': False,
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
    record['format_version'] = '0.3'
    record['analyses'] = {
        'surface': {
            'owner': 'bindingmt',
            'reference': {'analysis_id': analysis_id},
            'authority': 'bindingmt_calculated',
            'outcome': 'completed',
            'finding_refs': [
                {'analysis_id': analysis_id, 'result_kind': 'sasa_burial'}
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
