from smonitor import signal
from smonitor.integrations import CatalogException, context_extra

from .catalog import CATALOG, CODES, PACKAGE_ROOT, SIGNALS
from .emitter import resolve, warn, warn_once
from .meta import META
from .warnings import (
    BackendApproximationWarning,
    NotDigestedArgumentWarning,
    TemporaryFileCleanupWarning,
    UserBindingMTWarning,
)
from .warnings import (
    BindingMTCatalogWarning as BindingMTWarning,
)


class BindingMTException(CatalogException):
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


class LibraryNotFoundError(BindingMTException):
    catalog_key = 'LibraryNotFoundError'


class ArgumentError(BindingMTException):
    catalog_key = 'ArgumentError'


class CapabilityMismatchError(BindingMTException):
    catalog_key = 'CapabilityMismatchError'


class BindingMTViewerError(BindingMTException):
    """Docking-owned viewer diagnostics; native provider failures stay distinct."""

    def __init__(self, message=None, *, operation=None, **kwargs):
        context = context_extra(provider='molsysviewer', operation=operation)
        super().__init__(message, **{**context, **kwargs})


class ViewerPoseCountError(BindingMTViewerError, ValueError):
    catalog_key = 'ViewerPoseCountError'


class ViewerStructureCountError(BindingMTViewerError, ValueError):
    catalog_key = 'ViewerStructureCountError'


class ViewerInputMissingError(BindingMTViewerError, ValueError):
    catalog_key = 'ViewerInputMissingError'


class ViewerPosePositionError(BindingMTViewerError, ValueError):
    catalog_key = 'ViewerPosePositionError'


class ViewerShapeOwnershipError(BindingMTViewerError, ValueError):
    catalog_key = 'ViewerShapeOwnershipError'


class ViewerStateError(BindingMTViewerError, RuntimeError):
    catalog_key = 'ViewerStateError'


class ViewerCapabilityError(BindingMTViewerError, RuntimeError):
    catalog_key = 'ViewerCapabilityError'


class ViewerActionError(BindingMTViewerError, ValueError):
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
    'BindingMTException',
    'BindingMTWarning',
    'UserBindingMTWarning',
    'TemporaryFileCleanupWarning',
    'LibraryNotFoundError',
    'ArgumentError',
    'CapabilityMismatchError',
    'BindingMTViewerError',
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
