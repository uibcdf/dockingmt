from smonitor import signal
from smonitor.integrations import CatalogException, context_extra

from .catalog import CATALOG, CODES, PACKAGE_ROOT, SIGNALS
from .emitter import resolve, warn, warn_once
from .meta import META
from .warnings import (
    BackendApproximationWarning,
    NotDigestedArgumentWarning,
    TemporaryFileCleanupWarning,
    UserDockingMTWarning,
)
from .warnings import (
    DockingMTCatalogWarning as DockingMTWarning,
)


class DockingMTException(CatalogException):
    def __init__(self, message: str | None = None, **kwargs):
        standard_keys = {'message', 'code', 'extra', 'catalog', 'meta'}
        extra = dict(kwargs.get('extra') or {})

        captured_keys = [k for k in kwargs if k not in standard_keys]
        for k in captured_keys:
            extra[k] = kwargs.pop(k)

        kwargs.setdefault('catalog', CATALOG)
        kwargs.setdefault('meta', META)

        kwargs['extra'] = extra
        super().__init__(message=message, **kwargs)


class LibraryNotFoundError(DockingMTException):
    catalog_key = 'LibraryNotFoundError'


class ArgumentError(DockingMTException):
    catalog_key = 'ArgumentError'


class CapabilityMismatchError(DockingMTException):
    catalog_key = 'CapabilityMismatchError'


class DockingMTViewerError(DockingMTException):
    """Docking-owned viewer diagnostics; native provider failures stay distinct."""

    def __init__(self, message=None, *, operation=None, **kwargs):
        context = context_extra(provider='molsysviewer', operation=operation)
        super().__init__(message, **{**context, **kwargs})


class ViewerPoseCountError(DockingMTViewerError, ValueError):
    catalog_key = 'ViewerPoseCountError'


class ViewerStructureCountError(DockingMTViewerError, ValueError):
    catalog_key = 'ViewerStructureCountError'


class ViewerInputMissingError(DockingMTViewerError, ValueError):
    catalog_key = 'ViewerInputMissingError'


class ViewerPosePositionError(DockingMTViewerError, ValueError):
    catalog_key = 'ViewerPosePositionError'


class ViewerShapeOwnershipError(DockingMTViewerError, ValueError):
    catalog_key = 'ViewerShapeOwnershipError'


class ViewerStateError(DockingMTViewerError, RuntimeError):
    catalog_key = 'ViewerStateError'


class ViewerCapabilityError(DockingMTViewerError, RuntimeError):
    catalog_key = 'ViewerCapabilityError'


class ViewerActionError(DockingMTViewerError, ValueError):
    catalog_key = 'ViewerActionError'


__all__ = [
    'CATALOG',
    'CODES',
    'SIGNALS',
    'META',
    'PACKAGE_ROOT',
    'signal',
    'warn',
    'warn_once',
    'resolve',
    'DockingMTException',
    'DockingMTWarning',
    'UserDockingMTWarning',
    'TemporaryFileCleanupWarning',
    'LibraryNotFoundError',
    'ArgumentError',
    'CapabilityMismatchError',
    'DockingMTViewerError',
    'ViewerPoseCountError',
    'ViewerStructureCountError',
    'ViewerInputMissingError',
    'ViewerPosePositionError',
    'ViewerShapeOwnershipError',
    'ViewerStateError',
    'ViewerCapabilityError',
    'ViewerActionError',
    'NotDigestedArgumentWarning',
    'BackendApproximationWarning',
]
