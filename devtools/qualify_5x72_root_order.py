"""Prespecified single-ligand 5X72 controls against experimental heavy atoms.

The two experimental occupants are searched separately with the other absent.
Only eleven existing ROOT lines are permuted; no molecular writer or matching
algorithm is added. Original crystal SDFs use the explicit RDKit source bridge.
"""

from __future__ import annotations

import argparse
import gzip
import importlib.metadata as metadata
import itertools
import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw
from rdkit import Chem
from vina import Vina

import dockingmt as dmt
from devtools.audit_1iep_preparation import _compare_pdbqt, _compare_torsion_graphs
from devtools.qualify_1iep_representation import sha
from devtools.qualify_1iep_root_order import load_baseline
from devtools.qualify_181l_receptor import save
from devtools.qualify_chemical_templates import detached_record, load_5x72, snapshot
from devtools.qualify_named_types import CHARGE, TYPING
from dockingmt.engines.vina import _pdbqt_atom_records

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'tests/data/vina_torsions'
OUTPUT = ROOT / 'devguide/validation/data/5x72_root_order/audit_2026-10-09.json.gz'
CUTS = [(6, 7), (17, 18)]
NAMES = 'FAX CAS CAT CAU CAV CAW CAL CAH NAG CAE CAD CAC CAB CAA CAF CAJ OAM NAI CAK CAN CAO CAP CAQ CAR'.split()
INPUTS = {
    '5x72.pdb': '3694cbd211e444f0a56150be2fe8ca7f7ed584a7ca448c40d45699ac80490e77',
    '5x72_receptor.pdbqt': '25d4e9b5f3932bc2953152dffc2d9dadf13726ae029e5e88712a0dc9525361e6',
    '5x72_receptor.box.txt': 'e1e87f640b1976109f7358e871e8e63b6f965ad7e76a54b9e848c10518ac3354',
    '5x72_ligand_p59.sdf': 'a476b0d62652664596801fc88024fbd756294e9e2faf9234c8d90c2288aaa373',
    '5x72_ligand_p69.sdf': 'e8c2df94d37439aa558f47eee8f20504d01d11b2d974bbb3cf3d9675a88b1ea1',
    '5x72_ligand_p59H.sdf': 'ef26c05a198a16972efcf8baae644f6b38fd953561f130ee230626088766b08a',
    '5x72_ligand_p69H.sdf': '637a992134b2038a0ea3cff0c1f8355ea232720c9eae5347100b7186170fcdf1',
}
ARMS = [
    f'{name}_{order}' for name in ('p59', 'p69') for order in ('native', 'first_fixed')
]


def xyz(system):
    return puw.get_value(msm.get(system, coordinates=True), to_unit='angstrom')[0]


def reference_box():
    """Read only the six declared keys of this authenticated box fixture."""
    assert (
        sha((DATA / '5x72_receptor.box.txt').read_bytes())
        == INPUTS['5x72_receptor.box.txt']
    )
    values = dict(
        line.split(' = ')
        for line in (DATA / '5x72_receptor.box.txt').read_text().splitlines()
    )
    assert set(values) == {
        f'{kind}_{axis}' for kind in ('center', 'size') for axis in 'xyz'
    }
    return dmt.BoxRegion(
        puw.quantity([float(values[f'center_{a}']) for a in 'xyz'], 'angstrom'),
        puw.quantity([float(values[f'size_{a}']) for a in 'xyz'], 'angstrom'),
    )


def heavy_graph(system):
    """Inspect the explicitly corresponding first 24 atoms of these fixtures."""
    pairs = msm.get(system, element='bond', bonded_atom_pairs=True)
    return {tuple(sorted(map(int, pair))) for pair in pairs if max(pair) < 24}


