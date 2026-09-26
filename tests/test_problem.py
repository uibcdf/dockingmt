import json
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.search_domain import BoxRegion


def test_docking_problem_construction():
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    problem = DockingProblem(
        receptor=msm.systems['T4 lysozyme L99A']['181l.pdb'],
        partner=msm.systems['T4 lysozyme L99A']['181l.pdb'],
        search_domain=box,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
        metadata={'ligand_id': 'BENZENE', 'receptor_state_id': '181L_A'},
    )

    assert problem.receptor == msm.systems['T4 lysozyme L99A']['181l.pdb']
    assert problem.partner == problem.receptor
    assert msm.get_form(problem.receptor_molsys) == 'molsysmt.MolSys'
    assert msm.get_form(problem.partner_molsys) == 'molsysmt.MolSys'
    assert msm.get(problem.partner_molsys, element='system', n_atoms=True) == 6
    assert problem.partner_atom_indices == [1299, 1300, 1301, 1302, 1303, 1304]
    assert problem.receptor_structure_index == 0
    assert problem.partner_structure_index == 0
    assert problem.search_domain is box
    assert problem.metadata['ligand_id'] == 'BENZENE'
    assert problem.metadata['receptor_state_id'] == '181L_A'
    assert 'DockingProblem' in repr(problem)


def test_redocking_factory_uses_selected_partner_for_box():
    source = msm.systems['T4 lysozyme L99A']['181l.pdb']
    problem = DockingProblem.for_redocking(
        source,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
        padding=puw.quantity(8.0, 'angstrom'),
    )
    expected = BoxRegion.from_selection(
        problem.partner_molsys, padding=puw.quantity(8.0, 'angstrom')
    )
    np.testing.assert_allclose(
        puw.get_value(problem.search_domain.center),
        puw.get_value(expected.center),
    )
    np.testing.assert_allclose(
        puw.get_value(problem.search_domain.size),
        puw.get_value(expected.size),
    )
    assert problem.partner_atom_indices == [1299, 1300, 1301, 1302, 1303, 1304]
    assert problem.receptor_structure_index == problem.partner_structure_index == 0


def _multi_structure_redocking_source():
    path = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    molsys = msm.convert(path, to_form='molsysmt.MolSys')
    msm.append_structures(molsys, msm.copy(molsys))
    coordinates = np.array(
        puw.get_value(
            msm.get(molsys, element='atom', coordinates=True), to_unit='angstrom'
        ),
        copy=True,
    )
    coordinates[1] += [20.0, 0.0, 0.0]
    molsys.structures.coordinates = puw.quantity(coordinates, 'angstrom')
    second_state = molsys.topology._append_chemical_state(
        state_id='selected-second-state'
    )
    molsys._set_structure_chemical_state_indices([0, second_state])
    return molsys, coordinates


def test_redocking_factory_requires_explicit_multi_structure_choice():
    molsys, _ = _multi_structure_redocking_source()

    with pytest.raises(ArgumentError, match='choose structure_index'):
        DockingProblem.for_redocking(
            molsys,
            receptor_selection=[0, 1],
            partner_selection=[2, 3],
            padding=puw.quantity(2.0, 'angstrom'),
        )


def test_redocking_factory_uses_selected_structure_for_molecules_box_and_state():
    molsys, source_coordinates = _multi_structure_redocking_source()
    kwargs = {
        'receptor_selection': [0, 1],
        'partner_selection': [2, 3],
        'padding': puw.quantity(2.0, 'angstrom'),
    }
    first = DockingProblem.for_redocking(molsys, structure_index=0, **kwargs)
    second = DockingProblem.for_redocking(molsys, structure_index=1, **kwargs)

    assert second.receptor_structure_index == second.partner_structure_index == 1
    assert second.receptor_atom_indices == [0, 1]
    assert second.partner_atom_indices == [2, 3]
    np.testing.assert_allclose(
        puw.get_value(
            msm.get(second.receptor_molsys, element='atom', coordinates=True),
            to_unit='angstrom',
        )[0],
        source_coordinates[1, [0, 1]],
    )
    np.testing.assert_allclose(
        puw.get_value(
            msm.get(second.partner_molsys, element='atom', coordinates=True),
            to_unit='angstrom',
        )[0],
        source_coordinates[1, [2, 3]],
    )
    np.testing.assert_allclose(
        puw.get_value(second.search_domain.center, to_unit='angstrom')
        - puw.get_value(first.search_domain.center, to_unit='angstrom'),
        [20.0, 0.0, 0.0],
    )
    assert all(
        second.search_domain.contains(puw.quantity(point, 'angstrom'))
        for point in source_coordinates[1, [2, 3]]
    )
    assert all(
        not second.search_domain.contains(puw.quantity(point, 'angstrom'))
        for point in source_coordinates[0, [2, 3]]
    )
    recorded = second.to_dict()
    assert all(
        recorded['molecular_inputs'][role]['chemical_state_id']
        == 'selected-second-state'
        for role in ('receptor', 'partner')
    )
    reconstructed = DockingProblem.from_dict(recorded, receptor=molsys, partner=molsys)
    assert reconstructed.receptor_structure_index == 1
    assert reconstructed.partner_structure_index == 1
    assert reconstructed.search_domain.to_dict() == recorded['search_domain']


