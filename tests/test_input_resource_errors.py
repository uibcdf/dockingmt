"""Public admission must preserve native resource and process-control failures."""

import errno
import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import pyunitwizard as puw

import bindingmt as bmt
from bindingmt._private.smonitor import ArgumentError
from bindingmt.core import problem as problem_module

STEPS = (
    'form',
    'conversion',
    'sizes',
    'state_count',
    'state_index',
    'state_id',
    'selection',
    'extraction',
    'coordinates',
)
ERRORS = (MemoryError, KeyboardInterrupt, SystemExit, ValueError)


def _provider(monkeypatch, fail_at=None, failure=None):
    calls = []
    source, selected = object(), object()
    coordinates = puw.quantity([[[0, 0, 0], [1, 2, 3]]], 'angstrom')
    report = SimpleNamespace(
        outcome='control', audited_scopes=[], is_exhaustive=False, issues=[]
    )

    def visit(step):
        calls.append(step)
        if step == fail_at:
            raise failure

    def get_form(value):
        assert value is source
        visit('form')
        return 'control.native'

    def convert(value, *, to_form, return_report):
        assert value is source and to_form == 'molsysmt.MolSys'
        assert return_report
        visit('conversion')
        return source, report

    def get(value, **options):
        if options.get('n_structures'):
            visit('sizes')
            return 2, 1
        if options.get('n_chemical_states'):
            visit('state_count')
            return 1
        if options.get('structure_chemical_state_index'):
            visit('state_index')
            return [0]
        if options.get('chemical_state_id'):
            visit('state_id')
            return ['control-state']
        if options.get('coordinates'):
            assert value is selected
            visit('coordinates')
            return coordinates
        assert options.get('n_atoms')
        return 2

    def select(value, **options):
        assert value is source
        visit('selection')
        return [0, 1]

    def extract(value, **options):
        assert value is source and options['selection'] == [0, 1]
        visit('extraction')
        return selected

    monkeypatch.setattr(
        problem_module,
        'msm',
        SimpleNamespace(
            get_form=get_form, convert=convert, get=get, select=select, extract=extract
        ),
    )
    return source, selected, calls


def _construct(route, source):
    if route == 'redocking':
        return bmt.DockingProblem.for_redocking(
            source,
            receptor_selection='all',
            partner_selection='all',
            padding=puw.quantity(1, 'angstrom'),
        )
    box = bmt.BoxRegion(
        center=puw.quantity([0, 0, 0], 'angstrom'),
        lengths=puw.quantity([5, 5, 5], 'angstrom'),
    )
    inputs = {'receptor': 'pdbqt_text:CONTROL', 'partner': 'pdbqt_text:CONTROL'}
    inputs[route] = source
    return bmt.DockingProblem(**inputs, search_domain=box)


@pytest.mark.parametrize('route', ['receptor', 'partner', 'redocking'])
@pytest.mark.parametrize('step', STEPS)
@pytest.mark.parametrize('error_type', ERRORS)
def test_molecular_admission_preserves_resource_errors_and_stops(
    monkeypatch, route, step, error_type
):
    failure = error_type('injected provider failure')
    source, _, calls = _provider(monkeypatch, step, failure)
    expected = ArgumentError if error_type is ValueError else error_type
    with pytest.raises(expected) as caught:
        _construct(route, source)
    if error_type is ValueError:
        assert caught.value.__cause__ is failure
        assert caught.value.code == 'BMT-E002'
        assert caught.value.extra['arg_name'] == (
            'partner' if route == 'redocking' else route
        )
    else:
        assert caught.value is failure
    assert calls == list(STEPS[: STEPS.index(step) + 1])


@pytest.mark.parametrize('route', ['receptor', 'partner', 'redocking'])
def test_valid_molecular_admission_retains_axes_state_and_sources(monkeypatch, route):
    source, selected, calls = _provider(monkeypatch)
    problem = _construct(route, source)
    roles = ('receptor', 'partner') if route == 'redocking' else (route,)
    for role in roles:
        assert getattr(problem, role) is source
        assert getattr(problem, f'{role}_molsys') is selected
        assert getattr(problem, f'{role}_atom_indices') == [0, 1]
        assert getattr(problem, f'{role}_structure_index') == 0
        assert getattr(problem, f'{role}_chemical_state_index') == 0
        assert (
            problem.to_dict()['molecular_inputs'][role]['chemical_state_id']
            == 'control-state'
        )
    assert calls[: len(STEPS)] == list(STEPS)


