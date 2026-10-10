"""Named provider labels retain chemical context through consumer projection."""

import base64
import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_REC_PDBQT

import dockingmt as dmt
from devtools.qualify_chemical_templates import (
    load_5x72,
    load_181l_benzene,
    snapshot,
    template_options,
)
from devtools.qualify_named_types import (
    CHARGE,
    HYDROGEN,
    TYPING,
    declared_source,
    explicit_source,
)
from dockingmt._private.smonitor import ArgumentError


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
@pytest.mark.parametrize(
    'smiles,heavy',
    [
        ('CN', ['C', 'NA']),
        ('C[NH3+]', ['C', 'N']),
        ('CC(=O)N', ['C', 'C', 'OA', 'N']),
        ('c1ccncc1', ['A', 'A', 'A', 'NA', 'A', 'A']),
        ('c1cc[nH]c1', ['A', 'A', 'A', 'N', 'A']),
        ('CSC', ['C', 'SA', 'C']),
        ('CS(=O)(=O)C', ['C', 'S', 'OA', 'OA', 'C']),
    ],
)
def test_named_chemical_context_overrides_heuristics_without_changing_input(
    prepare, smiles, heavy
):
    source = explicit_source(smiles)
    before = snapshot(source)
    options = deepcopy(TYPING)
    prepared = prepare(source, selection='all', typing_options=options)
    assert prepared.atom_types[: len(heavy)] == heavy
    assert all(label == 'HD' for label in prepared.atom_types[len(heavy) :])
    assert options == TYPING
    assert snapshot(source) == before
    assert not msm.has_attribute(source, 'atom_ff_type')
    report = prepared.metadata['atom_type_assignment']
    assert report['typing_scheme'] == 'autodock4'
    assert report['rule_version'] == 'chemical_environment@1'
    assert report['n_atoms'] == msm.get(source, n_atoms=True)
    assert report['coverage'] == 'complete'
    assert report['software']['rdkit'] and report['attribution']['items']
    assert prepared.metadata['atom_type_source'] == 'molsysmt_named_autodock4'
    # A named type model does not hide the still absent charge model.
    assert dmt.assess_preparation(prepared)['provisional_reason_codes'] == [
        'zero_placeholder_charges'
    ]


@pytest.mark.parametrize('smiles,heavy', [('F', 'F'), ('P', 'P')])
@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_provider_polar_h_classification_is_preserved_for_f_and_p(
    prepare, smiles, heavy
):
    source = explicit_source(smiles)
    prepared = prepare(source, selection='all', typing_options=TYPING)
    assert prepared.n_atoms == msm.get(source, n_atoms=True)
    assert prepared.atom_types == [heavy] + ['HD'] * (prepared.n_atoms - 1)
    assert prepared.metadata['omitted_hydrogen_indices'] == []


