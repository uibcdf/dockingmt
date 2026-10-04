"""Offline summaries of explicitly selected, compatible redocking reports."""

from collections.abc import Mapping
from math import isfinite

import smonitor
from argdigest import arg_digest

from dockingmt._private.smonitor import ArgumentError
from dockingmt.evaluation import _digest, _json_copy


def _invalid(case_id, reason, argument='evaluations'):
    raise ArgumentError(arg_name=argument, reason=f'Case {case_id!r}: {reason}')


def _finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return isfinite(value)
    except OverflowError:
        return False


def _number(value):
    return _finite_number(value) and value >= 0


def _positive_integer(value):
    return type(value) is int and value > 0


def _case_ids(mapping, argument):
    if any(not isinstance(key, str) or not key.strip() for key in mapping):
        raise ArgumentError(arg_name=argument, reason='Use nonempty string case IDs.')


def _validate_evaluation(report, case_id):
    """Check the saved numerical protocol and summaries, without molecular IO."""
    if not isinstance(report, Mapping):
        _invalid(case_id, 'Supply an evaluate_redocking report mapping.')
    report = _json_copy(report, 'evaluations')
    if (
        report.get('schema_version') != '1.0'
        or report.get('evaluation_type') != 'redocking'
    ):
        _invalid(case_id, 'Use an explicit redocking evaluation schema 1.0.')
    criterion = report.get('criterion')
    expected = {
        'metric': 'positional_rmsd',
        'unit': 'angstrom',
        'comparison': '<=',
        'alignment': 'none',
        'symmetry_correction': 'none',
        'coordinate_frame': 'caller_declared_shared_receptor_frame',
        'atom_scope': 'retained_pose_atoms',
        'top_n_basis': 'result_order',
    }
    if (
        not isinstance(criterion, dict)
        or set(criterion) != set(expected) | {'cutoff', 'atom_correspondence'}
        or any(criterion[key] != value for key, value in expected.items())
        or criterion['atom_correspondence']
        not in ('caller_declared_positional', 'verified_source_atom_keys')
        or not _number(criterion['cutoff'])
    ):
        _invalid(case_id, 'Unsupported comparison criterion or fixed angstrom unit.')

    reference = report.get('reference')
    if not isinstance(reference, dict) or reference.get('kind') not in (
        'coordinates',
        'pose',
        'molecular_system',
    ):
        _invalid(case_id, 'Supply the saved reference evidence.')
    coordinates = reference.get('coordinates')
    if (
        not isinstance(coordinates, dict)
        or coordinates.get('unit') != 'angstrom'
        or not isinstance(coordinates.get('value'), list)
        or not coordinates['value']
        or any(
            not isinstance(xyz, list)
            or len(xyz) != 3
            or any(not _finite_number(value) for value in xyz)
            for xyz in coordinates['value']
        )
    ):
        _invalid(case_id, 'Reference coordinates must declare finite angstrom values.')
    if reference.get('snapshot_sha256') != _digest(
        {key: value for key, value in reference.items() if key != 'snapshot_sha256'}
    ):
        _invalid(case_id, 'Reference snapshot digest disagrees with its record.')
    if not isinstance(reference.get('declared_info'), dict) or (
        reference['kind'] == 'coordinates'
    ) != (criterion['atom_correspondence'] == 'caller_declared_positional'):
        _invalid(case_id, 'Reference declarations disagree with correspondence policy.')

    rows = report.get('poses')
    if (
        not isinstance(rows, list)
        or type(report.get('n_poses')) is not int
        or report['n_poses'] != len(rows)
    ):
        _invalid(case_id, 'Pose count disagrees with the saved population.')
    for position, row in enumerate(rows, 1):
        if (
            not isinstance(row, dict)
            or type(row.get('position')) is not int
            or row['position'] != position
            or not _positive_integer(row.get('n_atoms'))
            or not _number(row.get('rmsd'))
            or type(row.get('recovered')) is not bool
            or row['recovered'] != (row['rmsd'] <= criterion['cutoff'])
        ):
            _invalid(
                case_id, 'Pose position, count or recovery disagrees with its RMSD.'
            )
        if (
            'rank' not in row
            or row['rank'] is not None
            and not _positive_integer(row['rank'])
        ):
            _invalid(case_id, 'Declared ranks must be positive integers or None.')
        for field in ('pose_id', 'partner_state_id', 'receptor_state_id'):
            if field not in row or (
                row[field] is not None
                and (not isinstance(row[field], str) or not row[field].strip())
            ):
                _invalid(
                    case_id, 'Preserve explicit pose/state identities, including None.'
                )
        if row['n_atoms'] != rows[0]['n_atoms'] or (
            criterion['atom_correspondence'] == 'caller_declared_positional'
            and row['n_atoms'] != len(coordinates['value'])
        ):
            _invalid(
                case_id, 'Pose atom counts disagree with the comparison population.'
            )
    first = rows[0] if rows else None
    closest = min(rows, key=lambda row: row['rmsd']) if rows else None
    if (
        'first_pose' not in report
        or 'closest_pose' not in report
        or _digest(report['first_pose']) != _digest(first)
        or _digest(report['closest_pose']) != _digest(closest)
    ):
        _invalid(
            case_id, 'First/closest pose summaries disagree with current positions.'
        )
    top_n = report.get('top_n')
    if not isinstance(top_n, list) or not top_n:
        _invalid(case_id, 'Supply nonempty saved top-N requests.')
    requested = []
    for entry in top_n:
        if (
            not isinstance(entry, dict)
            or set(entry) != {'requested', 'considered', 'recovered'}
            or not _positive_integer(entry['requested'])
            or entry['requested'] in requested
            or type(entry['considered']) is not int
            or entry['considered'] != min(entry['requested'], len(rows))
            or type(entry['recovered']) is not bool
            or entry['recovered']
            != any(row['recovered'] for row in rows[: entry['requested']])
        ):
            _invalid(
                case_id,
                'Top-N requests/counts/recovery disagree with pose observations.',
            )
        requested.append(entry['requested'])
    context, evaluator = report.get('context'), report.get('evaluator')
    if (
        not isinstance(context, dict)
        or not isinstance(evaluator, dict)
        or not {'backend', 'backend_version', 'protocol_info', 'preparation'}
        <= context.keys()
        or not {'dockingmt_version', 'molsysmt_version', 'rmsd_function'}
        <= evaluator.keys()
        or not isinstance(context['protocol_info'], dict)
        or context['preparation'] is not None
        and not isinstance(context['preparation'], dict)
        or any(
            context[field] is not None
            and (not isinstance(context[field], str) or not context[field].strip())
            for field in ('backend', 'backend_version')
        )
        or any(
            not isinstance(evaluator[field], str) or not evaluator[field].strip()
            for field in ('dockingmt_version', 'molsysmt_version', 'rmsd_function')
        )
        or evaluator['rmsd_function'] != 'molsysmt.structure.get_rmsd'
    ):
        _invalid(
            case_id, 'Preserve method/protocol/preparation/evaluator declarations.'
        )
    policy = {
        'criterion': criterion,
        'top_n': requested,
        'evaluator': evaluator,
        'backend': context['backend'],
        'backend_version': context['backend_version'],
        'protocol_info': context['protocol_info'],
        'preparation': context['preparation'],
    }
    return report, policy


