"""Compare preparation coverage cost against the recorded prior operation.

Run with the development interpreter and a qualified MolSysMT source. Requires
Git history containing 559f7c3. Saves five warm-cache samples per profile/role;
these local measurements are not universal performance or scientific claims.
"""

import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path
from statistics import median
from time import perf_counter

import molsysmt as msm

from dockingmt.preparation import prepare_ligand, prepare_receptor

BASELINE = '559f7c33096d80983f44de4df6a0263f5f4ff7ca'


def main():
    root = Path(__file__).resolve().parents[1]
    legacy_source = subprocess.check_output(
        ['git', 'show', f'{BASELINE}:dockingmt/preparation/_molsys.py'],
        cwd=root,
        text=True,
    )
    legacy_namespace = {}
    exec(compile(legacy_source, 'legacy_chemistry_evidence', 'exec'), legacy_namespace)
    source = msm.convert(
        msm.systems['T4 lysozyme L99A']['181l.pdb'], to_form='molsysmt.MolSys'
    )
    records = []
    for role, prepare, selection in (
        ('ligand', prepare_ligand, "group_name=='BNZ'"),
        ('receptor', prepare_receptor, "molecule_type=='protein'"),
    ):
        module = importlib.import_module('dockingmt.preparation.' + role)
        current = module.chemistry_evidence
        try:
            profiles = (
                ('legacy', legacy_namespace['chemistry_evidence']),
                ('provider_readiness', current),
            )
            samples = {name: [] for name, _ in profiles}
            prepared_by_profile = {}
            for _, evidence in profiles:
                module.chemistry_evidence = evidence
                prepare(source, selection=selection)
            for round_index in range(5):
                for profile, evidence in (
                    profiles if round_index % 2 == 0 else profiles[::-1]
                ):
                    module.chemistry_evidence = evidence
                    start = perf_counter()
                    prepared = prepare(source, selection=selection)
                    samples[profile].append(perf_counter() - start)
                    prepared_by_profile[profile] = prepared
            for profile, _ in profiles:
                prepared = prepared_by_profile[profile]
                records.append(
                    {
                        'role': role,
                        'profile': profile,
                        'retained_atoms': prepared.n_atoms,
                        'median_seconds': median(samples[profile]),
                        'samples_seconds': samples[profile],
                        'metadata_bytes': len(
                            json.dumps(prepared.metadata, sort_keys=True).encode()
                        ),
                    }
                )
        finally:
            module.chemistry_evidence = current
    payload = {
        'evidence': 'Local warm-cache preparation samples, not a universal speed claim.',
        'baseline_source': BASELINE,
        'baseline_operation': 'Prior chemistry_evidence only; remaining preparation code unchanged.',
        'sampling': 'Five paired rounds per role, alternating profile order after one warm-up per profile.',
        'python': sys.version.split()[0],
        'interpreter': sys.executable,
        'provider_import': msm.__file__,
        'qualified_provider_source': '3edbf8ad0a13b9a56a009c0bd3f707e54b807351',
        'provider_readiness_sha256': hashlib.sha256(
            Path(msm.__file__)
            .parent.joinpath('_private/chemical_readiness.py')
            .read_bytes()
        ).hexdigest(),
        'cases': records,
    }
    destination = root / 'devguide/validation/data/readiness/preparation_profile.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    main()
