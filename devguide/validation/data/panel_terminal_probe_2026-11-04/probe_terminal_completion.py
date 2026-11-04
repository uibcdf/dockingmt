"""Probe provider terminal completion on the observed 1HSG protein copy.

Software receiving only: the output is not an admitted panel receptor.
All molecular reading, selection, generation and characterization use MolSysMT.
"""

import argparse
import hashlib
import json
import sys
import warnings
from pathlib import Path

import molsysmt as msm
import pyunitwizard as puw


def encode(value):
    """Encode returned observations without molecular interpretation."""
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
    raise TypeError(type(value).__name__)


def get(system, **kwargs):
    return msm.get(system, get_missing_bonds=False, **kwargs)


def snapshot(system):
    return {
        'counts': get(
            system, n_atoms=True, n_groups=True, n_bonds=True, output_type='dictionary'
        ),
        'atom_attributes': get(
            system,
            element='atom',
            atom_index=True,
            atom_id=True,
            atom_name=True,
            atom_type=True,
            group_index=True,
            output_type='dictionary',
        ),
        'coordinates': get(system, coordinates=True, structure_indices=0),
        'chemical_readiness': msm.physchem.get_chemical_readiness(
            system, structure_indices=0, chemical_state='structure'
        ),
    }


def digest(value):
    return hashlib.sha256(
        json.dumps(encode(value), sort_keys=True).encode()
    ).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.mkdir(exist_ok=False)
    assert Path(msm.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
    manifest = json.loads((args.inputs / 'manifest.json').read_text())
    member = next(x for x in manifest['records'] if x['path'] == '1HSG.pdb.gz')
    path = args.inputs / member['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == member['sha256']
    source = msm.convert(str(path), get_missing_bonds=False)
    source_before = digest(snapshot(source))
    receptor = msm.extract(source, selection='group_type=="amino acid"')
    before = encode(snapshot(receptor))
    record = {
        'entry': '1HSG',
        'scope': 'unadmitted_terminal_software_control',
        'producer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'input_sha256': member['sha256'],
        'before': before,
        'missing_terminal_before': msm.build.get_missing_terminal_cappings(receptor),
        'missing_standard_heavy_before': msm.build.get_missing_heavy_atoms(receptor),
        'history_before': receptor.chemical_states.get_preparation_history(),
    }
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        result = msm.build.add_missing_terminal_cappings(
            receptor,
            N_terminal=None,
            C_terminal=None,
            pH=7.4,
            keep_ids=True,
            engine='MolSysMT',
        )
    record['warnings'] = [
        {'category': w.category.__name__, 'message': str(w.message)} for w in caught
    ]
    record['return_form'] = msm.get_form(result)
    record['returned_dict_with_report'] = isinstance(result, dict)
    record['after'] = snapshot(result)
    record['history_after'] = result.chemical_states.get_preparation_history()
    record['missing_terminal_after'] = msm.build.get_missing_terminal_cappings(result)
    record['missing_standard_heavy_after'] = msm.build.get_missing_heavy_atoms(result)
    record['generated_oxt_observation'] = get(
        result,
        element='atom',
        selection='atom_name=="OXT"',
        atom_index=True,
        atom_id=True,
        atom_name=True,
        group_index=True,
        output_type='dictionary',
    )
    record['explicit_hydrogen_indices_after'] = msm.select(
        result, selection='atom_type=="H"'
    )
    record['source_digest_unchanged'] = source_before == digest(snapshot(source))
    record['receptor_input_digest_unchanged'] = digest(before) == digest(
        snapshot(receptor)
    )
    # This diagnostic detects reordered axes; it does not construct an atom map.
    old_ids = before['atom_attributes']['atom_id']
    new_ids = record['after']['atom_attributes']['atom_id']
    record['old_id_prefix_preserved'] = old_ids == list(new_ids[: len(old_ids)])
    record['old_atom_coordinate_preservation'] = 'unassessed_without_provider_atom_map'
    (args.output / 'observations.json').write_text(
        json.dumps(encode(record), indent=2) + '\n'
    )
    print(
        json.dumps(
            {
                'source_unchanged': record['source_digest_unchanged'],
                'receptor_input_unchanged': record['receptor_input_digest_unchanged'],
                'dict_report': record['returned_dict_with_report'],
                'searches': 0,
                'panel_preparations': 0,
            }
        )
    )


if __name__ == '__main__':
    main()
