"""Docking interpretation of MolSysMT's declared-state pose geometry."""

from copy import deepcopy

import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.results import _atom_key, _molecular_atom_keys


def evaluate_symmetry(result, reference, reference_selection, report, options):
    """Retain the positional report and independently evaluate admitted maps.

    The caller supplies a complete query chemical context. Only measured pose
    coordinates are set through MolSysMT; unselected context coordinates are not
    presented as reconstructed pose geometry. MolSysMT owns graph admission,
    correspondence enumeration, numerical geometry and their failure semantics.
    """
    import molsysmt as msm

    options = dict(options)
    context = options.pop('molecular_system', None)
    allowed = {
        'chemical_state',
        'reference_chemical_state',
        'method',
        'max_matches',
        'tie_tolerance',
    }
    if context is None or set(options) - allowed:
        raise ArgumentError(
            arg_name='symmetry_options',
            reason=(
                'Supply molecular_system as the complete declared query chemical '
                'context, plus supported MolSysMT state/method/bound/tolerance options.'
            ),
        )
    if not result.poses:
        raise ArgumentError(
            arg_name='result',
            reason='Symmetry evaluation needs a mapped pose population.',
        )
    if not hasattr(msm.structure, 'get_symmetry_corrected_rmsd'):
        raise ArgumentError(
            arg_name='symmetry_options',
            reason='Use a qualified MolSysMT provider delivering molsysmt#310.',
        )
    source = msm.convert(context, to_form='molsysmt.MolSys')
    if msm.get(source, n_structures=True) != 1:
        raise ArgumentError(
            arg_name='symmetry_options', reason='Use one query-context structure.'
        )
    source_keys = _molecular_atom_keys(source)
    reference_keys = _molecular_atom_keys(reference)
    query_lookup = {_atom_key(key): i for i, key in enumerate(source_keys)}
    reference_lookup = {_atom_key(reference_keys[i]): i for i in reference_selection}
    pose_keys = result.poses[0]._verified_atom_keys()
    population = {_atom_key(key) for key in pose_keys}
    if (
        len(query_lookup) != len(source_keys)
        or not population.issubset(query_lookup)
        or not population.issubset(reference_lookup)
    ):
        raise ArgumentError(
            arg_name='symmetry_options',
            reason='Query context and reference must retain the verified pose identities.',
        )
    selected = sorted(query_lookup[key] for key in population)
    baseline = [[i, reference_lookup[_atom_key(source_keys[i])]] for i in selected]
    correspondence_options = {
        name: value for name, value in options.items() if name != 'tie_tolerance'
    }
    maps = msm.chemical_states.get_atom_correspondences(
        source,
        selection=selected,
        reference_molecular_system=reference,
        reference_selection=[pair[1] for pair in baseline],
        **correspondence_options,
    )
    rows = []
    geometry = None
    for pose, original in zip(result.poses, report['poses'], strict=True):
        lookup = {_atom_key(key): i for i, key in enumerate(pose._verified_atom_keys())}
        order = [lookup[_atom_key(source_keys[i])] for i in selected]
        coordinates = puw.get_value(pose.coordinates, to_unit='angstrom')[order]
        query = msm.copy(source)
        msm.set(
            query,
            selection=selected,
            coordinates=puw.quantity(coordinates[None], 'angstrom'),
        )
        geometry = msm.structure.get_symmetry_corrected_rmsd(
            query,
            selection=selected,
            reference_molecular_system=reference,
            reference_selection=[pair[1] for pair in baseline],
            baseline_atom_correspondence=baseline,
            correspondences=maps,
            **options,
        )
        raw = float(puw.get_value(geometry['raw_rmsd'], to_unit='angstrom')[0])
        corrected = float(puw.get_value(geometry['rmsd'], to_unit='angstrom')[0])
        if (
            not np.isfinite(raw)
            or not np.isfinite(corrected)
            or corrected < 0
            or not np.isclose(raw, original['rmsd'], rtol=0, atol=1e-10)
        ):
            raise ArgumentError(
                arg_name='result',
                reason='Symmetry geometry must retain the original positional baseline.',
            )
        rows.append(
            {
                'position': original['position'],
                'pose_id': original['pose_id'],
                'rank': original['rank'],
                'raw_rmsd': raw,
                'rmsd': corrected,
                'recovered': corrected <= report['criterion']['cutoff'],
                'correspondence_index': int(geometry['correspondence_indices'][0]),
                'n_near_optimal_correspondences': int(
                    geometry['n_near_optimal_correspondences'][0]
                ),
            }
        )
    # This provider schema's top-level arrays are explicitly unitless index maps.
    mapping_record = {
        key: value.tolist() if isinstance(value, np.ndarray) else deepcopy(value)
        for key, value in maps.items()
    }
    return {
        'schema_version': '1.0',
        'criterion': {
            'metric': 'chemically_constrained_positional_rmsd',
            'unit': 'angstrom',
            'cutoff': report['criterion']['cutoff'],
            'comparison': '<=',
            'alignment': geometry['alignment'],
            'periodic_imaging': geometry['periodic_imaging'],
            'symmetry_correction': geometry['method'],
            'search_scope': geometry['search_scope'],
            'atom_scope': 'retained_pose_atoms',
            'coordinate_frame': 'caller_declared_shared_receptor_frame',
            'chemical_context': 'caller_declared_query_and_reference',
            'unselected_coordinates': 'unchanged_context_not_pose_geometry',
            'baseline_tolerance_angstrom': 1e-10,
            'tie_tolerance_angstrom': float(
                puw.get_value(geometry['tie_tolerance'], to_unit='angstrom')
            ),
            'top_n_basis': 'result_order',
        },
        'correspondences': mapping_record,
        'baseline_atom_correspondence': baseline,
        'poses': rows,
        'n_poses': len(rows),
        'first_pose': deepcopy(rows[0]),
        'closest_pose': deepcopy(min(rows, key=lambda row: row['rmsd'])),
        'top_n': [
            {
                'requested': item['requested'],
                'considered': item['considered'],
                'recovered': any(row['recovered'] for row in rows[: item['requested']]),
            }
            for item in report['top_n']
        ],
        'evaluator': {
            'rmsd_function': 'molsysmt.structure.get_symmetry_corrected_rmsd',
            'software': deepcopy(geometry['software']),
            'references': deepcopy(geometry.get('references', [])),
            'attribution': deepcopy(geometry.get('attribution')),
        },
    }
