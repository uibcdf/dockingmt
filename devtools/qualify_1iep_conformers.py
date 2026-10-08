"""Prespecified +/-60 degree 1IEP input controls using public MolSysMT geometry.

Evaluate against the unchanged original reference, never the perturbed input.
The two geometries are unminimized torsional controls, not a conformer ensemble.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_1iep_flexibility import CUTS
from devtools.qualify_1iep_representation import fixed_score, observe, save, sha
from devtools.qualify_1iep_root_order import OUTPUT as BASELINE
from devtools.qualify_1iep_root_order import prepare_control
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING
from dockingmt.engines.vina import _pdbqt_atom_records

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'devguide/validation/data/1iep_conformers/audit_2026-10-08.json.gz'
BASELINE_SHA256 = 'cfea8e331a9d3b53fe8adf6ca766bfaf68a8483f0d8984aae28949e6084b5eba'
QUARTETS = [
    [16, 17, 19, 20],
    [10, 12, 13, 14],
    [9, 10, 12, 13],
    [1, 2, 6, 7],
    [19, 20, 21, 22],
    [23, 24, 27, 28],
    [24, 27, 28, 29],
]
SHIFTS = {'plus60': 60.0, 'minus60': -60.0}


def load_baseline():
    """Authenticate historical bound-like observations without rerunning them."""
    content = BASELINE.read_bytes()
    assert sha(content) == BASELINE_SHA256
    return json.loads(gzip.decompress(content))


def xyz(system):
    return puw.get_value(msm.get(system, coordinates=True), to_unit='angstrom')[0]


def geometry_check(original, moved, shift):
    """Measure this fixture's covalent geometry and signed local orientation."""
    before, after = snapshot(original), snapshot(moved)
    expected = detached_record(before)
    expected['structures']['coordinates'] = after['structures']['coordinates']
    assert after == expected  # All chemistry, identities and frame metadata.
    pairs = np.asarray(msm.get(original, element='bond', bonded_atom_pairs=True))
    assert pairs.shape == (73, 2)
    neighbors = [set() for _ in range(69)]
    for a, b in pairs:
        neighbors[a].add(int(b))
        neighbors[b].add(int(a))
    triplets = [
        [a, center, b]
        for center, adjacent in enumerate(neighbors)
        for a, b in itertools.combinations(sorted(adjacent), 2)
    ]
    a, b = xyz(original), xyz(moved)
    bond_lengths = [
        np.linalg.norm(c[pairs[:, 0]] - c[pairs[:, 1]], axis=1) for c in (a, b)
    ]
    np.testing.assert_allclose(*bond_lengths, rtol=0, atol=1e-10)
    bond_angles = [
        puw.get_value(
            msm.structure.get_angles(
                system, triplets=triplets, pbc=False, use_gpu=False
            ),
            to_unit='degree',
        )
        for system in (original, moved)
    ]
    np.testing.assert_allclose(*bond_angles, rtol=0, atol=1e-8)
    orientation = []
    for center, adjacent in enumerate(neighbors):
        for triple in itertools.combinations(sorted(adjacent), 3):
            orientation.append(
                [float(np.linalg.det(c[list(triple)] - c[center])) for c in (a, b)]
            )
    np.testing.assert_allclose(
        np.array(orientation)[:, 0], np.array(orientation)[:, 1], rtol=0, atol=1e-9
    )
    angles = [
        puw.get_value(
            msm.structure.get_dihedral_angles(
                system, dihedral_quartets=QUARTETS, pbc=False, use_gpu=False
            ),
            to_unit='degree',
        )[0]
        for system in (original, moved)
    ]
    expected_delta = np.zeros(7)
    expected_delta[2] = shift
    error = (angles[1] - angles[0] - expected_delta + 180) % 360 - 180
    np.testing.assert_allclose(error, 0, rtol=0, atol=1e-8)
    return {
        'source_snapshot': after,
        'shift_degree': shift,
        'dihedrals_before_degree': angles[0].tolist(),
        'dihedrals_after_degree': angles[1].tolist(),
        'max_wrapped_dihedral_error_degree': float(np.max(np.abs(error))),
        'max_bond_length_change_angstrom': float(
            np.max(np.abs(bond_lengths[1] - bond_lengths[0]))
        ),
        'max_bond_angle_change_degree': float(
            np.max(np.abs(bond_angles[1] - bond_angles[0]))
        ),
        'max_signed_volume_change_angstrom3': float(
            np.max(np.abs(np.diff(orientation, axis=1)))
        ),
        'heavy_input_positional_rmsd_angstrom': float(
            np.sqrt(np.mean(np.sum((b[:37] - a[:37]) ** 2, axis=1)))
        ),
        'geometry_policy': 'one_declared_torsion_shift_no_minimization_or_selection',
    }


