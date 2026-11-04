"""Run bounded public evaluation controls, preserving declared preparation limits."""

import hashlib
from pathlib import Path

import molsysmt as msm
import pyunitwizard as puw

import dockingmt as dmt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'tests/data/vina_torsions'
INPUT_DIGESTS = {
    '1iep_receptor.pdbqt': 'f13cf3b36f61d87c3b58983e0b8ecf1c3456a685eb86dfe9ccfb139c7bdc2586',
    '1iep_ligand.pdbqt': '15fb35648d8c18c70317842f3a0631b73a19429c710a037ab07310084d579bb8',
}


def qualify():
    """Return finite reports for provisional 181L and external 1IEP/control.

    The 1IEP reference is the prepared input conformation, including all 40
    retained atoms, not the earlier 37-heavy-atom SDF comparison. This explicit
    positional comparison relies on the adapter's verified PDBQT output order.
    MolSysMT reads reference coordinates with explicit torsion-tree discard;
    untouched PDBQT input bytes and their tree still go to Vina.
    """
    system_path = msm.systems['T4 lysozyme L99A']['181l.pdb']
    source = msm.convert(system_path, to_form='molsysmt.MolSys')
    reference = msm.extract(source, selection="group_name=='BNZ'")
    domain = dmt.BoxRegion.from_selection(
        source, selection="group_name=='BNZ'", padding=puw.quantity(8, 'angstrom')
    )
    problem = dmt.DockingProblem(
        source,
        source,
        domain,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
    )
    protocol = dmt.VinaProtocol(
        seed=42,
        cpu=1,
        exhaustiveness=1,
        n_poses=5,
        capture_backend_inputs=True,
        allow_provisional_preparation=True,
    )
    result = dmt.dock(problem, protocol)
    reports = {
        '181l_provisional': dmt.evaluate_redocking(
            result,
            reference,
            rmsd_cutoff=puw.quantity(2.5, 'angstrom'),
            reference_info={
                'case': '181L BNZ',
                'source_sha256': hashlib.sha256(
                    Path(system_path).read_bytes()
                ).hexdigest(),
                'qualification': 'software_control_provisional_preparation',
            },
        )
    }
    assert (
        reports['181l_provisional']['context']['preparation']['partner']['assessment']
        == 'provisional'
    )

    for filename, digest in INPUT_DIGESTS.items():
        if hashlib.sha256((DATA / filename).read_bytes()).hexdigest() != digest:
            raise AssertionError(f'{filename} is not the pinned input.')
    reference_system = msm.convert(
        str(DATA / '1iep_ligand.pdbqt'),
        to_form='molsysmt.MolSys',
        discard_torsion_tree=True,
    )
    assert msm.get(reference_system, n_atoms=True) == 40
    coordinates = msm.get(reference_system, coordinates=True)
    assert puw.get_value(coordinates).shape == (1, 40, 3)
    protocol = dmt.VinaProtocol(
        seed=42, cpu=1, exhaustiveness=1, n_poses=5, capture_backend_inputs=True
    )
    for name, center in [
        ('1iep_external', [15.190, 53.903, 16.917]),
        ('1iep_displaced_domain', [45.190, 53.903, 16.917]),
    ]:
        domain = dmt.BoxRegion(
            puw.quantity(center, 'angstrom'), puw.quantity([20, 20, 20], 'angstrom')
        )
        if name == '1iep_displaced_domain':
            assert not any(
                domain.contains(puw.quantity(xyz, 'angstrom'))
                for xyz in puw.get_value(coordinates, to_unit='angstrom')[0]
            )
        problem = dmt.DockingProblem(
            DATA / '1iep_receptor.pdbqt', DATA / '1iep_ligand.pdbqt', domain
        )
        result = dmt.dock(problem, protocol)
        assert result.poses
        assert all(
            pose.n_atoms == 40
            and pose.metadata['pose_atom_order'] == 'verified_pdbqt_order'
            for pose in result.poses
        )
        for role, filename in [
            ('receptor', '1iep_receptor.pdbqt'),
            ('partner', '1iep_ligand.pdbqt'),
        ]:
            assert (
                result.provenance['backend_artifacts'][role]['sha256']
                == INPUT_DIGESTS[filename]
            )
        reports[name] = dmt.evaluate_redocking(
            result,
            coordinates,
            rmsd_cutoff=puw.quantity(2.5, 'angstrom'),
            reference_info={
                'case': name,
                'reference': 'pinned_prepared_ligand_conformation',
                'prepared_input_sha256': INPUT_DIGESTS['1iep_ligand.pdbqt'],
                'atom_order': 'verified_input_pdbqt_order',
                'atom_scope': 'all_40_retained_atoms_including_polar_hydrogens',
                'qualification': 'external_preparation_unassessed',
            },
        )
        assert (
            reports[name]['context']['preparation']['partner']['assessment']
            == 'unassessed'
        )
    return reports


def summary(reports):
    """Show per-case observations without interpreting a dataset success rate."""
    return {
        name: {
            'n_poses': report['n_poses'],
            'rmsds_angstrom': [row['rmsd'] for row in report['poses']],
            'top_n': report['top_n'],
            'atom_correspondence': report['criterion']['atom_correspondence'],
            'preparation': report['context']['preparation']['partner']['assessment'],
        }
        for name, report in reports.items()
    }
