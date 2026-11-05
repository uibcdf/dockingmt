"""Batch outcome admission retains offline, caller-specific record semantics."""

from copy import deepcopy

import numpy as np
import pytest
from argdigest import UnknownArgumentError

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError

ERROR = {'type': 'builtins.ValueError', 'message': 'control', 'code': None}


@pytest.mark.parametrize('factory', [dmt.DockingOutcome, dmt.DockingOutcome.from_dict])
def test_unknown_keywords_use_argdigest(factory):
    with pytest.raises(UnknownArgumentError):
        factory(indez=0)


@pytest.mark.parametrize('record', [None, [], 'record', 1])
def test_reader_admits_its_named_record_argument(record):
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingOutcome.from_dict(record)
    assert caught.value.extra['arg_name'] == 'record'


@pytest.mark.parametrize('index', [True, False, -1, 1.5, '0', np.int64(0)])
def test_index_remains_a_builtin_nonnegative_integer(index):
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingOutcome(index, error=ERROR)
    assert caught.value.extra['arg_name'] == 'index'


@pytest.mark.parametrize('backend', [None, 'custom.adapter', 'VINA'])
def test_inherited_failure_constructor_keeps_optional_result_and_backend(backend):
    class ExtensionOutcome(dmt.DockingOutcome):
        __module__ = 'consumer_extension.models'

    class OverrideOutcome(ExtensionOutcome):
        def __init__(self, index, **kwargs):
            super().__init__(index, **kwargs)

    for model in (dmt.DockingOutcome, ExtensionOutcome, OverrideOutcome):
        error = deepcopy(ERROR)
        declaration = {'nested': ['original']}
        outcome = model(0, backend=backend, error=error, problem_info=declaration)
        assert outcome.result is None and outcome.backend == backend
        error['message'] = 'changed'
        declaration['nested'].append('changed')
        assert outcome.error == ERROR
        assert outcome.problem_info == {'nested': ['original']}
        record = outcome.to_dict()
        original = deepcopy(record)
        restored = model.from_dict(record)
        assert isinstance(restored, model)
        assert restored.to_dict() == original and record == original
        with pytest.raises(UnknownArgumentError):
            model(0, error=ERROR, native_constructor='spoof')


@pytest.mark.parametrize('backend', ['', ' ', object(), 3])
def test_outcome_backend_is_a_label_without_relaxing_execution(backend):
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingOutcome(0, backend=backend, error=ERROR)
    assert caught.value.extra['arg_name'] == 'backend'


def test_outcome_optionality_does_not_relax_other_public_boundaries():
    with pytest.raises(ArgumentError) as caught:
        dmt.evaluate_redocking(None, reference=None)
    assert caught.value.extra['arg_name'] == 'result'
    with pytest.raises(ArgumentError) as caught:
        dmt.dock_many([], backend='custom.adapter')
    assert caught.value.extra['arg_name'] == 'backend'


@pytest.mark.parametrize(
    'error', [{}, dict(ERROR, message=3), dict(ERROR, code=' '), dict(ERROR, extra=1)]
)
def test_error_summary_retains_its_closed_typed_schema(error):
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingOutcome(0, error=error)
    assert caught.value.extra['arg_name'] == 'error'


@pytest.mark.parametrize(
    'payload', [{}, {'result': dmt.DockingResult([]), 'error': ERROR}]
)
def test_exactly_one_result_or_error_remains_required(payload):
    with pytest.raises(ArgumentError):
        dmt.DockingOutcome(0, **payload)


def test_success_reader_stays_offline_and_borrows_the_live_result(monkeypatch):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Outcome admission requested molecular work')

    for operation in ('get', 'get_form', 'select', 'convert', 'copy', 'set'):
        monkeypatch.setattr(msm, operation, forbidden)
    result = dmt.DockingResult([])
    outcome = dmt.DockingOutcome(1, result=result, backend='custom.adapter')
    assert outcome.result is result
    record = outcome.to_dict()
    restored = dmt.DockingOutcome.from_dict(record)
    assert restored.to_dict() == record
    assert restored.result is not result and restored.result.problem is None
