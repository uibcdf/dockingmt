"""Production prepared export delegates molecular construction and writing."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from test_flexible_reconstruction import _manual
from test_molecular_delegation import _manual_prepared

import dockingmt as dmt
from devtools.qualify_chemical_templates import detached_record, snapshot
from devtools.qualify_named_types import CHARGE, TYPING, explicit_source
from dockingmt.preparation._molsys import autodock_element


@pytest.mark.parametrize('kind', ['ligand', 'receptor'])
@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_source_free_writer_uses_public_decoder_and_native_export(
    kind, length_unit, monkeypatch
):
    prepared = _manual_prepared(kind)
    before = deepcopy(prepared.to_dict())
    convert = msm.convert
    decode = msm.element.atom.get_atom_type_from_atom_ff_type
    exports, decoded = [], []

    def observed_decode(labels, **kwargs):
        decoded.append((list(labels), kwargs))
        return decode(labels, **kwargs)

    def observed_convert(item, **kwargs):
        assert not isinstance(item, str), 'No writer/reader bootstrap is authorized.'
        exports.append((item, kwargs))
        return convert(item, **kwargs)

    monkeypatch.setattr(
        msm.element.atom, 'get_atom_type_from_atom_ff_type', observed_decode
    )
    monkeypatch.setattr(msm, 'convert', observed_convert)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        payload = prepared.to_pdbqt()
        assert puw.configure.report() == policy
    assert len(exports) == 1 and len(decoded) == 1
    assert decoded[0] == (prepared.atom_types, {'typing_scheme': 'autodock4'})
    native, options = exports[0]
    assert options['to_form'] == 'string:pdbqt_text'
    assert options['output_presentation']['atom_serials'] == 'consecutive'
    assert options['output_presentation']['group_names'] == prepared.group_names
    assert list(msm.get(native, element='atom', atom_type=True)) == ['C', 'C', 'O']
    atoms = [line for line in payload.splitlines() if line.startswith('ATOM')]
    assert [line[12:16].strip() for line in atoms] == prepared.atom_names
    assert [line[77:].strip() for line in atoms] == prepared.atom_types
    np.testing.assert_allclose(
        [[float(line[i : i + 8]) for i in (30, 38, 46)] for line in atoms],
        puw.get_value(prepared.coordinates, to_unit='angstrom'),
        rtol=0,
        atol=0.000501,
    )
    assert prepared.to_dict() == before and prepared.source_molsys is None


@pytest.mark.parametrize('nested', [False, True])
def test_source_free_flexible_tree_reaches_native_writer(nested, monkeypatch):
    prepared = _manual(nested)
    convert = msm.convert
    calls = []

    def recorded(item, **kwargs):
        calls.append(kwargs)
        return convert(item, **kwargs)

    monkeypatch.setattr(msm, 'convert', recorded)
    payload = prepared.to_pdbqt()
    assert len(calls) == 1
    tree = calls[0]['torsion_tree']
    assert tree['schema_version'] == 'molsysmt.pdbqt-torsion-tree@1'
    assert tree['torsdof'] == prepared.torsion_dof
    assert list(tree['fragment_atom_indices']) == prepared.pdbqt_atom_indices
    assert (
        sum(line.startswith('BRANCH ') for line in payload.splitlines())
        == prepared.torsion_dof
    )
    restored = prepared.to_molecular_system()
    assert (
        list(msm.get(restored, element='atom', atom_name=True)) == prepared.atom_names
    )
    assert not msm.has_attribute(restored, 'bond_order')


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_source_backed_writer_preserves_native_identity_and_derived_evidence(
    prepare, monkeypatch
):
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source('CO'), **CHARGE), **TYPING
    )
    prepared = prepare(source, selection='all')
    native = prepared.source_molsys
    before = snapshot(native)
    original = detached_record(native.molecular_mechanics.to_dict())
    convert = msm.convert
    seen = []

    def observed(item, **kwargs):
        if kwargs.get('to_form') != 'string:pdbqt_text':
            return convert(item, **kwargs)
        seen.append(
            (
                list(msm.get(item, element='atom', atom_id=True)),
                detached_record(item.molecular_mechanics.partial_charge_assignment),
                detached_record(item.molecular_mechanics.atom_type_assignment),
            )
        )
        return convert(item, **kwargs)

    monkeypatch.setattr(msm, 'convert', observed)
    payload = prepared.to_pdbqt()
    assert len(seen) == 1
    assert seen[0][0] == list(msm.get(native, element='atom', atom_id=True))
    assert seen[0][1]['status'] == seen[0][2]['status'] == 'derived'
    assert 'REMARK MOLSYSMT_PARTIAL_CHARGES ' in payload
    assert 'REMARK DOCKINGMT_PARTIAL_CHARGES ' in payload
    assert 'REMARK MOLSYSMT_ATOM_TYPES ' in payload
    assert 'REMARK DOCKINGMT_ATOM_TYPES ' in payload
    assert snapshot(native) == before
    assert detached_record(native.molecular_mechanics.to_dict()) == original


@pytest.mark.parametrize('kind', ['ligand', 'receptor'])
def test_writer_provider_failure_propagates_without_fallback(kind, monkeypatch):
    prepared = _manual_prepared(kind)
    error = RuntimeError('controlled public writer refusal')

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm, 'convert', fail)
    with pytest.raises(RuntimeError) as caught:
        prepared.to_pdbqt()
    assert caught.value is error


def test_existing_element_adapter_delegates_named_dictionary(monkeypatch):
    calls = []

    def decoded(label, **kwargs):
        calls.append((label, kwargs))
        return 'C'

    monkeypatch.setattr(msm.element.atom, 'get_atom_type_from_atom_ff_type', decoded)
    assert autodock_element('A') == 'C'
    assert calls == [('A', {'typing_scheme': 'autodock4'})]


@pytest.mark.parametrize('prepare', [dmt.prepare_ligand, dmt.prepare_receptor])
def test_explicit_manual_values_replace_only_the_export_copy(prepare, monkeypatch):
    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source('CO'), **CHARGE), **TYPING
    )
    prepared = prepare(source, selection='all')
    # An explicitly manual view has no claimed consumer assignment. The native
    # setters own clearing provenance for replaced mechanical values.
    prepared.metadata = {}
    prepared.charges[0] += 0.125
    prepared.coordinates = prepared.coordinates + puw.quantity(1.234567, 'angstrom')
    before = snapshot(prepared.source_molsys)
    assignment = detached_record(
        prepared.source_molsys.molecular_mechanics.partial_charge_assignment
    )
    convert = msm.convert
    seen = []

    def recorded(item, **kwargs):
        if kwargs.get('to_form') == 'string:pdbqt_text':
            seen.append(item)
        return convert(item, **kwargs)

    monkeypatch.setattr(msm, 'convert', recorded)
    text = prepared.to_pdbqt()
    assert len(seen) == 1
    assert seen[0].molecular_mechanics.partial_charge_assignment is None
    assert 'REMARK MOLSYSMT_PARTIAL_CHARGES ' not in text
    assert 'REMARK DOCKINGMT_PARTIAL_CHARGES ' not in text
    assert snapshot(prepared.source_molsys) == before
    assert (
        detached_record(
            prepared.source_molsys.molecular_mechanics.partial_charge_assignment
        )
        == assignment
    )
    atoms = [line for line in text.splitlines() if line.startswith('ATOM')]
    assert [float(line[68:76]) for line in atoms] == [
        float(f'{charge:.3f}') for charge in prepared.charges
    ]


def test_known_disconnected_rigid_ligand_refuses_before_engine(monkeypatch):
    from molsysmt._private.smonitor import FormatError
    from test_engines import MINIMAL_REC_PDBQT

    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source('CC(=O)N'), **CHARGE),
        **TYPING,
    )
    selected = msm.extract(source, selection=[3, 0])
    prepared = dmt.prepare_ligand(selected, selection='all')
    before = snapshot(prepared.source_molsys)

    def forbid(*args, **kwargs):
        raise AssertionError('Unsupported known graph must reject before Vina.')

    monkeypatch.setattr('vina.Vina', forbid)
    problem = dmt.DockingProblem(
        receptor='pdbqt_text:' + MINIMAL_REC_PDBQT,
        partner=prepared,
        search_domain=dmt.BoxRegion(
            puw.quantity([0, 0, 0], 'angstrom'), puw.quantity([16, 16, 16], 'angstrom')
        ),
    )
    with pytest.raises(FormatError, match='fragments must agree'):
        dmt.dock(problem, protocol=dmt.VinaProtocol(cpu=1))
    assert prepared.atom_types == ['C', 'N']
    assert snapshot(prepared.source_molsys) == before


def test_actual_export_map_must_match_the_declared_prepared_order():
    from dataclasses import replace

    from dockingmt._private.smonitor import ArgumentError

    prepared = _manual()
    prepared._torsion_tree = replace(
        prepared._torsion_tree, atom_order=tuple(reversed(prepared.pdbqt_atom_indices))
    )
    with pytest.raises(ArgumentError, match='Native written order differs'):
        prepared.to_pdbqt()


def test_readonly_export_ignores_unrelated_copy_resource_but_edits_require_copy():
    from test_molecular_variant_ownership import UnavailableResource

    source = msm.build.assign_autodock_atom_types(
        msm.build.assign_partial_charges(explicit_source('CO'), **CHARGE), **TYPING
    )
    prepared = dmt.prepare_ligand(source, selection='all')
    before = snapshot(prepared.source_molsys)
    prepared.source_molsys.unavailable_resource = UnavailableResource()
    assert 'ATOM' in prepared.to_pdbqt()
    assert snapshot(prepared.source_molsys) == before
    prepared.coordinates = prepared.coordinates + puw.quantity(1, 'angstrom')
    with pytest.raises(RuntimeError, match='test resource cannot be copied'):
        prepared.to_pdbqt()
    assert snapshot(prepared.source_molsys) == before
