"""Consumer-boundary controls using synthetic provider doubles, not molecular data."""

import sys
from copy import deepcopy
from types import SimpleNamespace

import numpy as np
import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError
from bindingmt.core.results import _molecular_atom_keys


class _Analysis:
    def __init__(self, evaluated):
        self.evaluated_structure_indices = np.asarray(evaluated, dtype=int)
        self.parameters = {'profile': 'synthetic-protocol-control'}
        self.software = {'producer': 'synthetic-test-double'}

    def copy(self):
        return deepcopy(self)


def _key(atom_id, element):
    return {
        'atom_id': atom_id,
        'atom_name': atom_id,
        'element': element,
        'group_id': '1',
        'group_name': 'CONTROL',
    }


@pytest.fixture
def case(monkeypatch):
    expected = [_key('A', 'C'), _key('B', 'N')]
    pose = bmt.DockingPose(
        puw.quantity([[1, 2, 3], [4, 5, 6]], 'angstrom'),
        scores={'original': -4},
        rank=7,
        pose_id='selected',
        partner_state_id='partner-state',
        receptor_state_id='receptor-state',
        metadata={
            'pose_atom_order': 'verified_pdbqt_order',
            'source_atom_keys': deepcopy(expected),
        },
    )
    other = bmt.DockingPose(
        pose.coordinates + puw.quantity([10, 0, 0], 'angstrom'),
        scores={'original': -5},
        rank=1,
        pose_id='other',
        partner_state_id=pose.partner_state_id,
        receptor_state_id=pose.receptor_state_id,
        metadata=deepcopy(pose.metadata),
    )
    result = bmt.DockingResult(
        [other, pose],
        provenance={'producer': 'synthetic-original', 'details': {'seed': 3}},
    )
    carrier = SimpleNamespace(
        keys=[_key('R', 'O'), expected[1], _key('H', 'H'), expected[0]],
        coordinates=puw.quantity(
            [[[9, 9, 9], [4, 5, 6], [7, 7, 7], [1, 2, 3]]], 'angstrom'
        ),
        n_structures=1,
        interactions={
            'stored': _Analysis([0]),
            'evaluated_empty': _Analysis([0]),
            'unevaluated': _Analysis([]),
        },
        metadata={'original': ['unchanged']},
    )
    calls = []

    def convert(value, *, to_form):
        calls.append('convert')
        assert to_form == 'molsysmt.MolSys'
        return value

    def copy(value):
        calls.append('copy')
        return deepcopy(value)

    def get(value, *, element, **options):
        calls.append('get')
        requested = [name for name, enabled in options.items() if enabled is True]
        assert len(requested) == 1
        name = requested[0]
        if name == 'n_atoms':
            return len(value.keys)
        if name == 'n_structures':
            return value.n_structures
        if name == 'coordinates':
            return deepcopy(value.coordinates)
        field = {'name': 'atom_name', 'atom_type': 'element'}.get(name, name)
        return [row[field] for row in value.keys]

    provider = SimpleNamespace(
        convert=convert,
        copy=copy,
        get=get,
        has_attribute=lambda value, name: True,
    )
    monkeypatch.setitem(sys.modules, 'molsysmt', provider)
    options = {
        'pose_index': 1,
        'pose_atom_indices': [3, 1],
        'partner_state_id': pose.partner_state_id,
        'receptor_state_id': pose.receptor_state_id,
        'assume_aligned': True,
    }
    return SimpleNamespace(
        result=result, carrier=carrier, calls=calls, options=options, provider=provider
    )


def _bind(case, **overrides):
    return bmt.bind_interactions(
        case.result, case.carrier, **{**case.options, **overrides}
    )


