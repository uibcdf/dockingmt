import copy
import pickle
import warnings
from dataclasses import replace
from importlib.metadata import requires

import depdigest
import pytest
import pyunitwizard as puw
import smonitor
from packaging.requirements import Requirement

import dockingmt as dmt
from dockingmt._private.smonitor import (
    ArgumentError,
    BackendApproximationWarning,
    CapabilityMismatchError,
    LibraryNotFoundError,
    NotDigestedArgumentWarning,
    TemporaryFileCleanupWarning,
    ViewerActionError,
    ViewerCapabilityError,
    ViewerInputMissingError,
    ViewerPoseCountError,
    ViewerPosePositionError,
    ViewerShapeOwnershipError,
    ViewerStateError,
    ViewerStructureCountError,
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
        lambda: TemporaryFileCleanupWarning(
            failures=[
                {'path': 'owned.pdbqt', 'errno': 13, 'error_type': 'PermissionError'}
            ]
        ),
        lambda: ViewerPoseCountError(n_poses=True, operation='build_reference'),
        lambda: ViewerStructureCountError(
            role='reference', expected=[1, 3], observed=2, operation='build_reference'
        ),
        lambda: ViewerInputMissingError(resource='receptor', operation='render_result'),
        lambda: ViewerPosePositionError(position=-1, operation='set_active_pose'),
        lambda: ViewerShapeOwnershipError(tag='foreign', operation='render_domain'),
        lambda: ViewerStateError(resource='search domain', operation='toggle_domain'),
        lambda: ViewerCapabilityError(capability='shapes', operation='render_domain'),
        lambda: ViewerActionError(
            panel='explorer', action_id='unknown', operation='panel_action'
        ),
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


@pytest.mark.parametrize(
    'library,operation', [('vina', 'dock'), ('vina', 'score'), ('molsysviewer', 'view')]
)
def test_missing_optional_dependency_has_local_code_and_install_advice(
    library, operation, monkeypatch
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
            getattr(dmt.VinaBackend(), operation)(problem)
    assert caught.value.code == 'DMT-E001'
    assert caught.value.extra['library'] == library
    if library == 'vina':
        assert 'pip install vina' in str(caught.value)
    else:
        assert 'conda install -c uibcdf molsysviewer' in str(caught.value)
        assert 'pip install molsysviewer' not in str(caught.value)


def test_optional_dependency_inventory_is_complete():
    info = depdigest.get_info('dockingmt', format='dict')
    dependencies = {entry['library']: entry for entry in info['dependencies']}
    requirements = [Requirement(value) for value in requires('dockingmt')]
    hard = {
        item.name
        for item in requirements
        if item.marker is None or item.marker.evaluate({'extra': ''})
    }
    optional = {
        item.name
        for item in requirements
        if item.marker is not None
        and any(item.marker.evaluate({'extra': extra}) for extra in ('vina', 'viewer'))
    } - hard
    assert {
        name for name, entry in dependencies.items() if entry['type'] == 'hard'
    } == hard
    assert {
        name for name, entry in dependencies.items() if entry['type'] == 'soft'
    } == optional


@pytest.mark.parametrize(
    'library',
    ['molsysmt', 'molsysviewer', 'argdigest', 'depdigest', 'smonitor', 'pyunitwizard'],
)
def test_suite_dependency_installation_routes_match_actual_distribution(library):
    info = depdigest.get_info('dockingmt', format='dict')
    entry = next(item for item in info['dependencies'] if item['library'] == library)
    assert entry['package_name'] == {'pypi': None, 'conda': library}
    assert entry['install']['pypi'] is None
    assert entry['install']['conda'] == f'conda install -c uibcdf {library}'
