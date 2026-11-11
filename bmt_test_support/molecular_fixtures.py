"""Finite shared test factories relocated from tests/molecular_fixtures.py at9375f3a8.

Test support only; original provider operations and fixture hypotheses are retained.
"""

from copy import deepcopy
from functools import lru_cache


@lru_cache(maxsize=1)
def _named_181l_pair():
    from bmt_test_support.qualify_181l_receptor import prepare_case

    receptor, ligand, _, _ = prepare_case()
    return receptor, ligand


def named_181l_pair():
    """Detach every test's mutable preparations from the shared fixture."""
    return deepcopy(_named_181l_pair())


def declared_methanol():
    """Six indexed atoms with an explicit CH4O hypothesis and no virtual H.

    This is a finite fixture declaration. Native SDF admission preserves absent
    virtual counts; production preparation must not infer these zeros.
    """
    from pathlib import Path

    import molsysmt as msm

    source = msm.convert(
        Path(__file__).resolve().parents[1] / 'tests/data/charges/methanol.sdf',
        to_form='molsysmt.MolSys',
    )
    msm.set(
        source,
        element='atom',
        n_explicit_hydrogens=0,
        n_implicit_hydrogens=0,
        allows_implicit_hydrogens=False,
    )
    return source
