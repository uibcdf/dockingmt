"""Molecular preparation requires explicit provider typing; no heuristic escape."""

from copy import deepcopy

import molsysmt as msm
import pytest
import pyunitwizard as puw
from test_engines import MINIMAL_LIG_PDBQT, MINIMAL_REC_PDBQT

import dockingmt as dmt
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING, explicit_source
from dockingmt._private.smonitor import ArgumentError


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
@pytest.mark.parametrize('input_kind', ['untyped', 'charged', 'bare_column'])
def test_missing_named_types_fail_without_implicit_molecular_work(
    prepare, input_kind, monkeypatch
):
    source = explicit_source('CN')
    if input_kind == 'charged':
        source = msm.build.assign_partial_charges(source, **CHARGE)
    elif input_kind == 'bare_column':
        msm.set(
            source.molecular_mechanics,
            element='atom',
            atom_ff_type=['C'] * msm.get(source, n_atoms=True),
        )
    before = snapshot(source)
    mechanics_before = deepcopy(source.molecular_mechanics.to_dict())

    def forbidden(*args, **kwargs):
        pytest.fail('No unrequested H, charge or typing model is authorized.')

    for name in (
        'add_missing_hydrogens',
        'assign_partial_charges',
        'assign_autodock_atom_types',
    ):
        monkeypatch.setattr(msm.build, name, forbidden)
    with pytest.raises(
        ArgumentError, match='Named MolSysMT AutoDock4 types are required'
    ) as caught:
        prepare(source, selection='all')
    assert 'typing_options' in str(caught.value)
    assert 'msm.build.assign_autodock_atom_types' in str(caught.value)
    assert snapshot(source) == before
    # Native report arrays are compared through their detached public dictionary.
    assert detached_record(source.molecular_mechanics.to_dict()) == detached_record(
        mechanics_before
    )


@pytest.mark.parametrize('role', ['receptor', 'partner'])
@pytest.mark.parametrize('allow_provisional', [False, True])
def test_automatic_vina_cannot_bypass_missing_types(
    role, allow_provisional, monkeypatch
):
    import vina

    source = explicit_source('CN')
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
        pytest.fail('Missing named types must fail before engine construction.')

    monkeypatch.setattr(vina, 'Vina', forbidden)
    with pytest.raises(
        ArgumentError, match='Named MolSysMT AutoDock4 types are required'
    ):
        dmt.dock(
            problem,
            dmt.VinaProtocol(cpu=1, allow_provisional_preparation=allow_provisional),
        )
    assert snapshot(source) == before


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_explicit_provider_choice_succeeds_without_charge_or_h_calculation(
    prepare, monkeypatch
):
    source = explicit_source('CN')
    before = snapshot(source)
    options = deepcopy(TYPING)
    calls = []
    assign = msm.build.assign_autodock_atom_types

    def observed(system, **kwargs):
        calls.append(kwargs)
        return assign(system, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail('Typing options do not authorize H or charge calculation.')

    monkeypatch.setattr(msm.build, 'assign_autodock_atom_types', observed)
    monkeypatch.setattr(msm.build, 'add_missing_hydrogens', forbidden)
    monkeypatch.setattr(msm.build, 'assign_partial_charges', forbidden)
    prepared = prepare(source, selection='all', typing_options=options)
    assert calls == [TYPING]
    assert options == TYPING
    assert prepared.atom_types == ['C', 'NA', 'HD', 'HD']
    assert prepared.metadata['atom_type_source'] == 'molsysmt_named_autodock4'
    assert prepared.metadata['charge_source'] == 'zero_placeholder'
    assert dmt.assess_preparation(prepared)['provisional_reason_codes'] == [
        'zero_placeholder_charges'
    ]
    assert snapshot(source) == before
