"""Observe DockingMT's scoped audit with an externally selected DepDigest."""

import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

from depdigest import get_info
from depdigest.cli import main


def audit(label, source, soft_deps, expected, exempt=None):
    arguments = ['audit', '--src-root', str(source), '--soft-deps', soft_deps, '--json']
    if exempt is not None:
        arguments.extend(['--exempt-file', str(exempt)])
    output = io.StringIO()
    with redirect_stdout(output):
        status = main(arguments)
    payload = json.loads(output.getvalue())
    findings = [
        dict(path=str(Path(path).relative_to(source)), **item)
        for path, items in payload['violations'].items()
        for item in items
    ]
    return {
        'case': label,
        'exit': status,
        'violation_count': payload['violation_count'],
        'findings': findings,
        'passed': status == int(expected > 0)
        and payload['violation_count'] == expected,
    }


def observe():
    info = get_info('dockingmt', format='dict')
    soft = sorted(
        entry['library'] for entry in info['dependencies'] if entry['type'] == 'soft'
    )
    soft_deps = ','.join(soft)
    core = Path('dockingmt')
    addon = Path('molsysviewer_dockingmt')
    rows = [
        audit('core', core, soft_deps, 0),
        audit('addon_raw', addon, soft_deps, 1),
        audit(
            'addon_exact_widget_exception',
            addon,
            soft_deps,
            0,
            exempt=addon / 'panels/_base.py',
        ),
    ]
    with tempfile.TemporaryDirectory(prefix='dmt-depdigest47-controls-') as directory:
        root = Path(directory)
        for label, text, count in (
            ('relative_adapter', 'from .vina import VinaBackend\n', 0),
            ('absolute_engine', 'import vina\n', 1),
            ('lazy_engine', 'def run():\n    import vina\n', 0),
        ):
            source = root / label
            source.mkdir()
            (source / 'adapter.py').write_text(text)
            rows.append(audit(label, source, soft_deps, count))
        source = root / 'new_addon_leak'
        source.mkdir()
        exempt = source / '_base.py'
        exempt.write_text('from molsysviewer.addons import AddonPanelWidget\n')
        (source / 'new_leak.py').write_text('import molsysviewer\n')
        rows.append(audit('new_addon_leak', source, soft_deps, 1, exempt=exempt))
    assert not root.exists()
    return {
        'soft_dependencies': soft,
        'passed': sum(row['passed'] for row in rows),
        'total': len(rows),
        'cases': rows,
        'temporary_fixtures_retired': True,
    }


if __name__ == '__main__':
    receipt = observe()
    Path(sys.argv[1]).write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: receipt[key] for key in ('passed', 'total')}))
    raise SystemExit(0 if receipt['passed'] == receipt['total'] else 1)
