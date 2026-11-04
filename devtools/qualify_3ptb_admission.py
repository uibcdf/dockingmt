"""Compatibility entry point for :mod:`dmt_test_support.qualify_3ptb_admission`."""

if __name__ == '__main__':
    import runpy
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    runpy.run_module('dmt_test_support.qualify_3ptb_admission', run_name='__main__')
else:
    from dmt_test_support import qualify_3ptb_admission as _implementation

    __all__ = [name for name in vars(_implementation) if not name.startswith('_')]

    def __getattr__(name):
        return getattr(_implementation, name)
