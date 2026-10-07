"""Audit one explicitly declared 181L receptor and bounded BNZ redocking.

This is a fixture-specific composition of public provider operations. Residue
choices and atom maps are caller declarations, not a protonation/matching tool.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.metadata as metadata
import json
import subprocess
import sys
import warnings
from collections import Counter
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

import dockingmt as dmt
from devtools.qualify_chemical_templates import (
    detached_record,
    load_181l_benzene,
    snapshot,
    template_options,
)
from devtools.qualify_named_types import CHARGE, HYDROGEN, TYPING

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_REVISION = '5bd893c85fe8d211663b2b1f865f5f1d2c382a90'
OUTPUT = ROOT / 'devguide/validation/data/181l_receptor/audit_2026-10-06.json.gz'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atom_keys(system):
    """Fixture map keys in the selected native group domain."""
    return list(
        zip(
            msm.get(system, element='atom', group_index=True),
            msm.get(system, element='atom', atom_name=True),
        )
    )


def rejection(operation):
    """Retain the provider failure; unexpected admission stops qualification."""
    try:
        operation()
    except msm.StructuralInconsistencyError as exc:
        return {'exception': type(exc).__name__, 'message': str(exc)}
    raise AssertionError('The undeclared chemical source was unexpectedly admitted.')


def prepare_case():
    """Return preparations, experimental reference and detached audit evidence."""
    path = Path(msm.systems['T4 lysozyme L99A']['181l.pdb'])
    source = msm.convert(path, to_form='molsysmt.MolSys')
    before = snapshot(source)
    selected_indices = msm.select(source, selection="molecule_type=='protein'")
    receptor = msm.extract(source, selection=selected_indices, structure_indices=0)
    original = snapshot(receptor)
    original_keys = atom_keys(receptor)
    residue_names = list(msm.get(receptor, element='group', group_name=True))
    # These are explicit hypotheses for this fixture, without a pH calculation.
    declared_residues = ['HIE' if name == 'HIS' else name for name in residue_names]
    factory = msm.physchem.get_peptide_chemical_template(
        declared_residues,
        n_terminal_state='ammonium',
        c_terminal_state='carboxylate',
        disulfide_group_pairs=None,
    )
    template = factory['template']
    template_keys = atom_keys(template)
    missing = sorted(set(template_keys) - set(original_keys))
    assert missing == [(161, 'OXT')]
    negative = {
        'unprepared_typing': rejection(
            lambda: msm.build.assign_autodock_atom_types(receptor, **TYPING)
        ),
        'unprepared_fixed_h': rejection(
            lambda: msm.build.add_missing_hydrogens(receptor, **HYDROGEN)
        ),
    }
    captured_warnings = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        repaired = msm.build.add_missing_terminal_cappings(
            receptor, N_terminal=None, C_terminal=None, engine='MolSysMT'
        )
        captured_warnings.extend(
            {'category': type(w.message).__name__, 'message': str(w.message)}
            for w in caught
        )
    # Terminal repair supplies geometry, not protonation. Require this fixture's
    # observed result to contain only the one new heavy atom, with no H removal.
    assert msm.get(repaired, n_atoms=True) == 1290
    assert Counter(msm.get(repaired, element='atom', atom_type=True))['H'] == 0
    repaired_keys = atom_keys(repaired)
    assert len(set(repaired_keys)) == len(repaired_keys)
    assert set(repaired_keys) == set(template_keys)
    lookup = {key: index for index, key in enumerate(repaired_keys)}
    original_to_repaired = [lookup[key] for key in original_keys]
    original_ids = list(msm.get(receptor, element='atom', atom_id=True))
    repaired_ids = list(msm.get(repaired, element='atom', atom_id=True))
    assert [repaired_ids[i] for i in original_to_repaired] == original_ids
    np.testing.assert_allclose(
        puw.get_value(msm.get(repaired, coordinates=True), to_unit='nm')[
            :, original_to_repaired, :
        ],
        puw.get_value(msm.get(receptor, coordinates=True), to_unit='nm'),
        rtol=0,
        atol=1e-12,
    )
    correspondence = np.asarray(
        [(index, lookup[key]) for index, key in enumerate(template_keys)], dtype=int
    )
    options = {
        'template': template,
        'atom_correspondence': correspondence,
        'template_provenance': {
            **factory['template_provenance'],
            'hydrogen_policy': 'stored_counts',
        },
    }
    application = msm.physchem.apply_chemical_template(repaired, **options)
    hydrogen = msm.build.add_missing_hydrogens(
        application['molecular_system'],
        **HYDROGEN,
        return_report=True,
        attribute_policy='strict',
    )
    assert hydrogen['report']['n_added_hydrogens'] == 1313
    # Explicit fixture naming through the owning public setter, before mechanical
    # assignments are bound. IDs and historical generation reports stay original.
    expanded = hydrogen['molecular_system']
    generated_indices = list(range(1290, 2603))
    names = list(msm.get(expanded, element='atom', atom_name=True))
    ids = list(msm.get(expanded, element='atom', atom_id=True))
    generated_names = [f'H{i:03X}' for i in generated_indices]
    naming_map = [
        {'atom_index': i, 'atom_id': ids[i], 'original_name': names[i], 'name': name}
        for i, name in zip(generated_indices, generated_names)
    ]
    msm.set(
        expanded,
        element='atom',
        selection=generated_indices,
        atom_name=generated_names,
    )
    charged = msm.build.assign_partial_charges(expanded, **CHARGE, return_report=True)
    prepared = dmt.prepare_receptor(
        charged['molecular_system'],
        selection='all',
        state_id='181L-explicit-HIE-ammonium-carboxylate',
        typing_options=TYPING,
    )
    charge_audit = dmt.audit_preparation_charges(prepared)
    assert charge_audit['assessment'] == 'consistent'
    assert abs(charge_audit['total_charge'] - 8) < 1e-8
    assert dmt.assess_preparation(prepared)['assessment'] == 'unassessed'
    bnz, benzene_template, ligand_full_indices = load_181l_benzene()
    ligand_application = msm.physchem.apply_chemical_template(
        bnz,
        **template_options(
            benzene_template,
            np.column_stack((np.arange(6), np.arange(6))),
            identity='Explicit heavy-only benzene SMILES template',
            uri='smiles:c1ccccc1',
            hydrogen_policy='stored_counts',
        ),
    )
    ligand = dmt.prepare_ligand(
        ligand_application['molecular_system'],
        selection='all',
        state_id='181L-BNZ-explicit-benzene',
        hydrogen_options={**HYDROGEN, 'attribute_policy': 'intersection'},
        charge_options=CHARGE,
        typing_options=TYPING,
        active_torsion_bonds=[],
    )
    assert ligand.n_atoms == 6
    assert snapshot(receptor) == original
    assert snapshot(source) == before
    expanded_coords = puw.get_value(
        msm.get(charged['molecular_system'], coordinates=True), to_unit='nm'
    )
    np.testing.assert_allclose(
        expanded_coords[:, original_to_repaired, :],
        puw.get_value(msm.get(receptor, coordinates=True), to_unit='nm'),
        rtol=0,
        atol=1e-12,
    )
    decisions = {
        'source_file_sha256': digest(path),
        'structure_index': 0,
        'receptor_full_source_atom_indices': [int(i) for i in selected_indices],
        'ligand_full_source_atom_indices': [int(i) for i in ligand_full_indices],
        'original_residue_names': residue_names,
        'declared_residue_states': declared_residues,
        'histidine_group_indices': [
            i for i, n in enumerate(residue_names) if n == 'HIS'
        ],
        'n_terminal_state': 'ammonium',
        'c_terminal_state': 'carboxylate',
        'disulfide_group_pairs': [],
        'pH': None,
        'protonation_basis': 'caller_declared_hypothesis_without_environmental_prediction',
        'water_policy': 'exclude_all_observed_waters',
        'other_components_policy': 'exclude_all_nonprotein_components_except_BNZ_partner',
        'charge_options': CHARGE,
        'typing_options': TYPING,
        'hydrogen_options': HYDROGEN,
        'ligand_active_torsion_bonds': [],
        'receptor_refinement': 'none',
        'generated_H_name_policy': 'explicit H plus three uppercase hexadecimal atom-index digits',
        'generated_H_name_map': naming_map,
        'source_to_repaired_atom_indices': original_to_repaired,
        'repaired_to_full_source_atom_indices': [
            int(selected_indices[original_keys.index(key)])
            if key in original_keys
            else None
            for key in repaired_keys
        ],
        'new_OXT_repaired_atom_index': lookup[(161, 'OXT')],
        'OXT_geometry_method': 'public MolSysMT native terminal completion',
    }
    record = {
        'decisions': decisions,
        'original_source_snapshot': before,
        'original_receptor_snapshot': original,
        'repaired_snapshot': snapshot(repaired),
        'template_report': factory['report'],
        'application_report': application['report'],
        'hydrogen_report': hydrogen['report'],
        'charge_report': charged['report'],
        'expanded_receptor_snapshot': snapshot(charged['molecular_system']),
        'receptor_preparation': prepared.to_dict(),
        'receptor_charge_audit': charge_audit,
        'ligand_application_report': ligand_application['report'],
        'ligand_preparation': ligand.to_dict(),
        'ligand_charge_audit': dmt.audit_preparation_charges(ligand),
        'negative_controls': negative,
        'repair_warnings': captured_warnings,
        'original_source_unchanged': True,
        'experimental_heavy_coordinates_preserved_tolerance_nm': 1e-12,
    }
    return prepared, ligand, bnz, detached_record(record)


def redock(receptor, ligand, reference, decisions, *, seed, exhaustiveness):
    """Use existing public docking/evaluation APIs and retain exact submitted bytes."""
    problem = dmt.DockingProblem(
        receptor,
        ligand,
        dmt.BoxRegion.from_points(
            msm.get(reference, coordinates=True)[0], padding=puw.quantity(8, 'angstrom')
        ),
        metadata={'preparation_decisions': decisions, 'qualification': 'bounded_181L'},
    )
    protocol = dmt.VinaProtocol(
        cpu=1,
        seed=seed,
        exhaustiveness=exhaustiveness,
        n_poses=5,
        capture_backend_inputs=True,
    )
    result = dmt.dock(problem, protocol)
    saved = detached_record(result.to_dict())
    restored = dmt.DockingResult.from_dict(saved)
    assert restored.problem_info['metadata']['preparation_decisions'] == decisions
    dmt.verify_captured_inputs(restored.provenance['backend_artifacts'])
    for role, prepared in [('receptor', receptor), ('partner', ligand)]:
        provenance = restored.provenance['preparation'][role]
        assert provenance['assessment'] == 'unassessed'
        assert (
            provenance['metadata']['atom_type_assignment']
            == prepared.metadata['atom_type_assignment']
        )
        assert (
            provenance['metadata']['charge_projection']
            == prepared.metadata['charge_projection']
        )
    evaluation = dmt.evaluate_redocking(
        restored,
        reference,
        rmsd_cutoff=puw.quantity(2.5, 'angstrom'),
        reference_info={
            'pdb_id': '181L',
            'group_name': 'BNZ',
            'scope': 'observed_six_C',
        },
    )
    return {'result': saved, 'evaluation': evaluation}


def qualify():
    """Run the real-source audit plus six declared search controls."""
    provider_root = Path(msm.__file__).resolve().parents[1]
    provider_files = (
        'molsysmt/physchem/get_peptide_chemical_template.py',
        'molsysmt/_private/peptide_chemical_template.py',
        'molsysmt/_private/chemical_template.py',
        'molsysmt/build/add_missing_terminal_cappings.py',
        'molsysmt/build/_native_placers.py',
        'molsysmt/_private/fixed_hydrogens.py',
        'molsysmt/_private/autodock_assignment.py',
        'molsysmt/_private/partial_charges.py',
    )
    proof = {}
    for relative in provider_files:
        actual = (provider_root / relative).read_bytes()
        committed = subprocess.check_output(
            [
                'git',
                '-C',
                str(ROOT.parent / 'molsysmt'),
                'show',
                f'{PROVIDER_REVISION}:{relative}',
            ]
        )
        assert actual == committed, f'Provider source mismatch: {relative}'
        proof[relative] = digest(provider_root / relative)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        receptor, ligand, reference, audit = prepare_case()
        runs = [
            redock(
                receptor,
                ligand,
                reference,
                audit['decisions'],
                seed=seed,
                exhaustiveness=e,
            )
            for e in (1, 8)
            for seed in (7, 42, 2026)
        ]
    return {
        'schema': 'dockingmt.181l_receptor_audit@1',
        'date': '2026-10-06',
        'interpreter': sys.executable,
        'python': sys.version,
        'provider_module': str(Path(msm.__file__).resolve()),
        'qualified_provider_commit': PROVIDER_REVISION,
        'provider_source_sha256': proof,
        'provider_native_artifacts': {
            str(path): digest(path)
            for path in provider_root.joinpath('molsysmt').glob('_rust*.so')
        },
        'producer_versions': {
            name: metadata.version(name)
            for name in (
                'molsysmt',
                'argdigest',
                'molsysviewer',
                'pyunitwizard',
                'rdkit',
                'vina',
            )
        },
        'consumer_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'consumer_source_sha256': {
            str(path.relative_to(ROOT)): digest(path)
            for path in [
                *sorted(ROOT.joinpath('dockingmt').rglob('*.py')),
                Path(__file__),
            ]
        },
        'audit': audit,
        'redocking_runs': runs,
        'warnings': [
            {'category': type(w.message).__name__, 'message': str(w.message)}
            for w in caught
        ],
        'limits': [
            'One explicit receptor hypothesis, not predicted protonation or a biological preparation certificate.',
            'HIE, charged termini and excluded waters are recorded choices; their scientific suitability is unassessed.',
            'OXT and H geometry are generated by declared provider tools without environmental refinement (molsysmt#323).',
            'Gasteiger charges and chemical_environment@1 types identify executed models, not universal scoring validity.',
            'Vina parsing and near-native recovery do not independently validate chemical preparation or affinity.',
            'Six search controls on one rigid symmetric ligand are not a benchmark population.',
            'RMSD uses source identities without symmetry correction (molsysmt#310) or alignment.',
            'Temporary consumer projection/export remains under molsysmt#223; no AD4, H5MSM mechanics or public artifact qualification.',
            'Python 3.14 source evidence only; other Python minors, clean installed artifacts and hosted CI remain outstanding.',
            'Native artifact digest does not provide fresh build provenance; prior host dependency conflicts remain unresolved.',
        ],
    }


def save(record, path=OUTPUT):
    """Retain finite original evidence, with reproducible gzip container bytes."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        detached_record(record), sort_keys=True, allow_nan=False
    ).encode()
    path.write_bytes(gzip.compress(payload, mtime=0))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    evidence = qualify()
    save(evidence, args.output)
    print(
        json.dumps(
            {
                'output': str(args.output),
                'redocking_runs': len(evidence['redocking_runs']),
            }
        )
    )
