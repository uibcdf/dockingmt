"""Scientific axes/order survive object-key normalization without native replay."""

import hashlib
import json
from pathlib import Path

import molsysmt as msm
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bindingmt._private.interface_records import _digest

FROZEN = Path(__file__).parent / 'data/interface_order_compat/original_04'
NATIVE = Path(__file__).parent / 'data/interface_native_handoff/cb6af716'


def reordered(record, style):
    if style == 'sorted':
        return json.loads(json.dumps(record, sort_keys=True))

    def reverse(value):
        if isinstance(value, dict):
            return {k: reverse(v) for k, v in reversed(list(value.items()))}
        if isinstance(value, list):
            return [reverse(v) for v in value]
        return value

    return reverse(json.loads(json.dumps(record)))


@pytest.fixture
def source():
    return msm.h5msm.read(str(NATIVE / 'source.h5msm'))


def ionic(source, names=('zeta', 'alpha', 'middle')):
    source.interactions = {
        **source.interactions,
        'zeta': source.interactions['ionic_035'],
        'alpha': source.interactions['ionic_031'],
        'middle': source.interactions['ionic_empty'],
    }
    return bmt.characterize_interface_interactions(
        source,
        participants={'Z': [0], 'B': [1], 'A': [2]},
        grouping=[['Z', 'B'], ['A']],
        analysis_names=list(names),
        structure_index=0,
        source_id='authored-four',
    )


@pytest.mark.parametrize('style', ['sorted', 'reversed'])
@pytest.mark.parametrize('cutoff', ['.35 nm', '0 nm'])
def test_contacts_and_independent_footprints_ignore_object_key_order(
    source, tmp_path, monkeypatch, style, cutoff
):
    result = bmt.calculate_interface_contacts(
        source,
        participants={'Z': [0, 1], 'A': [2]},
        cutoff=cutoff,
        structure_index=0,
        source_id='authored-four',
    )
    raw = result.to_dict()
    changed = reordered(raw, style)
    assert changed['content_sha256'] == _digest(changed) == raw['content_sha256']
    expected = {
        name: result.project_footprint(participant=name).to_dict()['footprint']
        for name in ('Z', 'A')
    }

    def forbidden(*args, **kwargs):
        raise AssertionError('Saved reading/projection must not perform molecular work')

    monkeypatch.setattr(msm, 'get', forbidden)
    monkeypatch.setattr(msm, 'select', forbidden)
    restored = bmt.BindingInterface.from_dict(changed, experimental=True)
    assert restored.to_dict() == raw
    assert restored.grouping == [['Z'], ['A']]
    assert restored.summary()['available_projections'] == ['Z', 'A']
    for name in ('Z', 'A'):
        projected = restored.project_footprint(participant=name)
        assert projected.to_dict()['footprint'] == expected[name]
        projected.save(tmp_path / (name + '.json'))
        payload = reordered(
            json.loads((tmp_path / (name + '.json')).read_text()), style
        )
        (tmp_path / (name + '.json')).write_text(json.dumps(payload))
        saved = bmt.ContactFootprint.read(
            tmp_path / (name + '.json'), experimental=True
        )
        assert saved.to_dict() == projected.to_dict()


def test_nonidentity_source_local_maps_remain_position_aligned(source):
    moved = msm.permute_atoms(source, [3, 2, 1, 0], return_report=True)
    result = bmt.calculate_interface_contacts(
        moved['molecular_system'],
        participants={'Z': [3, 2], 'A': [1]},
        cutoff='.35 nm',
        structure_index=0,
        source_structure_index=0,
        atom_map=moved['report'],
        source_id='authored-four',
    )
    restored = bmt.BindingInterface.from_dict(
        reordered(result.to_dict(), 'sorted'), experimental=True
    )
    footprint = restored.project_footprint(participant='Z')
    assert footprint.source_atom_indices == [0, 1] and footprint.local_atom_indices == [
        3,
        2,
    ]
    assert footprint.to_dict()['footprint']['contributors'] == [[0], [1]]


@pytest.mark.parametrize('style', ['sorted', 'reversed'])
def test_unequal_surface_sides_keep_original_context_axes(source, style):
    result = bmt.calculate_interface_burial(
        source,
        participants={'Z': [0], 'A': [2]},
        probe_radius='.14 nm',
        n_sphere_points=240,
        hydrogen_policy='as_supplied',
        structure_index=0,
        source_id='authored-four',
    )
    before = result.surface_calculation
    values = {
        k: float(puw.get_value(v, to_unit='nm**2'))
        for k, v in result.burial_areas['sides'].items()
    }
    assert values['Z'] != values['A']
    restored = bmt.BindingInterface.from_dict(
        reordered(result.to_dict(), style), experimental=True
    )
    assert restored.surface_calculation == before
    assert list(restored.burial_areas['sides']) == ['Z', 'A']
    assert {
        k: float(puw.get_value(v, to_unit='nm**2'))
        for k, v in restored.burial_areas['sides'].items()
    } == values


