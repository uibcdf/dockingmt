"""Receive chemical state prerequisites and remapping through real consumer paths."""

import json

import molsysmt as msm
import numpy as np
import pytest
import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError

import dockingmt as dmt
from devtools.qualify_named_types import declared_source
from dockingmt.preparation._temporary_torsions import build_torsion_tree


def _record(source):
    return json.dumps(
        msm.convert(source, to_form='molsysmt.MolSysDict').to_dict(),
        sort_keys=True,
        allow_nan=False,
    )


@pytest.mark.parametrize(
    'kind', ['absent', 'zero', 'unavailable', 'partial', 'missing']
)
def test_torsion_prerequisites_preserve_missing_or_unknown_chemistry(kind):
    source = declared_source('CCCCCC')
    if kind == 'absent':
        source = msm.convert(
            [source.topology, source.structures], to_form='molsysmt.MolSys'
        )
    elif kind == 'zero':
        source = msm.convert(
            [source.topology, msm.ChemicalStates(n_atoms=6), source.structures],
            to_form='molsysmt.MolSys',
        )
    elif kind in ('unavailable', 'partial'):
        # Deliberately declared incomplete input, not a production repair.
        source.chemical_states._states[0].connectivity_completeness = kind
    else:
        source.chemical_states.append_state()
    before = _record(source)
    message = 'complete' if kind in ('unavailable', 'partial') else 'association'
    with pytest.raises(StructuralInconsistencyError, match=message):
        build_torsion_tree(source, list(range(6)), [(1, 2)], ['C'] * 6)
    assert _record(source) == before
    if kind == 'absent':
        assert source.chemical_states is None
    elif kind == 'zero':
        assert source.chemical_states.n_chemical_states == 0


def test_structure_assigned_state_does_not_require_a_reference_default():
    source = declared_source('CCCCCC')
    assigned = source.chemical_states.append_state()
    source.chemical_states._set_chemical_state_bonds(
        source.chemical_states.get_bonds().copy(), state_index=assigned
    )
    source.chemical_states._states[assigned].connectivity_completeness = 'complete'
    source.chemical_states._set_reference_index(None)
    source._set_structure_chemical_state_indices([assigned])
    before = _record(source)
    with pytest.raises(StructuralInconsistencyError):
        msm.chemical_states.get_rotatable_bonds(source, chemical_state='reference')
    tree = build_torsion_tree(source, list(range(6)), [(1, 2)], ['C'] * 6)
    assert tree.active_bonds == ((1, 2),)
    assert tree.selection_report['provider_classification']['chemical_state_index'] == 1
    assert _record(source) == before


def test_complete_zero_bond_graph_is_an_admitted_rigid_fragment():
    source = declared_source('C')
    before = _record(source)
    tree = build_torsion_tree(source, [0], [], ['C'])
    assert tree.root_atoms == tree.atom_order == (0,)
    assert tree.branches == tree.active_bonds == ()
    assert _record(source) == before


@pytest.mark.parametrize('route', ['copy', 'dictionary', 'h5msm'])
@pytest.mark.parametrize('length_unit', ['angstrom', 'pm'])
def test_problem_retains_assigned_state_and_nonconsecutive_axes_after_transport(
    route, length_unit, tmp_path
):
    source = declared_source('CCCCCC')
    assigned = source.chemical_states.append_state()
    source.chemical_states._states[assigned].state_id = 'assigned-split'
    source.chemical_states._set_chemical_state_bonds(
        source.chemical_states.get_bonds().copy(), state_index=assigned
    )
    source.chemical_states._states[assigned].connectivity_completeness = 'complete'
    source.chemical_states.remove_bonds(2, chemical_state=assigned)
    source._set_structure_chemical_state_indices([assigned])
    ids = ['10', '30', '50', '70', '90', '110']
    msm.set(source, element='atom', atom_id=ids)
    before = _record(source)
    with puw.context(standard_units=[length_unit, 'fs', 'coulomb', 'kJ/mol']):
        policy = puw.configure.report()
        if route == 'copy':
            restored = msm.copy(source)
        elif route == 'dictionary':
            restored = msm.convert(
                msm.convert(source, to_form='molsysmt.MolSysDict'),
                to_form='molsysmt.MolSys',
            )
        else:
            path = str(tmp_path / 'chemical-states.h5msm')
            msm.convert(source, to_form=path)
            restored = msm.convert(path, to_form='molsysmt.MolSys')
        assert _record(restored) == before
        problem = dmt.DockingProblem(
            receptor=restored,
            partner=restored,
            receptor_selection=[0, 2, 5],
            partner_selection=[1, 3, 4],
            search_domain=dmt.BoxRegion(
                center=puw.quantity([0, 0, 0], 'angstrom'),
                size=puw.quantity([20, 20, 20], 'angstrom'),
            ),
        )
        assert problem.receptor_atom_indices == [0, 2, 5]
        assert problem.partner_atom_indices == [1, 3, 4]
        assert problem.partner_chemical_state_index == assigned
        assert problem.to_dict()['molecular_inputs']['partner'][
            'chemical_state_id'
        ] == ('assigned-split')
        selected = problem.partner_molsys
        assert list(msm.get(selected, element='atom', atom_id=True)) == [
            ids[i] for i in [1, 3, 4]
        ]
        np.testing.assert_allclose(
            puw.get_value(msm.get(selected, coordinates=True), to_unit='angstrom'),
            puw.get_value(msm.get(source, coordinates=True), to_unit='angstrom')[
                :, [1, 3, 4]
            ],
        )
        # Mutating a provider copy must not edit either the original or the
        # already extracted DockingMT input. Chemistry remains provider-owned.
        selected_before = _record(selected)
        restored.chemical_states.add_bonds([[2, 3]], chemical_state=assigned)
        assert _record(source) == before
        assert _record(selected) == selected_before
        assert _record(restored) != before
        assert puw.configure.report() == policy