def prepare_cases(*, verify_profile=False):
    """Retain original identity and prepare each public-geometry output."""
    baseline = load_baseline()
    if verify_profile:
        for relative, expected in baseline['consumer_source_sha256'].items():
            assert sha((ROOT / relative).read_bytes()) == expected, relative
    source, _, representation, audit = prepare_control(verify_profile=verify_profile)
    before = snapshot(source)
    native = representation['controls']['native']
    if verify_profile:
        original_native = native['pdbqt']
    else:
        # Portable guards compare provenance within the actual runtime. An
        # ordinary installation of the same source can report another version
        # in its REMARK records. Historical science still requires its exact
        # producer profile and original bytes above.
        original_native = dmt.prepare_ligand(
            source,
            selection='all',
            active_torsion_bonds=CUTS,
            charge_options=CHARGE,
            typing_options=TYPING,
        ).to_pdbqt()
    cases = {}
    for name, shift in SHIFTS.items():
        target = msm.structure.get_dihedral_angles(
            source, dihedral_quartets=[QUARTETS[2]], pbc=False, use_gpu=False
        )
        target = target + puw.quantity([[shift]], 'degree')
        moved = msm.structure.set_dihedral_angles(
            source,
            dihedral_quartets=[QUARTETS[2]],
            angles=target,
            pbc=False,
            in_place=False,
        )
        check = geometry_check(source, moved, shift)
        assert snapshot(source) == before
        ligand = dmt.prepare_ligand(
            moved,
            selection='all',
            active_torsion_bonds=CUTS,
            charge_options=CHARGE,
            typing_options=TYPING,
        )
        assert snapshot(moved) == check['source_snapshot']
        mapping = [
            ligand.metadata['retained_atom_indices'][i]
            for i in ligand.pdbqt_atom_indices
        ]
        assert mapping == native['pdbqt_to_source_atom_indices']
        lines = ligand.to_pdbqt().encode().splitlines(keepends=True)
        original_lines = original_native.encode().splitlines(keepends=True)
        # Every byte except the three coordinate columns stays identical.
        assert len(lines) == len(original_lines)
        for old, new in zip(original_lines, lines, strict=True):
            assert (
                (old[:30] + old[54:] == new[:30] + new[54:])
                if old.startswith(b'ATOM')
                else old == new
            )
        first, last = lines.index(b'ROOT\n') + 1, lines.index(b'ENDROOT\n')
        assert last - first == 8 and mapping[:8] == [28, 29, 30, 31, 32, 33, 34, 58]
        variants = {
            'native': (b''.join(lines), mapping),
            'first_fixed': (
                b''.join(
                    lines[: first + 1] + lines[first + 1 : last][::-1] + lines[last:]
                ),
                mapping[:1] + mapping[1:8][::-1] + mapping[8:],
            ),
        }
        controls = {}
        for order, (content, indices) in variants.items():
            records = _pdbqt_atom_records(content.decode())
            written_xyz = np.array([r[1] for r in records])
            np.testing.assert_allclose(
                written_xyz, xyz(moved)[indices], rtol=0, atol=0.000501
            )
            controls[order] = {
                'pdbqt': content.decode(),
                'sha256': sha(content),
                'pdbqt_to_source_atom_indices': indices,
                'heavy_pdbqt_indices': [
                    i for i, index in enumerate(indices) if index < 37
                ],
                'first_root_source_atom_index': indices[0],
                'rigid_body_origin_angstrom': list(records[0][1]),
            }
        assert (
            controls['native']['rigid_body_origin_angstrom']
            == controls['first_fixed']['rigid_body_origin_angstrom']
        )
        check['controls'] = controls
        cases[name] = check
    return source, detached_record(cases), baseline, representation, audit


