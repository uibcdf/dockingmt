"""Independent cohort, denominator and offline admission controls."""

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError


def make_report(distances=(4, 1), *, top_n=(1, 2, 5), n_atoms=2):
    reference = puw.quantity([[index, 0, 0] for index in range(n_atoms)], 'angstrom')
    poses = [
        dmt.DockingPose(
            puw.quantity(
                [[distance + atom, 0, 0] for atom in range(n_atoms)], 'angstrom'
            ),
            pose_id=f'pose_{index}',
            rank=10 - index,
        )
        for index, distance in enumerate(distances, 1)
    ]
    result = dmt.DockingResult(
        poses,
        protocol_info={'seed': 42, 'cpu': 1},
        problem_info={'metadata': {'fixture': ['analytical translations']}},
        provenance={
            'backend': 'declared_control',
            'backend_version': '1',
            'preparation': {'partner': {'assessment': 'unassessed'}},
        },
    )
    return dmt.evaluate_redocking(
        result,
        reference,
        rmsd_cutoff=puw.quantity(2, 'angstrom'),
        top_n=top_n,
        reference_info={'fixture': ['declared coordinate reference']},
    )


def failure():
    outcome = dmt.DockingOutcome(
        0,
        error={
            'type': 'builtins.RuntimeError',
            'message': 'fixture failure',
            'code': None,
        },
    )
    return {
        'stage': 'evaluation',
        'error': outcome.error,
        'context': {'origin': ['explicit fixture']},
    }


def digest(record):
    return hashlib.sha256(
        json.dumps(
            record, sort_keys=True, separators=(',', ':'), allow_nan=False
        ).encode()
    ).hexdigest()


def test_independent_denominators_empty_cases_and_pose_identity():
    inputs = {
        'later': make_report(),
        'empty': make_report(()),
        'first': make_report((0,)),
    }
    failures = {'missing': failure()}
    summary = dmt.summarize_redocking(inputs, failures=failures)
    assert (summary['n_submitted'], summary['n_evaluated'], summary['n_failed']) == (
        4,
        3,
        1,
    )
    assert summary['n_empty_results'] == 1
    assert summary['evaluation_coverage'] == 0.75
    assert summary['top_n'] == [
        {
            'requested': 1,
            'n_recovered': 1,
            'n_not_recovered': 2,
            'n_unknown': 1,
            'fraction_of_evaluated': 1 / 3,
            'fraction_of_submitted': 1 / 4,
        },
        {
            'requested': 2,
            'n_recovered': 2,
            'n_not_recovered': 1,
            'n_unknown': 1,
            'fraction_of_evaluated': 2 / 3,
            'fraction_of_submitted': 2 / 4,
        },
        {
            'requested': 5,
            'n_recovered': 2,
            'n_not_recovered': 1,
            'n_unknown': 1,
            'fraction_of_evaluated': 2 / 3,
            'fraction_of_submitted': 2 / 4,
        },
    ]
    assert [case['case_id'] for case in summary['cases']] == [
        'later',
        'empty',
        'first',
        'missing',
    ]
    case = summary['cases'][0]
    assert case['first_pose']['rmsd'] == pytest.approx(4)
    assert case['first_pose']['rank'] == 9
    assert case['closest_pose']['pose_id'] == 'pose_2'
    assert case['closest_pose']['rmsd'] == pytest.approx(1)
    assert case['evaluation_sha256'] == digest(inputs['later'])
    assert (
        case['reference']['snapshot_sha256']
        == inputs['later']['reference']['snapshot_sha256']
    )
    assert 'coordinates' not in case['reference'] and 'poses' not in case
    assert summary['cases'][1]['first_pose'] is None
    assert summary['cases'][-1]['recovery'] == 'unknown'
    assert summary['cases'][-1]['error'] == failures['missing']['error']


@pytest.mark.parametrize('failures', [None, {}, {'failed': failure()}])
def test_zero_evaluated_cases_infer_no_policy_or_recovery(failures):
    summary = dmt.summarize_redocking({}, failures=failures)
    assert summary['policy'] is None and summary['top_n'] == []
    assert summary['n_evaluated'] == summary['n_empty_results'] == 0
    assert summary['evaluation_coverage'] == (0 if failures else None)
    assert summary['n_submitted'] == summary['n_failed'] == (1 if failures else 0)
    assert json.loads(json.dumps(summary, allow_nan=False)) == summary


