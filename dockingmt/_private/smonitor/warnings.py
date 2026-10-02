from __future__ import annotations

from smonitor.integrations import CatalogWarning

from .catalog import CATALOG
from .emitter import warn, warn_once
from .meta import META


class DockingMTCatalogWarning(CatalogWarning):
    def __init__(self, message=None, **kwargs):
        super().__init__(message, catalog=CATALOG, meta=META, **kwargs)


class UserDockingMTWarning(DockingMTCatalogWarning):
    pass


class NotDigestedArgumentWarning(DockingMTCatalogWarning):
    catalog_key = 'NotDigestedArgumentWarning'

    def __init__(self, message=None, *, argument=None, caller=None):
        super().__init__(message, extra={'argument': argument, 'caller': caller})


class BackendApproximationWarning(UserDockingMTWarning):
    catalog_key = 'BackendApproximationWarning'

    def __init__(self, message=None, *, domain_type=None, engine=None):
        super().__init__(message, extra={'domain_type': domain_type, 'engine': engine})


__all__ = [
    'UserDockingMTWarning',
    'NotDigestedArgumentWarning',
    'BackendApproximationWarning',
    'warn',
    'warn_once',
]
