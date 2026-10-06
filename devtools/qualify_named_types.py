"""Bounded source-composition qualification of named AutoDock type consumption.

Synthetic poses exercise software boundaries, not experimental geometry or
receptor refinement. Molecular graphs and indexed H use public MolSysMT tools.
"""

import hashlib
import importlib.metadata as metadata
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import molsysmt as msm
import numpy as np
import pyunitwizard as puw
from molsysmt.native import Structures
from vina import Vina

import dockingmt as dmt
from devtools.qualify_chemical_templates import (
    detached_record,
    load_5x72,
    load_181l_benzene,
    snapshot,
    template_options,
)
from dockingmt._private.smonitor import ArgumentError

HYDROGEN = {'mode': 'fixed_chemical_state', 'pH': None, 'engine': 'RDKit'}
CHARGE = {'method': 'gasteiger_marsili'}
TYPING = {'typing_scheme': 'autodock4', 'method': 'chemical_environment'}
ROOT = Path(__file__).resolve().parents[1]
PROVIDER_REVISION = '5bd893c85fe8d211663b2b1f865f5f1d2c382a90'
OUTPUT = ROOT / 'devguide/validation/data/named_types/qualification_2026-10-06.json'


def declared_source(smiles):
    """Declare heavy-atom chemistry and a synthetic pose through public tools."""
    native = msm.convert(
        msm.convert('smiles:' + smiles, to_form='rdkit.Mol'), to_form='molsysmt.MolSys'
    )
    n_atoms = msm.get(native, n_atoms=True)
    coordinates = np.zeros((1, n_atoms, 3))
    if n_atoms > 2:
        # A declared regular polygon avoids collinear ring-neighbor geometry.
        # This is a test pose, not conformer generation or minimization.
        angles = np.arange(n_atoms) * (2 * np.pi / n_atoms)
        radius = 1.4 / (2 * np.sin(np.pi / n_atoms))
        coordinates[0, :, :2] = radius * np.column_stack(
            (np.cos(angles), np.sin(angles))
        )
    else:
        coordinates[0, :, 0] = np.arange(n_atoms) * 1.4
    pose = Structures(coordinates=puw.quantity(coordinates, 'angstrom'))
    return msm.convert([native, pose], to_form='molsysmt.MolSys')


def explicit_source(smiles):
    """Materialize the declared fixed H inventory, without choosing protonation."""
    return msm.build.add_missing_hydrogens(declared_source(smiles), **HYDROGEN)


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _observe(source, *, receptor=False, **options):
    before = snapshot(source)
    prepare = dmt.prepare_receptor if receptor else dmt.prepare_ligand
    prepared = prepare(source, selection='all', **options)
    assert snapshot(source) == before
    projection = prepared.metadata['atom_type_projection']
    order = list(getattr(prepared, 'pdbqt_atom_indices', range(prepared.n_atoms)))
    text = prepared.to_pdbqt()
    written = [
        line.split()[-1] for line in text.splitlines() if line.startswith('ATOM')
    ]
    assert written == [prepared.atom_types[i] for i in order]
    assert projection['pdbqt_to_source_atom_indices'] == [
        projection['retained_source_atom_indices'][i] for i in order
    ]
    audit = dmt.audit_preparation_charges(prepared)
    assert audit['assessment'] == 'consistent'
    assert dmt.assess_preparation(prepared)['assessment'] == 'unassessed'
    engine = Vina(cpu=1, verbosity=0)
    if receptor:
        with TemporaryDirectory(prefix='dockingmt-type-') as directory:
            target = Path(directory) / 'receptor.pdbqt'
            target.write_text(text)
            engine.set_receptor(str(target))
    else:
        engine.set_ligand_from_string(text)
    return prepared, {
        'source_snapshot': before,
        'prepared': prepared.to_dict(),
        'charge_audit': audit,
        'preparation_assessment': dmt.assess_preparation(prepared),
        'written_atom_types': written,
        'pdbqt_sha256': hashlib.sha256(text.encode()).hexdigest(),
        'pdbqt': text,
        'native_vina_parser_admitted': True,
        'source_unchanged': True,
        'role': 'receptor' if receptor else 'partner',
    }


