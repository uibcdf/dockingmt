"""Public model admission, inheritance and provider delegation contracts."""

from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError

pytestmark = pytest.mark.filterwarnings('error::RuntimeWarning')


@pytest.fixture
def coordinates():
    return puw.quantity([[1, 2, 3]], 'angstrom')


@pytest.fixture
def box():
    return dmt.BoxRegion(center='[0, 0, 0] nm', lengths='[1, 1, 1] nm')


@pytest.mark.parametrize(
    'model', [dmt.DockingPose, dmt.DockingResult, dmt.DockingProblem]
)
def test_model_constructor_unknown_keywords_use_argdigest(model):
    with pytest.raises(UnknownArgumentError):
        model(metdata={})


@pytest.mark.parametrize(
    'factory',
    [
        dmt.DockingPose.from_dict,
        dmt.DockingResult.from_dict,
        dmt.DockingProblem.from_dict,
        dmt.DockingProblem.for_redocking,
        dmt.VinaProtocol.from_dict,
        dmt.BoxRegion.from_dict,
        dmt.BoxRegion.from_points,
        dmt.BoxRegion.from_bounds,
        dmt.BoxRegion.from_selection,
    ],
)
def test_model_factory_unknown_keywords_use_argdigest(factory):
    with pytest.raises(UnknownArgumentError):
        factory(metdata={})


@pytest.mark.parametrize(
    'argument', ['rank', 'pose_id', 'partner_state_id', 'receptor_state_id', 'metadata']
)
@pytest.mark.parametrize('invalid', [True, 1.5, []])
def test_pose_rejects_invalid_declared_fields(argument, invalid, coordinates):
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingPose(coordinates, **{argument: invalid})
    assert caught.value.extra['arg_name'] == argument


@pytest.mark.parametrize('rank', [0, -1, '2'])
def test_pose_rank_is_optional_positive_integer(rank, coordinates):
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingPose(coordinates, rank=rank)
    assert caught.value.extra['arg_name'] == 'rank'


def test_pose_optional_scores_do_not_relax_with_scores(coordinates):
    class ExtensionPose(dmt.DockingPose):
        __module__ = 'consumer_extension.models'

    class OverridePose(ExtensionPose):
        def __init__(self, coordinates, **kwargs):
            super().__init__(coordinates, **kwargs)

    for model in (dmt.DockingPose, ExtensionPose, OverridePose):
        pose = model(coordinates, scores=None, rank=np.int64(2))
        assert pose.scores == {}
        assert type(pose.rank) is int
        assert pose.rank == 2
        with pytest.raises(ArgumentError) as caught:
            pose.with_scores(None)
        assert caught.value.extra['arg_name'] == 'scores'
        with pytest.raises(UnknownArgumentError):
            model(coordinates, native_constructor='spoof')
        with pytest.raises(ArgumentError):
            model(coordinates, rank=True)


def test_result_optional_problem_does_not_relax_dock(coordinates):
    class ExtensionResult(dmt.DockingResult):
        __module__ = 'consumer_extension.models'

    for model in (dmt.DockingResult, ExtensionResult):
        result = model((pose for pose in [dmt.DockingPose(coordinates)]), problem=None)
        assert len(result) == 1
        assert result.problem is None
        with pytest.raises(ArgumentError) as caught:
            model([], problem='invalid')
        assert caught.value.extra['arg_name'] == 'problem'
    with pytest.raises(ArgumentError) as caught:
        dmt.dock(None)
    assert caught.value.extra['arg_name'] == 'problem'


@pytest.mark.parametrize('poses', [None, 'pose', {}, [object()], [None]])
def test_result_requires_pose_collection(poses):
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingResult(poses)
    assert caught.value.extra['arg_name'] == 'poses'


@pytest.mark.parametrize('argument', ['problem_info', 'protocol_info', 'provenance'])
def test_result_optional_records_require_mappings(argument):
    assert getattr(dmt.DockingResult([], **{argument: None}), argument) == {}
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingResult([], **{argument: [('seed', 2)]})
    assert caught.value.extra['arg_name'] == argument


