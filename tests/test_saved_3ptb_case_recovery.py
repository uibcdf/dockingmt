"""The retained human case can be verified and recovered without molecular work."""

import gzip
import hashlib
import json
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

import molsysmt as msm
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools import recover_saved_3ptb_case as tool

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / 'devguide/validation/data/human_3ptb'
SOURCE = ROOT / 'devguide/validation/data/3ptb_prospective/3PTB.pdb.gz'


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture(scope='module', autouse=True)
def preserve_originals():
    files = [SOURCE, *[p for p in ORIGINAL.iterdir() if p.is_file()]]
    before = {p: _sha(p.read_bytes()) for p in files}
    yield
    assert before == {p: _sha(p.read_bytes()) for p in files}


@pytest.fixture
def bundle():
    with TemporaryDirectory(prefix='dockingmt-saved-case-test-') as directory:
        root = Path(directory) / 'relocated'
        shutil.copytree(ORIGINAL, root)
        yield root


def _record(bundle, name):
    raw = (bundle / name).read_bytes()
    return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)


def _replace(bundle, name, record):
    raw = json.dumps(record, allow_nan=False).encode()
    (bundle / name).write_bytes(
        gzip.compress(raw, compresslevel=1, mtime=0) if name.endswith('.gz') else raw
    )


def _refresh_manifest(bundle, names):
    qualification = _record(bundle, tool.QUALIFICATION)
    for entry in qualification['files']:
        if entry['path'] not in names:
            continue
        raw = (bundle / entry['path']).read_bytes()
        decoded = gzip.decompress(raw) if entry.get('encoding') == 'gzip' else raw
        entry.update(bytes=len(raw), sha256=_sha(raw))
        if 'original_bytes' in entry:
            entry['original_bytes'] = len(decoded)
        if 'original_sha256' in entry:
            entry['original_sha256'] = _sha(decoded)
    _replace(bundle, tool.QUALIFICATION, qualification)
    return _sha((bundle / tool.QUALIFICATION).read_bytes())


def _forbidden(*args, **kwargs):
    pytest.fail(
        'Saved case recovery must not perform molecular work or native computation.'
    )


