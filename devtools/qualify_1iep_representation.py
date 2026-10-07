"""Pinned 1IEP representation controls with unchanged chemistry and torsions.

The only generated fixture reverses the eight existing native ROOT lines.
This is not a PDBQT writer, rerooting tool or molecular matching algorithm.
"""

from __future__ import annotations

import argparse
import gzip
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
from devtools.audit_1iep_preparation import _compare_pdbqt, _compare_torsion_graphs
from devtools.qualify_1iep_flexibility import DATA, prepare_case
from devtools.qualify_1iep_flexibility import OUTPUT as BASELINE
from devtools.qualify_181l_receptor import save
from devtools.qualify_chemical_templates import detached_record, record_digest, snapshot
from devtools.validate_1iep_pdbqt import (
    INPUT_SHA256,
    _pose_metrics,
    _reference_box,
    _source_atom_map,
)
from dockingmt.engines.vina import _pdbqt_atom_records

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'devguide/validation/data/1iep_representation/audit_2026-10-07.json.gz'
BASELINE_SHA256 = 'a8e7891094593223e5b8518d6a0695cce673022182cde2eaa076fba397755eca'
NATIVE_SHA256 = '43e3219134099eee7d388b0f49ca90e5a46afea9b6b54a754276b21fab48761e'


def sha(content):
    return hashlib.sha256(content).hexdigest()


def root_order_control(native):
    """Permute exactly this fixture's ROOT records; preserve every line byte."""
    if sha(native) != NATIVE_SHA256:
        raise ValueError('The declared native 1IEP fixture changed.')
    lines = native.splitlines(keepends=True)
    start, end = lines.index(b'ROOT\n') + 1, lines.index(b'ENDROOT\n')
    assert end - start == 8 and all(x.startswith(b'ATOM') for x in lines[start:end])
    return b''.join(lines[:start] + lines[start:end][::-1] + lines[end:])


def prepare_controls(*, verify_profile=False):
    """Authenticate prior science before reusing any of its six native runs."""
    original = BASELINE.read_bytes()
    assert sha(original) == BASELINE_SHA256
    baseline = json.loads(gzip.decompress(original))
    source, prepared, audit = prepare_case()
    native = baseline['audit']['preparations']['flexible']['pdbqt'].encode()
    if verify_profile:
        for relative, expected in baseline['consumer_source_sha256'].items():
            assert sha((ROOT / relative).read_bytes()) == expected, relative
        for name, version in baseline['producer_versions'].items():
            assert metadata.version(name) == version, name
        assert (
            record_digest(snapshot(source))
            == baseline['audit']['source_snapshot_sha256']
        )
        assert prepared['flexible'].to_pdbqt().encode() == native
    assert sha(native) == NATIVE_SHA256
    published = (DATA / '1iep_ligand.pdbqt').read_bytes()
    assert sha(published) == INPUT_SHA256['partner']
    assert sha((DATA / '1iep_receptor.pdbqt').read_bytes()) == INPUT_SHA256['receptor']
    contents = {
        'native': native,
        'published': published,
        'native_root_reversed': root_order_control(native),
    }
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[0]
    elements = msm.get(source, element='atom', atom_type=True)
    controls = {}
    for name, content in contents.items():
        comparison = _compare_pdbqt(native, content)
        tree = _compare_torsion_graphs(native, content)
        assert comparison['coordinate_matched_atoms'] == 40
        assert comparison['matched_atom_type_disagreements'] == 0
        assert comparison['matched_charge_max_absolute_difference_e'] == 0
        assert tree['branch_bonds_match'] and tree['rigid_fragments_match']
        assert comparison['reference_torsion_dof'] == 7
        records = _pdbqt_atom_records(content.decode())
        # Existing bounded already-aligned fixture map, independently guarded.
        indices = _source_atom_map(records, xyz, elements)
        heavy = [
            i for i, source_index in enumerate(indices) if elements[source_index] != 'H'
        ]
        assert len(heavy) == 37
        Vina(cpu=1, verbosity=0).set_ligand_from_string(content.decode())
        controls[name] = {
            'pdbqt': content.decode(),
            'sha256': sha(content),
            'pdbqt_to_source_atom_indices': indices,
            'heavy_pdbqt_indices': heavy,
            'atom_comparison': comparison,
            'torsion_graph_comparison': tree,
        }
    return source, controls, baseline, audit


def problem(control, variant):
    return dmt.DockingProblem(
        DATA / '1iep_receptor.pdbqt',
        control['pdbqt'],
        _reference_box(),
        metadata={'variant': variant, 'qualification': 'bounded_1iep_representation'},
    )


