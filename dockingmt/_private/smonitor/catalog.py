from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

SIGNALS = {'dockingmt.dock': {'tags': ['api', 'docking']}}

CATALOG = {
    'signals': SIGNALS,
    'exceptions': {
        'LibraryNotFoundError': {'code': 'DMT-E001', 'category': 'dependency'},
        'ArgumentError': {'code': 'DMT-E002', 'category': 'validation'},
        'CapabilityMismatchError': {'code': 'DMT-E003', 'category': 'capability'},
    },
    'warnings': {
        'BackendApproximationWarning': {'code': 'DMT-W001', 'category': 'domain'},
        'NotDigestedArgumentWarning': {'code': 'DMT-W002', 'category': 'validation'},
    },
}

CODES = {
    'DMT-E001': {
        'user_message': "Required library '{library}' is not installed.",
        'user_hint': 'Install the required optional package in the active environment.',
    },
    'DMT-E002': {
        'user_message': "Invalid argument '{arg_name}': {reason}",
    },
    'DMT-E003': {
        'user_message': "Requested capability '{capability}' is not supported by engine '{engine}'.",
    },
    'DMT-W001': {
        'user_message': "SearchDomain '{domain_type}' was approximated by a rectangular box for engine '{engine}'.",
    },
    'DMT-W002': {
        'user_message': "The argument '{argument}' in '{caller}' was not digested.",
    },
}
