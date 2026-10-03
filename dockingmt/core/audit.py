"""Offline checks of evidence in the existing saved-result format."""

from collections.abc import Mapping

import numpy as np
import pyunitwizard as puw
from argdigest import arg_digest

from dockingmt._private.artifacts import inspect_artifact
from dockingmt._private.serialization import validate_schema_version
from dockingmt._private.smonitor import ArgumentError
from dockingmt._private.vina_records import score_components
from dockingmt.core._scores import normalize_definitions, ranking_history
from dockingmt.core.results import _normalize_scores


@arg_digest()
def verify_captured_inputs(artifacts):
    """Verify both captured PDBQT byte strings; return their sizes in bytes.

    Missing evidence and invalid bytes raise the local ArgumentError. This checks
    integrity against recorded hashes, not PDBQT syntax or chemical validity.
    """
    sizes = {}
    for role in ('receptor', 'partner'):
        status, reason, size = inspect_artifact(artifacts.get(role), role)
        if status != 'consistent':
            raise ArgumentError(arg_name='artifacts', reason=reason, role=role)
        sizes[role] = size
    return sizes


class _Report:
    def __init__(self):
        self.checks = []

    def add(self, check, path, status, reason):
        self.checks.append(
            {'check': check, 'path': path, 'status': status, 'reason': reason}
        )

    def validate(self, check, path, operation):
        try:
            value = operation()
        except (ArgumentError, TypeError, ValueError, KeyError, OverflowError):
            self.add(check, path, 'inconsistent', 'invalid_recorded_value')
            return False, None
        self.add(check, path, 'consistent', 'valid_recorded_value')
        return True, value

    def compare(self, check, path, actual, expected):
        if actual is None or expected is None:
            self.add(check, path, 'incomplete', 'comparison_evidence_missing')
        else:
            self.add(
                check,
                path,
                'consistent' if actual == expected else 'inconsistent',
                'claims_agree' if actual == expected else 'claims_disagree',
            )

    def export(self, scope='saved_result_internal_consistency'):
        statuses = {item['status'] for item in self.checks}
        status = next(
            item
            for item in ('inconsistent', 'incomplete', 'consistent')
            if item in statuses
        )
        return {
            'schema_version': '1.0',
            'scope': scope,
            'status': status,
            'checks': self.checks,
        }


def _schema(report, record, path, kind):
    valid, _ = report.validate(
        'schema', path, lambda: validate_schema_version(record, kind)
    )
    if valid and 'schema_version' not in record:
        report.add('schema_version', path, 'incomplete', 'legacy_version_implicit')
    return valid


def _length_values(record, shape, positive=False):
    if not isinstance(record, Mapping):
        raise ValueError('invalid_quantity_record')
    if not isinstance(record['unit'], str):
        raise ValueError('invalid_unit')
    try:
        quantity = puw.quantity(record['value'], record['unit'])
        if not puw.are_compatible(quantity, 'angstrom'):
            raise ValueError('length_units_required')
        values = np.asarray(puw.get_value(quantity, to_unit='angstrom'), dtype=float)
    except Exception as exc:
        # Unit backends have distinct parse and conversion exceptions.
        raise ValueError('invalid_length_quantity') from exc
    if (
        not np.isfinite(values).all()
        or values.shape != shape
        or (positive and np.any(values <= 0))
    ):
        raise ValueError('invalid_length_values')
    return values


def _box_values(box):
    return {
        key: _length_values(
            {'value': box[key], 'unit': box['unit']}, (3,), key == 'size'
        )
        for key in ('center', 'size')
    }