def _pose_summary(row):
    if row is None:
        return None
    return {
        field: row[field]
        for field in (
            'position',
            'pose_id',
            'rank',
            'partner_state_id',
            'receptor_state_id',
            'n_atoms',
            'rmsd',
            'recovered',
        )
    }


@smonitor.signal(tags=['api', 'analysis', 'redocking', 'aggregation'])
@arg_digest(config='dockingmt._argdigest')
def summarize_redocking(
    evaluations: Mapping, *, failures: Mapping | None = None
) -> dict:
    """Summarize one compatible cohort of saved redocking evaluation reports.

    ``evaluations`` maps caller case IDs to evaluate_redocking schema 1.0 reports.
    ``failures`` uses disjoint case IDs and records ``stage``, ``error`` (the
    type/message/code summary used by DockingOutcome), and optional ``context``.
    Invalid reports raise; this function never captures execution exceptions.

    Require exactly equal criteria, ordered top-N requests, evaluator identity,
    backend/version, protocol and preparation declarations. This conservative
    admission does not certify scientific comparability; unknowns stay unknown.
    Different inputs, references and search domains remain case-specific.

    Count empty results as evaluated/nonrecovered. Failed cases have unknown
    recovery, separate from observed nonrecovery. Fractions explicitly name
    evaluated or submitted denominators, and are None for zero denominators.
    Empty/all-failure collections have no inferred policy or top-N statistics.

    Return detached finite JSON with compact cases and original-report hashes.
    Retain original reports separately. No molecular operations, reranking,
    engine execution or viewer access occurs, and no dataset certification is
    inferred from these observations. Mapping order is kept within each input.
    """
    failures = failures if failures is not None else {}
    _case_ids(evaluations, 'evaluations')
    _case_ids(failures, 'failures')
    if evaluations.keys() & failures.keys():
        raise ArgumentError(
            arg_name='failures',
            reason='Evaluated and failed case IDs must be disjoint.',
        )
    policy = None
    cases = []
    counts = []
    empty = 0
    for case_id, original in evaluations.items():
        report, current = _validate_evaluation(original, case_id)
        if policy is None:
            policy = current
            counts = [0] * len(report['top_n'])
        elif _digest(current) != _digest(policy):
            _invalid(
                case_id,
                'Incompatible comparison/method/protocol/preparation declarations; summarize separately.',
            )
        for index, entry in enumerate(report['top_n']):
            counts[index] += entry['recovered']
        empty += report['n_poses'] == 0
        cases.append(
            {
                'case_id': case_id,
                'status': 'evaluated',
                'evaluation_sha256': _digest(report),
                'n_poses': report['n_poses'],
                'first_pose': _pose_summary(report['first_pose']),
                'closest_pose': _pose_summary(report['closest_pose']),
                'top_n': report['top_n'],
                'reference': {
                    'kind': report['reference']['kind'],
                    'snapshot_sha256': report['reference']['snapshot_sha256'],
                    'n_atoms': len(report['reference']['coordinates']['value']),
                    'declared_info': report['reference']['declared_info'],
                },
                # Common declarations are retained once in the summary policy.
                'context': {
                    key: value
                    for key, value in report['context'].items()
                    if key
                    not in (
                        'backend',
                        'backend_version',
                        'protocol_info',
                        'preparation',
                    )
                },
            }
        )
    for case_id, original in failures.items():
        failure = _json_copy(original, 'failures')
        if (
            not isinstance(failure, dict)
            or not {'stage', 'error'} <= failure.keys()
            or not failure.keys() <= {'stage', 'error', 'context'}
            or not isinstance(failure['stage'], str)
            or not failure['stage'].strip()
            or not isinstance(failure.get('context', {}), dict)
        ):
            _invalid(
                case_id,
                'Declare a nonempty stage, typed error and optional context.',
                'failures',
            )
        error = failure['error']
        # Reuse the public outcome's typed-summary admission; no result is created.
        from dockingmt.core.outcome import DockingOutcome

        error = DockingOutcome(0, error=error).error
        cases.append(
            {
                'case_id': case_id,
                'status': 'failed',
                'recovery': 'unknown',
                'stage': failure['stage'],
                'error': error,
                'context': failure.get('context', {}),
            }
        )
    n_evaluated, n_failed = len(evaluations), len(failures)
    n_submitted = n_evaluated + n_failed
    from dockingmt._version import __version__

    return _json_copy(
        {
            'schema_version': '1.0',
            'summary_type': 'redocking_collection',
            'interpretation': 'observations_in_caller_selected_cases',
            'compatibility': 'exact_recorded_declarations',
            'policy': policy,
            'n_submitted': n_submitted,
            'n_evaluated': n_evaluated,
            'n_failed': n_failed,
            'n_empty_results': empty,
            'evaluation_coverage': n_evaluated / n_submitted if n_submitted else None,
            'top_n': [
                {
                    'requested': n,
                    'n_recovered': count,
                    'n_not_recovered': n_evaluated - count,
                    'n_unknown': n_failed,
                    'fraction_of_evaluated': count / n_evaluated,
                    'fraction_of_submitted': count / n_submitted,
                }
                for n, count in zip(
                    policy['top_n'] if policy is not None else [], counts
                )
            ],
            'cases': cases,
            'summarizer': {'dockingmt_version': __version__},
        },
        'evaluations',
    )
