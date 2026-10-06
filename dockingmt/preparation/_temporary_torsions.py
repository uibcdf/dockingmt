"""Explicit docking choices over public provider torsion/fragment operations.

MolSysMT classifies chemistry and partitions fragments. DockingMT records selected
cuts and explicit exceptions and orients ROOT/BRANCH. The retained-axis connectivity
guard remains pending molsysmt#348; PDBQT writing is separate (dockingmt#33).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from numbers import Integral
from typing import Any

import molsysmt as msm

from dockingmt._private.smonitor import ArgumentError
from dockingmt.preparation._molsys import detached_provider_report


@dataclass(frozen=True)
class Branch:
    parent_atom: int
    child_atom: int
    atoms: tuple[int, ...]
    children: tuple[Branch, ...]


@dataclass(frozen=True)
class TorsionTree:
    root_atoms: tuple[int, ...]
    branches: tuple[Branch, ...]
    atom_order: tuple[int, ...]
    active_bonds: tuple[tuple[int, int], ...]
    selection_report: dict[str, Any]


def _retained_component(start: int, neighbors: list[set[int]]) -> set[int]:
    # Temporary state-aware induced connectivity pending molsysmt#348.
    # Owner: DockingMT contributors; review 2027-01-06. Retire when the public
    # provider operation passes assigned-state and retained-subset controls.
    visited = {start}
    pending = [start]
    while pending:
        atom = pending.pop()
        for neighbor in neighbors[atom]:
            if neighbor not in visited:
                visited.add(neighbor)
                pending.append(neighbor)
    return visited


def build_torsion_tree(
    source_molsys: Any,
    retained_indices: Sequence[int],
    requested_bonds: Sequence[Sequence[int]],
    elements: Sequence[str],
) -> TorsionTree:
    """Validate explicit selected-ligand bonds and derive rigid fragments.

    Indices in requested_bonds refer to atoms of the selected MolSysMT ligand before
    nonpolar hydrogen projection. MolSysMT partitions the selected structure's
    complete graph; DockingMT projects memberships and orients the docking tree.
    Public provider exclusions inform the explicit docking policy. There is no
    automatic cut selection and no local chemical classification or fallback.
    """
    n_source = int(msm.get(source_molsys, element='system', n_atoms=True))
    if len(elements) != n_source or len(set(retained_indices)) != len(retained_indices):
        raise ArgumentError(
            arg_name='molecular_system', reason='Ligand atom mapping is invalid.'
        )
    if not retained_indices or any(i < 0 or i >= n_source for i in retained_indices):
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Retained ligand atom indices are invalid.',
        )
    classification = msm.topology.get_rotatable_bonds(
        source_molsys,
        method='conjugation_restricted',
        chemical_state='structure',
        structure_indices=0,
    )
    source_edges = {
        tuple(sorted((int(a), int(b)))): index
        for index, (a, b) in enumerate(classification['bonded_atom_pairs'])
    }
    bond_ids = detached_provider_report(
        {
            'values': msm.get(
                source_molsys,
                element='bond',
                bond_id=True,
                chemical_state='structure',
                structure_indices=0,
            )
        }
    )['values']
    atom_ids = detached_provider_report(
        {'values': msm.get(source_molsys, element='atom', atom_id=True)}
    )['values']
    retained_lookup = {source: index for index, source in enumerate(retained_indices)}
    neighbors = [set() for _ in retained_indices]
    for a, b in source_edges:
        if a in retained_lookup and b in retained_lookup:
            x, y = retained_lookup[a], retained_lookup[b]
            neighbors[x].add(y)
            neighbors[y].add(x)
    if len(_retained_component(0, neighbors)) != len(retained_indices):
        raise ArgumentError(
            arg_name='molecular_system',
            reason='A flexible PDBQT ligand must have one connected retained graph.',
        )

    selected: list[tuple[int, int]] = []
    decisions = []
    for pair in requested_bonds:
        if (
            not isinstance(pair, (list, tuple))
            or len(pair) != 2
            or any(isinstance(i, bool) or not isinstance(i, Integral) for i in pair)
        ):
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason='Each torsion must be a pair of selected-ligand atom indices.',
            )
        source_pair = tuple(sorted((int(pair[0]), int(pair[1]))))
        if source_pair[0] == source_pair[1] or source_pair not in source_edges:
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'{source_pair} is not a source ligand bond.',
            )
        if (
            source_pair[0] not in retained_lookup
            or source_pair[1] not in retained_lookup
        ):
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'{source_pair} does not survive hydrogen projection.',
            )
        if source_pair in selected:
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'Duplicate torsion bond {source_pair}.',
            )
        row = source_edges[source_pair]
        reasons = [
            name
            for name, bit in classification['exclusion_bits'].items()
            if int(classification['exclusion_mask'][row]) & bit
        ]
        _require_explicit_cut(source_pair, reasons, elements)
        decisions.append(
            {
                'source_atom_indices': list(source_pair),
                'source_bond_index': int(classification['bond_indices'][row]),
                'source_bond_id': bond_ids[int(classification['bond_indices'][row])],
                'source_atom_ids': [atom_ids[i] for i in source_pair],
                'decision': 'explicit_override' if reasons else 'provider_candidate',
                'provider_exclusion_reasons': reasons,
            }
        )
        selected.append(source_pair)

    fragments = msm.topology.get_rigid_fragments(
        source_molsys,
        bond_indices=[decision['source_bond_index'] for decision in decisions],
        chemical_state='structure',
        structure_indices=0,
    )
    packed = fragments['fragment_atom_indices']
    offsets = fragments['fragment_offsets']
    # Project memberships onto the declared retained axis, without copying the
    # molecular system or substituting positional order for source indices.
    projected = (
        tuple(
            sorted(
                retained_lookup[int(atom)]
                for atom in packed[start:stop]
                if int(atom) in retained_lookup
            )
        )
        for start, stop in zip(offsets[:-1], offsets[1:])
    )
    components = sorted(
        (group for group in projected if group), key=lambda group: group[0]
    )
    atom_component = [-1] * len(retained_indices)
    for component_id, component in enumerate(components):
        for member in component:
            atom_component[member] = component_id

    adjacency: list[list[tuple[int, int, int]]] = [[] for _ in components]
    for a, b in selected:
        x, y = retained_lookup[a], retained_lookup[b]
        cx, cy = atom_component[x], atom_component[y]
        adjacency[cx].append((cy, x, y))
        adjacency[cy].append((cx, y, x))
    root = min(
        range(len(components)), key=lambda i: (-len(components[i]), components[i][0])
    )
    atom_order: list[int] = list(components[root])

    def branches(parent_component: int, component: int) -> tuple[Branch, ...]:
        output = []
        for child_component, parent_atom, child_atom in sorted(
            adjacency[component], key=lambda edge: (edge[1], edge[2])
        ):
            if child_component == parent_component:
                continue
            atoms = (
                child_atom,
                *(i for i in components[child_component] if i != child_atom),
            )
            atom_order.extend(atoms)
            children = branches(component, child_component)
            output.append(Branch(parent_atom, child_atom, atoms, children))
        return tuple(output)

    tree_branches = branches(-1, root)
    if len(atom_order) != len(retained_indices) or len(set(atom_order)) != len(
        atom_order
    ):
        raise ArgumentError(
            arg_name='active_torsion_bonds',
            reason='Selected torsions did not form a valid rigid-fragment tree.',
        )
    return TorsionTree(
        components[root],
        tree_branches,
        tuple(atom_order),
        tuple(selected),
        {
            'schema': 'dockingmt.explicit_torsion_selection@1',
            'policy': 'explicit_docking_cuts@1',
            'selection': 'caller_supplied_bonds',
            'provider_classification': detached_provider_report(classification),
            'selected_bonds': decisions,
            'retained_source_atom_indices': list(retained_indices),
            'pdbqt_to_source_atom_indices': [retained_indices[i] for i in atom_order],
            'limits': 'Graph eligibility and explicit docking exceptions do not certify rotational barriers or scientific readiness.',
        },
    )


def _require_explicit_cut(pair, reasons, elements):
    """Choose allowed docking exceptions without reclassifying the chemistry."""
    messages = {
        'hydrogen_endpoint': 'cannot rotate a hydrogen bond',
        'not_single': 'needs an explicit single bond order',
        'ring_bond': 'belongs to a ring',
        'terminal_heavy_atom': 'has a terminal heavy-atom side',
    }
    for reason in reasons:
        if reason in messages:
            raise ArgumentError(
                arg_name='active_torsion_bonds', reason=f'{pair} {messages[reason]}.'
            )
    if 'restricted_conjugation' in reasons and 'N' in (
        elements[pair[0]].upper(),
        elements[pair[1]].upper(),
    ):
        raise ArgumentError(
            arg_name='active_torsion_bonds',
            reason=f'{pair} is an amide C-N or other restricted C-N bond.',
        )
    if set(reasons) - {'restricted_conjugation', 'adjacent_triple_bond'}:
        raise ArgumentError(
            arg_name='active_torsion_bonds',
            reason=f'{pair} has unsupported provider exclusions: {reasons}.',
        )
