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
    assert 'bindingmt' in packages and 'molsysviewer_bindingmt' in packages
    assert not any(name.startswith('bmt_test_support') for name in packages)
    inventory = tomllib.loads(
        (ROOT / 'devtools/conda-build/resources.toml').read_text()
    )
    assert not any('bmt_test_support' in path for path in inventory['required_paths'])


def test_legacy_helper_import_delegates_without_scientific_dependencies():
    # This administrative control runs without the scientific dependency set.
    legacy = importlib.import_module('devtools.recover_saved_3ptb_case')
    current = importlib.import_module('bmt_test_support.recover_saved_3ptb_case')
    assert legacy._fingerprint is current._fingerprint


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


def test_shared_pdbqt_fixtures_keep_their_original_literal_bytes():
    import hashlib

    from bmt_test_support.pdbqt_fixtures import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT

    assert (
        hashlib.sha256(MINIMAL_REC_PDBQT.encode()).hexdigest()
        == 'fdf890083d54bf740b9ca1eab96069840bffbbf6cea4a8dfdbfa9651ba79d80b'
    )
    assert (
        hashlib.sha256(MINIMAL_LIG_PDBQT.encode()).hexdigest()
        == 'e195e663227eb6b77c2fe7b71efbc906ef6b5e72860261f0c18b8b37a43bf884'
    )


def test_shared_pdbqt_fixture_import_has_no_engine_or_sibling_test_dependency(tmp_path):
    code = """import sys
sys.path.insert(0, sys.argv[1])
from bmt_test_support.pdbqt_fixtures import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT
assert MINIMAL_REC_PDBQT.startswith('ATOM') and MINIMAL_LIG_PDBQT.startswith('ROOT')
assert not any(name == 'test_engines' or name.split('.')[0] in {'bindingmt', 'molsysmt', 'molsysviewer', 'vina', 'rdkit', 'openmm'} for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, '-I', '-B', '-c', code, str(ROOT)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
