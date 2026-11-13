"""H-R2: actual geometric evidence composition preserves native query semantics."""

import hashlib
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from pyunitwizard.record import RecordError

import bindingmt as bmt
from bindingmt._private.interface_annotations import KEY
from bindingmt._private.interface_records import _digest

INPUTS = Path(__file__).parent / 'data/interface_native_handoff/cb6af716'


@pytest.fixture
def source():
    return msm.h5msm.read(str(INPUTS / 'source.h5msm'))


def characterize(source):
    return bmt.characterize_interface_interactions(
        source,
        participants={'A': [0], 'B': [1], 'C': [2]},
        grouping=[['A', 'B'], ['C']],
        analysis_names=['ionic_031', 'ionic_035', 'ionic_empty'],
        structure_index=0,
        source_id='authored-four',
    )


def evidence(source, **options):
    common = {
        'participants': {'AB': [0, 1], 'C': [2]},
        'structure_index': 0,
        'source_id': 'authored-four',
        **options,
    }
    return {
        'contacts': bmt.calculate_interface_contacts(source, cutoff='.35 nm', **common),
        'burial': bmt.calculate_interface_burial(
            source,
            probe_radius='.14 nm',
            n_sphere_points=240,
            hydrogen_policy='as_supplied',
            **common,
        ),
    }


def model(source, interface):
    pytest.importorskip('pharmacophoremt')
    return bmt.build_interface_pharmacophore(
        interface,
        source,
        participant='C',
        radius='.02 nm',
        duplicate_policy='same_participant',
    )


