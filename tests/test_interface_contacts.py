"""Independent Cartesian controls through real public MolSysMT operations."""

import builtins
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt.native import MolSys, Structures
from pyunitwizard.record import QuantityRecord, RecordError

import bindingmt as bmt
from bindingmt._private.interface_contacts import DISTANCES_FIELD
from bindingmt._private.interface_records import _digest


@pytest.fixture
def source():
    system = MolSys(n_atoms=32, n_groups=2)
    groups = [0] * 32
    groups[30] = groups[10] = 1
    msm.set(system, element='atom', group_index=groups, atom_type=['C'] * 32)
    coordinates = np.zeros((3, 32, 3))
    coordinates[:, :, 0] = 100
    coordinates[:, [8, 2, 30, 10], 0] = [0, 3, 3.5, 1]
    system.structures = Structures(coordinates=puw.quantity(coordinates, 'nm'))
    return system


def calculate(source, **options):
    return bmt.calculate_interface_contacts(
        source,
        **{
            'participants': {'A': [8, 2], 'B': [30, 10]},
            'cutoff': '1 nm',
            'structure_index': 2,
            'source_id': 'authored-32',
            **options,
        },
    )


def test_exact_contacts_distances_groups_and_actual_owner_calls(source, monkeypatch):
    calls = []
    for name in ('get_contacts', 'get_distances'):
        original = getattr(msm.structure, name)

        def traced(*args, _name=name, _original=original, **kwargs):
            calls.append((_name, deepcopy(kwargs)))
            return _original(*args, **kwargs)

        monkeypatch.setattr(msm.structure, name, traced)
    result = calculate(source)
    calculation = result.contact_calculation
    assert calculation['local_pairs'] == [[8, 10], [2, 30]]
    assert calculation['source_pairs'] == [[8, 10], [2, 30]]
    distances = QuantityRecord.from_dict(calculation['distances']).to_quantity(
        field=DISTANCES_FIELD, unit='nm', dimensionality={'[L]': 1}
    )
    np.testing.assert_allclose(
        puw.get_value(distances, to_unit='nm'), [1, 0.5], rtol=0, atol=0
    )
    assert calculation['group_pairs'] == [[0, 1]]
    assert calculation['group_contributors'] == [[0, 1]]
    assert [name for name, _ in calls] == ['get_contacts', 'get_distances']
    for _, options in calls:
        assert options['selection'] == [8, 2] and options['selection_2'] == [30, 10]
        assert options['structure_indices'] == [2]
        assert (
            options['pairs']
            is options['pbc']
            is options['use_gpu']
            is options['parallel']
            is False
        )
        assert options['num_threads'] == 1
    assert result.summary()['native_contacts']['atomic_pair_count'] == 2
    assert result.summary()['native_contacts']['criterion'] == 'distance <= 1.0 nm'
    assert result.project_footprint(participant='A').source_atom_indices == [2, 8]
    assert result.project_footprint(participant='B').source_atom_indices == [10, 30]


def test_boundary_preceding_cutoff_and_exchange(source):
    result = calculate(source, cutoff=puw.quantity(np.nextafter(1.0, 0.0), 'nm'))
    assert result.contact_calculation['source_pairs'] == [[2, 30]]
    forward = calculate(source)
    reverse = calculate(source, participants={'B': [30, 10], 'A': [8, 2]})
    assert {tuple(p[::-1]) for p in reverse.contact_calculation['source_pairs']} == {
        tuple(p) for p in forward.contact_calculation['source_pairs']
    }
    for name in ('A', 'B'):
        assert (
            forward.project_footprint(participant=name).source_atom_indices
            == reverse.project_footprint(participant=name).source_atom_indices
        )


def test_completed_zero_and_independent_empty_footprint(source, tmp_path):
    result = calculate(source, cutoff='0 nm')
    assert result.contact_calculation['local_pairs'] == []
    assert result.summary()['analyses']['contacts']['original_outcome'] == 'completed'
    assert result.summary()['analyses']['contacts']['finding_count'] == 0
    footprint = result.project_footprint(participant='A')
    assert footprint.source_atom_indices == []
    assert footprint.summary()['value_state'] == 'evaluated_empty'
    footprint.save(tmp_path / 'empty.json')
    assert (
        bmt.ContactFootprint.read(tmp_path / 'empty.json', experimental=True).to_dict()
        == footprint.to_dict()
    )


