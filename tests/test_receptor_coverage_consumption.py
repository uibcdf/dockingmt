"""Qualify residue evidence without admitting provisional receptor chemistry."""

import hashlib
import json
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_flexible_ligand import _ligand

from dockingmt import prepare_ligand, prepare_receptor
from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._molsys import chemistry_evidence

SOURCE_1IEP = Path(__file__).parent / 'data/vina_torsions/1iep_receptorH.pdb'
SHA256_1IEP = '5f6aee6029f9a2a2c2be32d4eb948ae70808690573e1b69a0850cdffd7048ca7'


def _controls():
    builder = msm.MolSysBuilder()
    # Exact inventories, including an intentionally absent ALA CB and unknown PTR.
    specifications = [
        ('ALA', ['N', 'CA', 'C', 'O', 'CB'], ['N', 'C', 'C', 'O', 'C']),
        ('ALA', ['N', 'CA', 'C', 'O'], ['N', 'C', 'C', 'O']),
        (
            'MSE',
            ['N', 'CA', 'C', 'O', 'CB', 'CG', 'SE', 'CE'],
            ['N', 'C', 'C', 'O', 'C', 'C', 'Se', 'C'],
        ),
        (
            'SEP',
            ['N', 'CA', 'C', 'O', 'CB', 'OG', 'P', 'O1P', 'O2P', 'O3P'],
            ['N', 'C', 'C', 'O', 'C', 'O', 'P', 'O', 'O', 'O'],
        ),
        ('PTR', ['N'], ['N']),
        ('HOH', ['O'], ['O']),
        ('ZN', ['ZN'], ['Zn']),
    ]
    edges = [
        ('N', 'CA'),
        ('CA', 'C'),
        ('C', 'O'),
        ('CA', 'CB'),
        ('CB', 'CG'),
        ('CG', 'SE'),
        ('SE', 'CE'),
        ('CB', 'OG'),
        ('OG', 'P'),
        ('P', 'O1P'),
        ('P', 'O2P'),
        ('P', 'O3P'),
    ]
    count = 0
    for group_id, (name, atoms, elements) in enumerate(specifications, start=1):
        indices = {
            atom: builder.add_atom(atom_name=atom, atom_type=element)
            for atom, element in zip(atoms, elements)
        }
        builder.add_group(list(indices.values()), group_name=name, group_id=group_id)
        for first, second in edges:
            if first in indices and second in indices:
                builder.add_bond(
                    indices[first],
                    indices[second],
                    bond_order=2 if second in ('O', 'O1P') else 1,
                    bond_type='covalent',
                )
        count += len(atoms)
    builder.set_coordinates(puw.quantity(np.zeros((1, count, 3)), 'nm'))
    return builder.build()


@pytest.mark.parametrize(
    'case,n_atoms,n_groups,unassessed',
    [
        ('181L', 1441, 302, 140),
        ('1IEP', 4412, 274, 0),
    ],
)
def test_original_receptors_distinguish_inventory_from_preparation(
    case, n_atoms, n_groups, unassessed
):
    path = (
        msm.systems['T4 lysozyme L99A']['181l.pdb']
        if case == '181L'
        else str(SOURCE_1IEP)
    )
    before = Path(path).read_bytes()
    if case == '1IEP':
        assert hashlib.sha256(before).hexdigest() == SHA256_1IEP
    source = msm.convert(path, to_form='molsysmt.MolSys')
    evidence = chemistry_evidence(source, include_residue_coverage=True)
    summary = evidence['residue_coverage']
    assert evidence['chemical_readiness']['n_atoms'] == n_atoms
    assert summary['n_groups'] == msm.get(source, n_groups=True) == n_groups
    assert summary['status_counts'] == {
        'assessed': n_groups - unassessed,
        'incomplete': 0,
        'unassessed': unassessed,
    }
    assert summary['check_status_counts']['hydrogens'] == {'unassessed': n_groups}
    assert summary['check_status_counts']['protonation'] == {'unassessed': n_groups}
    assert 'docking_readiness' in summary['unassessed_checks']
    assert 'ready' not in summary
    if case == '1IEP':
        with pytest.raises(ArgumentError, match='exactly one explicit heavy-atom bond'):
            prepare_receptor(source, selection="molecule_type=='protein'")
    else:
        protein = prepare_receptor(source, selection="molecule_type=='protein'")
        assert protein.metadata['source_chemistry']['residue_coverage'][
            'status_counts'
        ] == {
            'assessed': 162,
            'incomplete': 0,
            'unassessed': 0,
        }
        assert protein.metadata['charge_source'] == 'zero_placeholder'
    assert Path(path).read_bytes() == before


def test_grouped_receptor_reuses_provider_audit_before_hydrogen_projection(monkeypatch):
    source = _ligand('CCO')
    builder = msm.MolSysBuilder(source)
    builder.add_group(list(range(9)), group_name='UNK', group_id=1)
    source = builder.build()
    reports = []
    provider = msm.build.get_residue_chemical_coverage

    def recorded(molecular_system, **kwargs):
        assert kwargs == {'chemical_state': 'structure', 'structure_indices': 0}
        reports.append(provider(molecular_system, **kwargs))
        return reports[-1]

    def redundant(*args, **kwargs):
        pytest.fail('The embedded chemical-readiness report must be reused.')

    monkeypatch.setattr(msm.build, 'get_residue_chemical_coverage', recorded)
    monkeypatch.setattr(msm.physchem, 'get_chemical_readiness', redundant)
    prepared = prepare_receptor(source, selection='all')
    assert len(reports) == 1
    assert prepared.n_atoms == 4
    assert prepared.metadata['source_chemistry']['chemical_readiness']['n_atoms'] == 9
    summary = prepared.metadata['source_chemistry']['residue_coverage']
    assert summary['group_axis'] == 'selected_source_before_hydrogen_projection'
    assert summary['status_counts'] == {'assessed': 0, 'incomplete': 0, 'unassessed': 1}
    assert 'groups' not in summary and 'group_indices' not in summary
    assert (
        json.loads(json.dumps(prepared.to_dict()))['metadata']['source_chemistry']
        == prepared.metadata['source_chemistry']
    )


