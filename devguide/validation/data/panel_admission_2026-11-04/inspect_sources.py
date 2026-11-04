"""Inspect the two proposed panel sources through public MolSysMT operations.

This is a case-specific evidence producer, not a molecular inspection API.
Run with an ordinary-installed scientific interpreter and a new output folder.
No search, preparation, chemistry completion or independent molecular parser.
"""

import argparse
import hashlib
import importlib.metadata as metadata
import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import molsysmt as msm
import pyunitwizard as puw


def encode(value):
    """Encode provider output without interpreting molecular content."""
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(item) for item in value]
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if puw.is_quantity(value):
        return {'value': encode(puw.get_value(value, to_unit='nm')), 'unit': 'nm'}
    if hasattr(value, 'tolist'):
        return encode(value.tolist())
    return str(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument(
        '--reuse', type=Path, help='Verified acquisition-only input ledger'
    )
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(exist_ok=False)
    reused = json.loads(args.reuse.read_text()) if args.reuse else {}
    prefix = Path(sys.prefix).resolve()
    assert Path(msm.__file__).resolve().is_relative_to(prefix)
    record = {
        'schema': 'dockingmt.panel_source_inspection@1',
        'owner': 'uibcdf/dockingmt#33',
        'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'started_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version.split()[0],
        'versions': {
            name: metadata.version(name)
            for name in ['molsysmt', 'argdigest', 'pyunitwizard', 'smonitor', 'openmm']
        },
        'ordinary_molsysmt_origin_verified': True,
        'cases': [],
        'searches': 0,
        'preparations': 0,
    }

    def observe(label, operation, target):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            try:
                value = operation()
                target[label] = {'status': 'returned', 'value': encode(value)}
            except Exception as error:
                message = str(error).replace(str(output), '<output>')
                message = message.replace(str(prefix), '<installed-prefix>')
                target[label] = {
                    'status': 'error',
                    'type': type(error).__name__,
                    'message': message,
                }
                value = None
            target[label]['warnings'] = [
                {'category': item.category.__name__, 'message': str(item.message)}
                for item in caught
            ]
        return value

    def get(system, **kwargs):
        return msm.get(system, get_missing_bonds=False, **kwargs)

    def inventory(system):
        return {
            'counts': get(
                system,
                output_type='dictionary',
                n_atoms=True,
                n_groups=True,
                n_chains=True,
                n_structures=True,
                n_bonds=True,
            ),
            'chains': get(
                system,
                element='chain',
                output_type='dictionary',
                chain_index=True,
                chain_id=True,
                chain_name=True,
            ),
            'groups': get(
                system,
                element='group',
                output_type='dictionary',
                group_index=True,
                group_id=True,
                group_name=True,
                group_type=True,
                chain_id=True,
            ),
        }

    for entry, ligand in [('1HSG', 'MK1'), ('1STP', 'BTN')]:
        case = {'entry': entry, 'ligand': ligand, 'sources': []}
        record['cases'].append(case)
        for extension, download in [
            ('pdb', msm.form.file_pdb.download),
            ('cif', msm.form.file_cif.download),
        ]:
            path = output / f'{entry}.{extension}'
            source = {
                'filename': path.name,
                'url': f'https://files.rcsb.org/download/{path.name}',
            }
            case['sources'].append(source)
            if path.name in reused:
                acquired = Path(reused[path.name]['path'])
                payload = acquired.read_bytes()
                assert (
                    hashlib.sha256(payload).hexdigest() == reused[path.name]['sha256']
                )
                path.write_bytes(payload)
                source['download'] = {
                    'status': 'reused',
                    'warnings': [],
                    'value': path.name,
                    'origin': 'prior_acquisition',
                }
            else:
                observe(
                    'download',
                    lambda: download(
                        entry, output_filename=str(path), retries=1, timeout=15
                    ),
                    source,
                )
            if source['download']['status'] == 'returned':
                source['download']['value'] = path.name
            if not path.exists():
                continue
            source['bytes'] = path.stat().st_size
            source['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            # Both declared representations are inspected independently.
            # CIF uses its provider's existing reader policy, recorded separately.
            options = {'get_missing_bonds': False} if extension == 'pdb' else {}
            source['reader_policy'] = (
                'explicit_only'
                if extension == 'pdb'
                else 'existing_provider_cif_policy'
            )
            system = observe(
                'convert', lambda: msm.convert(str(path), **options), source
            )
            if system is None:
                continue
            # Native objects stay in memory; only provider observations are serialized.
            source['convert']['value'] = 'molsysmt.MolSys'
            before = encode(inventory(system))
            source['inventory'] = before
            observe('bioassembly', lambda: get(system, bioassembly=True), source)
            observe(
                'alternate_locations',
                lambda: get(
                    system, element='atom', structure_indices=0, alternate_location=True
                ),
                source,
            )
            observe(
                'occupancy',
                lambda: get(
                    system, element='atom', structure_indices=0, occupancy=True
                ),
                source,
            )
            observe(
                'missing_heavy_atoms',
                lambda: msm.build.get_missing_heavy_atoms(system, engine='MolSysMT'),
                source,
            )
            observe(
                'chemical_readiness',
                lambda: msm.physchem.get_chemical_readiness(
                    system,
                    selection=f'group_name=="{ligand}"',
                    structure_indices=0,
                    chemical_state='structure',
                ),
                source,
            )
            observe(
                'ligand_atoms',
                lambda: get(
                    system,
                    element='atom',
                    selection=f'group_name=="{ligand}"',
                    output_type='dictionary',
                    atom_index=True,
                    atom_id=True,
                    atom_name=True,
                    atom_type=True,
                    group_index=True,
                    group_id=True,
                    chain_id=True,
                ),
                source,
            )
            assembly = observe(
                'make_bioassembly_1',
                lambda: msm.build.make_bioassembly(
                    system, bioassembly='1', structure_indices=0
                ),
                source,
            )
            if assembly is not None:
                source['make_bioassembly_1']['value'] = encode(inventory(assembly))
            # This query uses the provider's internal conversion/default policy;
            # it is not evidence about connectivity in the explicit-only object.
            if extension == 'pdb':
                observe(
                    'raw_alternate_locations',
                    lambda: msm.form.file_pdb.has_atoms_with_alternate_locations(
                        str(path)
                    ),
                    source,
                )
                observe(
                    'missing_residues',
                    lambda: msm.build.get_missing_residues(
                        str(path), engine='MolSysMT'
                    ),
                    source,
                )
            source['inventory_unchanged'] = before == encode(inventory(system))
            source['bytes_unchanged'] = (
                source['sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
            )
        (output / 'inspection.json').write_text(
            json.dumps(encode(record), indent=2) + '\n'
        )
    record['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'inspection.json').write_text(json.dumps(encode(record), indent=2) + '\n')
    print(json.dumps({'cases': len(record['cases']), 'searches': 0, 'preparations': 0}))


if __name__ == '__main__':
    main()