def comparison_rows(record, baseline, representation):
    """Separate original bound-like producers from the 24 new observations."""
    rows = []
    groups = [
        (
            'bound_like',
            'historical',
            representation['original_native_runs'] + baseline['new_runs'],
        ),
        ('perturbed', 'new', record['new_runs']),
    ]
    for geometry, provenance, runs in groups:
        for run in runs:
            p = run['result']['protocol_info']['parameters']
            metrics = [
                m['heavy_atom_positional_rmsd_angstrom']
                for m in run['heavy_atom_metrics']
            ]
            rows.append(
                {
                    'geometry': run.get('geometry', geometry),
                    'provenance': provenance,
                    'order': run.get(
                        'order',
                        'native' if run['variant'] == 'flexible' else 'first_fixed',
                    ),
                    'seed': p['seed'],
                    'exhaustiveness': p['exhaustiveness'],
                    'poses': len(metrics),
                    'first_heavy_rmsd_angstrom': metrics[0],
                    'closest_heavy_rmsd_angstrom': min(metrics),
                    'first_vina_score_kcal_mol': run['result']['poses'][0]['scores'][
                        'vina'
                    ],
                    'first_pose_recovered': metrics[0] <= 2.5,
                    'returned_set_recovered': min(metrics) <= 2.5,
                }
            )
    return rows


def score_observation(control, variant):
    """Retain the expected outside-grid refusal without hiding other failures."""
    try:
        return {'status': 'scored', 'pose': fixed_score(control, variant)}
    except RuntimeError as error:
        if 'The ligand is outside the grid box' not in str(error):
            raise
        return {
            'status': 'rejected_outside_grid',
            'exception_type': type(error).__name__,
            'message': str(error),
            'submitted_partner_sha256': control['sha256'],
            'scope': 'fixed input score rejected; search admission is a separate observation',
        }


def qualify(arm=None, checkpoint=None):
    source, cases, baseline, representation, audit = prepare_cases(verify_profile=True)
    runs, scores = [], {}
    for geometry, case in cases.items():
        scores[geometry] = {}
        for order, control in case['controls'].items():
            if arm is not None and arm != f'{geometry}_{order}':
                continue
            scores[geometry][order] = score_observation(control, f'{geometry}_{order}')
            for effort in (1, 8):
                for seed in (7, 42, 2026):
                    run = observe(
                        source,
                        control,
                        variant=f'{geometry}_{order}',
                        seed=seed,
                        exhaustiveness=effort,
                    )
                    run.update(geometry=geometry, order=order)
                    runs.append(run)
                    if checkpoint is not None:
                        save(
                            {
                                'schema': 'dockingmt.1iep_conformer_partial@1',
                                'date': '2026-10-08',
                                'arm': arm,
                                'driver_sha256': sha(Path(__file__).read_bytes()),
                                'interpreter': sys.executable,
                                'producer_versions': representation[
                                    'producer_versions'
                                ],
                                'baseline_sha256': BASELINE_SHA256,
                                'audit': audit,
                                'cases': cases,
                                'new_runs': runs,
                                'fixed_conformation_scores': scores,
                            },
                            checkpoint,
                        )
                    print(
                        f'Completed {len(runs)}/24: {geometry}/{order}, seed={seed}, effort={effort}',
                        file=sys.stderr,
                        flush=True,
                    )
    provider = Path(representation['provider_module']).parent.parent
    provider_paths = [
        'molsysmt/structure/set_dihedral_angles.py',
        'molsysmt/structure/get_dihedral_angles.py',
        'molsysmt/structure/get_angles.py',
        'molsysmt/topology/get_covalent_blocks.py',
        'molsysmt/lib/structure/_kernel_inputs.py',
    ]
    record = {
        'schema': 'dockingmt.1iep_conformer_audit@1',
        'date': '2026-10-08',
        'interpreter': sys.executable,
        'python': sys.version,
        'consumer_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'consumer_source_sha256': {
            **baseline['consumer_source_sha256'],
            str(Path(__file__).relative_to(ROOT)): sha(Path(__file__).read_bytes()),
        },
        'provider_module': representation['provider_module'],
        'qualified_provider_commit': representation['qualified_provider_commit'],
        'provider_source_sha256': {
            **representation['provider_source_sha256'],
            **{p: sha((provider / p).read_bytes()) for p in provider_paths},
        },
        'provider_native_artifacts': representation['provider_native_artifacts'],
        'producer_versions': representation['producer_versions'],
        'baseline': {
            'path': str(BASELINE.relative_to(ROOT)),
            'sha256': BASELINE_SHA256,
            'fixed_first_producer': '2f2ee8f7cebe9b07e5ac240937896dfaf9df197e',
            'native_producer': '7b11391e153f77f340fd039bc799352f90da83d3',
            'scope': '12 historical bound-like cells by authenticated reference, no reruns',
        },
        'prespecified_plan': [
            'https://github.com/uibcdf/dockingmt/issues/17#issuecomment-6068927987',
            'https://github.com/uibcdf/dockingmt/issues/6#issuecomment-6068927518',
        ],
        'audit': audit,
        'quartets': QUARTETS,
        'cases': cases,
        'fixed_conformation_scores': scores,
        'new_runs': runs,
        'limits': [
            'One complex, two prespecified unminimized torsion perturbations, three seeds; no conformer ensemble, convergence or recovery probability.',
            'Original chemistry/H and external rigid receptor remain declared/unassessed; no affinity or preparation qualification.',
            'Scores and RMSDs are observations, not criteria for selecting input conformers or a default ROOT policy.',
            'The first ROOT atom/origin agrees within each order pair but coordinates/origins change across conformers.',
            'Evaluate against original crystallographic coordinates through the preserved written/source axis, without alignment or symmetry correction.',
            'Rigid fragments, bond lengths/angles and local signed orientations are retained; steric strain/overlaps are not minimized or filtered.',
            'Historical observations retain original producers; preserved native digest is not fresh build provenance or new installed/public artifact qualification.',
        ],
    }
    record['comparison_rows'] = comparison_rows(record, baseline, representation)
    return detached_record(record)


