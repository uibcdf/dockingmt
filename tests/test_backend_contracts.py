import builtins
import importlib

import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

from dockingmt import (
    BoxRegion,
    DockingProblem,
    DockingProtocol,
    VinaBackend,
    VinaProtocol,
    dock,
)
from dockingmt._private.smonitor import ArgumentError, CapabilityMismatchError


class OtherProtocol(DockingProtocol):
    name = 'OtherProtocol'
    required_capabilities = {'rigid_receptor'}
    parameters = {}

    def validate_problem(self, problem):
        pytest.fail('An unsupported protocol hook was called')

    def to_dict(self):
        return {'protocol_type': self.name}


@pytest.fixture
def prepared_problem():
    return DockingProblem(
        receptor='unused_receptor.pdbqt',
        partner='unused_ligand.pdbqt',
        search_domain=BoxRegion(
            center=puw.quantity([0, 0, 0], 'nm'),
            size=puw.quantity([1, 1, 1], 'nm'),
        ),
    )


@pytest.fixture
def no_execution(monkeypatch):
    from depdigest.core import checker

    available = checker.is_installed
    monkeypatch.setattr(
        checker,
        'is_installed',
        lambda name: True if name == 'vina' else available(name),
    )
    engine = importlib.import_module('dockingmt.engines.vina')

    def forbidden(*args, **kwargs):
        pytest.fail('Unsupported request reached problem handling or input preparation')

    monkeypatch.setattr(VinaProtocol, 'validate_problem', forbidden)
    for operation in (
        '_vina_box',
        'prepare_ligand',
        'prepare_receptor',
        '_stage_pdbqt_bytes',
    ):
        monkeypatch.setattr(engine, operation, forbidden)
    monkeypatch.setattr(VinaBackend, '_resolve_receptor_path', forbidden)
    for operation in ('get_form', 'get', 'select', 'extract', 'convert'):
        monkeypatch.setattr(engine.msm, operation, forbidden)
    actual_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name == 'vina' or name.startswith('vina.'):
            pytest.fail('Unsupported request imported the native provider')
        return actual_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded_import)


@pytest.mark.parametrize(
    'dispatch',
    [
        lambda problem, protocol: VinaBackend().dock(problem, protocol),
        lambda problem, protocol: dock(problem, protocol, backend='vina'),
    ],
)
def test_ad4_rejected_before_problem_hooks_preparation_or_provider(
    dispatch, no_execution, prepared_problem
):
    protocol = VinaProtocol(scoring='ad4')
    with pytest.raises(CapabilityMismatchError) as caught:
        dispatch(prepared_problem, protocol)
    assert caught.value.code == 'DMT-E003'
    assert caught.value.extra['capability'] == 'scoring_ad4'
    assert caught.value.extra['engine'] == 'vina'
    assert caught.value.extra['missing_capabilities'] == ['scoring_ad4']


def test_ad4_intent_remains_serializable_without_claiming_backend_support():
    protocol = VinaProtocol(scoring='ad4')
    restored = VinaProtocol.from_dict(protocol.to_dict())
    assert restored.parameters == protocol.parameters
    assert 'scoring_ad4' in restored.required_capabilities
    with pytest.raises(CapabilityMismatchError):
        VinaBackend().validate_capabilities(restored)


@pytest.mark.parametrize('scoring', ['vina', 'vinardo'])
def test_supported_scoring_capabilities_accept_protocol(scoring):
    backend = VinaBackend()
    protocol = VinaProtocol(scoring=scoring)
    backend.validate_capabilities(protocol)
    assert protocol.required_capabilities <= backend.capabilities


def test_incompatible_protocol_fails_before_its_validation_hook(
    no_execution, prepared_problem
):
    with pytest.raises(ArgumentError) as caught:
        VinaBackend().dock(prepared_problem, OtherProtocol())
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == 'protocol'


@pytest.mark.parametrize('protocol', [None, 'vina', object()])
def test_capability_validation_requires_protocol_instance(protocol):
    with pytest.raises(ArgumentError) as caught:
        VinaBackend().validate_capabilities(protocol)
    assert caught.value.extra['arg_name'] == 'protocol'


def test_capability_validation_rejects_unknown_keywords():
    with pytest.raises(UnknownArgumentError):
        VinaBackend().validate_capabilities(protcol=VinaProtocol())


def test_capability_diagnostics_include_every_missing_request():
    class MissingCapabilities(OtherProtocol):
        required_capabilities = {'flexible_receptor', 'quantum_scoring'}

    backend = VinaBackend()
    with pytest.raises(CapabilityMismatchError) as caught:
        backend.validate_capabilities(MissingCapabilities())
    extra = caught.value.extra
    assert extra['missing_capabilities'] == ['flexible_receptor', 'quantum_scoring']
    assert extra['supported_capabilities'] == sorted(backend.capabilities)
    assert extra['protocol'] == 'OtherProtocol'
