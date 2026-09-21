from __future__ import annotations

from smonitor.integrations import DiagnosticBundle

from .catalog import CATALOG, PACKAGE_ROOT
from .meta import META

bundle = DiagnosticBundle(CATALOG, META, PACKAGE_ROOT)

warn = bundle.warn
warn_once = bundle.warn_once
resolve = bundle.resolve

__all__ = ['bundle', 'warn', 'warn_once', 'resolve']
