"""Explicit provider template transfer remains bounded at the docking boundary."""

import hashlib
import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_REC_PDBQT

from devtools.qualify_chemical_templates import (
    ROOT,
    SDF_DIGESTS,
    checked_application,
    detached_record,
    load_5x72,
    load_181l_benzene,
    make_5x72_control,
    record_digest,
    snapshot,
    template_options,
)
from dockingmt import BoxRegion, DockingProblem, DockingResult, VinaProtocol
from dockingmt._private.smonitor import ArgumentError
from dockingmt.engines.vina import VinaBackend
from dockingmt.preparation import prepare_ligand


@pytest.fixture
def p59():
    original, template = load_5x72('p59')
    source, correspondence = make_5x72_control(original)
    options = template_options(
        template,
        correspondence,
        identity='Pinned 5X72 P59 declared adapter template',
        uri='repository:tests/data/vina_torsions/5x72_ligand_p59H.sdf#native-to-rdkit-to-native',
        hydrogen_policy='explicit_atoms',
    )
    return source, options


@pytest.mark.parametrize('name,label', [('p59', 'R'), ('p69', 'S')])
def test_permuted_template_result_reaches_preparation_with_selected_pose(name, label):
    original, template = load_5x72(name)
    source, correspondence = make_5x72_control(original)
    options = template_options(
        template,
        correspondence,
        identity=f'Pinned 5X72 {name.upper()} declared adapter template',
        uri=f'repository:tests/data/vina_torsions/5x72_ligand_{name}H.sdf#native-to-rdkit-to-native',
        hydrogen_policy='explicit_atoms',
    )
    # A different application unit policy must not alter stored poses or chemistry.
    with puw.context(standard_units=['pm', 'fs']):
        result, before, after = checked_application(source, options)
        applied = result['molecular_system']
        assert msm.get(applied, n_atoms=True) == 39
        assert msm.get(applied, n_bonds=True) == 42
        assert msm.get(applied, n_structures=True) == 2
        assert msm.get(applied, element='atom', atom_stereochemistry=True)[31] == label
        assert list(msm.get(applied, element='atom', formal_charge=True)) == [0] * 39
        for attribute in ('n_implicit_hydrogens', 'n_explicit_hydrogens'):
            assert (
                list(msm.get(applied, element='atom', **{attribute: True})) == [0] * 39
            )
        assert puw.get_unit(msm.get(applied, coordinates=True)) == puw.get_unit(
            msm.get(source, coordinates=True)
        )
        chosen = msm.extract(applied, structure_indices=1)
        prepared = prepare_ligand(chosen, selection='all')
        retained = prepared.metadata['retained_atom_indices']
        # Unit standardization may round at machine precision; the two frames
        # differ by 1 nm and application itself preserves the stored geometry.
        np.testing.assert_allclose(
            puw.get_value(prepared.coordinates, to_unit='nm'),
            np.asarray(before['structures']['coordinates'])[1, retained],
            rtol=0,
            atol=1e-12,
        )
    assert before['structures'] == after['structures']
    assert prepared.n_atoms == 25  # 24 heavy atoms and one polar H.
    assert prepared.metadata['source_n_atoms'] == 39
    assert len(prepared.metadata['omitted_hydrogen_indices']) == 14
    readiness = prepared.metadata['source_chemistry']['chemical_readiness']
    assert readiness['fields']['formal_charge']['status'] == 'present'
    assert readiness['fields']['covalent_multiplicity']['status'] == 'present'
    assert readiness['n_explicit_hydrogens'] == 15
    assert readiness['connectivity']['declared_completeness'] == 'complete'
    assert 'docking_readiness' in readiness['unassessed_checks']
    assert prepared.metadata['charge_source'] == 'zero_placeholder'
    assert prepared.metadata['atom_type_source'] == 'element_aromaticity_heuristic'
    report = result['report']
    np.testing.assert_array_equal(report['atom_correspondence'], correspondence)
    assert report['coverage']['hydrogen_policy'] == 'explicit_atoms'
    assert 'docking_readiness' in report['unassessed_checks']
    assert report['units']['formal_charge'] == 'elementary_charge'
    assert report['template_provenance']['checksum'] == (
        'sha256:' + record_digest(snapshot(template))
    )
    # The provider report is a detached workflow record, not native provenance.
    saved = detached_record(report)
    saved['template_provenance']['identity'] = 'edited copy'
    assert report['template_provenance'] == options['template_provenance']
    path = ROOT / f'tests/data/vina_torsions/5x72_ligand_{name}H.sdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == SDF_DIGESTS[name]


def test_original_181l_benzene_accepts_declared_heavy_only_template():
    source, template, full_indices = load_181l_benzene()
    options = template_options(
        template,
        np.column_stack((np.arange(6), np.arange(6))),
        identity='Declared heavy-only benzene',
        uri='smiles:c1ccccc1',
        hydrogen_policy='stored_counts',
    )
    result, before, after = checked_application(source, options)
    applied = result['molecular_system']
    assert len(full_indices) == 6
    assert msm.get(applied, n_atoms=True) == 6
    assert list(msm.get(applied, element='atom', n_implicit_hydrogens=True)) == [1] * 6
    assert (
        list(msm.get(applied, element='bond', fractional_bond_order=True)) == [1.5] * 6
    )
    assert before['structures'] == after['structures']
    ligand = prepare_ligand(applied, selection='all')
    assert ligand.atom_types == ['A'] * 6
    assert (
        ligand.metadata['source_chemistry']['chemical_readiness'][
            'n_explicit_hydrogens'
        ]
        == 0
    )
    assert ligand.metadata['charge_source'] == 'zero_placeholder'


