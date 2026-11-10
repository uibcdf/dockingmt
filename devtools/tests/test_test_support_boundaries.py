"""Shared installed fixtures must not depend on pytest's source-path imports."""

import ast
import importlib
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]


def test_shared_helpers_never_import_sibling_test_modules():
    violations = []
    for folder in ('tests', 'dmt_test_support'):
        for source in (ROOT / folder).rglob('*.py'):
            for node in ast.walk(ast.parse(source.read_text())):
                names = []
                if isinstance(node, ast.ImportFrom):
                    names = [node.module or '']
                elif isinstance(node, ast.Import):
                    names = [item.name for item in node.names]
                for name in names:
                    parts = name.split('.')
                    if (
                        parts[0].startswith('test_')
                        or parts[0] == 'molecular_fixtures'
                        or (parts[0] == 'tests' and len(parts) > 1)
                    ):
                        violations.append(
                            (str(source.relative_to(ROOT)), node.lineno, name)
                        )
    assert not violations, violations


def test_declared_fixture_uses_the_same_staged_data_path(monkeypatch):
    # Exercise only the fixture's file routing. The provider stub performs no
    # molecular operation and keeps the original convert/set request observable.
    helper = importlib.import_module('dmt_test_support.molecular_fixtures')
    calls = []
    sentinel = object()

    def convert(path, **kwargs):
        calls.append(('convert', path, kwargs))
        assert Path(path).is_file()
        return sentinel

    def set_attributes(system, **kwargs):
        assert system is sentinel
        calls.append(('set', kwargs))

    monkeypatch.setitem(
        sys.modules, 'molsysmt', SimpleNamespace(convert=convert, set=set_attributes)
    )
    assert helper.declared_methanol() is sentinel
    assert calls == [
        (
            'convert',
            ROOT / 'tests/data/charges/methanol.sdf',
            {'to_form': 'molsysmt.MolSys'},
        ),
        (
            'set',
            {
                'element': 'atom',
                'n_explicit_hydrogens': 0,
                'n_implicit_hydrogens': 0,
                'allows_implicit_hydrogens': False,
            },
        ),
    ]


def test_fixture_file_routing_survives_an_export_without_runtime_source(tmp_path):
    namespace = tmp_path / 'dmt_test_support'
    namespace.mkdir()
    for name in ('__init__.py', 'molecular_fixtures.py'):
        shutil.copyfile(ROOT / 'dmt_test_support' / name, namespace / name)
    source = ROOT / 'tests/data/charges/methanol.sdf'
    target = tmp_path / 'tests/data/charges/methanol.sdf'
    target.parent.mkdir(parents=True)
    shutil.copyfile(source, target)
    code = """import sys
from pathlib import Path
from types import SimpleNamespace
root = Path(sys.argv[1])
sys.path.insert(0, str(root))
from dmt_test_support.molecular_fixtures import declared_methanol
sentinel = object()
calls = []
def convert(path, **kwargs):
    assert path == root / 'tests/data/charges/methanol.sdf'
    assert path.read_bytes() == (root / 'expected.sdf').read_bytes()
    calls.append('convert')
    return sentinel
def set_attributes(system, **kwargs):
    assert system is sentinel
    calls.append('set')
sys.modules['molsysmt'] = SimpleNamespace(convert=convert, set=set_attributes)
assert declared_methanol() is sentinel and calls == ['convert', 'set']
assert not any(name.split('.')[0] in {'dockingmt', 'vina', 'rdkit', 'openmm'} for name in sys.modules)
"""
    shutil.copyfile(source, tmp_path / 'expected.sdf')
    result = subprocess.run(
        [sys.executable, '-I', '-B', '-c', code, str(tmp_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
