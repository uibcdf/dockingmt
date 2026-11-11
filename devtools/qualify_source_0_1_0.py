"""Hosted-only caller for #74's fixed private source candidate, not a publisher.

MolSysSuite owns dependency checks, installed import guards and test-support
staging. This caller binds those operations to BindingMT's frozen 0.1.0 inputs.
"""

import argparse
import configparser
import hashlib
import importlib
import importlib.metadata as metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import sysconfig
import tomllib
import xml.etree.ElementTree as ET
import zipfile
from email.parser import BytesParser
from pathlib import Path

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

ROOT = Path(__file__).resolve().parents[1]
TASK = ROOT / '.molsyssuite/source-0.1.0-hosted'
CANDIDATE = '905abc9698cf9d4add78a52d57dab707859a148d'
TREE = '4f1583e0d2b315b503afa6d6d9912f1844beea9e'
DEPENDENCY_SDK = '738fe8dd731abb99dac421b0bb2acc8564110180'
INSTALLED_SDK = '95f693be10c9205ab9b912cb53453710a207bf45'
RECEIPT = (
    ROOT
    / 'devguide/validation/data/source_0_1_0_2026-11-05'
    / 'metadata_payload_receipt.json'
)
RECEIPT_SHA256 = 'be3c5a08668ff72d84caadaa847865e53b96bc7062ade4e647d8b288977e7c5f'
PROVIDERS = ('argdigest', 'molsysmt', 'molsysviewer')


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def frozen_receipt():
    if digest(RECEIPT) != RECEIPT_SHA256:
        raise ValueError('The frozen candidate receipt has changed')
    return json.loads(RECEIPT.read_text())


def wheel_payload(wheel, frozen):
    """Accept only this candidate's complete runtime and metadata boundary."""
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError('Duplicate wheel members')
        runtime = {
            name: hashlib.sha256(archive.read(name)).hexdigest()
            for name in names
            if not name.endswith('/') and '.dist-info/' not in name
        }
        if runtime != frozen['archive_checks']['runtime_sha256']:
            raise ValueError(
                'Runtime payload differs from the frozen versioned candidate'
            )
        prefix = 'bindingmt-0.1.0.dist-info/'
        message = BytesParser().parsebytes(archive.read(prefix + 'METADATA'))
        expected = frozen['archive_checks']
        if (
            message['Name'] != 'bindingmt'
            or message['Version'] != '0.1.0'
            or SpecifierSet(message['Requires-Python'])
            != SpecifierSet(expected['python_requires'])
            or message['License-Expression'] != 'MIT'
            or sorted(str(Requirement(v)) for v in message.get_all('Requires-Dist', []))
            != sorted(str(Requirement(v)) for v in expected['requires_dist'])
        ):
            raise ValueError(
                'Wheel metadata differs from the frozen candidate contract'
            )
        entry = configparser.ConfigParser()
        entry.read_string(archive.read(prefix + 'entry_points.txt').decode())
        if entry['molsysviewer.addons']['bindingmt'] != 'molsysviewer_bindingmt':
            raise ValueError('Wrong addon entry point')
        headers = BytesParser().parsebytes(archive.read(prefix + 'WHEEL'))
        if headers['Root-Is-Purelib'] != 'true' or headers.get_all('Tag') != [
            'py3-none-any'
        ]:
            raise ValueError('Unexpected wheel platform identity')
        if (
            hashlib.sha256(archive.read(prefix + 'licenses/LICENSE')).hexdigest()
            != (frozen['source_input_sha256']['LICENSE'])
        ):
            raise ValueError('License bytes differ from the candidate')
    return runtime


def require_hosted():
    if (
        os.environ.get('GITHUB_ACTIONS') != 'true'
        or os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted'
    ):
        raise ValueError('This heavy qualification runs only on GitHub-hosted runners')
    candidate = TASK / 'candidate'
    if git(candidate, 'rev-parse', 'HEAD') != CANDIDATE:
        raise ValueError('Wrong source candidate')
    if git(candidate, 'rev-parse', 'HEAD^{tree}') != TREE:
        raise ValueError('Wrong source tree')
    for name, value in frozen_receipt()['source_input_sha256'].items():
        if digest(candidate / name) != value:
            raise ValueError('Candidate source input has changed: ' + name)
    return candidate