@pytest.mark.parametrize('name', ['p59', 'p69'])
def test_original_sdf_representation_mismatch_is_unassessed_without_repair(name):
    original, template = load_5x72(name)
    options = template_options(
        template,
        np.column_stack((np.arange(39), np.arange(39))),
        identity='Declared RDKit-adapter template',
        uri=f'repository:5x72_ligand_{name}H.sdf#native-to-rdkit-to-native',
        hydrogen_policy='explicit_atoms',
    )
    before = snapshot(original)
    report = msm.physchem.assess_chemical_template(original, **options)
    assert report['status'] == 'unassessed'
    assert {issue['reason_code'] for issue in report['issues']} == {
        'aromatic_representation_requires_normalization'
    }
    with pytest.raises(msm.StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(original, **options)
    assert error.value.report['status'] == 'unassessed'
    assert snapshot(original) == before


@pytest.mark.parametrize('name', ['p59', 'p69'])
def test_native_sdf_is_not_automatically_a_complete_template(name):
    original, _ = load_5x72(name)
    options = template_options(
        original,
        np.column_stack((np.arange(39), np.arange(39))),
        identity='Original SDF completeness control',
        uri=f'repository:5x72_ligand_{name}H.sdf',
        hydrogen_policy='explicit_atoms',
    )
    before = snapshot(original)
    assessment = msm.physchem.assess_chemical_template(original, **options)
    assert assessment['status'] == 'unassessed'
    assert 'template_field_not_declared' in {
        issue['reason_code'] for issue in assessment['issues']
    }
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.physchem.apply_chemical_template(original, **options)
    assert snapshot(original) == before


@pytest.mark.parametrize('conflict', ['charge', 'enantiomer', 'missing-edge'])
def test_incompatible_transfer_fails_without_modifying_inputs(p59, conflict):
    source, options = p59
    if conflict == 'charge':
        msm.set(source, element='atom', selection=[38], formal_charge=[1])
    elif conflict == 'enantiomer':
        msm.set(source, element='atom', selection=[31], atom_stereochemistry=['S'])
    else:
        original, _ = load_5x72('p59')
        source, options['atom_correspondence'] = make_5x72_control(
            original, missing_edge=True
        )
    before_source, before_template = snapshot(source), snapshot(options['template'])
    report = msm.physchem.assess_chemical_template(source, **options)
    assert report['status'] == 'conflict'
    assert report['issues']
    with pytest.raises(msm.StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **options)
    assert error.value.report['status'] == 'conflict'
    assert snapshot(source) == before_source
    assert snapshot(options['template']) == before_template


def test_map_must_include_every_explicit_hydrogen(p59):
    source, options = p59
    # Heavy-only map against all-atom inputs is invalid; no inferred H matching.
    options['atom_correspondence'] = options['atom_correspondence'][:24]
    before = snapshot(source)
    with pytest.raises(msm.ArgumentError):
        msm.physchem.apply_chemical_template(source, **options)
    assert snapshot(source) == before


def test_existing_matching_assignment_is_preserved(p59):
    source, options = p59
    msm.set(source, element='atom', selection=[38], formal_charge=[0])
    result, _, _ = checked_application(source, options)
    report = result['report']
    assert any(
        entry['axis'] == 'atom'
        and entry['field'] == 'formal_charge'
        and entry['index'] == 38
        for entry in report['preserved_fields']
    )
    assert not any(
        entry['axis'] == 'atom'
        and entry['field'] == 'formal_charge'
        and entry['index'] == 38
        for entry in report['assigned_fields']
    )
    assert msm.get(source, element='atom', selection=[38], formal_charge=True) == [0]


def test_selected_state_transfer_preserves_an_unselected_state(p59):
    source, options = p59
    source.chemical_states.append_state()
    before = snapshot(source)
    result = msm.physchem.apply_chemical_template(
        source, **options, chemical_state=0, template_chemical_state=0
    )
    after = snapshot(result['molecular_system'])
    assert (
        after['chemical_states']['states'][1] == before['chemical_states']['states'][1]
    )
    assert after['structure_chemical_state_indices'] == [0, 0]
    assert result['report']['source']['chemical_state_index'] == 0
    assert snapshot(source) == before


def test_template_application_cannot_bypass_vina_preparation_safeguard(p59):
    # Require the installed engine in this consumer gate; there is no absence skip.
    from vina import Vina

    assert Vina is not None
    source, options = p59
    result = msm.physchem.apply_chemical_template(source, **options)
    selected = msm.extract(result['molecular_system'], structure_indices=0)
    ligand = prepare_ligand(selected, selection='all')
    problem = DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=ligand,
        search_domain=BoxRegion.from_selection(
            selected, padding=puw.quantity(4, 'angstrom')
        ),
    )
    backend = VinaBackend()
    with pytest.raises(ArgumentError, match='heuristic AutoDock atom types'):
        backend.dock(problem, VinaProtocol(cpu=1, n_poses=1, exhaustiveness=1))
    exploratory = backend.dock(
        problem,
        VinaProtocol(
            cpu=1,
            n_poses=1,
            exhaustiveness=1,
            seed=123,
            allow_provisional_preparation=True,
        ),
    )
    assert exploratory.poses
    provenance = exploratory.provenance['preparation']['partner']
    assert provenance['assessment'] == 'provisional'
    assert (
        provenance['metadata']['source_chemistry']
        == ligand.metadata['source_chemistry']
    )
    restored = DockingResult.from_dict(json.loads(json.dumps(exploratory.to_dict())))
    assert restored.provenance['preparation']['partner'] == provenance
    assert 'template_provenance' not in provenance['metadata']
    # The application keeps its own template report alongside the docking record.
    saved = detached_record(result['report'])
    assert saved['schema'] == 'molsysmt.chemical_template@1'
    assert saved['template_provenance'] == options['template_provenance']
