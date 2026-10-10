"""Protect the registered population, heavy map and all-attempt reporting."""

import gzip
import itertools
import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw

import dockingmt as dmt
from devtools.evaluate_3ptb_saved import OUTPUT as EVALUATIONS
from devtools.qualify_3ptb_admission import DATA, sha
from devtools.qualify_3ptb_search import (
    OUTPUT,
    baseline,
    evaluate,
    execution_protocol,
    qualify,
    summarize,
    verify_replay,
)


@pytest.fixture(scope='module')
def original():
    return baseline()[0]


@pytest.fixture(scope='module')
def searches():
    return json.loads(gzip.decompress(OUTPUT.read_bytes()))


@pytest.fixture(scope='module')
def measured(searches):
    received = json.loads(gzip.decompress(EVALUATIONS.read_bytes()))
    assert received['search_archive_sha256'] == sha(OUTPUT.read_bytes())
    assert received['new_searches_executed'] == 0
    assert received['registered_criterion_changed'] is False
    assert received['original_execution_summary'] == searches['summary']
    return [
        dict(raw, status=new['status'], evaluation=new['evaluation'])
        for raw, new in zip(searches['runs'], received['runs'], strict=True)
    ]


@pytest.fixture(scope='module')
def reference(tmp_path_factory):
    path = tmp_path_factory.mktemp('3ptb-heavy-reference') / '3PTB.pdb'
    path.write_bytes(gzip.decompress((DATA / '3PTB.pdb.gz').read_bytes()))
    source = msm.convert(path, to_form='molsysmt.MolSys', get_missing_bonds=False)
    return msm.extract(source, selection="group_name=='BEN'", structure_indices=0)


def test_prepared_protocol_projection_preserves_every_other_parameter(original):
    for row in original['population']:
        projected = execution_protocol(row).to_dict()
        declared = deepcopy(row['protocol'])
        declared['parameters']['active_torsion_bonds'] = []
        assert projected == declared
    assert original['population'][12]['protocol']['parameters'][
        'active_torsion_bonds'
    ] == [[0, 6]]


@pytest.mark.parametrize('change', ['tree', 'geometry', 'box', 'population'])
def test_input_drift_rejected_before_search(original, change):
    changed = deepcopy(original)
    if change == 'tree':
        changed['prepared_inputs']['flexible']['pdbqt'] += 'REMARK changed tree\n'
    elif change == 'geometry':
        changed['prepared_inputs']['rigid']['coordinates'][0][0] += 1
    elif change == 'box':
        changed['boxes']['negative']['backend_projection']['center'][0] -= 60
    else:
        changed['population'].pop()
    with pytest.raises(AssertionError):
        verify_replay(original, changed)


def test_existing_output_rejected_without_starting_another_experiment(tmp_path):
    output = tmp_path / 'saved.json.gz'
    output.write_bytes(b'owned scientific evidence')
    with pytest.raises(FileExistsError, match='never replace'):
        qualify(tmp_path / 'absent.pdb', output)
    assert output.read_bytes() == b'owned scientific evidence'


def test_original_archive_and_all_attempts_are_retained(original, searches):
    checkpoint = json.loads(OUTPUT.with_name('checkpoint_2026-10-10.json').read_text())
    assert sha(OUTPUT.read_bytes()) == checkpoint['original_producer']['archive_sha256']
    assert (
        sha(OUTPUT.with_name('producer_2026-10-10.py.txt').read_bytes())
        == searches['original_producer']['consumer_driver_sha256']
    )
    runs = searches['runs']
    assert len(runs) == 24
    assert [
        (
            r['arm'],
            r['domain'],
            r['protocol']['parameters']['seed'],
            r['protocol']['parameters']['exhaustiveness'],
        )
        for r in runs
    ] == list(
        itertools.product(
            ('rigid', 'flexible'), ('native', 'negative'), (7, 42, 2026), (1, 8)
        )
    )
    assert searches['fixed_evaluations_executed'] == 0
    for frozen, run in zip(original['population'], runs, strict=True):
        assert {key: run[key] for key in frozen if key != 'status'} == {
            key: frozen[key] for key in frozen if key != 'status'
        }
        assert run['status'] in ('evaluated', 'search_failed', 'evaluation_failed')
        if 'result' in run:
            restored = dmt.DockingResult.from_dict(run['result'])
            dmt.verify_captured_inputs(restored.provenance['backend_artifacts'])
            for role in ('receptor', 'partner'):
                assert (
                    restored.provenance['backend_artifacts'][role]['sha256']
                    == run[f'{role}_pdbqt_sha256']
                )
            native = restored.provenance['backend_output']
            assert len(native['energies']) == len(restored.poses)
            assert all(len(vector) == 5 for vector in native['energies'])
    assert searches['summary'] == summarize(runs)


@pytest.mark.parametrize('arm', ['rigid', 'flexible'])
def test_saved_metrics_replay_with_nondefault_units(original, measured, reference, arm):
    run = next(r for r in measured if r['arm'] == arm and r['status'] == 'evaluated')
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'degrees']
    ):
        result = dmt.DockingResult.from_dict(run['result'])
        box = dmt.BoxRegion(
            puw.quantity(run['backend_box']['center'], 'angstrom'),
            puw.quantity(run['backend_box']['size'], 'angstrom'),
        )
        replay = evaluate(result, reference, box, original, arm)
    np.testing.assert_allclose(
        [p['rmsd'] for p in replay['report']['poses']],
        [p['rmsd'] for p in run['evaluation']['report']['poses']],
        rtol=0,
        atol=1e-10,
    )
    for key in (
        'heavy_written_indices',
        'heavy_to_reference_indices',
        'pdbqt_to_full_source_atom_indices',
        'containment',
        'complete_energy_vectors',
        'top1_near',
        'any_near',
        'first_near_rank',
    ):
        assert replay[key] == run['evaluation'][key]
    assert (
        replay['report']['criterion']['atom_correspondence']
        == 'verified_source_atom_keys'
    )
    assert replay['report']['criterion']['alignment'] == 'none'
    assert replay['report']['criterion']['symmetry_correction'] == 'none'


