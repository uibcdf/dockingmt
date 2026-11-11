"""Software controls with saved observations and explicitly synthetic molecular seams.

These controls receive no new chemistry or energies and authenticate no producer.
"""

import base64
import builtins
import gzip
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

import bindingmt as bmt
from bindingmt import comparison
from bindingmt._private.smonitor import ArgumentError

DATA = (
    Path(__file__).resolve().parents[1]
    / 'devguide/validation/data/e1_native_rescoring_2026-11-06'
)


@pytest.fixture(scope='module')
def received_records():
    paths = [DATA / f'pose_{i}/vinardo_scored_pose.json.gz' for i in range(1, 6)]
    original = [path.read_bytes() for path in paths]
    yield [json.loads(gzip.decompress(raw)) for raw in original]
    assert [path.read_bytes() for path in paths] == original


@pytest.fixture(autouse=True)
def no_scientific_operations(monkeypatch):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('A software test attempted a molecular/native operation')

    for name in (
        'get',
        'get_form',
        'convert',
        'select',
        'extract',
        'copy',
        'set',
        'permute_atoms',
    ):
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(msm.chemical_states, 'get_atom_correspondences', forbidden)
    for name in ('score', 'dock', 'prepare_ligand', 'prepare_receptor'):
        monkeypatch.setattr(bmt, name, forbidden)


def _result(records):
    return bmt.DockingResult(
        poses=[bmt.DockingPose.from_dict(record) for record in records]
    )


def _set_score(record, name, value):
    # Coherent synthetic declaration, not a new producer observation.
    record['scores'][name] = value
    for entry in record['metadata']['scoring_history']:
        if name in entry['scores']:
            entry['scores'][name] = value


def _context(record, score_name, key, value):
    for entry in record['metadata']['scoring_history']:
        if score_name in entry['scores']:
            for name in entry['scores']:
                entry['score_definitions'][name]['context'][key] = deepcopy(value)
                record['metadata']['score_definitions'][name]['context'][key] = (
                    deepcopy(value)
                )


def _rename_evaluation(record, old, new):
    entry = next(
        item
        for item in record['metadata']['scoring_history']
        if item['score_name'] == old
    )
    for name in list(entry['scores']):
        renamed = new + name[len(old) :]
        for mapping in (
            record['scores'],
            record['metadata']['score_definitions'],
            entry['scores'],
            entry['score_definitions'],
        ):
            mapping[renamed] = mapping.pop(name)
    entry['score_name'] = new
    reference = entry['reference_energy']
    reference['score_name'] = new + reference['score_name'][len(old) :]


def _synthetic_evidence():
    return {
        'prepared': {'test_scope': 'synthetic software seam'},
        'export': {
            'output_to_source_atom_indices': [0, 1],
            'source_atom_ids': ['test-C', 'test-N'],
            'source_atom_names': ['C1', 'N1'],
            'source_atom_types': ['C', 'N'],
            'output_atom_ff_types': ['C', 'N'],
            'torsion_tree': {'torsdof': 0, 'branches': []},
            'partial_charge_before_rounding': [0.25, 0.75],
        },
        'geometry_check': {'test_scope': 'synthetic'},
        'charge_audit': {'assessment': 'consistent', 'test_scope': 'synthetic'},
        'preparation_policy': {
            'hydrogen_policy': 'synthetic',
            'torsion_policy': 'rigid',
            'active_torsion_bonds': [],
            'charges': {'method': 'synthetic'},
            'typing': {'method': 'synthetic'},
        },
    }


@pytest.fixture
def software_case(received_records, monkeypatch):
    records = deepcopy(received_records)
    problems = [
        SimpleNamespace(
            system=SimpleNamespace(position=i, keys=['test-C', 'test-N']),
            evidence=_synthetic_evidence(),
        )
        for i in range(1, 6)
    ]
    calls = []

    def prepared(problem, pose, entry, definition, position):
        evidence = deepcopy(problem.evidence)
        evidence['export']['payload_sha256'] = definition['context']['partner_sha256']
        return problem.system, evidence

    def correspondence(system, reference, keys, reference_keys, position):
        calls.append((system.position, reference.position, position))
        if keys != reference_keys:
            raise ArgumentError(
                arg_name='comparison', reason='Synthetic ordered identity mismatch'
            )
        return {'test_scope': 'synthetic', 'atom_correspondences': [[[0, 0], [1, 1]]]}

    monkeypatch.setattr(comparison, '_prepared_view', prepared)
    monkeypatch.setattr(
        comparison, '_molecular_atom_keys', lambda system: deepcopy(system.keys)
    )
    monkeypatch.setattr(comparison, '_correspondence', correspondence)
    return SimpleNamespace(
        records=records, problems=problems, correspondence_calls=calls
    )


