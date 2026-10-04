"""Consume named provider charges without certifying the remaining preparation."""

import json
from copy import deepcopy
from math import fsum
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_REC_PDBQT

import dockingmt as dmt
from dockingmt._private.smonitor import ArgumentError

METHANOL = Path(__file__).parent / 'data/charges/methanol.sdf'


@pytest.fixture
def assigned():
    source = msm.convert(METHANOL, to_form='molsysmt.MolSys')
    return msm.build.assign_partial_charges(source, method='gasteiger_marsili')


def atom_charges(system):
    values = msm.get(system, partial_charge=True)
    if puw.is_quantity(values):
        values = puw.get_value(values, to_unit='elementary_charge')
    return np.asarray(values)


def written_charges(prepared):
    # Independent assertion against the actual fixed-column text, not a reader
    # used by production preparation or its numeric audit.
    return [
        float(line[70:76])
        for line in prepared.to_pdbqt().splitlines()
        if line.startswith('ATOM')
    ]


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_named_charges_preserve_original_model_and_explicit_transfers(
    assigned, prepare
):
    before = atom_charges(assigned).copy()
    assignment = deepcopy(assigned.molecular_mechanics.partial_charge_assignment)
    prepared = prepare(assigned, selection='all')
    report = dmt.audit_preparation_charges(prepared)
    assert report['assessment'] == 'consistent'
    assert report['charge_unit'] == 'elementary_charge'
    assert report['matches_preparation_values'] is True
    assert report['total_charge'] == pytest.approx(0, abs=1e-12)
    model = report['partial_charge_assignment']
    assert model['method'] == 'gasteiger_marsili'
    assert model['software'] == assignment['software']
    assert model['references'] == assignment['references']
    assert model['parameters']['iterations'] == 12
    assert model['n_atoms'] == 6 and model['coverage'] == 'complete'
    projection = report['charge_projection']
    assert projection['selected_source_atom_indices'] == list(range(6))
    assert projection['retained_source_atom_indices'] == [0, 1, 5]
    assert projection['transfers'] == [
        {
            'omitted_source_atom_index': i,
            'recipient_source_atom_index': 0,
            'charge': before[i],
        }
        for i in (2, 3, 4)
    ]
    np.testing.assert_allclose(
        prepared.charges, [fsum(before[[0, 2, 3, 4]]), before[1], before[5]]
    )
    np.testing.assert_array_equal(atom_charges(assigned), before)
    assert (
        assigned.molecular_mechanics.partial_charge_assignment['status'] == 'assigned'
    )
    assert prepared.atom_types == ['C', 'OA', 'HD']
    assert dmt.assess_preparation(prepared)['provisional_reason_codes'] == [
        'heuristic_atom_types'
    ]
    assert report['pdbqt']['charges'] == written_charges(prepared)
    assert (
        abs(report['pdbqt']['rounding_difference'])
        <= report['pdbqt']['total_rounding_bound']
    )
    # Native retained-source values have not been silently replaced with the
    # consumer's united-atom values or attributed to a new provider calculation.
    np.testing.assert_array_equal(
        atom_charges(prepared.to_molecular_system()), before[[0, 1, 5]]
    )
    json.dumps(prepared.to_dict(), allow_nan=False)
    json.dumps(report, allow_nan=False)
    report['partial_charge_assignment']['software']['molsysmt'] = 'edited'
    assert (
        prepared.metadata['partial_charge_assignment']['software']
        == assignment['software']
    )


def test_receptor_forcefield_total_and_rounding_are_separate(tmp_path):
    source = msm.convert(
        msm.systems['chicken villin HP35']['1vii.pdb'], to_form='molsysmt.MolSys'
    )
    assigned = msm.build.assign_partial_charges(
        source, method='forcefield', forcefield='AMBER14', expected_total_charge=2
    )
    prepared = dmt.prepare_receptor(assigned, selection='all')
    report = dmt.audit_preparation_charges(prepared)
    assert not msm.has_attribute(source, 'partial_charge')
    assert report['assessment'] == 'consistent'
    assert report['n_atoms'] == 364
    assert len(report['charge_projection']['transfers']) == 232
    assert report['total_charge'] == pytest.approx(2, abs=1e-12)
    model = report['partial_charge_assignment']
    assert model['n_atoms'] == 596 and model['expected_total_charge'] == 2
    assert model['method'] == 'forcefield' and model['engine'] == 'OpenMM'
    assert model['parameters']['forcefield'] == 'AMBER14'
    assert report['pdbqt']['charges'] == written_charges(prepared)
    assert (
        abs(report['pdbqt']['rounding_difference'])
        <= report['pdbqt']['total_rounding_bound']
    )
    from vina import Vina

    receptor_file = tmp_path / 'named-receptor.pdbqt'
    receptor_file.write_text(prepared.to_pdbqt())
    Vina(cpu=1, verbosity=0).set_receptor(str(receptor_file))
    # Export precision is an observation, never silently renormalized to +2.
    assert report['pdbqt']['total_charge'] == pytest.approx(
        fsum(written_charges(prepared))
    )


