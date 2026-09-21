import sys

import pyunitwizard


def test_package_import_and_version():
    import dockingmt

    assert hasattr(dockingmt, '__version__')
    assert isinstance(dockingmt.__version__, str)


def test_pyunitwizard_policy_active():

    assert pyunitwizard.configure.has_active_policy()
    # Test standard units
    q = pyunitwizard.quantity(1.0, 'nm')
    assert pyunitwizard.get_value(q) == 1.0
    # Test fast tracks
    assert pyunitwizard.unit('nanometers') == pyunitwizard.unit('nm')
    assert pyunitwizard.unit('angstroms') == pyunitwizard.unit('angstrom')


def test_smonitor_configuration():
    from dockingmt._private.smonitor import CATALOG, META

    assert META['project_name'] == 'DockingMT'
    assert 'signals' in CATALOG
    assert 'errors' in CATALOG
    assert 'LibraryNotFoundError' in CATALOG['errors']


def test_depdigest_configuration():
    from dockingmt import _depdigest

    assert 'vina' in _depdigest.LIBRARIES
    assert _depdigest.LIBRARIES['vina']['type'] == 'soft'
    assert 'molsysmt' in _depdigest.LIBRARIES
    assert _depdigest.LIBRARIES['molsysmt']['type'] == 'hard'


def test_no_leaky_optional_imports():
    # Verify that importing dockingmt does not import heavy optional backends
    for module_name in ['vina', 'meeko', 'pdbfixer']:
        assert module_name not in sys.modules
