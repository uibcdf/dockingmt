"""Measure native 1IEP preparation against pinned public PDBQT inputs.

This is a diagnostic for dockingmt#5. Coordinate matching is valid only for
this aligned source pair. Neither preparation is declared chemically validated.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

import molsysmt as msm
import pyunitwizard as puw

from devtools.validate_1iep_pdbqt import INPUT_SHA256, UPSTREAM_COMMIT
from dockingmt.preparation import prepare_ligand, prepare_receptor

SOURCE_RECEPTOR_SHA256 = (
    '5f6aee6029f9a2a2c2be32d4eb948ae70808690573e1b69a0850cdffd7048ca7'
)


def _read_pinned(path: Path, expected_sha256: str) -> bytes:
    content = path.read_bytes()
    if hashlib.sha256(content).hexdigest() != expected_sha256:
        raise ValueError(f'{path} differs from the pinned 1IEP input.')
    return content


def _pdbqt_inventory(content: bytes) -> dict[str, Any]:
    """Read exactly the fields needed for this aligned PDBQT comparison."""
    atoms = {}
    lines = content.decode('utf-8').splitlines()
    for line in lines:
        if not line.startswith(('ATOM', 'HETATM')):
            continue
        coordinate = tuple(float(line[offset : offset + 8]) for offset in (30, 38, 46))
        if coordinate in atoms:
            raise ValueError(
                'PDBQT has duplicate atom coordinates; mapping is ambiguous.'
            )
        fields = line.split()
        if len(fields) < 2:
            raise ValueError('PDBQT atom line has no charge and atom type.')
        atoms[coordinate] = {'charge': float(fields[-2]), 'type': fields[-1]}
    if not atoms:
        raise ValueError('PDBQT contains no atoms.')
    torsions = [int(line.split()[1]) for line in lines if line.startswith('TORSDOF')]
    if len(torsions) > 1:
        raise ValueError('PDBQT declares multiple torsion counts.')
    return {
        'atoms': atoms,
        'torsion_dof': torsions[0] if torsions else None,
        'branch_count': sum(line.startswith('BRANCH') for line in lines),
    }


def _compare_pdbqt(native: bytes, reference: bytes) -> dict[str, Any]:
    """Compare chemistry only after matching this case's aligned coordinates."""
    native_data = _pdbqt_inventory(native)
    reference_data = _pdbqt_inventory(reference)
    native_atoms = native_data['atoms']
    reference_atoms = reference_data['atoms']
    matched = native_atoms.keys() & reference_atoms.keys()
    mismatches = Counter(
        (native_atoms[key]['type'], reference_atoms[key]['type'])
        for key in matched
        if native_atoms[key]['type'] != reference_atoms[key]['type']
    )
    charge_deltas = [
        abs(native_atoms[key]['charge'] - reference_atoms[key]['charge'])
        for key in matched
    ]
    return {
        'native_atoms': len(native_atoms),
        'reference_atoms': len(reference_atoms),
        'coordinate_matched_atoms': len(matched),
        'native_only_atoms': len(native_atoms.keys() - reference_atoms.keys()),
        'reference_only_atoms': len(reference_atoms.keys() - native_atoms.keys()),
        'native_nonzero_charge_atoms': sum(
            abs(atom['charge']) > 0.0005 for atom in native_atoms.values()
        ),
        'reference_nonzero_charge_atoms': sum(
            abs(atom['charge']) > 0.0005 for atom in reference_atoms.values()
        ),
        'matched_atom_type_disagreements': sum(mismatches.values()),
        'atom_type_disagreement_counts': [
            {'native': native_type, 'reference': reference_type, 'count': count}
            for (native_type, reference_type), count in sorted(mismatches.items())
        ],
        'matched_charge_mean_absolute_difference_e': (
            sum(charge_deltas) / len(charge_deltas) if charge_deltas else None
        ),
        'matched_charge_max_absolute_difference_e': (
            max(charge_deltas) if charge_deltas else None
        ),
        'native_torsion_dof': native_data['torsion_dof'],
        'reference_torsion_dof': reference_data['torsion_dof'],
        'native_branch_count': native_data['branch_count'],
        'reference_branch_count': reference_data['branch_count'],
        'native_pdbqt_sha256': hashlib.sha256(native).hexdigest(),
        'reference_pdbqt_sha256': hashlib.sha256(reference).hexdigest(),
    }


