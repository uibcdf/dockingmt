"""Canonical BindingMT public identities, records and optional independence."""

import subprocess
import sys
from pathlib import Path

import pytest


def test_public_classes_and_diagnostics_have_canonical_ownership():
    import bindingmt as bmt
    from bindingmt._private.smonitor import ArgumentError
    from bindingmt.core.results import DockingPose

    assert bmt.DockingPose is DockingPose
    assert bmt.exceptions.ArgumentError is ArgumentError
    assert bmt.DockingProblem.__module__.startswith('bindingmt.')
    assert ArgumentError.__module__.startswith('bindingmt.')
    assert ArgumentError(code='BMT-E002').code == 'BMT-E002'
    record = bmt.DockingResult(
        [], provenance={'bindingmt_version': bmt.__version__, 'producer': 'control'}
    ).to_dict()
    assert bmt.DockingResult.from_dict(record).to_dict() == record


def test_import_and_record_reading_do_not_load_optional_engines_or_viewer():
    program = """
import importlib.abc
import sys
blocked={'molsysviewer','vina','rdkit','torch','boltz','haddock'}
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in blocked:
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0,Absent())
import bindingmt as bmt
record=bmt.DockingResult([]).to_dict()
assert bmt.DockingResult.from_dict(record).to_dict()==record
assert not blocked & sys.modules.keys()
"""
    result = subprocess.run(
        [sys.executable, '-c', program],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_addon_uses_the_same_canonical_component_and_state_identity():
    pytest.importorskip('molsysviewer')
    import molsysviewer_bindingmt as addon

    assert addon.addon.name == addon.addon.package == 'bindingmt'
    assert addon.addon.workspaces[0].id == 'bindingmt'
    assert addon.BindingMTAddonRuntime().workspace == 'bindingmt'
    assert isinstance(
        addon.create_bindingmt_state(object()), addon.BindingMTAddonRuntime
    )
