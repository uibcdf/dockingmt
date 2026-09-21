# DepDigest configuration for DockingMT
from dockingmt._private.smonitor import LibraryNotFoundError

LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'molsysmt': {'type': 'hard', 'pypi': 'molsysmt'},
    'pyunitwizard': {'type': 'hard', 'pypi': 'pyunitwizard'},
    'argdigest': {'type': 'hard', 'pypi': 'argdigest'},
    'smonitor': {'type': 'hard', 'pypi': 'smonitor'},
    'vina': {'type': 'soft', 'pypi': 'vina', 'conda': 'vina'},
    'meeko': {'type': 'soft', 'pypi': 'meeko', 'conda': 'meeko'},
    'rdkit': {'type': 'soft', 'pypi': 'rdkit', 'conda': 'rdkit'},
    'pdbfixer': {'type': 'soft', 'pypi': 'pdbfixer', 'conda': 'pdbfixer'},
    'openmm': {'type': 'soft', 'pypi': 'openmm', 'conda': 'openmm'},
}

MAPPING = {}

SHOW_ALL_CAPABILITIES = True
EXCEPTION_CLASS = LibraryNotFoundError