def assemble(parts):
    """Join four independently retained six-cell arms with the same producers."""
    assert len(parts) == 4
    first = detached_record(parts[0])
    first['new_runs'] = []
    first['fixed_conformation_scores'] = {name: {} for name in SHIFTS}
    identity = [
        'consumer_base_commit',
        'consumer_source_sha256',
        'producer_versions',
        'provider_source_sha256',
        'provider_native_artifacts',
        'baseline',
        'audit',
        'cases',
    ]
    for part in parts:
        assert len(part['new_runs']) == 6
        for field in identity:
            assert part[field] == parts[0][field], field
        first['new_runs'].extend(part['new_runs'])
        for geometry, observations in part['fixed_conformation_scores'].items():
            for order, observation in observations.items():
                assert order not in first['fixed_conformation_scores'][geometry]
                first['fixed_conformation_scores'][geometry][order] = observation
    cells = {
        (
            r['geometry'],
            r['order'],
            r['result']['protocol_info']['parameters']['seed'],
            r['result']['protocol_info']['parameters']['exhaustiveness'],
        )
        for r in first['new_runs']
    }
    assert cells == {
        (g, o, s, e)
        for g in SHIFTS
        for o in ('native', 'first_fixed')
        for s in (7, 42, 2026)
        for e in (1, 8)
    }
    for observations in first['fixed_conformation_scores'].values():
        assert observations['native']['status'] == observations['first_fixed']['status']
        if observations['native']['status'] == 'scored':
            assert (
                observations['native']['pose']['scores']
                == observations['first_fixed']['pose']['scores']
            )
    from devtools.qualify_1iep_root_order import load_baseline as load_representation

    first['comparison_rows'] = comparison_rows(
        first, load_baseline(), load_representation()
    )
    return first


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument(
        '--arm', choices=[f'{g}_{o}' for g in SHIFTS for o in ('native', 'first_fixed')]
    )
    parser.add_argument('--parts', nargs=4, type=Path)
    args = parser.parse_args()
    if args.parts:
        if args.arm:
            parser.error('--arm and --parts are mutually exclusive')
        record = assemble(
            [json.loads(gzip.decompress(p.read_bytes())) for p in args.parts]
        )
    else:
        record = qualify(args.arm, args.output)
    save(record, args.output)