def _reference_torsion_bonds(
    reference: bytes, source_coordinates: Any
) -> list[tuple[int, int]]:
    """Map this pinned aligned reference's BRANCH records to source atom indices."""
    coordinates = puw.get_value(source_coordinates, to_unit='angstrom')
    coordinate_to_source = {
        tuple(round(float(value), 3) for value in xyz): index
        for index, xyz in enumerate(coordinates)
    }
    if len(coordinate_to_source) != len(coordinates):
        raise ValueError('Source ligand has duplicate rounded coordinates.')
    serial_to_source = {}
    lines = reference.decode('utf-8').splitlines()
    for line in lines:
        if line.startswith(('ATOM', 'HETATM')):
            serial = int(line[6:11])
            xyz = tuple(float(line[offset : offset + 8]) for offset in (30, 38, 46))
            if serial in serial_to_source or xyz not in coordinate_to_source:
                raise ValueError(
                    'Reference atom has no unique source coordinate match.'
                )
            serial_to_source[serial] = coordinate_to_source[xyz]
    bonds = []
    for line in lines:
        if line.startswith('BRANCH'):
            parent, child = (int(serial) for serial in line.split()[1:3])
            if parent not in serial_to_source or child not in serial_to_source:
                raise ValueError('Reference branch has an unmapped atom serial.')
            bonds.append((serial_to_source[parent], serial_to_source[child]))
    return bonds


def _preparation_summary(prepared: Any) -> dict[str, Any]:
    metadata = prepared.metadata
    return {
        'source_n_atoms': metadata['source_n_atoms'],
        'retained_n_atoms': metadata['retained_n_atoms'],
        'omitted_hydrogen_count': len(metadata['omitted_hydrogen_indices']),
        'charge_source': metadata['charge_source'],
        'atom_type_source': metadata['atom_type_source'],
        'hydrogen_policy': metadata['hydrogen_policy'],
        'torsion_policy': metadata.get('torsion_policy'),
        'active_torsion_bonds': metadata.get('active_torsion_bonds'),
        'source_chemistry': metadata['source_chemistry'],
    }


