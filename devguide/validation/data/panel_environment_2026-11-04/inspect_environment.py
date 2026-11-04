"""Inspect the two panel environments through public MolSysMT tools only.

Specific evidence producer: no chemical assignment, repair, preparation or search.
Inputs are the already recorded PDB archives; no new acquisition is performed.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

import molsysmt as msm
import pyunitwizard as puw


def encode(value):
    """Serialize returned provider values, retaining explicit length units."""
    if isinstance(value, dict):
        return {str(key): encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if value is None or isinstance(value, (str, bool, float, int)):
        return value
    if puw.is_quantity(value):
        return {
            'value': encode(puw.get_value(value, to_unit='angstrom')),
            'unit': 'angstrom',
        }
    if hasattr(value, 'tolist'):
        return encode(value.tolist())
    raise TypeError(f'Unserialized provider output: {type(value).__name__}')


def digest(value):
    return hashlib.sha256(
        json.dumps(encode(value), sort_keys=True).encode()
    ).hexdigest()


def get(system, **kwargs):
    return msm.get(system, get_missing_bonds=False, **kwargs)


def groups(system, selection):
    return get(
        system,
        element='group',
        selection=selection,
        output_type='dictionary',
        group_index=True,
        group_name=True,
        group_id=True,
        chain_index=True,
        chain_id=True,
        chain_name=True,
    )


def minimum(system, first, target):
    return msm.structure.get_minimum_distances(
        system,
        selection=first,
        selection_2=target,
        structure_indices=0,
        structure_indices_2=0,
        pbc=False,
        as_entity=True,
        as_entity_2=True,
    )


def snapshot(system):
    return digest(
        {
            'coordinates': get(system, coordinates=True, structure_indices=0),
            'chemistry': msm.physchem.get_chemical_readiness(
                system, structure_indices=0, chemical_state='structure'
            ),
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.mkdir(exist_ok=False)
    assert Path(msm.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    cases = []
    for entry, ligand in [
        ('1HSG', 'MK1'),
        ('1STP', 'BTN'),
    ]:
        source_manifest = json.loads((args.inputs / 'manifest.json').read_text())
        filename = f'{entry}.pdb.gz'
        member = next(x for x in source_manifest['records'] if x['path'] == filename)
        path = args.inputs / filename
        assert hashlib.sha256(path.read_bytes()).hexdigest() == member['sha256']
        source = msm.convert(str(path), get_missing_bonds=False)
        source_before = snapshot(source)
        assembly = msm.build.make_bioassembly(
            source, bioassembly='1', structure_indices=0
        )
        assembly_before = snapshot(assembly)
        ligand_groups = msm.select(
            assembly, selection=f'group_name=="{ligand}"', element='group'
        )
        # Freeze the first provider group-axis instance, independently of distances.
        target_group = int(ligand_groups[0])
        target = f'group_index=={target_group}'
        case = {
            'entry': entry,
            'ligand': ligand,
            'input_sha256': member['sha256'],
            'assembly': '1',
            'ligand_instances': groups(assembly, ligand_groups),
            'selected_target_group_index': target_group,
            'target_atoms': get(
                assembly,
                element='atom',
                selection=target,
                output_type='dictionary',
                atom_index=True,
                atom_name=True,
                atom_type=True,
            ),
            'water_shells': {},
            'other_ligands': [],
            'protein_termini': [],
        }
        for cutoff in [3.5, 5.0]:
            selection = (
                f'(group_type=="water") within {cutoff} angstroms '
                f'without pbc of ({target})'
            )
            selected = msm.select(
                assembly, selection=selection, structure_indices=0, element='group'
            )
            case['water_shells'][str(cutoff)] = {
                'cutoff': {'value': cutoff, 'unit': 'angstrom'},
                'groups': groups(assembly, selected),
            }
        for index in ligand_groups[1:]:
            other = f'group_index=={int(index)}'
            case['other_ligands'].append(
                {
                    'group': groups(assembly, [int(index)]),
                    'minimum_to_target': minimum(assembly, other, target),
                }
            )
        protein_chains = msm.select(
            assembly, selection='group_type=="amino acid"', element='chain'
        )
        for chain in protein_chains:
            protein = f'chain_index=={int(chain)} and group_type=="amino acid"'
            indices = msm.select(assembly, selection=protein, element='group')
            terminal = {
                'chain_index': int(chain),
                'protein_group_count': len(indices),
                'boundaries': [],
            }
            for position, index in [
                ('first_observed', indices[0]),
                ('last_observed', indices[-1]),
            ]:
                selected = f'group_index=={int(index)}'
                terminal['boundaries'].append(
                    {
                        'position': position,
                        'group': groups(assembly, [int(index)]),
                        'atom_names': get(
                            assembly, element='atom', selection=selected, atom_name=True
                        ),
                        'minimum_to_target': minimum(assembly, selected, target),
                    }
                )
            case['protein_termini'].append(terminal)
        case['source_coordinate_chemistry_digest_before'] = source_before
        case['source_coordinate_chemistry_digest_after'] = snapshot(source)
        case['assembly_coordinate_chemistry_digest_before'] = assembly_before
        case['assembly_coordinate_chemistry_digest_after'] = snapshot(assembly)
        assert case['source_coordinate_chemistry_digest_after'] == source_before
        assert case['assembly_coordinate_chemistry_digest_after'] == assembly_before
        cases.append(encode(case))
        (args.output / 'observations.json').write_text(
            json.dumps({'cases': cases}, indent=2) + '\n'
        )
    print(json.dumps({'cases': len(cases), 'preparations': 0, 'searches': 0}))


if __name__ == '__main__':
    main()
