"""Value contracts for the current docking and preparation entry points.

Molecular forms and selection syntax are delegated unchanged to MolSysMT.
Only absence is checked here; recognition and extraction stay in the provider.
"""

from collections.abc import Iterable, Mapping, Set
from numbers import Integral
from pathlib import Path

import numpy as np
import pyunitwizard as puw
from argdigest.core.caller import caller_is_one_of

from bindingmt._private.smonitor import ArgumentError

_PREPARED_CONSTRUCTORS = (
    'bindingmt.preparation.ligand.PreparedLigand.__init__',
    'bindingmt.preparation.receptor.PreparedReceptor.__init__',
)
_OUTCOME_CONSTRUCTOR = 'bindingmt.core.outcome.DockingOutcome.__init__'
_RMSD_HELPERS = (
    'bindingmt.core.results.DockingPose.get_rmsd',
    'bindingmt.core.results.DockingResult.get_rmsds',
)


def _invalid(argument, caller, reason):
    return ArgumentError(arg_name=argument, caller=caller, reason=reason)


def _integer(argument, minimum=None, optional=False):
    def digest(value, caller=None):
        if value is None and optional:
            return None
        if isinstance(value, bool) or not isinstance(value, Integral):
            raise _invalid(
                argument, caller, 'Use an integer; coercion is not supported.'
            )
        if minimum is not None and value < minimum:
            raise _invalid(argument, caller, f'Use an integer >= {minimum}.')
        return int(value)

    return digest


def _boolean(argument):
    def digest(value, caller=None):
        if not isinstance(value, bool):
            raise _invalid(argument, caller, 'Use a bool.')
        return value

    return digest


def digest_energy_range(energy_range, caller=None):
    if energy_range is None:
        energy_range = puw.quantity(3.0, 'kcal/mol')
    try:
        quantity = puw.ensure_quantity(
            energy_range,
            dimensionality=puw.get_dimensionality(puw.unit('kcal/mol')),
            to_unit='kcal/mol',
            standardized=False,
            caller=caller,
        )
    except MemoryError:
        raise
    except Exception as exc:
        # Unit forms and parsers have provider-specific exceptions. Preserve the
        # original cause while presenting the local public argument contract.
        raise _invalid(
            'energy_range',
            caller,
            'Use an energy-per-mole quantity with explicit units.',
        ) from exc
    values = np.asarray(puw.get_value(quantity))
    if (
        values.shape != ()
        or not np.issubdtype(values.dtype, np.number)
        or not np.isrealobj(values)
        or not np.isfinite(values).all()
        or values < 0
    ):
        raise _invalid(
            'energy_range', caller, 'Use a finite non-negative scalar energy.'
        )
    return quantity


def digest_problem(problem, caller=None, native_constructor=None, native_view=None):
    from bindingmt.core.problem import DockingProblem

    if native_view == 'bindingmt.view.view':
        return _view_option(problem, 'problem', DockingProblem, 'search_domain')
    if problem is None and caller_is_one_of(
        native_constructor, ['bindingmt.core.results.DockingResult.__init__']
    ):
        return None
    if not isinstance(problem, DockingProblem):
        raise _invalid('problem', caller, 'Use a DockingProblem instance.')
    return problem


def digest_problems(problems, caller=None):
    if isinstance(problems, (str, bytes, Mapping)) or not isinstance(
        problems, Iterable
    ):
        raise _invalid(
            'problems', caller, 'Use an iterable of prepared DockingProblem instances.'
        )
    return problems


def digest_on_error(on_error, caller=None):
    if not isinstance(on_error, str) or on_error not in ('raise', 'record'):
        raise _invalid('on_error', caller, "Use 'raise' or 'record'.")
    return on_error


def digest_prepared(prepared, caller=None):
    from bindingmt.preparation.ligand import PreparedLigand
    from bindingmt.preparation.receptor import PreparedReceptor

    if not isinstance(
        prepared, (PreparedLigand, PreparedReceptor, str, Path)
    ) and not callable(getattr(prepared, 'to_pdbqt', None)):
        raise _invalid(
            'prepared',
            caller,
            'Use a PreparedLigand, PreparedReceptor or external PDBQT representation.',
        )
    return prepared