def test_h_charge_type_stage_order_and_generated_h_correspondence():
    source = declared_source('CO')
    before = snapshot(source)
    prepared = dmt.prepare_ligand(
        source,
        selection='all',
        hydrogen_options=HYDROGEN,
        charge_options=CHARGE,
        typing_options=TYPING,
    )
    workflow = prepared.metadata['preparation_workflow']
    assert workflow['stages'] == [
        'hydrogen_addition',
        'partial_charge_assignment',
        'atom_type_assignment',
    ]
    assert workflow['type_assignment_record'] == 'metadata.atom_type_assignment'
    assert workflow['prepared_to_input_atom_indices'] == [0, 1, None]
    assert prepared.atom_types == ['C', 'OA', 'HD']
    assert prepared.metadata['atom_type_projection'][
        'retained_selected_atom_indices'
    ] == [0, 1, 5]
    assert prepared.metadata['atom_type_projection'][
        'retained_source_atom_indices'
    ] == [0, 1, 5]
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'
    assert dmt.assess_preparation(prepared)['assessment'] == 'unassessed'
    assert snapshot(source) == before


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_preassigned_projected_parent_labels_are_not_reclassified(prepare, monkeypatch):
    assigned = msm.build.assign_autodock_atom_types(
        explicit_source('CC(=O)N'), **TYPING
    )
    original = deepcopy(assigned.molecular_mechanics.atom_type_assignment)
    selected = msm.extract(assigned, selection=[3, 0])

    def forbid(*args, **kwargs):
        raise AssertionError('No new chemical classification is requested.')

    monkeypatch.setattr(msm.build, 'assign_autodock_atom_types', forbid)
    monkeypatch.setattr(msm.physchem, 'get_autodock_atom_types', forbid)
    prepared = prepare(selected, selection='all')
    assert prepared.atom_types == ['C', 'N']  # Parent amide N stays N on the fragment.
    report = prepared.metadata['atom_type_assignment']
    assert report['status'] == 'projected'
    assert report['atom_source_indices'] == [0, 3]
    assert report['evaluated_atom_indices'] == list(
        range(msm.get(assigned, n_atoms=True))
    )
    assert report['software'] == original['software']
    assert prepared.metadata['atom_type_projection'][
        'retained_source_atom_indices'
    ] == [0, 3]
    assert 'REMARK DOCKINGMT_ATOM_TYPES' in prepared.to_pdbqt()


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
@pytest.mark.parametrize('mutation', ['labels', 'chemistry'])
def test_stale_provider_binding_is_rejected(prepare, mutation):
    assigned = msm.build.assign_autodock_atom_types(explicit_source('CO'), **TYPING)
    # Bypass public setters deliberately to test provider binding detection.
    if mutation == 'labels':
        assigned.molecular_mechanics.atoms_ff.loc[0, 'atom_ff_type'] = 'A'
    else:
        assigned.topology.atoms.loc[0, 'atom_type'] = 'N'
    with pytest.raises(ArgumentError, match='stale'):
        prepare(assigned, selection='all')


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_manual_type_replacement_does_not_inherit_named_provenance(
    prepare, monkeypatch
):
    source = msm.build.assign_autodock_atom_types(explicit_source('CN'), **TYPING)
    source.molecular_mechanics.atom_ff_type = ['C'] * msm.get(source, n_atoms=True)

    def forbid(*args, **kwargs):
        raise AssertionError('No implicit typing is authorized.')

    monkeypatch.setattr(msm.build, 'assign_autodock_atom_types', forbid)
    with pytest.raises(
        ArgumentError, match='Named MolSysMT AutoDock4 types are required'
    ):
        prepare(source, selection='all')


@pytest.mark.parametrize(
    'options',
    [
        True,
        [],
        {},
        {'typing_scheme': 'other', 'method': 'chemical_environment'},
        {'typing_scheme': 'autodock4'},
        {**TYPING, 'return_report': False},
        {**TYPING, 'skip_digestion': True},
        {**TYPING, 'molecular_system': 'other'},
    ],
)
@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_invalid_options_fail_before_molecular_conversion(
    prepare, options, monkeypatch
):
    def forbid(*args, **kwargs):
        raise AssertionError('Invalid options must fail before conversion.')

    monkeypatch.setattr(msm, 'convert', forbid)
    with pytest.raises(ArgumentError):
        prepare('unused', selection='all', typing_options=options)


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_requested_provider_failure_propagates_without_heuristic_fallback(
    prepare, monkeypatch
):
    source = explicit_source('CO')
    error = msm.StructuralInconsistencyError('typing provider failure')

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm.build, 'assign_autodock_atom_types', fail)
    with pytest.raises(msm.StructuralInconsistencyError) as caught:
        prepare(source, selection='all', typing_options=TYPING)
    assert caught.value is error


def test_virtual_h_is_rejected_without_implicitly_adding_atoms():
    source = declared_source('CO')
    before = snapshot(source)
    with pytest.raises(msm.StructuralInconsistencyError, match='indexed'):
        dmt.prepare_ligand(source, selection='all', typing_options=TYPING)
    assert snapshot(source) == before


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_changed_prepared_labels_cannot_be_exported_as_named(prepare):
    prepared = prepare(explicit_source('CN'), selection='all', typing_options=TYPING)
    prepared.atom_types[1] = 'N'
    with pytest.raises(ArgumentError, match='no longer match'):
        prepared.to_pdbqt()


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
@pytest.mark.parametrize(
    'record,key,value',
    [
        ('atom_type_assignment', 'n_atoms', None),
        ('atom_type_assignment', 'software', {'invalid': float('nan')}),
        ('atom_type_projection', 'retained_selected_atom_indices', [100, 1, 5]),
        ('atom_type_projection', 'retained_source_atom_indices', [1, 0, 5]),
        ('atom_type_projection', 'pdbqt_atom_indices', [1, 0, 2]),
        ('atom_type_projection', 'pdbqt_to_source_atom_indices', [1, 0, 5]),
    ],
)
def test_changed_named_correspondence_or_malformed_evidence_is_rejected(
    prepare, record, key, value
):
    prepared = prepare(explicit_source('CO'), selection='all', typing_options=TYPING)
    prepared.metadata[record][key] = value
    with pytest.raises(ArgumentError):
        prepared.to_pdbqt()


