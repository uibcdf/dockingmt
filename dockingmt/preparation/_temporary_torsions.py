"""Temporary molecular graph bridge for molsysmt#224.

Remove this module when MolSysMT supplies validated rotatable-bond and rigid-fragment
operations. DockingMT will retain only torsion selection and PDBQT projection.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from numbers import Integral, Number
from typing import Any

import molsysmt as msm

from dockingmt._private.smonitor import ArgumentError


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


def _component(
    start: int, neighbors: list[set[int]], excluded: set[tuple[int, int]]
) -> set[int]:
    visited = {start}
    pending = [start]
    while pending:
        atom = pending.pop()
        for neighbor in neighbors[atom]:
            if (
                tuple(sorted((atom, neighbor))) not in excluded
                and neighbor not in visited
            ):
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
    nonpolar hydrogen projection. This temporary graph operation belongs in MolSysMT
    (molsysmt#224); it deliberately makes no automatic torsion-policy claim.
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
    if not msm.has_attribute(source_molsys, 'bonded_atom_pairs'):
        raise ArgumentError(
            arg_name='molecular_system',
            reason='Explicit ligand bonds are required for active torsions.',
        )
    pairs = msm.get(
        source_molsys,
        element='bond',
        bonded_atom_pairs=True,
        chemical_state='structure',
        structure_indices=0,
    )
    orders = (
        msm.get(
            source_molsys,
            element='bond',
            bond_order=True,
            chemical_state='structure',
            structure_indices=0,
        )
        if msm.has_attribute(
            source_molsys, 'bond_order', chemical_state='structure', structure_indices=0
        )
        else None
    )
    if orders is not None and len(orders) != len(pairs):
        raise ArgumentError(
            arg_name='molecular_system', reason='Ligand bond pairs and orders disagree.'
        )
    source_edges = {}
    for index, (a, b) in enumerate(pairs):
        pair = tuple(sorted((int(a), int(b))))
        if (
            pair[0] < 0
            or pair[1] >= n_source
            or pair[0] == pair[1]
            or pair in source_edges
        ):
            raise ArgumentError(
                arg_name='molecular_system', reason='Ligand bond graph is invalid.'
            )
        source_edges[pair] = index
    retained_lookup = {source: index for index, source in enumerate(retained_indices)}
    neighbors = [set() for _ in retained_indices]
    for a, b in source_edges:
        if a in retained_lookup and b in retained_lookup:
            x, y = retained_lookup[a], retained_lookup[b]
            neighbors[x].add(y)
            neighbors[y].add(x)
    if len(_component(0, neighbors, set())) != len(retained_indices):
        raise ArgumentError(
            arg_name='molecular_system',
            reason='A flexible PDBQT ligand must have one connected retained graph.',
        )

    source_neighbors = [set() for _ in range(n_source)]
    for a, b in source_edges:
        source_neighbors[a].add(b)
        source_neighbors[b].add(a)
    selected: list[tuple[int, int]] = []
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
        bond_order = orders[source_edges[source_pair]] if orders is not None else None
        if not isinstance(bond_order, Number) or float(bond_order) != 1.0:
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'{source_pair} needs an explicit single bond order.',
            )
        a, b = source_pair
        if elements[a].upper() == 'H' or elements[b].upper() == 'H':
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'{source_pair} cannot rotate a hydrogen bond.',
            )
        if _is_amide_cn(a, b, elements, source_neighbors, source_edges, orders):
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'{source_pair} is an amide C-N bond.',
            )
        retained_pair = tuple(sorted((retained_lookup[a], retained_lookup[b])))
        side = _component(retained_pair[0], neighbors, {retained_pair})
        if retained_pair[1] in side:
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'{source_pair} belongs to a ring.',
            )
        other = set(range(len(retained_indices))) - side
        if any(
            sum(elements[retained_indices[index]].upper() != 'H' for index in group) < 2
            for group in (side, other)
        ):
            raise ArgumentError(
                arg_name='active_torsion_bonds',
                reason=f'{source_pair} has a terminal heavy-atom side.',
            )
        selected.append(source_pair)

    cut_edges = {
        tuple(sorted((retained_lookup[a], retained_lookup[b]))) for a, b in selected
    }
    components: list[tuple[int, ...]] = []
    atom_component = [-1] * len(retained_indices)
    for atom in range(len(retained_indices)):
        if atom_component[atom] >= 0:
            continue
        component = tuple(sorted(_component(atom, neighbors, cut_edges)))
        component_id = len(components)
        components.append(component)
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
        components[root], tree_branches, tuple(atom_order), tuple(selected)
    )


def _is_amide_cn(
    a: int,
    b: int,
    elements: Sequence[str],
    neighbors: list[set[int]],
    edges: dict[tuple[int, int], int],
    orders: Sequence[Any] | None,
) -> bool:
    if {elements[a].upper(), elements[b].upper()} != {'C', 'N'} or orders is None:
        return False
    carbon = a if elements[a].upper() == 'C' else b
    nitrogen = b if carbon == a else a
    return any(
        other != nitrogen
        and elements[other].upper() in {'O', 'S'}
        and isinstance(orders[edges[tuple(sorted((carbon, other)))]], Number)
        and float(orders[edges[tuple(sorted((carbon, other)))]]) == 2.0
        for other in neighbors[carbon]
    )
