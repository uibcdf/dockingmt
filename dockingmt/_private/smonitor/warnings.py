from __future__ import annotations

from smonitor.integrations import CatalogWarning

from .emitter import warn, warn_once


class DockingMTCatalogWarning(CatalogWarning):
    def __init__(self, **kwargs):
        from . import CATALOG, META

        super().__init__(catalog=CATALOG, meta=META, **kwargs)


class UserDockingMTWarning(DockingMTCatalogWarning):
    pass


class NotDigestedArgumentWarning(DockingMTCatalogWarning):
    catalog_key = 'NotDigestedArgumentWarning'

    def __init__(self, argument, caller=None):
        super().__init__(extra={'argument': argument, 'caller': caller})


class BackendApproximationWarning(UserDockingMTWarning):
    catalog_key = 'BackendApproximationWarning'

    def __init__(self, domain_type: str, engine: str):
        super().__init__(extra={'domain_type': domain_type, 'engine': engine})


__all__ = [
    'UserDockingMTWarning',
    'NotDigestedArgumentWarning',
    'BackendApproximationWarning',
    'warn',
    'warn_once',
]
