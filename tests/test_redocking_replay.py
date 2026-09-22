import hashlib
import json
from pathlib import Path

import molsysmt as msm
import pytest
import pyunitwizard as puw

from devtools.redocking_181l import _summarize, record_manifest, replay_manifest
from dockingmt import BoxRegion, DockingPose, DockingProblem, DockingResult
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


def test_file_backed_181l_manifest_replays_without_original_objects(tmp_path):
    if not VinaBackend().is_available:
        pytest.skip('Vina is not installed in the environment.')

    manifest_path = tmp_path / '181l-manifest.json'
    report_path = tmp_path / '181l-report.json'
    record_manifest(manifest_path)
    saved = DockingResult.from_dict(json.loads(manifest_path.read_text()))
    assert saved.problem is None
    restored_problem = saved.reconstruct_problem()
    assert restored_problem.partner_atom_indices == [1299, 1300, 1301, 1302, 1303, 1304]
    assert saved.problem is restored_problem

    report = replay_manifest(manifest_path, report_path)
    assert report == json.loads(report_path.read_text())
    assert report['assessment'] == 'exploratory_provisional_preparation'
    assert (
        report['manifest_sha256']
        == hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    )
    assert report['recorded']['n_poses'] > 0
    assert len(report['recorded']['poses']) == report['recorded']['n_poses']
    assert report['comparison']['within_tolerance'] is True
    assert report['comparison']['input_hashes_match'] is True
    assert report['comparison']['pdbqt_hashes_match'] is True
    assert report['comparison']['identity_match'] is True
    assert report['comparison']['source_revision_match'] is True


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