def ref(path):
    return {'uri': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def test_actual_ionic_and_geometry_composition_retains_each_definition(
    source, tmp_path
):
    phmt = pytest.importorskip('pharmacophoremt')
    initial = characterize(source)
    query = model(source, initial)
    path = tmp_path / 'H0.json'
    phmt.io.to_json(query, str(path))
    linked = initial.with_pharmacophore(
        hypothesis=query, hypothesis_ref=ref(path), participant='C'
    )
    snapshot = linked.to_dict()
    original_bytes = path.read_bytes()
    calculations = evidence(source)
    annotated = linked.with_characterizations(
        source, characterizations=calculations, participant='C'
    )
    assert linked.to_dict() == snapshot and path.read_bytes() == original_bytes
    assert annotated.to_dict()['derivation']['parents'] == [linked.record_id]
    assert annotated.analyses == linked.analyses
    assert annotated.to_dict()['site_refs'] == linked.to_dict()['site_refs']
    assert [entry['definition'] for entry in annotated.characterizations.values()] == [
        'bindingmt.cartesian_atomic_contacts@1',
        'bindingmt.cartesian_sasa_burial@1',
    ]
    for label, result in calculations.items():
        assert annotated.characterizations[label]['record'] == result.to_dict()
    assert annotated.characterizations['contacts']['contributors'] == {
        'kind': 'contact_pair',
        'atoms': [
            {'source_atom_index': 2, 'local_atom_index': 2, 'witness_indices': [0, 1]}
        ],
    }
    assert annotated.characterizations['burial']['contributors'] == {
        'kind': 'atomic_loss_position',
        'atoms': [
            {'source_atom_index': 2, 'local_atom_index': 2, 'witness_indices': [0]}
        ],
    }
    assert len(initial.interaction_analyses['ionic_031']['observations']) == 1
    assert len(calculations['contacts'].contact_calculation['local_pairs']) == 2
    extension = annotated.to_dict()['extensions'][KEY]
    assert (
        extension['scope'] == 'participant_evidence'
        and extension['query_semantics'] == 'unchanged'
    )
    assert extension['source_assessment'] == 'historical_checked_at_annotation'
    assert extension['query_reference'] is None
    annotated.save(tmp_path / 'I2.json')
    restored = bmt.BindingInterface.read(tmp_path / 'I2.json', experimental=True)
    assert restored.to_dict() == annotated.to_dict()
    assert restored.copy().to_dict() == restored.to_dict()
    revised = restored.revise(
        question={'kind': 'association', 'description': 'new interpretation'},
        reason='new question',
    )
    assert revised.characterizations == restored.characterizations
    assert (
        revised.to_dict()['extensions'][KEY]['source_interface_record_id']
        == linked.record_id
    )
    assert all(
        item['current_assessment'] == 'not_performed'
        for item in restored.summary()['characterizations'].values()
    )


@pytest.mark.parametrize(
    'case',
    [
        'primary_self',
        'primary_alternative',
        'alternative_self',
        'alternative_primary',
        'zero_essential',
        'excluded',
        'keep',
    ],
)
def test_annotation_preserves_query_fields_and_independent_decisions(
    source, tmp_path, case
):
    phmt = pytest.importorskip('pharmacophoremt')
    from pharmacophoremt.screening import PoseEvaluator

    alternative = msm.h5msm.read(str(INPUTS / 'alternative.h5msm'))
    native_source = alternative if case.startswith('alternative_') else source
    initial = characterize(native_source)
    if case in ('zero_essential', 'excluded'):
        query = phmt.io.load_json(str(INPUTS / (case + '.json')))
    else:
        query = bmt.build_interface_pharmacophore(
            initial,
            native_source,
            participant='C',
            radius='.02 nm',
            duplicate_policy='keep' if case == 'keep' else 'same_participant',
        )
    target = (
        alternative
        if case == 'primary_alternative'
        else source
        if case == 'alternative_primary'
        else native_source
    )
    expected = (
        ('not_matched', 0)
        if case.endswith(('_alternative', '_primary'))
        else (
            ('not_matched', 0.5)
            if case == 'keep'
            else ('not_matched', 1)
            if case in ('zero_essential', 'excluded')
            else ('matched', 1)
        )
    )
    before = PoseEvaluator(query).evaluate(target, selection=[2])
    path = tmp_path / (case + '.json')
    phmt.io.to_json(query, str(path))
    payload = path.read_bytes()
    # Query-only/curated constraints use an explicitly caller-declared reference;
    # no observed-construction authority is fabricated by this annotation route.
    annotated = initial.with_characterizations(
        native_source,
        characterizations=evidence(native_source),
        participant='C',
        query_ref=ref(path),
    )
    annotated.save(tmp_path / 'I2.json')
    assert path.read_bytes() == payload
    restored_query = phmt.io.load_json(str(path))
    restored = bmt.BindingInterface.read(tmp_path / 'I2.json', experimental=True)
    again = tmp_path / 'query-readback.json'
    phmt.io.to_json(restored_query, str(again))
    assert again.read_bytes() == payload
    after = PoseEvaluator(restored_query).evaluate(target, selection=[2])
    for measured in (before, after):
        assert measured['status'] == expected[0] and measured[
            'fit_value'
        ] == pytest.approx(expected[1])
    assert restored.to_dict()['extensions'][KEY]['query_reference'] == {
        'authority': 'caller_declared',
        'reference': ref(path),
        'context_assessment': 'not_performed',
    }
    if case == 'zero_essential':
        assert (
            restored_query.interaction_sites[1].essential
            and restored_query.interaction_sites[1].weight == 0
        )
        assert after['missing_essential_sites'] == [1]
    if case == 'excluded':
        assert restored_query.interaction_sites[1].feature_name == 'excluded volume'
        assert after['excluded_volume_clashes'] == [{'site_index': 1, 'atom_index': 2}]


def test_known_zero_contact_evidence_keeps_all_target_atoms(source):
    initial = characterize(source)
    zero = bmt.calculate_interface_contacts(
        source,
        participants={'AB': [0, 1], 'C': [2]},
        structure_index=0,
        source_id='authored-four',
        cutoff='0 nm',
    )
    annotated = initial.with_characterizations(
        source, characterizations={'zero': zero}, participant='C'
    )
    assert annotated.characterizations['zero']['record'] == zero.to_dict()
    assert annotated.characterizations['zero']['contributors']['atoms'] == [
        {'source_atom_index': 2, 'local_atom_index': 2, 'witness_indices': []}
    ]


@pytest.mark.parametrize(
    'failure', ['source_id', 'label', 'population', 'frame', 'geometry']
)
def test_incompatible_evidence_is_refused_without_mutation(source, failure):
    initial = characterize(source)
    before = initial.to_dict()
    altered = msm.copy(source)
    options = {}
    if failure == 'source_id':
        options['source_id'] = 'other-source'
    elif failure == 'label':
        options['participants'] = {'AB': [0, 1], 'ligand': [2]}
    elif failure == 'population':
        options['participants'] = {'AB': [0], 'C': [2]}
    elif failure == 'frame':
        altered.interactions = {}
        altered.structures.append(
            coordinates=puw.quantity(
                [[[0, 0, 0], [0.2, 0, 0], [0, 0.25, 0], [0, 0.45, 0]]], 'nm'
            )
        )
        options['structure_index'] = 1
    else:
        altered = msm.structure.translate(
            altered, selection=[2], translation='[0,.01,0] nm', in_place=False
        )
    calculations = evidence(altered, **options)
    with pytest.raises(bmt.exceptions.ArgumentError):
        initial.with_characterizations(
            source, characterizations=calculations, participant='C'
        )
    assert initial.to_dict() == before


def test_changed_current_source_refuses(source):
    initial = characterize(source)
    calculations = evidence(source)
    msm.set(
        source,
        element='atom',
        selection=[2],
        structure_indices=[0],
        coordinates=puw.quantity([[[0, 0.3, 0]]], 'nm'),
    )
    with pytest.raises(bmt.exceptions.ArgumentError):
        initial.with_characterizations(
            source, characterizations=calculations, participant='C'
        )


def test_nonidentity_maps_are_explicitly_unsupported(source):
    initial = characterize(source)
    moved = msm.permute_atoms(source, [3, 2, 1, 0], return_report=True)
    contact = bmt.calculate_interface_contacts(
        moved['molecular_system'],
        participants={'AB': [3, 2], 'C': [1]},
        structure_index=0,
        source_structure_index=0,
        atom_map=moved['report'],
        source_id='authored-four',
        cutoff='.35 nm',
    )
    with pytest.raises(bmt.exceptions.ArgumentError):
        initial.with_characterizations(
            source, characterizations={'mapped': contact}, participant='C'
        )


@pytest.mark.parametrize(
    'options',
    [
        {'characterizations': {}},
        {'participant': 'unknown'},
        {'participant': 'A'},
        {'query_ref': {'uri': 'H.json', 'sha256': 'invalid'}},
    ],
)
def test_invalid_requests_preserve_original(source, options):
    initial = characterize(source)
    before = initial.to_dict()
    with pytest.raises(bmt.exceptions.ArgumentError):
        initial.with_characterizations(
            source,
            **{'characterizations': evidence(source), 'participant': 'C', **options},
        )
    assert initial.to_dict() == before


def test_already_annotated_input_refuses_replacement(source):
    initial = characterize(source)
    calculations = evidence(source)
    annotated = initial.with_characterizations(
        source, characterizations=calculations, participant='C'
    )
    before = annotated.to_dict()
    with pytest.raises(bmt.exceptions.ArgumentError):
        annotated.with_characterizations(
            source, characterizations=calculations, participant='C'
        )
    assert annotated.to_dict() == before


def test_required_radius_failure_preserves_existing_results(source, monkeypatch):
    initial = characterize(source)
    calculations = evidence(source)
    before = initial.to_dict()
    error = MemoryError('owned lookup failure')

    def failed(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm.physchem, 'get_atomic_radius', failed)
    with pytest.raises(MemoryError) as caught:
        initial.with_characterizations(
            source, characterizations=calculations, participant='C'
        )
    assert caught.value is error and initial.to_dict() == before


@pytest.mark.parametrize(
    'change', ['witness', 'record_id', 'context', 'scope', 'query', 'quantity']
)
def test_tampered_annotations_refuse_even_with_recomputed_outer_digest(source, change):
    annotated = characterize(source).with_characterizations(
        source, characterizations=evidence(source), participant='C'
    )
    record = annotated.to_dict()
    annotation = record['extensions'][KEY]
    if change == 'witness':
        annotation['characterizations']['contacts']['contributors']['atoms'][0][
            'witness_indices'
        ] = []
    elif change == 'record_id':
        annotation['characterizations']['contacts']['record_id'] = 'foreign'
    elif change == 'context':
        annotation['source_context_sha256'] = '0' * 64
    elif change == 'scope':
        annotation['scope'] = 'query_importance'
    elif change == 'query':
        annotation['query_semantics'] = 'updated_weights'
    else:
        original = annotation['characterizations']['burial']['record']
        original['analyses']['surface']['calculation']['totals']['total']['values'] = 0
        original['content_sha256'] = _digest(original)
        annotation['characterizations']['burial']['content_sha256'] = original[
            'content_sha256'
        ]
    record['content_sha256'] = _digest(record)
    with pytest.raises((bmt.exceptions.ArgumentError, RecordError)):
        bmt.BindingInterface.from_dict(record, experimental=True)


def test_offline_read_under_unyt_needs_no_molecular_work(source, tmp_path, monkeypatch):
    annotated = characterize(source).with_characterizations(
        source, characterizations=evidence(source), participant='C'
    )
    path = tmp_path / 'I2.json'
    annotated.save(path)

    def forbidden(*args, **kwargs):
        raise AssertionError('Saved core reading requested molecular work')

    for name in ('get', 'select', 'convert', 'get_form'):
        monkeypatch.setattr(msm, name, forbidden)
    with puw.context(default_form='unyt', standard_units=['pm', 'fs']):
        before = deepcopy(puw.configure.report())
        recovered = bmt.BindingInterface.read(path, experimental=True)
        assert recovered.to_dict() == annotated.to_dict()
        assert puw.configure.report() == before


def test_numerically_inconsistent_burial_stays_inspectable_but_refuses_annotation(
    source, monkeypatch
):
    initial = characterize(source)
    original = msm.physchem.get_sasa
    observations = []

    def injected(system, **kwargs):
        quantity = original(system, **kwargs)
        values = np.asarray(puw.get_value(quantity, to_unit='nm**2')).copy()
        if len(observations) == 2:
            values[0, 0] = observations[0][0, 0] + 0.0001
        observations.append(values)
        return puw.quantity(values, 'nm**2')

    monkeypatch.setattr(msm.physchem, 'get_sasa', injected)
    # Deliberately injected software adversity, not measured sampling behavior.
    calculations = evidence(source)
    assert (
        calculations['burial'].surface_calculation['numerical']['burial_usable']
        is False
    )
    with pytest.raises(bmt.exceptions.ArgumentError, match='Inconsistent burial'):
        initial.with_characterizations(
            source, characterizations=calculations, participant='C'
        )
    assert len(initial.interaction_analyses) == 3


def test_changed_geometry_during_required_lookup_refuses(source, monkeypatch):
    initial = characterize(source)
    calculations = evidence(source)
    before = initial.to_dict()
    original = msm.physchem.get_atomic_radius
    changed = []

    def traced(*args, **kwargs):
        quantity = original(*args, **kwargs)
        if not changed:
            changed.append(True)
            msm.set(
                source,
                element='atom',
                selection=[2],
                structure_indices=[0],
                coordinates=puw.quantity([[[0, 0.3, 0]]], 'nm'),
            )
        return quantity

    monkeypatch.setattr(msm.physchem, 'get_atomic_radius', traced)
    with pytest.raises(bmt.exceptions.ArgumentError):
        initial.with_characterizations(
            source, characterizations=calculations, participant='C'
        )
    assert changed and initial.to_dict() == before


def test_changed_group_correspondence_refuses(source):
    initial = characterize(source)
    calculations = evidence(source)
    msm.set(source, element='atom', group_index=[0, 1, 1, 3])
    with pytest.raises(bmt.exceptions.ArgumentError):
        initial.with_characterizations(
            source, characterizations=calculations, participant='C'
        )


def test_directed_native_query_and_explicit_matching_tolerance_stay_unchanged(
    source, tmp_path
):
    phmt = pytest.importorskip('pharmacophoremt')
    from pharmacophoremt.interaction_site import InteractionSite
    from pharmacophoremt.interaction_site.shape import SphereAndVector
    from pharmacophoremt.screening import PoseEvaluator

    initial = characterize(source)
    query = model(source, initial)
    # Authored optional query constraint, not an ionic detector observation.
    query.add_interaction_site(
        InteractionSite(
            SphereAndVector('[0,.25,0] nm', '.02 nm', [1, 0, 0]),
            'hb donor',
            essential=False,
            weight=0,
        )
    )
    evaluator = PoseEvaluator(query, direction_tolerance='12 degrees')
    before = evaluator.evaluate(source, selection=[2])
    assert before['status'] == 'matched' and before['fit_value'] == pytest.approx(1)
    path = tmp_path / 'directed.json'
    phmt.io.to_json(query, str(path))
    original = path.read_bytes()
    initial.with_characterizations(
        source, characterizations=evidence(source), participant='C', query_ref=ref(path)
    )
    recovered = phmt.io.load_json(str(path))
    assert path.read_bytes() == original
    directed = recovered.interaction_sites[1]
    assert (
        directed.shape_name == 'sphere and vector'
        and not directed.essential
        and directed.weight == 0
    )
    np.testing.assert_array_equal(
        puw.get_value(directed.direction, to_unit='dimensionless'), [1, 0, 0]
    )
    after_evaluator = PoseEvaluator(recovered, direction_tolerance='12 degrees')
    assert (
        evaluator.direction_tolerance
        == after_evaluator.direction_tolerance
        == pytest.approx(12)
    )
    after = after_evaluator.evaluate(source, selection=[2])
    assert (
        after['status'] == before['status']
        and after['fit_value'] == before['fit_value']
    )
