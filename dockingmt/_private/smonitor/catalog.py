from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

SIGNALS = {
    'dockingmt.dock': {'tags': ['api', 'docking']},
    'dockingmt.preparation.ligand.prepare_ligand': {'tags': ['api', 'preparation']},
    'dockingmt.preparation.receptor.prepare_receptor': {'tags': ['api', 'preparation']},
}

CATALOG = {
    'signals': SIGNALS,
    'exceptions': {
        'LibraryNotFoundError': {'code': 'DMT-E001', 'category': 'dependency'},
        'ArgumentError': {'code': 'DMT-E002', 'category': 'validation'},
        'CapabilityMismatchError': {'code': 'DMT-E003', 'category': 'capability'},
        'ViewerPoseCountError': {'code': 'DMT-E004', 'category': 'validation'},
        'ViewerStructureCountError': {'code': 'DMT-E005', 'category': 'validation'},
        'ViewerInputMissingError': {'code': 'DMT-E006', 'category': 'validation'},
        'ViewerPosePositionError': {'code': 'DMT-E007', 'category': 'validation'},
        'ViewerShapeOwnershipError': {'code': 'DMT-E008', 'category': 'validation'},
        'ViewerStateError': {'code': 'DMT-E009', 'category': 'visualization'},
        'ViewerCapabilityError': {'code': 'DMT-E010', 'category': 'capability'},
        'ViewerActionError': {'code': 'DMT-E011', 'category': 'validation'},
    },
    'warnings': {
        'BackendApproximationWarning': {'code': 'DMT-W001', 'category': 'domain'},
        'NotDigestedArgumentWarning': {'code': 'DMT-W002', 'category': 'validation'},
        'TemporaryFileCleanupWarning': {'code': 'DMT-W003', 'category': 'resource'},
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
    'DMT-E004': {
        'user_message': 'n_poses must be a positive integer.',
    },
    'DMT-E005': {
        'user_message': 'The {role} must have a supported structure count; got {observed} (allowed: {expected}).',
    },
    'DMT-E006': {
        'user_message': 'A {resource} is required to display molecular docking poses.',
    },
    'DMT-E007': {
        'user_message': 'Invalid pose position: supply one integer position within the loaded collection.',
    },
    'DMT-E008': {
        'user_message': "Shape tag '{tag}' is already owned by another scene element.",
        'user_hint': 'Choose a different tag or explicitly remove the other scene element.',
    },
    'DMT-E009': {
        'user_message': 'Supply the {resource} before using this docking control.',
    },
    'DMT-E010': {
        'user_message': "MolSysViewer support for '{capability}' is required for this docking control.",
    },
    'DMT-E011': {
        'user_message': "Unknown {panel} action '{action_id}'.",
    },
    'DMT-W001': {
        'user_message': "SearchDomain '{domain_type}' was approximated by a rectangular box for engine '{engine}'.",
    },
    'DMT-W002': {
        'user_message': "The argument '{argument}' in '{caller}' was not digested.",
    },
    'DMT-W003': {
        'user_message': 'Vina could not remove {failure_count} staged temporary file(s). Inspect these owned paths before retrying disposal: {paths}.',
    },
}
