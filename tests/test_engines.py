import molsysmt as msm
import pytest
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError, CapabilityMismatchError
from dockingmt.core.problem import DockingProblem
from dockingmt.core.protocol import DockingProtocol, VinaProtocol
from dockingmt.core.results import DockingResult
from dockingmt.core.search_domain import BoxRegion
from dockingmt.dock import dock
from dockingmt.engines.vina import VinaBackend, _verify_pose_atom_order
from dockingmt.preparation import prepare_ligand, prepare_receptor


class DummyCustomProtocol(DockingProtocol):
    @property
    def name(self):
        return 'DummyCustomProtocol'

    @property
    def required_capabilities(self):
        return {'flexible_receptor', 'quantum_scoring'}

    @property
    def parameters(self):
        return {}

    def validate_problem(self, problem):
        pass

    def to_dict(self):
        return {}


def test_capability_validation():
    backend = VinaBackend()
    # Vina backend does not support flexible_receptor or quantum_scoring
    custom_proto = DummyCustomProtocol()
    with pytest.raises(CapabilityMismatchError) as exc:
        backend.validate_capabilities(custom_proto)
    assert 'not supported by engine' in str(exc.value)


MINIMAL_REC_PDBQT = """ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00     0.000 N
ATOM      2  CA  ALA A   1       1.458   0.000   0.000  1.00  0.00     0.000 C
ATOM      3  C   ALA A   1       2.009   1.428   0.000  1.00  0.00     0.000 C
ATOM      4  O   ALA A   1       1.246   2.392   0.000  1.00  0.00     0.000 OA
"""

MINIMAL_LIG_PDBQT = """ROOT
ATOM      1  C1  LIG A   1       0.000   0.000   0.000  1.00  0.00     0.000 C
ATOM      2  C2  LIG A   1       1.500   0.000   0.000  1.00  0.00     0.000 C
ENDROOT
TORSDOF 0
"""


def test_vina_backend_docking_execution():
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'angstrom'),
        size=puw.quantity([10.0, 10.0, 10.0], 'angstrom'),
    )

    problem = DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=MINIMAL_LIG_PDBQT,
        search_domain=box,
        metadata={
            'partner_state_id': 'lig_state_1',
            'receptor_state_id': 'rec_state_1',
        },
    )

    protocol = VinaProtocol(exhaustiveness=1, n_poses=2, seed=123)

    result = backend.dock(problem, protocol)

    assert isinstance(result, DockingResult)
    assert len(result) > 0
    top_pose = result.top_pose
    assert top_pose is not None
    assert top_pose.rank == 1
    assert top_pose.partner_state_id == 'lig_state_1'
    assert top_pose.receptor_state_id == 'rec_state_1'
    assert 'vina' in top_pose.scores
    assert puw.are_compatible(top_pose.coordinates, 'nm')
    assert top_pose.metadata['pose_atom_order'] == 'verified_pdbqt_order'

    # Provenance checks
    assert result.provenance['backend'] == 'vina'
    assert 'elapsed_seconds' in result.provenance
    assert result.provenance['seed'] == 123


def test_dock_top_level_api():
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'angstrom'),
        size=puw.quantity([10.0, 10.0, 10.0], 'angstrom'),
    )

    problem = DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=MINIMAL_LIG_PDBQT,
        search_domain=box,
    )

    protocol = VinaProtocol(exhaustiveness=1, n_poses=1, seed=42)

    # Calling top-level dockingmt.dock
    result = dock(problem, protocol=protocol, backend='vina')
    assert isinstance(result, DockingResult)
    assert len(result) >= 1
    assert result.provenance['backend'] == 'vina'


def test_dock_invalid_backend():
    box = BoxRegion(
        center=puw.quantity([0.0, 0.0, 0.0], 'nm'),
        size=puw.quantity([1.0, 1.0, 1.0], 'nm'),
    )
    problem = DockingProblem(
        receptor='rec.pdbqt', partner='lig.pdbqt', search_domain=box
    )

    with pytest.raises(ArgumentError):
        dock(problem, backend='nonexistent_engine')

    with pytest.raises(ArgumentError):
        dock(problem, backend=12345)  # type: ignore


