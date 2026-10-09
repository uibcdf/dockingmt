"""Finite fixed-P69 intervention using public molecular composition and scoring.

Two same-writer receptor arms separate a fixed experimental heavy-atom occupant
from serialization. All retained geometries are scored unchanged in both arms.
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
from molsysmt.form.string_pdbqt_text import get_torsion_tree
from rdkit import Chem

import dockingmt as dmt
from devtools.qualify_5x72_root_order import (
    DATA,
    INPUTS,
    ROOT,
    comparison_rows,
    measure,
    prepare_cases,
    reference_box,
    sha,
    xyz,
)
from devtools.qualify_5x72_root_order import (
    OUTPUT as BASELINE,
)
from devtools.qualify_5x72_root_order import (
    producer_proof as baseline_proof,
)
from devtools.qualify_181l_receptor import save
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, HYDROGEN, TYPING

OUTPUT = ROOT / 'devguide/validation/data/5x72_occupancy/audit_2026-10-09.json.gz'
BASELINE_SHA = '2129d7eed2b73bcf90737b2a6c722e3b8e9269abeba0ca3b1444df51f046634e'
ARMS = [f'{r}_{o}' for r in ('sham', 'occupied') for o in ('native', 'first_fixed')]


def load_baseline():
    """Authenticate original searches without manufacturing new observations."""
    assert sha(BASELINE.read_bytes()) == BASELINE_SHA
    return json.loads(gzip.decompress(BASELINE.read_bytes()))


def atom_fields(text):
    """Independent fixed-column evidence for these explicitly prepared fixtures."""
    return [
        {
            'id': line[6:11].strip(),
            'name': line[12:16].strip(),
            'group': line[17:20].strip(),
            'group_id': line[22:26].strip(),
            'chain': line[21:22].strip(),
            'coordinates': [float(line[i : i + 8]) for i in (30, 38, 46)],
            'charge_e': float(line[70:76]),
            'type': line.split()[-1],
        }
        for line in text.splitlines()
        if line.startswith(('ATOM', 'HETATM'))
    ]


def prepare_receptors(*, companion='p69', reference_snapshot=None):
    """Compose prepared rigid records against an explicitly verified reference.

    Production defaults to the authenticated historical snapshot. Portable
    guards supply prepare_cases' independently verified current-runtime companion
    record, including that runtime's dataframe dtype annotations.
    """
    stereo = {'p59': 'R', 'p69': 'S'}[companion]
    ref = msm.convert(
        next(
            iter(
                Chem.SDMolSupplier(
                    str(DATA / f'5x72_ligand_{companion}.sdf'), removeHs=False
                )
            )
        ),
        to_form='molsysmt.MolSys',
    )
    before = snapshot(ref)
    if reference_snapshot is None:
        reference_snapshot = load_baseline()['cases'][companion]['reference_snapshot']
    assert before == reference_snapshot
    addition = msm.build.add_missing_hydrogens(ref, return_report=True, **HYDROGEN)
    source = addition['molecular_system']
    assert msm.get(source, n_atoms=True) == 39
    np.testing.assert_allclose(xyz(source)[:24], xyz(ref), rtol=0, atol=1e-12)
    assert msm.get(source, element='atom', atom_stereochemistry=True)[7] == stereo
    assert snapshot(ref) == before
    charged = msm.build.assign_partial_charges(source, **CHARGE)
    charged_before = snapshot(charged)
    prepared = dmt.prepare_receptor(charged, selection='all', typing_options=TYPING)
    assert snapshot(charged) == charged_before
    assert prepared.metadata['retained_atom_indices'] == [*range(24), 29]
    original = (DATA / '5x72_receptor.pdbqt').read_text()
    assert sha(original.encode()) == INPUTS['5x72_receptor.pdbqt']
    protein = msm.convert('pdbqt_text:' + original, to_form='molsysmt.MolSys')
    companion = msm.convert(
        'pdbqt_text:' + prepared.to_pdbqt(), to_form='molsysmt.MolSys'
    )
    msm.set(companion, element='atom', atom_id=list(range(1482, 1507)))
    protein_before, companion_before = snapshot(protein), snapshot(companion)
    combined = msm.add(
        protein, companion, in_place=False, keep_ids=True, attribute_policy='strict'
    )
    # Explicit fixture chain map: add preserves indices but drops chain IDs.
    assert msm.get(protein, element='chain', chain_id=True) == ['A']
    assert msm.get(companion, element='chain', chain_id=True) == ['A']
    assert msm.get(combined, n_chains=True) == 2
    msm.set(combined, element='chain', chain_id=['A', 'A'])
    assert snapshot(protein) == protein_before
    assert snapshot(companion) == companion_before
    payloads = {
        name: msm.convert(
            system, to_form='string:pdbqt_text', typing_scheme='autodock4'
        ).removeprefix('pdbqt_text:')
        for name, system in [('sham', protein), ('occupied', combined)]
    }
    old, sham, occupied = map(atom_fields, [original, *payloads.values()])
    assert len(old) == len(sham) == 1481 and len(occupied) == 1506
    for a, b in zip(sham, occupied[:1481], strict=True):
        assert a == b
    assert old == sham
    assert [a['id'] for a in occupied] == [str(i) for i in range(1, 1507)]
    np.testing.assert_allclose(
        [a['coordinates'] for a in occupied[1481:1505]], xyz(ref), rtol=0, atol=0.000501
    )
    assert not any(
        line.startswith(('ROOT', 'BRANCH', 'TORSDOF'))
        for text in payloads.values()
        for line in text.splitlines()
    )
    return detached_record(
        {
            'receptors': {
                k: {'pdbqt': v, 'sha256': sha(v.encode())} for k, v in payloads.items()
            },
            'companion_reference_snapshot': before,
            'hydrogen_addition': addition['report'],
            'companion_prepared': prepared.to_dict(),
            'companion_charge_audit': dmt.audit_preparation_charges(prepared),
            'companion_assessment': dmt.assess_preparation(prepared),
            'companion_pdbqt_to_generated_source': [*range(24), 29],
            'companion_serial_ids': list(range(1482, 1507)),
            'protein_atom_field_changes': [],
            'companion_generated_source_snapshot': snapshot(source),
            'explicit_chain_map': {
                'output_chain_indices': [0, 1],
                'chain_ids': ['A', 'A'],
                'provider_issue': 'uibcdf/molsysmt#353',
                'removal_condition': 'Provider add preserves these IDs without explicit restoration.',
            },
            'composition': 'public msm.add; detached, keep_ids=True, attribute_policy=strict',
            'representation': 'Prepared PDBQT projection; incomplete bonds/chemical states; original chemistry and H report retained separately.',
        }
    )


def producer_proof():
    proof = baseline_proof()
    baseline = load_baseline()
    for key in (
        'qualified_provider_commit',
        'provider_native_artifacts',
        'producer_versions',
    ):
        assert proof[key] == baseline[key]
    for relative, expected in baseline['consumer_source_sha256'].items():
        assert sha((ROOT / relative).read_bytes()) == expected, relative
    provider = Path(msm.__file__).resolve().parents[1]
    for relative in (
        'molsysmt/basic/add.py',
        'molsysmt/native/molsys.py',
        'molsysmt/native/topology.py',
        'molsysmt/native/structures.py',
        'molsysmt/basic/set.py',
        'molsysmt/build/add_missing_hydrogens.py',
        'molsysmt/_private/fixed_hydrogens.py',
        'molsysmt/form/molsysmt_MolSys/add.py',
        'molsysmt/form/molsysmt_MolSys/to_string_pdbqt_text.py',
        'molsysmt/_private/pdbqt_writer.py',
        'molsysmt/_private/pdbqt.py',
    ):
        expected = subprocess.check_output(
            [
                'git',
                '-C',
                str(ROOT.parent / 'molsysmt'),
                'show',
                f'{proof["qualified_provider_commit"]}:{relative}',
            ]
        )
        assert (provider / relative).read_bytes() == expected
        proof['provider_source_sha256'][relative] = sha(expected)
    proof['consumer_source_sha256'][str(Path(__file__).relative_to(ROOT))] = sha(
        Path(__file__).read_bytes()
    )
    return proof


def frozen_partner(control, pose):
    """Public native writer binds the unchanged two-cut tree to saved geometry."""
    text = 'pdbqt_text:' + control['pdbqt']
    tree = get_torsion_tree(text)
    native = msm.convert(text, to_form='molsysmt.MolSys', discard_torsion_tree=True)
    msm.set(
        native,
        coordinates=puw.quantity(
            puw.get_value(pose.coordinates, to_unit='angstrom')[None], 'angstrom'
        ),
    )
    written = msm.convert(
        native,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        torsion_tree=tree,
    ).removeprefix('pdbqt_text:')
    assert detached_record(tree) == detached_record(
        get_torsion_tree('pdbqt_text:' + written)
    )
    old, new = atom_fields(control['pdbqt']), atom_fields(written)
    assert len(old) == len(new) == 25
    for a, b in zip(old, new, strict=True):
        for field in ('id', 'name', 'group', 'group_id', 'charge_e', 'type'):
            assert a[field] == b[field], field
    np.testing.assert_allclose(
        [a['coordinates'] for a in new],
        puw.get_value(pose.coordinates, to_unit='angstrom'),
        rtol=0,
        atol=0.000500001,
    )
    return written


def fixed_pair(pose, control, receptors):
    before = detached_record(pose.to_dict())
    partner = frozen_partner(control, pose)
    scored = {}
    for name, receptor in receptors.items():
        evaluated = dmt.score(
            dmt.DockingProblem(receptor, partner, reference_box()),
            dmt.VinaProtocol(cpu=1, seed=42, capture_backend_inputs=True),
            pose=pose,
            score_name='fixed',
        )
        assert evaluated.rank == pose.rank
        np.testing.assert_array_equal(
            puw.get_value(evaluated.coordinates, to_unit='angstrom'),
            puw.get_value(pose.coordinates, to_unit='angstrom'),
        )
        history = evaluated.metadata['scoring_history'][-1]
        assert dmt.verify_captured_inputs(history['backend_artifacts'])
        assert history['backend_artifacts']['partner']['sha256'] == sha(
            partner.encode()
        )
        scored[name] = detached_record(evaluated.to_dict())
    assert detached_record(pose.to_dict()) == before
    return scored


def observe(
    source, case, preparation, *, receptor, order, seed, exhaustiveness, ligand='p59'
):
    before = snapshot(source)
    control = case['controls'][order]
    result = dmt.dock(
        dmt.DockingProblem(
            preparation['receptors'][receptor]['pdbqt'],
            control['pdbqt'],
            reference_box(),
        ),
        dmt.VinaProtocol(
            cpu=1,
            seed=seed,
            exhaustiveness=exhaustiveness,
            n_poses=5,
            capture_backend_inputs=True,
        ),
    )
    artifacts = result.provenance['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    assert (
        artifacts['receptor']['sha256'] == preparation['receptors'][receptor]['sha256']
    )
    assert artifacts['partner']['sha256'] == control['sha256']
    assert snapshot(source) == before
    receptors = {k: v['pdbqt'] for k, v in preparation['receptors'].items()}
    scores = [fixed_pair(p, control, receptors) for p in result.poses]
    return {
        'ligand': ligand,
        'receptor': receptor,
        'order': order,
        'result': detached_record(result.to_dict()),
        'heavy_atom_metrics': measure(result, case, control),
        'fixed_scores': scores,
    }


def diagnostic_rows(runs):
    rows = comparison_rows(runs)
    for run, row in zip(runs, rows, strict=True):
        row['receptor'] = run['receptor']
        row['fixed_score_lowest'] = {}
        for receptor in ('sham', 'occupied'):
            best = min(
                range(len(run['fixed_scores'])),
                key=lambda i: (
                    run['fixed_scores'][i][receptor]['scores']['fixed'],
                    run['heavy_atom_metrics'][i]['rank'],
                ),
            )
            row['fixed_score_lowest'][receptor] = {
                'original_rank': run['heavy_atom_metrics'][best]['rank'],
                'recovered': run['heavy_atom_metrics'][best]['recovered'],
                'heavy_rmsd_angstrom': run['heavy_atom_metrics'][best][
                    'heavy_atom_positional_rmsd_angstrom'
                ],
                'total_kcal_mol': run['fixed_scores'][best][receptor]['scores'][
                    'fixed'
                ],
            }
    return rows


def qualify(arm, output):
    proof = producer_proof()
    sources, cases = prepare_cases()
    preparation = prepare_receptors()
    assert cases == load_baseline()['cases']
    receptor, order = arm.split('_', 1)
    record = {
        'arm': arm,
        'proof': proof,
        'cases': cases,
        'preparation': preparation,
        'runs': [],
        'complete': False,
        'consumer_base_commit': subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'], text=True
        ).strip(),
    }
    for effort, seed in itertools.product((1, 8), (7, 42, 2026)):
        record['runs'].append(
            observe(
                sources['p59'],
                cases['p59'],
                preparation,
                receptor=receptor,
                order=order,
                seed=seed,
                exhaustiveness=effort,
            )
        )
        record['complete'] = len(record['runs']) == 6
        save(record, output)
        print(
            f'{arm}: {len(record["runs"])}/6, seed={seed}, effort={effort}',
            file=sys.stderr,
            flush=True,
        )


def assemble(paths):
    parts = [json.loads(gzip.decompress(p.read_bytes())) for p in paths]
    assert {p['arm'] for p in parts} == set(ARMS) and len(parts) == 4
    proof = producer_proof()
    for p in parts:
        assert p['complete'] and len(p['runs']) == 6 and p['proof'] == proof
        for key in ('cases', 'preparation', 'consumer_base_commit'):
            assert p[key] == parts[0][key]
    runs = [r for p in parts for r in p['runs']]
    assert {
        (
            r['receptor'],
            r['order'],
            r['result']['protocol_info']['parameters']['seed'],
            r['result']['protocol_info']['parameters']['exhaustiveness'],
        )
        for r in runs
    } == set(
        itertools.product(
            ('sham', 'occupied'), ('native', 'first_fixed'), (7, 42, 2026), (1, 8)
        )
    )
    historical = []
    for run in load_baseline()['new_runs']:
        if run['ligand'] != 'p59':
            continue
        control = parts[0]['cases']['p59']['controls'][run['order']]
        historical.append(
            {
                'order': run['order'],
                'protocol': run['result']['protocol_info'],
                'fixed_scores': [
                    fixed_pair(
                        p,
                        control,
                        {
                            'original': (DATA / '5x72_receptor.pdbqt').read_text(),
                            'sham': parts[0]['preparation']['receptors']['sham'][
                                'pdbqt'
                            ],
                        },
                    )
                    for p in dmt.DockingResult.from_dict(run['result']).poses
                ],
            }
        )
        print(
            f'historical serialization scores: {len(historical)}/12',
            file=sys.stderr,
            flush=True,
        )
    return {
        'schema': 'dockingmt.5x72_occupancy_audit@1',
        'date': '2026-10-09',
        'python': sys.version,
        'interpreter': sys.executable,
        **proof,
        'consumer_base_commit': parts[0]['consumer_base_commit'],
        'baseline_sha256': BASELINE_SHA,
        'input_sha256': INPUTS,
        'cases': parts[0]['cases'],
        'preparation': parts[0]['preparation'],
        'new_runs': runs,
        'comparison_rows': diagnostic_rows(runs),
        'historical_serialization_scores': historical,
        'criterion': load_baseline()['criterion'],
        'parts': {str(p): sha(p.read_bytes()) for p in paths},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--arm', choices=ARMS)
    parser.add_argument('--parts', nargs=4, type=Path)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.arm:
        qualify(args.arm, args.output)
    elif args.parts:
        save(assemble(args.parts), args.output)
    else:
        parser.error('Supply --arm or four --parts.')