def test_projected_inventory_retains_original_calculation_scope(assigned):
    before = atom_charges(assigned)
    projected = msm.extract(assigned, selection=[1, 5])
    prepared = dmt.prepare_ligand(projected, selection='all')
    report = dmt.audit_preparation_charges(prepared)
    assert report['assessment'] == 'consistent'
    assert report['partial_charge_assignment']['n_atoms'] == 6
    assert report['partial_charge_assignment']['total_charge'] == pytest.approx(
        0, abs=1e-12
    )
    projection = report['charge_projection']
    assert projection['selected_source_atom_indices'] == [1, 5]
    assert projection['retained_source_atom_indices'] == [1, 5]
    assert projection['transfers'] == []
    assert report['total_charge'] == pytest.approx(before[1] + before[5])
    assert abs(report['total_charge']) > 0.1


@pytest.mark.parametrize('mutation', ['charges', 'chemistry'])
@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_provider_marks_stale_assignment_and_consumer_rejects(
    assigned, mutation, prepare
):
    # Deliberately bypass public setters to exercise the provider's stale-binding
    # guard. Production code never manipulates molecular tables this way.
    if mutation == 'charges':
        assigned.molecular_mechanics.atoms_ff.loc[0, 'partial_charge'] += 0.01
    else:
        assigned.topology.atoms.loc[0, 'atom_type'] = 'N'
    with pytest.raises(ArgumentError, match='stale'):
        prepare(assigned, selection='all')


def test_coordinate_change_preserves_graph_charge_attribution(assigned):
    coords = msm.get(assigned, coordinates=True)
    msm.set(assigned, coordinates=coords + puw.quantity(1, 'nm'))
    assert (
        dmt.audit_preparation_charges(dmt.prepare_ligand(assigned, selection='all'))[
            'assessment'
        ]
        == 'consistent'
    )


def test_manual_charge_replacement_drops_named_attribution(assigned, monkeypatch):
    msm.set(assigned, partial_charge=[0.1] * 6)

    def forbid(*args, **kwargs):
        raise AssertionError('No implicit charge calculation is authorized.')

    monkeypatch.setattr(msm.physchem, 'get_partial_charges', forbid)
    monkeypatch.setattr(msm.build, 'assign_partial_charges', forbid)
    prepared = dmt.prepare_ligand(assigned, selection='all')
    report = dmt.audit_preparation_charges(prepared)
    assert report['assessment'] == 'unassessed'
    assert report['partial_charge_assignment'] is None
    assert report['charge_projection'] is None
    assert report['total_charge'] == pytest.approx(0.6)
    assert not prepared.to_pdbqt().startswith('REMARK DOCKINGMT_PARTIAL_CHARGES')


def test_nondefault_charge_units_do_not_change_consumed_values():
    source = msm.convert(METHANOL, to_form='molsysmt.MolSys')
    with puw.context(standard_units=['coulomb', 'pm']):
        assigned = msm.build.assign_partial_charges(source, method='gasteiger_marsili')
        prepared = dmt.prepare_ligand(assigned, selection='all')
        report = dmt.audit_preparation_charges(prepared)
    assert prepared.charges == pytest.approx(
        [0.19000057917, -0.39963024356, 0.20962966439], abs=1e-10
    )
    assert report['charge_unit'] == 'elementary_charge'
    assert report['pdbqt']['charges'] == [0.19, -0.4, 0.21]


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_changed_prepared_values_are_reported_and_not_exported_as_named(
    assigned, prepare
):
    prepared = prepare(assigned, selection='all')
    # Same total: conservation alone cannot detect exchanged atomic charges.
    prepared.charges[0] += 0.01
    prepared.charges[1] -= 0.01
    report = dmt.audit_preparation_charges(prepared)
    assert report['assessment'] == 'inconsistent'
    assert report['matches_preparation_values'] is False
    with pytest.raises(ArgumentError, match='no longer match'):
        prepared.to_pdbqt()


