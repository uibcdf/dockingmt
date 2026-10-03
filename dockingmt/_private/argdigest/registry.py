"""Value contracts for the current docking and preparation entry points.

Molecular forms and selection syntax are delegated unchanged to MolSysMT.
Only absence is checked here; recognition and extraction stay in the provider.
"""

from collections.abc import Mapping
from numbers import Integral

import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError


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


def digest_problem(problem, caller=None):
    from dockingmt.core.problem import DockingProblem

    if not isinstance(problem, DockingProblem):
        raise _invalid('problem', caller, 'Use a DockingProblem instance.')
    return problem


def digest_protocol(protocol, caller=None):
    from dockingmt.core.protocol import DockingProtocol

    if protocol is not None and not isinstance(protocol, DockingProtocol):
        raise _invalid('protocol', caller, 'Use a DockingProtocol instance or None.')
    return protocol


def digest_backend(backend, caller=None):
    from dockingmt.engines.base import DockingBackend

    if backend is None or isinstance(backend, DockingBackend):
        return backend
    if isinstance(backend, str) and backend.lower() == 'vina':
        return backend.lower()
    raise _invalid('backend', caller, "Use a DockingBackend instance, 'vina', or None.")


def digest_scoring(scoring, caller=None):
    from dockingmt.core.protocol import VinaProtocol

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


def digest_state_id(state_id, caller=None):
    if state_id is not None and (not isinstance(state_id, str) or not state_id.strip()):
        raise _invalid('state_id', caller, 'Use a nonempty string or None.')
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
        from dockingmt.core.search_domain import _ensure_length_quantity_1d

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


def _mapping(argument):
    def digest(value, caller=None):
        if not isinstance(value, Mapping):
            raise _invalid(argument, caller, 'Use a mapping containing a saved record.')
        return value

    return digest


ARGUMENT_DIGESTERS = {
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
    'selection': _required_provider_input('selection'),
    'state_id': digest_state_id,
    'torsion_dof': _integer('torsion_dof', minimum=0, optional=True),
}
