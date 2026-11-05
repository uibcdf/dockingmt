import subprocess
import sys
import tomllib
from pathlib import Path

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
    assert 'exceptions' in CATALOG
    assert 'LibraryNotFoundError' in CATALOG['exceptions']


def test_depdigest_configuration():
    from dockingmt import _depdigest

    assert 'vina' in _depdigest.LIBRARIES
    assert _depdigest.LIBRARIES['vina']['type'] == 'soft'
    assert 'meeko' not in _depdigest.LIBRARIES
    assert 'molsysmt' in _depdigest.LIBRARIES
    assert _depdigest.LIBRARIES['molsysmt']['type'] == 'hard'


def test_vina_extra_does_not_install_meeko():
    pyproject = Path(__file__).resolve().parents[1] / 'pyproject.toml'
    project = tomllib.loads(pyproject.read_text())['project']
    assert 'meeko' not in project['optional-dependencies']['vina']


def test_no_leaky_optional_imports():
    # A fresh import must be independent of previous real-engine tests.
    script = """
import importlib.abc
import sys
blocked = {'vina', 'meeko', 'pdbfixer', 'molsysviewer', 'rdkit', 'openmm'}
class BlockOptional(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, BlockOptional())
import dockingmt as dmt
record = dmt.DockingResult([]).to_dict()
assert dmt.DockingResult.from_dict(record).to_dict() == record
for outcome in (
    dmt.DockingOutcome(0, result=dmt.DockingResult([]), backend='control'),
    dmt.DockingOutcome(1, error={'type': 'ValueError', 'message': '', 'code': None}),
):
    record = outcome.to_dict()
    assert dmt.DockingOutcome.from_dict(record).to_dict() == record
assert not blocked & sys.modules.keys()
"""
    completed = subprocess.run(
        [
            sys.executable,
            '-c',
            script,
        ],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
