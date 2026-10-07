"""Fixed-first-ROOT-atom order control on the authenticated 1IEP fixture.

Only seven existing ATOM lines are permuted. Molecular readers, writers and
matching remain in their existing owners; this is a finite scientific control.
"""

from __future__ import annotations

import argparse
import gzip
import importlib.metadata as metadata
import json
import subprocess
import sys
from pathlib import Path

import molsysmt as msm
import pyunitwizard as puw
from vina import Vina

from devtools.audit_1iep_preparation import _compare_pdbqt, _compare_torsion_graphs
from devtools.qualify_1iep_representation import (
    NATIVE_SHA256,
    ROOT,
    fixed_score,
    observe,
    prepare_controls,
    save,
    sha,
    source_proof,
)
from devtools.qualify_1iep_representation import OUTPUT as BASELINE
from devtools.validate_1iep_pdbqt import _source_atom_map
from dockingmt.engines.vina import _pdbqt_atom_records

BASELINE_SHA256 = 'a7ba98a15191b7345e55c2de01533efe22a917d1c948bccd735970bf5d868436'
OUTPUT = ROOT / 'devguide/validation/data/1iep_root_order/audit_2026-10-07.json.gz'
VARIANT = 'native_root_first_fixed'


def load_baseline(*, verify_profile=False):
    """Keep historical observations attached to their authenticated producer."""
    content = BASELINE.read_bytes()
    assert sha(content) == BASELINE_SHA256
    record = json.loads(gzip.decompress(content))
    if verify_profile:
        for name, expected in record['consumer_source_sha256'].items():
            assert sha((ROOT / name).read_bytes()) == expected, name
        for name, version in record['producer_versions'].items():
            assert metadata.version(name) == version, name
        provider = Path(record['provider_module']).parent.parent
        for name, expected in record['provider_source_sha256'].items():
            assert sha((provider / name).read_bytes()) == expected, name
        for name, expected in record['provider_native_artifacts'].items():
            assert sha(Path(name).read_bytes()) == expected, name
    return record


def fixed_first_control(native):
    """Fix this fixture's first ROOT line and reverse its other seven lines."""
    if sha(native) != NATIVE_SHA256:
        raise ValueError('The declared native 1IEP fixture changed.')
    lines = native.splitlines(keepends=True)
    first, last = lines.index(b'ROOT\n') + 1, lines.index(b'ENDROOT\n')
    assert last - first == 8
    assert all(line.startswith(b'ATOM') for line in lines[first:last])
    return b''.join(lines[: first + 1] + lines[first + 1 : last][::-1] + lines[last:])


def prepare_control(*, verify_profile=False):
    """Verify a literal order intervention and its existing source mapping."""
    baseline = load_baseline(verify_profile=verify_profile)
    source, controls, _, audit = prepare_controls(verify_profile=verify_profile)
    native = controls['native']['pdbqt'].encode()
    changed = fixed_first_control(native)
    records = _pdbqt_atom_records(changed.decode())
    original_records = _pdbqt_atom_records(native.decode())
    assert records[0] == original_records[0]
    mapping = controls['native']['pdbqt_to_source_atom_indices']
    indices = mapping[:1] + mapping[1:8][::-1] + mapping[8:]
    assert indices[:8] == [28, 58, 34, 33, 32, 31, 30, 29]
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[0]
    elements = msm.get(source, element='atom', atom_type=True)
    assert _source_atom_map(records, xyz, elements) == indices
    comparison = _compare_pdbqt(native, changed)
    tree = _compare_torsion_graphs(native, changed)
    assert comparison['coordinate_matched_atoms'] == 40
    assert comparison['matched_atom_type_disagreements'] == 0
    assert comparison['matched_charge_max_absolute_difference_e'] == 0
    assert tree['branch_bonds_match'] and tree['rigid_fragments_match']
    assert comparison['reference_torsion_dof'] == 7
    Vina(cpu=1, verbosity=0).set_ligand_from_string(changed.decode())
    control = {
        'pdbqt': changed.decode(),
        'sha256': sha(changed),
        'pdbqt_to_source_atom_indices': indices,
        'heavy_pdbqt_indices': [
            i for i, source_index in enumerate(indices) if elements[source_index] != 'H'
        ],
        'atom_comparison': comparison,
        'torsion_graph_comparison': tree,
        'first_root_source_atom_index': indices[0],
        'first_root_record': changed.splitlines()[
            changed.splitlines().index(b'ROOT') + 1
        ].decode(),
        'rigid_body_origin_angstrom': list(records[0][1]),
    }
    assert len(control['heavy_pdbqt_indices']) == 37
    return source, control, baseline, audit