def _audit_vina(
    report, definition, name, provenance, path, *, stage='docking', components=None
):
    method = definition['method']
    if not method.startswith('AutoDock Vina/'):
        report.add(
            'score_provenance', path, 'incomplete', 'method_crosscheck_unavailable'
        )
        return
    protocol = provenance.get('protocol', {})
    if not isinstance(protocol, Mapping):
        report.add('score_provenance', path, 'inconsistent', 'invalid_protocol_record')
        return
    parameters = protocol.get('parameters', {})
    if not isinstance(parameters, Mapping):
        report.add(
            'score_provenance', path, 'inconsistent', 'invalid_protocol_parameters'
        )
        return
    scoring = parameters.get('scoring')
    report.compare('score_backend', path, provenance.get('backend'), 'vina')
    report.compare(
        'score_method', path, method, f'AutoDock Vina/{scoring}' if scoring else None
    )
    report.compare(
        'score_method_version',
        path,
        definition['method_version'],
        provenance.get('backend_version'),
    )
    if (
        definition['method_version'] == 'unknown'
        or provenance.get('backend_version') == 'unknown'
    ):
        report.add(
            'score_version_evidence', path, 'incomplete', 'method_version_unknown'
        )
    if scoring in ('vina', 'vinardo'):
        report.compare(
            'score_component',
            path,
            definition['component'],
            (score_components(scoring) if components is None else components).get(name),
        )
        report.compare('score_kind', path, definition['kind'], 'empirical')
        # The adapter records native numeric columns without converting energy.
        valid, value = report.validate(
            'score_native_unit',
            path,
            lambda: float(
                puw.get_value(puw.quantity(1, definition['unit']), to_unit='kcal/mol')
            ),
        )
        if valid:
            report.compare('score_native_scale', path, value, 1.0)
        # None is an explicit native declaration for component-only terms.
        total = (
            name == scoring if components is None else components.get(name) == 'total'
        )
        expected = 'lower' if total else None
        report.add(
            'score_preference',
            path,
            'consistent'
            if definition['preferred_direction'] == expected
            else 'inconsistent',
            'claims_agree'
            if definition['preferred_direction'] == expected
            else 'claims_disagree',
        )
    else:
        report.add(
            'score_scoring',
            path,
            'incomplete' if scoring is None else 'inconsistent',
            'native_scoring_unavailable',
        )
    context = definition['context']
    report.compare('score_stage', path, context.get('stage'), stage)
    if 'grid_spacing' not in context:
        report.add('score_grid_units', path, 'incomplete', 'grid_spacing_missing')
    else:
        report.validate(
            'score_grid_units',
            path,
            lambda: _length_values(context['grid_spacing'], (), positive=True),
        )
    if 'weights' not in context:
        report.add('score_weights', path, 'incomplete', 'weights_missing')
    else:

        def check_weights():
            weights = context['weights']
            if not isinstance(weights, list) or not weights:
                raise ValueError('invalid_weights')
            _normalize_scores({str(i): weight for i, weight in enumerate(weights)})

        report.validate('score_weights', path, check_weights)
    artifacts = provenance.get('backend_artifacts', {})
    preparation = provenance.get('preparation', {})
    for role in ('receptor', 'partner'):
        artifact = artifacts.get(role, {}) if isinstance(artifacts, Mapping) else {}
        assessment = (
            preparation.get(role, {}) if isinstance(preparation, Mapping) else {}
        )
        if stage == 'scoring':
            assessment = (
                assessment.get('assessment_report', {})
                if isinstance(assessment, Mapping)
                else {}
            )
        report.compare(
            'score_input_hash',
            f'{path}/{role}',
            context.get(f'{role}_sha256'),
            artifact.get('sha256') if isinstance(artifact, Mapping) else None,
        )
        declared = context.get('preparation_assessment', {})
        report.compare(
            'score_preparation',
            f'{path}/{role}',
            declared.get(role) if isinstance(declared, Mapping) else None,
            assessment.get('assessment') if isinstance(assessment, Mapping) else None,
        )
    boxes = (context.get('backend_box'), provenance.get('backend_box'))
    if any(box is None for box in boxes):
        report.add('score_box', path, 'incomplete', 'comparison_evidence_missing')
    else:
        valid, values = report.validate(
            'score_box_units', path, lambda: [_box_values(box) for box in boxes]
        )
        if valid:
            # Unit conversion roundoff only; this is not a geometric tolerance.
            agree = all(
                np.allclose(values[0][key], values[1][key], rtol=1e-12, atol=1e-12)
                for key in ('center', 'size')
            )
            report.add(
                'score_box',
                path,
                'consistent' if agree else 'inconsistent',
                'claims_agree' if agree else 'claims_disagree',
            )


