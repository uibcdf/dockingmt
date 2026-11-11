"""Compatibility entry point for :mod:`bmt_test_support.qualify_1iep_flexibility`."""

if __name__ == '__main__':
    import runpy
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    runpy.run_module('bmt_test_support.qualify_1iep_flexibility', run_name='__main__')
else:
    from bmt_test_support import qualify_1iep_flexibility as _implementation

    __all__ = [name for name in vars(_implementation) if not name.startswith('_')]

    def __getattr__(name):
        return getattr(_implementation, name)
