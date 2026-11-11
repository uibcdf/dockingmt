# DepDigest configuration for BindingMT
from bindingmt._private.smonitor import LibraryNotFoundError

LIBRARIES = {
    'numpy': {'type': 'hard', 'pypi': 'numpy'},
    'molsysmt': {
        'type': 'hard',
        'pypi': None,
        'conda': 'molsysmt',
        'channel': 'uibcdf',
    },
    'pyunitwizard': {
        'type': 'hard',
        'pypi': None,
        'conda': 'pyunitwizard',
        'channel': 'uibcdf',
    },
    'argdigest': {
        'type': 'hard',
        'pypi': None,
        'conda': 'argdigest',
        'channel': 'uibcdf',
    },
    'depdigest': {
        'type': 'hard',
        'pypi': None,
        'conda': 'depdigest',
        'channel': 'uibcdf',
    },
    'smonitor': {
        'type': 'hard',
        'pypi': None,
        'conda': 'smonitor',
        'channel': 'uibcdf',
    },
    'vina': {'type': 'soft', 'pypi': 'vina', 'conda': 'vina'},
    'molsysviewer': {
        'type': 'soft',
        'pypi': None,
        'conda': 'molsysviewer',
        'channel': 'uibcdf',
    },
}

# Molecular engines are selected and checked by MolSysMT. They are not
# BindingMT runtime capabilities; scientific test tools retain their own scope.

MAPPING = {}

SHOW_ALL_CAPABILITIES = True
EXCEPTION_CLASS = LibraryNotFoundError