def test_nondefault_units_and_input_pose_are_preserved():
    source = explicit_source('CO')
    before = puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom').copy()
    with puw.context(standard_units=['pm', 'coulomb']):
        charged = msm.build.assign_partial_charges(source, **CHARGE)
        prepared = dmt.prepare_ligand(charged, selection='all', typing_options=TYPING)
        assert prepared.charges == pytest.approx(
            [0.19000057917, -0.39963024356, 0.20962966439], abs=1e-10
        )
        np.testing.assert_allclose(
            puw.get_value(prepared.coordinates, to_unit='angstrom'),
            before[0, [0, 1, 5]],
            rtol=0,
            atol=1e-12,
        )
        assert prepared.atom_types == ['C', 'OA', 'HD']
        assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'


def test_original_bnz_template_h_charge_type_route_is_named():
    source, template, _ = load_181l_benzene()
    options = template_options(
        template,
        np.column_stack((np.arange(6), np.arange(6))),
        identity='Declared benzene',
        uri='smiles:c1ccccc1',
        hydrogen_policy='stored_counts',
    )
    applied = msm.physchem.apply_chemical_template(source, **options)[
        'molecular_system'
    ]
    before = snapshot(applied)
    prepared = dmt.prepare_ligand(
        applied,
        selection='all',
        hydrogen_options={**HYDROGEN, 'attribute_policy': 'intersection'},
        charge_options=CHARGE,
        typing_options=TYPING,
    )
    assert prepared.atom_types == ['A'] * 6
    assert prepared.metadata['atom_type_assignment']['n_atoms'] == 12
    assert prepared.metadata['preparation_workflow'][
        'pdbqt_to_input_atom_indices'
    ] == list(range(6))
    assert dmt.assess_preparation(prepared)['provisional_reason_codes'] == []
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'
    assert snapshot(applied) == before


def test_flexible_output_keeps_named_labels_on_verified_written_axis():
    _, source = load_5x72('p59')
    charged = msm.build.assign_partial_charges(source, **CHARGE)
    prepared = dmt.prepare_ligand(
        charged,
        selection='all',
        active_torsion_bonds=[(6, 7), (17, 18)],
        typing_options=TYPING,
    )
    written = [
        line.split()[-1]
        for line in prepared.to_pdbqt().splitlines()
        if line.startswith('ATOM')
    ]
    assert written == [prepared.atom_types[i] for i in prepared.pdbqt_atom_indices]
    assert prepared.pdbqt_atom_indices != list(range(prepared.n_atoms))
    projection = prepared.metadata['atom_type_projection']
    assert projection['pdbqt_to_source_atom_indices'] == [
        projection['retained_source_atom_indices'][i]
        for i in prepared.pdbqt_atom_indices
    ]
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'consistent'
    from vina import Vina

    Vina(cpu=1, verbosity=0).set_ligand_from_string(prepared.to_pdbqt())


def test_default_real_vina_run_retains_named_types_in_saved_result():
    prepared = dmt.prepare_ligand(
        declared_source('CO'),
        selection='all',
        hydrogen_options=HYDROGEN,
        charge_options=CHARGE,
        typing_options=TYPING,
    )
    problem = dmt.DockingProblem(
        receptor=MINIMAL_REC_PDBQT,
        partner=prepared,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
    )
    result = dmt.dock(
        problem,
        dmt.VinaProtocol(
            cpu=1, seed=17, n_poses=1, exhaustiveness=1, capture_backend_inputs=True
        ),
    )
    restored = dmt.DockingResult.from_dict(
        json.loads(json.dumps(result.to_dict(), allow_nan=False))
    )
    provenance = restored.provenance['preparation']['partner']
    assert len(restored.poses) == 1
    assert provenance['assessment'] == 'unassessed'
    assert (
        provenance['metadata']['atom_type_assignment']
        == prepared.metadata['atom_type_assignment']
    )
    assert (
        provenance['metadata']['atom_type_projection']
        == prepared.metadata['atom_type_projection']
    )
    captured = base64.b64decode(
        result.provenance['backend_artifacts']['partner']['content_base64']
    )
    assert b'REMARK DOCKINGMT_ATOM_TYPES' in captured