@pytest.mark.parametrize(
    'name,order',
    [('vina.lig_inter', [1, 2, 3, 4, 5]), ('vinardo.lig_inter', [1, 2, 4, 3, 5])],
)
def test_saved_observations_order_per_method_without_mutating_ranks(
    software_case, name, order
):
    case = software_case
    result = _result(case.records)
    before = result.to_dict()
    report = bmt.compare_scores(result, name, problems=case.problems, ascending=True)
    assert report['display_order'] == order
    assert len(report['rows']) == len(report['groups']) == 5
    assert [row['value'] for row in report['rows']] == [
        record['scores'][name] for record in case.records
    ]
    assert [row['original_rank'] for row in report['rows']] == [
        record['rank'] for record in case.records
    ]
    assert (
        len({row['definition']['context']['partner_sha256'] for row in report['rows']})
        == 5
    )
    assert 'authentication' in report['scope'] and 'not established' in report['scope']
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert case.correspondence_calls == [(i, 1, i) for i in range(1, 6)]
    assert result.to_dict() == before
    with pytest.raises(ArgumentError):
        result.rank_by(name)
    assert result.to_dict() == before


def test_selected_component_direction_and_exact_ties_are_explicit(software_case):
    case = software_case
    for index, record in enumerate(case.records):
        _set_score(record, 'vina', float(100 - index))  # Opposite total order.
        record['rank'] = 9 - index  # Synthetic ranks must not break ties.
    _set_score(
        case.records[1], 'vina.lig_inter', case.records[0]['scores']['vina.lig_inter']
    )
    result = _result(case.records)
    lower = bmt.compare_scores(
        result, 'vina.lig_inter', problems=case.problems, ascending=True
    )
    higher = bmt.compare_scores(
        result, 'vina.lig_inter', problems=case.problems, ascending=False
    )
    assert lower['display_order'] == [1, 2, 3, 4, 5]
    assert higher['display_order'] == [5, 4, 3, 1, 2]
    assert lower['groups'][0] == {'value': -6.422, 'positions': [1, 2]}
    assert higher['groups'][-1]['positions'] == [1, 2]
    assert lower['policy']['ties'] == 'equal_reported_values'
    assert lower['policy']['tie_presentation'] == 'source_order'
    assert [row['original_rank'] for row in lower['rows']] == [9, 8, 7, 6, 5]


def test_names_and_positions_are_not_a_five_pose_fixture_policy(software_case):
    case = software_case
    for i, record in enumerate(case.records, 20):
        record['pose_id'] = f'caller-conformer-{i}'
        _rename_evaluation(record, 'vina', 'caller_eval')
    permutation = [4, 0, 3, 1, 2]
    report = bmt.compare_scores(
        _result([case.records[i] for i in permutation]),
        'caller_eval.lig_inter',
        problems=[case.problems[i] for i in permutation],
        ascending=True,
    )
    assert report['display_order'] == [2, 4, 5, 3, 1]
    assert [report['rows'][i - 1]['pose_id'] for i in report['display_order']] == [
        f'caller-conformer-{i}' for i in range(20, 25)
    ]


def test_methods_cannot_be_pooled_by_renaming_the_score(software_case):
    case = software_case
    for index, record in enumerate(case.records):
        _rename_evaluation(record, 'vinardo' if index == 1 else 'vina', 'chosen')
    with pytest.raises(ArgumentError, match='shared comparison context differs'):
        bmt.compare_scores(
            _result(case.records),
            'chosen.lig_inter',
            problems=case.problems,
            ascending=True,
        )
    assert not case.correspondence_calls


