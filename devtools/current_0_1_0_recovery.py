"""Finite #74 recovery of the original 1030a29 candidate and attempt-1 wheel."""

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

CANDIDATE = '1030a29025914e01dff09e5fc606ec73b90f4cd9'
TREE = '5f0c98567ae06263c1a43b9a24c63f7c81675539'
WHEEL_SHA256 = '3b70094ee1d9103ceed19ee64214c0025662781acf8eb28eaeb4733f5c5a53ca'
HELPER_SHA256 = '9265587ac28970a25fa27cc31f5ef57cbb71d03651b918272e3db73b0b74e68e'
RECEIPT_SHA256 = '602117e87c127645ec12effd708f9c2810b97c2dca24402d0ad8f1a2b17979a5'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def admit(root, task, candidate_sha):
    """Admit only the named hosted 3.13 recovery; preserve actual workflow identity."""
    expected = {
        'GITHUB_ACTIONS': 'true',
        'RUNNER_ENVIRONMENT': 'github-hosted',
        'GITHUB_REPOSITORY': 'uibcdf/dockingmt',
        'GITHUB_EVENT_NAME': 'workflow_dispatch',
        'GITHUB_WORKFLOW_REF': (
            'uibcdf/dockingmt/.github/workflows/'
            'recover-current-0.1.0-python313.yml@refs/heads/main'
        ),
        'DOCKINGMT_RECOVERY': 'current-010-python313-original-wheel',
        'EXPECTED_PYTHON': '3.13',
        'EXPECTED_WHEEL_SHA256': WHEEL_SHA256,
    }
    if (
        candidate_sha != CANDIDATE
        or sys.version_info[:2] != (3, 13)
        or not re.fullmatch('[0-9a-f]{40}', os.environ.get('GITHUB_SHA', ''))
        or any(os.environ.get(key) != value for key, value in expected.items())
    ):
        raise ValueError('Use only the declared original-wheel Python 3.13 recovery')
    candidate = task / 'candidate'
    tree = subprocess.check_output(
        ['git', '-C', str(candidate), 'rev-parse', 'HEAD^{tree}'], text=True
    ).strip()
    if tree != TREE:
        raise ValueError('Recovery candidate tree differs from the original')
    helper = 'devtools/qualify_current_0_1_0.py'
    if digest(candidate / helper) != HELPER_SHA256:
        raise ValueError('Original qualification helper changed')

    def scientific_body(path):
        module = ast.parse(path.read_bytes())
        module.body = [
            node
            for node in module.body
            if not (isinstance(node, ast.FunctionDef) and node.name == 'require_hosted')
        ]
        return ast.dump(module, include_attributes=False)

    if scientific_body(candidate / helper) != scientific_body(root / helper):
        raise ValueError('Recovery changed qualification logic outside admission')
    for name in [
        'devtools/qualify_source_0_1_0.py',
        'devtools/source_0_1_0_current.toml',
    ]:
        if (candidate / name).read_bytes() != (root / name).read_bytes():
            raise ValueError('Recovery changed a frozen profile or wheel guard')
    receipt_path = task / 'evidence/build-receipt.json'
    wheel = task / 'wheels/dockingmt-0.1.0-py3-none-any.whl'
    if digest(receipt_path) != RECEIPT_SHA256 or digest(wheel) != WHEEL_SHA256:
        raise ValueError('Recovery must consume the original receipt and wheel bytes')
    receipt = json.loads(receipt_path.read_text())
    if (
        receipt['candidate'] != CANDIDATE
        or receipt['tree'] != TREE
        or receipt['qualification_source'] != CANDIDATE
        or receipt['run_id'] != 42976065511
        or receipt['run_attempt'] != 1
    ):
        raise ValueError('Recovery producer identity differs from the original')
    for name, value in receipt['contract']['source_input_sha256'].items():
        if digest(candidate / name) != value:
            raise ValueError('Recovery candidate build input changed: ' + name)