def test_owner_extraction_permutation_and_source_structure_map(source):
    selected = [2, 8, 10, 30]
    reduced = msm.extract(source, selection=[8, 2, 30, 10], structure_indices=[2])
    permuted = msm.permute_atoms(reduced, [1, 0, 3, 2], return_report=True)
    extraction = {
        'schema': 'molsysmt.atom_map@1',
        'n_source_atoms': 32,
        'n_output_atoms': 4,
        'source_to_output_atom_indices': [
            selected.index(i) if i in selected else -1 for i in range(32)
        ],
        'output_to_source_atom_indices': selected,
    }
    composed = msm.compose_atom_maps([extraction, permuted['report']])
    result = calculate(
        permuted['molecular_system'],
        participants={'A': [0, 1], 'B': [2, 3]},
        structure_index=0,
        atom_map=composed,
        source_structure_index=2,
    )
    a = result.project_footprint(participant='A')
    b = result.project_footprint(participant='B')
    assert a.source_atom_indices == [2, 8] and a.local_atom_indices == [1, 0]
    assert b.source_atom_indices == [10, 30] and b.local_atom_indices == [3, 2]
    assert a.summary()['context']['structure_index'] == 0
    assert a.summary()['context']['source_structure_index'] == 2
    assert a.to_dict()['calculation']['participants']['A']['group_indices'] == [0, 0]


@pytest.mark.parametrize(
    'options',
    [
        {'participants': {'A': [], 'B': [30]}},
        {'participants': {'A': [8, 8], 'B': [30]}},
        {'participants': {'A': [8], 'B': [8]}},
        {'participants': {'A': [8]}},
        {'cutoff': -1},
        {'cutoff': '-1 nm'},
        {'cutoff': '1 ps'},
        {'cutoff': 'nan nm'},
        {'cutoff': '[1, 2] nm'},
        {'structure_index': True},
        {'structure_index': 3},
        {'max_dense_pairs': 3},
        {'source_id': ''},
    ],
)
def test_invalid_or_over_budget_requests_refuse_before_numerical_calls(
    source, monkeypatch, options
):
    def forbidden(*args, **kwargs):
        pytest.fail('Invalid request reached numerical contact/distance execution')

    monkeypatch.setattr(msm.structure, 'get_contacts', forbidden)
    monkeypatch.setattr(msm.structure, 'get_distances', forbidden)
    with pytest.raises(bmt.exceptions.ArgumentError):
        calculate(source, **options)


def test_failed_required_child_is_not_completed_zero(source, monkeypatch):
    error = MemoryError('owned allocation failure')

    def failed(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm.structure, 'get_distances', failed)
    with pytest.raises(MemoryError) as caught:
        calculate(source)
    assert caught.value is error


def test_quantity_policy_and_typed_persistence(source, tmp_path):
    with puw.context(default_form='unyt', standard_units=['pm', 'fs']):
        before = deepcopy(puw.configure.get_standard_units())
        result = calculate(source, cutoff=puw.quantity(1000, 'pm'))
        result.save(tmp_path / 'result.json')
        restored = bmt.BindingInterface.read(
            tmp_path / 'result.json', experimental=True
        )
        assert restored.to_dict() == result.to_dict()
        assert restored.summary()['native_contacts']['atomic_pair_count'] == 2
        for name in ('A', 'B'):
            footprint = restored.project_footprint(participant=name)
            footprint.save(tmp_path / f'{name}.json')
            assert (
                bmt.ContactFootprint.read(
                    tmp_path / f'{name}.json', experimental=True
                ).to_dict()
                == footprint.to_dict()
            )
        assert puw.configure.get_standard_units() == before


