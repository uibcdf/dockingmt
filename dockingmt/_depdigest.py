# DepDigest configuration for DockingMT
from dockingmt._private.smonitor import LibraryNotFoundError

LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'molsysmt': {
        'type': 'hard',
        'pypi': None,
        'conda': 'molsysmt',
        'channel': 'uibcdf',
    },
    'pyunitwizard': {'type': 'hard', 'pypi': 'pyunitwizard'},
    'argdigest': {'type': 'hard', 'pypi': 'argdigest'},
    'depdigest': {'type': 'hard', 'pypi': 'depdigest'},
    'smonitor': {'type': 'hard', 'pypi': 'smonitor'},
    'vina': {'type': 'soft', 'pypi': 'vina', 'conda': 'vina'},
    'molsysviewer': {
        'type': 'soft',
        'pypi': None,
        'conda': 'molsysviewer',
        'channel': 'uibcdf',
    },
    'rdkit': {'type': 'soft', 'pypi': 'rdkit', 'conda': 'rdkit'},
    'pdbfixer': {'type': 'soft', 'pypi': 'pdbfixer', 'conda': 'pdbfixer'},
    'openmm': {'type': 'soft', 'pypi': 'openmm', 'conda': 'openmm'},
}

MAPPING = {}

SHOW_ALL_CAPABILITIES = True
EXCEPTION_CLASS = LibraryNotFoundError