def _audit_ranking(report, poses, definitions, provenance):
    path = '/provenance/ranking_history'
    if not provenance.get('ranking_history'):
        # An explicitly malformed container still needs the shared validator.
        if 'ranking_history' in provenance:
            report.validate(
                'ranking_history',
                path,
                lambda: ranking_history(provenance, detach=False),
            )
        report.add(
            'ranking_evidence', path, 'incomplete', 'ranking_observations_missing'
        )
        return
    valid, history = report.validate(
        'ranking_history', path, lambda: ranking_history(provenance, detach=False)
    )
    if not valid:
        return
    for index, entry in enumerate(history):
        entry_path = f'{path}/{index}'
        if entry['evidence'] != 'recorded':
            report.add(
                'ranking_evidence', entry_path, 'incomplete', 'legacy_policy_only'
            )
            continue
        observations = entry['input_order']
        expected = sorted(
            range(len(observations)),
            key=lambda i: observations[i]['value'],
            reverse=not entry['ascending'],
        )
        actual = entry['output_order']
        if entry['origin'] == 'backend':
            # Native ties carry no evidence of a tie-breaking algorithm.
            agree = [observations[i]['value'] for i in actual] == [
                observations[i]['value'] for i in expected
            ]
        else:
            agree = actual == expected
        report.add(
            'ranking_order',
            entry_path,
            'consistent' if agree else 'inconsistent',
            'order_matches_policy' if agree else 'order_contradicts_policy',
        )
        if index and history[index - 1]['evidence'] == 'recorded':
            previous = history[index - 1]
            keys = ('pose_id', 'partner_state_id', 'receptor_state_id')
            before = [
                tuple(previous['input_order'][i][key] for key in keys)
                for i in previous['output_order']
            ]
            after = [
                tuple(observation[key] for key in keys) for observation in observations
            ]
            if any(None in identity for identity in before + after):
                report.add(
                    'ranking_continuity',
                    entry_path,
                    'incomplete',
                    'identity_evidence_missing',
                )
            else:
                report.compare('ranking_continuity', entry_path, after, before)
    latest = history[-1]
    policy = provenance.get('ranking_policy')
    report.compare(
        'ranking_policy',
        '/provenance/ranking_policy',
        policy,
        {key: latest[key] for key in ('score_name', 'ascending')},
    )
    if latest['evidence'] != 'recorded':
        return
    projected = [latest['input_order'][i] for i in latest['output_order']]
    report.compare('ranking_membership', '/poses', len(poses), len(projected))
    for index, (pose, observation) in enumerate(zip(poses, projected)):
        path = f'/poses/{index}'
        if not isinstance(pose, Mapping):
            continue
        for key in ('pose_id', 'partner_state_id', 'receptor_state_id'):
            report.compare(
                'ranking_identity', f'{path}/{key}', pose.get(key), observation[key]
            )
        scores = pose.get('scores', {})
        report.compare(
            'ranking_value',
            path,
            scores.get(latest['score_name']) if isinstance(scores, Mapping) else None,
            observation['value'],
        )
        report.compare('ranking_rank', path, pose.get('rank'), index + 1)
        definition = definitions[index]
        if definition is not None:
            actual = definition.get(latest['score_name'])
            recorded = latest['score_definition']
            if actual is None and recorded is None:
                report.add(
                    'ranking_semantics', path, 'incomplete', 'score_meaning_missing'
                )
            else:
                normalized = (
                    normalize_definitions(
                        {latest['score_name']: recorded}, {latest['score_name']}
                    )[latest['score_name']]
                    if recorded is not None
                    else None
                )
                report.compare('ranking_semantics', path, actual, normalized)


