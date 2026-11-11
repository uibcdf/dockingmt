"""Compatibility entry point for :mod:`bmt_test_support.redocking_181l`."""

if __name__ == '__main__':
    import runpy
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    runpy.run_module('bmt_test_support.redocking_181l', run_name='__main__')
else:
    from bmt_test_support import redocking_181l as _implementation

    __all__ = [name for name in vars(_implementation) if not name.startswith('_')]

    def __getattr__(name):
        return getattr(_implementation, name)
