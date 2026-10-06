"""Record named type consumption and protect its prepared/written atom axes.

Chemical classification and native graph binding are MolSysMT operations. This
module binds only the consumer's saved ordered labels after H projection.
"""

import json

from dockingmt._private.smonitor import ArgumentError


def type_projection(assignment, retained, labels, written_order=None):
    if assignment is None:
        return None
    source_indices = assignment['atom_source_indices']
    written_order = (
        list(range(len(retained))) if written_order is None else list(written_order)
    )
    return {
        'schema_version': '1.0',
        'policy': 'retain_provider_polar_h_merge_provider_nonpolar_h',
        'selected_source_atom_indices': source_indices.copy(),
        'retained_selected_atom_indices': list(retained),
        'retained_source_atom_indices': [source_indices[i] for i in retained],
        'prepared_atom_types': list(labels),
        'pdbqt_atom_indices': written_order,
        'pdbqt_to_source_atom_indices': [
            source_indices[retained[i]] for i in written_order
        ],
    }


def type_remark(prepared):
    """Prevent changed labels from being exported with original attribution."""
    assignment = prepared.metadata.get('atom_type_assignment')
    projection = prepared.metadata.get('atom_type_projection')
    if assignment is None and projection is None:
        return []
    try:
        assignment, projection = json.loads(
            json.dumps([assignment, projection], allow_nan=False)
        )
    except (TypeError, ValueError) as exc:
        raise ArgumentError(
            arg_name='prepared', reason='Named type evidence must be finite JSON.'
        ) from exc
    if (
        not isinstance(assignment, dict)
        or assignment.get('schema') != 'molsysmt.atom_type_assignment@1'
        or assignment.get('status') not in ('assigned', 'projected')
        or assignment.get('typing_scheme') != 'autodock4'
        or assignment.get('coverage') != 'complete'
        or not isinstance(projection, dict)
        or projection.get('schema_version') != '1.0'
        or projection.get('policy')
        != 'retain_provider_polar_h_merge_provider_nonpolar_h'
        or not isinstance(projection.get('retained_source_atom_indices'), list)
        or len(projection['retained_source_atom_indices']) != prepared.n_atoms
        or not isinstance(projection.get('prepared_atom_types'), list)
        or len(projection['prepared_atom_types']) != prepared.n_atoms
        or not isinstance(assignment.get('software'), dict)
        or not isinstance(assignment.get('rule_version'), str)
        or not isinstance(assignment.get('method'), str)
        or type(assignment.get('n_atoms')) is not int
        or assignment['n_atoms'] < prepared.n_atoms
    ):
        raise ArgumentError(
            arg_name='prepared',
            reason='Named type evidence is incomplete or unsupported.',
        )
    selected = projection.get('selected_source_atom_indices')
    retained = projection.get('retained_selected_atom_indices')
    order = list(getattr(prepared, 'pdbqt_atom_indices', range(prepared.n_atoms)))
    if (
        not isinstance(selected, list)
        or selected != assignment.get('atom_source_indices')
        or any(
            type(i) is not int or not 0 <= i < assignment['n_atoms'] for i in selected
        )
        or not isinstance(retained, list)
        or len(retained) != prepared.n_atoms
        or any(type(i) is not int or not 0 <= i < len(selected) for i in retained)
        or len(set(retained)) != len(retained)
        or projection['retained_source_atom_indices'] != [selected[i] for i in retained]
        or sorted(order) != list(range(prepared.n_atoms))
        or projection.get('pdbqt_atom_indices') != order
        or projection.get('pdbqt_to_source_atom_indices')
        != [selected[retained[i]] for i in order]
    ):
        raise ArgumentError(
            arg_name='prepared',
            reason='Named type atom correspondence is incomplete or changed.',
        )
    if list(prepared.atom_types) != projection['prepared_atom_types']:
        raise ArgumentError(
            arg_name='prepared',
            reason='Prepared atom types no longer match their named assignment projection; prepare again with MolSysMT-assigned types.',
        )
    payload = {
        'typing_scheme': assignment['typing_scheme'],
        'rule_version': assignment['rule_version'],
        'software': assignment['software'],
        'evaluated_n_atoms': assignment['n_atoms'],
        'written_n_atoms': prepared.n_atoms,
        'source_status': assignment['status'],
        'hydrogen_policy': projection['policy'],
    }
    return [
        'REMARK DOCKINGMT_ATOM_TYPES '
        + json.dumps(payload, sort_keys=True, separators=(',', ':'))
    ]