@pytest.mark.parametrize('factory', [bmt.bind_interactions, bmt.PoseInteractions])
@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_full_result_identity_units_and_evaluation_are_preserved(
    case, factory, length_unit
):
    before = case.result.to_dict()
    with puw.context(standard_units=[length_unit, 'fs', 'kJ/mol']):
        policy = puw.configure.get_standard_units()
        binding = factory(
            case.result,
            case.carrier,
            **{
                **case.options,
                'pose_atom_indices': (np.int64(index) for index in [3, 1]),
                'coordinate_tolerance': puw.quantity(1e-10, 'pm'),
            },
        )
        assert puw.configure.get_standard_units() == policy
        assert binding.pose_index == 1 and binding.pose.pose_id == 'selected'
        assert binding.pose.rank == 7
        assert [pose.pose_id for pose in binding.result] == ['other', 'selected']
        assert binding.result.provenance == before['provenance']
        assert [pose.scores for pose in binding.result] == [
            pose['scores'] for pose in before['poses']
        ]
        association = binding.association
        assert association['pose_atom_indices'] == [3, 1]
        assert association['original_pose_count'] == 2
        assert association['coordinate_tolerance']['unit'] == 'angstrom'
        assert association['coordinate_tolerance']['value'] == pytest.approx(1e-12)
        assert association['analysis_evaluated'] == {
            'stored': True,
            'evaluated_empty': True,
            'unevaluated': False,
        }
        assert association['chemical_equivalence_validated'] is False
        assert association['analysis_producer_authenticated'] is False
    assert case.result.to_dict() == before
    assert case.carrier.metadata == {'original': ['unchanged']}
    assert binding.analysis_names == ('stored', 'evaluated_empty', 'unevaluated')


def test_accessors_and_source_edits_do_not_rewrite_the_binding(case):
    binding = _bind(case)
    case.result[1].scores['original'] = 999
    case.result.provenance['details']['seed'] = 99
    case.carrier.metadata['original'].append('source edit')
    case.carrier.interactions['stored'].parameters['profile'] = 'source edit'
    restored = binding.result
    restored[1].scores['original'] = 123
    restored.provenance['details']['seed'] = 123
    association = binding.association
    association['pose_atom_indices'][0] = 999
    analysis = binding.get_analysis('stored')
    analysis.parameters['profile'] = 'returned edit'
    copy = binding.to_molecular_system()
    copy.metadata['original'].append('returned edit')
    assert binding.pose.scores == {'original': -4}
    assert binding.result.provenance['details']['seed'] == 3
    assert binding.association['pose_atom_indices'] == [3, 1]
    assert binding.get_analysis('stored').parameters['profile'] == (
        'synthetic-protocol-control'
    )
    assert binding.to_molecular_system().metadata == {'original': ['unchanged']}


@pytest.mark.parametrize(
    'overrides',
    [
        {'pose_index': -1},
        {'pose_index': True},
        {'pose_index': 1.0},
        {'pose_index': 2},
        {'pose_atom_indices': None},
        {'pose_atom_indices': []},
        {'pose_atom_indices': {1, 3}},
        {'pose_atom_indices': [3, 3]},
        {'pose_atom_indices': [3, False]},
        {'pose_atom_indices': [3, -1]},
        {'pose_atom_indices': [3, 1.0]},
        {'pose_atom_indices': [3]},
        {'partner_state_id': None},
        {'partner_state_id': 'different'},
        {'receptor_state_id': None},
        {'receptor_state_id': 'different'},
        {'assume_aligned': False},
        {'assume_aligned': 'yes'},
    ],
)
def test_invalid_declarations_fail_before_provider_work(case, overrides):
    before = case.result.to_dict()
    with pytest.raises(ArgumentError) as caught:
        _bind(case, **overrides)
    assert caught.value.code == 'BMT-E002'
    assert case.calls == []
    assert case.result.to_dict() == before


@pytest.mark.parametrize(
    'tolerance',
    [
        1.0,
        '1 ps',
        puw.quantity(-1, 'angstrom'),
        puw.quantity(float('inf'), 'angstrom'),
        puw.quantity(float('nan'), 'angstrom'),
        puw.quantity([1, 2], 'angstrom'),
        puw.quantity(np.asarray(True), 'angstrom'),
        puw.quantity(1j, 'angstrom'),
    ],
)
def test_invalid_tolerance_is_rejected_before_provider_work(case, tolerance):
    with pytest.raises(ArgumentError) as caught:
        _bind(case, coordinate_tolerance=tolerance)
    assert caught.value.extra['arg_name'] == 'coordinate_tolerance'
    assert case.calls == []


def test_unknown_pose_atom_map_is_rejected_before_provider_work(case):
    case.result[1].metadata.pop('pose_atom_order')
    with pytest.raises(ArgumentError):
        _bind(case)
    assert case.calls == []


