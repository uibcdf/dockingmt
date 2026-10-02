from copy import deepcopy

import pytest
import pyunitwizard as puw

from dockingmt import (
    BoxRegion,
    DockingPose,
    DockingProblem,
    DockingResult,
    VinaProtocol,
)
from dockingmt._private.smonitor import ArgumentError

READERS = [BoxRegion, DockingPose, DockingProblem, DockingResult, VinaProtocol]


@pytest.fixture(params=READERS, ids=lambda reader: reader.__name__)
def reader_record(request):
    domain = BoxRegion(puw.quantity([0, 0, 0], 'nm'), puw.quantity([1, 1, 1], 'nm'))
    pose = DockingPose(puw.quantity([[0, 0, 0]], 'nm'), scores={'metric': 1})
    objects = {
        BoxRegion: domain,
        DockingPose: pose,
        DockingProblem: DockingProblem('unused_rec.pdbqt', 'unused_lig.pdbqt', domain),
        DockingResult: DockingResult([pose]),
        VinaProtocol: VinaProtocol(seed=42),
    }
    reader = request.param
    return reader, objects[reader].to_dict()


@pytest.mark.parametrize('version', ['999.0', '1', 1.0, None, True, '', {}, []])
@pytest.mark.parametrize('reader', READERS, ids=lambda reader: reader.__name__)
def test_reader_rejects_unsupported_schema_before_payload(reader, version):
    # No scientific fields: admission must fail before field access or conversion.
    with pytest.raises(ArgumentError) as caught:
        reader.from_dict({'schema_version': version})
    assert caught.value.code == 'DMT-E002'
    assert caught.value.extra['arg_name'] == 'schema_version'
    assert caught.value.extra['record_type'] == reader.__name__
    assert caught.value.extra['supported_versions'] == ['1.0']


@pytest.mark.parametrize('legacy', [False, True])
def test_reader_preserves_supported_and_legacy_round_trips(reader_record, legacy):
    reader, record = reader_record
    expected = deepcopy(record)
    if legacy:
        del record['schema_version']
    before = deepcopy(record)
    restored = reader.from_dict(record)
    assert restored.to_dict() == expected
    assert record == before


@pytest.mark.parametrize('record', [None, [], '1.0', 1])
@pytest.mark.parametrize('reader', READERS, ids=lambda reader: reader.__name__)
def test_reader_requires_mapping_record(reader, record):
    with pytest.raises(ArgumentError) as caught:
        reader.from_dict(record)
    assert caught.value.extra['arg_name'] == 'data'


def test_result_reader_validates_nested_pose_version():
    with pytest.raises(ArgumentError) as caught:
        DockingResult.from_dict(
            {'schema_version': '1.0', 'poses': [{'schema_version': '999.0'}]}
        )
    assert caught.value.extra['record_type'] == 'DockingPose'


def test_problem_reader_validates_nested_domain_before_inputs():
    with pytest.raises(ArgumentError) as caught:
        DockingProblem.from_dict(
            {
                'schema_version': '1.0',
                'search_domain': {'type': 'BoxRegion', 'schema_version': '999.0'},
            }
        )
    assert caught.value.extra['record_type'] == 'BoxRegion'


def test_result_rejects_nested_future_pose_before_copying_payload():
    class CopySentinel:
        def __deepcopy__(self, memo):
            pytest.fail('Unsupported nested pose payload was copied before admission')

    with pytest.raises(ArgumentError) as caught:
        DockingResult.from_dict(
            {
                'schema_version': '1.0',
                'poses': [{'schema_version': '999.0', 'metadata': CopySentinel()}],
            }
        )
    assert caught.value.extra['record_type'] == 'DockingPose'


@pytest.mark.parametrize('reader', [DockingPose, DockingResult])
def test_unknown_schema_rejected_before_snapshot_copy(reader):
    class CopySentinel:
        def __deepcopy__(self, memo):
            pytest.fail('Unsupported record payload was copied before admission')

    with pytest.raises(ArgumentError):
        reader.from_dict({'schema_version': '999.0', 'metadata': CopySentinel()})


def test_schema_admission_requests_no_molecular_or_optional_engine_operations(
    reader_record, monkeypatch
):
    import builtins

    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Scientific record admission requested a molecular operation')

    for name in ('get', 'select', 'extract', 'convert', 'copy', 'set'):
        monkeypatch.setattr(msm, name, forbidden)
    actual_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split('.')[0] in ('vina', 'molsysviewer'):
            pytest.fail('Scientific record reader imported an optional provider')
        return actual_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, '__import__', guarded_import)
    reader, record = reader_record
    assert reader.from_dict(record).to_dict() == record