def test_original_case_restores_five_poses_and_original_identity_without_molecular_work(
    monkeypatch,
):
    for name in ('dock', 'score', 'prepare_ligand', 'prepare_receptor'):
        monkeypatch.setattr(dmt, name, _forbidden)
    for name in ('get', 'select', 'convert', 'extract', 'copy'):
        monkeypatch.setattr(msm, name, _forbidden)
    with puw.context(standard_units=['pm', 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        result, report = tool.recover_saved_case(ORIGINAL, SOURCE)
        assert puw.configure.report() == policy
    assert len(result.poses) == report['recovered_pose_count'] == 5
    assert result.problem is None and report['molecular_problem_restored'] is False
    assert len(report['verified_files']) == 16
    assert report['status'] == report['result_audit']['status'] == 'consistent'
    assert report['original_producer'] == '1decee504b112cfd92026c52dcbe22449de30f4f'
    assert report['original_versions']['dockingmt'] == '0.0.0+180.g1decee5'
    assert report['verifier']['dockingmt_version'] == dmt.__version__
    assert (
        report['new_searches']
        == report['new_preparations']
        == report['new_energy_evaluations']
        == 0
    )
    assert all(
        info['source_fingerprint'] is None
        for info in result.problem_info['molecular_inputs'].values()
    )
    text = json.dumps(report)
    assert '/tmp/' not in text and '/home/' not in text
    assert 'imports' not in report and 'restored_result_source' not in report


def test_relocated_bundle_ignores_historical_operational_paths(bundle):
    result, report = tool.recover_saved_case(bundle, SOURCE)
    assert len(result.poses) == 5
    assert report['qualification_sha256'] == tool.QUALIFICATION_SHA256
    assert (
        report['original_result_sha256']
        == 'ed0eeb3ade25e54f8a5829729578fcbec9f0d73d6c0ceb03d146b0c3492d7fac'
    )


def test_member_symlink_cannot_escape_the_supplied_bundle(bundle, tmp_path):
    member = bundle / tool.MEMBERS['result']
    outside = tmp_path / member.name
    outside.write_bytes(member.read_bytes())
    member.unlink()
    member.symlink_to(outside)
    with pytest.raises(ValueError, match='escapes the bundle'):
        tool.recover_saved_case(bundle, SOURCE)


@pytest.mark.parametrize('kind', ['changed', 'missing'])
def test_changed_or_missing_member_rejects_before_result_reading(
    bundle, kind, monkeypatch
):
    target = bundle / tool.MEMBERS['result']
    if kind == 'changed':
        target.write_bytes(target.read_bytes() + b'changed')
    else:
        target.unlink()
    monkeypatch.setattr(dmt.DockingResult, 'from_dict', _forbidden)
    with pytest.raises(ValueError):
        tool.recover_saved_case(bundle, SOURCE)


def test_wrong_qualification_trust_root_rejects_before_member_reads(bundle):
    with pytest.raises(ValueError, match='trust root'):
        tool.recover_saved_case(bundle, SOURCE, qualification_sha256='0' * 64)


@pytest.mark.parametrize('digest', [None, 'bad', 123])
def test_malformed_trust_root_is_not_optional(digest):
    with pytest.raises(ValueError, match='trust root'):
        tool.recover_saved_case(ORIGINAL, SOURCE, qualification_sha256=digest)


def test_wrong_source_bytes_reject_without_a_molecular_reader(
    bundle, tmp_path, monkeypatch
):
    source = tmp_path / 'wrong-source'
    source.write_bytes(b'not the original compressed source')
    monkeypatch.setattr(msm, 'convert', _forbidden)
    with pytest.raises(ValueError, match='source bytes'):
        tool.recover_saved_case(bundle, source)


@pytest.mark.parametrize(
    'damage', ['path', 'duplicate', 'encoding', 'decoded', 'missing_required']
)
def test_explicitly_trusted_manifest_still_requires_valid_member_evidence(
    bundle, damage
):
    q = _record(bundle, tool.QUALIFICATION)
    if damage == 'path':
        q['files'][0]['path'] = '../outside'
    elif damage == 'duplicate':
        q['files'].append(deepcopy(q['files'][0]))
    elif damage == 'encoding':
        q['files'][0]['encoding'] = 'unsupported'
    elif damage == 'decoded':
        entry = next(x for x in q['files'] if x.get('encoding') == 'gzip')
        entry['original_sha256'] = '0' * 64
    else:
        q['files'] = [x for x in q['files'] if x['path'] != tool.MEMBERS['execution']]
    _replace(bundle, tool.QUALIFICATION, q)
    digest = _sha((bundle / tool.QUALIFICATION).read_bytes())
    with pytest.raises(ValueError):
        tool.recover_saved_case(bundle, SOURCE, qualification_sha256=digest)


@pytest.mark.parametrize(
    'damage',
    ['producer', 'source', 'protocol', 'domain', 'prepared', 'captured', 'score'],
)
def test_self_consistent_file_hashes_do_not_hide_broken_record_links(bundle, damage):
    names = set()
    if damage in ('producer', 'source'):
        name = (
            tool.MEMBERS['summary']
            if damage == 'producer'
            else tool.MEMBERS['execution']
        )
        r = _record(bundle, name)
        r['producer' if damage == 'producer' else 'source_sha256'] = '0' * (
            40 if damage == 'producer' else 64
        )
        _replace(bundle, name, r)
        names.add(name)
    else:
        name = tool.MEMBERS['result']
        r = _record(bundle, name)
        if damage == 'protocol':
            r['protocol_info']['parameters']['seed'] = 99
        elif damage == 'domain':
            r['provenance']['backend_box']['center'][0] += 10
        elif damage == 'prepared':
            r['problem_info']['partner']['value']['state_id'] = 'different-state'
        elif damage == 'captured':
            r['provenance']['backend_artifacts']['partner']['content_base64'] = (
                'Y2hhbmdlZA=='
            )
        else:
            r['poses'][0]['scores']['vina'] += 1
        _replace(bundle, name, r)
        names.add(name)
        summary_name = tool.MEMBERS['summary']
        summary = _record(bundle, summary_name)
        summary['original_result_sha256'] = _sha(
            gzip.decompress((bundle / name).read_bytes())
        )
        _replace(bundle, summary_name, summary)
        names.add(summary_name)
    trusted = _refresh_manifest(bundle, names)
    with pytest.raises(ValueError):
        tool.recover_saved_case(bundle, SOURCE, qualification_sha256=trusted)


def _command(bundle, report):
    return [
        sys.executable,
        '-m',
        'devtools.recover_saved_3ptb_case',
        '--bundle',
        str(bundle),
        '--source',
        str(SOURCE),
        '--report',
        str(report),
    ]


def test_cli_writes_new_report_and_preserves_existing_output(tmp_path):
    report = tmp_path / 'report.json'
    initial = subprocess.run(
        _command(ORIGINAL, report), cwd=ROOT, capture_output=True, text=True
    )
    assert initial.returncode == 0, initial.stderr
    content = report.read_bytes()
    assert json.loads(content)['recovered_pose_count'] == 5
    repeated = subprocess.run(
        _command(ORIGINAL, report), cwd=ROOT, capture_output=True, text=True
    )
    assert repeated.returncode != 0 and 'already exists' in repeated.stderr
    assert report.read_bytes() == content


def test_cli_failure_creates_no_report(bundle, tmp_path):
    (bundle / tool.MEMBERS['result']).unlink()
    report = tmp_path / 'new' / 'report.json'
    result = subprocess.run(
        _command(bundle, report), cwd=ROOT, capture_output=True, text=True
    )
    assert result.returncode != 0 and not report.exists()
    assert not report.parent.exists()


@pytest.mark.parametrize('cleanup_fails', [False, True])
def test_failed_write_removes_partial_or_reports_cleanup_failure(
    tmp_path, monkeypatch, cleanup_fails
):
    report = tmp_path / 'report.json'
    original = Path.open

    class FailedWrite:
        def __enter__(self):
            self.stream = original(report, 'x')
            return self

        def write(self, text):
            self.stream.write('partial')
            raise OSError('simulated write failure')

        def __exit__(self, *unused):
            self.stream.close()

    monkeypatch.setattr(
        Path,
        'open',
        lambda self, *a, **k: (
            FailedWrite() if self == report else original(self, *a, **k)
        ),
    )
    if cleanup_fails:

        def failed_unlink(self, *args, **kwargs):
            raise OSError('simulated cleanup failure')

        monkeypatch.setattr(Path, 'unlink', failed_unlink)
    message = 'could not be removed' if cleanup_fails else 'Cannot write'
    with pytest.raises(ValueError, match=message):
        tool._write_report(report, {'status': 'consistent'})
    assert report.exists() is cleanup_fails
