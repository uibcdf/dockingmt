# DockingMT/_smonitor.py
from dockingmt._private.smonitor.catalog import CODES

PROFILE = 'user'

SMONITOR = {
    'level': 'WARNING',
    'trace_depth': 3,
    'capture_warnings': True,
    'capture_logging': True,
    'theme': 'plain',
    'silence': ['pint'],
}

SIGNALS = CODES['SIGNALS']
ERRORS = CODES['ERRORS']
WARNINGS = CODES['WARNINGS']