@pytest.mark.parametrize('n_structures', [0, 2])
def test_carrier_frames_are_not_repeated_or_projected(case, n_structures):
    case.carrier.n_structures = n_structures
    with pytest.raises(ArgumentError) as caught:
        _bind(case)
    assert caught.value.extra['arg_name'] == 'molecular_system'
    assert case.carrier.n_structures == n_structures


@pytest.mark.parametrize('factory', [bmt.bind_interactions, bmt.PoseInteractions])
@pytest.mark.parametrize('missing', ['n_atoms', 'n_structures', 'coordinates'])
def test_missing_carrier_domains_have_a_local_argument_diagnostic(
    case, factory, missing
):
    original_get = case.provider.get
    before_result = case.result.to_dict()
    before_coordinates = puw.get_value(
        case.carrier.coordinates, to_unit='angstrom'
    ).copy()

    def get(value, *, element, **options):
        if options.get(missing) is True:
            return None
        return original_get(value, element=element, **options)

    case.provider.get = get
    with pytest.raises(ArgumentError) as caught:
        factory(case.result, case.carrier, **case.options)
    assert caught.value.code == 'BMT-E002'
    assert caught.value.extra['arg_name'] == 'molecular_system'
    assert case.result.to_dict() == before_result
    np.testing.assert_array_equal(
        puw.get_value(case.carrier.coordinates, to_unit='angstrom'), before_coordinates
    )


@pytest.mark.parametrize('indices', [[3, 4], [1, 3]])
def test_outside_or_wrong_order_maps_do_not_bind(case, indices):
    with pytest.raises(ArgumentError) as caught:
        _bind(case, pose_atom_indices=indices)
    assert caught.value.extra['arg_name'] == 'pose_atom_indices'


def test_translated_carrier_is_not_the_original_pose(case):
    case.carrier.coordinates = case.carrier.coordinates + puw.quantity(
        [100, 0, 0], 'pm'
    )
    before = puw.get_value(case.carrier.coordinates, to_unit='angstrom').copy()
    with pytest.raises(ArgumentError) as caught:
        _bind(case)
    assert caught.value.extra['arg_name'] == 'molecular_system'
    np.testing.assert_array_equal(
        puw.get_value(case.carrier.coordinates, to_unit='angstrom'), before
    )


def test_missing_analyses_and_unknown_names_are_distinct(case):
    binding = _bind(case)
    with pytest.raises(ArgumentError) as caught:
        binding.get_analysis('not-present')
    assert caught.value.extra['arg_name'] == 'name'
    case.carrier.interactions.clear()
    with pytest.raises(ArgumentError) as caught:
        _bind(case)
    assert caught.value.extra['arg_name'] == 'molecular_system'


def test_explicit_atom_axis_does_not_require_unmapped_labels(case):
    expected = deepcopy(case.result[1].metadata['source_atom_keys'])
    case.carrier.keys[0]['atom_id'] = None
    assert _molecular_atom_keys(case.carrier, atom_indices=(3, 1)) == expected
    binding = _bind(case)
    assert binding.pose.pose_id == 'selected'
    with pytest.raises(ArgumentError):
        _molecular_atom_keys(case.carrier)


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf')])
def test_nonfinite_mapped_carrier_coordinates_are_rejected(case, value):
    case.carrier.coordinates = puw.quantity(np.full((1, 4, 3), value), 'angstrom')
    with pytest.raises(ArgumentError) as caught:
        _bind(case)
    assert caught.value.extra['arg_name'] == 'coordinates'


def test_provider_failure_propagates_without_reclassification(case):
    error = RuntimeError('Synthetic provider conversion failure')

    def fail(*args, **kwargs):
        raise error

    case.provider.convert = fail
    before = case.result.to_dict()
    with pytest.raises(RuntimeError) as caught:
        _bind(case)
    assert caught.value is error
    assert case.result.to_dict() == before


def test_atom_key_annotations_are_preserved_without_becoming_identity_fields(case):
    case.result[1].metadata['source_atom_keys'][0]['annotation'] = 'original evidence'
    binding = _bind(case)
    assert binding.pose.metadata['source_atom_keys'][0]['annotation'] == (
        'original evidence'
    )
