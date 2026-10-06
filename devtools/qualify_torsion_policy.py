"""Bounded explicit torsion choices over native MolSysMT graph criteria.

Original curated SDF files retain the existing explicit RDKit reader bridge;
classification itself uses the public native provider operation only.
"""

import hashlib
import importlib.metadata as metadata
import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import pyunitwizard as puw
from vina import Vina

import dockingmt as dmt
from devtools.qualify_chemical_templates import load_5x72, record_digest, snapshot
from devtools.qualify_named_types import CHARGE, TYPING, declared_source
from dockingmt._private.smonitor import ArgumentError

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_REVISION = '5bd893c85fe8d211663b2b1f865f5f1d2c382a90'
OUTPUT = ROOT / 'devguide/validation/data/torsion_policy/qualification_2026-10-06.json'
BASELINE = ROOT / 'devguide/validation/data/fragments/legacy_trees.json'


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _observe(source, bonds):
    before = record_digest(snapshot(source))
    prepared = dmt.prepare_ligand(source, selection='all', active_torsion_bonds=bonds)
    assert record_digest(snapshot(source)) == before
    text = prepared.to_pdbqt()
    Vina(cpu=1, verbosity=0).set_ligand_from_string(text)
    return prepared, {
        'prepared': prepared.to_dict(),
        'source_snapshot_sha256': before,
        'source_unchanged': True,
        'pdbqt': text,
        'pdbqt_sha256': hashlib.sha256(text.encode()).hexdigest(),
        'vina_parser_admitted': True,
        'preparation_assessment': dmt.assess_preparation(prepared),
    }


def state_scope_probe():
    """Declare two native graphs to retain the provider #348 capability gap."""
    source = declared_source('CCCCCC')
    assigned = source.topology._append_chemical_state(state_id='assigned-split')
    bonds = source.topology.bonds.drop(index=2).reset_index(drop=True)
    source.topology._set_chemical_state_bonds(bonds, state_index=assigned)
    source.topology._chemical_states[assigned].connectivity_completeness = 'complete'
    source._set_structure_chemical_state_indices([assigned])
    before = record_digest(snapshot(source))
    assigned_fragments = msm.topology.get_rigid_fragments(
        source, chemical_state='structure', structure_indices=0
    )
    legacy_blocks = msm.topology.get_covalent_blocks(source)
    from argdigest.core.errors import UnknownArgumentError

    try:
        msm.topology.get_covalent_blocks(
            source, chemical_state='structure', structure_indices=0
        )
    except UnknownArgumentError as exc:
        failure = {'exception': type(exc).__name__, 'message': str(exc)}
    else:
        raise AssertionError(
            'Provider capability changed; review #348 removal condition.'
        )
    assert assigned_fragments['fragment_offsets'].tolist() == [0, 3, 6]
    assert [sorted(block) for block in legacy_blocks] == [list(range(6))]
    assert record_digest(snapshot(source)) == before
    return {
        'owning_issue': 'uibcdf/molsysmt#348',
        'assigned_fragment_offsets': assigned_fragments['fragment_offsets'].tolist(),
        'reference_default_blocks': [sorted(block) for block in legacy_blocks],
        'explicit_state_request': failure,
        'source_unchanged': True,
    }


