"""Core helper admission keeps molecular semantics in the provider."""

from copy import deepcopy

import numpy as np
import pytest
import pyunitwizard as puw
from argdigest import UnknownArgumentError

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError


@pytest.fixture
def pose():
    return bmt.DockingPose(puw.quantity([[1, 2, 3]], 'nm'))


@pytest.fixture
def box():
    return bmt.BoxRegion(center='[1, 2, 3] nm', lengths='[2, 4, 6] nm')


@pytest.mark.parametrize(
    'helper',
    [
        'get_rmsd',
        'get_rmsds',
        'to_molecular_system',
        'reconstruct_problem',
        'to_backend_box',
        'validate_problem',
    ],
)
def test_helper_unknown_names_use_argdigest(helper, pose, box):
    owner = {
        'get_rmsd': pose,
        'to_molecular_system': pose,
        'get_rmsds': bmt.DockingResult([]),
        'reconstruct_problem': bmt.DockingResult([]),
        'to_backend_box': box,
        'validate_problem': bmt.VinaProtocol(),
    }[helper]
    with pytest.raises(UnknownArgumentError):
        getattr(owner, helper)(unkown=object())


@pytest.mark.parametrize('collection', [False, True])
def test_absent_rmsd_reference_is_rejected_even_for_an_empty_collection(
    collection, pose
):
    owner = bmt.DockingResult([]) if collection else pose
    method = owner.get_rmsds if collection else owner.get_rmsd
    with pytest.raises(ArgumentError) as caught:
        method(None)
    assert caught.value.extra['arg_name'] == 'reference'


def test_absent_partner_fails_before_pose_map_or_molecular_work(pose):
    with pytest.raises(ArgumentError) as caught:
        pose.to_molecular_system(None)
    assert caught.value.extra['arg_name'] == 'partner'


@pytest.mark.parametrize('problem', [None, object(), {}])
def test_protocol_admits_a_docking_problem_before_inspecting_intent(problem):
    with pytest.raises(ArgumentError) as caught:
        bmt.VinaProtocol().validate_problem(problem)
    assert caught.value.extra['arg_name'] == 'problem'


@pytest.mark.parametrize('selection', [None, np.array([0]), object()])
def test_rmsd_selection_and_molecular_form_are_delegated_unchanged(
    selection, pose, monkeypatch
):
    import molsysmt as msm

    import bindingmt.core.results as models

    key = {'atom_id': '1', 'element': 'C'}
    pose.metadata.update(pose_atom_order='verified_pdbqt_order', source_atom_keys=[key])
    reference = object()
    converted = object()
    observed = []
    monkeypatch.setattr(models, '_molecular_atom_keys', lambda value: [key])

    def convert(value, to_form):
        assert value is reference and to_form == 'molsysmt.MolSys'
        return converted

    def get(value, **kwargs):
        assert value is converted
        if kwargs.get('n_structures'):
            return 1
        assert kwargs.get('coordinates')
        return puw.quantity([[[1, 2, 3]]], 'nm')

    def select(value, selection):
        assert value is converted
        observed.append(selection)
        return [0]

    monkeypatch.setattr(msm, 'convert', convert)
    monkeypatch.setattr(msm, 'get', get)
    monkeypatch.setattr(msm, 'select', select)
    monkeypatch.setattr(
        msm.structure, 'get_rmsd', lambda *args, **kwargs: puw.quantity([0.25], 'nm')
    )
    result = bmt.DockingResult([pose])
    measurements = result.get_rmsds(reference, selection=selection)
    assert observed[0] is selection and len(observed) == 1
    assert puw.get_value(measurements[0], to_unit='angstrom') == pytest.approx(2.5)


def test_reconstruction_keeps_optional_overrides_and_attaches_only_after_success(
    box, monkeypatch
):
    problem = bmt.DockingProblem('rec.pdbqt', 'lig.pdbqt', box)
    saved = bmt.DockingResult([], problem_info=problem.to_dict())
    original = deepcopy(saved.to_dict())
    assert saved.reconstruct_problem().to_dict() == problem.to_dict()
    assert saved.to_dict() == original
    attached = saved.problem
    with pytest.raises(UnknownArgumentError):
        saved.reconstruct_problem(receptro=object())
    assert saved.problem is attached


@pytest.mark.parametrize('unit', [None, '', 'ps', 'nm**2', 1, True])
def test_backend_box_requires_an_explicit_length_unit(unit, box):
    with pytest.raises(ArgumentError) as caught:
        box.to_backend_box(unit)
    assert caught.value.extra['arg_name'] == 'unit'


@pytest.mark.parametrize('form', ['pint', 'unyt'])
@pytest.mark.parametrize('as_object', [False, True])
@pytest.mark.parametrize('target, factor', [('angstrom', 10), ('pm', 1000)])
def test_backend_box_retains_explicit_unit_and_caller_policy(
    form, as_object, target, factor
):
    with puw.context(default_form=form, standard_units=['pm', 'fs', 'kJ/mol']):
        box = bmt.BoxRegion(center='[1, 2, 3] nm', lengths='[2, 4, 6] nm')
        original = deepcopy(box.to_dict())
        policy = deepcopy(puw.configure.get_standard_units())
        unit = puw.unit(target) if as_object else target
        record = box.to_backend_box(unit)
        assert record['unit'] is unit
        assert record['center'] == pytest.approx(np.array([1, 2, 3]) * factor)
        assert record['lengths'] == pytest.approx(np.array([2, 4, 6]) * factor)
        assert record['size'] == record['lengths']
        assert box.to_dict() == original
        assert puw.configure.get_default_form() == form
        assert puw.configure.get_standard_units() == policy


def test_backend_unit_validation_retains_a_provider_failure(box, monkeypatch):
    failure = RuntimeError('provider validation failed')

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(puw, 'check', fail)
    with pytest.raises(ArgumentError) as caught:
        box.to_backend_box('angstrom')
    assert caught.value.extra['arg_name'] == 'unit'
    assert caught.value.__cause__ is failure