@pytest.mark.parametrize('charges', [[0], [float('nan')] * 3, [float('inf')] * 3])
def test_audit_rejects_incomplete_or_nonfinite_values(assigned, charges):
    prepared = dmt.prepare_ligand(assigned, selection='all')
    prepared.charges = charges
    with pytest.raises(ArgumentError, match='complete and finite'):
        dmt.audit_preparation_charges(prepared)


def test_named_remark_and_result_provenance_pass_real_vina_without_lifting_gate(
    assigned,
):
    prepared = dmt.prepare_ligand(assigned, selection='all')
    problem = dmt.DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=prepared,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
    )
    with pytest.raises(ArgumentError, match='heuristic'):
        dmt.dock(problem, dmt.VinaProtocol(cpu=1, n_poses=1, exhaustiveness=1))
    result = dmt.dock(
        problem,
        dmt.VinaProtocol(
            cpu=1,
            seed=17,
            n_poses=1,
            exhaustiveness=1,
            allow_provisional_preparation=True,
            capture_backend_inputs=True,
        ),
    )
    restored = dmt.DockingResult.from_dict(
        json.loads(json.dumps(result.to_dict(), allow_nan=False))
    )
    metadata = restored.provenance['preparation']['partner']['metadata']
    assert (
        metadata['partial_charge_assignment']
        == prepared.metadata['partial_charge_assignment']
    )
    assert metadata['charge_projection'] == prepared.metadata['charge_projection']
    assert restored.provenance['preparation']['partner']['assessment'] == 'provisional'
    assert len(restored.poses) == 1


def test_flexible_sdf_charge_export_follows_verified_tree_order():
    source = msm.convert(
        METHANOL.parents[1] / 'vina_torsions/5x72_ligand_p59H.sdf',
        to_form='molsysmt.MolSys',
        stereo_engine='rdkit',
        discard_properties=True,
    )
    assigned = msm.build.assign_partial_charges(source, method='gasteiger_marsili')
    before = atom_charges(assigned).copy()
    prepared = dmt.prepare_ligand(
        assigned, selection='all', active_torsion_bonds=[(6, 7), (17, 18)]
    )
    report = dmt.audit_preparation_charges(prepared)
    expected = [
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        24,
        6,
        0,
        1,
        2,
        3,
        4,
        5,
        18,
        19,
        20,
        21,
        22,
        23,
    ]
    assert report['assessment'] == 'consistent'
    assert prepared.pdbqt_atom_indices == expected
    assert report['pdbqt']['prepared_atom_indices'] == expected
    retained = list(range(24)) + [29]
    assert report['pdbqt']['source_atom_indices'] == [retained[i] for i in expected]
    assert report['pdbqt']['charges'] == written_charges(prepared)
    assert report['total_charge'] == pytest.approx(0, abs=1e-12)
    assert prepared.torsion_dof == 2
    np.testing.assert_array_equal(atom_charges(assigned), before)
    from vina import Vina

    Vina(cpu=1, verbosity=0).set_ligand_from_string(prepared.to_pdbqt())


@pytest.mark.parametrize(
    'mutate',
    [
        lambda m: m.update(partial_charge_assignment={'schema': 'unknown'}),
        lambda m: m.update(charge_projection=None),
        lambda m: m['charge_projection'].update(charge_unit='coulomb'),
        lambda m: m['charge_projection'].update(total_charge_tolerance=1),
        lambda m: m['charge_projection'].update(selected_total_charge=float('nan')),
    ],
)
def test_audit_rejects_mutated_evidence_atomically(assigned, mutate):
    prepared = dmt.prepare_ligand(assigned, selection='all')
    mutate(prepared.metadata)
    with pytest.raises(ArgumentError):
        dmt.audit_preparation_charges(prepared)
    with pytest.raises(ArgumentError):
        prepared.to_pdbqt()


def test_charge_audit_reads_only_prepared_numeric_evidence(assigned, monkeypatch):
    prepared = dmt.prepare_ligand(assigned, selection='all')

    def forbid(*args, **kwargs):
        raise AssertionError('Audit must not read molecular chemistry or render PDBQT.')

    for name in ('get', 'convert', 'extract'):
        monkeypatch.setattr(msm, name, forbid)
    monkeypatch.setattr(prepared, 'to_pdbqt', forbid)
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'