def test_rdkit_ligand_with_explicit_hydrogens_has_pose_source_map():
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    pytest.importorskip('rdkit')
    from rdkit import Chem
    from rdkit.Chem import AllChem

    molecule = Chem.AddHs(Chem.MolFromSmiles('c1ccccc1'))
    assert AllChem.EmbedMolecule(molecule, randomSeed=7) == 0
    AllChem.ComputeGasteigerCharges(molecule)
    path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    complex_system = msm.convert(path, to_form='molsysmt.MolSys')
    native = msm.get(
        complex_system,
        element='atom',
        selection="group_name=='BNZ'",
        coordinates=True,
    )
    import numpy as np

    native_center = np.mean(puw.get_value(native, to_unit='angstrom')[0], axis=0)
    conformer = molecule.GetConformer()
    original = np.asarray(conformer.GetPositions())
    for i, xyz in enumerate(original - original.mean(axis=0) + native_center):
        conformer.SetAtomPosition(i, xyz)
    box = BoxRegion.from_selection(
        complex_system,
        selection="group_name=='BNZ'",
        padding=puw.quantity(8.0, 'angstrom'),
    )
    problem = DockingProblem(
        receptor=path,
        partner=molecule,
        search_domain=box,
        receptor_selection="molecule_type=='protein'",
    )
    result = backend.dock(
        problem,
        VinaProtocol(
            exhaustiveness=1,
            n_poses=1,
            cpu=1,
            seed=42,
            allow_provisional_preparation=True,
        ),
    )
    pose = result.top_pose
    assert pose.n_atoms == 6
    assert pose.metadata['selected_atom_indices'] == list(range(6))
    assert pose.metadata['source_atom_indices'] == list(range(6))
    assert pose.metadata['selected_partner_n_atoms'] == 12
    assert msm.get(pose.to_molecular_system(problem.partner_molsys), n_atoms=True) == 6
    from molsysviewer_dockingmt.adapters.complex import build_docking_complex_system

    complex_pose = build_docking_complex_system(
        problem.receptor_molsys, result.poses, partner=problem.partner_molsys
    )
    assert msm.get(complex_pose, n_atoms=True) == (
        msm.get(problem.receptor_molsys, n_atoms=True) + 6
    )


def test_vina_rejects_provisional_chemistry_from_automatic_and_prepared_inputs():
    backend = VinaBackend()
    if not backend.is_available:
        pytest.skip('Vina is not installed in the environment.')

    path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    box = BoxRegion.from_selection(
        path,
        selection="group_name=='BNZ'",
        padding=puw.quantity(8.0, 'angstrom'),
    )
    automatic = DockingProblem(
        receptor=path,
        partner=path,
        search_domain=box,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
    )
    with pytest.raises(ArgumentError, match='zero-placeholder partial charges'):
        backend.dock(automatic, VinaProtocol(exhaustiveness=1, n_poses=1))

    ligand = prepare_ligand(path, selection="group_name=='BNZ'")
    prepared = DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=ligand,
        search_domain=box,
    )
    with pytest.raises(ArgumentError, match='heuristic AutoDock atom types'):
        backend.dock(prepared, VinaProtocol(exhaustiveness=1, n_poses=1))

    receptor = prepare_receptor(path, selection="molecule_type=='protein'")
    prepared_receptor = DockingProblem(
        receptor=receptor,
        partner=MINIMAL_LIG_PDBQT,
        search_domain=box,
    )
    with pytest.raises(ArgumentError, match='zero-placeholder partial charges'):
        backend.dock(prepared_receptor, VinaProtocol(exhaustiveness=1, n_poses=1))

    result = backend.dock(
        prepared,
        VinaProtocol(
            exhaustiveness=1,
            n_poses=1,
            seed=42,
            allow_provisional_preparation=True,
        ),
    )
    assert result.provenance['preparation']['partner']['mode'] == 'provided'
    assert result.provenance['preparation']['partner']['assessment'] == 'provisional'


def test_vina_atom_order_verifier_rejects_permuted_pose():
    import numpy as np

    records = [
        line for line in MINIMAL_LIG_PDBQT.splitlines() if line.startswith('ATOM')
    ]
    coordinates = np.array([[[0.0, 0.0, 0.0], [1.5, 0.0, 0.0]]])
    with pytest.raises(ArgumentError, match='atom order or coordinates differ'):
        _verify_pose_atom_order(
            MINIMAL_LIG_PDBQT, '\n'.join(reversed(records)), coordinates
        )
