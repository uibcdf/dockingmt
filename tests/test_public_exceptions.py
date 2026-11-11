"""Users can catch real library failures without importing private modules."""

import importlib

import pytest
import pyunitwizard as puw

import bindingmt as bmt


def public_errors():
    return importlib.import_module('bindingmt.exceptions')


@pytest.mark.parametrize(
    'operation,field',
    [
        (lambda: bmt.DockingPose.from_dict({}), 'coordinates'),
        (lambda: bmt.DockingResult.from_dict({'poses': 42}), 'poses'),
        (lambda: bmt.BoxRegion.from_dict({}), 'center'),
        (lambda: bmt.VinaProtocol(cpu=True), 'cpu'),
        (lambda: bmt.DockingOutcome(0), 'result'),
        (lambda: bmt.summarize_redocking({'bad': None}), 'evaluations'),
        (lambda: bmt.dock(None), 'problem'),
    ],
)
def test_public_argument_class_catches_real_api_failures(operation, field):
    errors = public_errors()
    with pytest.raises(errors.ArgumentError) as caught:
        operation()
    assert isinstance(caught.value, errors.BindingMTException)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == field
    assert type(caught.value).__module__ == 'bindingmt._private.smonitor'


def test_root_namespace_and_owned_viewer_error_keep_native_family():
    errors = public_errors()
    assert bmt.exceptions is errors
    pose = bmt.DockingPose(puw.quantity([[0, 0, 0]], 'angstrom'))
    result = bmt.DockingResult([pose])
    with pytest.raises(errors.ViewerPosePositionError) as caught:
        bmt.view(result, pose_rank=2)
    assert isinstance(caught.value, (errors.BindingMTViewerError, ValueError))
    assert isinstance(caught.value, errors.BindingMTViewerError)
    assert isinstance(caught.value, ValueError)
    assert caught.value.code == 'BMT-E007'


def test_public_argument_error_retains_original_provider_cause(monkeypatch):
    errors = public_errors()
    energy = puw.quantity(3, 'kcal/mol')
    failure = ValueError('unit-provider control')

    def reject(*args, **kwargs):
        raise failure

    monkeypatch.setattr(puw, 'ensure_quantity', reject)
    with pytest.raises(errors.ArgumentError) as caught:
        bmt.VinaProtocol(energy_range=energy)
    assert caught.value.__cause__ is failure
    assert caught.value.extra['arg_name'] == 'energy_range'
    assert caught.value.code == 'BMT-E002'


@pytest.mark.parametrize('error_type', [MemoryError, KeyboardInterrupt, SystemExit])
def test_public_diagnostics_do_not_reclassify_native_interruptions(
    monkeypatch, error_type
):
    errors = public_errors()
    energy = puw.quantity(3, 'kcal/mol')
    failure = error_type('native interruption control')

    def reject(*args, **kwargs):
        raise failure

    monkeypatch.setattr(puw, 'ensure_quantity', reject)
    with pytest.raises(error_type) as caught:
        bmt.VinaProtocol(energy_range=energy)
    assert caught.value is failure
    assert not isinstance(caught.value, errors.BindingMTException)
