from smonitor import signal
from smonitor.integrations import CatalogException, CatalogWarning

from .catalog import CATALOG, CODES, PACKAGE_ROOT, SIGNALS
from .emitter import resolve, warn, warn_once
from .meta import META
from .warnings import (
    BackendApproximationWarning,
    NotDigestedArgumentWarning,
    UserDockingMTWarning,
)


class DockingMTException(CatalogException):
    def __init__(self, message: str | None = None, **kwargs):
        standard_keys = {'message', 'code', 'extra', 'catalog', 'meta'}
        extra = kwargs.get('extra', {})
        if not isinstance(extra, dict):
            extra = {'_raw_extra': extra}

        captured_keys = [k for k in kwargs if k not in standard_keys]
        for k in captured_keys:
            extra[k] = kwargs.pop(k)

        kwargs.setdefault('catalog', CATALOG)
        kwargs.setdefault('meta', META)

        if message is None and self.catalog_key:
            entry = CATALOG.get('errors', {}).get(self.catalog_key, {})
            template = entry.get('template')
            if template:
                try:
                    message = template.format(**extra)
                except Exception:
                    message = template

        kwargs['extra'] = extra
        super().__init__(message=message, **kwargs)


class DockingMTWarning(CatalogWarning):
    def __init__(self, **kwargs):
        standard_keys = {'message', 'code', 'extra', 'catalog', 'meta'}
        extra = kwargs.get('extra', {})
        if not isinstance(extra, dict):
            extra = {'_raw_extra': extra}

        captured_keys = [k for k in kwargs if k not in standard_keys]
        for k in captured_keys:
            extra[k] = kwargs.pop(k)

        kwargs.setdefault('catalog', CATALOG)
        kwargs.setdefault('meta', META)
        kwargs['extra'] = extra

        super().__init__(**kwargs)


class LibraryNotFoundError(DockingMTException):
    catalog_key = 'LibraryNotFoundError'


class ArgumentError(DockingMTException):
    catalog_key = 'ArgumentError'


class CapabilityMismatchError(DockingMTException):
    catalog_key = 'CapabilityMismatchError'


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
    'LibraryNotFoundError',
    'ArgumentError',
    'CapabilityMismatchError',
    'NotDigestedArgumentWarning',
    'BackendApproximationWarning',
]