@pytest.mark.parametrize(
    'key,value',
    [
        ('weights', [1.0]),
        (
            'backend_box',
            {'center': [0.0, 0.0, 0.0], 'size': [24.0] * 3, 'unit': 'angstrom'},
        ),
        ('grid_spacing', {'value': 0.5, 'unit': 'angstrom'}),
        ('receptor_sha256', '0' * 64),
        (
            'preparation_assessment',
            {'partner': 'provisional', 'receptor': 'unassessed'},
        ),
    ],
)
def test_changed_context_is_rejected_before_prepared_work(software_case, key, value):
    case = software_case
    _context(case.records[-1], 'vina.lig_inter', key, value)
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=case.problems,
            ascending=True,
        )
    assert not case.correspondence_calls


def test_caller_assertion_is_not_a_supported_context_field(software_case):
    case = software_case
    for record in case.records:
        _context(record, 'vina.lig_inter', 'caller_verified', True)
    with pytest.raises(ArgumentError, match='comparison-context fields'):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=case.problems,
            ascending=True,
        )
    assert not case.correspondence_calls


@pytest.mark.parametrize(
    'change',
    [
        'missing_history',
        'duplicate_history',
        'missing_reference',
        'bad_capture',
        'value_only',
    ],
)
def test_selected_evaluation_requires_complete_consistent_evidence(
    software_case, change
):
    case = software_case
    record = case.records[-1]
    history = record['metadata']['scoring_history']
    if change == 'missing_history':
        record['metadata']['scoring_history'] = history[1:]
    elif change == 'duplicate_history':
        history.append(deepcopy(history[0]))
    elif change == 'missing_reference':
        del history[0]['reference_energy']
    elif change == 'bad_capture':
        history[0]['backend_artifacts']['partner']['content_base64'] = '!!!'
    else:
        record['scores']['vina.lig_inter'] += 1
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=case.problems,
            ascending=True,
        )
    assert not case.correspondence_calls


@pytest.mark.parametrize('score_name', ['vina', 'vina.lig_intra_best_pose', 'absent'])
def test_unsupported_components_are_not_silently_substituted(software_case, score_name):
    case = software_case
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(case.records), score_name, problems=case.problems, ascending=True
        )
    assert not case.correspondence_calls


@pytest.mark.parametrize(
    'field,value',
    [
        ('pose_id', None),
        ('pose_id', 'e1-new-local-H-1'),
        ('partner_state_id', None),
        ('receptor_state_id', 'other-state'),
    ],
)
def test_unknown_or_conflicting_identity_is_not_guessed(software_case, field, value):
    case = software_case
    case.records[-1][field] = value
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=case.problems,
            ascending=True,
        )
    assert not case.correspondence_calls


@pytest.mark.parametrize(
    'change', ['types', 'tree', 'axis', 'policy', 'charges', 'identity']
)
def test_prepared_invariants_are_checked(software_case, change):
    case = software_case
    problem = case.problems[-1]
    if change == 'types':
        problem.evidence['export']['output_atom_ff_types'][0] = 'A'
    elif change == 'tree':
        problem.evidence['export']['torsion_tree']['torsdof'] = 1
    elif change == 'axis':
        problem.evidence['export']['source_atom_ids'].reverse()
    elif change == 'policy':
        problem.evidence['preparation_policy']['hydrogen_policy'] = 'other'
    elif change == 'charges':
        problem.evidence['export']['partial_charge_before_rounding'][0] += 1e-8
    else:
        problem.system.keys.reverse()
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=case.problems,
            ascending=True,
        )


@pytest.mark.parametrize('ascending', [None, 0, 1, 'lower'])
def test_direction_requires_an_explicit_boolean(software_case, ascending):
    case = software_case
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=case.problems,
            ascending=ascending,
        )


@pytest.mark.parametrize('count', [0, 4, 6])
def test_problem_count_must_match_the_complete_selection(software_case, count):
    case = software_case
    with pytest.raises(ArgumentError, match='at least two poses'):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=(case.problems * 2)[:count],
            ascending=True,
        )


def test_one_pose_does_not_create_a_comparison(software_case):
    case = software_case
    with pytest.raises(ArgumentError, match='at least two poses'):
        bmt.compare_scores(
            _result(case.records[:1]),
            'vina.lig_inter',
            problems=case.problems[:1],
            ascending=True,
        )


@pytest.mark.parametrize('name', [None, '', 7])
def test_selected_name_requires_an_explicit_nonempty_string(software_case, name):
    case = software_case
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(case.records), name, problems=case.problems, ascending=True
        )