def comparison_rows(record, baseline):
    """Join observed cells without treating reused searches as fresh runs."""
    rows = []
    for run in (
        baseline['original_native_runs'] + baseline['new_runs'] + record['new_runs']
    ):
        metrics = [
            row['heavy_atom_positional_rmsd_angstrom']
            for row in run['heavy_atom_metrics']
        ]
        parameters = run['result']['protocol_info']['parameters']
        rows.append(
            {
                'variant': 'native' if run['variant'] == 'flexible' else run['variant'],
                'seed': parameters['seed'],
                'exhaustiveness': parameters['exhaustiveness'],
                'poses': len(metrics),
                'first_heavy_rmsd_angstrom': metrics[0],
                'closest_heavy_rmsd_angstrom': min(metrics),
                'first_vina_score_kcal_mol': run['result']['poses'][0]['scores'][
                    'vina'
                ],
                'first_pose_recovered': metrics[0] <= 2.5,
                'returned_set_recovered': min(metrics) <= 2.5,
            }
        )
    return rows


def qualify():
    """Run the declared six cells once, keeping every outcome."""
    source, control, baseline, audit = prepare_control(verify_profile=True)
    scored = fixed_score(control, VARIANT)
    native_scores = baseline['fixed_conformation_scores']['native']['scores']
    assert scored['scores'] == native_scores
    runs = []
    for effort in (1, 8):
        for seed in (7, 42, 2026):
            runs.append(
                observe(
                    source, control, variant=VARIANT, seed=seed, exhaustiveness=effort
                )
            )
            print(
                f'{VARIANT}: completed {len(runs)}/6, seed={seed}, effort={effort}',
                file=sys.stderr,
            )
    record = {
        'schema': 'dockingmt.1iep_root_order_audit@1',
        'date': '2026-10-07',
        'interpreter': sys.executable,
        'python': sys.version,
        'consumer_base_commit': subprocess.check_output(
            ['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True
        ).strip(),
        'consumer_source_sha256': {
            **source_proof(),
            str(Path(__file__).relative_to(ROOT)): sha(Path(__file__).read_bytes()),
        },
        'provider_module': baseline['provider_module'],
        'qualified_provider_commit': baseline['qualified_provider_commit'],
        'provider_source_sha256': baseline['provider_source_sha256'],
        'provider_native_artifacts': baseline['provider_native_artifacts'],
        'producer_versions': baseline['producer_versions'],
        'baseline': {
            'path': str(BASELINE.relative_to(ROOT)),
            'sha256': BASELINE_SHA256,
            'published_by': 'dd571ef4dd0a1ddc9142e399a6da3683299a1db4',
            'original_native_producer': baseline['baseline']['source_producer'],
            'scope': '18 unchanged historical cells by authenticated reference; no reruns',
        },
        'audit': audit,
        'control': control,
        'new_runs': runs,
        'fixed_conformation_score': scored,
        'limits': [
            'Only seven ROOT line positions change; the first ROOT atom, its origin, membership, serials, labels, branch records and all other bytes remain fixed.',
            'One bound-like start, one external rigid receptor, three seeds and one fixed permutation; no convergence or recovery probability is established.',
            'Historical native/published/full-reversal searches retain their original producers; the earlier native repeat is not an independent matrix cell.',
            'A difference at fixed origin tests order sensitivity in this case; agreement would not prove general order invariance or that origin alone caused the full-reversal difference.',
            'All RMSDs use the earlier bounded positional correspondence without alignment or symmetry correction; no general matcher is introduced.',
            'Fixed-initial scoring equality is one observation, not energy-landscape or affinity equivalence.',
            'No ROOT/default policy, chemical-state qualification, provider migration or new installed/public artifact is selected by this experiment.',
        ],
    }
    record['comparison_rows'] = comparison_rows(record, baseline)
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    save(qualify(), args.output)