def save(name, value):
    evidence = TASK / 'evidence'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def build():
    candidate = require_hosted()
    if git(candidate, 'status', '--porcelain', '--untracked-files=no'):
        raise ValueError('Candidate tracked inputs must be clean before building')
    # The isolated runner checkout cannot push this private validation tag.
    for remote in git(candidate, 'remote').splitlines():
        subprocess.run(
            ['git', '-C', str(candidate), 'remote', 'remove', remote], check=True
        )
    subprocess.run(
        [
            'git',
            '-C',
            str(candidate),
            '-c',
            'tag.gpgSign=false',
            'tag',
            '0.1.0',
            CANDIDATE,
        ],
        check=True,
    )
    wheels = TASK / 'wheels'
    subprocess.run(
        [
            sys.executable,
            '-m',
            'build',
            '--wheel',
            '--no-isolation',
            '--outdir',
            str(wheels),
            str(candidate),
        ],
        check=True,
    )
    wheel = wheels / 'bindingmt-0.1.0-py3-none-any.whl'
    runtime = wheel_payload(wheel, frozen_receipt())
    if git(candidate, 'status', '--porcelain', '--untracked-files=no'):
        raise ValueError('Building changed tracked candidate inputs')
    receipt = {
        'candidate': CANDIDATE,
        'tree': TREE,
        'version': '0.1.0',
        'qualification_source': os.environ['GITHUB_SHA'],
        'run_id': int(os.environ['GITHUB_RUN_ID']),
        'run_attempt': int(os.environ['GITHUB_RUN_ATTEMPT']),
        'wheel': {'filename': wheel.name, 'sha256': digest(wheel)},
        'runtime_sha256': runtime,
        'frozen_receipt_sha256': RECEIPT_SHA256,
        'private_runner_tag_only': True,
        'public_release_or_package': False,
        'tools': {
            n: metadata.version(n)
            for n in (
                'build',
                'setuptools',
                'wheel',
                'versioningit',
                'packaging',
                'pyproject-hooks',
            )
        },
        'python': platform.python_version(),
        'population': 'new hosted build; not the earlier private archive',
    }
    save('build-receipt.json', receipt)
    with Path(os.environ['GITHUB_OUTPUT']).open('a') as output:
        output.write('wheel_sha256=' + receipt['wheel']['sha256'] + '\n')


def bounds():
    candidate = require_hosted()
    sdk = TASK / 'dependency-sdk'
    if git(sdk, 'rev-parse', 'HEAD') != DEPENDENCY_SDK:
        raise ValueError('Wrong dependency SDK')
    if git(sdk, 'status', '--porcelain', '--', 'devtools'):
        raise ValueError('Dependency SDK tools have changed')
    sys.path[:0] = [str(sdk), str(candidate / '.molsyssuite-tools')]
    from devtools.scripts.dependency_constraints import check_installed

    project = tomllib.loads((candidate / 'pyproject.toml').read_text())['project']
    save('installed-bounds.json', check_installed(project))


def snapshot():
    """Retain this receiver's exact consumer/provider bytes and import origins."""
    prefix = Path(sys.prefix).resolve()
    site = Path(sysconfig.get_path('purelib')).resolve()
    runtime = {}
    for name in ('bindingmt', *PROVIDERS):
        dist = metadata.distribution(name)
        for member in dist.files or []:
            if '.dist-info/' in str(member) or str(member).endswith('.pyc'):
                continue
            path = Path(dist.locate_file(member)).resolve()
            if not path.is_relative_to(prefix):
                raise ValueError('Installed payload escapes the fresh prefix')
            runtime[str(path.relative_to(prefix))] = digest(path)
    for name, module in list(sys.modules.items()):
        if name.split('.')[0] in ('bindingmt', 'molsysviewer_bindingmt', *PROVIDERS):
            origin = getattr(module, '__file__', None)
            if origin is None:
                continue
            path = Path(origin).resolve()
            if not path.is_relative_to(site):
                raise ValueError('Consumer/provider import escapes the installed site')
    return runtime


