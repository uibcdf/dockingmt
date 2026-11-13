"""Public declaration evidence stays distinct, immutable and offline across I/O."""

import builtins
import json
import sys
from copy import deepcopy
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

import bindingmt as bmt


def declare(**options):
    return bmt.characterize_interface(
        **{
            'question': {'kind': 'association'},
            'participants': {
                'A': {'source_id': 'source-a'},
                'B': {'source_id': 'source-b'},
            },
            'grouping': (('A',), ('B',)),
            **options,
        }
    )


def evidence(outcome='completed', finding_refs=None):
    value = {
        'owner': 'example.owner',
        'reference': {'run_id': 'run-1', 'analysis_id': 'an-1'},
        'outcome': outcome,
        'finding_refs': []
        if outcome == 'completed' and finding_refs is None
        else finding_refs,
        'asset_refs': [{'uri': '/absent/source.zip', 'format': 'example.native'}],
        'historical_checks': [{'context': 'C0', 'status': 'match'}],
    }
    if outcome == 'failed':
        value['failure'] = {
            'stage': 'analysis',
            'diagnostic_refs': ['original-diagnostic'],
        }
    return value


def test_no_analysis_and_distinct_original_outcomes_round_trip(tmp_path):
    values = [
        declare(),
        declare(analyses={'n': evidence('unknown')}),
        declare(analyses={'n': evidence()}),
        declare(analyses={'n': evidence(finding_refs=[{'record_id': 'r-1'}])}),
        declare(analyses={'n': evidence('failed')}),
    ]
    assert values[0].summary()['analysis_presence'] == 'not_supplied'
    for index, value in enumerate(values):
        value.save(tmp_path / f'{index}.json')
        saved = bmt.BindingInterface.read(tmp_path / f'{index}.json', experimental=True)
        assert saved.to_dict() == value.to_dict()
        assert saved.record_id == value.record_id
        assert saved.summary()['asset_access'] == 'not_checked'
        assert saved.summary()['current_assessment'] == 'not_performed'
    assert [
        value.summary()['analyses']['n']['original_outcome'] for value in values[1:]
    ] == ['unknown', 'completed', 'completed', 'failed']
    assert [
        value.summary()['analyses']['n']['finding_count'] for value in values[1:]
    ] == [None, 0, 1, None]


def test_detached_ownership_and_faithful_copy():
    analyses = {'n': evidence()}
    participants = {'A': {'source_id': 'a'}, 'B': {'source_id': 'b'}}
    original = deepcopy(analyses)
    result = declare(analyses=analyses, participants=participants)
    assert analyses == original
    analyses['n']['outcome'] = 'failed'
    participants['A']['source_id'] = 'changed'
    for snapshot in (result.to_dict(), result.copy().to_dict()):
        snapshot['analyses'].clear()
    result.analyses['n']['finding_refs'].append({'record_id': 'changed'})
    result.question['kind'] = 'changed'
    assert result.analyses['n']['finding_refs'] == []
    assert result.participants['A']['source_id'] == 'a'
    assert result.copy() is not result and result.copy().to_dict() == result.to_dict()
    with pytest.raises(FrozenInstanceError):
        result._json = '{}'


def test_revision_retains_original_analysis_claim_and_bounded_parent_history(tmp_path):
    original = declare(analyses={'n': evidence()})
    first = original.revise(
        question={'kind': 'association', 'description': 'new interpretation'},
        reason='curation',
    )
    second = first.revise(
        question={'kind': 'association', 'description': 'follow-up'}, reason='review'
    )
    assert len({original.record_id, first.record_id, second.record_id}) == 3
    assert second.to_dict()['derivation'] == {
        'parents': [first.record_id],
        'reason': 'review',
    }
    assert second.analyses == original.analyses
    assert second.analyses['n']['original_claim']['question'] == {'kind': 'association'}
    assert original.question == {'kind': 'association'}
    second.save(tmp_path / 'second.json')
    assert (
        bmt.BindingInterface.read(tmp_path / 'second.json', experimental=True).to_dict()
        == second.to_dict()
    )