def digest_protocol(protocol, caller=None):
    from bindingmt.core.protocol import DockingProtocol

    if protocol is not None and not isinstance(protocol, DockingProtocol):
        raise _invalid('protocol', caller, 'Use a DockingProtocol instance or None.')
    return protocol


def digest_backend(backend, caller=None, native_constructor=None):
    if caller_is_one_of(native_constructor, [_OUTCOME_CONSTRUCTOR]):
        # An outcome records an adapter's label; it does not resolve execution.
        if backend is not None and (
            not isinstance(backend, str) or not backend.strip()
        ):
            raise _invalid('backend', caller, 'Use an adapter name or None.')
        return backend
    from bindingmt.engines.base import DockingBackend

    if backend is None or isinstance(backend, DockingBackend):
        return backend
    if isinstance(backend, str) and backend.lower() == 'vina':
        return backend.lower()
    raise _invalid('backend', caller, "Use a DockingBackend instance, 'vina', or None.")


def digest_scoring(scoring, caller=None):
    from bindingmt.core.protocol import VinaProtocol

    if not isinstance(scoring, str) or scoring not in VinaProtocol.SUPPORTED_SCORING:
        raise _invalid(
            'scoring', caller, f'Use one of {VinaProtocol.SUPPORTED_SCORING}.'
        )
    return scoring


def _required_provider_input(argument):
    def digest(value, caller=None):
        if value is None:
            raise _invalid(argument, caller, 'Supply an input supported by MolSysMT.')
        return value

    return digest


def digest_state_id(state_id, caller=None, native_constructor=None):
    required = caller_is_one_of(native_constructor, _PREPARED_CONSTRUCTORS)
    if state_id is None and not required:
        return None
    if not isinstance(state_id, str) or not state_id.strip():
        reason = (
            'Use a nonempty string.' if required else 'Use a nonempty string or None.'
        )
        raise _invalid('state_id', caller, reason)
    return state_id


def digest_active_torsion_bonds(active_torsion_bonds, caller=None):
    if active_torsion_bonds is None:
        return None
    if not isinstance(active_torsion_bonds, (list, tuple)) or any(
        not isinstance(pair, (list, tuple))
        or len(pair) != 2
        or any(
            isinstance(i, bool) or not isinstance(i, Integral) or i < 0 for i in pair
        )
        for pair in active_torsion_bonds
    ):
        raise _invalid(
            'active_torsion_bonds',
            caller,
            'Use pairs of non-negative integer atom indices.',
        )
    # Chemical eligibility and source-index bounds are checked during preparation.
    return [tuple(int(i) for i in pair) for pair in active_torsion_bonds]


def _box_vector(argument, optional=False, positive=False):
    def digest(value, caller=None):
        if value is None and optional:
            return None
        from bindingmt.core.search_domain import _ensure_length_quantity_1d

        quantity = _ensure_length_quantity_1d(value, argument, caller=caller)
        if positive and np.any(puw.get_value(quantity) <= 0):
            raise _invalid(
                argument, caller, 'All box dimensions must be strictly positive (> 0).'
            )
        return quantity

    return digest


def digest_name(name, caller=None):
    if name is not None and not isinstance(name, str):
        raise _invalid('name', caller, 'Use a string or None.')
    return name


def digest_score_name(score_name, caller=None):
    if not isinstance(score_name, str) or not score_name.strip():
        raise _invalid('score_name', caller, 'Use a nonempty score name string.')
    return score_name


def digest_result(result, caller=None, native_view=None, native_constructor=None):
    from bindingmt.core.results import DockingResult

    if native_view == 'bindingmt.view.view':
        return _view_option(result, 'result', DockingResult, 'poses')
    if result is None and caller_is_one_of(native_constructor, [_OUTCOME_CONSTRUCTOR]):
        return None
    if not isinstance(result, DockingResult):
        raise _invalid('result', caller, 'Use a DockingResult instance.')
    return result


def digest_outcome_index(index, caller=None):
    # Preserve the serialized outcome's existing built-in-int contract.
    if type(index) is not int or index < 0:
        raise _invalid('index', caller, 'Use a non-negative integer.')
    return index