@pytest.mark.parametrize('style', ['sorted', 'reversed'])
def test_native_05_retains_nonlexical_analysis_and_construction_order(
    source, tmp_path, style
):
    phmt = pytest.importorskip('pharmacophoremt')
    original = ionic(source)
    assert original.to_dict()['format_version'] == '0.5'
    assert original.interaction_analysis_order == ['zeta', 'alpha', 'middle']
    restored = bmt.BindingInterface.from_dict(
        reordered(original.to_dict(), style), experimental=True
    )
    model = bmt.build_interface_pharmacophore(
        restored,
        source,
        participant='A',
        radius='.02 nm',
        duplicate_policy='same_participant',
    )
    assert [c['label'] for c in model.metadata['components']] == [
        'zeta',
        'alpha',
        'middle',
    ]
    assert model.interaction_sites[0].weight == 1
    assert {
        r['component'] for r in model.interaction_sites[0].metadata['observations']
    } == {'zeta', 'alpha'}
    assert model.metadata['bindingmt_interface']['analysis_order_authority'] == 'saved'
    path = tmp_path / 'H.json'
    phmt.io.to_json(model, str(path))
    linked = restored.with_pharmacophore(
        hypothesis=model,
        participant='A',
        hypothesis_ref={
            'uri': path.name,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        },
    )
    assert (
        bmt.BindingInterface.from_dict(
            reordered(linked.to_dict(), style), experimental=True
        ).to_dict()
        == linked.to_dict()
    )


@pytest.mark.parametrize('name', ['I0.json', 'I1.json', 'I2.json'])
@pytest.mark.parametrize('style', ['sorted', 'reversed'])
def test_actual_original_04_records_remain_readable_without_rewriting_history(
    name, style, monkeypatch
):
    manifest = json.loads((FROZEN / 'manifest.json').read_text())
    path = FROZEN / name
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == manifest['records'][name]['sha256']
    record = json.loads(raw)

    def forbidden(*args, **kwargs):
        raise AssertionError('Historical reading must not access molecules')

    for attr in ('get', 'select', 'convert'):
        monkeypatch.setattr(msm, attr, forbidden)
    restored = bmt.BindingInterface.from_dict(
        reordered(record, style), experimental=True
    )
    assert restored.to_dict() == record
    expected = None if name == 'I0.json' else ['ionic_031', 'ionic_035', 'ionic_empty']
    assert restored.interaction_analysis_order == expected
    assert path.read_bytes() == raw


def test_04_unknown_order_refuses_new_construction_before_molecular_work(monkeypatch):
    pytest.importorskip('pharmacophoremt')
    interface = bmt.BindingInterface.read(FROZEN / 'I0.json', experimental=True)
    assert interface.interaction_analysis_order is None

    def forbidden(*args, **kwargs):
        raise AssertionError('Unknown order reached a native operation')

    for attr in ('get', 'select', 'get_form'):
        monkeypatch.setattr(msm, attr, forbidden)
    with pytest.raises(
        bmt.exceptions.ArgumentError, match='explicitly supply analysis_names'
    ):
        bmt.build_interface_pharmacophore(
            interface,
            object(),
            participant='C',
            radius='.02 nm',
            duplicate_policy='same_participant',
        )


def test_04_explicit_order_is_a_new_caller_choice_and_survives_linking(
    source, tmp_path
):
    phmt = pytest.importorskip('pharmacophoremt')
    interface = bmt.BindingInterface.read(FROZEN / 'I0.json', experimental=True)
    before = interface.to_dict()
    order = ['ionic_035', 'ionic_empty', 'ionic_031']
    model = bmt.build_interface_pharmacophore(
        interface,
        source,
        participant='C',
        radius='.02 nm',
        duplicate_policy='same_participant',
        analysis_names=order,
    )
    assert (
        model.metadata['bindingmt_interface']['analysis_order_authority']
        == 'caller_explicit'
    )
    assert [c['label'] for c in model.metadata['components']] == order
    path = tmp_path / 'H.json'
    phmt.io.to_json(model, str(path))
    linked = interface.with_pharmacophore(
        hypothesis=model,
        participant='C',
        hypothesis_ref={
            'uri': path.name,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        },
    )
    restored = bmt.BindingInterface.from_dict(
        reordered(linked.to_dict(), 'sorted'), experimental=True
    )
    assert restored.interaction_analysis_order == order
    assert interface.to_dict() == before


