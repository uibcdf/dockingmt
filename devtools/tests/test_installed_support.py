"""Keep the owner helper selection separate from installed runtime payload."""

import ast
import importlib
import subprocess
import sys
import tomllib
from pathlib import Path

from setuptools import find_namespace_packages

ROOT = Path(__file__).resolve().parents[2]


def test_installed_helper_imports_have_declared_staged_modules():
    inventory = tomllib.loads(
        (ROOT / 'devtools/conda-build/resources.toml').read_text()
    )
    support = inventory['installed_tests']['support']
    namespace = support['namespace']
    declared = {record['target'] for record in support['files']}
    sources = [*(ROOT / 'tests').glob('*.py'), *(ROOT / namespace).glob('*.py')]
    imports = set()
    for source in sources:
        for node in ast.walk(ast.parse(source.read_text())):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert not node.module.startswith('devtools'), source
                if node.module == namespace:
                    imports.update(namespace + '.' + item.name for item in node.names)
                elif node.module.startswith(namespace + '.'):
                    imports.add(node.module)
            elif isinstance(node, ast.Import):
                for item in node.names:
                    assert not item.name.startswith('devtools'), source
                    if item.name.startswith(namespace + '.'):
                        imports.add(item.name)
    assert imports
    assert {name.replace('.', '/') + '.py' for name in imports} <= declared


def test_support_namespace_is_unshipped_by_actual_package_discovery():
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    discovery = project['tool']['setuptools']['packages']['find']
    packages = find_namespace_packages(where=str(ROOT), include=discovery['include'])
    assert 'dockingmt' in packages and 'molsysviewer_dockingmt' in packages
    assert not any(name.startswith('dmt_test_support') for name in packages)
    inventory = tomllib.loads(
        (ROOT / 'devtools/conda-build/resources.toml').read_text()
    )
    assert not any('dmt_test_support' in path for path in inventory['required_paths'])


def test_legacy_helper_imports_delegate_to_the_same_implementation():
    for name, operation in (
        ('recover_saved_3ptb_case', '_fingerprint'),
        ('qualify_named_types', 'explicit_source'),
        ('qualify_3ptb_admission', 'admit'),
    ):
        legacy = importlib.import_module('devtools.' + name)
        current = importlib.import_module('dmt_test_support.' + name)
        assert getattr(legacy, operation) is getattr(current, operation)


def test_legacy_script_entry_point_keeps_help_outside_the_clone(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / 'devtools/recover_saved_3ptb_case.py'),
            '--help',
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert '--bundle' in result.stdout and '--source' in result.stdout