def test_molsys_input_and_structure_selection():
    path = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    molsys = msm.convert(path, to_form='molsysmt.MolSys')
    msm.append_structures(molsys, msm.copy(molsys))
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )

    with pytest.raises(ArgumentError, match='choose receptor_structure_index'):
        DockingProblem(receptor=molsys, partner=molsys, search_domain=box)

    problem = DockingProblem(
        receptor=molsys,
        partner=molsys,
        search_domain=box,
        receptor_selection=[2, 1, 0],
        partner_selection=[4, 3],
        receptor_structure_index=1,
        partner_structure_index=0,
    )
    assert msm.get(problem.receptor_molsys, element='system', n_atoms=True) == 3
    assert msm.get(problem.partner_molsys, element='system', n_atoms=True) == 2
    assert problem.receptor_atom_indices == [0, 1, 2]
    assert problem.partner_atom_indices == [3, 4]
    assert problem.receptor_structure_index == 1
    assert problem.partner_structure_index == 0
    assert msm.get(problem.partner_molsys, element='atom', name=True) == msm.get(
        molsys, element='atom', selection=[3, 4], name=True
    )


def test_selected_input_roundtrip_records_provenance():
    path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    problem = DockingProblem(
        receptor=path,
        partner=path,
        search_domain=box,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
    )
    serialized = problem.to_dict()
    json.dumps(serialized)
    assert serialized['molecular_inputs']['receptor']['form'] == 'file:pdb'
    assert serialized['molecular_inputs']['partner']['atom_indices'] == [
        1299,
        1300,
        1301,
        1302,
        1303,
        1304,
    ]
    reconstructed = DockingProblem.from_dict(serialized)
    assert reconstructed.partner_atom_indices == problem.partner_atom_indices
    assert reconstructed.receptor_selection == problem.receptor_selection
    changed_selection = json.loads(json.dumps(serialized))
    changed_selection['molecular_inputs']['partner']['atom_indices'] = [0]
    with pytest.raises(
        ArgumentError, match='differs from the recorded molecular selection'
    ):
        DockingProblem.from_dict(changed_selection)
    assert serialized['molecular_inputs']['partner']['chemical_state_index'] == 0
    report = serialized['molecular_inputs']['partner']['conversion_report']
    assert report['outcome'] == 'lossy'
    assert any(issue['attribute'] == 'bond_order' for issue in report['issues'])


def test_reconstruction_rejects_changed_source_file(tmp_path):
    source = Path(msm.systems['T4 lysozyme L99A']['181l.pdb'])
    local = tmp_path / 'complex.pdb'
    local.write_bytes(source.read_bytes())
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    problem = DockingProblem(
        receptor=local,
        partner=local,
        search_domain=box,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
    )
    manifest = problem.to_dict()
    assert (
        manifest['molecular_inputs']['partner']['source_fingerprint']['kind'] == 'file'
    )
    local.write_bytes(local.read_bytes() + b'REMARK changed\n')
    with pytest.raises(ArgumentError, match='source content has changed'):
        DockingProblem.from_dict(manifest)


def test_problem_selects_chemistry_of_chosen_structure():
    molsys = msm.native.MolSys(n_atoms=2)
    molsys.topology.atoms['atom_id'] = ['0', '1']
    molsys.topology.atoms['atom_name'] = ['C', 'O']
    molsys.topology.atoms['atom_type'] = ['C', 'O']
    molsys.topology._set_chemical_state_atom_attribute('formal_charge', [0, -1])
    product = molsys.topology._append_chemical_state(state_id='product')
    molsys.topology._set_chemical_state_atom_attribute(
        'formal_charge', [1, 0], state_index=product
    )
    molsys.topology._set_reference_chemical_state_index(None)
    molsys.structures.coordinates = puw.quantity(np.zeros((2, 2, 3)), 'nm')
    molsys._set_structure_chemical_state_indices([0, 1])
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    problem = DockingProblem(
        receptor=molsys,
        partner=molsys,
        search_domain=box,
        receptor_selection='formal_charge==-1',
        partner_selection='formal_charge==1',
        receptor_structure_index=0,
        partner_structure_index=1,
    )
    assert problem.receptor_atom_indices == [1]
    assert problem.partner_atom_indices == [0]
    assert problem.receptor_chemical_state_index == 0
    assert problem.partner_chemical_state_index == 1
    assert (
        problem.to_dict()['molecular_inputs']['partner']['chemical_state_id']
        == 'product'
    )

    molsys._set_structure_chemical_state_indices([0, None])
    with pytest.raises(ArgumentError, match='no resolved chemical-state association'):
        DockingProblem(
            receptor=molsys,
            partner=molsys,
            search_domain=box,
            receptor_structure_index=0,
            partner_structure_index=1,
        )