def prepare_cases():
    """Check crystal identity independently of prepared geometry or pose results."""
    for name, expected in INPUTS.items():
        assert sha((DATA / name).read_bytes()) == expected, name
    crystal = msm.convert(
        DATA / '5x72.pdb', to_form='molsysmt.MolSys', get_missing_bonds=False
    )
    box = reference_box()
    cases = {}
    sources = {}
    for name, stereo, group in [('p59', 'R', 201), ('p69', 'S', 202)]:
        original, source = load_5x72(name)
        before = snapshot(source)
        np.testing.assert_allclose(xyz(original), xyz(source), rtol=0, atol=1e-12)
        molecules = list(
            Chem.SDMolSupplier(str(DATA / f'5x72_ligand_{name}.sdf'), removeHs=False)
        )
        assert len(molecules) == 1 and molecules[0] is not None
        reference = msm.convert(molecules[0], to_form='molsysmt.MolSys')
        bound = msm.extract(crystal, selection=f"group_name=='{name.upper()}'")
        assert msm.get(bound, element='atom', atom_name=True) == NAMES
        assert set(msm.get(bound, element='atom', group_id=True)) == {str(group)}
        assert set(msm.get(bound, element='atom', chain_id=True)) == {'A'}
        assert msm.get(reference, n_atoms=True) == 24
        elements = msm.get(source, element='atom', atom_type=True)
        assert elements[:24] == msm.get(reference, element='atom', atom_type=True)
        assert elements[:24] == msm.get(bound, element='atom', atom_type=True)
        assert elements[24:] == ['H'] * 15
        assert heavy_graph(reference) == heavy_graph(source)
        assert len(heavy_graph(reference)) == 27
        assert msm.get(source, element='atom', atom_stereochemistry=True)[7] == stereo
        assert (
            msm.get(reference, element='atom', atom_stereochemistry=True)[7] == stereo
        )
        np.testing.assert_allclose(xyz(reference), xyz(bound), rtol=0, atol=1e-12)
        assert all(box.contains(puw.quantity(c, 'angstrom')) for c in xyz(reference))
        assert not any(box.contains(puw.quantity(c, 'angstrom')) for c in xyz(source))
        ligand = dmt.prepare_ligand(
            source,
            selection='all',
            active_torsion_bonds=CUTS,
            charge_options=CHARGE,
            typing_options=TYPING,
        )
        assert snapshot(source) == before
        indices = [
            ligand.metadata['retained_atom_indices'][i]
            for i in ligand.pdbqt_atom_indices
        ]
        assert indices == list(range(7, 18)) + [29, 6] + list(range(6)) + list(
            range(18, 24)
        )
        lines = ligand.to_pdbqt().encode().splitlines(keepends=True)
        first, last = lines.index(b'ROOT\n') + 1, lines.index(b'ENDROOT\n')
        assert last - first == 12
        variants = {
            'native': (b''.join(lines), indices),
            'first_fixed': (
                b''.join(
                    lines[: first + 1] + lines[first + 1 : last][::-1] + lines[last:]
                ),
                indices[:1] + indices[1:12][::-1] + indices[12:],
            ),
        }
        controls = {}
        for order, (content, mapping) in variants.items():
            comparison = _compare_pdbqt(b''.join(lines), content)
            tree = _compare_torsion_graphs(b''.join(lines), content)
            assert comparison['coordinate_matched_atoms'] == 25
            assert comparison['matched_atom_type_disagreements'] == 0
            assert comparison['matched_charge_max_absolute_difference_e'] == 0
            assert tree['branch_bonds_match'] and tree['rigid_fragments_match']
            assert comparison['reference_torsion_dof'] == 2
            records = _pdbqt_atom_records(content.decode())
            np.testing.assert_allclose(
                [r[1] for r in records], xyz(source)[mapping], rtol=0, atol=0.000501
            )
            Vina(cpu=1, verbosity=0).set_ligand_from_string(content.decode())
            heavy = [i for i, atom in enumerate(mapping) if atom < 24]
            assert sorted(mapping[i] for i in heavy) == list(range(24))
            controls[order] = {
                'pdbqt': content.decode(),
                'sha256': sha(content),
                'pdbqt_to_source_atom_indices': mapping,
                'heavy_pdbqt_indices': heavy,
                'heavy_pdbqt_to_reference_atom_indices': [mapping[i] for i in heavy],
                'rigid_body_origin_angstrom': list(records[0][1]),
                'first_root_source_atom_index': mapping[0],
                'atom_comparison': comparison,
                'torsion_graph_comparison': tree,
            }
        assert (
            controls['native']['rigid_body_origin_angstrom']
            == controls['first_fixed']['rigid_body_origin_angstrom']
        )
        cases[name] = {
            'source_snapshot': before,
            'original_native_snapshot': snapshot(original),
            'reference_snapshot': snapshot(reference),
            'reference_coordinates_angstrom': xyz(reference).tolist(),
            'reference_pdb_atom_names_in_source_order': NAMES,
            'reference_group_id': group,
            'reference_stereochemistry': stereo,
            'active_torsion_bonds': CUTS,
            'source_to_reference_heavy_atom_indices': list(range(24)),
            'charge_audit': dmt.audit_preparation_charges(ligand),
            'preparation_assessment': dmt.assess_preparation(ligand),
            'controls': controls,
        }
        sources[name] = source
    return sources, detached_record(cases)


