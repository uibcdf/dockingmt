"""Qualify explicit provider H/charge stages, including original 181L BNZ."""

import hashlib
import importlib.metadata as metadata
import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw
from molsysmt.native import Structures
from vina import Vina

import dockingmt as dmt
from devtools.qualify_chemical_templates import (
    detached_record,
    load_181l_benzene,
    snapshot,
    template_options,
)

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_REVISION = '5bd893c85fe8d211663b2b1f865f5f1d2c382a90'
OUTPUT = ROOT / 'devguide/validation/data/ligand_stages/qualification_2026-10-06.json'
HYDROGEN = {'mode': 'fixed_chemical_state', 'pH': None, 'engine': 'RDKit'}
CHARGE = {'method': 'gasteiger_marsili'}


def polar_source():
    """Declare a synthetic methanol pose through public provider composition."""
    native = msm.convert(
        msm.convert('smiles:CO', to_form='rdkit.Mol'), to_form='molsysmt.MolSys'
    )
    pose = Structures(coordinates=puw.quantity([[[0, 0, 0], [1.4, 0, 0]]], 'angstrom'))
    return msm.convert([native, pose], to_form='molsysmt.MolSys')


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def qualify():
    provider_root = Path(msm.__file__).resolve().parents[1]
    proof = {}
    for relative in (
        'molsysmt/build/add_missing_hydrogens.py',
        'molsysmt/_private/fixed_hydrogens.py',
        'molsysmt/build/assign_partial_charges.py',
        'molsysmt/_private/partial_charges.py',
    ):
        actual = (provider_root / relative).read_bytes()
        published = subprocess.check_output(
            [
                'git',
                '-C',
                str(ROOT.parent / 'molsysmt'),
                'show',
                f'{PROVIDER_REVISION}:{relative}',
            ]
        )
        assert actual == published
        proof[relative] = hashlib.sha256(actual).hexdigest()
    source = polar_source()
    before = snapshot(source)
    prepared = dmt.prepare_ligand(
        source, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
    )
    assert snapshot(source) == before
    assert prepared.metadata['preparation_workflow'][
        'prepared_to_input_atom_indices'
    ] == [0, 1, None]
    audit = dmt.audit_preparation_charges(prepared)
    assert audit['assessment'] == 'consistent'
    assert abs(audit['total_charge']) < 1e-12
    sites = msm.physchem.get_hbond_sites(prepared.source_molsys)
    assert sites['donor_hydrogen_pairs'].tolist() == [[1, 2]]
    text = prepared.to_pdbqt()
    Vina(cpu=1, verbosity=0).set_ligand_from_string(text)
    full = msm.build.add_missing_hydrogens(
        source, attribute_policy='strict', **HYDROGEN
    )
    idempotent = dmt.prepare_ligand(
        full, selection='all', hydrogen_options=HYDROGEN, charge_options=CHARGE
    )
    assert (
        idempotent.metadata['preparation_workflow']['hydrogen_addition'][
            'n_added_hydrogens'
        ]
        == 0
    )
    bnz_source, template, full_indices = load_181l_benzene()
    options = template_options(
        template,
        np.column_stack((np.arange(6), np.arange(6))),
        identity='Explicit heavy-only benzene SMILES template',
        uri='smiles:c1ccccc1',
        hydrogen_policy='stored_counts',
    )
    application = msm.physchem.apply_chemical_template(bnz_source, **options)
    applied = application['molecular_system']
    before_bnz = snapshot(applied)
    benzene = dmt.prepare_ligand(
        applied,
        selection='all',
        hydrogen_options={**HYDROGEN, 'attribute_policy': 'intersection'},
        charge_options=CHARGE,
    )
    workflow = benzene.metadata['preparation_workflow']
    hydrogen = workflow['hydrogen_addition']
    assert hydrogen['n_added_hydrogens'] == 6
    assert hydrogen['dropped_attributes'] == ['b_factor', 'occupancy']
    assert hydrogen['coordinate_evidence'] == 'generated_local_geometry'
    assert workflow['prepared_to_input_atom_indices'] == list(range(6))
    assert workflow['pdbqt_to_input_atom_indices'] == list(range(6))
    assert benzene.atom_types == ['A'] * 6
    np.testing.assert_array_equal(
        puw.get_value(benzene.coordinates, to_unit='nm')[None],
        before_bnz['structures']['coordinates'],
    )
    assert msm.get(benzene.source_molsys, element='atom', atom_id=True) == msm.get(
        applied, element='atom', atom_id=True
    )
    benzene_audit = dmt.audit_preparation_charges(benzene)
    assert benzene_audit['assessment'] == 'consistent'
    assert benzene_audit['partial_charge_assignment']['n_atoms'] == 12
    assert len(benzene_audit['charge_projection']['transfers']) == 6
    assert abs(benzene_audit['total_charge']) < 1e-10
    Vina(cpu=1, verbosity=0).set_ligand_from_string(benzene.to_pdbqt())
    assert snapshot(applied) == before_bnz
    return {
        'schema_version': '1.0',
        'qualification': 'explicit_ligand_preparation_stages',
        'interpreter': sys.executable,
        'python': sys.version,
        'qualified_provider_commit': PROVIDER_REVISION,
        'provider_source_sha256': proof,
        'distribution_versions': {
            name: metadata.version(name)
            for name in ('dockingmt', 'molsysmt', 'rdkit', 'vina')
        },
        'version_limit': 'Original producer distribution versions are retained separately from exact loaded source qualification.',
        'dockingmt_source_sha256': {
            relative: _digest(ROOT / relative)
            for relative in (
                'dockingmt/preparation/_stages.py',
                'dockingmt/preparation/_molsys.py',
                'dockingmt/preparation/ligand.py',
                'devtools/qualify_ligand_stages.py',
                'devtools/qualify_chemical_templates.py',
            )
        },
        'polar_control': {
            'source_smiles': 'CO',
            'source_snapshot': before,
            'prepared': prepared.to_dict(),
            'charge_audit': audit,
            'hbond_sites': detached_record(sites),
            'pdbqt_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'vina_parser_admitted': True,
            'source_unchanged': True,
        },
        'idempotent_control': {
            'prepared': idempotent.to_dict(),
            'existing_coordinates_preserved': True,
        },
        '181l_bnz': {
            'full_source_atom_indices': full_indices,
            'input_sha256': _digest(msm.systems['T4 lysozyme L99A']['181l.pdb']),
            'template_application_report': detached_record(application['report']),
            'applied_snapshot': before_bnz,
            'prepared': benzene.to_dict(),
            'hydrogen_addition': hydrogen,
            'charge_audit': benzene_audit,
            'vina_parser_admitted': True,
            'source_unchanged': True,
            'status': 'software_qualified_provisional_typing',
        },
        'limits': [
            'Original BNZ is qualified only for the declared template, fixed-state H and named-charge software route.',
            'Generated local H geometry is not receptor or energy refinement.',
            'AutoDock typing and the default provisional gate remain unchanged.',
            'Charge projection/writing remains the existing temporary consumer profile (#223).',
            'Template history is retained natively; H5MSM cannot retain a nonempty MolecularMechanics domain.',
            'An explicit-H SDF can still lack the stored virtual-H counts required by fixed-state addition.',
            'The public composition route emits its existing atom_index off-axis diagnostic; source identity/coordinates are checked.',
            'Source qualification and original producer versions do not establish public artifact or biological acceptance.',
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
                'polar_prepared_atoms': record['polar_control']['prepared']['n_atoms'],
                'polar_charge_audit': record['polar_control']['charge_audit'][
                    'assessment'
                ],
                'bnz': record['181l_bnz']['status'],
            },
            indent=2,
        )
    )
