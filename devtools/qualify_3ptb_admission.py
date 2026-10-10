"""Admit the registered 3PTB inputs through public molecular operations.

The caller supplies authenticated, uncompressed PDB bytes. This case-specific
orchestration performs no scoring, search, molecular repair or format adaptation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory

import molsysmt as msm
import numpy as np
import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from vina import Vina

import dockingmt as dmt
from devtools.qualify_5x72_occupancy import atom_fields
from devtools.qualify_181l_receptor import atom_keys, save
from devtools.qualify_chemical_templates import (
    detached_record,
    snapshot,
    template_options,
)
from devtools.qualify_named_types import CHARGE, HYDROGEN, TYPING
from dockingmt.engines.vina import _vina_box

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'devguide/validation/data/3ptb_prospective'
OUTPUT = ROOT / 'devguide/validation/data/3ptb_admission/audit_2026-10-10.json.gz'
SOURCE_SHA = '288f7954d4d013fa8eab3808e1037e2958e2dcd12c9eca65a3f1014404a9f9a2'
PROTOCOL_SHA = '042fa8a871184ad30278565a8f517583b6079cd874d8d9b26e17159a8b4b49ad'
HANDOFF_SHA = '60e8b4ccfb873666885a570d339f1ddc34d1c630ebf779862f66aa2c665ecf32'
HANDOFF_URL = 'https://github.com/uibcdf/dockingmt/issues/5#issuecomment-6097647900'
PROVIDER = '739395d7ea31bec5c3f77cdcb1135ecf7e7c9bac'
NATIVE_SHA = 'c535c7d2f0e2a92b6ebf8298a60b19e4b5555467b4aa087e9563c6760619827e'
DISULFIDES = [(22, 157), (42, 58), (128, 232), (136, 201), (168, 182), (191, 220)]
LIGAND_NAMES = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C', 'N1', 'N2']


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def registration():
    """Reject changes to the registered scientific and handoff documents."""
    record = json.loads((DATA / 'registration_2026-10-10.json').read_text())
    assert sha((ROOT / record['protocol_file']).read_bytes()) == PROTOCOL_SHA
    assert record['protocol_sha256'] == PROTOCOL_SHA
    handoff = ROOT / 'devguide/validation/3ptb_source_handoff_2026-10-10.md'
    assert sha(handoff.read_bytes()) == HANDOFF_SHA
    return {
        'original': record,
        'handoff': {
            'file': str(handoff.relative_to(ROOT)),
            'sha256': HANDOFF_SHA,
            'registration_url': HANDOFF_URL,
            'provider_issue': 'uibcdf/molsysmt#385',
        },
    }


def xyz(system):
    return puw.get_value(msm.get(system, coordinates=True), to_unit='angstrom')[0]


def original_attributes(system):
    """Retain observed arrays before the explicitly permitted H expansion loss."""
    b_factor = msm.get(system, element='atom', b_factor=True)
    return detached_record(
        {
            'occupancy': msm.get(system, element='atom', occupancy=True),
            'b_factor': puw.get_value(b_factor, to_unit='angstrom**2'),
            'b_factor_unit': 'angstrom**2',
        }
    )


def expand(system, *, receptor):
    before = snapshot(system)
    attributes = original_attributes(system)
    try:
        msm.build.add_missing_hydrogens(
            msm.copy(system), **HYDROGEN, return_report=True, attribute_policy='strict'
        )
    except StructuralInconsistencyError as error:
        rejection = {'exception': type(error).__name__, 'message': str(error)}
        assert 'b_factor' in str(error) and 'occupancy' in str(error)
    else:
        raise AssertionError('Expected the strict atom-expansion attribute rejection')
    result = msm.build.add_missing_hydrogens(
        system, **HYDROGEN, return_report=True, attribute_policy='intersection'
    )
    expanded, report = result['molecular_system'], result['report']
    mapping = np.asarray(report['atom_correspondence'], dtype=int)
    assert mapping.shape == (msm.get(system, n_atoms=True), 2)
    np.testing.assert_array_equal(mapping[:, 0], np.arange(len(mapping)))
    assert len(set(mapping[:, 1])) == len(mapping)
    np.testing.assert_allclose(
        xyz(expanded)[mapping[:, 1]], xyz(system), rtol=0, atol=1e-12
    )
    old_ids = msm.get(system, element='atom', atom_id=True)
    new_ids = msm.get(expanded, element='atom', atom_id=True)
    assert [new_ids[i] for i in mapping[:, 1]] == list(old_ids)
    assert report['original_coordinates_preserved']
    assert sorted(report['dropped_attributes']) == ['b_factor', 'occupancy']
    assert snapshot(system) == before
    names = None
    if receptor:
        generated = [int(pair[1]) for pair in report['parent_hydrogen_pairs']]
        assert len(generated) == report['n_added_hydrogens']
        assert max(generated) < 4096
        names = {
            'indices': generated,
            'original_names': msm.get(
                expanded, element='atom', selection=generated, atom_name=True
            ),
            'export_names': [f'H{i:03X}' for i in generated],
        }
        msm.set(
            expanded,
            element='atom',
            selection=generated,
            atom_name=names['export_names'],
        )
    return expanded, {
        'original_attributes': attributes,
        'strict_policy_rejection': rejection,
        'attribute_policy': 'intersection',
        'hydrogen_report': report,
        'source_unchanged': True,
        'generated_name_assignment': names,
        'expanded_snapshot': snapshot(expanded),
    }


def prepared_evidence(prepared, source_indices):
    text = prepared.to_pdbqt()
    projection = prepared.metadata['atom_type_projection']
    written_to_expanded = projection['pdbqt_to_source_atom_indices']
    retained = projection['retained_source_atom_indices']
    assert set(written_to_expanded) == set(retained)
    assert len(set(written_to_expanded)) == prepared.n_atoms
    order = list(getattr(prepared, 'pdbqt_atom_indices', range(prepared.n_atoms)))
    fields = atom_fields(text)
    assert len(fields) == prepared.n_atoms
    coordinates = puw.get_value(prepared.coordinates, to_unit='angstrom')
    np.testing.assert_allclose(
        [f['coordinates'] for f in fields], coordinates[order], rtol=0, atol=0.000501
    )
    np.testing.assert_allclose(
        [f['charge_e'] for f in fields],
        np.asarray(prepared.charges)[order],
        rtol=0,
        atol=0.000501,
    )
    assert [f['type'] for f in fields] == [prepared.atom_types[i] for i in order]
    assignment = prepared.metadata['atom_type_assignment']
    assert assignment['coverage'] == 'complete'
    assert assignment['rule_version'] == 'chemical_environment@1'
    charge = dmt.audit_preparation_charges(prepared)
    assert charge['assessment'] == 'consistent'
    assessment = dmt.assess_preparation(prepared)
    assert assessment['assessment'] == 'unassessed'
    assert assessment['provisional_reason_codes'] == []
    return {
        'prepared': prepared.to_dict(),
        'coordinates': coordinates,
        'coordinate_unit': 'angstrom',
        'charge_unit': 'elementary_charge',
        'charge_audit': charge,
        'preparation_assessment': assessment,
        'pdbqt': text,
        'pdbqt_sha256': sha(text.encode()),
        'written_fields': fields,
        'pdbqt_to_expanded_atom_indices': written_to_expanded,
        'pdbqt_to_full_source_atom_indices': [
            source_indices[i] if i < len(source_indices) else None
            for i in written_to_expanded
        ],
    }


def admit(path):
    """Execute the bounded admission; return preparations and detached evidence."""
    binding = registration()
    path = Path(path)
    payload = path.read_bytes()
    if sha(payload) != SOURCE_SHA:
        raise ValueError(
            '3PTB plain input differs from the registered original PDB bytes'
        )
    assert path.suffix == '.pdb'
    alternates = sorted(
        {
            line[16]
            for line in payload.decode().splitlines()
            if line.startswith(('ATOM  ', 'HETATM'))
        }
    )
    assert alternates == [' ']
    source = msm.convert(path, to_form='molsysmt.MolSys', get_missing_bonds=False)
    original = snapshot(source)
    counts = msm.get(
        source,
        n_atoms=True,
        n_groups=True,
        n_structures=True,
        n_bonds=True,
        output_type='dictionary',
    )
    assert counts == {
        'n_atoms': 1701,
        'n_groups': 287,
        'n_structures': 1,
        'n_bonds': 21,
    }
    source_attributes = original_attributes(source)
    protein_indices = msm.select(source, selection="molecule_type=='protein'")
    ligand_indices = msm.select(source, selection="group_name=='BEN'")
    receptor = msm.extract(source, selection=protein_indices, structure_indices=0)
    reference = msm.extract(source, selection=ligand_indices, structure_indices=0)
    assert msm.get(receptor, n_atoms=True) == 1629
    assert msm.get(receptor, n_groups=True) == 223
    assert list(msm.get(reference, element='atom', atom_name=True)) == LIGAND_NAMES
    assert list(msm.get(reference, element='atom', atom_id=True)) == [
        str(i) for i in range(1632, 1641)
    ]
    assert set(msm.get(receptor, element='atom', chain_id=True)) == {'A'}
    assert set(msm.get(reference, element='atom', chain_id=True)) == {'A'}
    assert set(msm.get(reference, element='atom', group_id=True)) == {'1'}
    assert msm.get(
        receptor, element='atom', selection="atom_name=='OXT'", atom_id=True
    ) == ['1629']
    original_receptor, original_ligand = snapshot(receptor), snapshot(reference)
    ids = list(msm.get(receptor, element='group', group_id=True))
    names = list(msm.get(receptor, element='group', group_name=True))
    histidines = [(i, str(ids[i])) for i, name in enumerate(names) if name == 'HIS']
    assert histidines == [(22, '40'), (39, '57'), (72, '91')]
    lookup = {str(value): i for i, value in enumerate(ids)}
    pairs = [[lookup[str(a)], lookup[str(b)]] for a, b in DISULFIDES]
    states = names.copy()
    for index, group_id in histidines:
        states[index] = 'HID' if group_id == '57' else 'HIE'
    keys = atom_keys(receptor)
    key_index = {key: i for i, key in enumerate(keys)}
    sulfur_pairs = []
    for left, right in pairs:
        assert names[left] == names[right] == 'CYS'
        states[left] = states[right] = 'CYX'
        sulfur_pairs.append(sorted([key_index[(left, 'SG')], key_index[(right, 'SG')]]))
    source_pairs = msm.get(receptor, element='bond', bonded_atom_pairs=True)
    assert sorted(map(sorted, source_pairs)) == sorted(sulfur_pairs)
    factory = msm.physchem.get_peptide_chemical_template(
        states,
        n_terminal_state='ammonium',
        c_terminal_state='carboxylate',
        disulfide_group_pairs=pairs,
    )
    template = factory['template']
    template_keys = atom_keys(template)
    assert len(set(keys)) == len(keys) and set(keys) == set(template_keys)
    correspondence = np.asarray(
        [(i, key_index[key]) for i, key in enumerate(template_keys)], dtype=int
    )
    options = {
        'template': template,
        'atom_correspondence': correspondence,
        'template_provenance': factory['template_provenance'],
        'connectivity_policy': 'complete_from_template',
    }
    assessment = msm.physchem.assess_chemical_template(receptor, **options)
    assert assessment['status'] == 'compatible'
    application = msm.physchem.apply_chemical_template(receptor, **options)
    receptor_full, receptor_h = expand(application['molecular_system'], receptor=True)
    parents = {
        int(pair[0]) for pair in receptor_h['hydrogen_report']['parent_hydrogen_pairs']
    }
    assert not parents.intersection(i for pair in sulfur_pairs for i in pair)
    for index, group_id in histidines:
        assert (key_index[(index, 'ND1')] in parents) == (group_id == '57')
        assert (key_index[(index, 'NE2')] in parents) == (group_id != '57')
    receptor_charged = msm.build.assign_partial_charges(
        receptor_full, **CHARGE, return_report=True
    )
    charged_receptor = receptor_charged['molecular_system']
    prepared_receptor = dmt.prepare_receptor(
        charged_receptor,
        selection='all',
        state_id='3PTB-HID57-HIE40-HIE91-CYX-ammonium-carboxylate-dry',
        typing_options=TYPING,
    )
    ligand_template = msm.convert(
        msm.convert('smiles:NC(=[NH2+])c1ccccc1', to_form='rdkit.Mol'),
        to_form='molsysmt.MolSys',
    )
    ligand_mapping = np.column_stack((np.arange(9), [8, 6, 7, 0, 1, 2, 3, 4, 5]))
    ligand_options = template_options(
        ligand_template,
        ligand_mapping,
        identity='Explicit benzamidinium +1; N2,C,N1,C1,C2,C3,C4,C5,C6',
        uri='smiles:NC(=[NH2+])c1ccccc1',
        hydrogen_policy='stored_counts',
    )
    ligand_assessment = msm.physchem.assess_chemical_template(
        reference, **ligand_options, connectivity_policy='complete_from_template'
    )
    assert ligand_assessment['status'] == 'compatible'
    ligand_application = msm.physchem.apply_chemical_template(
        reference, **ligand_options, connectivity_policy='complete_from_template'
    )
    ligand_full, ligand_h = expand(
        ligand_application['molecular_system'], receptor=False
    )
    assert (
        list(msm.get(ligand_full, element='atom', formal_charge=True))
        == [0, 0, 0, 0, 0, 0, 0, 1, 0] + [0] * 9
    )
    assert sorted(map(list, ligand_h['hydrogen_report']['parent_hydrogen_pairs'])) == [
        [1, 9],
        [2, 10],
        [3, 11],
        [4, 12],
        [5, 13],
        [7, 14],
        [7, 15],
        [8, 16],
        [8, 17],
    ]
    ligand_charged = msm.build.assign_partial_charges(
        ligand_full, **CHARGE, return_report=True
    )
    charged_ligand = ligand_charged['molecular_system']
    charged_snapshot = snapshot(charged_ligand)
    classification = msm.topology.get_rotatable_bonds(
        charged_ligand, chemical_state='structure', structure_indices=0
    )
    assert list(map(list, classification['rotatable_bonded_atom_pairs'])) == [[0, 6]]
    fragments = msm.topology.get_rigid_fragments(
        charged_ligand,
        bond_indices=classification['rotatable_bond_indices'],
        chemical_state='structure',
        structure_indices=0,
    )
    assert len(fragments['fragment_offsets']) == 3
    prepared = {
        arm: dmt.prepare_ligand(
            msm.copy(charged_ligand),
            selection='all',
            state_id='3PTB-benzamidinium-plus1',
            typing_options=TYPING,
            active_torsion_bonds=cuts,
        )
        for arm, cuts in (('rigid', []), ('flexible', [(0, 6)]))
    }
    evidence = {'receptor': prepared_evidence(prepared_receptor, list(protein_indices))}
    for arm, ligand in prepared.items():
        evidence[arm] = prepared_evidence(ligand, list(ligand_indices))
        assert ligand.n_atoms == 13
        np.testing.assert_allclose(
            evidence[arm]['charge_audit']['total_charge'], 1, rtol=0, atol=1e-8
        )
    assert prepared_receptor.n_atoms == 2011
    np.testing.assert_allclose(
        evidence['receptor']['charge_audit']['total_charge'], 6, rtol=0, atol=1e-8
    )
    assert [prepared[a].torsion_dof for a in ('rigid', 'flexible')] == [0, 1]
    # Independent serialized-field comparison on the provider's source axis.
    canonical = {}
    for arm in prepared:
        canonical[arm] = {
            i: {k: row[k] for k in ('name', 'coordinates', 'charge_e', 'type')}
            for i, row in zip(
                evidence[arm]['pdbqt_to_expanded_atom_indices'],
                evidence[arm]['written_fields'],
                strict=True,
            )
        }
    assert canonical['rigid'] == canonical['flexible']
    assert snapshot(charged_ligand) == charged_snapshot
    center = msm.structure.get_center(reference, weights=None)[0, 0]
    boxes = {
        'native': dmt.BoxRegion(
            center=center, lengths=puw.quantity([20, 20, 20], 'angstrom')
        ),
        'negative': dmt.BoxRegion(
            center=puw.quantity(
                puw.get_value(center, to_unit='angstrom') + [60, 0, 0], 'angstrom'
            ),
            lengths=puw.quantity([20, 20, 20], 'angstrom'),
        ),
    }
    box_evidence = {}
    for name, box in boxes.items():
        containment = [
            box.contains(point) for point in msm.get(reference, coordinates=True)[0]
        ]
        assert containment == [name == 'native'] * 9
        backend_center, backend_size = _vina_box(box)
        box_evidence[name] = {
            'unrounded': box.to_backend_box('angstrom'),
            'backend_projection': {
                'center': backend_center,
                'size': backend_size,
                'unit': 'angstrom',
            },
            'native_heavy_containment': containment,
            'submitted': False,
        }
    with TemporaryDirectory(prefix='dockingmt-3ptb-native-parse-') as directory:
        receptor_path = Path(directory) / 'receptor.pdbqt'
        receptor_path.write_text(evidence['receptor']['pdbqt'])
        for arm in prepared:
            engine = Vina(sf_name='vina', cpu=1, seed=7, verbosity=0)
            engine.set_receptor(str(receptor_path))
            engine.set_ligand_from_string(evidence[arm]['pdbqt'])
            evidence[arm]['native_vina_parser_admitted'] = True
        evidence['receptor']['native_vina_parser_admitted'] = True
    population = []
    for arm in ('rigid', 'flexible'):
        for domain in ('native', 'negative'):
            for seed in (7, 42, 2026):
                for effort in (1, 8):
                    protocol = dmt.VinaProtocol(
                        seed=seed,
                        exhaustiveness=effort,
                        scoring='vina',
                        cpu=1,
                        n_poses=9,
                        energy_range='3 kcal/mol',
                        allow_provisional_preparation=False,
                        capture_backend_inputs=True,
                        active_torsion_bonds=[] if arm == 'rigid' else [(0, 6)],
                    )
                    population.append(
                        {
                            'index': len(population),
                            'arm': arm,
                            'domain': domain,
                            'protocol': protocol.to_dict(),
                            'backend_box': box_evidence[domain]['backend_projection'],
                            'receptor_pdbqt_sha256': evidence['receptor'][
                                'pdbqt_sha256'
                            ],
                            'partner_pdbqt_sha256': evidence[arm]['pdbqt_sha256'],
                            'status': 'not_attempted',
                        }
                    )
    assert snapshot(source) == original and snapshot(reference) == original_ligand
    assert snapshot(receptor) == original_receptor
    assert sha(path.read_bytes()) == SOURCE_SHA
    record = {
        'schema': 'dockingmt.3ptb_molecular_admission@1',
        'status': 'plain_input_admitted',
        'registration': binding,
        'direct_compressed_input_admitted': False,
        'fixed_evaluations_executed': 0,
        'docking_searches_executed': 0,
        'source_sha256': SOURCE_SHA,
        'source_counts': counts,
        'source_snapshot': original,
        'source_observed_attributes': source_attributes,
        'input_altloc_inventory': alternates,
        'native_altloc_getter': msm.get(
            source, element='atom', alternate_location=True
        ),
        'original_source_unchanged': True,
        'original_plain_file_unchanged': True,
        'protein_full_source_indices': protein_indices,
        'ligand_full_source_indices': ligand_indices,
        'receptor': {
            'observed_snapshot': original_receptor,
            'declared_group_states': states,
            'disulfide_author_pairs': DISULFIDES,
            'disulfide_selected_group_pairs': pairs,
            'disulfide_selected_atom_pairs': sulfur_pairs,
            'template_report': factory['report'],
            'template_correspondence': correspondence,
            'template_assessment': assessment,
            'application_report': application['report'],
            'expansion': receptor_h,
            'charge_report': receptor_charged['report'],
            'charged_snapshot': snapshot(charged_receptor),
        },
        'ligand': {
            'observed_snapshot': original_ligand,
            'template_options': {
                k: v for k, v in ligand_options.items() if k != 'template'
            },
            'template_assessment': ligand_assessment,
            'application_report': ligand_application['report'],
            'expansion': ligand_h,
            'charge_report': ligand_charged['report'],
            'charged_snapshot': charged_snapshot,
            'rotatable_bonds': classification,
            'rigid_fragments': fragments,
        },
        'prepared_inputs': evidence,
        'boxes': box_evidence,
        'population': population,
        'limitations': [
            'RDKit sanitation and complete named-field coverage do not certify experimental protonation, independent valence correctness or model suitability.',
            'Environmental H refinement, symmetry-aware RMSD and general native projection retirement remain unassessed.',
            'No pose generation, ranking, affinity or search performance evidence in this admission.',
        ],
    }
    return prepared_receptor, prepared, reference, boxes, detached_record(record)


def producer_identity():
    """Bind original execution to actual source composition and native bytes."""
    provider_root = Path(msm.__file__).resolve().parents[1]
    proof = {}
    for relative in (
        'molsysmt/basic/convert.py',
        'molsysmt/basic/extract.py',
        'molsysmt/basic/copy.py',
        'molsysmt/form/file_pdb/is_form.py',
        'molsysmt/form/file_pdb/to_molsysmt_MolSys.py',
        'molsysmt/physchem/get_peptide_chemical_template.py',
        'molsysmt/physchem/assess_chemical_template.py',
        'molsysmt/physchem/apply_chemical_template.py',
        'molsysmt/_private/fixed_hydrogens.py',
        'molsysmt/build/add_missing_hydrogens.py',
        'molsysmt/build/assign_partial_charges.py',
        'molsysmt/build/assign_autodock_atom_types.py',
        'molsysmt/topology/get_rotatable_bonds.py',
        'molsysmt/topology/get_rigid_fragments.py',
        'molsysmt/structure/get_center.py',
    ):
        expected = subprocess.check_output(
            [
                'git',
                '-C',
                str(ROOT.parent / 'molsysmt'),
                'show',
                f'{PROVIDER}:{relative}',
            ]
        )
        assert (provider_root / relative).read_bytes() == expected, relative
        proof[relative] = sha(expected)
    native = next((provider_root / 'molsysmt').glob('_rust*.so'))
    assert sha(native.read_bytes()) == NATIVE_SHA
    packages = {}
    for name in (
        'dockingmt',
        'molsysmt',
        'argdigest',
        'molsysviewer',
        'pyunitwizard',
        'vina',
        'rdkit',
        'pandas',
    ):
        module = importlib.import_module(name)
        packages[name] = {
            'version': str(module.__version__),
            'loaded_import': str(Path(module.__file__).resolve()),
        }
    source_composition = {}
    for name, revision in (
        ('molsysmt', PROVIDER),
        ('argdigest', '1bea27fab5f5b15ee4c16ca2402cd0cfa1614d2e'),
        ('molsysviewer', 'ec4c71e574d798b7c8675b7e7e983da878ce9889'),
        ('pyunitwizard', '2ab37a525ce99728ad8aee846b4a4f7acc4f1b65'),
    ):
        loaded_root = Path(packages[name]['loaded_import']).parents[1]
        archive = subprocess.check_output(
            ['git', '-C', str(ROOT.parent / name), 'archive', revision, name]
        )
        digests = {}
        with tarfile.open(fileobj=io.BytesIO(archive)) as files:
            for entry in files:
                if not entry.isfile() or not entry.name.endswith('.py'):
                    continue
                if entry.name == f'{name}/_version.py':
                    continue
                expected = files.extractfile(entry).read()
                assert (loaded_root / entry.name).read_bytes() == expected, entry.name
                digests[entry.name] = sha(expected)
        assert digests
        generated = loaded_root / name / '_version.py'
        source_composition[name] = {
            'source_commit': revision,
            'loaded_root': str(loaded_root),
            'verified_python_source_sha256': digests,
            'generated_version_sha256': sha(generated.read_bytes())
            if generated.exists()
            else None,
        }
    consumer_paths = [
        *sorted((ROOT / 'dockingmt').rglob('*.py')),
        Path(__file__),
        ROOT / 'devtools/qualify_181l_receptor.py',
        ROOT / 'devtools/qualify_chemical_templates.py',
        ROOT / 'devtools/qualify_named_types.py',
        ROOT / 'devtools/qualify_5x72_occupancy.py',
    ]
    return {
        'qualified_provider_commit': PROVIDER,
        'provider_source_sha256': proof,
        'provider_native_artifact': {'path': str(native), 'sha256': NATIVE_SHA},
        'runtime': {
            'python': sys.version,
            'executable': sys.executable,
            'packages': packages,
        },
        'consumer_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'consumer_driver_sha256': sha(Path(__file__).read_bytes()),
        'consumer_source_sha256': {
            str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in consumer_paths
        },
        'source_composition': source_composition,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'pdb', type=Path, help='Caller-staged original 3PTB.pdb; exact bytes required'
    )
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    identity = producer_identity()
    *_, record = admit(args.pdb)
    record['original_producer'] = identity
    save(record, args.output)
    print(
        json.dumps(
            {
                'status': record['status'],
                'planned': len(record['population']),
                'searches_executed': 0,
                'output': str(args.output),
            }
        )
    )


if __name__ == '__main__':
    main()
