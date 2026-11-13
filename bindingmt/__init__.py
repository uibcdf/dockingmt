# ruff: noqa: E402,I001
"""
BindingMT
Reproducible molecular binding modelling for MolSysSuite.
"""

from ._version import __version__


def __print_version__():
    print('BindingMT version ' + __version__)


from ._pyunitwizard import pyunitwizard

from smonitor.integrations import ensure_configured
from ._private.smonitor import PACKAGE_ROOT

ensure_configured(PACKAGE_ROOT)

from . import exceptions

from .core import (
    ContactFootprint,
    BindingInterface,
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
    characterize_interface,
    verify_captured_inputs,
)
from .dock import dock
from .contacts import calculate_interface_contacts
from .batch import dock_many
from .score import score
from .evaluation import evaluate_redocking
from .aggregation import summarize_redocking
from .comparison import compare_scores
from .interactions import PoseInteractions, bind_interactions
from .engines import DockingBackend, VinaBackend
from .preparation import (
    PreparedLigand,
    PreparedReceptor,
    assess_preparation,
    audit_preparation_charges,
    prepare_ligand,
    prepare_receptor,
)
from .view import show, view

__all__ = [
    'ContactFootprint',
    'calculate_interface_contacts',
    'BindingInterface',
    'characterize_interface',
    'exceptions',
    'PoseInteractions',
    'bind_interactions',
    'compare_scores',
    'summarize_redocking',
    'evaluate_redocking',
    'dock_many',
    'DockingOutcome',
    'audit_pose',
    'assess_preparation',
    'audit_preparation_charges',
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