@pytest.mark.parametrize(
    'order', [['alpha', 'zeta', 'middle'], ['zeta'], ['zeta', 'zeta', 'alpha'], []]
)
def test_new_request_cannot_replace_known_saved_order(source, order):
    pytest.importorskip('pharmacophoremt')
    interface = ionic(source)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.build_interface_pharmacophore(
            interface,
            source,
            participant='A',
            radius='.02 nm',
            duplicate_policy='same_participant',
            analysis_names=order,
        )


@pytest.mark.parametrize('change', ['missing', 'duplicate', 'foreign', 'downgrade'])
def test_malformed_or_downgraded_05_order_is_refused(source, change):
    record = ionic(source).to_dict()
    contexts = (
        [record['contexts']['native_interactions']]
        + [a['native_observation']['context'] for a in record['analyses'].values()]
        + [
            a['original_claim']['contexts']['native_interactions']
            for a in record['analyses'].values()
        ]
    )
    for context in contexts:
        if change == 'missing':
            context.pop('analysis_names', None)
        elif change == 'duplicate':
            context['analysis_names'] = ['zeta', 'zeta', 'middle']
        elif change == 'foreign':
            context['analysis_names'] = ['zeta', 'alpha', 'other']
    if change == 'downgrade':
        record['format_version'] = '0.4'
    record['content_sha256'] = _digest(record)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.from_dict(record, experimental=True)


def test_h_r2_annotations_use_saved_axes_even_after_key_normalization(source):
    initial = ionic(source)
    contact = bmt.calculate_interface_contacts(
        source,
        participants={'ZZ': [0, 1], 'A': [2]},
        cutoff='.35 nm',
        structure_index=0,
        source_id='authored-four',
    )
    surface = bmt.calculate_interface_burial(
        source,
        participants={'ZZ': [0, 1], 'A': [2]},
        probe_radius='.14 nm',
        n_sphere_points=240,
        hydrogen_policy='as_supplied',
        structure_index=0,
        source_id='authored-four',
    )
    normalized = {
        k: bmt.BindingInterface.from_dict(
            reordered(v.to_dict(), 'sorted'), experimental=True
        )
        for k, v in {'contacts': contact, 'surface': surface}.items()
    }
    annotated = initial.with_characterizations(
        source, characterizations=normalized, participant='A'
    )
    restored = bmt.BindingInterface.from_dict(
        reordered(annotated.to_dict(), 'sorted'), experimental=True
    )
    assert restored.characterizations == annotated.characterizations
    assert restored.characterizations['contacts']['contributors']['atoms'][0][
        'witness_indices'
    ] == [0, 1]


def test_unknown_old_order_is_not_upgraded_by_geometric_annotation(source):
    unknown = bmt.BindingInterface.read(FROZEN / 'I0.json', experimental=True)
    contacts = bmt.calculate_interface_contacts(
        source,
        participants={'ZZ': [0, 1], 'C': [2]},
        cutoff='.35 nm',
        structure_index=0,
        source_id='authored-four',
    )
    annotated = unknown.with_characterizations(
        source, characterizations={'contacts': contacts}, participant='C'
    )
    restored = bmt.BindingInterface.from_dict(
        reordered(annotated.to_dict(), 'sorted'), experimental=True
    )
    assert restored.interaction_analysis_order is None
    assert restored.analyses == unknown.analyses


@pytest.mark.parametrize('corruption', ['unknown', 'duplicate'])
def test_unresolvable_contact_orientation_refuses_without_guessing(source, corruption):
    original = bmt.calculate_interface_contacts(
        source,
        participants={'Z': [0, 1], 'A': [2]},
        cutoff='.35 nm',
        structure_index=0,
        source_id='authored-four',
    )
    record = original.to_dict()
    options = record['analyses']['contacts']['calculation']['calls'][0]['options']
    options['selection'] = [3] if corruption == 'unknown' else options['selection_2']
    record['content_sha256'] = _digest(record)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.from_dict(record, experimental=True)


def test_malformed_old_construction_order_uses_public_argument_diagnostic():
    record = json.loads((FROZEN / 'I1.json').read_text())
    record['site_refs'][0]['construction'] = []
    record['content_sha256'] = _digest(record)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.from_dict(record, experimental=True)
