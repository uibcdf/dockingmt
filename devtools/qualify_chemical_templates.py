"""Qualify explicit MolSysMT template transfer at DockingMT's input boundary.

All molecular construction, conversion, inspection and assignment use public
MolSysMT tools. The deliberately incomplete 5X72 controls are not original SDF
inputs. Successful transfer is not a docking-readiness certificate.
"""

import hashlib
import importlib.metadata as metadata
import json
import sys
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

from dockingmt.preparation import prepare_ligand

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_REVISION = 'c19a47ada0c2279029abfa296cf915560610ad9a'
SDF_DIGESTS = {
    'p59': 'ef26c05a198a16972efcf8baae644f6b38fd953561f130ee230626088766b08a',
    'p69': '637a992134b2038a0ea3cff0c1f8355ea232720c9eae5347100b7186170fcdf1',
}


def _numpy_json(value):
    """Encode numeric report arrays; units remain in the provider report."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f'Unsupported evidence value: {type(value).__name__}')


def detached_record(value):
    return json.loads(json.dumps(value, default=_numpy_json, allow_nan=False))


def snapshot(system):
    """Capture public native values with their declared fixed protocol units."""
    record = msm.convert(system, to_form='molsysmt.MolSysDict').data
    record['chemical_states'] = msm.convert(
        system.chemical_states, to_form='molsysmt.ChemicalStatesDict'
    ).to_dict()
    record['structure_units'] = {
        'coordinates': 'nm',
        'box': 'nm',
        'time': 'ps',
    }
    # This nullable public axis is separate from the topology reference state.
    associations = msm.get(system, structure_chemical_state_index=True)
    record['structure_chemical_state_indices'] = [
        None if value is None or str(value) == '<NA>' else int(value)
        for value in associations
    ]
    return detached_record(record)


def record_digest(record):
    payload = json.dumps(
        detached_record(record), sort_keys=True, separators=(',', ':'), allow_nan=False
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def template_options(template, correspondence, *, identity, uri, hydrogen_policy):
    """Identify the actual native template, separately from its source file."""
    return {
        'template': template,
        'atom_correspondence': correspondence,
        'template_provenance': {
            'identity': identity,
            'version': f'MolSysMT {msm.__version__}; RDKit {metadata.version("rdkit")}',
            'source_uri': uri,
            'checksum': 'sha256:' + record_digest(snapshot(template)),
            'checksum_scope': 'canonical native snapshot including chemical states and declared structure units',
            'hydrogen_policy': hydrogen_policy,
        },
    }


def load_5x72(name):
    """Read the unchanged native SDF, then explicitly select an adapter template."""
    path = ROOT / f'tests/data/vina_torsions/5x72_ligand_{name}H.sdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == SDF_DIGESTS[name]
    original = msm.convert(
        path,
        to_form='molsysmt.MolSys',
        stereo_engine='rdkit',
        discard_properties=True,
    )
    template = msm.convert(
        msm.convert(original, to_form='rdkit.Mol'), to_form='molsysmt.MolSys'
    )
    return original, template


def make_5x72_control(original, *, missing_edge=False):
    """Build a permuted, two-frame absent-chemistry control from declared values.

    The permutation is explicitly constructed, not discovered by atom matching.
    The second translated frame, box and time are preservation controls.
    """
    n_atoms = msm.get(original, n_atoms=True)
    order = np.arange(n_atoms)[::-1]
    inverse = np.argsort(order)
    atoms = msm.get(
        original,
        element='atom',
        atom_id=True,
        atom_name=True,
        atom_type=True,
        output_type='dictionary',
    )
    builder = msm.MolSysBuilder()
    for index in order:
        builder.add_atom(**{field: values[index] for field, values in atoms.items()})
    builder.add_group(
        np.arange(n_atoms), group_id='1', group_name='LIG', group_type='small molecule'
    )
    pairs = msm.get(original, element='bond', bonded_atom_pairs=True)
    for first, second in pairs[1:] if missing_edge else pairs:
        builder.add_bond(int(inverse[first]), int(inverse[second]))
    xyz = puw.get_value(msm.get(original, coordinates=True), to_unit='angstrom')[0]
    frames = np.stack((xyz[order], xyz[order] + [10.0, -7.0, 2.0]))
    builder.set_coordinates(puw.quantity(frames, 'angstrom'))
    builder.set_box(puw.quantity(np.tile(np.eye(3) * 100, (2, 1, 1)), 'angstrom'))
    builder.set_time(puw.quantity([0.0, 7.0], 'fs'))
    system = builder.build()
    msm.set(system, structure_chemical_state_index=[0, 0])
    return system, np.column_stack((np.arange(n_atoms), inverse))


def load_181l_benzene():
    path = Path(msm.systems['T4 lysozyme L99A']['181l.pdb'])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        '77018feaaa65bb22dea47c784e8c059b0ccc09cd6dc7442b79cce83f3170985f'
    )
    full = msm.convert(path, to_form='molsysmt.MolSys')
    indices = msm.select(full, selection="group_name=='BNZ'")
    source = msm.extract(full, selection=indices)
    # Fixture-specific declaration: C1..C6 form the declared SMILES ring order.
    assert msm.get(source, element='atom', atom_name=True) == [
        'C1',
        'C2',
        'C3',
        'C4',
        'C5',
        'C6',
    ]
    template = msm.convert(
        msm.convert('smiles:c1ccccc1', to_form='rdkit.Mol'), to_form='molsysmt.MolSys'
    )
    return source, template, indices


def checked_application(source, options):
    before_source = snapshot(source)
    before_template = snapshot(options['template'])
    assessment = msm.physchem.assess_chemical_template(source, **options)
    assert snapshot(source) == before_source
    assert snapshot(options['template']) == before_template
    assert assessment['status'] == 'compatible'
    result = msm.physchem.apply_chemical_template(source, **options)
    assert result['molecular_system'] is not source
    assert snapshot(source) == before_source
    assert snapshot(options['template']) == before_template
    after = snapshot(result['molecular_system'])
    for field in ('atoms', 'groups', 'chains'):
        assert after['topology'][field] == before_source['topology'][field]
    assert after['structures'] == before_source['structures']
    assert (
        after['structure_chemical_state_indices']
        == before_source['structure_chemical_state_indices']
    )
    return result, before_source, after


def checked_rejection(source, options, expected):
    """Retain failed preflight and verify that application leaves inputs intact."""
    before_source, before_template = snapshot(source), snapshot(options['template'])
    report = msm.physchem.assess_chemical_template(source, **options)
    assert report['status'] == expected
    try:
        msm.physchem.apply_chemical_template(source, **options)
    except msm.StructuralInconsistencyError as error:
        assert error.report['status'] == expected
    else:
        raise AssertionError('Unresolved template application unexpectedly succeeded')
    assert snapshot(source) == before_source
    assert snapshot(options['template']) == before_template
    return detached_record(report)


def qualify():
    cases = []
    for name in ('p59', 'p69'):
        original, template = load_5x72(name)
        source, correspondence = make_5x72_control(original)
        options = template_options(
            template,
            correspondence,
            identity=f'5X72 {name.upper()} explicit RDKit-adapter assignments',
            uri=f'repository:tests/data/vina_torsions/5x72_ligand_{name}H.sdf#native-to-rdkit-to-native',
            hydrogen_policy='explicit_atoms',
        )
        result, before, after = checked_application(source, options)
        chosen = msm.extract(result['molecular_system'], structure_indices=1)
        ligand = prepare_ligand(chosen, selection='all')
        raw_options = {
            **options,
            'atom_correspondence': np.column_stack((np.arange(39), np.arange(39))),
        }
        raw_assessment = checked_rejection(original, raw_options, 'unassessed')
        cases.append(
            {
                'case': f'5X72 {name.upper()} permuted absent-field control',
                'source_file_sha256': SDF_DIGESTS[name],
                'control': 'same stored graph; all chemical assignments omitted; reversed atom order; two frames',
                'source_snapshot_sha256': record_digest(before),
                'applied_snapshot_sha256': record_digest(after),
                'template_snapshot': snapshot(template),
                'application_report': detached_record(result['report']),
                'original_sdf_assessment': detached_record(raw_assessment),
                'chosen_structure_index': 1,
                'prepared_ligand': ligand.to_dict(),
                'pdbqt_sha256': hashlib.sha256(ligand.to_pdbqt().encode()).hexdigest(),
            }
        )
    source, template, full_indices = load_181l_benzene()
    options = template_options(
        template,
        np.column_stack((np.arange(6), np.arange(6))),
        identity='Explicit heavy-only benzene SMILES template',
        uri='smiles:c1ccccc1',
        hydrogen_policy='stored_counts',
    )
    result, before, after = checked_application(source, options)
    ligand = prepare_ligand(result['molecular_system'], selection='all')
    cases.append(
        {
            'case': '181L original BNZ heavy-atom source',
            'source_file_sha256': '77018feaaa65bb22dea47c784e8c059b0ccc09cd6dc7442b79cce83f3170985f',
            'full_source_atom_indices': full_indices,
            'source_snapshot_sha256': record_digest(before),
            'applied_snapshot_sha256': record_digest(after),
            'template_snapshot': snapshot(template),
            'application_report': detached_record(result['report']),
            'prepared_ligand': ligand.to_dict(),
            'pdbqt_sha256': hashlib.sha256(ligand.to_pdbqt().encode()).hexdigest(),
        }
    )
    negative_controls = []
    original, template = load_5x72('p59')
    for name in ('charge', 'enantiomer', 'missing-edge'):
        source, correspondence = make_5x72_control(
            original, missing_edge=name == 'missing-edge'
        )
        if name == 'charge':
            msm.set(source, element='atom', selection=[38], formal_charge=[1])
        elif name == 'enantiomer':
            msm.set(source, element='atom', selection=[31], atom_stereochemistry=['S'])
        options = template_options(
            template,
            correspondence,
            identity='5X72 P59 explicit RDKit-adapter assignments',
            uri='repository:tests/data/vina_torsions/5x72_ligand_p59H.sdf#native-to-rdkit-to-native',
            hydrogen_policy='explicit_atoms',
        )
        negative_controls.append(
            {'case': name, 'assessment': checked_rejection(source, options, 'conflict')}
        )
    return detached_record(
        {
            'schema': 'dockingmt.chemical_template_qualification@1',
            'evidence': 'Bounded software transfer/consumer qualification, not template authenticity, docking validation or a performance benchmark',
            'provider_reference_source': PROVIDER_REVISION,
            'provider_import': msm.__file__,
            'provider_implementation_sha256': {
                relative: hashlib.sha256(
                    (Path(msm.__file__).parent / relative).read_bytes()
                ).hexdigest()
                for relative in (
                    'physchem/assess_chemical_template.py',
                    'physchem/apply_chemical_template.py',
                    '_private/chemical_template.py',
                    'form/rdkit_Mol/to_molsysmt_Topology.py',
                )
            },
            'python': sys.version.split()[0],
            'interpreter': sys.executable,
            'versions': {
                name: metadata.version(name)
                for name in ('rdkit', 'numpy', 'pandas', 'vina')
            },
            'cases': cases,
            'negative_controls': negative_controls,
        }
    )


def main():
    record = qualify()
    destination = ROOT / 'devguide/validation/data/chemical_templates/cases.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(record, indent=2) + '\n')
    print(destination)
    for case in record['cases']:
        print(
            case['case'],
            case['application_report']['status'],
            'retained atoms:',
            case['prepared_ligand']['n_atoms'],
        )


if __name__ == '__main__':
    main()