def test_inherited_factories_preserve_units_and_detached_snapshots(coordinates, box):
    class ExtensionPose(dmt.DockingPose):
        __module__ = 'consumer_extension.models'

    class ExtensionResult(dmt.DockingResult):
        __module__ = 'consumer_extension.models'

    class ExtensionBox(dmt.BoxRegion):
        __module__ = 'consumer_extension.models'

    class ExtensionProtocol(dmt.VinaProtocol):
        __module__ = 'consumer_extension.models'

    original_values = puw.get_value(coordinates).copy()
    with puw.context(standard_units=['angstrom', 'fs', 'kcal/mol']):
        pose = ExtensionPose(coordinates, metadata={'nested': ['original']})
        result = ExtensionResult([pose])
        for model, record in (
            (ExtensionPose, pose.to_dict()),
            (ExtensionResult, result.to_dict()),
            (ExtensionBox, box.to_dict()),
            (ExtensionProtocol, dmt.VinaProtocol().to_dict()),
        ):
            original = deepcopy(record)
            restored = model.from_dict(data=record)
            assert isinstance(restored, model)
            assert restored.to_dict() == original
            assert record == original
        wire = pose.to_dict()
        restored = ExtensionPose.from_dict(wire)
        wire['metadata']['nested'].append('changed')
        assert restored.metadata['nested'] == ['original']
        assert str(puw.get_unit(restored.coordinates)) == 'nanometer'
    np.testing.assert_array_equal(puw.get_value(coordinates), original_values)


@pytest.mark.parametrize(
    'argument', ['search_domain', 'metadata', 'constraints', 'search_guidance']
)
def test_problem_local_options_fail_before_molecular_operations(
    argument, monkeypatch, box
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Invalid docking options reached molecular operations')

    for operation in ('get_form', 'get', 'select', 'convert'):
        monkeypatch.setattr(msm, operation, forbidden)
    kwargs = {'receptor': object(), 'partner': object(), 'search_domain': box}
    kwargs[argument] = object()
    with pytest.raises(ArgumentError) as caught:
        dmt.DockingProblem(**kwargs)
    assert caught.value.extra['arg_name'] == argument


def test_problem_inherited_constructor_and_factory_preserve_optional_inputs(box):
    class ExtensionProblem(dmt.DockingProblem):
        __module__ = 'consumer_extension.models'

    problem = ExtensionProblem('rec.pdbqt', 'lig.pdbqt', box)
    record = problem.to_dict()
    restored = ExtensionProblem.from_dict(record, receptor=None, partner=None)
    assert isinstance(restored, ExtensionProblem)
    assert restored.to_dict() == record
    with pytest.raises(ArgumentError) as caught:
        ExtensionProblem(None, 'lig.pdbqt', box)
    assert caught.value.extra['arg_name'] == 'receptor'


@pytest.mark.parametrize(
    'factory', [dmt.BoxRegion.from_selection, dmt.DockingProblem.for_redocking]
)
def test_molecular_factories_reject_invalid_padding_before_provider_work(
    factory, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Invalid padding reached molecular operations')

    for operation in ('get_form', 'get', 'select', 'convert'):
        monkeypatch.setattr(msm, operation, forbidden)
    source = (
        {'molecular_system': object()}
        if factory == dmt.BoxRegion.from_selection
        else {
            'complex_system': object(),
            'receptor_selection': 'all',
            'partner_selection': 'all',
        }
    )
    with pytest.raises(ArgumentError) as caught:
        factory(**source, padding='-1 nm')
    assert caught.value.extra['arg_name'] == 'padding'


@pytest.mark.parametrize('selection', [None, np.array([2, 0])])
def test_selection_factory_preserves_provider_values_and_exception(
    selection, monkeypatch
):
    import molsysmt as msm

    class ExtensionBox(dmt.BoxRegion):
        __module__ = 'consumer_extension.models'

    source = object()
    structures = object()
    state = object()
    provider_error = ValueError('Provider selection refusal')
    calls = []

    def provider_select(molecular_system, **kwargs):
        calls.append(kwargs)
        assert molecular_system is source
        assert kwargs['selection'] is selection
        assert kwargs['structure_indices'] is structures
        assert kwargs['chemical_state'] is state
        raise provider_error

    monkeypatch.setattr(msm, 'select', provider_select)
    with pytest.raises(ValueError) as caught:
        ExtensionBox.from_selection(
            source,
            selection=selection,
            structure_indices=structures,
            chemical_state=state,
        )
    assert caught.value is provider_error
    assert len(calls) == 1