def test_saved_readback_needs_no_molecular_or_optional_provider_work(
    source, tmp_path, monkeypatch
):
    result = calculate(source)
    footprint = result.project_footprint(participant='A')
    result.save(tmp_path / 'result.json')
    footprint.save(tmp_path / 'footprint.json')
    original_import = builtins.__import__

    def no_provider(name, *args, **kwargs):
        assert name.split('.')[0] not in {'topomt', 'pharmacophoremt', 'vina'}
        return original_import(name, *args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail('Saved evidence required molecular execution or discovery')

    monkeypatch.setattr(builtins, '__import__', no_provider)
    for name in ('get', 'select', 'get_form', 'convert', 'compose_atom_maps'):
        monkeypatch.setattr(msm, name, forbidden)
    for name in ('get_contacts', 'get_distances'):
        monkeypatch.setattr(msm.structure, name, forbidden)
    assert (
        bmt.BindingInterface.read(tmp_path / 'result.json', experimental=True)
        .copy()
        .to_dict()
        == result.to_dict()
    )
    assert (
        bmt.ContactFootprint.read(tmp_path / 'footprint.json', experimental=True)
        .copy()
        .to_dict()
        == footprint.to_dict()
    )


def test_resealed_wrong_quantity_field_and_bad_footprint_refuse(source):
    record = calculate(source).to_dict()
    record['analyses']['contacts']['calculation']['cutoff'] = record['analyses'][
        'contacts'
    ]['calculation']['distances']
    record['content_sha256'] = _digest(record)
    with pytest.raises(RecordError):
        bmt.BindingInterface.from_dict(record, experimental=True)
    footprint = calculate(source).project_footprint(participant='A').to_dict()
    footprint['footprint']['local_atom_indices'].reverse()
    footprint['content_sha256'] = _digest(footprint)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.ContactFootprint.from_dict(footprint, experimental=True)


def test_missing_group_correspondence_does_not_fabricate_zero():
    source = MolSys(n_atoms=4)
    source.structures = Structures(
        coordinates=puw.quantity([[[0, 0, 0], [3, 0, 0], [3.5, 0, 0], [1, 0, 0]]], 'nm')
    )
    result = calculate(
        source, participants={'A': [0, 1], 'B': [2, 3]}, structure_index=0
    )
    assert result.summary()['native_contacts']['atomic_pair_count'] == 2
    assert result.summary()['native_contacts']['group_pair_count'] is None
    assert result.summary()['native_contacts']['group_coverage'] == 'partial'


def test_geometry_change_during_calls_refuses_and_keeps_old_result(source, monkeypatch):
    previous = calculate(source)
    before = previous.to_dict()
    original = msm.structure.get_distances

    def changed(*args, **kwargs):
        value = original(*args, **kwargs)
        msm.set(
            source,
            element='atom',
            selection=[8],
            structure_indices=[2],
            coordinates=puw.quantity([[[10, 0, 0]]], 'nm'),
        )
        return value

    monkeypatch.setattr(msm.structure, 'get_distances', changed)
    with pytest.raises(bmt.exceptions.ArgumentError):
        calculate(source)
    assert previous.to_dict() == before


def test_native_reinterpretation_keeps_original_calculation(source):
    result = calculate(source)
    revised = result.revise(
        question={'kind': 'association', 'description': 'reviewed interpretation'},
        reason='review',
    )
    assert revised.contact_calculation == result.contact_calculation
    assert revised.analyses == result.analyses
    assert revised.record_id != result.record_id
    assert (
        revised.project_footprint(participant='A').summary()['parent_record_id']
        == revised.record_id
    )


@pytest.mark.parametrize('physical_error', ['field', 'dimension', 'outside_bound'])
def test_resealed_quantity_semantics_are_checked(source, physical_error):
    record = calculate(source).to_dict()
    calculation = record['analyses']['contacts']['calculation']
    if physical_error == 'field':
        quantity = QuantityRecord.from_quantity(
            puw.quantity([1, 0.5], 'nm'), field='unrelated.field'
        )
    elif physical_error == 'dimension':
        quantity = QuantityRecord.from_quantity(
            puw.quantity([1, 0.5], 'ps'), field=DISTANCES_FIELD
        )
    else:
        quantity = QuantityRecord.from_quantity(
            puw.quantity([2, 0.5], 'nm'), field=DISTANCES_FIELD
        )
    calculation['distances'] = quantity.to_dict()
    record['content_sha256'] = _digest(record)
    with pytest.raises((RecordError, bmt.exceptions.ArgumentError)):
        bmt.BindingInterface.from_dict(record, experimental=True)


def test_multiple_native_analyses_and_self_parent_refuse(source):
    result = calculate(source)
    record = result.to_dict()
    record['analyses']['second'] = deepcopy(record['analyses']['contacts'])
    record['content_sha256'] = _digest(record)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.from_dict(record, experimental=True)
    footprint = result.project_footprint(participant='A').to_dict()
    footprint['parent_record_id'] = footprint['record_id']
    footprint['content_sha256'] = _digest(footprint)
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.ContactFootprint.from_dict(footprint, experimental=True)


def test_owner_group_axis_stays_aligned_with_reordered_atomic_endpoints():
    source = MolSys(n_atoms=4, n_groups=4)
    msm.set(source, element='atom', group_index=[0, 1, 2, 3])
    source.structures = Structures(
        coordinates=puw.quantity([[[0, 0, 0], [3, 0, 0], [3.5, 0, 0], [1, 0, 0]]], 'nm')
    )
    result = calculate(
        source, participants={'A': [1, 0], 'B': [3, 2]}, structure_index=0
    )
    assert result.contact_calculation['local_pairs'] == [[1, 2], [0, 3]]
    assert result.contact_calculation['participants']['A']['group_indices'] == [1, 0]
    assert result.contact_calculation['participants']['B']['group_indices'] == [3, 2]
    assert result.contact_calculation['group_pairs'] == [[1, 2], [0, 3]]
    assert result.contact_calculation['group_contributors'] == [[0], [1]]
