"""Offline crosschecks of standalone pose and scoring-evaluation records."""

import json
from collections.abc import Mapping

from argdigest import arg_digest

from dockingmt._private.artifacts import inspect_artifact
from dockingmt._private.vina_records import fixed_score_components
from dockingmt.core._scores import normalize_definitions
from dockingmt.core.audit import (
    _audit_pose_payload,
    _audit_vina,
    _length_values,
    _Report,
    _schema,
)
from dockingmt.core.protocol import VinaProtocol
from dockingmt.core.results import _normalize_scores
from dockingmt.preparation.assessment import _assessment_from_sources


def _mapping(report, record, key, path):
    if key not in record:
        report.add(key, path, 'incomplete', 'recorded_evidence_missing')
        return {}
    value = record[key]
    if not isinstance(value, Mapping):
        report.add(key, path, 'inconsistent', 'invalid_recorded_container')
        return {}
    return value


def _protocol(report, entry, path):
    if 'protocol' not in entry:
        report.add('scoring_protocol', path, 'incomplete', 'protocol_missing')
        return None
    record = entry['protocol']
    if not _schema(report, record, path, 'VinaProtocol'):
        return None
    report.compare('protocol_type', path, record.get('protocol_type'), 'VinaProtocol')
    parameters = _mapping(report, record, 'parameters', path + '/parameters')
    required = {
        'scoring',
        'cpu',
        'seed',
        'capture_backend_inputs',
        'allow_provisional_preparation',
        'collect_timings',
        'active_torsion_bonds',
        'exhaustiveness',
        'n_poses',
        'energy_range',
    }
    if set(parameters) != required:
        report.add(
            'scoring_protocol',
            path,
            'inconsistent' if set(parameters) - required else 'incomplete',
            'resolved_parameters_unavailable',
        )
        return None

    def validate():
        energy = parameters['energy_range']
        if not isinstance(energy, Mapping) or 'unit' not in energy:
            raise ValueError('explicit_energy_unit_required')
        _normalize_scores({'energy_range': energy['value']})
        try:
            return VinaProtocol.from_dict(record)
        except Exception as exc:
            # Quantity parsers have distinct exception types for malformed units.
            raise ValueError('invalid_protocol') from exc

    valid, protocol = report.validate('scoring_protocol', path, validate)
    return protocol if valid else None


def _execution(report, entry, path, protocol):
    applied = _mapping(
        report, entry, 'applied_parameters', path + '/applied_parameters'
    )
    report.compare(
        'unused_parameters',
        path,
        entry.get('unused_search_parameters'),
        ['exhaustiveness', 'n_poses', 'energy_range'],
    )
    if protocol is None:
        return
    for field in (
        'scoring',
        'cpu',
        'allow_provisional_preparation',
        'capture_backend_inputs',
        'collect_timings',
    ):
        actual = applied.get(field)
        expected = getattr(protocol, field)
        report.compare(
            'applied_parameter', f'{path}/applied_parameters/{field}', actual, expected
        )
        if actual is not None and type(actual) is not type(expected):
            report.add(
                'applied_parameter_type',
                f'{path}/applied_parameters/{field}',
                'inconsistent',
                'parameter_type_disagrees',
            )
    seed = applied.get('seed')
    if 'seed' not in applied:
        report.add('effective_seed', path, 'incomplete', 'effective_seed_missing')
    elif type(seed) is not int:
        report.add('effective_seed', path, 'inconsistent', 'invalid_effective_seed')
    elif protocol.seed not in (None, 0):
        report.compare('effective_seed', path, seed, protocol.seed)
    if protocol.active_torsion_bonds:
        report.add(
            'scoring_torsions',
            path,
            'inconsistent',
            'fixed_scoring_cannot_select_torsions',
        )


def _preparation(report, pose, entry, path, protocol):
    preparation = _mapping(report, entry, 'preparation', path + '/preparation')
    for role in ('receptor', 'partner'):
        role_path = f'{path}/preparation/{role}'
        recorded = _mapping(report, preparation, role, role_path)
        identities = (pose.get(f'{role}_state_id'), recorded.get('state_id'))
        if any(
            value is not None and (not isinstance(value, str) or not value.strip())
            for value in identities
        ):
            report.add(
                'scoring_state', role_path, 'inconsistent', 'invalid_state_identifier'
            )
            continue
        report.compare(
            'scoring_state',
            role_path,
            pose.get(f'{role}_state_id'),
            recorded.get('state_id'),
        )
        assessment = _mapping(
            report, recorded, 'assessment_report', role_path + '/assessment_report'
        )
        if not assessment or not _schema(
            report, assessment, role_path, 'PreparationAssessment'
        ):
            continue

        def expected_report():
            evidence = assessment.get('evidence')
            if (
                not isinstance(evidence, Mapping)
                or set(evidence) != {'charge_source', 'atom_type_source'}
                or any(
                    value is not None and not isinstance(value, str)
                    for value in evidence.values()
                )
            ):
                raise ValueError('invalid_preparation_evidence')
            return _assessment_from_sources(dict(evidence))

        valid, expected = report.validate(
            'preparation_evidence', role_path, expected_report
        )
        if valid:
            for key in (
                'scope',
                'assessment',
                'provisional_reason_codes',
                'provisional_reasons',
            ):
                report.compare(
                    'preparation_declaration',
                    role_path + '/' + key,
                    assessment.get(key),
                    expected[key],
                )
            if (
                expected['assessment'] == 'provisional'
                and protocol is not None
                and not protocol.allow_provisional_preparation
            ):
                report.add(
                    'preparation_policy',
                    role_path,
                    'inconsistent',
                    'provisional_execution_without_opt_in',
                )