def observe(source, control, *, variant, seed, exhaustiveness):
    """Evaluate actual written-order poses through the explicit fixture map."""
    before = record_digest(snapshot(source))
    result = dmt.dock(
        problem(control, variant),
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
    assert artifacts['partner']['sha256'] == control['sha256']
    assert artifacts['receptor']['sha256'] == INPUT_SHA256['receptor']
    assert record_digest(snapshot(source)) == before
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[
        0, control['pdbqt_to_source_atom_indices']
    ]
    evaluation = dmt.evaluate_redocking(
        restored,
        puw.quantity(xyz, 'angstrom'),
        rmsd_cutoff=puw.quantity(2.5, 'angstrom'),
        reference_info={
            'case': '1IEP',
            'scope': '40_retained_original_SDF_atoms',
            'atom_order': 'verified_PDBQT_order_with_bounded_fixture_source_map',
            'source_sha256': INPUT_SHA256['source_ligand'],
        },
    )
    return {
        'variant': variant,
        'result': saved,
        'evaluation': evaluation,
        'heavy_atom_metrics': _pose_metrics(
            restored, xyz, control['heavy_pdbqt_indices']
        ),
        'pdbqt_to_source_atom_indices': control['pdbqt_to_source_atom_indices'],
        'heavy_pdbqt_indices': control['heavy_pdbqt_indices'],
    }


def fixed_score(control, variant):
    """Compose public fixed-conformation scoring; no search or optimization."""
    pose = dmt.score(
        problem(control, variant),
        dmt.VinaProtocol(cpu=1, seed=42, capture_backend_inputs=True),
        score_name='vina',
    )
    saved = detached_record(pose.to_dict())
    artifacts = saved['metadata']['scoring_history'][0]['backend_artifacts']
    dmt.verify_captured_inputs(artifacts)
    assert artifacts['partner']['sha256'] == control['sha256']
    return saved


def qualify_variant(variant):
    """Two independent process arms, each using CPU 1 and a fixed grid of cases."""
    source, controls, _, _ = prepare_controls(verify_profile=True)
    runs = []
    for effort in (1, 8):
        for seed in (7, 42, 2026):
            runs.append(
                observe(
                    source,
                    controls[variant],
                    variant=variant,
                    seed=seed,
                    exhaustiveness=effort,
                )
            )
            print(
                f'{variant}: completed {len(runs)}/6, seed={seed}, effort={effort}',
                file=sys.stderr,
            )
    return {
        'variant': variant,
        'baseline_sha256': BASELINE_SHA256,
        'consumer_source_sha256': source_proof(),
        'producer_versions': {
            name: metadata.version(name)
            for name in ('molsysmt', 'argdigest', 'pyunitwizard', 'rdkit', 'vina')
        },
        'runs': runs,
    }


def source_proof():
    return {
        str(p.relative_to(ROOT)): sha(p.read_bytes())
        for p in [
            *sorted((ROOT / 'dockingmt').rglob('*.py')),
            Path(__file__),
            ROOT / 'devtools/qualify_1iep_flexibility.py',
            ROOT / 'devtools/audit_1iep_preparation.py',
            ROOT / 'devtools/validate_1iep_pdbqt.py',
            ROOT / 'devtools/qualify_chemical_templates.py',
            ROOT / 'devtools/qualify_181l_receptor.py',
            ROOT / 'devtools/qualify_named_types.py',
        ]
    }


def assemble(parts):
    """Preserve reused original producer and actual newly executed observations."""
    source, controls, baseline, audit = prepare_controls(verify_profile=True)
    for part in parts:
        assert part['baseline_sha256'] == BASELINE_SHA256
        assert part['consumer_source_sha256'] == source_proof()
        assert part['producer_versions'] == baseline['producer_versions']
    assert {p['variant'] for p in parts} == {'published', 'native_root_reversed'}
    native_runs = [r for r in baseline['redocking_runs'] if r['variant'] == 'flexible']
    assert len(native_runs) == 6
    fixed = {name: fixed_score(control, name) for name, control in controls.items()}
    repeat = observe(
        source, controls['native'], variant='native_repeat', seed=42, exhaustiveness=1
    )
    return {
        'schema': 'dockingmt.1iep_representation_audit@1',
        'date': '2026-10-07',
        'interpreter': sys.executable,
        'python': sys.version,
        'consumer_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'consumer_source_sha256': source_proof(),
        'provider_module': baseline['provider_module'],
        'qualified_provider_commit': baseline['qualified_provider_commit'],
        'provider_source_sha256': baseline['provider_source_sha256'],
        'provider_native_artifacts': baseline['provider_native_artifacts'],
        'producer_versions': baseline['producer_versions'],
        'baseline': {
            'path': str(BASELINE.relative_to(ROOT)),
            'sha256': BASELINE_SHA256,
            'source_producer': '7b11391e153f77f340fd039bc799352f90da83d3',
            'scope': 'six original native flexible runs, unchanged bytes and reports',
        },
        'audit': audit,
        'controls': controls,
        'original_native_runs': native_runs,
        'new_runs': [r for part in parts for r in part['runs']],
        'native_repeat': repeat,
        'fixed_conformation_scores': fixed,
        'limits': [
            'Published/native comparison changes ROOT, ordering and labels together; it does not isolate ROOT alone.',
            'ROOT-reversed control changes only eight existing ATOM line positions, keeping serials, labels, ROOT membership and all other bytes.',
            'Full RMSD is caller-declared positional matching through a verified bounded fixture map, not a public general atom correspondence operation.',
            'One bound-like initial conformer, rigid externally prepared receptor and declared chemical state; no broader preparation or affinity qualification.',
            'No automatic policy tuning, conformer challenge, convergence or recovery probability is established.',
            'Two new search arms run in independent processes, each with Vina CPU 1; original native evidence is reused only after code/version/input/source checks.',
            'Original native repeat reports actual stochastic agreement; it is not a portable exact-pose guarantee.',
            'Existing installed artifacts and native build-provenance/public dependency-closure limits remain unchanged.',
        ],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=['published', 'native_root_reversed'])
    parser.add_argument('--parts', nargs=2, type=Path)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.variant:
        evidence = qualify_variant(args.variant)
    else:
        if not args.parts:
            parser.error('--parts is required when no --variant is supplied')
        evidence = assemble(
            [json.loads(gzip.decompress(p.read_bytes())) for p in args.parts]
        )
    save(evidence, args.output)
    print(json.dumps({'output': str(args.output)}))
