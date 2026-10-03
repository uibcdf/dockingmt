"""Incremental prepared execution preserves individual docking boundaries."""

import importlib
import json
import weakref
from copy import deepcopy

import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError
from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError


def problem(label='ligand-control', partner=MINIMAL_LIG_PDBQT):
    return dmt.DockingProblem(
        MINIMAL_REC_PDBQT,
        partner,
        dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
        metadata={
            'ligand_id': label,
            'partner_state_id': label + '-state',
            'receptor_state_id': 'receptor-control',
            'nested': {'declaration': [1]},
        },
    )


class ControlBackend(dmt.DockingBackend):
    name = 'control'
    capabilities = set()
    is_available = True

    def __init__(self, fail=None):
        self.calls = []
        self.fail = fail

    def dock(self, problem, protocol=None):
        self.calls.append(problem.metadata['ligand_id'])
        if problem.metadata['ligand_id'] == 'bad':
            raise self.fail if self.fail is not None else ValueError('control failure')
        return dmt.DockingResult(
            [],
            problem_info=deepcopy(problem.to_dict()),
            protocol_info=protocol.to_dict(),
        )


def test_batch_is_lazy_ordered_and_uses_public_dock(monkeypatch):
    source_events = []
    backend = ControlBackend()
    public = importlib.import_module('dockingmt.batch')
    calls = []
    original = public.dock

    def observed(*args, **kwargs):
        calls.append(kwargs['problem'])
        return original(*args, **kwargs)

    monkeypatch.setattr(public, 'dock', observed)

    def source():
        for label in ('first', 'second', 'third'):
            source_events.append(label)
            yield problem(label)

    stream = dmt.dock_many(source(), backend=backend)
    assert source_events == [] and backend.calls == []
    first = next(stream)
    assert isinstance(first, dmt.DockingOutcome)
    assert first.index == 0 and first.status == 'success' and first.error is None
    assert first.backend == 'control'
    assert first.result.problem is calls[0]
    assert source_events == backend.calls == ['first']
    second = next(stream)
    assert second.index == 1 and second.result is not first.result
    assert source_events == backend.calls == ['first', 'second']
    stream.close()
    assert source_events == ['first', 'second']


def test_recorded_failure_preserves_prior_results_and_next_item():
    backend = ControlBackend()
    items = [problem(label) for label in ('first', 'bad', 'third')]
    stream = dmt.dock_many(items, backend=backend, on_error='record')
    first = next(stream)
    before = first.to_dict()
    failed = next(stream)
    assert failed.index == 1 and failed.status == 'failure' and failed.result is None
    assert failed.error == {
        'type': 'builtins.ValueError',
        'message': 'control failure',
        'code': None,
    }
    assert failed.problem_info['metadata']['ligand_id'] == 'bad'
    assert failed.backend == 'control'
    assert next(stream).index == 2
    assert list(stream) == []
    assert backend.calls == ['first', 'bad', 'third']
    assert first.to_dict() == before
    assert 'traceback' not in json.dumps(failed.to_dict())


def test_default_failure_propagates_original_and_stops_source():
    error = RuntimeError('original failure')
    backend = ControlBackend(error)
    consumed = []

    def source():
        for label in ('first', 'bad', 'third'):
            consumed.append(label)
            yield problem(label)

    stream = dmt.dock_many(source(), backend=backend)
    first = next(stream)
    with pytest.raises(RuntimeError) as caught:
        next(stream)
    assert caught.value is error
    assert consumed == ['first', 'bad']
    assert first.status == 'success' and list(stream) == []


@pytest.mark.parametrize('policy', ['raise', 'record'])
@pytest.mark.parametrize('error', [KeyboardInterrupt(), SystemExit(), MemoryError()])
def test_control_and_resource_exceptions_propagate(policy, error):
    stream = dmt.dock_many(
        [problem('bad')], backend=ControlBackend(error), on_error=policy
    )
    with pytest.raises(type(error)) as caught:
        next(stream)
    assert caught.value is error


def test_source_failure_is_not_an_item_failure_and_source_is_borrowed():
    error = RuntimeError('source failed')

    def source():
        yield problem('first')
        raise error

    supplied = source()
    stream = dmt.dock_many(supplied, backend=ControlBackend(), on_error='record')
    first = next(stream)
    with pytest.raises(RuntimeError) as caught:
        next(stream)
    assert caught.value is error and first.status == 'success'

    supplied = iter([problem('first'), problem('second')])
    stream = dmt.dock_many(supplied, backend=ControlBackend())
    next(stream)
    stream.close()
    assert next(supplied).metadata['ligand_id'] == 'second'


def test_batch_does_not_retain_completed_result_history():
    stream = dmt.dock_many(
        (problem(str(i)) for i in range(8)), backend=ControlBackend()
    )
    first = next(stream)
    previous = weakref.ref(first.result)
    del first
    next(stream)
    assert previous() is None
    stream.close()


