"""Shared offline persistence for BindingMT interface records and footprints."""

import hashlib
import json
import os
from pathlib import Path

from argdigest import arg_digest

from bindingmt._private.smonitor import ArgumentError


def _digest(record):
    content = {key: value for key, value in record.items() if key != 'content_sha256'}
    return hashlib.sha256(
        json.dumps(
            content, sort_keys=True, separators=(',', ':'), allow_nan=False
        ).encode()
    ).hexdigest()


def _require(condition, field, reason):
    if not condition:
        raise ArgumentError(arg_name=field, reason=reason)


class _InterfaceRecordIO:
    """Actual common lifecycle; concrete records retain their own admission."""

    @property
    def record_id(self):
        return self.to_dict()['record_id']

    def to_dict(self):
        """Return a detached finite JSON record; resolve no external references."""
        return json.loads(self._json)

    @classmethod
    @arg_digest(config='bindingmt._argdigest')
    def from_dict(cls, record, *, experimental=False):
        return cls(record, experimental=experimental)

    def copy(self):
        """Faithful detached copy, preserving declaration and original evidence identity."""
        return type(self)(self.to_dict(), experimental=True)

    @arg_digest(config='bindingmt._argdigest')
    def save(self, path):
        """Exclusively create a JSON file; preserve existing files on every failure.

        A failed new-file write is removed only if its inode is still ours.
        Filesystem exceptions propagate without becoming scientific outcomes.
        """
        payload = self._json + '\n'
        target = Path(path)
        stream = target.open('x', encoding='utf-8')
        owned = None
        try:
            owned = os.fstat(stream.fileno())
            stream.write(payload)
            stream.flush()
            stream.close()
        except BaseException:
            try:
                stream.close()
            except BaseException:
                pass  # A secondary close failure must preserve the original error.
            if owned is not None:
                try:
                    current = target.lstat()
                    if (current.st_dev, current.st_ino) == (owned.st_dev, owned.st_ino):
                        target.unlink()
                except OSError:
                    pass  # Preserve the original failure; never remove a replacement.
            raise

    @classmethod
    @arg_digest(config='bindingmt._argdigest')
    def read(cls, path, *, experimental=False):
        """Read only this core JSON; never locate assets, import owners or restore policy."""
        _require(experimental is True, 'experimental', 'Opt in with experimental=True.')

        def unique_object(pairs):
            result = {}
            for name, value in pairs:
                _require(
                    name not in result,
                    'record',
                    'Duplicate JSON object keys are invalid.',
                )
                result[name] = value
            return result

        with Path(path).open(encoding='utf-8') as stream:
            record = json.load(stream, object_pairs_hook=unique_object)
        return cls(record, experimental=True)