@pytest.mark.parametrize('error_type', ERRORS)
@pytest.mark.parametrize(
    'boundary,field',
    [
        ('box', 'center'),
        ('protocol', 'energy_range'),
        ('evaluation', 'rmsd_cutoff'),
        ('binding', 'coordinate_tolerance'),
        ('unit_parser', 'unit'),
        ('unit_dimension', 'unit'),
        ('score', 'score_definitions'),
    ],
)
def test_quantity_admission_preserves_resource_errors_and_provider_causes(
    monkeypatch, boundary, field, error_type
):
    length = puw.quantity(1, 'angstrom')
    energy = puw.quantity(1, 'kcal/mol')
    vector = puw.quantity([1, 2, 3], 'angstrom')
    box = bmt.BoxRegion(center=vector, lengths=vector)
    pose = bmt.DockingPose(puw.quantity([[0, 0, 0]], 'angstrom'))
    result = bmt.DockingResult([pose])
    failure = error_type('injected quantity-provider failure')
    calls = []

    def fail(*args, **kwargs):
        calls.append(boundary)
        raise failure

    def invoke():
        if boundary == 'box':
            return bmt.BoxRegion(center=vector, lengths=vector)
        if boundary == 'protocol':
            return bmt.VinaProtocol(energy_range=energy)
        if boundary == 'evaluation':
            return bmt.evaluate_redocking(result, pose.coordinates, rmsd_cutoff=length)
        if boundary == 'binding':
            return bmt.bind_interactions(
                result,
                object(),
                pose_index=0,
                pose_atom_indices=[0],
                partner_state_id='partner',
                receptor_state_id='receptor',
                assume_aligned=True,
                coordinate_tolerance=length,
            )
        if boundary.startswith('unit_'):
            return box.to_backend_box(unit='angstrom')
        return pose.with_scores(
            {'control': -1},
            score_definitions={
                'control': {
                    'schema_version': '1.0',
                    'method': 'control',
                    'method_version': '1',
                    'component': 'control',
                    'kind': 'empirical',
                    'unit': 'kcal/mol',
                    'preferred_direction': 'lower',
                    'context': {'control': True},
                }
            },
        )

    operation = {
        'unit_parser': 'is_unit',
        'unit_dimension': 'check',
        'score': 'quantity',
    }.get(boundary, 'ensure_quantity')
    monkeypatch.setattr(puw, operation, fail)
    expected = ArgumentError if error_type is ValueError else error_type
    with pytest.raises(expected) as caught:
        invoke()
    if error_type is ValueError:
        assert caught.value.__cause__ is failure
        assert caught.value.code == 'BMT-E002'
        assert caught.value.extra['arg_name'] == field
    else:
        assert caught.value is failure
    assert calls == [boundary]
    assert not pose.scores


@pytest.mark.parametrize('step', ['conversion', 'coordinates', 'names', 'elements'])
@pytest.mark.parametrize(
    'error_kind', ['memory', 'os_memory', 'ordinary', 'os_ordinary']
)
def test_scoring_geometry_preserves_resource_errors_and_cleans_staging(
    monkeypatch, tmp_path, step, error_kind
):
    from depdigest.core import checker

    from bmt_test_support.pdbqt_fixtures import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT

    scoring = importlib.import_module('bindingmt.engines._vina_scoring')
    engine = importlib.import_module('bindingmt.engines.vina')
    problem = bmt.DockingProblem(
        MINIMAL_REC_PDBQT,
        MINIMAL_LIG_PDBQT,
        bmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'),
            puw.quantity([10, 10, 10], 'angstrom'),
        ),
    )
    protocol = bmt.VinaProtocol(cpu=1, seed=17)
    before = problem.to_dict(), protocol.to_dict()
    failure = {
        'memory': MemoryError('controlled geometry allocation failure'),
        'os_memory': OSError(errno.ENOMEM, 'controlled geometry allocation failure'),
        'ordinary': ValueError('controlled malformed geometry'),
        'os_ordinary': OSError(errno.ENOSPC, 'controlled geometry I/O failure'),
    }[error_kind]
    native = object()
    coordinates = puw.quantity([[[0, 0, 0], [1.5, 0, 0]]], 'angstrom')
    calls = []
    staged = []

    def visit(operation):
        calls.append(operation)
        if operation == step:
            raise failure

    def convert(value, **options):
        assert value == 'pdbqt_text:' + MINIMAL_LIG_PDBQT
        assert options == {
            'to_form': 'molsysmt.MolSys',
            'discard_torsion_tree': True,
        }
        visit('conversion')
        return native

    def get(value, **options):
        assert value is native and options['element'] == 'atom'
        if options.get('coordinates'):
            visit('coordinates')
            return coordinates
        if options.get('name'):
            visit('names')
            return ['C1', 'C2']
        assert options.get('atom_type')
        visit('elements')
        return ['C', 'C']

    def forbidden(*args, **kwargs):
        pytest.fail('Geometry failure reached native construction')

    available = checker.is_installed
    monkeypatch.setattr(
        checker,
        'is_installed',
        lambda name: True if name == 'vina' else available(name),
    )
    monkeypatch.setitem(sys.modules, 'vina', SimpleNamespace(Vina=forbidden))
    monkeypatch.setattr(scoring, 'msm', SimpleNamespace(convert=convert, get=get))
    factory = engine.tempfile.NamedTemporaryFile

    def allocate(**options):
        created = factory(dir=tmp_path, **options)
        staged.append(Path(created.name))
        return created

    monkeypatch.setattr(engine.tempfile, 'NamedTemporaryFile', allocate)
    expected = type(failure) if error_kind in ('memory', 'os_memory') else ArgumentError
    with pytest.raises(expected) as caught:
        bmt.score(problem, protocol)
    if error_kind in ('memory', 'os_memory'):
        assert caught.value is failure
    else:
        assert caught.value.__cause__ is failure
        assert caught.value.code == 'BMT-E002'
        assert caught.value.extra['arg_name'] == 'problem.partner'
    order = ['conversion', 'coordinates', 'names', 'elements']
    assert calls == order[: order.index(step) + 1]
    assert staged and all(not path.exists() for path in staged)
    assert (problem.to_dict(), protocol.to_dict()) == before