@pytest.mark.parametrize('problems', ['prepared', {}, None])
def test_problem_argument_is_an_iterable_collection(software_case, problems):
    with pytest.raises(ArgumentError):
        bmt.compare_scores(
            _result(software_case.records),
            'vina.lig_inter',
            problems=problems,
            ascending=True,
        )


def test_caller_boolean_is_not_a_chemical_authentication_option(software_case):
    case = software_case
    with pytest.raises(UnknownArgumentError):
        bmt.compare_scores(
            _result(case.records),
            'vina.lig_inter',
            problems=case.problems,
            ascending=True,
            same_state=True,
        )


def test_report_is_detached_json_under_a_different_unit_policy(
    software_case, monkeypatch
):
    case = software_case
    result = _result(case.records)
    before = result.to_dict()
    original_import = builtins.__import__

    def guarded(name, *args, **kwargs):
        if name.split('.')[0] in ('vina', 'rdkit', 'openmm', 'molsysviewer'):
            pytest.fail(f'Comparison imported optional backend {name}')
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded)
    with puw.context(standard_units=['pm', 'fs', 'coulomb', 'kJ/mol']):
        report = bmt.compare_scores(
            result, 'vina.lig_inter', problems=iter(case.problems), ascending=True
        )
        assert result.to_dict() == before
        assert json.loads(json.dumps(report, allow_nan=False)) == report
    report['rows'][0]['definition']['context']['weights'][0] = 999
    report['rows'][0]['prepared_evidence']['export']['source_atom_ids'][0] = 'changed'
    report['display_order'].reverse()
    assert result.to_dict() == before
    assert case.problems[0].evidence['export']['source_atom_ids'] == [
        'test-C',
        'test-N',
    ]
    fresh = bmt.compare_scores(
        result, 'vina.lig_inter', problems=case.problems, ascending=True
    )
    assert fresh['display_order'] == [1, 2, 3, 4, 5]
    assert fresh['rows'][0]['definition']['context']['weights'][0] != 999


@pytest.fixture
def prepared_case(received_records, monkeypatch):
    """Real binding helper, with synthetic provider/export/geometry doubles."""
    import molsysmt as msm

    from bindingmt.engines import _vina_scoring

    pose = bmt.DockingPose.from_dict(deepcopy(received_records[0]))
    entry = pose.to_dict()['metadata']['scoring_history'][0]
    definition = pose.score_definitions['vina.lig_inter']
    captures = entry['backend_artifacts']
    ligand = base64.b64decode(captures['partner']['content_base64'])
    receptor = base64.b64decode(captures['receptor']['content_base64'])
    prepared = bmt.PreparedLigand(
        state_id=pose.partner_state_id,
        atom_names=[f'test-{i}' for i in range(pose.n_atoms)],
        group_name='LIG',
        coordinates=pose.coordinates,
        atom_types=['C'] * pose.n_atoms,
        charges=[0.0] * pose.n_atoms,
        metadata={
            'hydrogen_policy': 'synthetic',
            'torsion_policy': 'rigid',
            'active_torsion_bonds': [],
        },
    )
    box = definition['context']['backend_box']
    problem = bmt.DockingProblem(
        receptor='pdbqt_text:' + receptor.decode(),
        partner=prepared,
        search_domain=bmt.BoxRegion(
            puw.quantity(box['center'], 'angstrom'),
            puw.quantity(box['size'], 'angstrom'),
        ),
    )
    # Attach the opaque double after admission so no molecular operation occurs.
    system = SimpleNamespace(
        molecular_mechanics=SimpleNamespace(
            partial_charge_assignment={'method': 'synthetic'},
            atom_type_assignment={'method': 'synthetic'},
        )
    )
    prepared.source_molsys = system
    exported = SimpleNamespace(
        text=ligand.decode(),
        molecular_system=system,
        atom_map={
            'schema': 'molsysmt.atom_export@1',
            'charge_unit': 'elementary_charge',
            'payload_sha256': hashlib.sha256(ligand).hexdigest(),
        },
    )
    extract_calls = []

    def extract(native, *, selection):
        assert native is system
        extract_calls.append(selection)
        return system

    monkeypatch.setattr(msm, 'extract', extract)
    monkeypatch.setattr(comparison, 'export_pdbqt', lambda *args, **kwargs: exported)
    monkeypatch.setattr(
        comparison,
        'audit_preparation_charges',
        lambda prepared: {'assessment': 'consistent', 'test_scope': 'synthetic'},
    )
    monkeypatch.setattr(
        comparison, 'source_charge_assignment', lambda system: {'method': 'synthetic'}
    )
    monkeypatch.setattr(
        comparison,
        'source_atom_types',
        lambda system, count: (['C'] * count, {'method': 'synthetic'}),
    )
    monkeypatch.setattr(
        _vina_scoring,
        '_input_pose',
        lambda *args: (pose, {'test_scope': 'synthetic geometry'}),
    )
    return SimpleNamespace(
        problem=problem,
        pose=pose,
        entry=entry,
        definition=definition,
        exported=exported,
        system=system,
        extract_calls=extract_calls,
    )


