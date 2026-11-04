"""Compatibility entry point for :mod:`dmt_test_support.validate_1iep_pdbqt`."""

if __name__ == '__main__':
    import runpy
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    runpy.run_module('dmt_test_support.validate_1iep_pdbqt', run_name='__main__')
else:
    from dmt_test_support import validate_1iep_pdbqt as _implementation

    __all__ = [name for name in vars(_implementation) if not name.startswith('_')]

    def __getattr__(name):
        return getattr(_implementation, name)