def qualify():
    """Exercise bounded contracts and retain finite original producer evidence."""
    profile_path = (
        ROOT
        / 'devguide/validation/data/chemical_templates/source_profile_2026-10-06.json'
    )
    prior_profile = json.loads(profile_path.read_text())
    provider_root = Path(msm.__file__).resolve().parents[1]
    assert (
        str(provider_root / 'molsysmt/__init__.py')
        == prior_profile['qualified_committed_sources']['molsysmt']['loaded_import']
    )
    proof = {}
    for relative in (
        'molsysmt/build/assign_autodock_atom_types.py',
        'molsysmt/physchem/get_autodock_atom_types.py',
        'molsysmt/_private/autodock_assignment.py',
        'molsysmt/basic/extract.py',
        'molsysmt/native/molecular_mechanics.py',
        'molsysmt/build/add_missing_hydrogens.py',
        'molsysmt/_private/fixed_hydrogens.py',
        'molsysmt/build/assign_partial_charges.py',
        'molsysmt/_private/partial_charges.py',
    ):
        actual = (provider_root / relative).read_bytes()
        published = subprocess.check_output(
            ['git', '-C', str(provider_root), 'show', f'{PROVIDER_REVISION}:{relative}']
        )
        assert actual == published, relative
        proof[relative] = hashlib.sha256(actual).hexdigest()
    native_artifacts = {
        path: _digest(path) for path in prior_profile['provider_native_artifacts']
    }
    assert native_artifacts == prior_profile['provider_native_artifacts']
    cases = {}
    methanol, cases['methanol_stages'] = _observe(
        declared_source('CO'),
        hydrogen_options=HYDROGEN,
        charge_options=CHARGE,
        typing_options=TYPING,
    )
    expected = {
        'CN': ['C', 'NA'],
        'C[NH3+]': ['C', 'N'],
        'CC(=O)N': ['C', 'C', 'OA', 'N'],
        'c1ccncc1': ['A', 'A', 'A', 'NA', 'A', 'A'],
        'c1cc[nH]c1': ['A', 'A', 'A', 'N', 'A'],
        'CSC': ['C', 'SA', 'C'],
        'CS(=O)(=O)C': ['C', 'S', 'OA', 'OA', 'C'],
    }
    for smiles, labels in expected.items():
        charged = msm.build.assign_partial_charges(explicit_source(smiles), **CHARGE)
        for receptor in (False, True):
            prepared, case = _observe(charged, receptor=receptor, typing_options=TYPING)
            assert prepared.atom_types[: len(labels)] == labels
            assert all(label == 'HD' for label in prepared.atom_types[len(labels) :])
            case['declared_smiles'] = smiles
            case['independent_expected_heavy_types'] = labels
            cases[f'{smiles}:{case["role"]}'] = case
    for smiles, heavy in [('F', 'F'), ('P', 'P')]:
        charged = msm.build.assign_partial_charges(explicit_source(smiles), **CHARGE)
        prepared, case = _observe(charged, typing_options=TYPING)
        assert prepared.atom_types == [heavy] + ['HD'] * (prepared.n_atoms - 1)
        cases[f'{smiles}:polar_h'] = case
    parent = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source('CC(=O)N'), **CHARGE), **TYPING
    )
    fragment = msm.extract(parent, selection=[0, 3])
    prepared, cases['amide_parent_projection'] = _observe(fragment)
    assert prepared.atom_types == ['C', 'N']
    assert prepared.metadata['atom_type_assignment']['n_atoms'] > prepared.n_atoms
    with puw.context(standard_units=['pm', 'coulomb']):
        charged = msm.build.assign_partial_charges(explicit_source('CO'), **CHARGE)
        prepared, cases['nondefault_units'] = _observe(charged, typing_options=TYPING)
        np.testing.assert_allclose(
            prepared.charges,
            [0.19000057917, -0.39963024356, 0.20962966439],
            rtol=0,
            atol=1e-10,
        )
    bnz, template, full_indices = load_181l_benzene()
    application = msm.physchem.apply_chemical_template(
        bnz,
        **template_options(
            template,
            np.column_stack((np.arange(6), np.arange(6))),
            identity='Explicit heavy-only benzene SMILES template',
            uri='smiles:c1ccccc1',
            hydrogen_policy='stored_counts',
        ),
    )
    prepared, cases['181l_bnz'] = _observe(
        application['molecular_system'],
        hydrogen_options={**HYDROGEN, 'attribute_policy': 'intersection'},
        charge_options=CHARGE,
        typing_options=TYPING,
    )
    assert prepared.atom_types == ['A'] * 6
    cases['181l_bnz'].update(
        {
            'original_input_sha256': _digest(
                msm.systems['T4 lysozyme L99A']['181l.pdb']
            ),
            'full_source_atom_indices': full_indices,
            'template_application_report': detached_record(application['report']),
        }
    )
    _, flexible = load_5x72('p59')
    charged = msm.build.assign_partial_charges(flexible, **CHARGE)
    prepared, cases['5x72_flexible'] = _observe(
        charged,
        active_torsion_bonds=[(6, 7), (17, 18)],
        typing_options=TYPING,
    )
    assert prepared.pdbqt_atom_indices != list(range(prepared.n_atoms))
    cases['5x72_flexible']['original_input_sha256'] = _digest(
        ROOT / 'tests/data/vina_torsions/5x72_ligand_p59H.sdf'
    )
    charged = msm.build.assign_partial_charges(explicit_source('CO'), **CHARGE)
    receptor, cases['synthetic_receptor'] = _observe(
        charged,
        receptor=True,
        typing_options=TYPING,
    )
    problem = dmt.DockingProblem(
        receptor=receptor,
        partner=methanol,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([12, 12, 12], 'angstrom')
        ),
    )
    result = dmt.dock(
        problem,
        dmt.VinaProtocol(
            cpu=1,
            seed=17,
            exhaustiveness=1,
            n_poses=1,
            capture_backend_inputs=True,
        ),
    )
    restored = dmt.DockingResult.from_dict(
        json.loads(json.dumps(result.to_dict(), allow_nan=False))
    )
    assert len(restored.poses) == 1
    for role, prepared in [('receptor', receptor), ('partner', methanol)]:
        saved = restored.provenance['preparation'][role]
        assert saved['assessment'] == 'unassessed'
        for key in ('atom_type_assignment', 'atom_type_projection'):
            assert saved['metadata'][key] == prepared.metadata[key]
    captured = dmt.verify_captured_inputs(restored.provenance['backend_artifacts'])
    negative = {}
    try:
        dmt.prepare_ligand(
            declared_source('CO'), selection='all', typing_options=TYPING
        )
    except msm.StructuralInconsistencyError as exc:
        negative['virtual_h'] = {'exception': type(exc).__name__, 'message': str(exc)}
    else:
        raise AssertionError('Undeclared indexed H was admitted.')
    methanol.atom_types[1] = 'O'
    try:
        methanol.to_pdbqt()
    except ArgumentError as exc:
        negative['changed_prepared_label'] = {
            'exception': type(exc).__name__,
            'message': str(exc),
        }
    else:
        raise AssertionError('Changed named labels were exported.')
    return {
        'schema': 'dockingmt.named_autodock_type_qualification@1',
        'date': '2026-10-06',
        'interpreter': sys.executable,
        'python': sys.version,
        'dockingmt_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'qualified_provider_commit': PROVIDER_REVISION,
        'provider_source_sha256': proof,
        'provider_native_artifacts': native_artifacts,
        'prior_source_profile': {
            'path': str(profile_path.relative_to(ROOT)),
            'sha256': _digest(profile_path),
        },
        'producer_versions': {
            name: metadata.version(name)
            for name in (
                'molsysmt',
                'argdigest',
                'molsysviewer',
                'pyunitwizard',
                'smonitor',
                'depdigest',
                'rdkit',
                'vina',
                'numpy',
            )
        },
        'consumer_implementation_sha256': {
            path: _digest(ROOT / path)
            for path in (
                'dockingmt/preparation/_typing.py',
                'dockingmt/preparation/_molsys.py',
                'dockingmt/preparation/_stages.py',
                'dockingmt/preparation/ligand.py',
                'dockingmt/preparation/receptor.py',
                'dockingmt/_private/argdigest/registry.py',
                'devtools/qualify_named_types.py',
            )
        },
        'cases': cases,
        'negative_controls': negative,
        'default_vina_result': restored.to_dict(),
        'verified_captured_bytes': captured,
        'limits': [
            'Local Python 3.14 source composition; no clean installed artifact, hosted or other Python/platform qualification.',
            'Synthetic polygon/linear poses are declared software controls, not conformers or experimental refinement.',
            'chemical_environment@1 is the provider experimental bounded profile, not a universal donor/acceptor model.',
            'Named type/charge declarations remove known provisional flags but assessment remains unassessed scientifically.',
            'Vina parsing and one default toy docking pose establish software interoperability only; AD4 scoring and predictive accuracy are not qualified.',
            '5X72 uses explicit RDKit stereo and declared SDF property loss plus a public adapter template; native versionless MOLI legacy inputs are not repaired here.',
            'Torsion choice and charge-preserving H projection/export remain their existing policies (#33/provider #223).',
            'H5MSM 0.5 cannot preserve nonempty MolecularMechanics; use native/result JSON evidence as qualified.',
            'Original producer metadata is separate from committed source bytes; native artifact digest carries no fresh build provenance.',
            'The earlier source profile retains host AmberTools dependency conflicts and pre-existing synchronized guide drift; neither is resolved here.',
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
                'cases': len(record['cases']),
                'default_vina_poses': len(record['default_vina_result']['poses']),
            }
        )
    )
