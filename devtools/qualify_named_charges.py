"""Reproduce bounded charge-model consumption through public MolSysMT APIs."""

import hashlib
import importlib.metadata as metadata
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

import molsysmt as msm
import numpy as np
import pyunitwizard as puw
from vina import Vina

import dockingmt as dmt

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_REVISION = '7894435e748bc55254b6c3d2b63ae82c101e5774'
OUTPUT = ROOT / 'devguide/validation/data/named_charges/qualification.json'


def _digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _charges(system):
    values = msm.get(system, partial_charge=True)
    if puw.is_quantity(values):
        values = puw.get_value(values, to_unit='elementary_charge')
    return np.asarray(values, dtype=float)


def _case(
    source, *, method, receptor=False, selection='all', active_bonds=None, **options
):
    source_coords = puw.get_value(
        msm.get(source, coordinates=True), to_unit='angstrom'
    ).copy()
    start = perf_counter()
    assigned = msm.build.assign_partial_charges(source, method=method, **options)
    assignment_seconds = perf_counter() - start
    before = _charges(assigned).copy()
    start = perf_counter()
    prepared = (
        dmt.prepare_receptor(assigned, selection=selection)
        if receptor
        else dmt.prepare_ligand(
            assigned, selection=selection, active_torsion_bonds=active_bonds
        )
    )
    report = dmt.audit_preparation_charges(prepared)
    preparation_seconds = perf_counter() - start
    assert report['assessment'] == 'consistent'
    np.testing.assert_array_equal(_charges(assigned), before)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom'),
        source_coords,
    )
    assert not msm.has_attribute(source, 'partial_charge')
    text = prepared.to_pdbqt()
    written = [
        float(line[70:76]) for line in text.splitlines() if line.startswith('ATOM')
    ]
    assert report['pdbqt']['charges'] == written
    assert (
        abs(report['pdbqt']['rounding_difference'])
        <= report['pdbqt']['total_rounding_bound']
    )
    engine = Vina(cpu=1, verbosity=0)
    if receptor:
        with TemporaryDirectory(prefix='dockingmt-charge-') as directory:
            target = Path(directory) / 'receptor.pdbqt'
            target.write_text(text)
            engine.set_receptor(str(target))
    else:
        engine.set_ligand_from_string(text)
    return {
        'audit': report,
        'preparation_assessment': dmt.assess_preparation(prepared),
        'pdbqt_sha256': hashlib.sha256(text.encode()).hexdigest(),
        'pdbqt_bytes': len(text.encode()),
        'assignment_seconds': assignment_seconds,
        'preparation_and_audit_seconds': preparation_seconds,
        'source_unchanged': True,
        'native_vina_input_admitted': True,
        'role': 'receptor' if receptor else 'partner',
    }


def qualify():
    """Return finite evidence; source commit proof is separate from package metadata."""
    provider_root = Path(msm.__file__).resolve().parents[1]
    provider_files = [
        'molsysmt/build/assign_partial_charges.py',
        'molsysmt/physchem/get_partial_charges.py',
        'molsysmt/_private/partial_charges.py',
        'molsysmt/native/molsys.py',
    ]
    proof = {}
    for relative in provider_files:
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
        assert actual == published, f'Unqualified provider source: {relative}'
        proof[relative] = hashlib.sha256(actual).hexdigest()
    methanol = ROOT / 'tests/data/charges/methanol.sdf'
    flexible = ROOT / 'tests/data/vina_torsions/5x72_ligand_p59H.sdf'
    receptor = Path(msm.systems['chicken villin HP35']['1vii.pdb'])
    sources = {
        'methanol': msm.convert(methanol, to_form='molsysmt.MolSys'),
        '5x72_p59': msm.convert(
            flexible,
            to_form='molsysmt.MolSys',
            stereo_engine='rdkit',
            discard_properties=True,
        ),
        '1vii': msm.convert(receptor, to_form='molsysmt.MolSys'),
    }
    cases = {
        'methanol_full': _case(sources['methanol'], method='gasteiger_marsili'),
        'methanol_oh_projection': _case(
            sources['methanol'], method='gasteiger_marsili', selection=[1, 5]
        ),
        '5x72_p59_flexible': _case(
            sources['5x72_p59'],
            method='gasteiger_marsili',
            active_bonds=[(6, 7), (17, 18)],
        ),
        '1vii_amber14': _case(
            sources['1vii'],
            method='forcefield',
            receptor=True,
            forcefield='AMBER14',
            expected_total_charge=2,
        ),
    }
    assert abs(cases['1vii_amber14']['audit']['total_charge'] - 2) < 1e-12
    assert cases['1vii_amber14']['audit']['n_atoms'] == 364
    assert abs(cases['methanol_full']['audit']['total_charge']) < 1e-12
    assert abs(cases['methanol_oh_projection']['audit']['total_charge']) > 0.1
    return {
        'schema_version': '1.0',
        'qualification': 'bounded_named_charge_consumption',
        'interpreter': sys.executable,
        'python': sys.version,
        'dockingmt_module': str(Path(dmt.__file__).resolve()),
        'provider_module': str(Path(msm.__file__).resolve()),
        'qualified_provider_commit': PROVIDER_REVISION,
        'provider_source_sha256': proof,
        'distribution_versions': {
            name: metadata.version(name)
            for name in ('dockingmt', 'molsysmt', 'vina', 'rdkit', 'openmm')
        },
        'version_limit': 'Provider reports retain actual distribution metadata. Exact tested source is identified independently by commit and file hashes.',
        'input_sha256': {
            'methanol.sdf': _digest(methanol),
            '5x72_ligand_p59H.sdf': _digest(flexible),
            '1vii.pdb': _digest(receptor),
        },
        'dockingmt_source_sha256': {
            relative: _digest(ROOT / relative)
            for relative in (
                'dockingmt/preparation/_molsys.py',
                'dockingmt/preparation/ligand.py',
                'dockingmt/preparation/receptor.py',
                'dockingmt/preparation/charges.py',
                'devtools/qualify_named_charges.py',
            )
        },
        'cases': cases,
        'limits': [
            'AutoDock typing remains heuristic and preparation provisional.',
            'No AD4 scoring or charge-model suitability for an energy function is qualified.',
            'Vina ligand parsing is an interoperability control, not scientific validation.',
            'The existing consumer H transfers remain temporary pending molsysmt#223.',
            'Projected charges were calculated on the original full graph, not recalculated on a fragment.',
            'No H5MSM 0.5 molecular-mechanics attribution roundtrip is claimed.',
            'Single-run timings include first-use costs and are not a benchmark.',
            'Other Python minors are qualified separately in CI.',
        ],
    }


def save(record):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(record, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    result = qualify()
    save(result)
    print(
        json.dumps(
            {
                name: {
                    'n_atoms': case['audit']['n_atoms'],
                    'total_charge': case['audit']['total_charge'],
                    'pdbqt_total_charge': case['audit']['pdbqt']['total_charge'],
                }
                for name, case in result['cases'].items()
            },
            indent=2,
        )
    )