def qualify():
    """Retain full producer criteria, original comparison bytes and local limits."""
    provider_root = Path(msm.__file__).resolve().parents[1]
    proof = {}
    for relative in (
        'molsysmt/topology/get_rotatable_bonds.py',
        'molsysmt/topology/get_rigid_fragments.py',
        'molsysmt/topology/_chemical_graph.py',
        'molsysmt/topology/get_covalent_blocks.py',
        'molsysmt/topology/get_bondgraph.py',
    ):
        actual = (provider_root / relative).read_bytes()
        committed = subprocess.check_output(
            ['git', '-C', str(provider_root), 'show', f'{PROVIDER_REVISION}:{relative}']
        )
        assert actual == committed, relative
        proof[relative] = hashlib.sha256(actual).hexdigest()
    original_cases = {}
    from rdkit import Chem

    for case in json.loads(BASELINE.read_text())['cases']:
        suffix = 'H' if case['case'].startswith('5x72') else ''
        path = ROOT / f'tests/data/vina_torsions/{case["case"]}{suffix}.sdf'
        reference = ROOT / f'tests/data/vina_torsions/{case["case"]}.pdbqt'
        assert _digest(path) == case['source_sdf_sha256']
        assert _digest(reference) == case['reference_pdbqt_sha256']
        molecules = list(Chem.SDMolSupplier(str(path), removeHs=False))
        assert len(molecules) == 1 and molecules[0] is not None
        source = msm.convert(molecules[0], to_form='molsysmt.MolSys')
        prepared, observation = _observe(source, case['active_bonds'])
        assert observation['pdbqt_sha256'] == case['generated_pdbqt_sha256']
        assert prepared.pdbqt_atom_indices == case['pdbqt_atom_indices']
        assert (
            prepared.metadata['retained_atom_indices'] == case['retained_atom_indices']
        )
        decisions = prepared.metadata['torsion_selection']['selected_bonds']
        exceptions = [d for d in decisions if d['decision'] == 'explicit_override']
        assert len(exceptions) == (1 if case['case'] == '1s63_ligand' else 0)
        observation.update(
            {
                'original_source_sha256': case['source_sdf_sha256'],
                'original_reference_sha256': case['reference_pdbqt_sha256'],
                'original_bytes_and_permutation_preserved': True,
                'provider_candidate_count': len(
                    prepared.metadata['torsion_selection']['provider_classification'][
                        'rotatable_bond_indices'
                    ]
                ),
            }
        )
        original_cases[case['case']] = observation
    analytical = {}
    for smiles, bond, reasons in [
        ('CCCCCC', (1, 2), []),
        ('CC(=O)OCC', (1, 3), ['restricted_conjugation']),
        ('CC(=O)OCC', (3, 4), []),
        ('CC(=O)SCC', (1, 3), ['restricted_conjugation']),
        ('c1ccccc1C#N', (5, 6), ['adjacent_triple_bond']),
        ('CCC#CCC', (1, 2), ['adjacent_triple_bond']),
    ]:
        source = declared_source(smiles)
        prepared, observation = _observe(source, [bond])
        assert (
            prepared.metadata['torsion_selection']['selected_bonds'][0][
                'provider_exclusion_reasons'
            ]
            == reasons
        )
        analytical[f'{smiles}:{bond}'] = observation
    rejections = {}
    for smiles, bond in [
        ('CC(=O)NCC', (1, 3)),
        ('CC(=S)NCC', (1, 3)),
        ('CC(=N)NCC', (1, 3)),
        ('CC(=O)N(C)CC', (1, 3)),
    ]:
        source = declared_source(smiles)
        before = record_digest(snapshot(source))
        try:
            dmt.prepare_ligand(source, selection='all', active_torsion_bonds=[bond])
        except ArgumentError as exc:
            rejections[smiles] = {'exception': type(exc).__name__, 'message': str(exc)}
        else:
            raise AssertionError('Restricted C-N was admitted.')
        assert record_digest(snapshot(source)) == before
    _, source = load_5x72('p59')
    typed = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(source, **CHARGE), **TYPING
    )
    before = record_digest(snapshot(typed))
    # Keep the existing bounded external receptor fixture: it is unassessed.
    receptor_path = ROOT / 'tests/data/vina_torsions/1iep_receptor.pdbqt'
    center = puw.get_value(msm.get(typed, coordinates=True), to_unit='angstrom')[
        0
    ].mean(axis=0)
    with puw.context(standard_units=['pm', 'fs']):
        problem = dmt.DockingProblem(
            receptor=receptor_path,
            partner=typed,
            search_domain=dmt.BoxRegion(
                puw.quantity(center, 'angstrom'), puw.quantity([20, 20, 20], 'angstrom')
            ),
        )
        result = dmt.dock(
            problem,
            dmt.VinaProtocol(
                cpu=1,
                seed=17,
                exhaustiveness=1,
                n_poses=1,
                active_torsion_bonds=[(6, 7), (17, 18)],
                capture_backend_inputs=True,
            ),
        )
    restored = dmt.DockingResult.from_dict(
        json.loads(json.dumps(result.to_dict(), allow_nan=False))
    )
    assert len(restored.poses) == 1
    report = restored.provenance['preparation']['partner']
    assert report['assessment'] == 'unassessed'
    assert (
        report['metadata']['torsion_selection']['policy'] == 'explicit_docking_cuts@1'
    )
    assert (
        report['metadata']['torsion_selection']['pdbqt_to_source_atom_indices']
        == restored.poses[0].metadata['selected_atom_indices']
    )
    assert record_digest(snapshot(typed)) == before
    captured = dmt.verify_captured_inputs(restored.provenance['backend_artifacts'])
    profile = (
        ROOT
        / 'devguide/validation/data/chemical_templates/source_profile_2026-10-06.json'
    )
    return {
        'schema': 'dockingmt.explicit_torsion_policy_qualification@1',
        'date': '2026-10-06',
        'python': sys.version,
        'interpreter': sys.executable,
        'dockingmt_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'qualified_provider_commit': PROVIDER_REVISION,
        'provider_source_sha256': proof,
        'producer_versions': {
            name: metadata.version(name)
            for name in (
                'molsysmt',
                'argdigest',
                'molsysviewer',
                'rdkit',
                'networkx',
                'vina',
                'pyunitwizard',
            )
        },
        'prior_source_profile': {
            'path': str(profile.relative_to(ROOT)),
            'sha256': _digest(profile),
        },
        'legacy_baseline_sha256': _digest(BASELINE),
        'consumer_implementation_sha256': {
            p: _digest(ROOT / p)
            for p in (
                'dockingmt/preparation/_temporary_torsions.py',
                'dockingmt/preparation/ligand.py',
                'devtools/qualify_torsion_policy.py',
            )
        },
        'original_cases': original_cases,
        'analytical_cases': analytical,
        'restricted_c_n_rejections': rejections,
        'state_scope_gap': state_scope_probe(),
        'default_vina_result': restored.to_dict(),
        'verified_captured_bytes': captured,
        'receptor_input_sha256': _digest(receptor_path),
        'limits': [
            'Experimental provider conjugation_restricted@1 with explicit consumer overrides; no automatic torsion selection or barrier prediction.',
            'Original four SDFs retain the pre-existing explicit RDKit reader bridge; native graph classification itself imports no RDKit/Meeko.',
            'Original PDBQT byte parity is provisional software evidence, not chemically validated ground truth.',
            'The default Vina control pairs a named/charged 5X72 ligand with an unrelated external 1IEP receptor; it tests software/provenance, not biological redocking or affinity.',
            'Provider eligibility/metadata do not qualify scientific preparation/scoring; the default real control remains unassessed.',
            'Existing retained-axis connectivity remains a bounded exception under MolSysMT #348 (review 2027-01-06). PDBQT/H projection stays under #223/#33.',
            'Local Python 3.14 source composition only; no hosted, Python 3.11-3.13, macOS, clean installed or public admission claim.',
            'Prior source profile retains native artifact build-provenance limits, AmberTools host dependency conflicts and unchanged SMonitor/ArgDigest guide drift.',
        ],
    }


def save(record):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(record, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    record = qualify()
    save(record)
    print(
        json.dumps(
            {
                'original_cases': len(record['original_cases']),
                'analytical_cases': len(record['analytical_cases']),
                'default_vina_poses': len(record['default_vina_result']['poses']),
            }
        )
    )
