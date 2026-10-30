"""Probe current chemical-domain receiving without rewriting dated producers."""

import molsysmt as msm

from devtools.qualify_chemical_templates import record_digest, snapshot
from devtools.qualify_named_types import declared_source


def state_scope_probe():
    """Compare explicit assigned-state connectivity with the reference graph."""
    source = declared_source('CCCCCC')
    assigned = source.chemical_states.append_state()
    source.chemical_states._states[assigned].state_id = 'assigned-split'
    bonds = source.chemical_states.get_bonds().drop(index=2).reset_index(drop=True)
    source.chemical_states._set_chemical_state_bonds(bonds, state_index=assigned)
    source.chemical_states._states[assigned].connectivity_completeness = 'complete'
    source._set_structure_chemical_state_indices([assigned])
    before = record_digest(snapshot(source))
    assigned_fragments = msm.chemical_states.get_rigid_fragments(
        source, chemical_state='structure', structure_indices=0
    )
    reference_blocks = msm.chemical_states.get_covalent_blocks(source)
    assigned_blocks = msm.chemical_states.get_covalent_blocks(
        source, chemical_state='structure', structure_indices=0
    )
    assert assigned_fragments['fragment_offsets'].tolist() == [0, 3, 6]
    assert [sorted(block) for block in reference_blocks] == [list(range(6))]
    assert [sorted(block) for block in assigned_blocks] == [[0, 1, 2], [3, 4, 5]]
    assert record_digest(snapshot(source)) == before
    return {
        'owning_issue': 'uibcdf/molsysmt#348',
        'assigned_fragment_offsets': assigned_fragments['fragment_offsets'].tolist(),
        'reference_default_blocks': [sorted(block) for block in reference_blocks],
        'explicit_state_request': {
            'status': 'supported',
            'blocks': [sorted(block) for block in assigned_blocks],
        },
        'source_unchanged': True,
    }
