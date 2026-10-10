"""Absent charges must not become prepared zeros, even with provisional opt-in."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT
from test_named_partial_charges import METHANOL

import dockingmt as dmt
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING
from dockingmt._private.smonitor import ArgumentError


def _typed_without_charges():
    return msm.build.assign_autodock_atom_types(
        msm.convert(METHANOL, to_form='molsysmt.MolSys'), **TYPING
    )


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_missing_charges_reject_without_unrequested_calculation(prepare, monkeypatch):
    source = _typed_without_charges()
    before = snapshot(source)
    mechanics = detached_record(source.molecular_mechanics.to_dict())

    def forbidden(*args, **kwargs):
        pytest.fail('No implicit hydrogen, charge or typing calculation is authorized.')

    for name in (
        'add_missing_hydrogens',
        'assign_partial_charges',
        'assign_autodock_atom_types',
    ):
        monkeypatch.setattr(msm.build, name, forbidden)
    with pytest.raises(
        ArgumentError, match='Atomic partial charges are required'
    ) as caught:
        prepare(source, selection='all')
    assert 'charge_options' in str(caught.value)
    assert 'msm.build.assign_partial_charges' in str(caught.value)
    assert snapshot(source) == before
    assert detached_record(source.molecular_mechanics.to_dict()) == mechanics


@pytest.mark.parametrize('role', ['receptor', 'partner'])
@pytest.mark.parametrize('allow_provisional', [False, True])
def test_automatic_vina_cannot_bypass_missing_charges(
    role, allow_provisional, monkeypatch
):
    import vina

    source = _typed_without_charges()
    inputs = {'receptor': MINIMAL_REC_PDBQT, 'partner': MINIMAL_LIG_PDBQT}
    inputs[role] = source
    problem = dmt.DockingProblem(
        **inputs,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([10, 10, 10], 'angstrom')
        ),
    )
    before = snapshot(source)

    def forbidden(*args, **kwargs):
        pytest.fail('Missing charges must fail before constructing the engine.')

    monkeypatch.setattr(vina, 'Vina', forbidden)
    with pytest.raises(ArgumentError, match='Atomic partial charges are required'):
        dmt.dock(
            problem,
            dmt.VinaProtocol(cpu=1, allow_provisional_preparation=allow_provisional),
        )
    assert snapshot(source) == before


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_explicit_supplied_zeros_remain_unattributed_and_are_not_placeholders(
    prepare, monkeypatch
):
    source = _typed_without_charges()
    # Deliberate synthetic input values; this is not a chemical charge model.
    msm.set(source, element='atom', partial_charge=puw.quantity([0.0] * 6, 'e'))
    mechanics = detached_record(source.molecular_mechanics.to_dict())

    def forbidden(*args, **kwargs):
        pytest.fail('Supplied values require no new model calculation.')

    monkeypatch.setattr(msm.build, 'assign_partial_charges', forbidden)
    with puw.context(standard_units=['pm', 'coulomb']):
        prepared = prepare(source, selection='all')
    assert prepared.charges == [0.0] * 3
    assert prepared.metadata['charge_source'] == 'source_partial_charge'
    assert prepared.metadata['partial_charge_assignment'] is None
    assert prepared.metadata['charge_projection'] is None
    assert dmt.assess_preparation(prepared)['provisional_reason_codes'] == []
    assert dmt.audit_preparation_charges(prepared)['assessment'] == 'unassessed'
    assert detached_record(source.molecular_mechanics.to_dict()) == mechanics


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_explicit_charge_then_typing_stage_matches_public_pipeline(
    prepare, monkeypatch
):
    source = msm.convert(METHANOL, to_form='molsysmt.MolSys')
    before = snapshot(source)
    options = deepcopy(CHARGE)
    expected = prepare(
        msm.build.assign_autodock_atom_types(
            msm.build.assign_partial_charges(source, **CHARGE), **TYPING
        ),
        selection='all',
    )
    charges = msm.build.assign_partial_charges
    types = msm.build.assign_autodock_atom_types
    calls = []

    def observed_charges(system, **kwargs):
        calls.append(('Q', kwargs))
        return charges(system, **kwargs)

    def observed_types(system, **kwargs):
        calls.append(('T', kwargs))
        return types(system, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail('Charge options do not authorize hydrogen addition or repair.')

    monkeypatch.setattr(msm.build, 'assign_partial_charges', observed_charges)
    monkeypatch.setattr(msm.build, 'assign_autodock_atom_types', observed_types)
    monkeypatch.setattr(msm.build, 'add_missing_hydrogens', forbidden)
    prepared = prepare(
        source, selection='all', charge_options=options, typing_options=TYPING
    )
    assert calls == [('Q', CHARGE), ('T', TYPING)]
    assert options == CHARGE
    assert prepared.charges == expected.charges
    # Calculation follows selected-input extraction in the explicit-stage route;
    # manual preassignment precedes it. Keep their different valid statuses.
    actual_report = prepared.metadata['partial_charge_assignment']
    expected_report = expected.metadata['partial_charge_assignment']
    assert actual_report['status'] == 'assigned'
    assert expected_report['status'] == 'projected'
    for key in (
        'method',
        'parameters',
        'software',
        'references',
        'atom_source_indices',
    ):
        assert actual_report[key] == expected_report[key]
    assert (
        prepared.metadata['charge_projection'] == expected.metadata['charge_projection']
    )
    assert prepared.metadata['preparation_workflow']['stages'] == [
        'partial_charge_assignment',
        'atom_type_assignment',
    ]
    assert prepared.metadata['preparation_workflow'][
        'prepared_to_input_atom_indices'
    ] == [0, 1, 5]
    assert snapshot(source) == before
    assert not msm.has_attribute(source, 'partial_charge')


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_charge_provider_failure_propagates_without_zero_fallback(prepare, monkeypatch):
    source = _typed_without_charges()
    before = snapshot(source)
    failure = msm.StructuralInconsistencyError('explicit charge provider failure')

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(msm.build, 'assign_partial_charges', fail)
    with pytest.raises(msm.StructuralInconsistencyError) as caught:
        prepare(source, selection='all', charge_options=CHARGE)
    assert caught.value is failure
    assert snapshot(source) == before


@pytest.mark.parametrize('value', [float('nan'), float('inf')])
@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_nonfinite_provider_values_cannot_reach_prepared_export(
    prepare, value, monkeypatch
):
    source = _typed_without_charges()
    values = [0.0] * 6
    values[1] = value
    # Public setters already reject nonfinite values. Exercise the consumer
    # boundary without mutating native internals to bypass those checks.
    msm.set(source, element='atom', partial_charge=puw.quantity([0.0] * 6, 'e'))
    get = msm.get

    def invalid_charge_values(system, **kwargs):
        if kwargs.get('partial_charge'):
            return np.asarray(values)
        return get(system, **kwargs)

    monkeypatch.setattr(msm, 'get', invalid_charge_values)
    with pytest.raises(ArgumentError, match='complete and finite'):
        prepare(source, selection='all')
    np.testing.assert_equal(get(source, element='atom', partial_charge=True), [0.0] * 6)


@pytest.mark.parametrize(
    'options', [{}, {'method': None}, {**CHARGE, 'return_report': True}]
)
def test_receptor_invalid_charge_request_fails_before_conversion(options, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('Invalid charge options must fail before converting the input.')

    monkeypatch.setattr(msm, 'convert', forbidden)
    with pytest.raises(ArgumentError):
        dmt.prepare_receptor('unused', selection='all', charge_options=options)
