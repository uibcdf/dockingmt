import subprocess
import sys
from pathlib import Path


def test_devguide_records_and_generated_indexes_are_valid():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, 'devtools/devguide_index.py', '--check'],
        cwd=root,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
