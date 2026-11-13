"""Actual native ionic grouping/construction and frozen H0/H1 receiving."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from pyunitwizard.record import QuantityRecord, RecordError
from unyt.exceptions import UnitParseError

import bindingmt as bmt
from bindingmt._private.interface_ionic import quantity_values
from bindingmt._private.interface_records import _digest

INPUTS = Path(__file__).parent / 'data/interface_native_handoff/cb6af716'
NAMES = ['ionic_031', 'ionic_035', 'ionic_empty']


@pytest.fixture
def source():
    manifest = json.loads((INPUTS / 'manifest.json').read_text())
    for name, row in manifest['artifacts'].items():
        assert hashlib.sha256((INPUTS / name).read_bytes()).hexdigest() == row['sha256']
    return msm.h5msm.read(str(INPUTS / 'source.h5msm'))


def characterize(source, **options):
    return bmt.characterize_interface_interactions(
        source,
        **{
            'participants': {'A': [0], 'B': [1], 'C': [2]},
            'grouping': [['A', 'B'], ['C']],
            'analysis_names': NAMES,
            'structure_index': 0,
            'source_id': 'authored-four',
            **options,
        },
    )


def build(interface, source, **options):
    pytest.importorskip('pharmacophoremt')
    return bmt.build_interface_pharmacophore(
        interface,
        source,
        **{
            'participant': 'C',
            'radius': '0.02 nm',
            'duplicate_policy': 'same_participant',
            **options,
        },
    )


def rows(native):
    data = native.to_dict()
    return [
        (
            int(r),
            int(o),
            sorted(
                int(a)
                for p in native.relation(int(r))['participants']
                for a in p['atom_indices']
            ),
        )
        for r, o in zip(data['relation_indices'], data['occurrence_indices'])
    ]


def test_real_native_detection_then_binding_scope_without_an_external_provider(
    source, monkeypatch
):
    calls = []
    for threshold in ('0.31 nm', '0.35 nm'):
        detected = msm.interactions.ionic.get_ionic_interactions(
            source,
            threshold,
            selection='all',
            structure_indices=[0],
            selection_mode='internal',
            pbc=False,
        )
        assert [r[2] for r in rows(detected)] == [[0, 1], [0, 2], [2, 3]]
        source.interactions = {**source.interactions, 'fresh_' + threshold: detected}
    original = msm.Interactions.between_selections

    def traced(self, *args, **kwargs):
        calls.append((args, deepcopy(kwargs)))
        return original(self, *args, **kwargs)

    monkeypatch.setattr(msm.Interactions, 'between_selections', traced)
    interface = characterize(source, analysis_names=['fresh_0.31 nm', 'fresh_0.35 nm'])
    assert len(calls) == 2
    assert all(
        args == ([0, 1], [2]) and opts == {'structure_indices': [0], 'exclusive': True}
        for args, opts in calls
    )
    for view in interface.interaction_analyses.values():
        assert view['original_count'] == 3
        assert [
            (r['relation_index'], r['occurrence_index']) for r in view['observations']
        ] == [(1, 1)]
        assert sorted(
            a
            for p in view['observations'][0]['participants']
            for a in p['atom_indices']
        ) == [0, 2]
        np.testing.assert_array_equal(
            quantity_values(view['measurements']['distance'], 'distance'), [0.25]
        )
    assert rows(source.interactions['ionic_031']) == [
        (0, 0, [0, 1]),
        (1, 1, [0, 2]),
        (2, 2, [2, 3]),
    ]


def test_frozen_positive_empty_and_native_carrier_roundtrip(source, tmp_path):
    interface = characterize(source)
    assert interface.to_dict()['format_version'] == '0.5'
    assert interface.summary()['native_interactions']['ionic_empty'] == {
        'occurrence_count': 0,
        'original_count': 0,
        'evaluated_structure_indices': [0],
        'definition': 'bindingmt.native_ionic_scope@1',
    }
    assert interface.summary()['analyses']['ionic_empty']['finding_count'] == 0
    interface.save(tmp_path / 'I0.json')
    assert (
        bmt.BindingInterface.read(tmp_path / 'I0.json', experimental=True).to_dict()
        == interface.to_dict()
    )
    msm.h5msm.write(source, str(tmp_path / 'source.h5msm'), format_version='1.0')
    recovered = msm.h5msm.read(str(tmp_path / 'source.h5msm'))
    assert (
        characterize(recovered).interaction_analyses == interface.interaction_analyses
    )
    assert interface.copy().to_dict() == interface.to_dict()
    assert (
        interface.revise(
            question={'kind': 'association', 'description': 'new question'},
            reason='test',
        ).interaction_analyses
        == interface.interaction_analyses
    )


def test_actual_pharmacophore_construction_association_and_native_persistence(
    source, tmp_path
):
    phmt = pytest.importorskip('pharmacophoremt')
    interface = characterize(source)
    before = deepcopy(interface.to_dict())
    model = build(interface, source)
    assert model.n_interaction_sites == 1
    site = model.interaction_sites[0]
    assert (
        site.feature_name == 'positive charge' and site.essential and site.weight == 1
    )
    np.testing.assert_allclose(
        puw.get_value(site.center, to_unit='nm'), [0, 0.25, 0], rtol=0, atol=1e-14
    )
    assert len(site.metadata['composition_contributions']) == 2
    assert {
        (r['component'], r['relation_index'], r['occurrence_index'])
        for r in site.metadata['observations']
    } == {('ionic_031', 1, 1), ('ionic_035', 1, 1)}
    assert model.metadata['components'][-1]['n_sites'] == 0
    assert model.metadata['policy']['weight_aggregation'] == 'not_performed'
    path = tmp_path / 'H0.json'
    phmt.io.to_json(model, str(path))
    ref = {'uri': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    recovered = phmt.io.load_json(str(path))
    linked = interface.with_pharmacophore(
        hypothesis=recovered, hypothesis_ref=ref, participant='C'
    )
    assert interface.to_dict() == before
    assert linked.to_dict()['derivation']['parents'] == [interface.record_id]
    link = linked.to_dict()['site_refs'][0]
    assert link['reference'] == ref and len(link['sites'][0]['contributors']) == 2
    assert link['sites'][0]['weight'] == 1
    linked.save(tmp_path / 'I1.json')
    assert (
        bmt.BindingInterface.read(tmp_path / 'I1.json', experimental=True).to_dict()
        == linked.to_dict()
    )


def test_alternative_and_constraint_decisions_use_public_binding_construction(source):
    phmt = pytest.importorskip('pharmacophoremt')
    from pharmacophoremt.screening import PoseEvaluator

    alt = msm.h5msm.read(str(INPUTS / 'alternative.h5msm'))
    primary = build(characterize(source), source)
    alternative = build(characterize(alt), alt)
    keep = build(characterize(source), source, duplicate_policy='keep')
    models = {
        'zero': phmt.io.load_json(str(INPUTS / 'zero_essential.json')),
        'excluded': phmt.io.load_json(str(INPUTS / 'excluded.json')),
    }
    cases = [
        (primary, source, 'matched', 1),
        (primary, alt, 'not_matched', 0),
        (alternative, alt, 'matched', 1),
        (alternative, source, 'not_matched', 0),
        (models['zero'], source, 'not_matched', 1),
        (models['excluded'], source, 'not_matched', 1),
        (keep, source, 'not_matched', 0.5),
    ]
    for model, target, status, fit in cases:
        result = PoseEvaluator(model).evaluate(target, selection=[2])
        assert result['status'] == status and result['fit_value'] == pytest.approx(fit)


@pytest.mark.parametrize(
    'options',
    [
        {'analysis_names': []},
        {'analysis_names': ['missing']},
        {'analysis_names': ['ionic_031', 'ionic_031']},
        {'participants': {'A': [0], 'B': [0]}},
        {'grouping': [['A'], ['B']]},
        {'structure_index': 1},
        {'source_id': ''},
        {'max_source_atoms': 3},
        {'max_native_occurrences': 5},
    ],
)
def test_invalid_requests_refuse(source, options):
    with pytest.raises(bmt.exceptions.ArgumentError):
        characterize(source, **options)


@pytest.mark.parametrize(
    'failure', ['state', 'maps', 'coverage', 'profile', 'source_id']
)
def test_incompatible_native_observations_refuse(source, failure):
    observed = source.interactions['ionic_035']
    if failure == 'coverage':
        changed = observed.invalidate_structures([0])
    else:
        data = msm.convert(observed, to_form='molsysmt.InteractionsDict')
        if failure == 'state':
            data.data['parameters']['chemical_state_index'] = 1
        elif failure == 'source_id':
            data.data['source_id'] = 'contradictory-source'
        elif failure == 'maps':
            data.data['atom_source_indices'] = np.array([3, 2, 1, 0])
        else:
            data.data['parameters']['method_definition'] = 'unknown@1'
        changed = msm.convert(data, to_form='molsysmt.Interactions')
    source.interactions = {**source.interactions, 'ionic_035': changed}
    with pytest.raises(bmt.exceptions.ArgumentError):
        characterize(source)


def test_cut_compound_charge_participant_refuses_in_owner_tool():
    system = msm.convert(
        msm.convert('smiles:CC(=O)[O-].[Na+]', to_form='rdkit.Mol'),
        to_form='molsysmt.MolSys',
    )
    system.structures.append(
        coordinates=puw.quantity(
            [[[0, -0.15, 0], [0, 0, 0], [-0.1, 0.1, 0], [0.1, 0.1, 0], [0.1, 0.4, 0]]],
            'nm',
        )
    )
    system.interactions = {
        'ionic': msm.interactions.ionic.get_ionic_interactions(
            system,
            '.31 nm',
            selection=[0, 1, 2, 3],
            selection_2=[4],
            selection_mode='between',
            structure_indices=[0],
            pbc=False,
        )
    }
    with pytest.raises(Exception, match='cuts a compound charge center'):
        characterize(
            system,
            participants={'negative': [2, 3], 'positive': [4]},
            grouping=[['negative'], ['positive']],
            analysis_names=['ionic'],
        )


def test_required_child_failure_preserves_original(source, monkeypatch):
    interface = characterize(source)
    snapshot = interface.to_dict()
    error = MemoryError('owned query failure')

    def failed(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm.Interactions, 'between_selections', failed)
    with pytest.raises(MemoryError) as caught:
        characterize(source)
    assert caught.value is error and interface.to_dict() == snapshot


def test_changed_required_context_refuses_current_use(source):
    interface = characterize(source)
    msm.set(
        source,
        element='atom',
        selection=[2],
        structure_indices=[0],
        coordinates=puw.quantity([[[0, 0.3, 0]]], 'nm'),
    )
    with pytest.raises(bmt.exceptions.ArgumentError):
        build(interface, source)


def test_explicit_empty_hypothesis_retains_coverage(source, tmp_path):
    phmt = pytest.importorskip('pharmacophoremt')
    from pharmacophoremt.screening import PoseEvaluator

    interface = characterize(source, analysis_names=['ionic_empty'])
    model = build(interface, source)
    assert model.n_interaction_sites == 0
    with pytest.raises(Exception, match='positive total weight'):
        PoseEvaluator(model)
    path = tmp_path / 'empty.json'
    phmt.io.to_json(model, str(path))
    linked = interface.with_pharmacophore(
        hypothesis=model,
        hypothesis_ref={
            'uri': path.name,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        },
        participant='C',
    )
    assert linked.to_dict()['site_refs'][0]['sites'] == []


@pytest.mark.parametrize('change', ['center', 'flag', 'radius', 'contributor'])
def test_edited_hypothesis_is_not_linked_as_original_construction(source, change):
    interface = characterize(source)
    model = build(interface, source)
    site = model.interaction_sites[0]
    if change == 'center':
        site.shape.center = puw.quantity([1, 1, 1], 'nm')
    elif change == 'flag':
        site.essential = False
    elif change == 'radius':
        site.shape.radius = puw.quantity(0.03, 'nm')
    else:
        site.metadata['observations'].pop()
    with pytest.raises(bmt.exceptions.ArgumentError):
        interface.with_pharmacophore(
            hypothesis=model,
            hypothesis_ref={'uri': 'H.json', 'sha256': '0' * 64},
            participant='C',
        )


@pytest.mark.xfail(
    strict=True,
    raises=UnitParseError,
    reason='PyUnitWizard #156: elementary-charge Pint/unyt conversion blocks native recognition',
)
def test_nondefault_unit_form_preserves_policy_and_known_quantity_fields(
    source, tmp_path
):
    with puw.context(default_form='unyt', standard_units=['pm', 'fs']):
        before = deepcopy(puw.configure.report())
        interface = characterize(source)
        model = build(interface, source, radius=puw.quantity(20, 'pm'))
        assert model.interaction_sites[0].weight == 1
        interface.save(tmp_path / 'I0.json')
        assert (
            bmt.BindingInterface.read(
                tmp_path / 'I0.json', experimental=True
            ).interaction_analyses
            == interface.interaction_analyses
        )
        assert puw.configure.report() == before


@pytest.mark.parametrize(
    'change', ['unit', 'field', 'occurrence', 'group', 'scope', 'authority']
)
def test_semantic_tampering_refuses_even_with_new_outer_digest(source, change):
    record = characterize(source).to_dict()
    a = record['analyses']['ionic_031']
    view = a['native_observation']
    if change == 'unit':
        view['measurements']['distance'] = QuantityRecord.from_quantity(
            puw.quantity([1], 'ps'), field='bindingmt.ionic.distance'
        ).to_dict()
    elif change == 'field':
        view['threshold'] = QuantityRecord.from_quantity(
            puw.quantity(0.31, 'nm'), field='foreign.cutoff'
        ).to_dict()
    elif change == 'occurrence':
        view['observations'][0]['occurrence_index'] = 0
    elif change == 'group':
        view['context']['grouping'] = [['A'], ['B', 'C']]
    elif change == 'scope':
        view['observations'][0]['participants'][0]['atom_indices'] = [3]
    else:
        a['authority'] = 'caller_declared'
    record['content_sha256'] = _digest(record)
    with pytest.raises((bmt.exceptions.ArgumentError, RecordError)):
        bmt.BindingInterface.from_dict(record, experimental=True)


def test_saved_core_can_be_read_under_unyt_without_native_recognition(
    source, tmp_path, monkeypatch
):
    interface = characterize(source)
    path = tmp_path / 'I0.json'
    interface.save(path)

    def forbidden(*args, **kwargs):
        raise AssertionError('Core read must not request native recognition')

    monkeypatch.setattr(msm.physchem, 'get_charge_centers', forbidden)
    with puw.context(default_form='unyt', standard_units=['pm', 'fs']):
        before = deepcopy(puw.configure.report())
        restored = bmt.BindingInterface.read(path, experimental=True)
        assert restored.to_dict() == interface.to_dict()
        assert (
            restored.summary()['native_interactions']['ionic_031']['occurrence_count']
            == 1
        )
        assert puw.configure.report() == before