def audit(
    source_receptor_path: Path,
    source_ligand_path: Path,
    reference_receptor_path: Path,
    reference_ligand_path: Path,
    report_path: Path,
    check_vina_parser: bool = False,
) -> dict[str, Any]:
    """Run DockingMT preparation using MolSysMT and save bounded evidence."""
    from rdkit import Chem

    paths = (
        source_receptor_path,
        source_ligand_path,
        reference_receptor_path,
        reference_ligand_path,
        report_path,
    )
    if len({path.resolve() for path in paths}) != len(paths):
        raise ValueError('Input and report paths must be distinct.')
    _read_pinned(source_receptor_path, SOURCE_RECEPTOR_SHA256)
    _read_pinned(source_ligand_path, INPUT_SHA256['source_ligand'])
    reference_receptor = _read_pinned(reference_receptor_path, INPUT_SHA256['receptor'])
    reference_ligand = _read_pinned(reference_ligand_path, INPUT_SHA256['partner'])

    source = msm.convert(source_receptor_path, to_form='molsysmt.MolSys')
    protein_indices = msm.select(
        source,
        selection="molecule_type=='protein'",
        chemical_state='structure',
        structure_indices=0,
    )
    protein = msm.extract(source, selection=protein_indices, structure_indices=0)
    provider_output = io.StringIO()
    with redirect_stdout(provider_output):
        added_bonds = msm.build.get_missing_bonds(protein)
    atom_names = msm.get(protein, element='atom', name=True)
    group_names = msm.get(protein, element='atom', group_name=True)
    group_ids = msm.get(protein, element='atom', group_id=True)
    added_bond_identifiers = [
        [
            {
                'atom_index': int(index),
                'atom_name': str(atom_names[index]),
                'group_name': str(group_names[index]),
                'group_id': str(group_ids[index]),
            }
            for index in pair
        ]
        for pair in added_bonds
    ]
    if added_bonds:
        protein.topology.add_bonds(added_bonds)
    prepared_receptor = prepare_receptor(protein, selection='all')

    molecules = list(Chem.SDMolSupplier(str(source_ligand_path), removeHs=False))
    if len(molecules) != 1 or molecules[0] is None:
        raise ValueError('The pinned SDF must contain one valid ligand.')
    ligand = msm.convert(molecules[0], to_form='molsysmt.MolSys')
    prepared_ligand = prepare_ligand(ligand, selection='all')
    source_coordinates = msm.get(ligand, element='atom', coordinates=True)[0]
    reference_bonds = _reference_torsion_bonds(reference_ligand, source_coordinates)
    flexible_ligand = prepare_ligand(
        ligand, selection='all', active_torsion_bonds=reference_bonds
    )

    native_receptor = prepared_receptor.to_pdbqt().encode('utf-8')
    native_ligand = prepared_ligand.to_pdbqt().encode('utf-8')
    report = {
        'schema_version': '1.0',
        'case': 'Official AutoDock Vina 1IEP preparation audit',
        'assessment': 'native_preparation_provisional_external_reference_unassessed',
        'reference_commit': UPSTREAM_COMMIT,
        'input_sha256': {
            'source_receptor': SOURCE_RECEPTOR_SHA256,
            'source_ligand': INPUT_SHA256['source_ligand'],
            'reference_receptor': INPUT_SHA256['receptor'],
            'reference_ligand': INPUT_SHA256['partner'],
        },
        'comparison_method': (
            'Exact PDBQT coordinates rounded to 0.001 angstrom; valid only for '
            'the pinned aligned 1IEP pair. No bond-order or chemical equivalence '
            'is inferred from PDBQT.'
        ),
        'receptor_connectivity': {
            'molsysmt_added_bonds': added_bond_identifiers,
            'provider_stdout_warning_count': sum(
                line.startswith('Warning!')
                for line in provider_output.getvalue().splitlines()
            ),
        },
        'receptor': {
            'preparation': _preparation_summary(prepared_receptor),
            'comparison': _compare_pdbqt(native_receptor, reference_receptor),
        },
        'ligand': {
            'preparation': _preparation_summary(prepared_ligand),
            'comparison': _compare_pdbqt(native_ligand, reference_ligand),
        },
        'flexible_ligand': {
            'selection_source': 'pinned_reference_branch_coordinate_map',
            'preparation': _preparation_summary(flexible_ligand),
            'comparison': _compare_pdbqt(
                flexible_ligand.to_pdbqt().encode('utf-8'), reference_ligand
            ),
        },
    }
    if check_vina_parser:
        import vina

        engine = vina.Vina(verbosity=0)
        engine.set_ligand_from_string(flexible_ligand.to_pdbqt())
        report['flexible_ligand']['vina_parser'] = {
            'accepted': True,
            'vina_version': getattr(vina, '__version__', 'unknown'),
        }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-receptor', required=True, type=Path)
    parser.add_argument('--source-ligand', required=True, type=Path)
    parser.add_argument('--reference-receptor', required=True, type=Path)
    parser.add_argument('--reference-ligand', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--check-vina-parser', action='store_true')
    args = parser.parse_args()
    audit(
        args.source_receptor,
        args.source_ligand,
        args.reference_receptor,
        args.reference_ligand,
        args.report,
        check_vina_parser=args.check_vina_parser,
    )


if __name__ == '__main__':
    main()
