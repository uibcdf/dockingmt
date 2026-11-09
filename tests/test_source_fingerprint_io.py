"""Identified file read failures retain their original filesystem meaning."""

import errno
import hashlib
from pathlib import Path

import pytest

import dockingmt as dmt
from dockingmt.exceptions import ArgumentError


def make_problem(receptor):
    return dmt.DockingProblem(
        receptor,
        'unused-ligand.pdbqt',
        dmt.BoxRegion('[0,0,0] angstrom', '[10,10,10] angstrom'),
    )


@pytest.mark.parametrize('route', ['construct', 'restore'])
@pytest.mark.parametrize('step', ['open', 'read'])
@pytest.mark.parametrize(
    'kind', [PermissionError, FileNotFoundError, OSError, MemoryError]
)
def test_public_file_fingerprint_propagates_exact_read_failure(
    tmp_path, monkeypatch, route, step, kind
):
    source = tmp_path / 'receptor.pdbqt'
    source.write_text('REMARK fixed tiny file\n')
    record = make_problem(source).to_dict()
    original_open = Path.open
    error = kind('original read failure')
    visits = []

    class BrokenReader:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            visits.append('closed')

        def read(self, *args):
            visits.append('read')
            raise error

    def controlled_open(path, *args, **kwargs):
        if path == source:
            visits.append('open')
            if step == 'open':
                raise error
            return BrokenReader()
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'open', controlled_open)
    with pytest.raises(kind) as caught:
        if route == 'construct':
            make_problem(source)
        else:
            dmt.DockingProblem.from_dict(record)
    assert caught.value is error
    assert visits == (['open'] if step == 'open' else ['open', 'read', 'closed'])


@pytest.mark.parametrize(
    'content', [b'', b'REMARK exact content\n', b'x' * (1024 * 1024 + 1)]
)
@pytest.mark.parametrize('as_path', [False, True])
def test_file_hash_binds_exact_bytes_including_chunked_reads(
    tmp_path, content, as_path
):
    source = tmp_path / 'receptor.pdbqt'
    source.write_bytes(content)
    item = make_problem(source if as_path else str(source))
    expected = {'kind': 'file', 'sha256': hashlib.sha256(content).hexdigest()}
    assert (
        item.to_dict()['molecular_inputs']['receptor']['source_fingerprint'] == expected
    )
    assert dmt.DockingProblem.from_dict(item.to_dict()).to_dict() == item.to_dict()


@pytest.mark.parametrize(
    'literal',
    ['missing.pdbqt', 'pdbqt_text:REMARK literal\n', 'pdbqt_text:' + 'A' * 5000],
)
def test_literal_and_nonfile_inputs_keep_their_existing_identity(literal):
    item = make_problem(literal)
    assert item.to_dict()['molecular_inputs']['receptor']['source_fingerprint'] == {
        'kind': 'literal',
        'sha256': hashlib.sha256(literal.encode()).hexdigest(),
    }


def test_changed_file_content_is_distinct_from_an_io_failure(tmp_path):
    source = tmp_path / 'receptor.pdbqt'
    source.write_text('REMARK original\n')
    record = make_problem(source).to_dict()
    source.write_text('REMARK changed\n')
    with pytest.raises(ArgumentError, match='source content has changed'):
        dmt.DockingProblem.from_dict(record)
    assert (
        record['molecular_inputs']['receptor']['source_fingerprint']['sha256']
        == hashlib.sha256(b'REMARK original\n').hexdigest()
    )


def test_failed_file_read_never_produces_a_literal_snapshot(tmp_path, monkeypatch):
    source = tmp_path / 'receptor.pdbqt'
    source.write_text('REMARK input\n')
    original_open = Path.open
    error = OSError(errno.EIO, 'input read failed', str(source))

    def fail(path, *args, **kwargs):
        if path == source:
            raise error
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'open', fail)
    with pytest.raises(OSError) as caught:
        make_problem(source)
    assert caught.value is error and caught.value.errno == errno.EIO