def test_empty_result_is_evaluated_nonrecovery():
    summary = dmt.summarize_redocking({'empty': make_report(())})
    assert summary['evaluation_coverage'] == 1
    assert summary['policy'] is not None
    assert all(
        entry['fraction_of_evaluated'] == entry['fraction_of_submitted'] == 0
        and entry['n_not_recovered'] == 1
        and entry['n_unknown'] == 0
        for entry in summary['top_n']
    )


def test_json_detachment_in_both_directions_and_between_output_sections():
    inputs, failures = {'case': make_report()}, {'failed': failure()}
    before = deepcopy((inputs, failures))
    summary = dmt.summarize_redocking(inputs, failures=failures)
    assert (inputs, failures) == before
    assert json.loads(json.dumps(summary, allow_nan=False)) == summary
    summary['policy']['protocol_info']['seed'] = 100
    assert 'protocol_info' not in summary['cases'][0]['context']
    summary['cases'][0]['context']['problem_info']['metadata']['fixture'].append('edit')
    summary['cases'][0]['reference']['declared_info']['fixture'].append('edit')
    summary['cases'][1]['context']['origin'].append('edit')
    assert (inputs, failures) == before
    inputs['case']['closest_pose']['rmsd'] = 90
    failures['failed']['error']['message'] = 'new'
    assert summary['cases'][0]['closest_pose']['rmsd'] == pytest.approx(1)
    assert summary['cases'][1]['error']['message'] == 'fixture failure'


@pytest.mark.parametrize(
    'path,value',
    [
        (('criterion', 'cutoff'), 3),
        (('context', 'backend'), 'other'),
        (('context', 'backend_version'), None),
        (('context', 'protocol_info', 'seed'), None),
        (('context', 'protocol_info', 'cpu'), True),
        (('context', 'preparation'), None),
        (('context', 'preparation', 'partner', 'assessment'), 'provisional'),
        (('evaluator', 'molsysmt_version'), 'other'),
        (('evaluator', 'dockingmt_version'), 'other'),
    ],
)
def test_incompatible_known_unknown_or_changed_declarations_raise(path, value):
    a = make_report((4, 1))
    b = deepcopy(a)
    target = b
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    with pytest.raises(ArgumentError, match='Incompatible'):
        dmt.summarize_redocking({'a': a, 'b': b})


def test_top_n_order_and_population_are_conservative_cohort_choices():
    a = make_report(top_n=(1, 2))
    for counts in ((2, 1), (1, 5)):
        with pytest.raises(ArgumentError, match='Incompatible'):
            dmt.summarize_redocking({'a': a, 'b': make_report(top_n=counts)})


def test_different_inputs_atom_counts_domains_and_reference_declarations_remain_case_specific():
    a, b = make_report(), make_report((0,), n_atoms=3)
    b['context']['problem_info']['metadata']['fixture'] = ['different domain/input']
    b['reference']['declared_info'] = {'different': 'case'}
    b['reference']['snapshot_sha256'] = digest(
        {k: v for k, v in b['reference'].items() if k != 'snapshot_sha256'}
    )
    summary = dmt.summarize_redocking({'a': a, 'b': b})
    assert summary['n_evaluated'] == 2
    assert summary['cases'][0]['reference'] != summary['cases'][1]['reference']
    assert summary['cases'][1]['context'] == {
        key: value
        for key, value in b['context'].items()
        if key not in ('backend', 'backend_version', 'protocol_info', 'preparation')
    }


@pytest.mark.parametrize(
    'field,value',
    [
        ('schema_version', None),
        ('schema_version', 1),
        ('schema_version', '2.0'),
        ('evaluation_type', 'other'),
        ('n_poses', True),
        ('n_poses', 99),
        ('poses', {}),
        ('top_n', []),
        ('context', None),
        ('evaluator', []),
        ('first_pose', None),
        ('closest_pose', None),
    ],
)
def test_malformed_or_inconsistent_saved_reports_raise(field, value):
    report = make_report()
    report[field] = value
    with pytest.raises(ArgumentError):
        dmt.summarize_redocking({'bad': report})


