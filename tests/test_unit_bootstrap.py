"""Fresh processes preserve application units and an existing Pint registry."""

import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    'mode', ['existing_pint', 'application_pint', 'application_unyt']
)
def test_import_preserves_registry_and_application_authority(mode):
    program = r"""
import sys
import warnings
from math import isclose
import pyunitwizard as puw
mode = sys.argv[1]
keys = ('default_form', 'default_parser', 'standard_units')
if mode == 'existing_pint':
    quantity = puw.quantity(1, 'nm')
    assert not puw.configure.has_active_policy()
    assert 'pint' in puw.configure.report()['loaded_libraries']
    before = None
else:
    puw.configure.set_default_form(mode.removeprefix('application_'))
    puw.configure.set_default_parser('pint')
    puw.configure.set_standard_units(['pm', 'fs'], provenance='application')
    before = {key: puw.configure.report()[key] for key in keys}
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    import bindingmt as bmt
assert not any('registry has been built' in str(w.message) for w in caught)
if before is not None:
    assert {key: puw.configure.report()[key] for key in keys} == before
assert isclose(float(puw.get_value(puw.quantity(1, 'nm'), to_unit='pm')), 1000, rel_tol=8*sys.float_info.epsilon)
assert isclose(float(puw.get_value(puw.quantity(1000, 'pm'), to_unit='nm')), 1, rel_tol=8*sys.float_info.epsilon)
"""
    result = subprocess.run(
        [sys.executable, '-B', '-c', program, mode],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (result.stdout, result.stderr)
