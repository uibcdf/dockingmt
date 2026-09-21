from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

CATALOG = {
    'signals': {
        'dockingmt.dock': {
            'tags': ['api', 'docking'],
        },
    },
    'errors': {
        'LibraryNotFoundError': {
            'template': "Required library '{library}' is not installed. Please install it using '{hint}'.",
            'category': 'dependency',
        },
        'ArgumentError': {
            'template': "Invalid argument '{arg_name}': {reason}",
            'category': 'validation',
        },
        'CapabilityMismatchError': {
            'template': "Requested capability '{capability}' is not supported by engine '{engine}'.",
            'category': 'capability',
        },
    },
    'warnings': {
        'BackendApproximationWarning': {
            'template': "SearchDomain '{domain_type}' was approximated by a rectangular box for engine '{engine}'.",
            'category': 'domain',
        },
        'NotDigestedArgumentWarning': {
            'template': "The argument '{argument}' in '{caller}' was not digested.",
            'category': 'validation',
        },
    },
}

CODES = {
    'SIGNALS': CATALOG['signals'],
    'ERRORS': CATALOG['errors'],
    'WARNINGS': CATALOG['warnings'],
}

SIGNALS = CATALOG['signals']