def receive():
    candidate = require_hosted()
    minor = f'{sys.version_info.major}.{sys.version_info.minor}'
    if minor not in ('3.11', '3.13') or minor != os.environ['EXPECTED_PYTHON']:
        raise ValueError('Only the two remaining minors are selected')
    if sys.platform != 'linux' or platform.machine() != 'x86_64':
        raise ValueError('Only Linux x86_64 is qualified by this route')
    if not sys.flags.isolated or Path.cwd().resolve().is_relative_to(ROOT):
        raise ValueError('Use isolated Python outside the tooling/source checkout')
    sdk = TASK / 'installed-sdk'
    if git(sdk, 'rev-parse', 'HEAD') != INSTALLED_SDK:
        raise ValueError('Wrong installed-test SDK')
    wheel = TASK / 'wheels/bindingmt-0.1.0-py3-none-any.whl'
    expected = os.environ['EXPECTED_WHEEL_SHA256']
    if digest(wheel) != expected:
        raise ValueError('Downloaded wheel differs from the same-run build output')
    runtime = wheel_payload(wheel, frozen_receipt())
    dist = metadata.distribution('bindingmt')
    direct = json.loads(dist.read_text('direct_url.json'))
    if metadata.version('bindingmt') != '0.1.0' or (
        direct.get('archive_info', {}).get('hashes', {}).get('sha256') != expected
    ):
        raise ValueError('Ordinary installation is not the qualified private wheel')
    for name, value in runtime.items():
        if digest(Path(dist.locate_file(name))) != value:
            raise ValueError('Installed consumer bytes differ from the qualified wheel')
    for namespace in ('bindingmt', 'molsysviewer_bindingmt'):
        shutil.rmtree(candidate / namespace)
    # Shared SDK verifies the candidate's selected support files against Git.
    # Production source roots are absent; only its tests may enter the path.
    sys.path[:0] = [
        str(sdk),
        str(candidate / 'tests'),
        str(candidate / '.molsyssuite-tools'),
    ]
    from devtools.scripts.installed_noarch import run_tests
    from devtools.scripts.installed_test_support import check_unshipped_support

    check_unshipped_support('bmt_test_support', list(runtime))
    bmt = importlib.import_module('bindingmt')
    addon = importlib.import_module('molsysviewer_bindingmt.addon')
    if bmt.__version__ != '0.1.0' or addon.addon.version != '0.1.0':
        raise ValueError('Runtime/addon version attribution differs')
    if bmt.summarize_redocking({})['summarizer']['bindingmt_version'] != '0.1.0':
        raise ValueError('Summary version attribution differs')
    before = snapshot()
    metadata_before = {
        dist.metadata['Name']: hashlib.sha256(
            (dist.read_text('METADATA') or dist.read_text('PKG-INFO') or '').encode()
        ).hexdigest()
        for dist in metadata.distributions()
    }
    inventory = tomllib.loads(
        (candidate / 'devtools/conda-build/resources.toml').read_text()
    )
    inventory['import_name'] = 'bindingmt'
    evidence = TASK / 'evidence'
    inventory['installed_tests']['pytest_args'] += [
        '--junitxml=' + str(evidence / 'installed-tests.xml'),
        '--basetemp=' + str(TASK / 'pytest-scratch'),
    ]
    receipt = {
        'candidate': CANDIDATE,
        'qualification_source': os.environ['GITHUB_SHA'],
        'run_id': int(os.environ['GITHUB_RUN_ID']),
        'run_attempt': int(os.environ['GITHUB_RUN_ATTEMPT']),
        'python': platform.python_version(),
        'consumer_version': '0.1.0',
        'wheel_sha256': expected,
        'selection': inventory['installed_tests']['paths'],
        'runtime_sha256_before': before,
        'distribution_metadata_sha256_before': metadata_before,
        'completed_gate': False,
        'profile': 'new hosted wheel plus exact directory-installed sibling sources',
        'public_conda_qualification': False,
    }
    try:
        result = run_tests(
            candidate,
            inventory,
            support_output=evidence / 'support.json',
            support_context={
                'candidate_sha': CANDIDATE,
                'qualification_sha': os.environ['GITHUB_SHA'],
                'provider_sha': INSTALLED_SDK,
                'sha256': expected,
                'run_id': receipt['run_id'],
                'run_attempt': receipt['run_attempt'],
            },
        )
        receipt['pytest_exit'] = result
        after = snapshot()
        receipt['runtime_sha256_after'] = after
        if before != after:
            raise ValueError('Installed runtime payload changed during the suite')
        metadata_after = {
            dist.metadata['Name']: hashlib.sha256(
                (
                    dist.read_text('METADATA') or dist.read_text('PKG-INFO') or ''
                ).encode()
            ).hexdigest()
            for dist in metadata.distributions()
        }
        receipt['distribution_metadata_sha256_after'] = metadata_after
        if metadata_before != metadata_after:
            raise ValueError('Installed distribution metadata changed during the suite')
        if result:
            return result
        suites = ET.parse(evidence / 'installed-tests.xml').getroot()
        rows = list(suites) if suites.tag == 'testsuites' else [suites]
        totals = {
            k: sum(int(row.get(k, 0)) for row in rows)
            for k in ('tests', 'failures', 'errors', 'skipped')
        }
        receipt['tests'] = totals
        if totals != {'tests': 1761, 'failures': 0, 'errors': 0, 'skipped': 0}:
            raise ValueError('The fixed full selection did not complete without skips')
        support = json.loads((evidence / 'support.json').read_text())
        if not support['resources_retired'] or not support['imports_retired']:
            raise ValueError('Shared support was not retired')
        subprocess.run([sys.executable, '-m', 'pip', 'check'], check=True)
        receipt['completed_gate'] = True
        return 0
    finally:
        save('installed-receipt.json', receipt)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('build', 'bounds', 'receive'))
    operation = parser.parse_args().operation
    return {'build': build, 'bounds': bounds, 'receive': receive}[operation]() or 0


if __name__ == '__main__':
    raise SystemExit(main())
