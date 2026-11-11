from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

SIGNALS = {
    'bindingmt.dock': {'tags': ['api', 'docking']},
    'bindingmt.preparation.ligand.prepare_ligand': {'tags': ['api', 'preparation']},
    'bindingmt.preparation.receptor.prepare_receptor': {'tags': ['api', 'preparation']},
}

CATALOG = {
    'signals': SIGNALS,
    'exceptions': {
        'LibraryNotFoundError': {'code': 'BMT-E001', 'category': 'dependency'},
        'ArgumentError': {'code': 'BMT-E002', 'category': 'validation'},
        'CapabilityMismatchError': {'code': 'BMT-E003', 'category': 'capability'},
        'ViewerPoseCountError': {'code': 'BMT-E004', 'category': 'validation'},
        'ViewerStructureCountError': {'code': 'BMT-E005', 'category': 'validation'},
        'ViewerInputMissingError': {'code': 'BMT-E006', 'category': 'validation'},
        'ViewerPosePositionError': {'code': 'BMT-E007', 'category': 'validation'},
        'ViewerShapeOwnershipError': {'code': 'BMT-E008', 'category': 'validation'},
        'ViewerStateError': {'code': 'BMT-E009', 'category': 'visualization'},
        'ViewerCapabilityError': {'code': 'BMT-E010', 'category': 'capability'},
        'ViewerActionError': {'code': 'BMT-E011', 'category': 'validation'},
    },
    'warnings': {
        'BackendApproximationWarning': {'code': 'BMT-W001', 'category': 'domain'},
        'NotDigestedArgumentWarning': {'code': 'BMT-W002', 'category': 'validation'},
        'TemporaryFileCleanupWarning': {'code': 'BMT-W003', 'category': 'resource'},
    },
}

CODES = {
    'BMT-E001': {
        'user_message': "Required library '{library}' is not installed.",
        'user_hint': 'Install the required optional package in the active environment.',
    },
    'BMT-E002': {
        'user_message': "Invalid argument '{arg_name}': {reason}",
    },
    'BMT-E003': {
        'user_message': "Requested capability '{capability}' is not supported by engine '{engine}'.",
    },
    'BMT-E004': {
        'user_message': 'n_poses must be a positive integer.',
    },
    'BMT-E005': {
        'user_message': 'The {role} must have a supported structure count; got {observed} (allowed: {expected}).',
    },
    'BMT-E006': {
        'user_message': 'A {resource} is required to display molecular docking poses.',
    },
    'BMT-E007': {
        'user_message': 'Invalid pose position: supply one integer position within the loaded collection.',
    },
    'BMT-E008': {
        'user_message': "Shape tag '{tag}' is already owned by another scene element.",
        'user_hint': 'Choose a different tag or explicitly remove the other scene element.',
    },
    'BMT-E009': {
        'user_message': 'Supply the {resource} before using this docking control.',
    },
    'BMT-E010': {
        'user_message': "MolSysViewer support for '{capability}' is required for this docking control.",
    },
    'BMT-E011': {
        'user_message': "Unknown {panel} action '{action_id}'.",
    },
    'BMT-W001': {
        'user_message': "SearchDomain '{domain_type}' was approximated by a rectangular box for engine '{engine}'.",
    },
    'BMT-W002': {
        'user_message': "The argument '{argument}' in '{caller}' was not digested.",
    },
    'BMT-W003': {
        'user_message': 'Vina could not remove {failure_count} staged temporary file(s). Inspect these owned paths before retrying disposal: {paths}.',
    },
}