@pytest.mark.parametrize('items', [None, 'file.pdbqt', {}, 3, problem()])
def test_invalid_global_input_is_rejected_at_call(items):
    with pytest.raises(ArgumentError):
        dmt.dock_many(items)


@pytest.mark.parametrize(
    'kwargs', [{'on_error': 'ignore'}, {'protocol': 'vina'}, {'backend': 'other'}]
)
def test_invalid_global_options_are_rejected_at_call(kwargs):
    with pytest.raises(ArgumentError):
        dmt.dock_many([], **kwargs)


def test_unknown_keywords_are_rejected():
    with pytest.raises(UnknownArgumentError):
        dmt.dock_many([], on_eror='record')


def test_invalid_item_is_recorded_without_execution():
    backend = ControlBackend()
    outcomes = list(
        dmt.dock_many([None, problem('valid')], backend=backend, on_error='record')
    )
    assert [item.status for item in outcomes] == ['failure', 'success']
    assert outcomes[0].problem_info == {}
    assert outcomes[0].error['code'] == 'DMT-E002'
    assert backend.calls == ['valid']


def test_snapshots_are_detached_and_inputs_settings_are_not_modified():
    supplied = problem()
    protocol = dmt.VinaProtocol(seed=23)
    before_problem = deepcopy(supplied.to_dict())
    before_protocol = protocol.to_dict()
    item = next(dmt.dock_many([supplied], protocol, backend=ControlBackend()))
    assert (
        supplied.to_dict() == before_problem and protocol.to_dict() == before_protocol
    )
    supplied.metadata['nested']['declaration'][0] = 20
    declaration = item.problem_info
    declaration['metadata']['nested']['declaration'][0] = 99
    assert item.problem_info['metadata']['nested']['declaration'] == [1]
    exported = item.to_dict()
    restored = dmt.DockingOutcome.from_dict(exported)
    exported['problem_info']['metadata']['nested']['declaration'][0] = 30
    assert restored.problem_info['metadata']['nested']['declaration'] == [1]
    assert restored.result.problem is None


@pytest.mark.parametrize('scoring', ['vina', 'vinardo'])
def test_native_batch_matches_individual_seeded_docking(scoring):
    protocol = dmt.VinaProtocol(
        seed=123,
        cpu=1,
        exhaustiveness=1,
        n_poses=2,
        scoring=scoring,
        capture_backend_inputs=True,
    )
    items = [problem('first'), problem('second')]
    individual = [dmt.dock(item, protocol) for item in items]
    outcomes = list(dmt.dock_many(iter(items), protocol, backend='vina'))
    for index, (outcome, expected) in enumerate(zip(outcomes, individual)):
        actual = outcome.result.to_dict()
        reference = expected.to_dict()
        actual['provenance'].pop('elapsed_seconds')
        reference['provenance'].pop('elapsed_seconds')
        assert actual == reference
        assert outcome.index == index and outcome.error is None
        assert outcome.backend == 'vina'
        assert (
            outcome.problem_info['metadata']['ligand_id']
            == items[index].metadata['ligand_id']
        )
        assert dmt.audit_result(outcome.result.to_dict())['status'] == 'consistent'
        assert (
            dmt.DockingOutcome.from_dict(outcome.to_dict()).to_dict()
            == outcome.to_dict()
        )


def test_empty_source_never_executes_backend():
    backend = ControlBackend()
    assert list(dmt.dock_many([], backend=backend)) == []
    assert backend.calls == []


