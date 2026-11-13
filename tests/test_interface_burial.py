"""Independent analytic receiving of MolSysMT-composed interface burial."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt.native import MolSys, Structures
from pyunitwizard.record import QuantityRecord, RecordError

import bindingmt as bmt
from bindingmt._private.interface_burial import (
    AREA_FIELD,
    VERIFICATION_RTOL,
    area_values,
    loss_statuses,
)
from bindingmt._private.interface_records import _digest


def spheres(types=('C', 'H'), distance=0.31, angle=0.0, groups=True):
    system = MolSys(n_atoms=len(types), **({'n_groups': len(types)} if groups else {}))
    msm.set(system, element='atom', atom_type=list(types))
    if groups:
        msm.set(system, element='atom', group_index=list(range(len(types))))
    coordinates = np.zeros((3, len(types), 3))
    coordinates[:, 1, :2] = distance * np.array([np.cos(angle), np.sin(angle)])
    if len(types) > 2:
        coordinates[:, 2, 0] = -0.31
    system.structures = Structures(coordinates=puw.quantity(coordinates, 'nm'))
    return system


def calculate(system, **options):
    return bmt.calculate_interface_burial(
        system,
        **{
            'participants': {'A': [0], 'B': [1]},
            'structure_index': 2,
            'source_id': 'authored-spheres',
            'probe_radius': '0.14 nm',
            'n_sphere_points': 960,
            'hydrogen_policy': 'as_supplied',
            **options,
        },
    )


def sides(result):
    return np.array(
        [
            float(puw.get_value(q, to_unit='nm**2'))
            for q in result.burial_areas['sides'].values()
        ]
    )


def analytic_losses(ra, rb, distance):
    # Independent spherical-cap geometry, used only as a test oracle.
    ha = ra - (distance**2 + ra**2 - rb**2) / (2 * distance)
    hb = rb - (distance**2 + rb**2 - ra**2) / (2 * distance)
    return np.array([2 * np.pi * ra * ha, 2 * np.pi * rb * hb])


@pytest.mark.parametrize('points', [240, 960, 3840])
@pytest.mark.parametrize('angle', [0.0, 0.37, 1.12])
@pytest.mark.parametrize(
    'types,radii', [(('C', 'C'), (0.31, 0.31)), (('C', 'H'), (0.31, 0.25))]
)
def test_independent_spherical_caps_at_declared_densities_and_rotations(
    points, angle, types, radii
):
    result = calculate(spheres(types, angle=angle), n_sphere_points=points)
    expected = analytic_losses(*radii, 0.31)
    # Frozen admission: eight largest-sphere sample patches per side, not a
    # universal accuracy estimate or an assumed monotonic convergence property.
    budget = 8 * 4 * np.pi * max(radii) ** 2 / points
    np.testing.assert_allclose(sides(result), expected, rtol=0, atol=budget)
    assert result.surface_calculation['numerical']['burial_usable'] is True
    for side, radius in zip(result.surface_calculation['participants'].values(), radii):
        np.testing.assert_allclose(
            area_values(side['isolated_area']),
            [4 * np.pi * radius**2],
            rtol=2e-14,
            atol=0,
        )


def test_actual_three_contexts_and_asymmetric_conventions(monkeypatch):
    calls = []
    original = msm.physchem.get_sasa

    def traced(system, **kwargs):
        calls.append((msm.get(system, n_atoms=True), deepcopy(kwargs)))
        return original(system, **kwargs)

    monkeypatch.setattr(msm.physchem, 'get_sasa', traced)
    result = calculate(spheres())
    losses = sides(result)
    assert losses[0] != losses[1]
    assert [n for n, _ in calls] == [1, 1, 2]
    for _, options in calls:
        assert options['selection'] == 'all' and options['structure_indices'] == [0]
        assert (
            options['pbc']
            is options['use_gpu']
            is options['use_cell_list']
            is options['parallel']
            is False
        )
        assert options['num_threads'] == 1 and options['engine'] == 'MolSysMT'
    assert float(
        puw.get_value(result.burial_areas['total'], to_unit='nm**2')
    ) == pytest.approx(sum(losses))
    assert float(
        puw.get_value(result.burial_areas['mean_side'], to_unit='nm**2')
    ) == pytest.approx(sum(losses) / 2)
    assert result.contact_calculation is None
    assert result.summary()['native_contacts'] is None
    assert (
        result.summary()['native_surface']['positive_interface_finding']
        == 'not_assessed'
    )
    assert result.summary()['analyses']['surface']['finding_count'] == 1
    with pytest.raises(bmt.exceptions.ArgumentError):
        result.project_footprint(participant='A')


def test_separated_zero_and_containment():
    result = calculate(spheres(distance=5))
    np.testing.assert_array_equal(sides(result), [0, 0])
    assert result.summary()['analyses']['surface']['original_outcome'] == 'completed'
    assert result.summary()['native_surface']['result_count'] == 1
    contained = calculate(spheres(distance=0))
    np.testing.assert_allclose(
        sides(contained), [0, 4 * np.pi * 0.25**2], rtol=2e-14, atol=0
    )


def test_unrelated_occluder_is_removed_by_context_extraction():
    system = spheres(types=('C', 'C', 'C'))
    result = calculate(system)
    isolated = area_values(
        result.surface_calculation['participants']['A']['isolated_area']
    )
    selected = msm.physchem.get_sasa(
        system,
        selection=[0],
        structure_indices=[2],
        probe_radius='0.14 nm',
        n_sphere_points=960,
        pbc=False,
        use_gpu=False,
        use_cell_list=False,
        parallel=False,
        num_threads=1,
    )
    assert float(puw.get_value(selected, to_unit='nm**2')[0, 0]) < float(isolated[0])
    np.testing.assert_array_equal(
        sides(result), sides(calculate(spheres(types=('C', 'C'))))
    )


def test_groups_source_permutation_and_immutability():
    system = spheres(types=('C', 'H', 'O'))
    before = puw.get_value(msm.get(system, coordinates=True), to_unit='nm').copy()
    moved = msm.permute_atoms(system, [2, 1, 0], return_report=True)
    result = calculate(
        moved['molecular_system'],
        participants={'A': [2], 'B': [1]},
        atom_map=moved['report'],
        source_structure_index=2,
    )
    evidence = result.surface_calculation
    assert evidence['participants']['A']['source_atom_indices'] == [0]
    assert evidence['participants']['A']['local_atom_indices'] == [2]
    assert evidence['participants']['A']['group_indices'] == [0]
    assert [p['input_atom_indices'] for p in evidence['context']['projections']] == [
        [2],
        [1],
        [1, 2],
    ]
    assert all(
        p['input_structure_index'] == 2 and p['local_structure_index'] == 0
        for p in evidence['context']['projections']
    )
    for side in evidence['participants'].values():
        assert side['group_contributions'][0]['atom_positions'] == [0]
        np.testing.assert_array_equal(
            area_values(side['group_contributions'][0]['loss']),
            area_values(side['side_loss']),
        )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(system, coordinates=True), to_unit='nm'), before
    )
    edited = result.surface_calculation
    edited['participants']['A']['local_atom_indices'][0] = 999
    assert result.surface_calculation == evidence
    assert (
        result.revise(
            question={'kind': 'association', 'description': 'reinterpretation'},
            reason='new question',
        ).surface_calculation
        == evidence
    )


def test_partial_groups_remain_partial():
    result = calculate(spheres(groups=False))
    for side in result.surface_calculation['participants'].values():
        assert side['group_coverage'] == 'partial' and side['group_contributions'] == []
    assert result.summary()['native_surface']['group_coverage'] == {
        'A': 'partial',
        'B': 'partial',
    }


@pytest.mark.parametrize(
    'options',
    [
        {'probe_radius': 1},
        {'probe_radius': '-1 nm'},
        {'probe_radius': '1 ps'},
        {'probe_radius': 'nan nm'},
        {'probe_radius': '[1, 2] nm'},
        {'n_sphere_points': 0},
        {'n_sphere_points': True},
        {'hydrogen_policy': 'implicit'},
        {'max_surface_evaluations': 5759},
        {'participants': {'A': [], 'B': [1]}},
        {'participants': {'A': [0], 'B': [0]}},
        {'structure_index': 3},
        {'source_id': ''},
    ],
)
def test_invalid_and_budget_refusal_before_extract_or_surface(options, monkeypatch):
    system = spheres()

    def forbidden(*args, **kwargs):
        pytest.fail('Invalid request reached extraction or surface execution')

    monkeypatch.setattr(msm, 'extract', forbidden)
    monkeypatch.setattr(msm.physchem, 'get_sasa', forbidden)
    with pytest.raises(bmt.exceptions.ArgumentError):
        calculate(system, **options)


def test_required_failure_and_missing_radius_never_become_zero(monkeypatch):
    system = spheres()
    previous = calculate(system)
    snapshot = previous.to_dict()
    error = MemoryError('owned child failure')

    def failed(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm.physchem, 'get_sasa', failed)
    with pytest.raises(MemoryError) as caught:
        calculate(system)
    assert caught.value is error and previous.to_dict() == snapshot
    # An absent owner element is a refusal; no local radius fallback is permitted.
    with pytest.raises((KeyError, TypeError, ValueError, bmt.exceptions.ArgumentError)):
        calculate(spheres(types=('C', 'Xx')))


def test_changed_source_refuses(monkeypatch):
    system = spheres()
    original = msm.physchem.get_sasa
    calls = []

    def changed(subset, **kwargs):
        result = original(subset, **kwargs)
        calls.append(True)
        if len(calls) == 3:
            msm.set(
                system,
                structure_indices=[2],
                coordinates=puw.quantity([[[0, 0, 0], [5, 0, 0]]], 'nm'),
            )
        return result

    monkeypatch.setattr(msm.physchem, 'get_sasa', changed)
    with pytest.raises(bmt.exceptions.ArgumentError, match='source changed'):
        calculate(system)


def test_negative_roundoff_and_inconsistent_controls_are_never_clamped():
    eps = np.finfo(float).eps
    assert VERIFICATION_RTOL == 32 * eps
    assert loss_statuses([1, 1, 0, 1], [0, -eps, -eps, -1e-6]) == [
        'nonnegative',
        'negative_within_roundoff',
        'inconsistent_negative',
        'inconsistent_negative',
    ]


def test_quantity_policy_and_typed_readback(tmp_path):
    system = spheres()
    baseline = sides(calculate(system))
    with puw.context(default_form='unyt', standard_units=['pm', 'fs']):
        before = deepcopy(puw.configure.report())
        result = calculate(system, probe_radius=puw.quantity(140, 'pm'))
        result.save(tmp_path / 'surface.json')
        restored = bmt.BindingInterface.read(
            tmp_path / 'surface.json', experimental=True
        )
        assert restored.to_dict() == result.to_dict()
        np.testing.assert_allclose(sides(restored), baseline, rtol=2e-14, atol=0)
        assert puw.configure.report() == before
        assert puw.get_form(restored.burial_areas['total']) == 'unyt'
        assert restored.copy().to_dict() == restored.to_dict()
    with pytest.raises(bmt.exceptions.ArgumentError):
        bmt.BindingInterface.read(tmp_path / 'surface.json')


@pytest.mark.parametrize(
    'change',
    ['dimension', 'field', 'loss', 'total', 'groups', 'call', 'projection', 'status'],
)
def test_semantic_tampering_refuses_even_with_recomputed_digest(change):
    record = calculate(spheres()).to_dict()
    c = record['analyses']['surface']['calculation']
    side = c['participants']['A']
    if change == 'dimension':
        side['atomic_loss'] = c['probe_radius']
    elif change == 'field':
        side['side_loss'] = QuantityRecord.from_quantity(
            puw.quantity(1, 'nm**2'), field='foreign.area'
        ).to_dict()
    elif change == 'loss':
        side['atomic_loss'] = side['isolated_area']
    elif change == 'total':
        c['totals']['total'] = c['totals']['mean_side']
    elif change == 'groups':
        side['group_contributions'][0]['atom_positions'] = []
    elif change == 'call':
        c['calls'][0]['options']['pbc'] = True
    elif change == 'projection':
        c['context']['projections'][0]['local_structure_index'] = 2
    else:
        c['numerical']['burial_usable'] = False
    record['content_sha256'] = _digest(record)
    with pytest.raises((bmt.exceptions.ArgumentError, RecordError)):
        bmt.BindingInterface.from_dict(record, experimental=True)
    assert AREA_FIELD == 'bindingmt.burial.area'


def test_multiatom_group_contributions_and_original_frame_projection():
    system = spheres(types=('C', 'H', 'O'))
    msm.set(system, element='atom', group_index=[0, 1, 0])
    extracted = msm.extract(system, structure_indices=[2])
    mapping = {
        'schema': 'molsysmt.atom_map@1',
        'n_source_atoms': 3,
        'n_output_atoms': 3,
        'source_to_output_atom_indices': [0, 1, 2],
        'output_to_source_atom_indices': [0, 1, 2],
    }
    result = calculate(
        extracted,
        participants={'A': [2, 0], 'B': [1]},
        structure_index=0,
        source_structure_index=2,
        atom_map=mapping,
    )
    c = result.surface_calculation
    assert (
        c['context']['structure_index'] == 0
        and c['context']['source_structure_index'] == 2
    )
    a = c['participants']['A']
    assert a['local_atom_indices'] == [0, 2] and a['source_atom_indices'] == [0, 2]
    assert a['group_indices'] == [0, 0]
    assert len(a['group_contributions']) == 1
    assert a['group_contributions'][0]['atom_positions'] == [0, 1]
    np.testing.assert_allclose(
        area_values(a['group_contributions'][0]['loss']),
        np.sum(area_values(a['atomic_loss'])),
        rtol=2e-14,
        atol=0,
    )
    reverse = calculate(system, participants={'B': [1], 'A': [0, 2]})
    np.testing.assert_allclose(sides(reverse)[::-1], sides(result), rtol=2e-14, atol=0)


@pytest.mark.parametrize('inconsistent', [False, True])
def test_injected_negative_child_observation_is_preserved_with_its_status(
    inconsistent, monkeypatch, tmp_path
):
    # Software adversity only: wrap real calls, then deliberately inject a
    # negative loss. These injected values are not scientific sampling evidence.
    original = msm.physchem.get_sasa
    observations = []

    def injected(system, **kwargs):
        quantity = original(system, **kwargs)
        values = np.asarray(puw.get_value(quantity, to_unit='nm**2')).copy()
        if len(observations) == 2:
            isolated = observations[0][0, 0]
            values[0, 0] = isolated + (1e-4 if inconsistent else np.spacing(isolated))
        observations.append(values)
        return puw.quantity(values, 'nm**2')

    monkeypatch.setattr(msm.physchem, 'get_sasa', injected)
    result = calculate(spheres())
    c = result.surface_calculation
    loss = area_values(c['participants']['A']['atomic_loss'])[0]
    assert loss < 0
    assert c['numerical']['atomic_loss_status']['A'] == [
        'inconsistent_negative' if inconsistent else 'negative_within_roundoff'
    ]
    assert c['numerical']['burial_usable'] is (not inconsistent)
    assert c['numerical']['clamped'] is False
    result.save(tmp_path / 'injected-software-only.json')
    restored = bmt.BindingInterface.read(
        tmp_path / 'injected-software-only.json', experimental=True
    )
    assert restored.to_dict() == result.to_dict()
