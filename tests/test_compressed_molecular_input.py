"""Accept the frozen compressed source through MolSysMT's public input route."""

import gzip
import hashlib
from pathlib import Path

import molsysmt as msm
import numpy as np
import pyunitwizard as puw

import dockingmt as dmt

SOURCE = (
    Path(__file__).resolve().parents[1]
    / 'devguide/validation/data/3ptb_prospective/3PTB.pdb.gz'
)


def test_compressed_source_matches_plain_truth_and_public_docking_selection(tmp_path):
    raw = SOURCE.read_bytes()
    plain = gzip.decompress(raw)
    assert hashlib.sha256(plain).hexdigest() == (
        '288f7954d4d013fa8eab3808e1037e2958e2dcd12c9eca65a3f1014404a9f9a2'
    )
    control = tmp_path / 'original.pdb'
    control.write_bytes(plain)
    with puw.context(standard_units=['pm', 'fs']):
        compressed = msm.convert(
            SOURCE, to_form='molsysmt.MolSys', get_missing_bonds=False
        )
        reference = msm.convert(
            control, to_form='molsysmt.MolSys', get_missing_bonds=False
        )
        assert msm.get(
            compressed, n_atoms=True, n_groups=True, n_structures=True, n_bonds=True
        ) == [1701, 287, 1, 21]
        np.testing.assert_array_equal(
            puw.get_value(msm.get(compressed, coordinates=True), to_unit='angstrom'),
            puw.get_value(msm.get(reference, coordinates=True), to_unit='angstrom'),
        )
        for field in (
            'atom_id',
            'atom_name',
            'group_id',
            'chain_id',
            'bonded_atom_pairs',
        ):
            element = 'bond' if field == 'bonded_atom_pairs' else 'atom'
            assert msm.get(compressed, element=element, **{field: True}) == msm.get(
                reference, element=element, **{field: True}
            )
        problem = dmt.DockingProblem(
            compressed,
            compressed,
            search_domain=dmt.BoxRegion(
                puw.quantity([0, 0, 0], 'angstrom'),
                puw.quantity([20, 20, 20], 'angstrom'),
            ),
            receptor_selection="molecule_type=='protein'",
            partner_selection="group_name=='BEN'",
        )
        assert msm.get(problem.partner_molsys, n_atoms=True) == 9
        assert msm.get(problem.receptor_molsys, n_atoms=True) == 1629
    assert SOURCE.read_bytes() == raw
