"""Compatibility entry point for :mod:`bmt_test_support.evaluate_3ptb_saved`."""

if __name__ == '__main__':
    import runpy
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    runpy.run_module('bmt_test_support.evaluate_3ptb_saved', run_name='__main__')
else:
    from bmt_test_support import evaluate_3ptb_saved as _implementation

    __all__ = [name for name in vars(_implementation) if not name.startswith('_')]

    def __getattr__(name):
        return getattr(_implementation, name)
