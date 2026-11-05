"""Controlled file failures; no native search or molecular preparation."""

import errno
import importlib
import sys
import warnings
from pathlib import Path
from types import SimpleNamespace

import pytest
import pyunitwizard as puw

from dockingmt import BoxRegion, DockingProblem, VinaBackend

engine = importlib.import_module('dockingmt.engines.vina')


@pytest.mark.parametrize('branch', ['bytes', 'prepared', 'text'])
@pytest.mark.parametrize('failure', ['write', 'flush', 'close'])
def test_staging_registers_allocation_before_fallible_io(
    monkeypatch, tmp_path, branch, failure
):
    factory = engine.tempfile.NamedTemporaryFile
    allocated = []
    primary = OSError(errno.ENOSPC, 'controlled staging failure')

    class FailingFile:
        def __init__(self, **kwargs):
            self.file = factory(dir=tmp_path, **kwargs)
            self.name = self.file.name
            allocated.append(self.name)

        def __enter__(self):
            return self

        def write(self, content):
            if failure == 'write':
                raise primary
            return self.file.write(content)

        def flush(self):
            if failure == 'flush':
                raise primary
            self.file.flush()

        def close(self):
            try:
                self.flush()
            finally:
                self.file.close()
            if failure == 'close':
                raise primary

        def __exit__(self, *args):
            self.close()

    monkeypatch.setattr(engine.tempfile, 'NamedTemporaryFile', FailingFile)
    owned = []
    try:
        with pytest.raises(OSError) as caught:
            if branch == 'bytes':
                engine._stage_pdbqt_bytes(b'ATOM test\r\n', owned)
            else:
                receptor = 'pdbqt_text:ATOM test\n'
                if branch == 'prepared':
                    receptor = SimpleNamespace(to_pdbqt=lambda: 'ATOM test\n')
                VinaBackend()._resolve_receptor_path(receptor, owned)
        assert caught.value is primary
        assert owned == allocated
        engine._cleanup_staged_files(owned)
        assert all(not Path(path).exists() for path in allocated)
    finally:
        # Retire controlled leftovers even when the regression fails before the fix.
        for path in allocated:
            Path(path).unlink(missing_ok=True)


def test_staging_keeps_exact_bytes_and_caller_owned_input(tmp_path):
    content = b'ATOM test\r\n\x00'
    caller = tmp_path / 'caller.pdbqt'
    caller.write_bytes(content)
    owned = []
    assert VinaBackend()._resolve_receptor_path(caller, owned) == str(caller)
    assert owned == []
    staged = engine._stage_pdbqt_bytes(content, owned)
    try:
        assert Path(staged).read_bytes() == content
        assert owned == [staged]
    finally:
        engine._cleanup_staged_files(owned)
    assert caller.read_bytes() == content
    assert not Path(staged).exists()


@pytest.fixture
def blocked_cleanup(monkeypatch, tmp_path):
    blocked, removable, absent = [
        tmp_path / name for name in ('blocked', 'ok', 'absent')
    ]
    blocked.write_bytes(b'controlled retained input')
    removable.write_bytes(b'controlled removable input')
    remove = engine.os.remove
    attempted = []

    def fail_one(path):
        attempted.append(path)
        if path == str(blocked):
            raise PermissionError(errno.EACCES, 'controlled removal failure', path)
        remove(path)

    monkeypatch.setattr(engine.os, 'remove', fail_one)
    return [str(blocked), str(removable), str(absent)], attempted


def test_cleanup_warns_after_attempting_all_paths(blocked_cleanup):
    paths, attempted = blocked_cleanup
    with pytest.warns(Warning) as caught:
        engine._cleanup_staged_files(paths)
    assert attempted == paths
    diagnostic = caught[0].message
    assert diagnostic.code == 'DMT-W003'
    assert diagnostic.extra['paths'] == [paths[0]]
    assert diagnostic.extra['failures'] == [
        {'path': paths[0], 'errno': errno.EACCES, 'error_type': 'PermissionError'}
    ]
    assert paths[0] in str(diagnostic)
    assert Path(paths[0]).exists()
    assert not Path(paths[1]).exists()


