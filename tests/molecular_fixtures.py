"""Finite declared molecular controls assembled through public MolSysMT tools.

The 181L controls reuse the qualified public workflow. HIE, charged termini and
the methanol virtual-H inventory are explicit fixture hypotheses, not generic
perception, normalization or molecular algorithms.
"""

from copy import deepcopy
from functools import lru_cache


@lru_cache(maxsize=1)
def _named_181l_pair():
    from devtools.qualify_181l_receptor import prepare_case

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
        Path(__file__).parent / 'data/charges/methanol.sdf', to_form='molsysmt.MolSys'
    )
    msm.set(
        source,
        element='atom',
        n_explicit_hydrogens=0,
        n_implicit_hydrogens=0,
        allows_implicit_hydrogens=False,
    )
    return source