def test_prepared_binding_links_render_map_capture_and_actual_export_view(
    prepared_case,
):
    case = prepared_case
    system, evidence = comparison._prepared_view(
        case.problem, case.pose, case.entry, case.definition, 1
    )
    assert system is case.system
    assert (
        evidence['export']['payload_sha256']
        == case.definition['context']['partner_sha256']
    )
    assert evidence['preparation_policy']['charges']['method'] == 'synthetic'
    assert case.extract_calls == [list(range(case.pose.n_atoms))]


@pytest.mark.parametrize(
    'change', ['render', 'map_hash', 'capture', 'map_schema', 'charge_unit']
)
def test_prepared_binding_refuses_broken_render_map_capture_links(
    prepared_case, change
):
    case = prepared_case
    if change == 'render':
        case.exported.text += '\n'
    elif change == 'map_hash':
        case.exported.atom_map['payload_sha256'] = '0' * 64
    elif change == 'capture':
        case.entry['backend_artifacts']['partner']['content_base64'] = base64.b64encode(
            b'other capture'
        ).decode()
    elif change == 'map_schema':
        case.exported.atom_map['schema'] = 'unknown'
    else:
        case.exported.atom_map['charge_unit'] = 'coulomb'
    with pytest.raises(ArgumentError):
        comparison._prepared_view(
            case.problem, case.pose, case.entry, case.definition, 1
        )
    assert not case.extract_calls


def test_source_free_preparation_never_reaches_the_export_provider(
    prepared_case, monkeypatch
):
    case = prepared_case
    case.problem.partner.source_molsys = None

    def forbidden(*args, **kwargs):
        pytest.fail('A source-free view reached the export provider')

    monkeypatch.setattr(comparison, 'export_pdbqt', forbidden)
    with pytest.raises(ArgumentError, match='complete molecular source'):
        comparison._prepared_view(
            case.problem, case.pose, case.entry, case.definition, 1
        )
    assert not case.extract_calls


@pytest.mark.parametrize('complete', [True, False])
def test_correspondence_requires_a_complete_supplied_candidate_witness(
    monkeypatch, complete
):
    import molsysmt as msm

    calls = []
    system, reference = object(), object()
    candidate = [[0, 0], [1, 1]]
    report = {
        'schema': 'molsysmt.atom_correspondences@1',
        'method': 'declared_graph_isomorphism',
        'rule_version': 'declared_graph_isomorphism@1',
        'evidence': {'kind': 'declared_complete_covalent_graph'},
        'search_scope': 'supplied_atom_correspondences',
        'search_complete': complete,
        'atom_correspondences': [candidate],
        'test_scope': 'synthetic provider return',
    }

    def witness(actual, **kwargs):
        assert actual is system
        calls.append(kwargs)
        return report

    monkeypatch.setattr(msm.chemical_states, 'get_atom_correspondences', witness)
    if complete:
        admitted = comparison._correspondence(
            system, reference, ['C', 'N'], ['C', 'N'], 2
        )
        assert admitted == report and admitted is not report
    else:
        with pytest.raises(ArgumentError, match='complete chemical correspondence'):
            comparison._correspondence(system, reference, ['C', 'N'], ['C', 'N'], 2)
    assert len(calls) == 1
    assert calls[0]['reference_molecular_system'] is reference
    assert calls[0]['candidate_atom_correspondences'] == [candidate]
    assert calls[0]['max_matches'] == 1