def test_unknown_and_failed_attempts_keep_the_planned_denominator(original):
    rows = deepcopy(original['population'])
    rows[0]['status'] = 'search_failed'
    rows[1]['status'] = 'attempting'
    rows[2].update(status='evaluation_failed', result={'poses': []})
    summary = summarize(rows)
    assert sum(r['planned'] for r in summary) == 24
    assert summary[0]['attempted'] == 3
    assert summary[0]['returned'] == 1
    assert summary[0]['evaluated'] == 0
    assert summary[0]['search_failures'] == summary[0]['evaluation_failures'] == 1
    assert summary[0]['top1_near'] == summary[0]['any_near'] == 0


def test_changed_pose_identity_is_rejected_before_geometry(
    original, measured, reference, monkeypatch
):
    run = next(
        r for r in measured if r['arm'] == 'flexible' and r['status'] == 'evaluated'
    )
    result = dmt.DockingResult.from_dict(run['result'])
    index = run['evaluation']['heavy_written_indices'][0]
    result.poses[0].metadata['source_atom_keys'][index]['atom_id'] = 'wrong-observed-id'

    def forbidden(*args, **kwargs):
        pytest.fail('Identity drift reached molecular geometry')

    monkeypatch.setattr(msm.structure, 'get_rmsd', forbidden)
    box = dmt.BoxRegion(
        puw.quantity(run['backend_box']['center'], 'angstrom'),
        puw.quantity(run['backend_box']['size'], 'angstrom'),
    )
    with pytest.raises(AssertionError):
        evaluate(result, reference, box, original, 'flexible')


def test_heavy_selection_ignores_hydrogens_without_aligning_the_pose(
    original, measured, reference
):
    run = next(
        r for r in measured if r['arm'] == 'flexible' and r['status'] == 'evaluated'
    )
    result = dmt.DockingResult.from_dict(run['result'])
    pose = result.poses[0]
    original_xyz = puw.get_value(
        msm.get(reference, coordinates=True), to_unit='angstrom'
    )[0]
    coordinates = np.full((13, 3), 1000.0)
    for written, observed in zip(
        run['evaluation']['heavy_written_indices'],
        run['evaluation']['heavy_to_reference_indices'],
        strict=True,
    ):
        coordinates[written] = original_xyz[observed] + [3, 4, 0]
    metadata = deepcopy(pose.metadata)
    metadata.pop('score_definitions', None)
    synthetic = dmt.DockingPose(
        coordinates=puw.quantity(coordinates, 'angstrom'),
        scores=pose.scores,
        rank=pose.rank,
        pose_id=pose.pose_id,
        partner_state_id=pose.partner_state_id,
        receptor_state_id=pose.receptor_state_id,
        score_definitions=pose.score_definitions,
        metadata=metadata,
    )
    provenance = deepcopy(result.provenance)
    provenance.pop('ranking_history', None)
    provenance['backend_output']['energies'] = provenance['backend_output']['energies'][
        :1
    ]
    reduced = dmt.DockingResult([synthetic], provenance=provenance)
    box = dmt.BoxRegion(
        puw.quantity(run['backend_box']['center'], 'angstrom'),
        puw.quantity(run['backend_box']['size'], 'angstrom'),
    )
    measured = evaluate(reduced, reference, box, original, 'flexible')
    assert measured['best_rmsd_angstrom'] == pytest.approx(5, abs=1e-10)
    assert measured['any_near'] is False


def test_receiving_all_saved_poses_forbids_new_native_work(
    tmp_path, searches, monkeypatch
):
    from vina import Vina

    import devtools.evaluate_3ptb_saved as receiver

    # CI tests the receiving behavior in each supported interpreter. Native/source
    # qualification of the scientific producer is a separate executed receipt.
    monkeypatch.setattr(
        receiver, 'producer_identity', lambda: {'consumer_source_sha256': {}}
    )

    def forbidden(*args, **kwargs):
        pytest.fail('Saved evaluation attempted new preparation, scoring or search')

    for name in ('compute_vina_maps', 'score', 'optimize', 'dock'):
        monkeypatch.setattr(Vina, name, forbidden)
    for name in ('dock', 'score', 'prepare_ligand', 'prepare_receptor'):
        monkeypatch.setattr(dmt, name, forbidden)
    source = tmp_path / '3PTB.pdb'
    source.write_bytes(gzip.decompress((DATA / '3PTB.pdb.gz').read_bytes()))
    with puw.context(
        standard_units=['pm', 'fs', 'K', 'mole', 'dalton', 'e', 'kJ/mol', 'degrees']
    ):
        received = receiver.qualify(
            source,
            search_sha256=sha(OUTPUT.read_bytes()),
            output=tmp_path / 'received.json.gz',
        )
    original = json.loads(gzip.decompress(EVALUATIONS.read_bytes()))
    assert received['summary'] == original['summary']
    for expected, actual in zip(original['runs'], received['runs'], strict=True):
        np.testing.assert_allclose(
            [row['rmsd'] for row in actual['evaluation']['report']['poses']],
            [row['rmsd'] for row in expected['evaluation']['report']['poses']],
            rtol=0,
            atol=1e-10,
        )
        assert actual['original_status'] == expected['original_status']
        assert actual['original_error'] == expected['original_error']
