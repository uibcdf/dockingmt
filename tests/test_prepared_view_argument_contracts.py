"""Prepared declaration and owned view admission without molecular interpretation."""

import importlib
from types import SimpleNamespace

import numpy as np
import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError, ViewerPosePositionError

pytestmark = pytest.mark.filterwarnings('error::RuntimeWarning')


def prepared_options(role):
    values = dict(
        state_id='declared',
        atom_names=['C1'],
        coordinates=None,
        atom_types=['C'],
        charges=[0.0],
    )
    if role == 'ligand':
        values['group_name'] = 'LIG'
    else:
        values.update(group_names=['LIG'], group_ids=[1])
    return values


@pytest.mark.parametrize('model', [bmt.PreparedLigand, bmt.PreparedReceptor])
def test_prepared_unknown_keywords_use_argdigest(model):
    with pytest.raises(UnknownArgumentError):
        model(metdata={})


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
@pytest.mark.parametrize('state_id', [None, '', '   ', 7])
def test_prepared_state_identifier_is_required(role, state_id):
    options = prepared_options(role)
    options['state_id'] = state_id
    with pytest.raises(ArgumentError) as caught:
        getattr(bmt, f'Prepared{role.title()}')(**options)
    assert caught.value.extra['arg_name'] == 'state_id'


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
@pytest.mark.parametrize('metadata', [False, [('method', 'external')]])
def test_prepared_metadata_refuses_accidental_coercion(role, metadata):
    options = prepared_options(role)
    with pytest.raises(ArgumentError) as caught:
        getattr(bmt, f'Prepared{role.title()}')(**options, metadata=metadata)
    assert caught.value.extra['arg_name'] == 'metadata'


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
@pytest.mark.parametrize('argument', ['atom_names', 'atom_types', 'charges'])
@pytest.mark.parametrize('value', ['C1', {'C1': 0}, {'C1'}])
def test_prepared_columns_require_ordered_collections(role, argument, value):
    options = prepared_options(role)
    options[argument] = value
    with pytest.raises(ArgumentError) as caught:
        getattr(bmt, f'Prepared{role.title()}')(**options)
    assert caught.value.extra['arg_name'] == argument


@pytest.mark.parametrize('argument', ['group_names', 'group_ids'])
def test_required_receptor_groups_do_not_inherit_ligand_defaults(argument):
    options = prepared_options('receptor')
    options[argument] = None
    with pytest.raises(ArgumentError) as caught:
        bmt.PreparedReceptor(**options)
    assert caught.value.extra['arg_name'] == argument


@pytest.mark.parametrize(
    'argument,value', [('group_name', 7), ('_torsion_tree', object())]
)
def test_ligand_owned_fields_fail_before_constructor_access(argument, value):
    options = prepared_options('ligand')
    options[argument] = value
    with pytest.raises(ArgumentError) as caught:
        bmt.PreparedLigand(**options)
    assert caught.value.extra['arg_name'] == argument


