"""Receive the real prepared protein through the native writer before adoption."""

import hashlib
import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molecular_fixtures import named_181l_pair
from vina import Vina

from devtools.qualify_chemical_templates import detached_record, snapshot


@pytest.fixture(scope='module')
def receptor():
    prepared, _ = named_181l_pair()
    return prepared


@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_real_receptor_preserves_native_ids_values_and_completed_lineage(
    receptor, length_unit, tmp_path
):
    native = receptor.source_molsys
    before = snapshot(native)
    charge_assignment = detached_record(
        native.molecular_mechanics.partial_charge_assignment
    )
    type_assignment = detached_record(native.molecular_mechanics.atom_type_assignment)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        text, mapping = msm.convert(
            native,
            to_form='string:pdbqt_text',
            typing_scheme='autodock4',
            structure_indices=0,
            return_atom_map=True,
        )
        composed = msm.compose_atom_maps(
            [receptor.metadata['preparation_workflow']['atom_map'], mapping]
        )
        assert puw.configure.report() == policy
    payload = text.removeprefix('pdbqt_text:')
    atoms = [line for line in payload.splitlines() if line.startswith('ATOM')]
    assert len(atoms) == receptor.n_atoms == 1615
    ids = list(msm.get(native, element='atom', atom_id=True))
    assert [str(int(line[6:11])) for line in atoms] == ids
    assert ids != [str(i + 1) for i in range(receptor.n_atoms)]
    assert [line[12:16].strip() for line in atoms] == receptor.atom_names
    assert [line[17:20].strip() for line in atoms] == receptor.group_names
    assert [int(line[22:26]) for line in atoms] == receptor.group_ids
    assert [line[77:].strip() for line in atoms] == receptor.atom_types
    np.testing.assert_allclose(
        [[float(line[i : i + 8]) for i in (30, 38, 46)] for line in atoms],
        puw.get_value(receptor.coordinates, to_unit='angstrom'),
        atol=0.000501,
        rtol=0,
    )
    assert [float(line[70:76]) for line in atoms] == [
        float(f'{charge:.3f}') for charge in receptor.charges
    ]
    assert mapping['payload_sha256'] == hashlib.sha256(payload.encode()).hexdigest()
    assert mapping['torsion_tree'] is None
    np.testing.assert_array_equal(
        mapping['output_to_source_atom_indices'], np.arange(1615)
    )
    np.testing.assert_array_equal(
        mapping['source_to_output_atom_indices'], np.arange(1615)
    )
    np.testing.assert_array_equal(
        mapping['partial_charge_before_rounding'], receptor.charges
    )
    assert mapping['charge_unit'] == 'elementary_charge'
    assert composed['n_source_atoms'] == 2603 and composed['n_output_atoms'] == 1615
    assert (
        composed['output_to_source_atom_indices'].tolist()
        == receptor.metadata['retained_atom_indices']
    )
    assert list(composed['source_atom_status']).count('merged') == 988
    assert composed['generated_output_atom_indices'].tolist() == []
    assert [stage['origin_schema'] for stage in composed['stages']] == [
        'molsysmt.atom_projection@1',
        'molsysmt.atom_export@1',
    ]
    assert charge_assignment['status'] == type_assignment['status'] == 'derived'
    for name, assignment in [
        ('PARTIAL_CHARGES', charge_assignment),
        ('ATOM_TYPES', type_assignment),
    ]:
        prefix = f'REMARK MOLSYSMT_{name} '
        remark = json.loads(
            next(
                line[len(prefix) :]
                for line in payload.splitlines()
                if line.startswith(prefix)
            )
        )
        assert remark['status'] == 'derived'
        assert remark['method'] == assignment['method']
    json.dumps(detached_record(mapping), allow_nan=False)
    json.dumps(detached_record(composed), allow_nan=False)
    path = tmp_path / 'native-181l-receptor.pdbqt'
    path.write_text(payload)
    Vina(cpu=1, verbosity=0).set_receptor(str(path))
    assert snapshot(native) == before
    assert (
        detached_record(native.molecular_mechanics.partial_charge_assignment)
        == charge_assignment
    )
    assert (
        detached_record(native.molecular_mechanics.atom_type_assignment)
        == type_assignment
    )


def test_serial_copy_cannot_claim_the_original_preparation_map(receptor):
    before = snapshot(receptor.source_molsys)
    native = msm.copy(receptor.source_molsys)
    msm.set(native, element='atom', atom_id=list(range(1, receptor.n_atoms + 1)))
    _, mapping = msm.convert(
        native,
        to_form='string:pdbqt_text',
        typing_scheme='autodock4',
        return_atom_map=True,
    )
    assert list(mapping['source_atom_ids']) != list(
        msm.get(receptor.source_molsys, element='atom', atom_id=True)
    )
    with pytest.raises(
        msm.StructuralInconsistencyError, match='Adjacent atom-map ids disagree'
    ):
        msm.compose_atom_maps(
            [receptor.metadata['preparation_workflow']['atom_map'], mapping]
        )
    assert snapshot(receptor.source_molsys) == before
