# ruff: noqa: E402,I001
"""
DockingMT
The molecular docking layer of MolSysSuite.
"""

from ._version import __version__


def __print_version__():
    print('DockingMT version ' + __version__)


from ._pyunitwizard import pyunitwizard

from smonitor.integrations import ensure_configured
from ._private.smonitor import PACKAGE_ROOT

ensure_configured(PACKAGE_ROOT)

from .core import (
    BoxRegion,
    DockingPose,
    DockingResult,
    SearchDomain,
)

__all__ = [
    '__version__',
    '__print_version__',
    'pyunitwizard',
    'SearchDomain',
    'BoxRegion',
    'DockingPose',
    'DockingResult',
]

# The unit policy is declared when this package is imported, not on first use.
from . import _pyunitwizard  # noqa: E402,F401