@pytest.mark.parametrize('role', ['receptor', 'partner'])
def test_automatic_preparation_is_rejected_before_backend_or_molecular_work(
    role, monkeypatch
):
    import molsysmt as msm

    item = problem()
    setattr(item, '_' + role, object())

    def forbidden(*args, **kwargs):
        pytest.fail('Batch attempted automatic preparation or molecular work.')

    for name in ('get', 'convert', 'select', 'extract', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    backend = ControlBackend()
    outcome = next(dmt.dock_many([item], backend=backend, on_error='record'))
    assert outcome.status == 'failure' and outcome.error['code'] == 'DMT-E002'
    assert backend.calls == []


def test_prepared_objects_are_accepted_without_preparation(monkeypatch):
    item = problem()
    coordinates = puw.quantity([[0, 0, 0]], 'angstrom')
    receptor = dmt.PreparedReceptor(
        'prepared-receptor', ['C'], ['ALA'], [1], coordinates, ['C'], [0.0]
    )
    ligand = dmt.PreparedLigand(
        'prepared-ligand', ['C'], 'LIG', coordinates, ['C'], [0.0]
    )
    item = dmt.DockingProblem(
        receptor, ligand, item.search_domain, metadata=item.metadata
    )
    batch = importlib.import_module('dockingmt.batch')

    def observed(problem, **kwargs):
        assert problem.receptor is receptor and problem.partner is ligand
        return dmt.DockingResult([])

    monkeypatch.setattr(batch, 'dock', observed)
    outcome = next(dmt.dock_many([item], backend=ControlBackend()))
    assert outcome.status == 'success'
    assert outcome.problem_info['partner']['value']['state_id'] == 'prepared-ligand'


@pytest.mark.parametrize(
    'changes',
    [
        {'index': True},
        {'index': -1},
        {'index': 1.5},
        {'status': 'failure'},
        {'error': {}},
        {'schema_version': '99'},
        {'result': {'schema_version': '99'}},
    ],
)
def test_outcome_reader_rejects_malformed_or_contradictory_records(changes):
    item = next(dmt.dock_many([problem()], backend=ControlBackend()))
    record = item.to_dict()
    record.update(changes)
    with pytest.raises(ArgumentError):
        dmt.DockingOutcome.from_dict(record)


def test_failure_roundtrip_is_offline_detached_and_retains_catalog_code(monkeypatch):
    import molsysmt as msm

    error = ArgumentError(arg_name='control', reason='invalid item')
    outcome = next(
        dmt.dock_many(
            [problem('bad')], backend=ControlBackend(error), on_error='record'
        )
    )
    saved = json.loads(json.dumps(outcome.to_dict()))
    baseline = deepcopy(saved)

    def forbidden(*args, **kwargs):
        pytest.fail('Outcome restoration attempted molecular or backend work.')

    for name in ('get', 'convert', 'select', 'extract'):
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(dmt.VinaBackend, 'dock', forbidden)
    restored = dmt.DockingOutcome.from_dict(saved)
    assert restored.to_dict() == baseline
    assert restored.error['code'] == 'DMT-E002'
    saved['error']['message'] = 'changed'
    detached = restored.error
    detached['code'] = 'changed'
    assert restored.to_dict() == baseline


def test_native_missing_file_failure_does_not_contaminate_next_execution(tmp_path):
    items = [
        problem('first'),
        problem('bad', tmp_path / 'missing.pdbqt'),
        problem('third'),
    ]
    protocol = dmt.VinaProtocol(
        seed=123, cpu=1, exhaustiveness=1, n_poses=1, capture_backend_inputs=True
    )
    outcomes = list(dmt.dock_many(items, protocol, on_error='record'))
    assert [item.status for item in outcomes] == ['success', 'failure', 'success']
    assert outcomes[1].problem_info['metadata']['ligand_id'] == 'bad'
    assert dmt.audit_result(outcomes[2].result.to_dict())['status'] == 'consistent'
    first = outcomes[0].result.to_dict()
    third = outcomes[2].result.to_dict()
    assert first['poses'][0]['scores'] == third['poses'][0]['scores']
    assert first['poses'][0]['coordinates'] == third['poses'][0]['coordinates']


def test_iterator_does_not_retain_failed_execution_traceback():
    class Marker:
        pass

    class FailureBackend(ControlBackend):
        def dock(self, problem, protocol=None):
            marker = Marker()
            self.marker = weakref.ref(marker)
            raise ValueError('temporary frame')

    backend = FailureBackend()
    stream = dmt.dock_many([problem()], backend=backend, on_error='record')
    failed = next(stream)
    assert failed.status == 'failure'
    assert backend.marker() is None
    stream.close()


def test_batch_preserves_caller_unit_policy_and_unknown_state():
    item = problem()
    item.metadata.pop('partner_state_id')
    item.metadata.pop('receptor_state_id')
    with puw.context(standard_units=['pm', 'fs', 'kJ/mol']):
        before = deepcopy(puw.configure.get_standard_units())
        outcome = next(dmt.dock_many([item], backend=ControlBackend()))
        assert puw.configure.get_standard_units() == before
        assert 'partner_state_id' not in outcome.problem_info['metadata']
        assert outcome.problem_info['search_domain'] == item.search_domain.to_dict()


def test_custom_result_export_is_detached():
    class SharedExport(dmt.DockingResult):
        def to_dict(self):
            return shared

    shared = {'schema_version': '1.0', 'poses': [], 'extension': {'value': [1]}}
    outcome = dmt.DockingOutcome(0, result=SharedExport([]))
    record = outcome.to_dict()
    record['result']['extension']['value'][0] = 10
    assert shared['extension']['value'] == [1]


def test_unavailable_selected_engine_is_recorded_without_fallback(monkeypatch):
    from depdigest.core import checker

    installed = checker.is_installed
    monkeypatch.setattr(
        checker,
        'is_installed',
        lambda name: False if name == 'vina' else installed(name),
    )
    outcome = next(dmt.dock_many([problem()], backend='vina', on_error='record'))
    assert outcome.status == 'failure'
    assert outcome.error['code'] == 'DMT-E001'
    assert outcome.result is None
