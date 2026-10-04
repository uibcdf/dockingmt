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
    DockingProblem,
    DockingProtocol,
    DockingResult,
    DockingOutcome,
    SearchDomain,
    VinaProtocol,
    audit_result,
    audit_pose,
    verify_captured_inputs,
)
from .dock import dock
from .batch import dock_many
from .score import score
from .evaluation import evaluate_redocking
from .aggregation import summarize_redocking
from .engines import DockingBackend, VinaBackend
from .preparation import (
    PreparedLigand,
    PreparedReceptor,
    assess_preparation,
    prepare_ligand,
    prepare_receptor,
)
from .view import show, view

__all__ = [
    'summarize_redocking',
    'evaluate_redocking',
    'dock_many',
    'DockingOutcome',
    'audit_pose',
    'assess_preparation',
    'audit_result',
    'verify_captured_inputs',
    '__version__',
    '__print_version__',
    'pyunitwizard',
    'SearchDomain',
    'BoxRegion',
    'DockingPose',
    'DockingResult',
    'DockingProblem',
    'DockingProtocol',
    'VinaProtocol',
    'DockingBackend',
    'VinaBackend',
    'PreparedReceptor',
    'prepare_receptor',
    'PreparedLigand',
    'prepare_ligand',
    'dock',
    'score',
    'show',
    'view',
]

# The unit policy is declared when this package is imported, not on first use.
from . import _pyunitwizard  # noqa: E402,F401
