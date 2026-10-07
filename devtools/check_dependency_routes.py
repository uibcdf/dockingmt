"""Invoke the immutable dependency SDK without importing scientific packages."""

import importlib
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
SDK_SHA = '738fe8dd731abb99dac421b0bb2acc8564110180'


def load_sdk(module_name: str = 'dependency_routes') -> ModuleType:
    """Load an administrative module from the clean, accepted SDK.

    Parameters
    ----------
    module_name : str
        Reviewed MolSysSuite administrative module.

    Returns
    -------
    ModuleType
        Module whose actual origin is inside the immutable SDK checkout.

    Raises
    ------
    ValueError
        The SDK identity, worktree or imported namespace differs.
    """
    sdk = Path(
        os.environ.get('DOCKINGMT_SUITE_ROOT', ROOT / '.molsyssuite/sdk')
    ).resolve()
    head = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=sdk, text=True
    ).strip()
    dirty = subprocess.check_output(
        ['git', 'status', '--porcelain', '--', 'devtools'], cwd=sdk, text=True
    ).strip()
    if head != SDK_SHA or dirty:
        raise ValueError('Use the accepted clean immutable dependency SDK')
    sys.path[:0] = [str(sdk), str(ROOT / '.molsyssuite-tools')]
    module = importlib.import_module('devtools.scripts.' + module_name)
    origin = module.__file__
    if origin is None or not Path(origin).resolve().is_relative_to(sdk):
        raise ValueError('Another editable SDK namespace was selected')
    return module


def main() -> int:
    """Delegate the CLI to the SDK with this owner root."""
    routes = load_sdk()
    sys.argv[1:1] = ['--root', str(ROOT)]
    return routes.main()


if __name__ == '__main__':
    raise SystemExit(main())
