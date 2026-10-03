"""Byte integrity of the captured PDBQT record, shared by audit and replay."""

import base64
import binascii
import hashlib
import re
from collections.abc import Mapping


def inspect_artifact(artifact, role):
    """Return status, bounded reason, and size; never parse molecular content."""
    if artifact is None:
        return 'incomplete', f'The {role} PDBQT artifact is missing.', None
    if (
        not isinstance(artifact, Mapping)
        or 'format' in artifact
        and artifact['format'] != 'pdbqt'
    ):
        return 'inconsistent', f'The {role} PDBQT artifact is invalid.', None
    digest = artifact.get('sha256')
    if 'sha256' in artifact and (
        not isinstance(digest, str) or re.fullmatch('[0-9a-f]{64}', digest) is None
    ):
        return 'inconsistent', f'The {role} SHA-256 digest is invalid.', None
    encoded = artifact.get('content_base64')
    if 'content_base64' in artifact and not isinstance(encoded, str):
        return 'inconsistent', f'The {role} PDBQT input bytes are invalid.', None
    content = None
    if isinstance(encoded, str):
        try:
            content = base64.b64decode(encoded, validate=True)
        except (binascii.Error, ValueError):
            return 'inconsistent', f'The {role} PDBQT input bytes are invalid.', None
    if 'format' not in artifact:
        return 'incomplete', f'The {role} PDBQT artifact format is missing.', None
    if digest is None:
        return 'incomplete', f'The {role} SHA-256 digest is missing.', None
    if content is None:
        return 'incomplete', f'The {role} PDBQT input bytes were not captured.', None
    if hashlib.sha256(content).hexdigest() != digest:
        return (
            'inconsistent',
            f'The {role} PDBQT input bytes failed SHA-256 validation.',
            None,
        )
    return 'consistent', 'sha256_matches_captured_bytes', len(content)
