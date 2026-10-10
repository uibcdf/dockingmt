"""Retain the native energy matrix and actual wrapper defaults for replay."""

from functools import wraps

import numpy as np
import pyunitwizard as puw
from molecular_fixtures import named_181l_pair
from vina import Vina

import dockingmt as dmt


def test_native_fifth_energy_column_and_defaults_survive_serialization(monkeypatch):
    observed = []
    original = Vina.energies

    @wraps(original)
    def capture(self, *args, **kwargs):
        value = original(self, *args, **kwargs)
        observed.append(value.copy())
        return value

    monkeypatch.setattr(Vina, 'energies', capture)
    receptor, ligand = named_181l_pair()
    result = dmt.dock(
        dmt.DockingProblem(
            receptor,
            ligand,
            dmt.BoxRegion.from_points(
                ligand.coordinates, padding=puw.quantity(8, 'angstrom')
            ),
        ),
        dmt.VinaProtocol(cpu=1, seed=7, exhaustiveness=1, n_poses=3),
    )
    restored = dmt.DockingResult.from_dict(result.to_dict())
    native = restored.provenance['backend_output']
    assert len(observed) == 1
    assert np.asarray(native['energies']).shape == (len(result), 5)
    np.testing.assert_array_equal(native['energies'], observed[0])
    assert native['energy_columns'][-1] == 'intra_best_pose'
    assert native['energy_unit'] == 'kcal/mol'
    assert native['resolved_calls']['dock'] == {
        'exhaustiveness': 1,
        'n_poses': 3,
        'min_rmsd': 1.0,
        'max_evals': 0,
    }
    assert native['resolved_calls']['compute_vina_maps']['spacing'] == 0.375
    assert native['resolved_calls']['compute_vina_maps']['force_even_voxels'] is False
    assert native['engine_info']['box_spacing'] == 0.375
    for pose, vector in zip(result.poses, native['energies'], strict=True):
        assert list(pose.scores.values()) == vector[:4]