@pytest.mark.parametrize('outcome', ['unknown', 'completed', 'failed'])
def test_default_read_and_inspection_probe_no_assets_or_molecular_sources(
    tmp_path, monkeypatch, outcome
):
    value = declare(analyses={'n': evidence(outcome)}, context_policy='require_match')
    target = tmp_path / 'record.json'
    value.save(target)
    original_open = Path.open
    original_import = builtins.__import__

    def only_core(path, *args, **kwargs):
        assert path == target
        return original_open(path, *args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail('Core read/inspection performed lookup, import or molecular work')

    def no_optional(name, *args, **kwargs):
        assert name.split('.')[0] not in {'topomt', 'pharmacophoremt', 'vina'}
        return original_import(name, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(Path, 'open', only_core)
        patch.setattr(builtins, '__import__', no_optional)
        for name in ('get', 'convert', 'select'):
            patch.setattr(sys.modules['molsysmt'], name, forbidden)
        restored = bmt.BindingInterface.read(target, experimental=True)
        summary = restored.copy().summary()
        assert summary['analyses']['n']['original_outcome'] == outcome
        assert summary['analyses']['n']['historical_checks'] == [
            {'context': 'C0', 'status': 'match'}
        ]
        assert summary['context_policy_applicability'] == 'not_applicable'
        assert summary['molecular_correspondence'] == 'not_required'
        assert summary['current_assessment'] == 'not_performed'


@pytest.mark.parametrize(
    'scope', ['molecular_correspondence', 'current_finding', '', None]
)
def test_stronger_or_unknown_assurance_is_refused(scope):
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare(assurance_scope=scope)


@pytest.mark.parametrize(
    'options',
    [
        {'question': {}},
        {'question': {'kind': 'prediction'}},
        {'question': {'kind': 'association', 'required_new_semantics': True}},
        {'participants': {'A': {'id': 'a'}}},
        {'participants': {'A': {}, 'B': {'id': 'b'}}},
        {'grouping': []},
        {'grouping': [['A'], []]},
        {'grouping': [['A'], ['A']]},
        {'grouping': [['A'], ['C']]},
        {'grouping': {'A', 'B'}},
        {'context_policy': 'trust'},
        {'claim_status': 'validated'},
        {'extensions': {'unscoped': {}}},
    ],
)
def test_malformed_core_is_refused_without_mutation(options):
    before = deepcopy(options)
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare(**options)
    assert options == before


@pytest.mark.parametrize(
    'changes',
    [
        {'outcome': 'completed', 'finding_refs': None},
        {'outcome': 'unknown', 'finding_refs': []},
        {'outcome': 'failed', 'finding_refs': [], 'failure': {'stage': 'analysis'}},
        {'outcome': 'failed', 'finding_refs': None},
        {'outcome': 'unsupported'},
        {'authority': 'owner_verified'},
        {'finding_refs': [{}]},
        {'context_refs': ['absent']},
        {'failure': {'stage': 'analysis'}},
        {'required_new_semantics': True},
    ],
)
def test_malformed_analysis_cannot_become_successful_empty(changes):
    value = {**evidence(), **changes}
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare(analyses={'n': value})


@pytest.mark.parametrize('version', [None, 1, '1.0', '0.2'])
def test_missing_legacy_and_future_versions_are_not_silently_admitted(version):
    record = declare().to_dict()
    if version is None:
        del record['format_version']
    else:
        record['format_version'] = version
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.from_dict(record, experimental=True)


def test_experimental_opt_in_and_unknown_required_fields(tmp_path):
    value = declare()
    value.save(tmp_path / 'record.json')
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.from_dict(value.to_dict())
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.read(tmp_path / 'record.json')
    record = value.to_dict()
    record['future_core'] = {'required': True}
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.from_dict(record, experimental=True)


def test_namespaced_opaque_extensions_survive_without_dynamic_import(tmp_path):
    value = declare(
        extensions={
            'unavailable.owner': {'format': 'future', 'payload': [1, None, 'unknown']}
        }
    )
    value.save(tmp_path / 'record.json')
    assert (
        bmt.BindingInterface.read(tmp_path / 'record.json', experimental=True).to_dict()
        == value.to_dict()
    )


def test_exclusive_save_and_malformed_reads_preserve_existing_bytes(tmp_path):
    value = declare()
    target = tmp_path / 'record.json'
    value.save(target)
    before = target.read_bytes()
    with pytest.raises(FileExistsError):
        declare().save(target)
    assert target.read_bytes() == before
    for malformed in ('{', '{"format": 1, "format": 2}'):
        broken = tmp_path / 'broken.json'
        broken.write_text(malformed)
        with pytest.raises((json.JSONDecodeError, bmt.exceptions.ArgumentError)):
            bmt.BindingInterface.read(broken, experimental=True)
        assert broken.read_text() == malformed
    with pytest.raises(FileNotFoundError):
        bmt.BindingInterface.read(tmp_path / 'missing.json', experimental=True)


@pytest.mark.parametrize('stage', ['write', 'flush', 'close'])
def test_failed_owned_write_cleans_new_file_and_preserves_error(
    tmp_path, monkeypatch, stage
):
    original = Path.open
    error = (
        MemoryError('allocation interrupted')
        if stage == 'flush'
        else OSError(28, 'disk full')
    )

    class FailingWrite:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.stream.close()

        def fileno(self):
            return self.stream.fileno()

        def write(self, value):
            self.stream.write('partial')
            if stage == 'write':
                raise error

        def flush(self):
            if stage == 'flush':
                raise error
            self.stream.flush()

        def close(self):
            self.stream.close()
            if stage == 'close':
                raise error

    def open_failing(path, *args, **kwargs):
        return FailingWrite(original(path, *args, **kwargs))

    with monkeypatch.context() as patch:
        patch.setattr(Path, 'open', open_failing)
        with pytest.raises(type(error)) as caught:
            declare().save(tmp_path / 'new.json')
        assert caught.value is error
    assert not (tmp_path / 'new.json').exists()


@pytest.mark.parametrize(
    'value', [float('nan'), float('inf'), (1, 2), object(), {1: 'bad key'}]
)
def test_opaque_data_still_requires_finite_json(value):
    with pytest.raises(bmt.exceptions.ArgumentError):
        declare(extensions={'example.owner': value})


def test_unknown_keywords_use_argdigest_and_policy_survives_read(tmp_path):
    with pytest.raises(UnknownArgumentError):
        bmt.characterize_interface(questoin={})
    with puw.context(standard_units=['pm', 'fs']):
        before = puw.configure.report()
        value = declare()
        value.save(tmp_path / 'record.json')
        bmt.BindingInterface.read(tmp_path / 'record.json', experimental=True)
        assert puw.configure.report() == before


def test_changed_payload_with_original_identity_and_digest_is_refused():
    record = declare().to_dict()
    record['question']['description'] = 'changed outside revision API'
    before = deepcopy(record)
    with pytest.raises(bmt.exceptions.ArgumentError) as caught:
        bmt.BindingInterface.from_dict(record, experimental=True)
    assert caught.value.extra['arg_name'] == 'content_sha256'
    assert record == before
