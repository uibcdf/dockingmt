"""The frozen public quickstart runs outside the checkout with the active consumer."""

import json
import subprocess
import sys
from pathlib import Path

import dockingmt as dmt
from dmt_test_support.pdbqt_fixtures import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT


def test_prepared_input_quickstart_saves_and_restores_original_tiny_result(tmp_path):
    source = Path(__file__).resolve().parents[1] / 'QUICKSTART.md'
    text = source.read_text()
    assert text.count('```python\n') == 1
    code = text.split('```python\n')[1].split('```')[0]
    (tmp_path / 'receptor.pdbqt').write_text(MINIMAL_REC_PDBQT)
    (tmp_path / 'ligand.pdbqt').write_text(MINIMAL_LIG_PDBQT)
    script = code + (
        "\nPath('consumer.json').write_text(json.dumps({"
        "'origin': str(Path(dmt.__file__).resolve()), 'version': dmt.__version__}))\n"
    )
    completed = subprocess.run(
        [sys.executable, '-I', '-B', '-c', script],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert 'Audit: consistent' in completed.stdout
    record = json.loads((tmp_path / 'result.json').read_text())
    assert 1 <= len(record['poses']) <= 2
    assert record['provenance']['backend'] == 'vina'
    consumer = json.loads((tmp_path / 'consumer.json').read_text())
    assert consumer['version'] == dmt.__version__
    assert consumer['origin'] == str(Path(dmt.__file__).resolve())
    original_output = (tmp_path / 'result.json').read_bytes()
    refusal = (
        'import dockingmt\n'
        'def forbidden(*args, **kwargs):\n'
        '    raise AssertionError("Existing output reached engine execution")\n'
        'dockingmt.dock = forbidden\n'
    ) + code
    repeated = subprocess.run(
        [sys.executable, '-I', '-B', '-c', refusal],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert repeated.returncode != 0
    assert 'FileExistsError: Choose a new result filename' in repeated.stderr
    assert 'Existing output reached engine execution' not in repeated.stderr
    assert (tmp_path / 'result.json').read_bytes() == original_output