def measure(result, case, control):
    """Use public positional RMSD on the explicitly declared heavy population."""
    indices = control['heavy_pdbqt_indices']
    mapped = control['heavy_pdbqt_to_reference_atom_indices']
    reference = np.asarray(case['reference_coordinates_angstrom'])[mapped]
    rows = []
    for pose in result.poses:
        coordinates = puw.get_value(pose.coordinates, to_unit='angstrom')[indices]
        rmsd = float(
            puw.get_value(
                msm.structure.get_rmsd(
                    puw.quantity(coordinates[None], 'angstrom'),
                    selection='all',
                    reference_molecular_system=puw.quantity(
                        reference[None], 'angstrom'
                    ),
                    use_gpu=False,
                ),
                to_unit='angstrom',
            )[0]
        )
        independent = float(
            np.sqrt(np.mean(np.sum((coordinates - reference) ** 2, axis=1)))
        )
        np.testing.assert_allclose(rmsd, independent, rtol=0, atol=1e-10)
        rows.append(
            {
                'rank': pose.rank,
                'heavy_atom_positional_rmsd_angstrom': rmsd,
                'recovered': rmsd <= 2.5,
                'vina_score_kcal_mol': pose.scores['vina'],
            }
        )
    return rows


def observe(source, case, *, name, order, seed, exhaustiveness):
    control = case['controls'][order]
    before = snapshot(source)
    result = dmt.dock(
        dmt.DockingProblem(
            DATA / '5x72_receptor.pdbqt',
            control['pdbqt'],
            reference_box(),
            metadata={'case': name, 'order': order, 'other_ligand': 'absent'},
        ),
        dmt.VinaProtocol(
            cpu=1,
            seed=seed,
            exhaustiveness=exhaustiveness,
            n_poses=5,
            capture_backend_inputs=True,
        ),
    )
    saved = detached_record(result.to_dict())
    restored = dmt.DockingResult.from_dict(saved)
    assert restored.poses and all(p.n_atoms == 25 for p in restored.poses)
    artifacts = restored.provenance['backend_artifacts']
    assert dmt.verify_captured_inputs(artifacts)
    assert artifacts['partner']['sha256'] == control['sha256']
    assert artifacts['receptor']['sha256'] == INPUTS['5x72_receptor.pdbqt']
    assert snapshot(source) == before
    return {
        'ligand': name,
        'order': order,
        'result': saved,
        'heavy_atom_metrics': measure(restored, case, control),
    }


def producer_proof():
    """Authenticate the preserved profile, without reusing historical searches."""
    historical = load_baseline(verify_profile=True)
    provider = Path(msm.__file__).resolve().parents[1]
    extra = [
        'molsysmt/structure/get_rmsd.py',
        'molsysmt/_private/ctfile.py',
        'molsysmt/form/file_pdb/to_molsysmt_MolSys.py',
        'molsysmt/form/file_sdf/to_molsysmt_MolSys.py',
        'molsysmt/form/rdkit_Mol/to_molsysmt_MolSys.py',
    ]
    proof = dict(historical['provider_source_sha256'])
    for relative in extra:
        expected = subprocess.check_output(
            [
                'git',
                '-C',
                str(ROOT.parent / 'molsysmt'),
                'show',
                f'{historical["qualified_provider_commit"]}:{relative}',
            ]
        )
        assert (provider / relative).read_bytes() == expected, relative
        proof[relative] = sha(expected)
    return {
        'qualified_provider_commit': historical['qualified_provider_commit'],
        'provider_module': str(Path(msm.__file__).resolve()),
        'provider_source_sha256': proof,
        'provider_native_artifacts': historical['provider_native_artifacts'],
        'producer_versions': {
            n: metadata.version(n)
            for n in ('molsysmt', 'argdigest', 'pyunitwizard', 'rdkit', 'vina')
        },
        'consumer_source_sha256': {
            str(p.relative_to(ROOT)): sha(p.read_bytes())
            for p in [
                *sorted((ROOT / 'dockingmt').rglob('*.py')),
                Path(__file__),
                ROOT / 'devtools/qualify_chemical_templates.py',
                ROOT / 'devtools/qualify_named_types.py',
                ROOT / 'devtools/audit_1iep_preparation.py',
                ROOT / 'devtools/qualify_181l_receptor.py',
                ROOT / 'devtools/qualify_1iep_representation.py',
                ROOT / 'devtools/qualify_1iep_root_order.py',
            ]
        },
    }


