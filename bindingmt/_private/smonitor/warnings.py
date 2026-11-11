from __future__ import annotations

from smonitor.integrations import CatalogWarning

from .catalog import CATALOG
from .emitter import warn, warn_once
from .meta import META


class BindingMTCatalogWarning(CatalogWarning):
    def __init__(self, message=None, **kwargs):
        super().__init__(message, catalog=CATALOG, meta=META, **kwargs)


class UserBindingMTWarning(BindingMTCatalogWarning):
    pass


class NotDigestedArgumentWarning(BindingMTCatalogWarning):
    catalog_key = 'NotDigestedArgumentWarning'

    def __init__(self, message=None, *, argument=None, caller=None):
        super().__init__(message, extra={'argument': argument, 'caller': caller})


class BackendApproximationWarning(UserBindingMTWarning):
    catalog_key = 'BackendApproximationWarning'

    def __init__(self, message=None, *, domain_type=None, engine=None):
        super().__init__(message, extra={'domain_type': domain_type, 'engine': engine})


class TemporaryFileCleanupWarning(UserBindingMTWarning):
    catalog_key = 'TemporaryFileCleanupWarning'

    def __init__(self, message=None, *, failures=()):
        failures = [dict(failure) for failure in failures]
        super().__init__(
            message,
            extra={
                'failures': failures,
                'paths': [failure['path'] for failure in failures],
                'failure_count': len(failures),
            },
        )


__all__ = [
    'UserBindingMTWarning',
    'NotDigestedArgumentWarning',
    'BackendApproximationWarning',
    'TemporaryFileCleanupWarning',
    'warn',
    'warn_once',
]
