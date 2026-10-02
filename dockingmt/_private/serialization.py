"""Admission policy shared by DockingMT's existing scientific record readers."""

from collections.abc import Mapping
from typing import Any

from dockingmt._private.smonitor import ArgumentError

SCHEMA_VERSION = '1.0'


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