def test_incomplete_modified_unknown_water_and_metal_are_not_parent_substituted():
    source = _controls()
    summary = chemistry_evidence(source, include_residue_coverage=True)[
        'residue_coverage'
    ]
    assert summary['status_counts'] == {'assessed': 3, 'incomplete': 1, 'unassessed': 3}
    assert summary['reason_counts']['missing_heavy_atoms'] == 1
    assert summary['reason_counts']['no_exact_residue_template'] == 3
    assert summary['check_status_counts']['protonation'] == {'unassessed': 7}
    assert summary['check_status_counts']['hydrogens'] == {'unassessed': 7}
    assert set(summary['template_usage']) == {'ALA', 'MSE', 'SEP'}
    assert summary['template_usage']['ALA']['n_groups'] == 2
    for template in summary['template_usage'].values():
        assert len(template['packaged_sha256']) == 64
    assert (
        'MET' not in summary['template_usage']
        and 'TYR' not in summary['template_usage']
    )
    full = msm.build.get_residue_chemical_coverage(source)
    assert full['groups'][1]['heavy_atoms']['missing_atom_names'] == ['CB']
    assert full['groups'][2]['hydrogens']['reason_code'] == 'heavy_only_template'
    assert 'SE' in full['groups'][2]['heavy_atoms']['expected_atom_names']
    assert 'SD' not in full['groups'][2]['heavy_atoms']['expected_atom_names']
    assert full['groups'][3]['hydrogens']['reason_code'] == 'heavy_only_template'
    assert full['groups'][4]['template'] is None
    for group_name, element in [('MSE', 'Se'), ('ZN', 'Zn')]:
        selected = msm.extract(source, selection=f"group_name=='{group_name}'")
        with pytest.raises(ArgumentError, match=f"rule exists for element '{element}'"):
            prepare_receptor(selected, selection='all')


def test_residue_summary_is_detached_and_read_only_under_nondefault_units():
    source = _controls()
    states = msm.convert(
        source.chemical_states, to_form='molsysmt.ChemicalStatesDict'
    ).to_dict()
    with puw.context(standard_units=['pm', 'fs']):
        source.structures.coordinates = puw.convert(
            source.structures.coordinates, to_unit='angstrom'
        )
        unit = puw.get_unit(source.structures.coordinates)
        before = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
        evidence = chemistry_evidence(source, include_residue_coverage=True)
        assert evidence['chemical_readiness']['fields']['coordinates']['unit'] == 'nm'
        evidence['residue_coverage']['template_usage']['MSE']['n_groups'] = 1000
        evidence['residue_coverage']['unassessed_checks'].clear()
        fresh = chemistry_evidence(source, include_residue_coverage=True)[
            'residue_coverage'
        ]
        assert fresh['template_usage']['MSE']['n_groups'] == 1
        assert 'repair_placement' in fresh['unassessed_checks']
        assert puw.get_unit(source.structures.coordinates) == unit
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit='nm'), before
        )
    np.testing.assert_equal(
        msm.convert(
            source.chemical_states, to_form='molsysmt.ChemicalStatesDict'
        ).to_dict(),
        states,
    )


def test_residue_audit_follows_structure_assigned_state():
    source = _controls()
    assigned = source.topology._append_chemical_state(state_id='incomplete')
    source.topology._set_chemical_state_bonds(
        source.topology.bonds.iloc[1:].copy(), state_index=assigned
    )
    source._set_structure_chemical_state_indices([assigned])
    evidence = chemistry_evidence(source, include_residue_coverage=True)
    assert evidence['chemical_readiness']['chemical_state_index'] == assigned
    assert evidence['residue_coverage']['status_counts']['incomplete'] == 2
    assert msm.build.get_residue_chemical_coverage(source)['summary']['incomplete'] == 1


def test_group_free_receptor_reports_unavailable_hierarchy_without_fabricating_groups():
    source = _ligand('CCO')
    prepared = prepare_receptor(source, selection='all')
    assert prepared.metadata['source_chemistry']['residue_coverage'] == {
        'status': 'unassessed',
        'reason_code': 'no_group_domain',
        'n_groups': 0,
        'group_axis': 'selected_source_before_hydrogen_projection',
    }
    assert msm.get(source, n_groups=True) == 0
    ligand = prepare_ligand(source, selection='all')
    assert 'residue_coverage' not in ligand.metadata['source_chemistry']


def test_provider_failure_propagates_without_a_local_fallback(monkeypatch):
    def unavailable(*args, **kwargs):
        raise RuntimeError('coverage provider unavailable')

    monkeypatch.setattr(msm.build, 'get_residue_chemical_coverage', unavailable)
    with pytest.raises(RuntimeError, match='coverage provider unavailable'):
        chemistry_evidence(_controls(), include_residue_coverage=True)