@pytest.mark.parametrize('role', ['ligand', 'receptor'])
def test_inherited_prepared_declarations_preserve_opaque_provider_values(
    role, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail('Declaration admission performed a molecular operation')

    for operation in ('get', 'get_form', 'select', 'convert', 'set', 'copy'):
        monkeypatch.setattr(msm, operation, forbidden)
    base = getattr(bmt, f'Prepared{role.title()}')

    class Extension(base):
        __module__ = 'consumer_extension.prepared'

    class Override(Extension):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

    coordinates, source = object(), object()
    for model in (base, Extension, Override):
        options = prepared_options(role)
        options.update(
            atom_names=(name for name in ['C1']),
            atom_types=np.array(['C']),
            charges=iter([0.0]),
            coordinates=coordinates,
            source_molsys=source,
        )
        if role == 'ligand':
            options.update(torsion_dof=np.int64(0), group_names=None, group_ids=None)
        prepared = model(**options)
        assert prepared.coordinates is coordinates
        assert prepared.source_molsys is source
        assert prepared.atom_names == ['C1']
        assert prepared.atom_types == ['C']
        assert prepared.charges == [0.0]
        assert prepared.group_names == ['LIG']
        assert prepared.group_ids == [1]
        assert prepared.metadata == {}
        if role == 'ligand':
            assert type(prepared.torsion_dof) is int
        with pytest.raises(ArgumentError):
            model(**dict(options, state_id=None))


@pytest.mark.parametrize('torsion_dof', [None, True, -1, 1.5])
def test_ligand_torsion_count_refuses_invalid_scalars(torsion_dof):
    with pytest.raises(ArgumentError) as caught:
        bmt.PreparedLigand(**prepared_options('ligand'), torsion_dof=torsion_dof)
    assert caught.value.extra['arg_name'] == 'torsion_dof'


def test_ligand_keeps_its_independent_tree_count_invariant():
    with pytest.raises(ArgumentError, match='matching ROOT/BRANCH tree'):
        bmt.PreparedLigand(**prepared_options('ligand'), torsion_dof=1)


@pytest.fixture
def view_calls(monkeypatch):
    import molsysmt as msm
    import molsysviewer as msv

    from molsysviewer_bindingmt.adapters import complex, shapes

    addon = importlib.import_module('molsysviewer_bindingmt.addon')
    calls = []
    widget = object()

    def create(**kwargs):
        calls.append(('create', kwargs))
        return widget

    monkeypatch.setattr(msv, 'new_view', create)
    monkeypatch.setattr(addon, 'on_enable', lambda view: calls.append(('enable', view)))
    monkeypatch.setattr(
        complex,
        'render_docking_result',
        lambda **kwargs: calls.append(('result', kwargs)),
    )
    monkeypatch.setattr(
        complex, 'set_active_pose', lambda view, rank: calls.append(('position', rank))
    )
    monkeypatch.setattr(
        shapes,
        'render_search_domain',
        lambda view, domain: calls.append(('domain', domain)),
    )

    def forbidden(*args, **kwargs):
        pytest.fail('Invalid view options reached molecular operations')

    for operation in ('get', 'get_form', 'select', 'convert', 'set', 'copy'):
        monkeypatch.setattr(msm, operation, forbidden)
    return calls, widget


@pytest.mark.parametrize(
    'argument,value',
    [
        ('item', object()),
        ('result', object()),
        ('problem', object()),
        ('search_domain', object()),
        ('pose_rank', True),
        ('pose_rank', 0),
        ('pose_rank', -1),
        ('pose_rank', 1.5),
        ('pose_rank', '2'),
    ],
)
def test_invalid_owned_view_arguments_fail_before_scene_changes(
    argument, value, view_calls
):
    calls, _ = view_calls
    with pytest.raises(ArgumentError) as caught:
        bmt.view(**{argument: value})
    assert caught.value.extra['arg_name'] == argument
    assert caught.value.extra['caller'] == 'bindingmt.view.view'
    assert calls == []


@pytest.mark.parametrize('entry', [bmt.view, bmt.show])
def test_view_forwards_provider_options_without_digestion_or_bypass(entry, view_calls):
    calls, widget = view_calls
    opaque = object()
    provider_options = dict(
        height='500px', coordinates=opaque, kwargs=opaque, skip_digestion=True
    )
    assert entry(**provider_options) is widget
    assert calls == [('create', provider_options), ('enable', widget)]
    calls.clear()
    with pytest.raises(ArgumentError):
        entry(pose_rank=False, **provider_options)
    assert calls == []


def test_existing_view_is_reused_with_optional_owned_defaults(view_calls):
    calls, _ = view_calls
    existing = object()
    assert (
        bmt.view(view=existing, result=None, problem=None, search_domain=None)
        is existing
    )
    assert calls == [('enable', existing)]


def test_view_resolves_item_and_preserves_molecular_provider_values(view_calls):
    calls, widget = view_calls
    poses = [bmt.DockingPose(puw.quantity([[0, 0, 0]], 'nm'), rank=9)]
    result = bmt.DockingResult(poses)
    receptor, partner, reference = object(), object(), object()
    assert (
        bmt.view(result, receptor=receptor, partner=partner, reference=reference)
        is widget
    )
    kwargs = next(value for action, value in calls if action == 'result')
    assert kwargs['result'] is result
    assert kwargs['receptor'] is receptor
    assert kwargs['partner'] is partner
    assert kwargs['reference'] is reference
    calls.clear()
    with pytest.raises(ViewerPosePositionError):
        bmt.view(result, pose_rank=2)
    assert calls == []


def test_view_position_is_collection_index_and_accepts_numpy_integer(view_calls):
    calls, _ = view_calls
    result = bmt.DockingResult(
        [bmt.DockingPose(puw.quantity([[0, 0, 0]], 'nm'), rank=rank) for rank in (9, 2)]
    )
    bmt.view(result, pose_rank=np.int64(2))
    position = next(value for action, value in calls if action == 'position')
    assert type(position) is int
    assert position == 2


def test_view_preserves_existing_duck_typed_item_route(view_calls):
    calls, _ = view_calls
    result = SimpleNamespace(poses=[], problem=None)
    bmt.view(result)
    assert (
        next(value for action, value in calls if action == 'result')['result'] is result
    )


def test_view_rejects_conflicting_result_before_scene_changes(view_calls):
    calls, _ = view_calls
    with pytest.raises(ArgumentError):
        bmt.view(bmt.DockingResult([]), result=bmt.DockingResult([]))
    assert calls == []


def test_view_preserves_provider_factory_failure(view_calls, monkeypatch):
    import molsysviewer as msv

    calls, _ = view_calls
    failure = ValueError('provider option refusal')

    def refuse(**kwargs):
        raise failure

    monkeypatch.setattr(msv, 'new_view', refuse)
    with pytest.raises(ValueError) as caught:
        bmt.view(height=object())
    assert caught.value is failure
    assert calls == []
