"""Finite shared test factories relocated from tests/test_problem.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

import molsysmt as msm
import numpy as np
import pyunitwizard as puw


def _multi_structure_redocking_source():
    path = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    molsys = msm.convert(path, to_form='molsysmt.MolSys')
    msm.append_structures(molsys, msm.copy(molsys))
    coordinates = np.array(
        puw.get_value(
            msm.get(molsys, element='atom', coordinates=True), to_unit='angstrom'
        ),
        copy=True,
    )
    coordinates[1] += [20.0, 0.0, 0.0]
    molsys.structures.coordinates = puw.quantity(coordinates, 'angstrom')
    second_state = molsys.chemical_states.append_state()
    molsys.chemical_states._states[second_state].state_id = 'selected-second-state'
    molsys._set_structure_chemical_state_indices([0, second_state])
    return molsys, coordinates
