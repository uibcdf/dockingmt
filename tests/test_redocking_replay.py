import base64
import hashlib
import json
from pathlib import Path

import molsysmt as msm
import pytest
import pyunitwizard as puw
from molecular_fixtures import named_181l_pair

from devtools.redocking_181l import (
    _compare,
    _summarize,
    record_manifest,
    replay_manifest,
)
from dockingmt import (
    BoxRegion,
    DockingPose,
    DockingProblem,
    DockingResult,
    VinaProtocol,
    dock,
)
from dockingmt._private.smonitor import ArgumentError
from dockingmt.engines.vina import VinaBackend


def test_redocking_report_identifies_near_native_rank_and_failure():
    reference = puw.quantity([[0.0, 0.0, 0.0]], 'angstrom')
    result = DockingResult(
        poses=[
            DockingPose(
                coordinates=puw.quantity([[3.0, 0.0, 0.0]], 'angstrom'),
                scores={'vina': -4.0},
                rank=1,
            ),
            DockingPose(
                coordinates=puw.quantity([[1.0, 0.0, 0.0]], 'angstrom'),
                scores={'vina': -3.0},
                rank=2,
            ),
        ]
    )
    summary = _summarize(result, reference)
    assert summary['near_native_rank'] == 2
    assert summary['failure_mode'] is None
    assert summary['vina_score_range'] == [-4.0, -3.0]
    assert summary['poses'][0]['rmsd_angstrom'] == pytest.approx(3.0)
    assert _summarize(DockingResult(poses=[]), reference)['failure_mode'] == 'no_poses'


def test_named_181l_result_replays_with_explicit_original_objects(tmp_path):
    if not VinaBackend().is_available:
        pytest.skip('Vina is not installed in the environment.')

    manifest_path = tmp_path / '181l-manifest.json'
    report_path = tmp_path / '181l-report.json'
    receptor, ligand = named_181l_pair()
    domain = BoxRegion.from_selection(
        ligand.source_molsys, padding=puw.quantity(8, 'angstrom')
    )
    problem = DockingProblem(receptor, ligand, domain)
    result = dock(
        problem,
        VinaProtocol(
            exhaustiveness=1, n_poses=5, seed=42, cpu=1, capture_backend_inputs=True
        ),
    )
    manifest_path.write_text(json.dumps(result.to_dict()))
    manifest = json.loads(manifest_path.read_text())
    saved = DockingResult.from_dict(manifest)
    for role in ('receptor', 'partner'):
        artifact = saved.provenance['backend_artifacts'][role]
        content = base64.b64decode(artifact['content_base64'], validate=True)
        assert content
        assert hashlib.sha256(content).hexdigest() == artifact['sha256']
    assert saved.problem is None
    # A PDB fingerprint cannot persist a named mechanical assignment. Provider
    # H5MSM 0.6 persistence is tracked in molsysmt#256; original objects are explicit.
    with pytest.raises(ArgumentError, match='require explicit receptor and partner'):
        replay_manifest(manifest_path, report_path)
    assert not report_path.exists()
    restored_problem = saved.reconstruct_problem(receptor=receptor, partner=ligand)
    assert restored_problem.partner_atom_indices == list(range(6))
    assert saved.problem is restored_problem

    replayed = dock(restored_problem, VinaProtocol.from_dict(saved.protocol_info))
    comparison = _compare(saved, replayed, ligand.source_molsys)
    assert comparison['within_tolerance'] is True
    assert comparison['input_hashes_match'] is True
    assert comparison['pdbqt_hashes_match'] is True
    assert comparison['backend_box_match'] is True
    assert comparison['identity_match'] is True
    assert saved.provenance['preparation']['partner']['assessment'] == 'unassessed'
    assert len(saved) == len(replayed) > 0

    manifest['provenance']['backend_artifacts']['partner']['content_base64'] = (
        base64.b64encode(b'changed PDBQT').decode('ascii')
    )
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match='partner PDBQT input bytes failed SHA-256'):
        replay_manifest(manifest_path, report_path)


def test_legacy_recording_rejects_untyped_inputs_before_creating_manifest(tmp_path):
    target = tmp_path / 'legacy.json'
    with pytest.raises(
        ArgumentError, match='Named MolSysMT AutoDock4 types are required'
    ):
        record_manifest(target)
    assert not target.exists()


def test_file_backed_reconstruction_preserves_identity_but_does_not_invent_types():
    source = Path(msm.systems['T4 lysozyme L99A']['181l.pdb']).resolve()
    problem = DockingProblem.for_redocking(
        source,
        receptor_selection="molecule_type=='protein'",
        partner_selection="group_name=='BNZ'",
        padding=puw.quantity(8, 'angstrom'),
    )
    saved = DockingResult.from_dict(
        DockingResult([], problem_info=problem.to_dict()).to_dict()
    )
    restored = saved.reconstruct_problem()
    assert restored.partner_atom_indices == [1299, 1300, 1301, 1302, 1303, 1304]
    assert restored.to_dict() == problem.to_dict()
    with pytest.raises(
        ArgumentError, match='Named MolSysMT AutoDock4 types are required'
    ):
        dock(restored, VinaProtocol(allow_provisional_preparation=True))


def test_result_problem_reconstruction_rejects_changed_file(tmp_path):
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
    result = DockingResult.from_dict(
        json.loads(
            json.dumps(DockingResult([], problem_info=problem.to_dict()).to_dict())
        )
    )
    local.write_bytes(local.read_bytes() + b'REMARK changed\n')
    with pytest.raises(ArgumentError, match='source content has changed'):
        result.reconstruct_problem()
    assert result.problem is None
