"""Docking presentation and declared ROOT choices over public MolSysMT export."""

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._typing import type_remark
from dockingmt.preparation.charges import _charge_remark


def _native_input(prepared):
    """Supply this prepared object's actual values without changing its source."""
    coordinates = puw.quantity(
        puw.get_value(prepared.coordinates)[None], puw.get_unit(prepared.coordinates)
    )
    if prepared.source_molsys is None:
        from molsysmt.native import MolSys

        # A source-free prepared object declares only partial molecular data.
        # The provider decodes labels and constructs/sets its native domains;
        # no graph, bond order, H inventory or experimental identity is inferred.
        native = MolSys(n_atoms=prepared.n_atoms)
        elements = msm.element.atom.get_atom_type_from_atom_ff_type(
            prepared.atom_types, typing_scheme='autodock4'
        )
        msm.set(
            native,
            element='atom',
            atom_id=[str(i + 1) for i in range(prepared.n_atoms)],
            atom_name=prepared.atom_names,
            atom_type=elements,
            coordinates=coordinates,
            atom_ff_type=prepared.atom_types,
            partial_charge=puw.quantity(prepared.charges, 'elementary_charge'),
        )
        return native

    native = msm.copy(prepared.source_molsys)
    if msm.get(native, n_atoms=True) != prepared.n_atoms:
        raise ArgumentError(
            arg_name='source_molsys',
            reason='Prepared atom count differs from its molecular source.',
        )
    msm.set(native, element='atom', coordinates=coordinates)
    # Identical values retain the actual native original/derived reports.
    # Manual replacement goes through public setters, which own invalidation.
    values = msm.get(native, element='atom', partial_charge=True)
    if puw.is_quantity(values):
        values = puw.get_value(values, to_unit='elementary_charge')
    if not np.array_equal(values, prepared.charges):
        msm.set(
            native,
            element='atom',
            partial_charge=puw.quantity(prepared.charges, 'elementary_charge'),
        )
    labels = msm.get(native, element='atom', atom_ff_type=True)
    if labels is None or list(labels) != list(prepared.atom_types):
        msm.set(native, element='atom', atom_ff_type=prepared.atom_types)
    return native


def _declared_tree(prepared, native):
    """Express the existing explicit docking tree in the provider's schema."""
    tree = prepared._torsion_tree
    fragments = (
        [list(tree.root_atoms)] if tree is not None else [list(range(prepared.n_atoms))]
    )
    atom_pairs, fragment_pairs = [], []
    pending = [(0, branch) for branch in reversed(tree.branches)] if tree else []
    while pending:
        parent, branch = pending.pop()
        child = len(fragments)
        fragments.append(list(branch.atoms))
        atom_pairs.append([branch.parent_atom, branch.child_atom])
        fragment_pairs.append([parent, child])
        pending.extend((child, item) for item in reversed(branch.children))
    return {
        'schema_version': 'molsysmt.pdbqt-torsion-tree@1',
        'atom_ids': msm.get(native, element='atom', atom_id=True),
        'fragment_atom_indices': [atom for fragment in fragments for atom in fragment],
        'fragment_offsets': np.cumsum(
            [0] + [len(fragment) for fragment in fragments]
        ).tolist(),
        'branch_atom_pairs': np.asarray(atom_pairs, dtype=int).reshape(-1, 2),
        'branch_fragment_pairs': np.asarray(fragment_pairs, dtype=int).reshape(-1, 2),
        'root_fragment_index': 0,
        'torsdof': prepared.torsion_dof,
    }


def render_pdbqt(prepared, *, ligand):
    """Render the current prepared view without a local molecular serializer."""
    # Keep the established public prepared-name diagnostic. The provider also
    # validates all field widths and the complete representation before output.
    if any(not 1 <= len(name) <= 4 for name in prepared.atom_names):
        raise ArgumentError(
            arg_name='atom_names',
            reason='PDBQT atom names must contain one to four characters.',
        )
    remarks = _charge_remark(prepared) + type_remark(prepared)
    native = _native_input(prepared)
    text, exported = msm.convert(
        native,
        to_form='string:pdbqt_text',
        structure_indices=0,
        typing_scheme='autodock4',
        torsion_tree=_declared_tree(prepared, native) if ligand else None,
        output_presentation={
            'atom_serials': 'consecutive',
            'atom_names': prepared.atom_names,
            'group_names': prepared.group_names,
            'group_ids': [str(value) for value in prepared.group_ids],
            'chain_ids': 'A',
            'occupancy': 1.0,
            'b_factor': puw.quantity(0.0, 'angstrom**2'),
        },
        remarks=remarks,
        return_atom_map=True,
    )
    expected_order = getattr(prepared, 'pdbqt_atom_indices', range(prepared.n_atoms))
    if not np.array_equal(exported['output_to_source_atom_indices'], expected_order):
        raise ArgumentError(
            arg_name='prepared',
            reason='Native written order differs from the declared prepared atom order.',
        )
    return text.removeprefix('pdbqt_text:')