@pytest.mark.parametrize(
    'field,value',
    [
        ('unit', 'nanometer'),
        ('metric', 'least_rmsd'),
        ('cutoff', True),
        ('cutoff', -1),
        ('alignment', 'superposed'),
        ('symmetry_correction', 'corrected'),
        ('atom_scope', 'heavy_atoms'),
        ('atom_correspondence', 'inferred'),
        ('top_n_basis', 'stored_rank'),
        ('unknown_policy', 'value'),
    ],
)
def test_unsupported_criterion_or_units_are_not_silently_normalized(field, value):
    report = make_report()
    report['criterion'][field] = value
    with pytest.raises(ArgumentError, match='criterion'):
        dmt.summarize_redocking({'bad': report})


@pytest.mark.parametrize(
    'field,value',
    [
        ('position', True),
        ('position', 9),
        ('n_atoms', 0),
        ('n_atoms', 3),
        ('rmsd', True),
        ('rmsd', -1),
        ('rmsd', 0),
        ('recovered', 1),
        ('rank', True),
        ('pose_id', ''),
        ('partner_state_id', 1),
    ],
)
def test_inconsistent_pose_evidence_is_rejected(field, value):
    report = make_report()
    report['poses'][0][field] = value
    with pytest.raises(ArgumentError):
        dmt.summarize_redocking({'bad': report})


@pytest.mark.parametrize(
    'field,value',
    [
        ('requested', True),
        ('requested', 0),
        ('considered', True),
        ('considered', 99),
        ('recovered', True),
        ('recovered', 0),
    ],
)
def test_top_n_numerical_evidence_must_agree_with_observations(field, value):
    report = make_report()
    report['top_n'][0][field] = value
    with pytest.raises(ArgumentError, match='Top-N'):
        dmt.summarize_redocking({'bad': report})


def test_missing_fields_duplicate_top_n_and_reference_digest_reject():
    for mutate in (
        lambda r: r.pop('schema_version'),
        lambda r: r['context'].pop('preparation'),
        lambda r: r['poses'][0].pop('pose_id'),
        lambda r: r['poses'][0].pop('rank'),
        lambda r: r['top_n'].append(deepcopy(r['top_n'][0])),
        lambda r: r['reference']['coordinates']['value'][0].__setitem__(0, 99),
        lambda r: r['reference']['coordinates'].__setitem__('unit', 'nm'),
    ):
        report = make_report()
        mutate(report)
        with pytest.raises(ArgumentError):
            dmt.summarize_redocking({'bad': report})


def test_closest_tie_and_typed_summary_identity_cannot_change():
    tied = make_report((1, 1))
    tied['closest_pose'] = deepcopy(tied['poses'][1])
    with pytest.raises(ArgumentError, match='First/closest'):
        dmt.summarize_redocking({'tied': tied})
    report = make_report()
    report['poses'][0]['rank'] = 1
    report['first_pose'] = deepcopy(report['poses'][0])
    report['first_pose']['rank'] = True
    with pytest.raises(ArgumentError, match='First/closest'):
        dmt.summarize_redocking({'boolean_rank': report})


def test_saved_report_units_are_admitted_without_implicit_conversion():
    report = make_report()
    # An internally agreeing alternate length protocol still needs its own schema.
    report['criterion']['unit'] = 'nanometer'
    report['criterion']['cutoff'] /= 10
    for row in report['poses']:
        row['rmsd'] /= 10
    report['first_pose'] = deepcopy(report['poses'][0])
    report['closest_pose'] = deepcopy(report['poses'][1])
    with pytest.raises(ArgumentError, match='angstrom'):
        dmt.summarize_redocking({'alternate_protocol': report})


@pytest.mark.parametrize('bad', [None, [], 'report', float('nan'), np.asarray([1])])
def test_invalid_evaluation_payload_is_rejected(bad):
    with pytest.raises(ArgumentError):
        dmt.summarize_redocking({'bad': bad})


@pytest.mark.parametrize('bad', [float('inf'), (1, 2), np.float64(1), {1: 'value'}])
def test_finite_json_contract_is_preserved_even_in_unused_context(bad):
    report = make_report()
    report['context']['caller_extension'] = bad
    with pytest.raises(ArgumentError):
        dmt.summarize_redocking({'bad': report})


