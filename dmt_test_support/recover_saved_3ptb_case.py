"""Verify and recover the retained 2026-10-20 3PTB human result offline.

This case-specific operation reads evidence records, never molecular systems.
It ignores historical operational paths and performs no preparation or search.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dockingmt import DockingResult

QUALIFICATION = 'qualification_2026-10-20.json'
QUALIFICATION_SHA256 = (
    'b89b8dcb9ec296d01f12cd28cb633577e868e5c60b264c5f4bb4eefd6f3b9bf2'
)
MEMBERS = {
    'result': 'native_result_2026-10-20.json.gz',
    'admission': 'admission_2026-10-20.json.gz',
    'summary': 'summary_2026-10-20.json',
    'execution': 'kernel_receipt_2026-10-20.json',
    'wheel': 'wheel_2026-10-20.json',
}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _fingerprint(path, label, *, compressed=False, limit=None):
    digest = hashlib.sha256()
    size = 0
    try:
        with gzip.open(path, 'rb') if compressed else path.open('rb') as stream:
            while block := stream.read(1024 * 1024):
                size += len(block)
                _require(
                    limit is None or size <= limit,
                    f'{label}: decoded size exceeds the record.',
                )
                digest.update(block)
    except (OSError, EOFError) as error:
        raise ValueError(f'{label}: cannot read the retained bytes.') from error
    return size, digest.hexdigest()


def _json(path, label, *, compressed=False):
    def nonfinite(_):
        raise ValueError(f'{label}: nonfinite JSON data is unsupported.')

    try:
        with gzip.open(path, 'rt') if compressed else path.open() as stream:
            result = json.load(stream, parse_constant=nonfinite)
    except (OSError, EOFError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f'{label}: cannot decode the retained JSON record.') from error
    _require(isinstance(result, dict), f'{label}: a JSON object is required.')
    return result


def _members(root, qualification):
    verified, paths = [], {}
    records = qualification.get('files')
    _require(
        isinstance(records, list) and bool(records),
        'The qualification has no file records.',
    )
    for record in records:
        _require(isinstance(record, dict), 'Invalid qualification file record.')
        name = record.get('path')
        _require(
            isinstance(name, str) and bool(name), 'Missing qualification member name.'
        )
        relative = PurePosixPath(name)
        _require(
            not relative.is_absolute()
            and '..' not in relative.parts
            and '\\' not in name,
            'A qualification member has an unsafe relative path.',
        )
        name = relative.as_posix()
        _require(
            type(record.get('bytes')) is int
            and record['bytes'] >= 0
            and isinstance(record.get('sha256'), str)
            and re.fullmatch('[0-9a-f]{64}', record['sha256']) is not None,
            f'{name}: invalid member length or digest declaration.',
        )
        if 'original_bytes' in record:
            _require(
                type(record['original_bytes']) is int and record['original_bytes'] >= 0,
                f'{name}: invalid decoded length declaration.',
            )
        path = (root / name).resolve()
        _require(
            path.is_relative_to(root)
            and name not in paths
            and path not in paths.values(),
            'A qualification member escapes the bundle or is duplicated.',
        )
        size, digest = _fingerprint(path, name)
        _require(
            size == record.get('bytes') and digest == record.get('sha256'),
            f'{name}: member length or SHA-256 differs from qualification.',
        )
        encoding = record.get('encoding', 'identity')
        _require(
            encoding in ('identity', 'gzip'), f'{name}: unsupported evidence encoding.'
        )
        decoded_size, decoded_digest = (size, digest)
        if encoding == 'gzip':
            decoded_size, decoded_digest = _fingerprint(
                path, name, compressed=True, limit=record.get('original_bytes')
            )
        for field, actual in [
            ('original_bytes', decoded_size),
            ('original_sha256', decoded_digest),
        ]:
            _require(
                field not in record or record[field] == actual,
                f'{name}: decoded evidence differs from qualification.',
            )
        paths[name] = path
        verified.append(
            {
                'path': name,
                'bytes': size,
                'sha256': digest,
                'encoding': encoding,
                'decoded_bytes': decoded_size,
                'decoded_sha256': decoded_digest,
            }
        )
    _require(
        set(MEMBERS.values()) <= paths.keys(),
        'Required saved-case evidence is missing.',
    )
    return paths, verified


def recover_saved_case(
    bundle_directory: str | Path,
    original_source: str | Path,
    *,
    qualification_sha256: str = QUALIFICATION_SHA256,
) -> tuple[DockingResult, dict[str, Any]]:
    """Return the verified saved result and a path-free record-link report.

    The default trust root is the unchanged original qualification manifest.
    An explicit alternative digest is a caller trust decision, not authentication.
    Input names follow this existing case's layout; no general archive format is
    introduced. Native systems, chemistry and a replayable problem are not restored.
    The returned result remains detached from its input record with problem=None.
    """
    _require(
        isinstance(qualification_sha256, str)
        and re.fullmatch('[0-9a-f]{64}', qualification_sha256) is not None,
        'Supply an explicit valid qualification SHA-256 trust root.',
    )
    root = Path(bundle_directory).resolve()
    qualification_path = root / QUALIFICATION
    _, digest = _fingerprint(qualification_path, 'qualification')
    _require(
        digest == qualification_sha256,
        'The qualification SHA-256 differs from the trust root.',
    )
    qualification = _json(qualification_path, 'qualification')
    _require(
        qualification.get('schema') == 'dockingmt.human_workflow_receiving@1',
        'Unsupported human-case qualification schema.',
    )
    paths, verified = _members(root, qualification)
    records = {
        role: _json(paths[name], name, compressed=name.endswith('.gz'))
        for role, name in MEMBERS.items()
    }
    _, source_digest = _fingerprint(Path(original_source), 'original source')
    record, admission, summary, execution, wheel = (
        records[name]
        for name in ('result', 'admission', 'summary', 'execution', 'wheel')
    )
    try:
        _require(
            admission['schema'] == 'dockingmt.3ptb_molecular_admission@1',
            'Unsupported molecular-admission record schema.',
        )
        _require(
            source_digest
            == admission['compressed_source_sha256']
            == execution['source_sha256'],
            'Original source bytes disagree with admission or execution evidence.',
        )
        result_identity = next(
            item for item in verified if item['path'] == MEMBERS['result']
        )
        _require(
            result_identity['decoded_sha256'] == summary['original_result_sha256'],
            'The saved result disagrees with the original result identity.',
        )
        _require(
            qualification['wheel_producer'] == wheel['producer'] == summary['producer'],
            'Original producer records disagree.',
        )
        provenance = record['provenance']
        for name in ('dockingmt', 'molsysmt'):
            _require(
                provenance[name + '_version'] == execution['versions'][name],
                f'The original {name} version records disagree.',
            )
        _require(
            provenance['backend'] == 'vina'
            and provenance['backend_version'] == execution['versions']['vina'],
            'The original backend/version records disagree.',
        )
        row = admission['population'][0]
        _require(
            (row['arm'], row['domain']) == ('rigid', 'native'),
            'The saved human case requires the registered rigid/native row.',
        )
        _require(
            row['protocol'] == record['protocol_info'] == provenance['protocol'],
            'Admission and result protocol records disagree.',
        )
        expected_box = admission['boxes']['native']['backend_projection']
        _require(
            all(
                provenance['backend_box'][key] == expected_box[key]
                for key in ('center', 'size', 'unit')
            ),
            'Admission and submitted domain records disagree.',
        )
        state_ids = {}
        for role, arm in [('receptor', 'receptor'), ('partner', 'rigid')]:
            prepared = admission['prepared_inputs'][arm]
            _require(
                prepared['prepared'] == record['problem_info'][role]['value'],
                f'{role}: admission and prepared-result declarations disagree.',
            )
            _require(
                prepared['pdbqt_sha256']
                == provenance['backend_artifacts'][role]['sha256'],
                f'{role}: admission and submitted input identities disagree.',
            )
            state_ids[role] = prepared['prepared']['state_id']
    except (KeyError, TypeError, IndexError) as error:
        raise ValueError(
            'Saved-case record links are incomplete or malformed.'
        ) from error

    import dockingmt as dmt
    from dockingmt._private.smonitor import ArgumentError

    try:
        dmt.verify_captured_inputs(provenance['backend_artifacts'])
    except ArgumentError as error:
        raise ValueError('The saved captured-input evidence is invalid.') from error
    audit = dmt.audit_result(record)
    _require(
        audit['status'] == 'consistent',
        'The saved-result consistency audit is not consistent.',
    )
    result = dmt.DockingResult.from_dict(record)
    _require(
        result.problem is None, 'Record recovery must not attach a molecular problem.'
    )
    report = {
        'schema': 'dockingmt.saved_3ptb_case_recovery@1',
        'scope': 'saved_case_file_integrity_and_record_links',
        'status': 'consistent',
        'qualification_sha256': qualification_sha256,
        'verified_files': verified,
        'source': {
            'verified_compressed_sha256': source_digest,
            'plain_sha256_declared_by_original_admission': admission['source_sha256'],
        },
        'original_result_sha256': result_identity['decoded_sha256'],
        'original_producer': qualification['wheel_producer'],
        'original_provider_sources': qualification['providers'],
        'original_versions': execution['versions'],
        'recorded_original_wheel_sha256': wheel['sha256'],
        'historical_package_files_reverified': False,
        'verifier': {
            'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'dockingmt_version': dmt.__version__,
        },
        'recovered_pose_count': len(result.poses),
        'state_ids': state_ids,
        'result_audit': audit,
        'molecular_problem_restored': False,
        'new_preparations': 0,
        'new_searches': 0,
        'new_energy_evaluations': 0,
        'limitations': [
            'Record integrity and links do not establish chemical validity or external authenticity.',
            'Native systems and mechanical assignments are not reconstructed.',
            'Original standalone prepared-input file fingerprints remain unchanged.',
        ],
    }
    return result, report


def _write_report(path, report):
    payload = json.dumps(report, indent=2, allow_nan=False) + '\n'
    path.parent.mkdir(parents=True, exist_ok=True)
    created = False
    try:
        with path.open('x') as stream:
            created = True
            stream.write(payload)
    except OSError as error:
        if created:
            try:
                path.unlink()
            except OSError as cleanup_error:
                raise ValueError(
                    'Report writing failed and the partial new report could not be removed.'
                ) from cleanup_error
        raise ValueError('Cannot write the new output report.') from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--qualification-sha256', default=QUALIFICATION_SHA256)
    args = parser.parse_args()
    try:
        _require(
            not args.report.exists(),
            'The output report already exists; choose a new file.',
        )
        _, report = recover_saved_case(
            args.bundle, args.source, qualification_sha256=args.qualification_sha256
        )
        _write_report(args.report, report)
    except (ValueError, OSError) as error:
        message = (
            str(error)
            if isinstance(error, ValueError)
            else 'Cannot create the new output report.'
        )
        raise SystemExit(message) from None
    print(
        json.dumps(
            {
                key: report[key]
                for key in (
                    'status',
                    'recovered_pose_count',
                    'original_producer',
                    'new_searches',
                )
            }
        )
    )


if __name__ == '__main__':
    main()
