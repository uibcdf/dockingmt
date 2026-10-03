"""Validated score meaning and compact ranking evidence for result operations."""

import json
from collections.abc import Mapping
from copy import deepcopy
from math import isfinite

import pyunitwizard as puw

from dockingmt._private.serialization import validate_schema_version
from dockingmt._private.smonitor import ArgumentError


def _error(reason, score_name=None):
    return ArgumentError(
        arg_name='score_definitions', reason=reason, score_name=score_name
    )


def normalize_definitions(definitions, score_names):
    """Detach and validate descriptors; missing descriptors remain unknown."""
    if not isinstance(definitions, Mapping):
        raise _error('Use a mapping of score names to descriptors.')
    normalized = {}
    required = {
        'method',
        'method_version',
        'component',
        'kind',
        'unit',
        'preferred_direction',
        'context',
    }
    for name, definition in definitions.items():
        if name not in score_names:
            raise _error('A descriptor must refer to an existing score.', name)
        validate_schema_version(definition, 'ScoreDefinition')
        if set(definition) - {'schema_version'} != required:
            raise _error('Supply exactly the documented descriptor fields.', name)
        for field in ('method', 'method_version', 'component'):
            if not isinstance(definition[field], str) or not definition[field].strip():
                raise _error(f"Descriptor '{field}' must be a nonempty string.", name)
        if not isinstance(definition['kind'], str) or definition['kind'] not in (
            'empirical',
            'dimensionless',
        ):
            raise _error('Use empirical or dimensionless score meaning.', name)
        direction = definition['preferred_direction']
        if direction is not None and (
            not isinstance(direction, str) or direction not in ('lower', 'higher')
        ):
            raise _error('Use lower, higher or None for preferred direction.', name)
        unit = definition['unit']
        if not isinstance(unit, str) or not unit.strip():
            raise _error('Declare a nonempty unit string.', name)
        if definition['kind'] == 'dimensionless':
            if unit != 'dimensionless':
                raise _error('Dimensionless scores require unit dimensionless.', name)
        else:
            try:
                quantity = puw.quantity(1, unit)
                if not puw.are_compatible(quantity, 'kcal/mol'):
                    raise _error(
                        'Empirical scores require energy-per-mole units.', name
                    )
                unit = str(puw.get_unit(quantity))
            except ArgumentError:
                raise
            except Exception as exc:
                raise _error(
                    'The empirical unit must be recognized by PyUnitWizard.', name
                ) from exc
        context = definition['context']
        if not isinstance(context, dict) or not context:
            raise _error('Declare a nonempty JSON comparison context.', name)
        try:
            json.dumps(context, allow_nan=False)
        except (TypeError, ValueError, RecursionError) as exc:
            raise _error(
                'Context must contain finite, acyclic JSON values.', name
            ) from exc
        _check_json(context, name)
        normalized[name] = {
            'schema_version': '1.0',
            **deepcopy(dict(definition)),
            'unit': unit,
        }
    return normalized


def _check_json(value, score_name):
    if isinstance(value, dict):
        if any(not isinstance(key, str) or not key for key in value):
            raise _error('Context keys must be nonempty strings.', score_name)
        for item in value.values():
            _check_json(item, score_name)
    elif isinstance(value, list):
        for item in value:
            _check_json(item, score_name)
    elif value is not None and type(value) not in (str, bool, int, float):
        raise _error('Context must contain only JSON values.', score_name)
    elif type(value) is float and not isfinite(value):
        raise _error('Context must contain finite JSON values.', score_name)


def comparable_definition(poses, score_name):
    """Require identical declared semantics; never infer legacy meaning."""
    definitions = [pose.score_definitions.get(score_name) for pose in poses]
    if not definitions:
        return None
    signatures = {
        json.dumps(
            [definition, pose.partner_state_id, pose.receptor_state_id]
            if definition is not None
            else None,
            sort_keys=True,
            allow_nan=False,
        )
        for pose, definition in zip(poses, definitions)
    }
    if len(signatures) != 1:
        raise _error(
            'Ranking requires identical declared definitions and contexts, '
            'or an entirely undescribed legacy collection.',
            score_name,
        )
    return definitions[0]


def ranking_history(provenance, *, detach=True):
    """Return detached evidence; reject malformed history rather than erase it."""
    history = provenance.get('ranking_history', [])
    if not isinstance(history, list):
        raise ArgumentError(
            arg_name='ranking_history', reason='Use a list of ranking records.'
        )
    for entry in history:
        validate_schema_version(entry, 'RankingRecord')
        if (
            not isinstance(entry.get('score_name'), str)
            or not entry['score_name'].strip()
        ):
            raise ArgumentError(
                arg_name='ranking_history', reason='Declare a score name.'
            )
        if type(entry.get('ascending')) is not bool:
            raise ArgumentError(
                arg_name='ranking_history', reason='Declare a boolean direction.'
            )
        if entry.get('evidence') not in ('recorded', 'legacy_policy_only'):
            raise ArgumentError(
                arg_name='ranking_history', reason='Declare the evidence scope.'
            )
        if entry['evidence'] == 'recorded':
            _check_recorded_ranking(entry)
    return deepcopy(history) if detach else history


def _check_recorded_ranking(entry):
    from dockingmt.core.results import _normalize_score

    required = {
        'schema_version',
        'evidence',
        'origin',
        'score_name',
        'ascending',
        'score_definition',
        'input_order',
        'output_order',
    }
    if set(entry) != required or entry['origin'] not in ('rank_by', 'backend'):
        raise ArgumentError(
            arg_name='ranking_history',
            reason='Supply the documented recorded-ranking fields.',
        )
    observations = entry.get('input_order')
    order = entry.get('output_order')
    if (
        not isinstance(observations, list)
        or not isinstance(order, list)
        or any(type(index) is not int for index in order)
        or sorted(order) != list(range(len(observations)))
    ):
        raise ArgumentError(
            arg_name='ranking_history',
            reason='Output order must permute the recorded input indices.',
        )
    for observation in observations:
        if not isinstance(observation, dict) or set(observation) != {
            'pose_id',
            'partner_state_id',
            'receptor_state_id',
            'rank',
            'value',
        }:
            raise ArgumentError(
                arg_name='ranking_history', reason='Use structured pose observations.'
            )
        _normalize_score(observation.get('value'), entry['score_name'])
    definition = entry.get('score_definition')
    if definition is not None:
        normalize_definitions({entry['score_name']: definition}, {entry['score_name']})


def make_ranking_record(
    poses, score_name, ascending, definition, values, order, origin
):
    """Capture scalar evidence and indices without duplicating coordinates."""
    return {
        'schema_version': '1.0',
        'evidence': 'recorded',
        'origin': origin,
        'score_name': score_name,
        'ascending': ascending,
        'score_definition': deepcopy(definition),
        'input_order': deepcopy(
            [
                {
                    'pose_id': pose.pose_id,
                    'partner_state_id': pose.partner_state_id,
                    'receptor_state_id': pose.receptor_state_id,
                    'rank': pose.rank,
                    'value': value,
                }
                for pose, value in zip(poses, values)
            ]
        ),
        'output_order': list(order),
    }
