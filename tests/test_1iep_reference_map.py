"""Guard the source-atom correspondence used by the public 1IEP check."""

import numpy as np
import pytest

from devtools.validate_1iep_pdbqt import _source_atom_map


def test_1iep_reference_map_preserves_source_indices_across_pdbqt_reordering():
    source_coordinates = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    source_elements = ['N', 'C', 'H']
    pdbqt_records = [
        (('2', 'C2', 'C'), np.array([2.0, 0.0, 0.0])),
        (('1', 'N1', 'N'), np.array([0.0, 0.0, 0.0])),
    ]

    assert _source_atom_map(pdbqt_records, source_coordinates, source_elements) == [
        1,
        0,
    ]


def test_1iep_reference_map_rejects_ambiguous_and_reused_source_atoms():
    source_coordinates = np.array([[0.0, 0.0, 0.0], [0.01, 0.0, 0.0]])
    source_elements = ['C', 'C']
    atom = (('1', 'C1', 'C'), np.array([0.0, 0.0, 0.0]))

    with pytest.raises(ValueError, match='no unique source ligand atom'):
        _source_atom_map([atom], source_coordinates, source_elements)

    source_coordinates[1, 0] = 2.0
    with pytest.raises(ValueError, match='no unique source ligand atom'):
        _source_atom_map([atom, atom], source_coordinates, source_elements)
