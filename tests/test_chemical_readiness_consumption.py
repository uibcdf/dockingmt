"""Stored chemistry coverage stays distinct from Vina preparation validity."""

import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_flexible_ligand import _ligand

from dockingmt.preparation import prepare_ligand, prepare_receptor
from dockingmt.preparation._molsys import chemistry_evidence


@pytest.mark.parametrize('prepare', [prepare_ligand, prepare_receptor])
def test_preparation_consumes_provider_on_source_before_projection(
    prepare, monkeypatch
):
    source = _ligand('CCO')
    reports = []
    provider = msm.physchem.get_chemical_readiness

    def recorded(molecular_system, **kwargs):
        assert kwargs == {'chemical_state': 'structure', 'structure_indices': 0}
        report = provider(molecular_system, **kwargs)
        reports.append(report)
        return report

    monkeypatch.setattr(msm.physchem, 'get_chemical_readiness', recorded)
    prepared = prepare(source, selection='all')
    assert len(reports) == 1
    original = reports[0]
    summary = prepared.metadata['source_chemistry']['chemical_readiness']
    assert summary['provider_schema'] == 'molsysmt.chemical_readiness@1'
    assert summary['atom_axis'] == 'selected_source_before_hydrogen_projection'
    assert summary['n_atoms'] == 9
    assert summary['n_explicit_hydrogens'] == 6
    assert prepared.n_atoms == 4
    assert summary['n_atoms'] == prepared.metadata['source_n_atoms']
    assert summary['structure_index'] == 0
    assert summary['chemical_state_index'] == original['chemical_state_index']
    assert summary['unassessed_checks'] == original['unassessed_checks']
    assert 'docking_readiness' in summary['unassessed_checks']
    assert 'charge_model' in summary['unassessed_checks']
    assert 'ready' not in summary
    for name, field in original['fields'].items():
        observed = summary['fields'][name]
        assert observed['status'] == field['status']
        for category in ('present', 'missing', 'unsupported', 'conflict'):
            assert observed[f'n_{category}'] == len(field[f'{category}_indices'])
        assert 'values' not in observed and 'indices' not in observed
        assert (
            'origin' not in observed
        )  # Origins are compact counts, not per-atom copies.
    assert summary['fields']['formal_charge']['status'] == 'present'
    assert summary['fields']['formal_charge']['origin_counts'] == {'unassessed': 9}
    assert prepared.metadata['charge_source'] == 'source_partial_charge'
    assert prepared.metadata['atom_type_source'] == 'molsysmt_named_autodock4'
    assert (
        json.loads(json.dumps(prepared.to_dict()))['metadata']['source_chemistry']
        == (prepared.metadata['source_chemistry'])
    )


def test_incomplete_pdb_coverage_is_reported_without_chemical_completion():
    source = msm.systems['T4 lysozyme L99A']['181l.pdb']
    from dockingmt._private.smonitor import ArgumentError

    with pytest.raises(
        ArgumentError, match='Named MolSysMT AutoDock4 types are required'
    ):
        prepare_ligand(source, selection="group_name=='BNZ'")
    selected = msm.extract(
        msm.convert(source, to_form='molsysmt.MolSys'), selection="group_name=='BNZ'"
    )
    summary = chemistry_evidence(selected)['chemical_readiness']
    assert summary['connectivity']['declared_completeness'] == 'partial'
    assert summary['fields']['formal_charge']['status'] == 'missing'
    assert summary['fields']['covalent_multiplicity']['status'] == 'missing'
    assert summary['fields']['coordinates']['status'] == 'present'
    assert summary['fields']['formal_charge']['n_missing'] == 6
    assert not msm.has_attribute(selected, 'partial_charge')


def test_summary_is_detached_and_preserves_chemical_source_and_coordinates():
    source = _ligand('CCO')
    before = msm.convert(
        source.chemical_states, to_form='molsysmt.ChemicalStatesDict'
    ).to_dict()
    coordinates = np.array(
        puw.get_value(msm.get(source, element='atom', coordinates=True), to_unit='nm'),
        copy=True,
    )
    summary = chemistry_evidence(source)['chemical_readiness']
    summary['fields']['formal_charge']['n_present'] = 1000
    summary['unassessed_checks'].clear()
    np.testing.assert_equal(
        msm.convert(
            source.chemical_states, to_form='molsysmt.ChemicalStatesDict'
        ).to_dict(),
        before,
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, element='atom', coordinates=True), to_unit='nm'),
        coordinates,
    )
    fresh = chemistry_evidence(source)['chemical_readiness']
    assert fresh['fields']['formal_charge']['n_present'] == 9
    assert 'docking_readiness' in fresh['unassessed_checks']


def test_assessment_uses_structure_state_and_reports_partial_formal_charge():
    source = _ligand('CCO')
    assigned = source.topology._append_chemical_state(state_id='assigned')
    source.topology._set_chemical_state_bonds(
        source.topology.bonds.copy(), state_index=assigned
    )
    source.topology._set_chemical_state_atom_attribute(
        'formal_charge', [0, None, -1, 0, 0, 0, 0, 0, 0], state_index=assigned
    )
    source.topology._chemical_states[assigned].connectivity_completeness = 'partial'
    source._set_structure_chemical_state_indices([assigned])
    summary = chemistry_evidence(source)['chemical_readiness']
    assert summary['chemical_state_index'] == assigned
    assert summary['chemical_state_status'] == 'resolved'
    assert summary['fields']['formal_charge']['status'] == 'partial'
    assert summary['fields']['formal_charge']['n_missing'] == 1
    assert summary['connectivity']['declared_completeness'] == 'partial'
    assert (
        msm.physchem.get_chemical_readiness(source)['fields']['formal_charge']['status']
        == 'present'
    )  # The reference state differs from the selected frame.


def test_coverage_under_nondefault_unit_policy_preserves_unit_and_source():
    source = _ligand('CCO')
    expected = chemistry_evidence(source)['chemical_readiness']
    with puw.context(standard_units=['pm', 'fs']):
        source.structures.coordinates = puw.convert(
            source.structures.coordinates, to_unit='angstrom'
        )
        unit_before = puw.get_unit(source.structures.coordinates)
        values_before = puw.get_value(
            source.structures.coordinates, to_unit='nm'
        ).copy()
        observed = chemistry_evidence(source)['chemical_readiness']
        assert observed == expected
        assert observed['fields']['coordinates']['unit'] == 'nm'
        assert observed['fields']['formal_charge']['unit'] == 'elementary_charge'
        assert puw.get_unit(source.structures.coordinates) == unit_before
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit='nm'), values_before
        )


def test_conflicting_coordinates_are_reported_without_repair():
    source = _ligand('CCO')
    coordinates = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    coordinates[0, 2, 0] = np.nan
    source.structures.coordinates = puw.quantity(coordinates, 'nm')
    summary = chemistry_evidence(source)['chemical_readiness']
    assert summary['fields']['coordinates']['status'] == 'conflict'
    assert summary['fields']['coordinates']['n_conflict'] == 1
    assert np.isnan(puw.get_value(source.structures.coordinates, to_unit='nm')[0, 2, 0])
