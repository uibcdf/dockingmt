"""Verify actual benchmark tracing custody without molecular dependencies."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHILD = r"""
import importlib.util
from pathlib import Path
import sys
import tracemalloc
from types import SimpleNamespace

source, caller_owned, failure, memory = Path(sys.argv[1]), *[v == 'true' for v in sys.argv[2:]]
spec = importlib.util.spec_from_file_location('export_tool', source)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)
class InertResult:
    calls = 0
    def __len__(self):
        return 1
    def __iter__(self):
        return iter([SimpleNamespace(n_atoms=1)])
    def to_dict(self):
        self.calls += 1
        if failure and self.calls == 3:
            raise RuntimeError('injected memory export failure')
        return {'fixture': 'no molecular operations'}
assert not tracemalloc.is_tracing()
if caller_owned:
    tracemalloc.start()
caught = None
try:
    result = tool._measure(InertResult(), 1, memory, False)
except RuntimeError as error:
    caught = error
if failure and memory:
    assert str(caught) == 'injected memory export failure'
else:
    assert caught is None
    assert result['n_poses'] == 1 and result['atoms_per_pose'] == [1]
    assert len(result['record_sha256']) == 64
    assert ('python_peak_bytes' in result) is memory
assert tracemalloc.is_tracing() is caller_owned, 'benchmark changed caller tracing ownership'
assert not any(n.split('.')[0] in ('dockingmt', 'molsysmt', 'numpy', 'vina', 'pyunitwizard') for n in sys.modules)
tracemalloc.stop()
"""


class TestResultExportResources(unittest.TestCase):
    def run_case(self, *, caller_owned, failure, memory=True):
        with tempfile.TemporaryDirectory(prefix='dockingmt-tracing-test-') as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    '-S',
                    '-c',
                    CHILD,
                    str(ROOT / 'devtools/benchmark_result_export.py'),
                    str(caller_owned).lower(),
                    str(failure).lower(),
                    str(memory).lower(),
                ],
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse(Path(directory).exists())

    def test_success_preserves_caller_tracing(self):
        self.run_case(caller_owned=True, failure=False)

    def test_memory_failure_preserves_caller_tracing(self):
        self.run_case(caller_owned=True, failure=True)

    def test_success_releases_owned_tracing(self):
        self.run_case(caller_owned=False, failure=False)

    def test_memory_failure_releases_owned_tracing(self):
        self.run_case(caller_owned=False, failure=True)

    def test_without_memory_preserves_caller_tracing(self):
        self.run_case(caller_owned=True, failure=False, memory=False)