def _geometry(report, pose, entry, path):
    geometry = _mapping(report, entry, 'geometry_check', path + '/geometry_check')
    if not geometry:
        return
    report.compare(
        'geometry_order', path, geometry.get('atom_order'), 'pdbqt_record_order'
    )
    if 'identity_check' not in geometry:
        report.add('geometry_identity', path, 'incomplete', 'identity_check_missing')
    elif geometry['identity_check'] not in ('positional_only', 'names_and_elements'):
        report.add('geometry_identity', path, 'inconsistent', 'invalid_identity_check')
    if 'coordinate_tolerance' not in geometry:
        report.add('geometry_tolerance', path, 'incomplete', 'tolerance_missing')
    else:
        report.validate(
            'geometry_tolerance',
            path,
            lambda: _length_values(geometry['coordinate_tolerance'], (), positive=True),
        )
    states = _mapping(
        report, geometry, 'state_checks', path + '/geometry_check/state_checks'
    )
    preparation = entry.get('preparation', {})
    for role in ('receptor', 'partner'):
        recorded = preparation.get(role, {}) if isinstance(preparation, Mapping) else {}
        state = recorded.get('state_id') if isinstance(recorded, Mapping) else None
        expected = (
            'matched'
            if state is not None and pose.get(f'{role}_state_id') is not None
            else 'unknown'
        )
        if isinstance(recorded, Mapping) and 'state_id' in recorded:
            report.compare(
                'geometry_state_check', path + '/' + role, states.get(role), expected
            )


def _evaluation(report, pose, entry, path, current_scores, current_definitions, owners):
    report.compare('scoring_operation', path, entry.get('operation'), 'score')
    protocol = _protocol(report, entry, path + '/protocol')
    _execution(report, entry, path, protocol)
    _preparation(report, pose, entry, path, protocol)
    _geometry(report, pose, entry, path)
    artifacts = _mapping(
        report, entry, 'backend_artifacts', path + '/backend_artifacts'
    )
    for role in ('receptor', 'partner'):
        status, reason, _ = inspect_artifact(artifacts.get(role), role)
        report.add(
            'captured_input', path + '/backend_artifacts/' + role, status, reason
        )
    scores = _mapping(report, entry, 'scores', path + '/scores')
    valid, scores = report.validate(
        'evaluation_scores', path, lambda: _normalize_scores(scores)
    )
    if not valid:
        return
    definitions = _mapping(
        report, entry, 'score_definitions', path + '/score_definitions'
    )
    valid, definitions = report.validate(
        'evaluation_definitions',
        path,
        lambda: normalize_definitions(definitions, scores),
    )
    if not valid:
        return
    components = None
    if 'score_name' not in entry:
        report.add('evaluation_name', path, 'incomplete', 'evaluation_name_missing')
    elif not isinstance(entry['score_name'], str) or not entry['score_name'].strip():
        report.add('evaluation_name', path, 'inconsistent', 'invalid_evaluation_name')
    else:
        components = fixed_score_components(entry['score_name'])
        report.compare(
            'evaluation_components', path, sorted(scores), sorted(components)
        )
    if not scores or set(scores) != set(definitions):
        report.add('evaluation_meaning', path, 'incomplete', 'score_meaning_missing')
    for name, value in scores.items():
        score_path = path + '/scores/' + name
        if name in owners:
            report.add(
                'score_ownership',
                score_path,
                'inconsistent',
                'score_recorded_more_than_once',
            )
        owners.add(name)
        if isinstance(pose.get('scores'), Mapping) and name not in pose['scores']:
            report.add(
                'score_membership',
                score_path,
                'inconsistent',
                'historical_score_missing_from_pose',
            )
        report.compare('evaluation_value', score_path, current_scores.get(name), value)
        if name in definitions:
            current = current_definitions.get(name)
            report.compare(
                'evaluation_semantics',
                score_path,
                json.dumps(current, sort_keys=True) if current is not None else None,
                json.dumps(definitions[name], sort_keys=True),
            )
            if components is not None:
                _audit_vina(
                    report,
                    definitions[name],
                    name,
                    entry,
                    score_path,
                    stage='scoring',
                    components=components,
                )


@arg_digest(config='dockingmt._argdigest')
def audit_pose(record):
    """Audit an already loaded saved DockingPose mapping, including rescoring.

    Return a detached JSON consistency report without file access, molecular
    operations or optional engines/viewers. Missing evidence stays incomplete;
    contradictions take precedence. This checks recorded declarations, not
    coordinate/PDBQT matching, chemical validity or score correctness.
    """
    report = _Report()
    scope = 'saved_pose_internal_consistency'
    admitted, scores, definitions = _audit_pose_payload(report, record, '/')
    if admitted is None:
        return report.export(scope)
    metadata = record.get('metadata', {})
    if not isinstance(metadata, Mapping):
        return report.export(scope)
    history = metadata.get('scoring_history', [])
    if not isinstance(history, list):
        report.add(
            'scoring_history',
            '/metadata/scoring_history',
            'inconsistent',
            'invalid_history_container',
        )
        return report.export(scope)
    if not history:
        report.add(
            'scoring_history',
            '/metadata/scoring_history',
            'incomplete',
            'scoring_evidence_missing',
        )
    owners = set()
    for index, entry in enumerate(history):
        path = f'/metadata/scoring_history/{index}'
        if _schema(report, entry, path, 'ScoringEvaluation'):
            _evaluation(
                report, record, entry, path, scores or {}, definitions or {}, owners
            )
    for name in sorted(set(scores or {}) - owners):
        report.add(
            'score_origin',
            '/scores/' + name,
            'incomplete',
            'evaluation_evidence_missing',
        )
    return report.export(scope)