def digest_outcome_error(error, caller=None):
    if error is not None and (
        not isinstance(error, Mapping)
        or set(error) != {'type', 'message', 'code'}
        or not isinstance(error['type'], str)
        or not error['type'].strip()
        or not isinstance(error['message'], str)
        or error['code'] is not None
        and (not isinstance(error['code'], str) or not error['code'].strip())
    ):
        raise _invalid('error', caller, 'Use a typed error summary.')
    return error


def digest_rmsd_cutoff(rmsd_cutoff, caller=None):
    try:
        quantity = puw.ensure_quantity(
            rmsd_cutoff,
            dimensionality={'[L]': 1},
            to_unit='angstrom',
            standardized=False,
            caller=caller,
        )
    except MemoryError:
        raise
    except Exception as exc:
        raise _invalid(
            'rmsd_cutoff', caller, 'Use a scalar length with explicit units.'
        ) from exc
    values = np.asarray(puw.get_value(quantity))
    if (
        values.shape != ()
        or not np.issubdtype(values.dtype, np.number)
        or not np.isrealobj(values)
        or not np.isfinite(values).all()
        or values < 0
    ):
        raise _invalid(
            'rmsd_cutoff', caller, 'Use a finite non-negative scalar length.'
        )
    return quantity


def digest_top_n(top_n, caller=None):
    if not isinstance(top_n, (list, tuple)) or not top_n:
        raise _invalid(
            'top_n', caller, 'Use a nonempty list or tuple of positive integers.'
        )
    digest = _integer('top_n', minimum=1)
    values = [digest(value, caller) for value in top_n]
    if len(set(values)) != len(values):
        raise _invalid('top_n', caller, 'Supply each top-N position count only once.')
    return values


def digest_reference_info(reference_info, caller=None):
    if reference_info is not None and not isinstance(reference_info, Mapping):
        raise _invalid('reference_info', caller, 'Use a finite JSON mapping or None.')
    return reference_info


def digest_failures(failures, caller=None):
    if failures is not None and not isinstance(failures, Mapping):
        raise _invalid('failures', caller, 'Use a case-ID mapping or None.')
    return failures


def digest_pose(pose, caller=None):
    from bindingmt.core.results import DockingPose

    if pose is not None and not isinstance(pose, DockingPose):
        raise _invalid('pose', caller, 'Use a DockingPose instance or None.')
    return pose


def digest_scores(scores, caller=None, native_constructor=None):
    from bindingmt.core.results import _normalize_scores

    if scores is None and caller_is_one_of(
        native_constructor, ['bindingmt.core.results.DockingPose.__init__']
    ):
        return {}
    if not isinstance(scores, Mapping):
        raise _invalid('scores', caller, 'Use a mapping of named finite scores.')
    return _normalize_scores(scores)


def digest_coordinates(coordinates, caller=None, native_constructor=None):
    if caller_is_one_of(native_constructor, _PREPARED_CONSTRUCTORS):
        # Prepared declarations can be assessed without coordinates. Molecular
        # values and representation validation stay with the MolSysMT consumer.
        return coordinates
    # Pose-record numerical admission, not molecular-system interpretation.
    from bindingmt.core.results import _ensure_coordinates_quantity

    return _ensure_coordinates_quantity(coordinates)


def digest_poses(poses, caller=None):
    from bindingmt.core.results import DockingPose

    if isinstance(poses, (str, bytes, Mapping, Set)) or not isinstance(poses, Iterable):
        raise _invalid(
            'poses', caller, 'Use an ordered iterable of DockingPose instances.'
        )
    values = list(poses)
    if any(not isinstance(pose, DockingPose) for pose in values):
        raise _invalid(
            'poses', caller, 'Use an ordered iterable of DockingPose instances.'
        )
    return values


def _optional_mapping(argument):
    def digest(value, caller=None):
        if value is not None and not isinstance(value, Mapping):
            raise _invalid(argument, caller, 'Use a mapping or None.')
        return value

    return digest


def _optional_string(argument):
    def digest(value, caller=None):
        if value is not None and not isinstance(value, str):
            raise _invalid(argument, caller, 'Use a string or None.')
        return value

    return digest


def digest_search_domain(search_domain, caller=None, native_view=None):
    from bindingmt.core.search_domain import SearchDomain

    if native_view == 'bindingmt.view.view':
        return _view_option(
            search_domain,
            'search_domain',
            SearchDomain,
            'bounds',
            'as_box_approximation',
        )
    if not isinstance(search_domain, SearchDomain):
        raise _invalid('search_domain', caller, 'Use a SearchDomain instance.')
    return search_domain


