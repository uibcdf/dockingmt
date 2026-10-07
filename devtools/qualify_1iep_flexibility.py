"""Compare explicit flexible and rigid 1IEP under identical named preparation.

This pinned fixture composes public molecular operations. It keeps the original
SDF chemical state/H inventory and external receptor; it predicts neither state
nor receptor chemistry. The rigid bound-conformation control is favorable.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as metadata
import json
import subprocess
import sys
import warnings
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw
from rdkit import Chem

import dockingmt as dmt
from devtools.qualify_181l_receptor import save
from devtools.qualify_chemical_templates import detached_record, record_digest, snapshot
from devtools.qualify_named_types import CHARGE, PROVIDER_REVISION, TYPING
from devtools.validate_1iep_pdbqt import _pose_metrics

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'tests/data/vina_torsions'
OUTPUT = ROOT / 'devguide/validation/data/1iep_flexibility/audit_2026-10-07.json.gz'
INPUTS = {
    '1iep_ligand.sdf': '051b8742c32adc05c07fb486a4e7c9327f84e131cee33ac4e6a568d07553eb38',
    '1iep_receptor.pdbqt': 'f13cf3b36f61d87c3b58983e0b8ecf1c3456a685eb86dfe9ccfb139c7bdc2586',
}
# Caller-declared source axes from the existing independently mapped reference
# matrix. Counts are insufficient: these exact identities define this experiment.
CUTS = [(17, 19), (12, 13), (10, 12), (2, 6), (20, 21), (24, 27), (27, 28)]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare_case():
    """Keep observed SDF coordinates/H and vary only selected active cuts."""
    for filename, expected in INPUTS.items():
        assert digest(DATA / filename) == expected, filename
    molecules = list(Chem.SDMolSupplier(str(DATA / '1iep_ligand.sdf'), removeHs=False))
    assert len(molecules) == 1 and molecules[0] is not None
    # Existing explicit adapter for this original SDF dialect, no chemistry edits.
    source = msm.convert(molecules[0], to_form='molsysmt.MolSys')
    before = snapshot(source)
    assert msm.get(source, n_atoms=True) == 69
    assert msm.get(source, n_bonds=True) == 73
    prepared = {
        name: dmt.prepare_ligand(
            source,
            selection='all',
            active_torsion_bonds=cuts,
            charge_options=CHARGE,
            typing_options=TYPING,
        )
        for name, cuts in [('rigid', []), ('flexible', CUTS)]
    }
    assert snapshot(source) == before
    rigid, flexible = prepared.values()
    for ligand in prepared.values():
        assert ligand.n_atoms == 40
        assert dmt.audit_preparation_charges(ligand)['assessment'] == 'consistent'
        assert dmt.assess_preparation(ligand)['assessment'] == 'unassessed'
    assert rigid.atom_types == flexible.atom_types
    assert rigid.charges == flexible.charges
    assert np.array_equal(
        puw.get_value(rigid.coordinates, to_unit='angstrom'),
        puw.get_value(flexible.coordinates, to_unit='angstrom'),
    )
    assert (
        rigid.metadata['retained_atom_indices']
        == flexible.metadata['retained_atom_indices']
    )
    audit = {
        'source_snapshot': before,
        'source_snapshot_sha256': record_digest(before),
        'source_unchanged': True,
        'decisions': {
            'chemical_state': 'original_SDF_declared_state',
            'hydrogen_policy': 'retain_original_indexed_H_no_generation',
            'pH': None,
            'receptor_policy': 'unchanged_external_pinned_PDBQT',
            'charge_options': CHARGE,
            'typing_options': TYPING,
            'rigid_active_torsion_bonds': [],
            'flexible_active_torsion_bonds': [list(pair) for pair in CUTS],
            'rmsd_scope': '37_original_SDF_heavy_atoms',
            'cutoff_angstrom': 2.5,
        },
        'preparations': {
            name: {
                'prepared': ligand.to_dict(),
                'pdbqt': ligand.to_pdbqt(),
                'pdbqt_sha256': hashlib.sha256(ligand.to_pdbqt().encode()).hexdigest(),
                'charge_audit': dmt.audit_preparation_charges(ligand),
            }
            for name, ligand in prepared.items()
        },
    }
    return source, prepared, detached_record(audit)


def redock(source, ligand, decisions, *, variant, seed, exhaustiveness):
    """Retain actual search, source-key RMSD and exact captured submitted bytes."""
    before = record_digest(snapshot(source))
    problem = dmt.DockingProblem(
        DATA / '1iep_receptor.pdbqt',
        ligand,
        dmt.BoxRegion(
            puw.quantity([15.190, 53.903, 16.917], 'angstrom'),
            puw.quantity([20, 20, 20], 'angstrom'),
        ),
        metadata={'variant': variant, 'preparation_decisions': decisions},
    )
    result = dmt.dock(
        problem,
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
    assert restored.poses
    artifacts = restored.provenance['backend_artifacts']
    dmt.verify_captured_inputs(artifacts)
    assert artifacts['receptor']['sha256'] == INPUTS['1iep_receptor.pdbqt']
    assert (
        artifacts['partner']['sha256']
        == hashlib.sha256(ligand.to_pdbqt().encode()).hexdigest()
    )
    assert record_digest(snapshot(source)) == before
    report = dmt.evaluate_redocking(
        restored,
        source,
        rmsd_cutoff=puw.quantity(2.5, 'angstrom'),
        reference_info={
            'case': '1IEP',
            'source_sha256': INPUTS['1iep_ligand.sdf'],
            'scope': 'all_40_retained_SDF_atoms_including_3_polar_H',
            'qualification': 'bounded_torsion_sensitivity_unassessed_preparation',
        },
    )
    source_indices = [
        ligand.metadata['retained_atom_indices'][index]
        for index in ligand.pdbqt_atom_indices
    ]
    elements = msm.get(source, element='atom', atom_type=True)
    heavy_indices = [
        index
        for index, source_index in enumerate(source_indices)
        if elements[source_index] != 'H'
    ]
    assert len(heavy_indices) == 37
    reference = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[
        0, source_indices
    ]
    # Reuse the existing reference-driver metric on this explicitly declared map;
    # the public full-inventory report above retains source-key verification.
    heavy = _pose_metrics(restored, reference, heavy_indices)
    return {
        'variant': variant,
        'result': saved,
        'evaluation': report,
        'heavy_atom_metrics': heavy,
        'pdbqt_to_source_atom_indices': source_indices,
        'heavy_pdbqt_indices': heavy_indices,
    }


def qualify():
    """Run matched seed/exhaustiveness cells without tuning from their outcomes."""
    provider_root = Path(msm.__file__).resolve().parents[1]
    paths = (
        'molsysmt/topology/get_rotatable_bonds.py',
        'molsysmt/topology/get_rigid_fragments.py',
        'molsysmt/_private/autodock_assignment.py',
        'molsysmt/_private/partial_charges.py',
    )
    proof = {}
    for relative in paths:
        committed = subprocess.check_output(
            [
                'git',
                '-C',
                str(ROOT.parent / 'molsysmt'),
                'show',
                f'{PROVIDER_REVISION}:{relative}',
            ]
        )
        assert (provider_root / relative).read_bytes() == committed, relative
        proof[relative] = digest(provider_root / relative)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        source, preparations, audit = prepare_case()
        runs = []
        for exhaustiveness in (1, 8):
            for seed in (7, 42, 2026):
                for variant, ligand in preparations.items():
                    runs.append(
                        redock(
                            source,
                            ligand,
                            audit['decisions'],
                            variant=variant,
                            seed=seed,
                            exhaustiveness=exhaustiveness,
                        )
                    )
                    print(
                        f'Completed {len(runs)}/12: {variant}, seed={seed}, '
                        f'exhaustiveness={exhaustiveness}',
                        file=sys.stderr,
                    )
    return {
        'schema': 'dockingmt.1iep_flexibility_audit@1',
        'date': '2026-10-07',
        'python': sys.version,
        'interpreter': sys.executable,
        'input_sha256': INPUTS,
        'qualified_provider_commit': PROVIDER_REVISION,
        'provider_module': str(Path(msm.__file__).resolve()),
        'provider_source_sha256': proof,
        'provider_native_artifacts': {
            str(path): digest(path)
            for path in provider_root.joinpath('molsysmt').glob('_rust*.so')
        },
        'producer_versions': {
            name: metadata.version(name)
            for name in ('molsysmt', 'argdigest', 'pyunitwizard', 'rdkit', 'vina')
        },
        'consumer_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'consumer_source_sha256': {
            str(path.relative_to(ROOT)): digest(path)
            for path in [
                *sorted(ROOT.joinpath('dockingmt').rglob('*.py')),
                Path(__file__),
                ROOT / 'devtools/qualify_181l_receptor.py',
                ROOT / 'devtools/qualify_chemical_templates.py',
                ROOT / 'devtools/qualify_named_types.py',
                ROOT / 'devtools/validate_1iep_pdbqt.py',
            ]
        },
        'audit': audit,
        'redocking_runs': runs,
        'warnings': [
            {'category': type(w.message).__name__, 'message': str(w.message)}
            for w in caught
        ],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    evidence = qualify()
    save(evidence, args.output)
    print(
        json.dumps(
            {'output': str(args.output), 'runs': len(evidence['redocking_runs'])}
        )
    )