def comparison_rows(runs):
    return [
        {
            'ligand': r['ligand'],
            'order': r['order'],
            'seed': r['result']['protocol_info']['parameters']['seed'],
            'exhaustiveness': r['result']['protocol_info']['parameters'][
                'exhaustiveness'
            ],
            'poses': len(r['heavy_atom_metrics']),
            'first_heavy_rmsd_angstrom': r['heavy_atom_metrics'][0][
                'heavy_atom_positional_rmsd_angstrom'
            ],
            'closest_heavy_rmsd_angstrom': min(
                m['heavy_atom_positional_rmsd_angstrom']
                for m in r['heavy_atom_metrics']
            ),
            'first_recovered': r['heavy_atom_metrics'][0]['recovered'],
            'returned_set_recovered': any(
                m['recovered'] for m in r['heavy_atom_metrics']
            ),
            'first_vina_score_kcal_mol': r['heavy_atom_metrics'][0][
                'vina_score_kcal_mol'
            ],
        }
        for r in runs
    ]


def qualify(arm, output):
    proof = producer_proof()
    sources, cases = prepare_cases()
    name, order = arm.split('_', 1)
    runs = []
    record = {
        'arm': arm,
        'proof': proof,
        'cases': cases,
        'input_sha256': INPUTS,
        'consumer_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'runs': runs,
        'complete': False,
    }
    for effort, seed in itertools.product((1, 8), (7, 42, 2026)):
        runs.append(
            observe(
                sources[name],
                cases[name],
                name=name,
                order=order,
                seed=seed,
                exhaustiveness=effort,
            )
        )
        record['complete'] = len(runs) == 6
        save(record, output)
        print(
            f'{arm}: {len(runs)}/6, seed={seed}, effort={effort}',
            file=sys.stderr,
            flush=True,
        )
    return record


def assemble(paths):
    parts = [json.loads(gzip.decompress(p.read_bytes())) for p in paths]
    assert {p['arm'] for p in parts} == set(ARMS) and len(parts) == 4
    assert all(p['complete'] and len(p['runs']) == 6 for p in parts)
    for p in parts:
        assert p['proof'] == producer_proof()
        assert p['cases'] == parts[0]['cases'] and p['input_sha256'] == INPUTS
        assert p['consumer_base_commit'] == parts[0]['consumer_base_commit']
    runs = [r for p in parts for r in p['runs']]
    cells = {
        (
            r['ligand'],
            r['order'],
            r['result']['protocol_info']['parameters']['seed'],
            r['result']['protocol_info']['parameters']['exhaustiveness'],
        )
        for r in runs
    }
    assert cells == set(
        itertools.product(
            ('p59', 'p69'), ('native', 'first_fixed'), (7, 42, 2026), (1, 8)
        )
    )
    return {
        'schema': 'dockingmt.5x72_root_order_audit@1',
        'date': '2026-10-09',
        'python': sys.version,
        'interpreter': sys.executable,
        'consumer_base_commit': parts[0]['consumer_base_commit'],
        **parts[0]['proof'],
        'input_sha256': INPUTS,
        'cases': parts[0]['cases'],
        'new_runs': runs,
        'comparison_rows': comparison_rows(runs),
        'criterion': {
            'metric': 'positional_rmsd',
            'atom_population': '24_experimental_heavy_atoms',
            'cutoff_angstrom': 2.5,
            'alignment': False,
            'symmetry_correction': False,
        },
        'parts': {str(p): sha(p.read_bytes()) for p in paths},
        'limits': [
            'Each ligand is searched independently, with the other experimental occupant absent; not simultaneous-ligand docking.',
            'One independent complex with two chemically related enantiomers; no dataset recovery probability or convergence claim.',
            'Prepared SDF geometries are not crystal coordinates. Explicit indexed graph/element/stereo checks establish this bounded reference map only.',
            'No experimental H reference is manufactured. Public MolSysMT RMSD uses the 24-heavy-atom population, independently recomputed from all saved poses.',
            'Eleven ROOT lines reversed while the first source atom 7/origin remains fixed. No default root, torsion, conformer or representation policy is selected.',
            'Original prepared coordinates lie outside the box. Search admission does not imply fixed-input scoring admission; no such score is requested.',
            'External receptor and explicit preparation decisions remain unassessed; energies do not establish affinities or stereoselectivity.',
            'Explicit RDKit reference bridge retains unversioned SDF bytes; native dialect decision remains MolSysMT #215.',
            'Preserved source/native profile, original bytes and identities; no new installed artifact, native build provenance, public dependency closure or platform admission.',
        ],
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
        parser.error('Supply --arm or the four --parts.')
    print(json.dumps({'output': str(args.output)}))
