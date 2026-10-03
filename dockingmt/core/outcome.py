"""One item outcome from incremental docking, separate from scientific results."""

from collections.abc import Mapping
from copy import deepcopy

from dockingmt._private.serialization import SCHEMA_VERSION, validate_schema_version
from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.results import DockingResult


class DockingOutcome:
    """A successful result or recorded item failure, with detached declarations.

    ``index`` is the zero-based input position, not a molecular or run identity.
    The successful ``result`` has the ownership of an individual ``dock`` call.
    Declaration/error properties and dictionary exports are detached snapshots.
    """

    def __init__(
        self,
        index,
        *,
        backend=None,
        problem_info=None,
        protocol_info=None,
        result=None,
        error=None,
    ):
        if type(index) is not int or index < 0:
            raise ArgumentError(arg_name='index', reason='Use a non-negative integer.')
        if (result is None) == (error is None):
            raise ArgumentError(
                arg_name='result', reason='Supply exactly one result or error summary.'
            )
        if result is not None and not isinstance(result, DockingResult):
            raise ArgumentError(arg_name='result', reason='Use a DockingResult.')
        if backend is not None and (
            not isinstance(backend, str) or not backend.strip()
        ):
            raise ArgumentError(
                arg_name='backend', reason='Use an adapter name or None.'
            )
        if error is not None and (
            not isinstance(error, Mapping)
            or set(error) != {'type', 'message', 'code'}
            or not isinstance(error['type'], str)
            or not error['type'].strip()
            or not isinstance(error['message'], str)
            or error['code'] is not None
            and (not isinstance(error['code'], str) or not error['code'].strip())
        ):
            raise ArgumentError(arg_name='error', reason='Use a typed error summary.')
        for name, value in (
            ('problem_info', problem_info),
            ('protocol_info', protocol_info),
        ):
            if value is not None and not isinstance(value, Mapping):
                raise ArgumentError(arg_name=name, reason='Use a declaration mapping.')
        self._index = index
        self._backend = backend
        self._problem_info = deepcopy(dict(problem_info or {}))
        self._protocol_info = deepcopy(dict(protocol_info or {}))
        self._error = deepcopy(dict(error)) if error is not None else None
        self._result = result

    @property
    def index(self):
        return self._index

    @property
    def status(self):
        return 'success' if self._result is not None else 'failure'

    @property
    def backend(self):
        return self._backend

    @property
    def result(self):
        return self._result

    @property
    def error(self):
        return deepcopy(self._error)

    @property
    def problem_info(self):
        return deepcopy(self._problem_info)

    @property
    def protocol_info(self):
        return deepcopy(self._protocol_info)

    def to_dict(self):
        """Export detached evidence without serializing an exception/traceback."""
        record = deepcopy(
            {
                'schema_version': SCHEMA_VERSION,
                'index': self.index,
                'status': self.status,
                'backend': self.backend,
                'problem_info': self._problem_info,
                'protocol_info': self._protocol_info,
                'error': self._error,
            }
        )
        record['result'] = None
        if self.result is not None:
            serializer = self.result.to_dict
            snapshot = serializer()
            if getattr(serializer, '__func__', None) is not DockingResult.to_dict:
                snapshot = deepcopy(snapshot)
            record['result'] = snapshot
        return record

    @classmethod
    def from_dict(cls, record):
        """Restore an outcome offline; no problem reconstruction or execution."""
        validate_schema_version(record, cls.__name__)
        result = record.get('result')
        outcome = cls(
            record.get('index'),
            backend=record.get('backend'),
            problem_info=record.get('problem_info'),
            protocol_info=record.get('protocol_info'),
            result=DockingResult.from_dict(result) if result is not None else None,
            error=record.get('error'),
        )
        if record.get('status') != outcome.status:
            raise ArgumentError(
                arg_name='status', reason='Outcome status disagrees with its payload.'
            )
        return outcome