def _audit_pose_payload(report, pose, path):
    if not _schema(report, pose, path, 'DockingPose'):
        return None, None, None
    coordinates = pose.get('coordinates')
    if (
        coordinates is None
        or isinstance(coordinates, Mapping)
        and 'unit' not in coordinates
    ):
        report.add(
            'coordinate_units', path, 'incomplete', 'explicit_length_unit_missing'
        )
    else:

        def check_coordinates():
            values = coordinates['value']
            shape = np.asarray(values).shape
            if len(shape) != 2 or shape[1] != 3:
                raise ValueError('invalid_coordinate_shape')
            return _length_values(coordinates, shape)

        report.validate('coordinate_units', path, check_coordinates)
    scores = pose.get('scores')
    if scores is None:
        report.add('scores', path, 'incomplete', 'scores_missing')
        return pose, None, None
    valid, scores = report.validate('scores', path, lambda: _normalize_scores(scores))
    if not valid:
        return pose, None, None
    metadata = pose.get('metadata', {})
    if not isinstance(metadata, Mapping):
        report.add('score_definitions', path, 'inconsistent', 'invalid_metadata')
        return pose, None, None
    valid, described = report.validate(
        'score_definitions',
        path,
        lambda: normalize_definitions(metadata.get('score_definitions', {}), scores),
    )
    if not valid:
        return pose, scores, None
    if not scores or set(scores) != set(described):
        report.add('score_meaning', path, 'incomplete', 'score_meaning_missing')
    return pose, scores, described


@arg_digest()
def audit_result(record):
    """Audit a saved mapping without files, molecular operations or a live engine.

    Return a detached JSON report with consistent, incomplete or inconsistent
    status. Contradictions take precedence over missing evidence. The report is
    an internal-consistency audit, not authentication or scientific qualification.
    Unsupported explicit schema versions are reported without interpreting them.
    """
    report = _Report()
    if not _schema(report, record, '/', 'DockingResult'):
        return report.export()
    poses = record.get('poses')
    provenance = record.get('provenance')
    if poses is None or provenance is None:
        report.add('result_payload', '/', 'incomplete', 'result_payload_missing')
    if not isinstance(poses, list) or not isinstance(provenance, Mapping):
        if (
            poses is not None
            and not isinstance(poses, list)
            or provenance is not None
            and not isinstance(provenance, Mapping)
        ):
            report.add('result_payload', '/', 'inconsistent', 'invalid_result_payload')
        return report.export()
    if not poses:
        report.add('pose_evidence', '/poses', 'incomplete', 'poses_missing')
    artifacts = provenance.get('backend_artifacts', {})
    if not isinstance(artifacts, Mapping):
        report.add(
            'captured_inputs',
            '/provenance/backend_artifacts',
            'inconsistent',
            'invalid_artifacts_record',
        )
        artifacts = {}
    for role in ('receptor', 'partner'):
        status, reason, _ = inspect_artifact(artifacts.get(role), role)
        report.add(
            'captured_input', f'/provenance/backend_artifacts/{role}', status, reason
        )
    report.compare(
        'protocol_snapshot',
        '/protocol_info',
        record.get('protocol_info'),
        provenance.get('protocol'),
    )
    definitions = []
    admitted_poses = []
    for index, pose in enumerate(poses):
        path = f'/poses/{index}'
        admitted, scores, described = _audit_pose_payload(report, pose, path)
        definitions.append(described)
        admitted_poses.append(admitted)
        if described is None:
            continue
        for name, definition in described.items():
            _audit_vina(report, definition, name, provenance, f'{path}/scores/{name}')
    _audit_ranking(report, admitted_poses, definitions, provenance)
    return report.export()