@pytest.mark.parametrize(
    'evaluations,failures',
    [
        ([], None),
        ({}, []),
        ({'': {}}, None),
        ({1: {}}, None),
        ({'a': make_report()}, {'a': failure()}),
        ({}, {' ': failure()}),
    ],
)
def test_mapping_contract_and_disjoint_case_ids(evaluations, failures):
    with pytest.raises(ArgumentError):
        dmt.summarize_redocking(evaluations, failures=failures)


@pytest.mark.parametrize(
    'bad',
    [
        None,
        {},
        {'stage': '', 'error': failure()['error']},
        {'stage': 'dock', 'error': {'type': 'Exception', 'message': 'oops'}},
        {'stage': 'dock', 'error': {'type': '', 'message': 'oops', 'code': None}},
        {'stage': 'dock', 'error': {'type': 'Exception', 'message': 1, 'code': None}},
        {'stage': 'dock', 'error': {'type': 'Exception', 'message': 'oops', 'code': 1}},
        dict(failure(), context=[]),
        dict(failure(), hidden_policy=True),
    ],
)
def test_declared_failures_use_typed_outcome_error_contract(bad):
    with pytest.raises(ArgumentError):
        dmt.summarize_redocking({}, failures={'bad': bad})


def test_unknown_preparation_is_preserved_without_qualification():
    a = make_report()
    a['context']['preparation'] = None
    summary = dmt.summarize_redocking({'unknown': a})
    assert summary['policy']['preparation'] is None
    assert summary['interpretation'] == 'observations_in_caller_selected_cases'


def test_nondefault_units_and_no_molecular_or_engine_calls(monkeypatch):
    report = make_report()

    def forbidden(*args, **kwargs):
        raise AssertionError('Summary must use saved observations only.')

    monkeypatch.setattr(msm.structure, 'get_rmsd', forbidden)
    monkeypatch.setattr(msm, 'convert', forbidden)
    monkeypatch.setattr(dmt, 'dock', forbidden)
    with puw.context(standard_units=['pm', 'fs']):
        summary = dmt.summarize_redocking({'saved': report})
    assert summary['policy']['criterion']['unit'] == 'angstrom'
    assert summary['cases'][0]['first_pose']['rmsd'] == pytest.approx(4)


def test_fresh_offline_reader_has_no_engine_or_viewer_imports(tmp_path):
    saved = tmp_path / 'reports.json'
    saved.write_text(json.dumps({'saved': make_report()}, allow_nan=False))
    program = """
import importlib.abc, json, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in ('vina', 'molsysviewer', 'meeko'):
            raise AssertionError(fullname)
sys.meta_path.insert(0, Block())
import dockingmt as dmt
from pathlib import Path
summary = dmt.summarize_redocking(json.loads(Path(sys.argv[1]).read_text()))
assert summary['n_evaluated'] == 1
assert summary['top_n'][0]['n_recovered'] == 0
assert json.loads(json.dumps(summary, allow_nan=False)) == summary
assert 'vina' not in sys.modules and 'molsysviewer' not in sys.modules and 'meeko' not in sys.modules
"""
    subprocess.run(
        [sys.executable, '-c', program, str(saved)],
        check=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
    )


def test_retained_native_reports_show_positive_and_displaced_controls():
    reports = json.loads(
        (
            Path(__file__).parents[1]
            / 'devguide/validation/data/redocking_evaluation/cases.json'
        ).read_text()
    )
    with pytest.raises(ArgumentError, match='Incompatible'):
        dmt.summarize_redocking(reports)
    selected = {key: reports[key] for key in ('1iep_external', '1iep_displaced_domain')}
    summary = dmt.summarize_redocking(selected, failures={'fixture': failure()})
    assert summary['n_evaluated'] == 2 and summary['n_failed'] == 1
    assert all(
        entry['n_recovered'] == 1
        and entry['n_not_recovered'] == 1
        and entry['n_unknown'] == 1
        and entry['fraction_of_evaluated'] == 0.5
        and entry['fraction_of_submitted'] == 1 / 3
        for entry in summary['top_n']
    )
    assert summary['policy']['preparation']['partner']['assessment'] == 'unassessed'