def _optional_guidance(argument):
    def digest(value, caller=None):
        if value is not None and not isinstance(value, (list, Mapping)):
            raise _invalid(argument, caller, 'Use a list, mapping, or None.')
        return value

    return digest


def _problem_input(value, argument, caller, record_factory):
    if value is None and record_factory is not True:
        raise _invalid(argument, caller, 'Supply an input supported by MolSysMT.')
    return value


def digest_receptor(receptor, caller=None, record_factory=None):
    return _problem_input(receptor, 'receptor', caller, record_factory)


def digest_partner(partner, caller=None, record_factory=None):
    return _problem_input(partner, 'partner', caller, record_factory)


def _provider_owned(value):
    """Leave molecular selection/state semantics to the existing MolSysMT route."""
    return value


def digest_selection(selection, caller=None, native_factory=None, native_helper=None):
    if caller_is_one_of(native_helper, _RMSD_HELPERS):
        # MolSysMT owns selection values, including its handling of None.
        return selection
    if selection is None and not caller_is_one_of(
        native_factory, ['bindingmt.core.search_domain.BoxRegion.from_selection']
    ):
        raise _invalid('selection', caller, 'Supply an input supported by MolSysMT.')
    return selection


def digest_backend_unit(unit, caller=None):
    reason = 'Use an explicit length unit supported by PyUnitWizard.'
    if unit is None:
        raise _invalid('unit', caller, reason)
    try:
        valid = puw.is_unit(unit) and puw.check(unit, dimensionality={'[L]': 1})
    except MemoryError:
        raise
    except Exception as exc:
        raise _invalid('unit', caller, reason) from exc
    if not valid:
        raise _invalid('unit', caller, reason)
    # Retain the caller's unit representation; conversion stays in PyUnitWizard.
    return unit


def digest_padding(padding, caller=None):
    if padding is None:
        return None
    from bindingmt.core.search_domain import _ensure_scalar_length_quantity

    quantity = _ensure_scalar_length_quantity(padding, 'padding')
    if puw.get_value(quantity) < 0:
        raise _invalid('padding', caller, 'padding must be non-negative (>= 0).')
    return quantity


def digest_points(points, caller=None):
    from bindingmt.core.search_domain import _ensure_length_quantity

    quantity = _ensure_length_quantity(points, 'points', caller=caller)
    values = puw.get_value(quantity)
    if values.ndim != 2 or values.shape[1:] != (3,) or values.shape[0] == 0:
        raise _invalid('points', caller, 'Use a non-empty array of shape (N, 3).')
    return quantity


def digest_score_definitions(score_definitions, caller=None):
    if score_definitions is not None and not isinstance(score_definitions, Mapping):
        raise _invalid('score_definitions', caller, 'Use a descriptor mapping or None.')
    return score_definitions


def _mapping(argument):
    def digest(value, caller=None):
        if not isinstance(value, Mapping):
            raise _invalid(argument, caller, 'Use a mapping containing a saved record.')
        return value

    return digest


def _optional_provider_options(argument):
    def digest(value, caller=None):
        if value is None:
            return None
        if not isinstance(value, Mapping):
            raise _invalid(argument, caller, 'Use a provider-option mapping or None.')
        return dict(value)

    return digest


def _prepared_sequence(argument):
    def digest(value, caller=None):
        if isinstance(value, (str, bytes, Mapping, Set)) or not isinstance(
            value, Iterable
        ):
            raise _invalid(
                argument, caller, 'Use an ordered iterable of declared values.'
            )
        # Preserve the supplied axis. Do not classify labels, inspect source
        # atoms, assign charges or validate molecular representation here.
        return list(value)

    return digest


def digest_group_names(group_names, caller=None, native_constructor=None):
    if group_names is None and caller_is_one_of(
        native_constructor, _PREPARED_CONSTRUCTORS[:1]
    ):
        return None
    return _prepared_sequence('group_names')(group_names, caller)


def digest_group_ids(group_ids, caller=None, native_constructor=None):
    if group_ids is None and caller_is_one_of(
        native_constructor, _PREPARED_CONSTRUCTORS[:1]
    ):
        return None
    return _prepared_sequence('group_ids')(group_ids, caller)


