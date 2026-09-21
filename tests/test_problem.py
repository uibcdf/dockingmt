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
        receptor='dummy_receptor.pdb',
        partner='dummy_ligand.pdb',
        search_domain=box,
        metadata={'ligand_id': 'BENZENE', 'receptor_state_id': '181L_A'},
    )

    assert problem.receptor == 'dummy_receptor.pdb'
    assert problem.partner == 'dummy_ligand.pdb'
    assert problem.search_domain is box
    assert problem.metadata['ligand_id'] == 'BENZENE'
    assert problem.metadata['receptor_state_id'] == '181L_A'
    assert 'DockingProblem' in repr(problem)


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