def test_cleanup_honors_warning_errors_after_all_attempts(blocked_cleanup):
    paths, attempted = blocked_cleanup
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        with pytest.raises(Warning) as caught:
            engine._cleanup_staged_files(paths)
    assert caught.value.code == 'DMT-W003'
    assert attempted == paths
    assert not Path(paths[1]).exists()


def test_cleanup_keeps_primary_exception_under_warning_errors(blocked_cleanup):
    paths, attempted = blocked_cleanup
    primary = RuntimeError('controlled primary failure')
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        with pytest.raises(RuntimeError) as caught:
            try:
                raise primary
            finally:
                engine._cleanup_staged_files(paths, primary_error=primary)
    assert caught.value is primary
    assert attempted == paths
    assert len(primary.__notes__) == 1
    assert 'DMT-W003' in primary.__notes__[0]
    assert paths[0] in primary.__notes__[0]


def test_cleanup_of_absent_file_is_idempotent(tmp_path):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        engine._cleanup_staged_files([str(tmp_path / 'absent')])
    assert not caught


def test_cleanup_does_not_annotate_unrelated_handled_exception(blocked_cleanup):
    paths, attempted = blocked_cleanup
    unrelated = LookupError('already handled by the caller')
    try:
        raise unrelated
    except LookupError:
        with pytest.warns(Warning):
            engine._cleanup_staged_files(paths)
    assert attempted == paths
    assert not hasattr(unrelated, '__notes__')


@pytest.mark.parametrize('operation', ['dock', 'score'])
@pytest.mark.parametrize('cleanup_fails', [False, True])
def test_backend_finally_preserves_staging_error_and_caller_files(
    monkeypatch, tmp_path, operation, cleanup_fails
):
    from depdigest.core import checker

    available = checker.is_installed
    monkeypatch.setattr(
        checker,
        'is_installed',
        lambda name: True if name == 'vina' else available(name),
    )
    monkeypatch.setitem(sys.modules, 'vina', SimpleNamespace())
    content = b'ATOM controlled input\r\n'
    files = {role: tmp_path / f'{role}.pdbqt' for role in ('receptor', 'partner')}
    for path in files.values():
        path.write_bytes(content)
    problem = DockingProblem(
        **files,
        search_domain=BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'),
            puw.quantity([10, 10, 10], 'angstrom'),
        ),
    )
    primary = OSError(errno.ENOSPC, 'controlled staging failure')
    allocated = []
    factory = engine.tempfile.NamedTemporaryFile
    monkeypatch.setattr(
        engine.tempfile,
        'NamedTemporaryFile',
        lambda **kwargs: factory(dir=tmp_path, **kwargs),
    )

    def stage(self, receptor, partner, protocol, owned):
        allocated.append(engine._stage_pdbqt_bytes(content, owned))
        raise primary

    monkeypatch.setattr(VinaBackend, '_stage_inputs', stage)
    remove = engine.os.remove

    def cleanup(path):
        assert path in allocated
        if cleanup_fails:
            raise PermissionError(errno.EACCES, 'controlled removal failure', path)
        remove(path)

    monkeypatch.setattr(engine.os, 'remove', cleanup)
    filters = list(warnings.filters)
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        with pytest.raises(OSError) as caught:
            getattr(VinaBackend(), operation)(problem)
    assert caught.value is primary
    assert len(allocated) == 1
    assert Path(allocated[0]).exists() is cleanup_fails
    assert all(path.read_bytes() == content for path in files.values())
    assert warnings.filters == filters
    if cleanup_fails:
        assert 'DMT-W003' in primary.__notes__[0]
        assert allocated[0] in primary.__notes__[0]
