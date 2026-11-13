"""Admission policy shared by BindingMT's existing scientific record readers."""

from collections.abc import Mapping
from math import isfinite
from typing import Any

from bindingmt._private.smonitor import ArgumentError

SCHEMA_VERSION = '1.0'


def json_copy(value, argument):
    """Detach finite JSON without coercing keys, arrays or arbitrary objects."""
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ArgumentError(arg_name=argument, reason='JSON keys must be strings.')
        return {key: json_copy(item, argument) for key, item in value.items()}
    if isinstance(value, list):
        return [json_copy(item, argument) for item in value]
    if value is None or type(value) in (str, bool, int):
        return value
    if type(value) is float and isfinite(value):
        return value
    raise ArgumentError(arg_name=argument, reason='Supply finite JSON values.')


def validate_schema_version(record: Any, record_type: str) -> None:
    """Admit schema 1.0, including legacy records without a version field.

    An explicit version must be the supported string. Validate before copying or
    interpreting payload fields; this does not migrate or modify the record.
    """
    if not isinstance(record, Mapping):
        raise ArgumentError(
            arg_name='data',
            reason='Use a mapping containing a scientific object record.',
            record_type=record_type,
            value_type=type(record).__name__,
        )
    version = record.get('schema_version', SCHEMA_VERSION)
    if not isinstance(version, str) or version != SCHEMA_VERSION:
        raise ArgumentError(
            arg_name='schema_version',
            reason=(
                f"Only schema version '{SCHEMA_VERSION}' is supported. "
                'A missing version denotes a legacy 1.0 record.'
            ),
            record_type=record_type,
            received_version=version,
            supported_versions=[SCHEMA_VERSION],
        )
