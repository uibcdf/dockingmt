import copy
import pickle
import warnings
from dataclasses import replace

import depdigest
import pytest
import pyunitwizard as puw
import smonitor

import dockingmt as dmt
from dockingmt._private.smonitor import (
    ArgumentError,
    BackendApproximationWarning,
    CapabilityMismatchError,
    LibraryNotFoundError,
    NotDigestedArgumentWarning,
    warn,
)
from dockingmt._private.smonitor.catalog import CATALOG, CODES


@pytest.mark.parametrize('profile', ['user', 'dev', 'qa', 'agent', 'debug'])
def test_catalog_messages_render_in_all_profiles(profile, monkeypatch):
    manager = smonitor.get_manager()
    monkeypatch.setattr(manager, '_config', replace(manager._config, profile=profile))
    codes = {
        entry['code']
        for group in ('exceptions', 'warnings')
        for entry in CATALOG[group].values()
    }
    assert codes == set(CODES)
    assert all(smonitor.resolve(code=code, extra={})[0] for code in codes)


@pytest.mark.parametrize(
    'build',
    [
        lambda: ArgumentError(
            arg_name='cpu', reason='Use an integer.', caller='example'
        ),
        lambda: LibraryNotFoundError(library='vina', caller='dock'),
        lambda: CapabilityMismatchError(capability='flexible_receptor', engine='vina'),
        lambda: BackendApproximationWarning(domain_type='sphere', engine='vina'),
        lambda: NotDigestedArgumentWarning(argument='selection', caller='example'),
    ],
)
def test_diagnostics_rebuild_and_preserve_structured_data(build):
    original = build()
    assert original.code in CODES
    assert str(original)
    assert str(type(original)(*original.args)) == str(original)
    for restored in (pickle.loads(pickle.dumps(original)), copy.deepcopy(original)):
        assert str(restored) == str(original)
        assert restored.code == original.code
        assert restored.extra == original.extra


def test_warning_emission_preserves_fields_and_python_filters():
    events = []

    class Collector:
        def handle(self, event, **kwargs):
            events.append(event)

    manager = smonitor.get_manager()
    handler = Collector()
    manager.add_handler(handler)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', BackendApproximationWarning)
            with pytest.raises(BackendApproximationWarning):
                warn(BackendApproximationWarning(domain_type='sphere', engine='vina'))
    finally:
        manager.remove_handler(handler)
    matching = [event for event in events if event.get('code') == 'DMT-W001']
    assert matching
    assert matching[-1]['extra']['domain_type'] == 'sphere'
    assert matching[-1]['extra']['engine'] == 'vina'


@pytest.mark.parametrize('library', ['vina', 'molsysviewer'])
def test_missing_optional_dependency_has_local_code_and_install_advice(
    library, monkeypatch
):
    from depdigest.core import checker

    installed = checker.is_installed
    monkeypatch.setattr(
        checker,
        'is_installed',
        lambda name: False if name == library else installed(name),
    )
    with pytest.raises(LibraryNotFoundError) as caught:
        if library == 'molsysviewer':
            dmt.view()
        else:
            problem = dmt.DockingProblem(
                receptor='rec.pdbqt',
                partner='lig.pdbqt',
                search_domain=dmt.BoxRegion(
                    center=puw.quantity([0, 0, 0], 'nm'),
                    size=puw.quantity([1, 1, 1], 'nm'),
                ),
            )
            dmt.VinaBackend().dock(problem)
    assert caught.value.code == 'DMT-E001'
    assert caught.value.extra['library'] == library
    assert f'pip install {library}' in str(caught.value)


def test_optional_dependency_inventory_is_complete():
    info = depdigest.get_info('dockingmt', format='dict')
    dependencies = {entry['library']: entry for entry in info['dependencies']}
    for library in ('vina', 'molsysviewer'):
        assert dependencies[library]['type'] == 'soft'