def digest_group_name(group_name, caller=None):
    if not isinstance(group_name, str):
        raise _invalid('group_name', caller, 'Use a string.')
    return group_name


def digest_torsion_dof(torsion_dof, caller=None, native_constructor=None):
    optional = not caller_is_one_of(native_constructor, _PREPARED_CONSTRUCTORS)
    return _integer('torsion_dof', minimum=0, optional=optional)(torsion_dof, caller)


def digest_torsion_tree(value, caller=None):
    from bindingmt.preparation._temporary_torsions import TorsionTree

    if value is not None and not isinstance(value, TorsionTree):
        raise _invalid('_torsion_tree', caller, 'Use a declared TorsionTree or None.')
    return value


def _view_option(value, argument, model, *attributes):
    if (
        value is None
        or isinstance(value, model)
        or any(hasattr(value, attribute) for attribute in attributes)
    ):
        return value
    raise _invalid(argument, 'bindingmt.view.view', f'Use a {model.__name__} or None.')


def digest_view_item(item, caller=None):
    from bindingmt.core.problem import DockingProblem
    from bindingmt.core.results import DockingResult
    from bindingmt.core.search_domain import SearchDomain
    from bindingmt.interactions import PoseInteractions

    if item is None or isinstance(
        item, (DockingResult, DockingProblem, SearchDomain, PoseInteractions)
    ):
        return item
    if any(hasattr(item, name) for name in ('poses', 'search_domain', 'bounds')):
        return item
    raise _invalid(
        'item',
        'bindingmt.view.view',
        'Use a docking result, interaction binding, problem, search domain, or None.',
    )


def digest_pose_rank(pose_rank, caller=None, native_view=None):
    return _integer('pose_rank', minimum=1)(pose_rank, native_view or caller)


def digest_pose_atom_indices(pose_atom_indices, caller=None):
    if isinstance(pose_atom_indices, (str, bytes, Mapping, Set)) or not isinstance(
        pose_atom_indices, Iterable
    ):
        raise _invalid(
            'pose_atom_indices', caller, 'Supply an ordered sequence of atom indices.'
        )
    indices = tuple(pose_atom_indices)
    if not indices or any(
        isinstance(index, bool) or not isinstance(index, Integral) or index < 0
        for index in indices
    ):
        raise _invalid('pose_atom_indices', caller, 'Use non-negative integer indices.')
    if len(set(indices)) != len(indices):
        raise _invalid('pose_atom_indices', caller, 'Atom indices must be unique.')
    return tuple(int(index) for index in indices)


def digest_coordinate_tolerance(coordinate_tolerance, caller=None):
    if coordinate_tolerance is None:
        coordinate_tolerance = puw.quantity(1e-12, 'angstrom')
    try:
        quantity = puw.ensure_quantity(
            coordinate_tolerance,
            dimensionality=puw.get_dimensionality(puw.unit('angstrom')),
            to_unit='angstrom',
            standardized=False,
            caller=caller,
        )
    except MemoryError:
        raise
    except Exception as exc:
        raise _invalid(
            'coordinate_tolerance', caller, 'Supply a length with explicit units.'
        ) from exc
    value = np.asarray(puw.get_value(quantity))
    if (
        value.shape != ()
        or not np.issubdtype(value.dtype, np.number)
        or not np.isrealobj(value)
        or not np.isfinite(value).all()
        or value < 0
    ):
        raise _invalid(
            'coordinate_tolerance', caller, 'Use a finite non-negative scalar length.'
        )
    return quantity


