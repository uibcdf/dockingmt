"""Guard the search-domain exclusion used by the public 1IEP control."""

import numpy as np
import pytest
import pyunitwizard as puw

from devtools.validate_1iep_pdbqt import _displaced_control_box
from dockingmt import BoxRegion


def test_1iep_displaced_control_excludes_native_reference():
    reference_box = BoxRegion(
        center=puw.quantity([15.190, 53.903, 16.917], 'angstrom'),
        size=puw.quantity([20.0, 20.0, 20.0], 'angstrom'),
    )
    native_coordinates = np.array([[12.0, 54.0, 17.0], [20.0, 51.0, 19.0]])

    control = _displaced_control_box(reference_box, native_coordinates)

    assert control.to_backend_box('angstrom')['center'] == pytest.approx(
        (45.190, 53.903, 16.917)
    )
    assert all(
        not control.contains(puw.quantity(coordinate, 'angstrom'))
        for coordinate in native_coordinates
    )


def test_1iep_displaced_control_rejects_an_overlapping_reference():
    reference_box = BoxRegion(
        center=puw.quantity([15.190, 53.903, 16.917], 'angstrom'),
        size=puw.quantity([20.0, 20.0, 20.0], 'angstrom'),
    )

    with pytest.raises(ValueError, match='overlaps the native ligand'):
        _displaced_control_box(reference_box, np.array([[45.0, 54.0, 17.0]]))