def test_pdb_text_is_normalized_as_molecular_input():
    path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    atom_lines = [
        line for line in Path(path).read_text().splitlines() if line.startswith('ATOM')
    ][:2]
    pdb_text = '\n'.join([*atom_lines, 'END', ''])
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    problem = DockingProblem(
        receptor=pdb_text,
        partner=pdb_text,
        search_domain=box,
    )
    assert problem.receptor_molsys is not None
    assert problem.partner_molsys is not None
    assert (
        problem.to_dict()['molecular_inputs']['receptor']['form'] == 'string:pdb_text'
    )


def test_molsys_object_roundtrip_requires_original_objects():
    molsys = msm.convert(
        msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
        to_form='molsysmt.MolSys',
    )
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    problem = DockingProblem(
        receptor=molsys,
        partner=molsys,
        search_domain=box,
        partner_selection=[3, 4],
    )
    serialized = problem.to_dict()
    json.dumps(serialized)
    with pytest.raises(ArgumentError, match='explicit receptor and partner'):
        DockingProblem.from_dict(serialized)
    reconstructed = DockingProblem.from_dict(
        serialized, receptor=molsys, partner=molsys
    )
    assert reconstructed.partner_atom_indices == [3, 4]


def test_molecular_input_errors_before_docking():
    path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )
    with pytest.raises(ArgumentError, match='partner_selection selected no atoms'):
        DockingProblem(
            receptor=path,
            partner=path,
            search_domain=box,
            partner_selection="group_name=='NOT_PRESENT'",
        )
    with pytest.raises(ArgumentError, match='receptor_structure_index'):
        DockingProblem(
            receptor=path, partner=path, search_domain=box, receptor_structure_index=7
        )
    with pytest.raises(ArgumentError, match='Cannot select a MolSysMT'):
        DockingProblem(receptor='missing_receptor.pdb', partner=path, search_domain=box)


def test_docking_problem_validation_errors():
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([2.0, 2.0, 2.0], 'nm'),
    )

    with pytest.raises(ArgumentError) as exc:
        DockingProblem(receptor=None, partner='ligand.pdb', search_domain=box)
    assert 'receptor' in str(exc.value)

    with pytest.raises(ArgumentError) as exc:
        DockingProblem(receptor='rec.pdb', partner=None, search_domain=box)
    assert 'partner' in str(exc.value)

    with pytest.raises(ArgumentError) as exc:
        DockingProblem(
            receptor='rec.pdb', partner='ligand.pdb', search_domain='not_a_domain'
        )  # type: ignore
    assert 'search_domain' in str(exc.value)


def test_docking_problem_serialization():
    box = BoxRegion(
        center=puw.quantity([1.0, 2.0, 3.0], 'angstrom'),
        size=puw.quantity([15.0, 15.0, 15.0], 'angstrom'),
    )
    problem = DockingProblem(
        receptor='rec.pdbqt',
        partner='lig.pdbqt',
        search_domain=box,
        constraints=[{'type': 'distance', 'val': 2.5}],
        search_guidance=[{'bias': 'pocket_mouth'}],
        metadata={'test_run': True},
    )

    d = problem.to_dict()
    assert d['schema_version'] == '1.0'
    assert d['receptor']['value'] == 'rec.pdbqt'
    assert d['partner']['value'] == 'lig.pdbqt'
    assert d['metadata']['test_run'] is True

    # Reconstruct
    reconstructed = DockingProblem.from_dict(d)
    assert reconstructed.receptor == 'rec.pdbqt'
    assert reconstructed.partner == 'lig.pdbqt'
    assert reconstructed.metadata['test_run'] is True
    assert isinstance(reconstructed.search_domain, BoxRegion)
    assert float(puw.get_value(reconstructed.search_domain.center)[0]) == pytest.approx(
        0.1
    )  # converted to nm