ARGUMENT_DIGESTERS = {
    'cutoff': _provider_owned,
    'source_id': _optional_string('source_id'),
    'source_structure_index': _integer(
        'source_structure_index', minimum=0, optional=True
    ),
    'max_dense_pairs': _integer('max_dense_pairs', minimum=1),
    'atom_map': _optional_mapping('atom_map'),
    'participant': _optional_string('participant'),
    'question': _mapping('question'),
    'participants': _mapping('participants'),
    'grouping': _provider_owned,
    'analyses': _optional_mapping('analyses'),
    'contexts': _optional_mapping('contexts'),
    'site_refs': _provider_owned,
    'claim_status': _optional_string('claim_status'),
    'assurance_scope': _optional_string('assurance_scope'),
    'context_policy': _optional_string('context_policy'),
    'extensions': _optional_mapping('extensions'),
    'experimental': _boolean('experimental'),
    'path': _provider_owned,
    'reason': _optional_string('reason'),
    'unit': digest_backend_unit,
    'index': digest_outcome_index,
    'error': digest_outcome_error,
    'item': digest_view_item,
    'pose_rank': digest_pose_rank,
    'pose_index': _integer('pose_index', minimum=0),
    'pose_atom_indices': digest_pose_atom_indices,
    'coordinate_tolerance': digest_coordinate_tolerance,
    'assume_aligned': _boolean('assume_aligned'),
    'atom_names': _prepared_sequence('atom_names'),
    'atom_types': _prepared_sequence('atom_types'),
    'charges': _prepared_sequence('charges'),
    'group_names': digest_group_names,
    'group_ids': digest_group_ids,
    'group_name': digest_group_name,
    'source_molsys': _provider_owned,
    '_torsion_tree': digest_torsion_tree,
    'data': _mapping('data'),
    'coordinates': digest_coordinates,
    'poses': digest_poses,
    'rank': _integer('rank', minimum=1, optional=True),
    'pose_id': _optional_string('pose_id'),
    'partner_state_id': _optional_string('partner_state_id'),
    'receptor_state_id': _optional_string('receptor_state_id'),
    'metadata': _optional_mapping('metadata'),
    'problem_info': _optional_mapping('problem_info'),
    'protocol_info': _optional_mapping('protocol_info'),
    'provenance': _optional_mapping('provenance'),
    'search_domain': digest_search_domain,
    'constraints': _optional_guidance('constraints'),
    'search_guidance': _optional_guidance('search_guidance'),
    'receptor': digest_receptor,
    'partner': digest_partner,
    'complex_system': _required_provider_input('complex_system'),
    'receptor_selection': _provider_owned,
    'partner_selection': _provider_owned,
    'receptor_structure_index': _provider_owned,
    'partner_structure_index': _provider_owned,
    'structure_index': _provider_owned,
    'structure_indices': _provider_owned,
    'chemical_state': _provider_owned,
    'min_coords': _box_vector('min_coords'),
    'max_coords': _box_vector('max_coords'),
    'points': digest_points,
    'padding': digest_padding,
    'symmetry_options': _optional_provider_options('symmetry_options'),
    'hydrogen_options': _optional_provider_options('hydrogen_options'),
    'charge_options': _optional_provider_options('charge_options'),
    'typing_options': _optional_provider_options('typing_options'),
    'evaluations': _mapping('evaluations'),
    'failures': digest_failures,
    'result': digest_result,
    'reference': _required_provider_input('reference'),
    'reference_info': digest_reference_info,
    'rmsd_cutoff': digest_rmsd_cutoff,
    'top_n': digest_top_n,
    'problems': digest_problems,
    'on_error': digest_on_error,
    'pose': digest_pose,
    'scores': digest_scores,
    'score_definitions': digest_score_definitions,
    'prepared': digest_prepared,
    'record': _mapping('record'),
    'artifacts': _mapping('artifacts'),
    'score_name': digest_score_name,
    'ascending': _boolean('ascending'),
    'center': _box_vector('center'),
    'lengths': _box_vector('lengths', optional=True, positive=True),
    'size': _box_vector('size', optional=True, positive=True),
    'point': _box_vector('point'),
    'name': digest_name,
    'problem': digest_problem,
    'protocol': digest_protocol,
    'backend': digest_backend,
    'exhaustiveness': _integer('exhaustiveness', minimum=1),
    'n_poses': _integer('n_poses', minimum=1),
    'energy_range': digest_energy_range,
    'seed': _integer('seed', optional=True),
    'scoring': digest_scoring,
    'cpu': _integer('cpu', minimum=0),
    'allow_provisional_preparation': _boolean('allow_provisional_preparation'),
    'capture_backend_inputs': _boolean('capture_backend_inputs'),
    'collect_timings': _boolean('collect_timings'),
    'active_torsion_bonds': digest_active_torsion_bonds,
    'molecular_system': _required_provider_input('molecular_system'),
    'selection': digest_selection,
    'state_id': digest_state_id,
    'torsion_dof': digest_torsion_dof,
}
